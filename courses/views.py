from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from accounts.models import User
from .models import Module, Lesson, Exercise, Submission, LessonProgress
from .services import evaluate_python_code, get_codo_ai_feedback
from gamification.models import (
    Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution,
    CoinDrop, CoinDropClaim, DorosTransaction
)


@login_required
def dashboard(request):
    user = request.user
    modules = Module.objects.prefetch_related('lessons__exercises').all()
    completed_lesson_ids = list(
        LessonProgress.objects.filter(student=user, is_completed=True).values_list('lesson_id', flat=True)
    )

    # Osobné questy (Daily / Weekly / Monthly)
    active_quests = Quest.objects.filter(is_active=True)
    quest_items = []
    for q in active_quests:
        prog, _ = StudentQuestProgress.objects.get_or_create(student=user, quest=q)
        quest_items.append(prog)

    # Kolektívny triedny quest
    class_quest = None
    top_contributors = []
    if user.school_class:
        class_quest = ClassQuest.objects.filter(school_class=user.school_class).first()
        if class_quest:
            top_contributors = class_quest.contributions.select_related('student').order_by('-amount_contributed')[:5]

    # Aktívny Coin Drop, ktorý si študent ešte nevyzdvihol
    now = timezone.now()
    claimed_drop_ids = CoinDropClaim.objects.filter(student=user).values_list('coin_drop_id', flat=True)
    active_drop = CoinDrop.objects.filter(
        available_from__lte=now,
        available_until__gte=now
    ).exclude(id__in=claimed_drop_ids).first()
    if active_drop and not active_drop.is_currently_active():
        active_drop = None

    # Rebríček triedy (Leaderboard)
    leaderboard = User.objects.filter(role=User.Role.STUDENT).order_by('-xp', '-doros')[:8]

    context = {
        'modules': modules,
        'completed_lesson_ids': completed_lesson_ids,
        'quest_items': quest_items,
        'class_quest': class_quest,
        'top_contributors': top_contributors,
        'active_drop': active_drop,
        'leaderboard': leaderboard,
    }
    return render(request, 'courses/dashboard.html', context)


@login_required
@transaction.atomic
def lesson_detail(request, lesson_id):
    user = request.user
    lesson = get_object_or_404(Lesson.objects.select_related('module'), id=lesson_id)

    if lesson.module.is_pro_only and not user.has_pro_access():
        messages.warning(request, "Tento pokročilý modul vyžaduje účet Codoro PRO alebo školskú EDU licenciu.")
        return redirect('shop')

    exercises = lesson.exercises.all()
    selected_ex_id = request.GET.get('exercise')
    current_exercise = exercises.filter(id=selected_ex_id).first() if selected_ex_id else exercises.first()

    latest_submission = None
    if current_exercise:
        latest_submission = Submission.objects.filter(student=user, exercise=current_exercise).first()

    # Spracovanie odoslania Python kódu alebo kvízu
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'run_code' and current_exercise:
            submitted_code = request.POST.get('submitted_code', '')
            already_passed = Submission.objects.filter(
                student=user, exercise=current_exercise, status=Submission.Status.PASSED
            ).exists()
            previous_attempts = Submission.objects.filter(student=user, exercise=current_exercise).count()

            passed, status_str, output_log = evaluate_python_code(current_exercise, submitted_code)

            ai_feedback = ""
            if not passed:
                ai_feedback = get_codo_ai_feedback(
                    current_exercise, submitted_code, output_log, lang=user.preferred_language
                )

            latest_submission = Submission.objects.create(
                student=user,
                exercise=current_exercise,
                submitted_code=submitted_code,
                status=status_str,
                output_log=output_log,
                ai_tutor_feedback=ai_feedback
            )

            if passed and not already_passed:
                # 1. Pripísanie XP a prípadný Level-Up bonus
                lvl_bonus = user.add_xp_and_check_level_up(current_exercise.xp_reward)

                # 2. Odmena Doros (plná na 1. pokus, polovičná na ďalšie pokusy)
                earned_doros = current_exercise.doros_reward if previous_attempts == 0 else max(5, current_exercise.doros_reward // 2)
                user.doros += earned_doros

                # 3. Aktualizácia denného Streaku
                today = timezone.now().date()
                if user.last_activity_date != today:
                    if user.last_activity_date == today - timedelta(days=1):
                        user.current_streak += 1
                    else:
                        user.current_streak = 1
                    user.last_activity_date = today
                    if user.current_streak > user.longest_streak:
                        user.longest_streak = user.current_streak

                user.save()

                DorosTransaction.objects.create(
                    student=user,
                    amount=earned_doros + lvl_bonus,
                    reason_sk=f"Vyriešená úloha: {current_exercise.title_sk}",
                    reason_en=f"Solved exercise: {current_exercise.title_en}"
                )

                # 4. Označenie lekcie ako dokončenej
                LessonProgress.objects.get_or_create(
                    student=user, lesson=lesson, defaults={'is_completed': True}
                )

                # 5. Aktualizácia osobných Questov
                for prog in StudentQuestProgress.objects.filter(student=user, is_completed=False).select_related('quest'):
                    if prog.quest.metric_type == Quest.MetricType.SOLVE_EXERCISES:
                        prog.current_value += 1
                    elif prog.quest.metric_type == Quest.MetricType.EARN_XP:
                        prog.current_value += current_exercise.xp_reward
                    elif prog.quest.metric_type == Quest.MetricType.FIRST_TRY_SOLVES and previous_attempts == 0:
                        prog.current_value += 1

                    if prog.current_value >= prog.quest.target_value:
                        prog.current_value = prog.quest.target_value
                        prog.is_completed = True
                    prog.save()

                # 6. Príspevok do Kolektívneho triedneho questu
                if user.school_class:
                    cq = ClassQuest.objects.select_for_update().filter(
                        school_class=user.school_class, is_completed=False
                    ).first()
                    if cq:
                        cq.current_exercises_count += 1
                        contrib, _ = ClassQuestContribution.objects.get_or_create(class_quest=cq, student=user)
                        contrib.amount_contributed += 1
                        contrib.save()

                        if cq.current_exercises_count >= cq.target_exercises_count:
                            cq.is_completed = True
                        cq.save()

                msg = f"✅ Výborne! Všetky testy prešli (+{current_exercise.xp_reward} XP, +{earned_doros} Doros)."
                if lvl_bonus > 0:
                    msg += f" 🎉 LEVEL UP na úroveň {user.level}! Získavaš bonus +{lvl_bonus} Doros!"
                messages.success(request, msg)
            elif passed:
                messages.info(request, "✅ Kód opäť prešiel všetkými testami (odmenu za túto úlohu si už získal).")
            else:
                messages.error(request, "❌ Niektoré testy zlyhali. Pozri si výpis z konzoly a radu od AI tútora Codo nižšie.")

        elif action == 'submit_quiz':
            all_correct = True
            for q in lesson.quiz_questions.all():
                ans = request.POST.get(f"quiz_{q.id}")
                if ans != q.correct_option:
                    all_correct = False
            if all_correct:
                user.add_xp_and_check_level_up(20)
                messages.success(request, "🎯 Kvíz vyplnený na 100 %! Získavaš +20 XP.")
            else:
                messages.warning(request, "Niektorá odpoveď v kvíze nebola správna. Skús to znova!")

    context = {
        'lesson': lesson,
        'exercises': exercises,
        'current_exercise': current_exercise,
        'latest_submission': latest_submission,
        'quiz_questions': lesson.quiz_questions.all(),
    }
    return render(request, 'courses/lesson_detail.html', context)