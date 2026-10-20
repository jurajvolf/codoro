import json
import secrets
from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone

from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase, Submission, QuizQuestion
from gamification.models import (
    RewardItem, RewardPurchase, DorosTransaction, ClassQuest, CoinDrop, Quest
)
from courses.services import generate_exercise_with_ai, translate_to_english, evaluate_python_code


def teacher_required(view_func):
    """Dekorátor vyžadujúci prihláseného používateľa s rolou TEACHER."""
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_teacher():
            messages.error(request, "Prístup povolený iba pre účet učiteľa.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ==============================================================================
# 1. HLAVNÝ PREHĽAD (DASHBOARD)
# ==============================================================================

@teacher_required
def teacher_dashboard(request):
    """Centrálny prehľad študentov, kupónov, odmien, tried a licencií."""
    students = User.objects.filter(role=User.Role.STUDENT).select_related('school_class').order_by('-xp')
    pending_coupons = RewardPurchase.objects.filter(status=RewardPurchase.Status.PENDING).select_related('student', 'reward')
    rewards = RewardItem.objects.all().order_by('-id')
    recent_submissions = Submission.objects.select_related('student', 'exercise')[:30]
    modules = Module.objects.annotate(
        lesson_count=Count('lessons', distinct=True),
        exercise_count=Count('lessons__exercises', distinct=True)
    ).order_by('order')
    lessons = Lesson.objects.select_related('module').all().order_by('module__order', 'order')
    classes = SchoolClass.objects.select_related('teacher').annotate(student_count=Count('students')).prefetch_related('students').order_by('name')
    licenses = SubscriptionLicense.objects.all().order_by('-created_at')
    active_drops = CoinDrop.objects.order_by('-available_from')[:10]
    all_quests = Quest.objects.all().order_by('period', '-id')
    class_quests = ClassQuest.objects.select_related('school_class').order_by('-deadline')[:10]
    batch_created_students = request.session.pop('batch_created_students', None)

    return render(request, 'teacher_panel/dashboard.html', {
        'students': students,
        'pending_coupons': pending_coupons,
        'rewards': rewards,
        'recent_submissions': recent_submissions,
        'modules': modules,
        'lessons': lessons,
        'classes': classes,
        'licenses': licenses,
        'active_drops': active_drops,
        'all_quests': all_quests,
        'class_quests': class_quests,
        'batch_created_students': batch_created_students,
    })


# ==============================================================================
# 2. SPRÁVA VZDELÁVACÍCH MODULOV (CRUD PRE MODULE)
# ==============================================================================

@teacher_required
def cms_modules(request):
    """Zoznam a správa vzdelávacích modulov Codoro."""
    modules = Module.objects.annotate(
        lesson_count=Count('lessons', distinct=True),
        exercise_count=Count('lessons__exercises', distinct=True)
    ).prefetch_related('lessons__exercises', 'lessons__quiz_questions').order_by('order')

    total_hours = sum(m.estimated_hours for m in modules)
    total_lessons = sum(m.lesson_count for m in modules)
    total_exercises = sum(m.exercise_count for m in modules)

    return render(request, 'teacher_panel/cms_modules.html', {
        'modules': modules,
        'total_hours': total_hours,
        'total_lessons': total_lessons,
        'total_exercises': total_exercises,
    })


@teacher_required
def cms_module_create(request):
    """Vytvorenie nového vzdelávacieho modulu."""
    if request.method == 'POST':
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        desc_sk = request.POST.get('description_sk', '').strip()
        desc_en = request.POST.get('description_en', '').strip() or desc_sk
        lang = request.POST.get('programming_language', 'python')
        hours = int(request.POST.get('estimated_hours', 10))
        difficulty = request.POST.get('difficulty_level', 'BEGINNER')
        is_pro = request.POST.get('is_pro_only') == 'on'
        is_published = request.POST.get('is_published') == 'on'
        icon = request.POST.get('icon_name', 'bi-terminal').strip() or 'bi-terminal'

        next_order = (Module.objects.order_by('-order').values_list('order', flat=True).first() or 0) + 1

        module = Module.objects.create(
            title_sk=title_sk,
            title_en=title_en,
            description_sk=desc_sk,
            description_en=desc_en,
            programming_language=lang,
            order=next_order,
            estimated_hours=hours,
            difficulty_level=difficulty,
            is_pro_only=is_pro,
            is_published=is_published,
            icon_name=icon
        )
        messages.success(request, f"Modul '{module.title_sk}' bol úspešne vytvorený.")
    return redirect('cms_modules')


@teacher_required
def cms_module_edit(request, module_id):
    """Úprava existujúceho modulu."""
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        module.title_sk = request.POST.get('title_sk', '').strip() or module.title_sk
        module.title_en = request.POST.get('title_en', '').strip() or module.title_en
        module.description_sk = request.POST.get('description_sk', '').strip()
        module.description_en = request.POST.get('description_en', '').strip() or module.description_sk
        module.programming_language = request.POST.get('programming_language', module.programming_language)
        module.estimated_hours = int(request.POST.get('estimated_hours', module.estimated_hours))
        module.difficulty_level = request.POST.get('difficulty_level', module.difficulty_level)
        module.icon_name = request.POST.get('icon_name', module.icon_name).strip() or 'bi-terminal'
        module.is_pro_only = request.POST.get('is_pro_only') == 'on'
        module.is_published = request.POST.get('is_published') == 'on'
        module.save()
        messages.success(request, f"Modul '{module.title_sk}' bol aktualizovaný.")
        return redirect('cms_modules')

    return render(request, 'teacher_panel/cms_module_edit.html', {'module': module})


@teacher_required
def cms_module_delete(request, module_id):
    """Vymazanie modulu a jeho lekcií/cvičení s potvrdením."""
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        title = module.title_sk
        module.delete()
        messages.success(request, f"Modul '{title}' a všetky jeho lekcie boli vymazané.")
    return redirect('cms_modules')


@teacher_required
def cms_module_reorder(request, module_id, direction):
    """Zmena poradia modulu nahor (up) alebo nadol (down)."""
    module = get_object_or_404(Module, id=module_id)
    all_modules = list(Module.objects.order_by('order', 'id'))
    try:
        idx = all_modules.index(module)
    except ValueError:
        return redirect('cms_modules')

    if direction == 'up' and idx > 0:
        other = all_modules[idx - 1]
        module.order, other.order = other.order, module.order
        module.save(update_fields=['order'])
        other.save(update_fields=['order'])
        messages.success(request, f"Modul '{module.title_sk}' bol posunutý nahor.")
    elif direction == 'down' and idx < len(all_modules) - 1:
        other = all_modules[idx + 1]
        module.order, other.order = other.order, module.order
        module.save(update_fields=['order'])
        other.save(update_fields=['order'])
        messages.success(request, f"Modul '{module.title_sk}' bol posunutý nadol.")

    return redirect('cms_modules')


@teacher_required
def cms_module_toggle_pro(request, module_id):
    """Jedným klikom prepne modul medzi FREE a PRO/EDU."""
    module = get_object_or_404(Module, id=module_id)
    module.is_pro_only = not module.is_pro_only
    module.save(update_fields=['is_pro_only'])
    status = "PRO/EDU" if module.is_pro_only else "FREE"
    messages.success(request, f"Modul '{module.title_sk}' je teraz označený ako {status}.")
    return redirect('cms_modules')


@teacher_required
def cms_module_toggle_publish(request, module_id):
    """Prepnutie stavu publikovania (Publikovaný <-> Skrytý)."""
    module = get_object_or_404(Module, id=module_id)
    module.is_published = not module.is_published
    module.save(update_fields=['is_published'])
    status = "publikovaný" if module.is_published else "skrytý"
    messages.success(request, f"Modul '{module.title_sk}' je teraz {status}.")
    return redirect('cms_modules')


# ==============================================================================
# 3. SPRÁVA LEKCIÍ A MARKDOWN EDITOR SO ŽIVÝM NÁHĽADOM (CRUD PRE LESSON)
# ==============================================================================

@teacher_required
def cms_lesson_create(request, module_id):
    """Vytvorenie novej lekcie v danom module."""
    module = get_object_or_404(Module, id=module_id)
    if request.method == 'POST':
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        summary_sk = request.POST.get('summary_sk', '').strip()
        summary_en = request.POST.get('summary_en', '').strip() or summary_sk
        content_sk = request.POST.get('content_sk', '### Úvod do lekcie\n\nNapíš výklad sem.').strip()
        content_en = request.POST.get('content_en', '### Introduction\n\nWrite explanation here.').strip()
        minutes = int(request.POST.get('estimated_minutes', 45))
        xp = int(request.POST.get('xp_reward', 25))
        is_published = request.POST.get('is_published') == 'on'

        next_order = (module.lessons.order_by('-order').values_list('order', flat=True).first() or 0) + 1

        lesson = Lesson.objects.create(
            module=module,
            title_sk=title_sk,
            title_en=title_en,
            summary_sk=summary_sk,
            summary_en=summary_en,
            content_sk=content_sk,
            content_en=content_en,
            estimated_minutes=minutes,
            xp_reward=xp,
            order=next_order,
            is_published=is_published,
        )
        messages.success(request, f"Lekcia '{lesson.title_sk}' bola vytvorená.")
        return redirect('cms_lesson_edit', lesson_id=lesson.id)

    return render(request, 'teacher_panel/cms_lesson_form.html', {
        'module': module,
        'lesson': None,
        'is_new': True,
        'modules': Module.objects.order_by('order'),
    })


@teacher_required
def cms_lesson_edit(request, lesson_id):
    """Dvojstĺpcový Markdown editor so živým náhľadom marked.js pre lekciu."""
    lesson = get_object_or_404(Lesson.objects.select_related('module'), id=lesson_id)
    if request.method == 'POST':
        action = request.POST.get('action', 'save_lesson')
        if action == 'save_lesson':
            lesson.title_sk = request.POST.get('title_sk', '').strip() or lesson.title_sk
            lesson.title_en = request.POST.get('title_en', '').strip() or lesson.title_en
            lesson.summary_sk = request.POST.get('summary_sk', '').strip()
            lesson.summary_en = request.POST.get('summary_en', '').strip() or lesson.summary_sk
            lesson.content_sk = request.POST.get('content_sk', '').strip()
            lesson.content_en = request.POST.get('content_en', '').strip() or lesson.content_sk
            lesson.estimated_minutes = int(request.POST.get('estimated_minutes', lesson.estimated_minutes))
            lesson.xp_reward = int(request.POST.get('xp_reward', lesson.xp_reward))
            lesson.order = int(request.POST.get('order', lesson.order))
            lesson.is_published = request.POST.get('is_published') == 'on'

            new_module_id = request.POST.get('module_id')
            if new_module_id and str(new_module_id) != str(lesson.module_id):
                lesson.module = get_object_or_404(Module, id=new_module_id)

            lesson.save()
            messages.success(request, f"Lekcia '{lesson.title_sk}' bola úspešne uložená.")
            return redirect('cms_lesson_edit', lesson_id=lesson.id)

    quizzes = lesson.quiz_questions.all().order_by('order', 'id')
    exercises = lesson.exercises.all().prefetch_related('test_cases').order_by('order', 'id')
    modules = Module.objects.order_by('order')

    return render(request, 'teacher_panel/cms_lesson_form.html', {
        'lesson': lesson,
        'module': lesson.module,
        'quizzes': quizzes,
        'exercises': exercises,
        'modules': modules,
        'is_new': False,
    })


@teacher_required
def cms_lesson_delete(request, lesson_id):
    """Vymazanie lekcie a jej cvičení."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        title = lesson.title_sk
        module_id = lesson.module_id
        lesson.delete()
        messages.success(request, f"Lekcia '{title}' bola vymazaná.")
        return redirect('cms_modules')
    return redirect('cms_lesson_edit', lesson_id=lesson_id)


@teacher_required
def cms_lesson_duplicate(request, lesson_id):
    """Duplikuje lekciu vrátane jej kvízov a cvičení."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    next_order = (lesson.module.lessons.order_by('-order').values_list('order', flat=True).first() or 0) + 1

    with transaction.atomic():
        new_lesson = Lesson.objects.create(
            module=lesson.module,
            title_sk=f"{lesson.title_sk} (Kópia)",
            title_en=f"{lesson.title_en} (Copy)",
            summary_sk=lesson.summary_sk,
            summary_en=lesson.summary_en,
            content_sk=lesson.content_sk,
            content_en=lesson.content_en,
            estimated_minutes=lesson.estimated_minutes,
            xp_reward=lesson.xp_reward,
            order=next_order,
            is_published=False,
        )
        for q in lesson.quiz_questions.all():
            QuizQuestion.objects.create(
                lesson=new_lesson,
                question_sk=q.question_sk,
                question_en=q.question_en,
                option_a_sk=q.option_a_sk,
                option_a_en=q.option_a_en,
                option_b_sk=q.option_b_sk,
                option_b_en=q.option_b_en,
                option_c_sk=q.option_c_sk,
                option_c_en=q.option_c_en,
                option_d_sk=q.option_d_sk,
                option_d_en=q.option_d_en,
                correct_option=q.correct_option,
                explanation_sk=q.explanation_sk,
                explanation_en=q.explanation_en,
                order=q.order,
            )
        for ex in lesson.exercises.all():
            new_ex = Exercise.objects.create(
                lesson=new_lesson,
                title_sk=ex.title_sk,
                title_en=ex.title_en,
                instructions_sk=ex.instructions_sk,
                instructions_en=ex.instructions_en,
                starter_code=ex.starter_code,
                solution_code=ex.solution_code,
                explanation_sk=ex.explanation_sk,
                explanation_en=ex.explanation_en,
                hint_sk=ex.hint_sk,
                hint_en=ex.hint_en,
                hint_cost_doros=ex.hint_cost_doros,
                difficulty=ex.difficulty,
                xp_reward=ex.xp_reward,
                doros_reward=ex.doros_reward,
                order=ex.order,
            )
            for tc in ex.test_cases.all():
                TestCase.objects.create(
                    exercise=new_ex,
                    input_data=tc.input_data,
                    expected_output=tc.expected_output,
                    test_code=tc.test_code,
                    is_hidden=tc.is_hidden,
                    order=tc.order,
                )

    messages.success(request, f"Lekcia bola zduplikovaná ako '{new_lesson.title_sk}'.")
    return redirect('cms_lesson_edit', lesson_id=new_lesson.id)


# ==============================================================================
# 4. SPRÁVA KVÍZOVÝCH OTÁZOK (CRUD PRE QUIZQUESTION)
# ==============================================================================

@teacher_required
def cms_quiz_create(request, lesson_id):
    """Pridanie novej kvízovej otázky do lekcie."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        q_sk = request.POST.get('question_sk', '').strip()
        q_en = request.POST.get('question_en', '').strip() or q_sk
        a_sk = request.POST.get('option_a_sk', '').strip()
        a_en = request.POST.get('option_a_en', '').strip() or a_sk
        b_sk = request.POST.get('option_b_sk', '').strip()
        b_en = request.POST.get('option_b_en', '').strip() or b_sk
        c_sk = request.POST.get('option_c_sk', '').strip()
        c_en = request.POST.get('option_c_en', '').strip() or c_sk
        d_sk = request.POST.get('option_d_sk', '').strip()
        d_en = request.POST.get('option_d_en', '').strip() or d_sk
        correct = request.POST.get('correct_option', 'A')
        exp_sk = request.POST.get('explanation_sk', '').strip()
        exp_en = request.POST.get('explanation_en', '').strip() or exp_sk

        next_order = (lesson.quiz_questions.order_by('-order').values_list('order', flat=True).first() or 0) + 1

        QuizQuestion.objects.create(
            lesson=lesson,
            question_sk=q_sk,
            question_en=q_en,
            option_a_sk=a_sk,
            option_a_en=a_en,
            option_b_sk=b_sk,
            option_b_en=b_en,
            option_c_sk=c_sk,
            option_c_en=c_en,
            option_d_sk=d_sk,
            option_d_en=d_en,
            correct_option=correct,
            explanation_sk=exp_sk,
            explanation_en=exp_en,
            order=next_order,
        )
        messages.success(request, "Kvízová otázka bola úspešne pridaná.")
    return redirect('cms_lesson_edit', lesson_id=lesson_id)


@teacher_required
def cms_quiz_edit(request, quiz_id):
    """Úprava existujúcej kvízovej otázky."""
    quiz = get_object_or_404(QuizQuestion, id=quiz_id)
    if request.method == 'POST':
        quiz.question_sk = request.POST.get('question_sk', quiz.question_sk).strip()
        quiz.question_en = request.POST.get('question_en', quiz.question_en).strip()
        quiz.option_a_sk = request.POST.get('option_a_sk', quiz.option_a_sk).strip()
        quiz.option_a_en = request.POST.get('option_a_en', quiz.option_a_en).strip()
        quiz.option_b_sk = request.POST.get('option_b_sk', quiz.option_b_sk).strip()
        quiz.option_b_en = request.POST.get('option_b_en', quiz.option_b_en).strip()
        quiz.option_c_sk = request.POST.get('option_c_sk', quiz.option_c_sk).strip()
        quiz.option_c_en = request.POST.get('option_c_en', quiz.option_c_en).strip()
        quiz.option_d_sk = request.POST.get('option_d_sk', '').strip()
        quiz.option_d_en = request.POST.get('option_d_en', '').strip()
        quiz.correct_option = request.POST.get('correct_option', quiz.correct_option)
        quiz.explanation_sk = request.POST.get('explanation_sk', '').strip()
        quiz.explanation_en = request.POST.get('explanation_en', '').strip()
        quiz.save()
        messages.success(request, "Kvízová otázka bola upravená.")
    return redirect('cms_lesson_edit', lesson_id=quiz.lesson_id)


@teacher_required
def cms_quiz_delete(request, quiz_id):
    """Vymazanie kvízovej otázky."""
    quiz = get_object_or_404(QuizQuestion, id=quiz_id)
    lesson_id = quiz.lesson_id
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, "Kvízová otázka bola vymazaná.")
    return redirect('cms_lesson_edit', lesson_id=lesson_id)


# ==============================================================================
# 5. SPRÁVA CVIČENÍ A TESTOVACÍCH PRÍPADOV (CRUD PRE EXERCISE + TESTCASE)
# ==============================================================================

@teacher_required
def cms_exercise_create(request, lesson_id):
    """Vytvorenie nového cvičenia v lekcii a presmerovanie do CodeMirror editora."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        instructions_sk = request.POST.get('instructions_sk', 'Zadanie úlohy...').strip()
        instructions_en = request.POST.get('instructions_en', instructions_sk).strip()
        starter_code = request.POST.get('starter_code', '# Napíš svoj kód sem\n')
        solution_code = request.POST.get('solution_code', starter_code)
        difficulty = request.POST.get('difficulty', Exercise.Difficulty.EASY)
        xp_reward = int(request.POST.get('xp_reward', 50))
        doros_reward = int(request.POST.get('doros_reward', 25))

        next_order = (lesson.exercises.order_by('-order').values_list('order', flat=True).first() or 0) + 1

        ex = Exercise.objects.create(
            lesson=lesson,
            title_sk=title_sk,
            title_en=title_en,
            instructions_sk=instructions_sk,
            instructions_en=instructions_en,
            starter_code=starter_code,
            solution_code=solution_code,
            difficulty=difficulty,
            xp_reward=xp_reward,
            doros_reward=doros_reward,
            order=next_order,
        )
        test_code = request.POST.get('test_code', '').strip()
        if test_code:
            TestCase.objects.create(
                exercise=ex,
                input_data=request.POST.get('input_data', 'Základný test'),
                expected_output='True',
                test_code=test_code,
                is_hidden=False,
                order=1
            )
        messages.success(request, f"Cvičenie '{ex.title_sk}' bolo vytvorené.")
        return redirect('cms_exercise_edit', exercise_id=ex.id)

    return render(request, 'teacher_panel/cms_exercise_form.html', {
        'lesson': lesson,
        'exercise': None,
        'is_new': True,
        'lessons': Lesson.objects.select_related('module').order_by('module__order', 'order'),
    })


@teacher_required
def cms_exercise_edit(request, exercise_id):
    """CodeMirror editor cvičenia, vzorového riešenia, TestCase testov a AI asistent."""
    exercise = get_object_or_404(Exercise.objects.select_related('lesson__module'), id=exercise_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_exercise':
            exercise.title_sk = request.POST.get('title_sk', '').strip() or exercise.title_sk
            exercise.title_en = request.POST.get('title_en', '').strip() or exercise.title_en
            exercise.instructions_sk = request.POST.get('instructions_sk', '').strip()
            exercise.instructions_en = request.POST.get('instructions_en', '').strip() or exercise.instructions_sk
            exercise.starter_code = request.POST.get('starter_code', exercise.starter_code)
            exercise.solution_code = request.POST.get('solution_code', exercise.solution_code)
            exercise.explanation_sk = request.POST.get('explanation_sk', '').strip()
            exercise.explanation_en = request.POST.get('explanation_en', '').strip() or exercise.explanation_sk
            exercise.hint_sk = request.POST.get('hint_sk', '').strip()
            exercise.hint_en = request.POST.get('hint_en', '').strip() or exercise.hint_sk
            exercise.hint_cost_doros = int(request.POST.get('hint_cost_doros', exercise.hint_cost_doros))
            exercise.difficulty = request.POST.get('difficulty', exercise.difficulty)
            exercise.xp_reward = int(request.POST.get('xp_reward', exercise.xp_reward))
            exercise.doros_reward = int(request.POST.get('doros_reward', exercise.doros_reward))
            exercise.order = int(request.POST.get('order', exercise.order))

            new_lesson_id = request.POST.get('lesson_id')
            if new_lesson_id and str(new_lesson_id) != str(exercise.lesson_id):
                exercise.lesson = get_object_or_404(Lesson, id=new_lesson_id)

            exercise.save()
            messages.success(request, f"Cvičenie '{exercise.title_sk}' bolo úspešne uložené.")
            return redirect('cms_exercise_edit', exercise_id=exercise.id)

    test_cases = exercise.test_cases.all().order_by('order', 'id')
    lessons = Lesson.objects.select_related('module').order_by('module__order', 'order')

    return render(request, 'teacher_panel/cms_exercise_form.html', {
        'exercise': exercise,
        'lesson': exercise.lesson,
        'test_cases': test_cases,
        'lessons': lessons,
        'is_new': False,
    })


@teacher_required
def cms_exercise_delete(request, exercise_id):
    """Vymazanie cvičenia."""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    lesson_id = exercise.lesson_id
    if request.method == 'POST':
        title = exercise.title_sk
        exercise.delete()
        messages.success(request, f"Cvičenie '{title}' bolo vymazané.")
    return redirect('cms_lesson_edit', lesson_id=lesson_id)


@teacher_required
def cms_testcase_create(request, exercise_id):
    """Pridanie nového TestCase prípadu k cvičeniu."""
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        input_data = request.POST.get('input_data', '').strip()
        expected = request.POST.get('expected_output', '').strip() or 'OK'
        test_code = request.POST.get('test_code', '').strip()
        is_hidden = request.POST.get('is_hidden') == 'on'

        next_order = (exercise.test_cases.order_by('-order').values_list('order', flat=True).first() or 0) + 1

        TestCase.objects.create(
            exercise=exercise,
            input_data=input_data,
            expected_output=expected,
            test_code=test_code,
            is_hidden=is_hidden,
            order=next_order,
        )
        messages.success(request, "Nový testovací prípad (TestCase) bol pridaný.")
    return redirect('cms_exercise_edit', exercise_id=exercise_id)


@teacher_required
def cms_testcase_edit(request, testcase_id):
    """Úprava existujúceho testovacieho prípadu."""
    tc = get_object_or_404(TestCase, id=testcase_id)
    if request.method == 'POST':
        tc.input_data = request.POST.get('input_data', tc.input_data).strip()
        tc.expected_output = request.POST.get('expected_output', tc.expected_output).strip()
        tc.test_code = request.POST.get('test_code', tc.test_code).strip()
        tc.is_hidden = request.POST.get('is_hidden') == 'on'
        tc.order = int(request.POST.get('order', tc.order))
        tc.save()
        messages.success(request, "Testovací prípad bol upravený.")
    return redirect('cms_exercise_edit', exercise_id=tc.exercise_id)


@teacher_required
def cms_testcase_delete(request, testcase_id):
    """Vymazanie testovacieho prípadu."""
    tc = get_object_or_404(TestCase, id=testcase_id)
    exercise_id = tc.exercise_id
    if request.method == 'POST':
        tc.delete()
        messages.success(request, "Testovací prípad bol vymazaný.")
    return redirect('cms_exercise_edit', exercise_id=exercise_id)


@teacher_required
def cms_test_solution(request):
    """
    AJAX endpoint: Overí vzorové riešenie učiteľa voči zadaným testom v AST sandboxe.
    Učiteľ hneď vidí, či jeho solution_code funguje a aký je presný výstup.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("POST required")

    solution_code = request.POST.get('solution_code', '')
    exercise_id = request.POST.get('exercise_id')
    raw_tests = request.POST.get('tests_json') or request.POST.get('custom_test_cases')

    custom_tests = None
    exercise = None

    if raw_tests:
        try:
            parsed = json.loads(raw_tests)
            if isinstance(parsed, list):
                custom_tests = [
                    {
                        'test_code': t.get('test_code', ''),
                        'input_data': t.get('input_data', ''),
                        'is_hidden': t.get('is_hidden', False),
                    }
                    for t in parsed if t.get('test_code')
                ]
        except (ValueError, TypeError):
            pass

    if exercise_id:
        exercise = get_object_or_404(Exercise, id=exercise_id)

    eval_result = evaluate_python_code(
        exercise=exercise,
        student_code=solution_code,
        lang=request.user.preferred_language,
        custom_test_cases=custom_tests
    )
    passed, status, log = eval_result
    exec_ms = getattr(eval_result, 'execution_time_ms', 0)

    return JsonResponse({
        'success': True,
        'passed': passed,
        'status': status,
        'output_log': log,
        'execution_time_ms': exec_ms,
    })


# ==============================================================================
# 6. SPRÁVA OBCHODU A SKLADOVÝCH ZÁSOB (CRUD PRE REWARDITEM)
# ==============================================================================

@teacher_required
def cms_reward_edit(request, reward_id):
    """Úprava existujúcej položky obchodu."""
    reward = get_object_or_404(RewardItem, id=reward_id)
    if request.method == 'POST':
        reward.title_sk = request.POST.get('title_sk', reward.title_sk).strip()
        reward.title_en = request.POST.get('title_en', reward.title_en).strip() or reward.title_sk
        reward.description_sk = request.POST.get('description_sk', reward.description_sk).strip()
        reward.description_en = request.POST.get('description_en', reward.description_en).strip() or reward.description_sk
        reward.cost_doros = int(request.POST.get('cost_doros', reward.cost_doros))
        reward.max_stock = int(request.POST.get('max_stock', reward.max_stock))
        reward.current_stock = min(reward.current_stock, reward.max_stock)
        reward.restock_period = request.POST.get('restock_period', reward.restock_period)
        reward.limit_per_student_per_period = int(request.POST.get('limit_per_student', reward.limit_per_student_per_period))
        reward.is_active = request.POST.get('is_active') == 'on'
        reward.save()
        messages.success(request, f"Odmena '{reward.title_sk}' bola upravená.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_reward_restock(request, reward_id):
    """Okamžite doplní skladové zásoby danej odmeny na maximum (Restock Now)."""
    reward = get_object_or_404(RewardItem, id=reward_id)
    if request.method == 'POST':
        reward.current_stock = reward.max_stock
        reward.last_restocked_at = timezone.now()
        reward.save(update_fields=['current_stock', 'last_restocked_at'])
        messages.success(request, f"Zásoby odmeny '{reward.title_sk}' boli doplnené na maximum ({reward.max_stock} ks).")
    return redirect('teacher_dashboard')


@teacher_required
def cms_reward_toggle_active(request, reward_id):
    """Pozastaví alebo aktivuje odmenu v obchode."""
    reward = get_object_or_404(RewardItem, id=reward_id)
    reward.is_active = not reward.is_active
    reward.save(update_fields=['is_active'])
    status = "aktivovaná" if reward.is_active else "pozastavená"
    messages.success(request, f"Odmena '{reward.title_sk}' je teraz v obchode {status}.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_reward_delete(request, reward_id):
    """Vymazanie odmeny z obchodu."""
    reward = get_object_or_404(RewardItem, id=reward_id)
    if request.method == 'POST':
        title = reward.title_sk
        reward.delete()
        messages.success(request, f"Odmena '{title}' bola vymazaná z obchodu.")
    return redirect('teacher_dashboard')


# ==============================================================================
# 7. SPRÁVA QUESTOV A MANUÁLNE VYHODNOTENIE
# ==============================================================================

@teacher_required
def cms_quest_edit(request, quest_id):
    """Úprava osobného questu."""
    q = get_object_or_404(Quest, id=quest_id)
    if request.method == 'POST':
        q.title_sk = request.POST.get('title_sk', q.title_sk).strip()
        q.title_en = request.POST.get('title_en', q.title_en).strip() or q.title_sk
        q.target_value = int(request.POST.get('target_value', q.target_value))
        q.reward_doros = int(request.POST.get('reward_doros', q.reward_doros))
        q.reward_xp = int(request.POST.get('reward_xp', q.reward_xp))
        q.is_active = request.POST.get('is_active') == 'on'
        q.save()
        messages.success(request, f"Výzva '{q.title_sk}' bola upravená.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_quest_delete(request, quest_id):
    """Vymazanie osobného questu."""
    q = get_object_or_404(Quest, id=quest_id)
    if request.method == 'POST':
        title = q.title_sk
        q.delete()
        messages.success(request, f"Výzva '{title}' bola vymazaná.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_classquest_edit(request, class_quest_id):
    """Úprava kolektívneho triedneho questu."""
    cq = get_object_or_404(ClassQuest, id=class_quest_id)
    if request.method == 'POST':
        cq.title_sk = request.POST.get('title_sk', cq.title_sk).strip()
        cq.title_en = request.POST.get('title_en', cq.title_en).strip() or cq.title_sk
        cq.target_exercises_count = int(request.POST.get('target_exercises_count', cq.target_exercises_count))
        cq.reward_doros_per_student = int(request.POST.get('reward_doros_per_student', cq.reward_doros_per_student))
        cq.min_contribution_required = int(request.POST.get('min_contribution_required', cq.min_contribution_required))
        cq.save()
        messages.success(request, f"Triedna výzva '{cq.title_sk}' bola upravená.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_classquest_delete(request, class_quest_id):
    """Vymazanie kolektívnej triednej výzvy."""
    cq = get_object_or_404(ClassQuest, id=class_quest_id)
    if request.method == 'POST':
        title = cq.title_sk
        cq.delete()
        messages.success(request, f"Triedna výzva '{title}' bola vymazaná.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_classquest_distribute(request, class_quest_id):
    """Tlačidlo manuálneho vyhodnotenia a rozdelenia mincí Doros triede."""
    cq = get_object_or_404(ClassQuest, id=class_quest_id)
    if request.method == 'POST':
        if cq.rewards_distributed:
            messages.info(request, f"Odmeny za výzvu '{cq.title_sk}' už boli rozdelené skôr.")
        else:
            rewarded_count = cq.distribute_rewards()
            messages.success(request, f"Triedna výzva '{cq.title_sk}' bola vyhodnotená! {rewarded_count} študentov získalo po +{cq.reward_doros_per_student} Doros.")
    return redirect('teacher_dashboard')


# ==============================================================================
# 8. TRIEDY, LICENCIE A DETAILNÝ PROFIL ŠTUDENTA
# ==============================================================================

@teacher_required
def cms_class_create(request):
    """Vytvorenie novej školskej triedy s unikátnym kódom."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        join_code = request.POST.get('join_code', '').strip().upper()
        if not join_code:
            join_code = f"{name.replace('.', '').replace(' ', '').upper()}-{timezone.now().year}"

        if SchoolClass.objects.filter(join_code=join_code).exists():
            messages.error(request, f"Kód triedy '{join_code}' už existuje. Zvoľ iný kód.")
            return redirect('teacher_dashboard')

        sc = SchoolClass.objects.create(name=name, join_code=join_code, teacher=request.user)
        messages.success(request, f"Trieda '{sc.name}' s prihlasovacím kódom '{sc.join_code}' bola vytvorená.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_class_delete(request, class_id):
    """Zmazanie školskej triedy (žiaci zostanú v systéme, len sa odhlásia z triedy)."""
    sc = get_object_or_404(SchoolClass, id=class_id)
    if sc.teacher != request.user and not request.user.is_admin():
        messages.error(request, "Nemáte oprávnenie zmazať túto triedu.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        name = sc.name
        User.objects.filter(school_class=sc).update(school_class=None)
        sc.delete()
        messages.success(request, f"Trieda '{name}' bola vymazaná. Žiaci boli odhlásení z triedy.")
    return redirect('teacher_dashboard')


@teacher_required
@transaction.atomic
def cms_class_batch_students(request, class_id):
    """
    Hromadné vytvorenie študentských účtov pre triedu zo zoznamu mien.
    Učiteľ zadá zoznam mien (1 na riadok) a systém automaticky vygeneruje študentské účty.
    """
    import unicodedata
    import re
    sc = get_object_or_404(SchoolClass, id=class_id)
    if sc.teacher != request.user and not request.user.is_admin():
        messages.error(request, "Nemáte oprávnenie spravovať túto triedu.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        raw_names = request.POST.get('student_names', '').strip()
        default_pwd = request.POST.get('default_password', '').strip() or 'Codoro2027!'
        lines = [line.strip() for line in raw_names.split('\n') if line.strip()]

        if not lines:
            messages.warning(request, "Nezadali ste žiadne mená žiakov.")
            return redirect('teacher_dashboard')

        created_students = []
        for full_name in lines:
            parts = full_name.split(None, 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

            # Vyčistenie diakritiky pre login
            clean_first = unicodedata.normalize('NFKD', first_name).encode('ASCII', 'ignore').decode('utf-8').lower()
            clean_last = unicodedata.normalize('NFKD', last_name).encode('ASCII', 'ignore').decode('utf-8').lower()
            clean_first = re.sub(r'[^a-z0-9]', '', clean_first)
            clean_last = re.sub(r'[^a-z0-9]', '', clean_last)

            base_username = f"{clean_first}_{clean_last}" if clean_last else clean_first
            base_username = base_username[:20] or "student"

            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"
                counter += 1

            email = f"{username}@{sc.join_code.lower()}.codoro.local"
            User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=default_pwd,
                role=User.Role.STUDENT,
                school_class=sc,
                subscription_tier=User.SubscriptionTier.EDU,
                doros=100
            )
            created_students.append({
                'full_name': full_name,
                'username': username,
                'password': default_pwd,
                'class_name': sc.name,
                'join_code': sc.join_code,
            })

        request.session['batch_created_students'] = created_students
        messages.success(request, f"Úspešne vytvorených {len(created_students)} študentských účtov pre triedu {sc.name}.")

    return redirect('teacher_dashboard')


@teacher_required
def cms_class_remove_student(request, class_id, student_id):
    """Odstránenie žiaka z triedy."""
    sc = get_object_or_404(SchoolClass, id=class_id)
    if sc.teacher != request.user and not request.user.is_admin():
        messages.error(request, "Nemáte oprávnenie spravovať túto triedu.")
        return redirect('teacher_dashboard')

    student = get_object_or_404(User, id=student_id, school_class=sc)
    if request.method == 'POST':
        student.school_class = None
        student.save(update_fields=['school_class'])
        messages.info(request, f"Študent {student.username} bol odhlásený z triedy {sc.name}.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_license_create(request):
    """Generovanie nového licenčného kľúča pre EDU alebo PRO predplatné."""
    if request.method == 'POST':
        tier = request.POST.get('tier', User.SubscriptionTier.EDU)
        max_uses = int(request.POST.get('max_uses', 30))
        code = request.POST.get('code', '').strip().upper()

        if not code:
            suffix = secrets.token_hex(3).upper()
            code = f"{tier}-{timezone.now().year}-{suffix}"

        if SubscriptionLicense.objects.filter(code=code).exists():
            messages.error(request, f"Licenčný kód '{code}' už existuje.")
            return redirect('teacher_dashboard')

        lic = SubscriptionLicense.objects.create(code=code, tier=tier, max_uses=max_uses, is_active=True)
        messages.success(request, f"Licenčný kľúč '{lic.code}' ({tier}, {max_uses} použití) bol vygenerovaný.")
    return redirect('teacher_dashboard')


@teacher_required
def cms_student_assign_class(request, student_id):
    """Priradenie alebo zmena triedy študenta."""
    student = get_object_or_404(User, id=student_id, role=User.Role.STUDENT)
    if request.method == 'POST':
        class_id = request.POST.get('school_class_id')
        if class_id:
            sc = get_object_or_404(SchoolClass, id=class_id)
            student.school_class = sc
            messages.success(request, f"Študent {student.username} bol zaradený do triedy {sc.name}.")
        else:
            student.school_class = None
            messages.info(request, f"Študent {student.username} bol odhlásený z triedy.")
        student.save(update_fields=['school_class'])
    return redirect('teacher_dashboard')


@teacher_required
def student_detail(request, student_id):
    """Detailný profil žiaka s históriou odovzdaných kódov a Code Review komentármi."""
    student = get_object_or_404(User.objects.select_related('school_class'), id=student_id, role=User.Role.STUDENT)
    submissions = Submission.objects.filter(student=student).select_related('exercise__lesson__module').order_by('-created_at')

    total_submissions = submissions.count()
    passed_count = submissions.filter(status=Submission.Status.PASSED).values('exercise').distinct().count()
    total_exercises = Exercise.objects.count()
    success_rate = int((passed_count / total_exercises) * 100) if total_exercises else 0

    all_classes = SchoolClass.objects.all().order_by('name')

    return render(request, 'teacher_panel/student_detail.html', {
        'student': student,
        'submissions': submissions,
        'total_submissions': total_submissions,
        'passed_count': passed_count,
        'total_exercises': total_exercises,
        'success_rate': success_rate,
        'all_classes': all_classes,
    })


# ==============================================================================
# 9. PÔVODNÉ ENDPOINTY (SPÄTNÁ KOMPATIBILITA)
# ==============================================================================

@teacher_required
@transaction.atomic
def manage_student_economy(request, student_id):
    """Umožní učiteľovi pridať/odobrať Doros, upraviť Streak alebo prepnúť PRO/EDU licenciu."""
    if request.method == 'POST':
        student = get_object_or_404(User, id=student_id, role=User.Role.STUDENT)
        action = request.POST.get('action')

        if action == 'adjust_doros':
            amount = int(request.POST.get('amount', 0))
            reason = request.POST.get('reason', 'Úprava od učiteľa').strip()
            student.doros = max(0, student.doros + amount)
            student.save()

            DorosTransaction.objects.create(
                student=student,
                amount=amount,
                reason_sk=f"Učiteľ ({request.user.username}): {reason}",
                reason_en=f"Teacher ({request.user.username}): {reason}",
                performed_by_teacher=request.user
            )
            messages.success(request, f"Mince Doros pre študenta {student.username} boli upravené o {amount}.")

        elif action == 'set_streak':
            new_streak = int(request.POST.get('streak_value', 1))
            student.current_streak = max(0, new_streak)
            student.lost_streak_value = 0
            student.save()
            messages.success(request, f"Streak študenta {student.username} bol nastavený na {new_streak} dní.")

        elif action == 'toggle_edu':
            student.subscription_tier = (
                User.SubscriptionTier.FREE if student.subscription_tier != User.SubscriptionTier.FREE else User.SubscriptionTier.EDU
            )
            student.save()
            messages.success(request, f"Predplatné pre {student.username} zmenené na {student.subscription_tier}.")

    return redirect('teacher_dashboard')


@teacher_required
@transaction.atomic
def process_coupon(request, purchase_id):
    """Schválenie uplatnenia kupónu na hodine alebo jeho zamietnutie s vrátením Doros."""
    if request.method == 'POST':
        purchase = get_object_or_404(RewardPurchase.objects.select_for_update(), id=purchase_id)
        decision = request.POST.get('decision') or request.POST.get('action')

        if purchase.status != RewardPurchase.Status.PENDING:
            return redirect('teacher_dashboard')

        purchase.processed_at = timezone.now()
        purchase.processed_by = request.user

        if decision in ('approve', 'redeem'):
            purchase.status = RewardPurchase.Status.REDEEMED
            purchase.save()
            messages.success(request, f"Kupón {purchase.coupon_code} ({purchase.student.username}) bol schválený a uplatnený.")
        elif decision in ('refund', 'reject'):
            purchase.status = RewardPurchase.Status.REFUNDED
            purchase.save()

            student = purchase.student
            student.doros += purchase.cost_paid
            student.save()

            purchase.reward.current_stock += 1
            purchase.reward.save()

            DorosTransaction.objects.create(
                student=student,
                amount=purchase.cost_paid,
                reason_sk=f"Vrátenie Doros za zamietnutý kupón {purchase.coupon_code}",
                reason_en=f"Refunded Doros for coupon {purchase.coupon_code}",
                performed_by_teacher=request.user
            )
            messages.info(request, f"Kupón {purchase.coupon_code} bol zamietnutý a {purchase.cost_paid} Doros sa vrátilo študentovi.")

    return redirect('teacher_dashboard')


@teacher_required
def create_reward_item(request):
    """Vytvorenie novej odmeny do obchodu."""
    if request.method == 'POST':
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        desc_sk = request.POST.get('description_sk', '').strip()
        cost = int(request.POST.get('cost_doros', 100))
        max_stock = int(request.POST.get('max_stock', 2))
        restock_period = request.POST.get('restock_period', RewardItem.RestockPeriod.WEEKLY)
        limit_per_student = int(request.POST.get('limit_per_student', 1))

        RewardItem.objects.create(
            title_sk=title_sk,
            title_en=title_en,
            description_sk=desc_sk,
            description_en=desc_sk,
            cost_doros=cost,
            max_stock=max_stock,
            current_stock=max_stock,
            restock_period=restock_period,
            limit_per_student_per_period=limit_per_student,
            created_by=request.user
        )
        messages.success(request, f"Odmena '{title_sk}' so skladom {max_stock} ks ({restock_period}) bola pridaná do obchodu.")
    return redirect('teacher_dashboard')


@teacher_required
def create_coin_drop(request):
    """Spustenie nového časovaného Coin Dropu pre študentov."""
    if request.method == 'POST':
        title = request.POST.get('title_sk', 'Bonusový Coin Drop!').strip()
        duration_minutes = int(request.POST.get('duration_minutes', 60))
        max_claims = int(request.POST.get('max_claims', 5))
        min_doros = int(request.POST.get('min_doros', 30))
        max_doros = int(request.POST.get('max_doros', 100))

        now = timezone.now()
        CoinDrop.objects.create(
            title_sk=title,
            title_en=title,
            available_from=now,
            available_until=now + timedelta(minutes=duration_minutes),
            max_claims=max_claims,
            min_doros=min_doros,
            max_doros=max_doros,
            created_by=request.user
        )
        messages.success(request, f"Coin Drop '{title}' bol spustený na {duration_minutes} minút pre prvých {max_claims} študentov!")
    return redirect('teacher_dashboard')


@teacher_required
def create_exercise(request):
    """Rýchle pridanie cvičenia z dashboardu."""
    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id)
        title_sk = request.POST.get('title_sk', '').strip()
        instructions_sk = request.POST.get('instructions_sk', '').strip()
        starter_code = request.POST.get('starter_code', '# Napíš svoj kód sem\n')
        test_code = request.POST.get('test_code', '').strip()
        xp_reward = int(request.POST.get('xp_reward', 50))
        doros_reward = int(request.POST.get('doros_reward', 30))

        ex = Exercise.objects.create(
            lesson=lesson,
            title_sk=title_sk,
            title_en=title_sk,
            instructions_sk=instructions_sk,
            instructions_en=instructions_sk,
            starter_code=starter_code,
            solution_code=starter_code,
            xp_reward=xp_reward,
            doros_reward=doros_reward,
            order=lesson.exercises.count() + 1
        )
        if test_code:
            TestCase.objects.create(
                exercise=ex,
                input_data="Automatický test učiteľa",
                expected_output="True",
                test_code=test_code,
                is_hidden=False
            )
        messages.success(request, f"Cvičenie '{title_sk}' bolo pridané do lekcie {lesson.title_sk}.")
    return redirect('teacher_dashboard')


@teacher_required
def comment_submission(request, submission_id):
    """Učiteľ pridá alebo aktualizuje Code Review komentár k študentskému riešeniu."""
    if request.method == 'POST':
        sub = get_object_or_404(Submission, id=submission_id)
        comment = request.POST.get('teacher_comment', '').strip()
        sub.teacher_comment = comment
        sub.save(update_fields=['teacher_comment'])
        messages.success(request, f"Komentár pre študenta {sub.student.username} bol uložený.")

        redirect_to = request.POST.get('next')
        if redirect_to:
            return redirect(redirect_to)
    return redirect('teacher_dashboard')


@teacher_required
def create_quest(request):
    """Učiteľ vytvorí novú osobnú alebo triednu výzvu (Quest)."""
    if request.method == 'POST':
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        metric_type = request.POST.get('metric_type', Quest.MetricType.SOLVE_EXERCISES)
        target_value = int(request.POST.get('target_value', 3))
        reward_doros = int(request.POST.get('reward_doros', 50))
        reward_xp = int(request.POST.get('reward_xp', 40))
        period = request.POST.get('period', Quest.Period.TEACHER)

        Quest.objects.create(
            title_sk=title_sk,
            title_en=title_en,
            metric_type=metric_type,
            target_value=target_value,
            reward_doros=reward_doros,
            reward_xp=reward_xp,
            period=period,
            created_by=request.user,
            is_active=True,
        )
        messages.success(request, f"Výzva '{title_sk}' bola pridaná študentom.")
    return redirect('teacher_dashboard')


@teacher_required
def create_class_quest(request):
    """Učiteľ vytvorí novú kolektívnu výzvu pre triedu."""
    if request.method == 'POST':
        class_id = request.POST.get('school_class_id')
        school_class = get_object_or_404(SchoolClass, id=class_id)
        title_sk = request.POST.get('title_sk', '').strip()
        title_en = request.POST.get('title_en', '').strip() or title_sk
        target = int(request.POST.get('target_exercises_count', 20))
        reward = int(request.POST.get('reward_doros_per_student', 60))
        min_contrib = int(request.POST.get('min_contribution_required', 1))
        days = int(request.POST.get('days_duration', 7))
        policy = request.POST.get('reward_policy', ClassQuest.RewardPolicy.ALL_STUDENTS)

        deadline = timezone.now() + timedelta(days=days)
        ClassQuest.objects.create(
            school_class=school_class,
            title_sk=title_sk,
            title_en=title_en,
            target_exercises_count=target,
            reward_doros_per_student=reward,
            min_contribution_required=min_contrib,
            reward_policy=policy,
            deadline=deadline,
        )
        messages.success(request, f"Kolektívna výzva pre triedu {school_class.name} na cieľ {target} úloh bola spustená.")
    return redirect('teacher_dashboard')


@teacher_required
def ai_generate_exercise(request):
    """API endpoint: Gemini AI vygeneruje kompletné cvičenie podľa zadanej témy."""
    topic = request.GET.get('topic', 'Podmienky if-else')
    difficulty = request.GET.get('difficulty', 'EASY')
    data = generate_exercise_with_ai(topic, difficulty)
    return JsonResponse(data)


@teacher_required
def ai_translate_exercise(request):
    """API endpoint: Preloží texty zo slovenčiny do angličtiny."""
    title_sk = request.GET.get('title_sk', '')
    instructions_sk = request.GET.get('instructions_sk', '')
    hint_sk = request.GET.get('hint_sk', '')
    explanation_sk = request.GET.get('explanation_sk', '')
    data = translate_to_english({
        'title_en': title_sk,
        'instructions_en': instructions_sk,
        'hint_en': hint_sk,
        'explanation_en': explanation_sk,
    })
    return JsonResponse(data)