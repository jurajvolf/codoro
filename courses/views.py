from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.security import is_rate_limited, sanitize_text
from accounts.utils import tr
from .models import Module, Lesson, Exercise, Submission, LessonProgress, HintUnlock
from .services import evaluate_python_code, get_codo_ai_feedback
from gamification.models import Quest, CoinDrop, CoinDropClaim, DorosTransaction
from gamification.services import (
    get_quest_progress_for, update_quests, get_active_class_quest,
    contribute_to_class_quest, award_badges, badge_leaderboard_counts
)
from .curriculum.cheatsheets_data import CHEATSHEET_CATEGORIES, CHEATSHEET_ITEMS


def _leaderboard_for(user, limit=8):
    qs = User.objects.filter(role=User.Role.STUDENT)
    if user.school_class_id:
        qs = qs.filter(school_class_id=user.school_class_id)
    return list(qs.order_by('-xp', '-doros')[:limit])


def landing_page(request):
    """Verejná landing page Codoro pre návštevníkov a prezentáciu školy."""
    modules = list(Module.objects.prefetch_related('lessons__exercises').all())
    total_modules = len(modules)
    total_lessons = sum(len(m.lessons.all()) for m in modules)
    total_exercises = sum(
        sum(len(l.exercises.all()) for l in m.lessons.all())
        for m in modules
    )
    total_hours = sum(m.estimated_hours for m in modules)

    track_meta = {
        Module.Track.FUNDAMENTALS: {
            'sk': '1. Základy a Logika',
            'en': '1. Fundamentals & Logic',
            'icon': 'zap',
            'badge': '4 Moduly • 46h',
            'desc_sk': 'Úvod do algoritmizácie, premenné, dátové typy, operátory, podmienky if/else a 2D cykly.',
            'desc_en': 'Algorithmics intro, variables, data types, logic operators, conditions and 2D loops.',
        },
        Module.Track.DATA_STRUCTURES: {
            'sk': '2. Funkcie a Dátové štruktúry',
            'en': '2. Functions & Data Structures',
            'icon': 'layers',
            'badge': '4 Moduly • 50h',
            'desc_sk': 'Definície funkcií, scope, rekurzia, zoznamy, slovníky, množiny a ošetrovanie výnimiek.',
            'desc_en': 'Function scopes, recursion, lists, dicts, sets, comprehensions and exception handling.',
        },
        Module.Track.OOP: {
            'sk': '3. OOP a Softvérové inžinierstvo',
            'en': '3. OOP & Software Engineering',
            'icon': 'box',
            'badge': '2 Moduly • 24h',
            'desc_sk': 'Triedy, inštancie, konštruktor __init__, dedičnosť, polymorfizmus a magické dunder metódy.',
            'desc_en': 'Classes, instances, constructor __init__, inheritance, polymorphism and dunder methods.',
        },
        Module.Track.ALGORITHMS_AND_DATA: {
            'sk': '4. Algoritmy, Dáta a Bezpečnosť',
            'en': '4. Algorithms, Data & Security',
            'icon': 'cpu',
            'badge': '5 Modulov • 60h',
            'desc_sk': 'Big-O zložitosť, binárne vyhľadávanie, Regex, SQL v pamäti (sqlite3), REST API a TDD testy.',
            'desc_en': 'Big-O notation, binary search, Regex parsing, SQLite in-memory, REST APIs and TDD.',
        },
        Module.Track.MATURITA_PREP: {
            'sk': '5. Záverečné projekty a certifikácia',
            'en': '5. Capstone Projects & Certification',
            'icon': 'award',
            'badge': '3 Moduly • 42h',
            'desc_sk': 'Kryptografia, praktické algoritmické zadania a záverečné certifikačné projekty.',
            'desc_en': 'Applied cryptography, practical software tasks, and capstone certification projects.',
        },
    }

    tracks_data = []
    for track_key, track_label in Module.Track.choices:
        mods = [m for m in modules if m.track == track_key]
        meta = track_meta.get(track_key, {
            'sk': track_label,
            'en': track_label,
            'icon': 'book',
            'badge': f'{len(mods)} Modulov',
            'desc_sk': '',
            'desc_en': '',
        })
        tracks_data.append({
            'key': track_key,
            'label_sk': meta['sk'],
            'label_en': meta['en'],
            'icon': meta['icon'],
            'badge': meta['badge'],
            'desc_sk': meta['desc_sk'],
            'desc_en': meta['desc_en'],
            'modules': mods,
        })

    context = {
        'modules': modules,
        'tracks_data': tracks_data,
        'total_modules': total_modules,
        'total_lessons': total_lessons,
        'total_exercises': total_exercises,
        'total_hours': total_hours,
        'is_public_landing': True,
    }
    return render(request, 'landing.html', context)


def dashboard(request):
    if not request.user.is_authenticated:
        return landing_page(request)
    user = request.user
    modules = Module.objects.prefetch_related('lessons__exercises').all()
    completed_lesson_ids = set(
        LessonProgress.objects.filter(student=user, is_completed=True).values_list('lesson_id', flat=True)
    )
    solved_ids = set(
        Submission.objects.filter(student=user, status=Submission.Status.PASSED).values_list('exercise_id', flat=True)
    )

    # Prehľad modulov s percentuálnym progresom
    module_cards = []
    next_lesson = None
    total_lessons = 0
    total_completed = 0
    first_incomplete_module_id = None

    for module in modules:
        lessons = list(module.lessons.all())
        for lesson in lessons:
            exercises = list(lesson.exercises.all())
            done_ex = sum(1 for ex in exercises if ex.id in solved_ids)
            lesson.is_completed = (lesson.id in completed_lesson_ids)
            if lesson.is_completed:
                lesson.progress_pct = 100
            elif exercises and done_ex > 0:
                lesson.progress_pct = int(done_ex * 100 / len(exercises))
            else:
                lesson.progress_pct = 0
            # Obvod mini krúžku (r=6): 2 * pi * 6 = 37.7
            lesson.dash_offset = round(37.7 - (37.7 * lesson.progress_pct / 100), 1)

        done = sum(1 for lesson in lessons if getattr(lesson, 'is_completed', False))
        total_lessons += len(lessons)
        total_completed += done
        locked = module.is_pro_only and not user.has_pro_access()
        if not next_lesson and not locked:
            next_lesson = next((lesson for lesson in lessons if not getattr(lesson, 'is_completed', False)), None)
        if first_incomplete_module_id is None and not locked and (done < len(lessons) or len(lessons) == 0):
            first_incomplete_module_id = module.id

        pct = int(done * 100 / len(lessons)) if lessons else 0
        # Obvod modulu (r=14): 2 * pi * 14 = 88
        dash_offset = round(88 - (88 * pct / 100), 1)

        module_cards.append({
            'module': module,
            'lessons': lessons,
            'done': done,
            'total': len(lessons),
            'pct': pct,
            'dash_offset': dash_offset,
            'locked': locked,
        })

    if first_incomplete_module_id is None and module_cards:
        first_incomplete_module_id = module_cards[0]['module'].id

    overall_progress_pct = int(total_completed * 100 / total_lessons) if total_lessons else 0

    # Osobné questy (Daily / Weekly / Monthly) s automatickým resetom obdobia
    quest_items = get_quest_progress_for(user) if not user.is_teacher() else []

    # Kolektívny triedny quest
    class_quest = get_active_class_quest(user.school_class)
    top_contributors = []
    if class_quest:
        top_contributors = class_quest.contributions.select_related('student').order_by('-amount_contributed')[:5]

    # Aktívny Coin Drop pre triedu študenta (alebo pre všetkých), ktorý si ešte nevyzdvihol
    now = timezone.now()
    claimed_drop_ids = CoinDropClaim.objects.filter(student=user).values_list('coin_drop_id', flat=True)
    drops = CoinDrop.objects.filter(available_from__lte=now, available_until__gte=now).filter(
        Q(school_class__isnull=True) | Q(school_class_id=user.school_class_id)
    ).exclude(id__in=claimed_drop_ids).order_by('available_until')
    active_drop = next((d for d in drops if d.is_currently_active()), None)

    leaderboard = _leaderboard_for(user)
    badge_counts = badge_leaderboard_counts([s.id for s in leaderboard])
    for s in leaderboard:
        s.badge_count = badge_counts.get(s.id, 0)

    total_exercises = sum(len(lesson.exercises.all()) for m in modules for lesson in m.lessons.all()) or 28
    modules_completed = sum(1 for c in module_cards if c['done'] == c['total'] and c['total'] > 0)
    total_modules = len(modules)

    track_meta = {
        Module.Track.FUNDAMENTALS: {
            'sk': 'Základy Pythonu',
            'en': 'Python Foundations',
            'short_sk': '1. Základy Pythonu',
            'short_en': '1. Foundations',
            'icon': 'zap',
            'desc_sk': 'Sprevádzaná praktická cesta od základov až po skutočné projekty.',
            'desc_en': 'A guided, hands-on journey from basics to real projects.',
        },
        Module.Track.DATA_STRUCTURES: {
            'sk': 'Funkcie a Dátové štruktúry',
            'en': 'Data Structures',
            'short_sk': '2. Funkcie a Dáta',
            'short_en': '2. Data Structures',
            'icon': 'layers',
            'desc_sk': 'Zoznamy, n-tice, slovníky, množiny a štruktúrované dáta.',
            'desc_en': 'Lists, tuples, dictionaries, sets and structured data handling.',
        },
        Module.Track.OOP: {
            'sk': 'Objektovo-orientované programovanie',
            'en': 'OOP & Architecture',
            'short_sk': '3. OOP a Architektúra',
            'short_en': '3. OOP Architecture',
            'icon': 'box',
            'desc_sk': 'Triedy, inštancie, dedičnosť, polymorfizmus a dunder metódy.',
            'desc_en': 'Classes, instances, inheritance, polymorphism and dunder methods.',
        },
        Module.Track.ALGORITHMS_AND_DATA: {
            'sk': 'Algoritmy, SQL a Bezpečnosť',
            'en': 'Algorithms & SQL',
            'short_sk': '4. Algoritmy a SQL',
            'short_en': '4. Algorithms & SQL',
            'icon': 'cpu',
            'desc_sk': 'Big-O zložitosť, vyhľadávanie, SQLite v pamäti a REST API.',
            'desc_en': 'Big-O notation, search, in-memory SQLite and REST APIs.',
        },
        Module.Track.MATURITA_PREP: {
            'sk': 'Záverečné projekty a certifikácia',
            'en': 'Capstone Projects & Certification',
            'short_sk': '5. Projekty & Certifikácia',
            'short_en': '5. Capstone Projects',
            'icon': 'award',
            'desc_sk': 'Komplexné záverečné projekty, kryptografia a certifikačná skúška Codoro.',
            'desc_en': 'Comprehensive capstone boss projects, cryptography, and Codoro certification.',
        },
    }

    tracks_data = []
    for track_key, track_label in Module.Track.choices:
        mods = [c for c in module_cards if c['module'].track == track_key]
        t_done = sum(c['done'] for c in mods)
        t_total = sum(c['total'] for c in mods)
        t_pct = int(t_done * 100 / t_total) if t_total else 0
        meta = track_meta.get(track_key, {
            'sk': track_label,
            'en': track_label,
            'short_sk': track_label,
            'short_en': track_label,
            'icon': 'book',
            'desc_sk': '',
            'desc_en': '',
        })
        tracks_data.append({
            'key': track_key,
            'title_sk': meta['sk'],
            'title_en': meta['en'],
            'short_sk': meta.get('short_sk', meta['sk']),
            'short_en': meta.get('short_en', meta['en']),
            'icon': meta.get('icon', 'book'),
            'desc_sk': meta['desc_sk'],
            'desc_en': meta['desc_en'],
            'count': len(mods),
            'done': t_done,
            'total': t_total,
            'pct': t_pct,
        })

    context = {
        'modules': modules,
        'module_cards': module_cards,
        'next_lesson': next_lesson,
        'completed_lesson_ids': completed_lesson_ids,
        'solved_count': len(solved_ids),
        'total_lessons': total_lessons,
        'total_completed': total_completed,
        'total_modules': total_modules,
        'modules_completed': modules_completed,
        'total_exercises': total_exercises,
        'overall_progress_pct': overall_progress_pct,
        'default_open_module_id': first_incomplete_module_id,
        'quest_items': quest_items,
        'class_quest': class_quest,
        'top_contributors': top_contributors,
        'active_drop': active_drop,
        'leaderboard': leaderboard,
        'ai_hints_remaining': user.ai_hints_remaining(),
        'tracks_data': tracks_data,
    }
    return render(request, 'courses/dashboard.html', context)


def _reward_solved_exercise(request, user, lesson, exercise, previous_attempts):
    """Pripíše všetky odmeny za prvé úspešné vyriešenie úlohy (atomicky)."""
    lang = user.preferred_language
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)

        # 1. XP a prípadný Level-Up bonus
        lvl_bonus = user.add_xp_and_check_level_up(exercise.xp_reward)

        # 2. Doros (plná odmena na 1. pokus, polovičná na ďalšie pokusy)
        first_try = previous_attempts == 0
        earned_doros = exercise.doros_reward if first_try else max(5, exercise.doros_reward // 2)
        user.doros += earned_doros

        # 3. Denný Streak
        user.register_activity()
        user.save()

        DorosTransaction.objects.create(
            student=user,
            amount=earned_doros + lvl_bonus,
            reason_sk=f"Vyriešená úloha: {exercise.title_sk}" + (" (1. pokus)" if first_try else ""),
            reason_en=f"Solved exercise: {exercise.title_en}" + (" (1st try)" if first_try else ""),
        )

        # 4. Dokončenie lekcie - až keď sú vyriešené všetky jej cvičenia
        lesson_completed_now = False
        exercise_ids = set(lesson.exercises.values_list('id', flat=True))
        solved_in_lesson = set(Submission.objects.filter(
            student=user, exercise_id__in=exercise_ids, status=Submission.Status.PASSED
        ).values_list('exercise_id', flat=True))
        if exercise_ids and exercise_ids.issubset(solved_in_lesson):
            progress, _ = LessonProgress.objects.get_or_create(student=user, lesson=lesson)
            if not progress.is_completed:
                progress.is_completed = True
                progress.save(update_fields=['is_completed'])
                lesson_completed_now = True
                lvl_bonus += user.add_xp_and_check_level_up(lesson.xp_reward)

        # 5. Osobné questy
        update_quests(user, Quest.MetricType.SOLVE_EXERCISES, 1)
        update_quests(user, Quest.MetricType.EARN_XP, exercise.xp_reward + (lesson.xp_reward if lesson_completed_now else 0))
        if first_try:
            update_quests(user, Quest.MetricType.FIRST_TRY_SOLVES, 1)
        if lesson_completed_now:
            update_quests(user, Quest.MetricType.COMPLETE_LESSONS, 1)

        # 6. Kolektívny triedny quest (pri splnení automaticky rozdelí odmeny celej triede)
        cq = contribute_to_class_quest(user)

        # 7. Odznaky
        new_badges = award_badges(user)

    msg = tr(lang,
             f"Výborne! Všetky testy prešli (+{exercise.xp_reward} XP, +{earned_doros} Doros).",
             f"Great job! All tests passed (+{exercise.xp_reward} XP, +{earned_doros} Doros).")
    if lesson_completed_now:
        msg += tr(lang, f" Lekcia dokončená (+{lesson.xp_reward} XP)!", f" Lesson completed (+{lesson.xp_reward} XP)!")
    if lvl_bonus > 0:
        msg += tr(lang, f" LEVEL UP na úroveň {user.level}! Bonus +{lvl_bonus} Doros!",
                  f" LEVEL UP to level {user.level}! Bonus +{lvl_bonus} Doros!")
    messages.success(request, msg)
    if cq and cq.is_completed:
        messages.success(request, tr(lang,
                                     f"Trieda splnila kolektívnu výzvu „{cq.title_sk}“! Odmeny boli rozdelené.",
                                     f"Your class completed the quest “{cq.title_en}”! Rewards have been distributed."))
    for badge in new_badges:
        messages.success(request, tr(lang,
                                     f"Nový odznak: {badge.name_sk} (+{badge.bonus_doros} Doros)",
                                     f"New badge: {badge.name_en} (+{badge.bonus_doros} Doros)"))


@login_required
def lesson_detail(request, lesson_id):
    user = request.user
    lang = user.preferred_language
    lesson = get_object_or_404(Lesson.objects.select_related('module'), id=lesson_id)

    if not user.is_teacher() and (not lesson.is_published or not lesson.module.is_published):
        messages.error(request, tr(lang, "Táto lekcia momentálne nie je publikovaná.", "This lesson is currently not published."))
        return redirect('dashboard')

    if lesson.module.is_pro_only and not user.has_pro_access():
        messages.warning(request, tr(lang,
                                     "Tento pokročilý modul vyžaduje účet Codoro PRO alebo školskú EDU licenciu.",
                                     "This advanced module requires a Codoro PRO account or a school EDU license."))
        return redirect('shop')

    exercises = list(lesson.exercises.all())
    selected_ex_id = request.GET.get('exercise') or request.POST.get('exercise_id')
    current_exercise = None
    if selected_ex_id:
        current_exercise = next((e for e in exercises if str(e.id) == str(selected_ex_id)), None)
    if not current_exercise and exercises:
        current_exercise = exercises[0]

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'run_code' and current_exercise:
            if is_rate_limited(request, 'code_run', limit=30, window_seconds=60, identifier=str(user.id)):
                messages.warning(request, tr(
                    lang,
                    "Spúšťaš kód príliš rýchlo za sebou. Počkaj pár sekúnd a skús to znova.",
                    "You are running code too quickly. Please wait a few seconds and try again."
                ))
                return redirect(f"{request.path}?exercise={current_exercise.id}#workbench")

            submitted_code = request.POST.get('submitted_code', '')[:20000]
            already_passed = Submission.objects.filter(
                student=user, exercise=current_exercise, status=Submission.Status.PASSED
            ).exists()
            previous_attempts = Submission.objects.filter(student=user, exercise=current_exercise).count()

            # Spustenie sandboxu prebieha MIMO databázovej transakcie (nedrží zámok počas behu kódu)
            eval_result = evaluate_python_code(current_exercise, submitted_code, lang=lang)
            passed, status_str, output_log = eval_result
            exec_time_ms = getattr(eval_result, 'execution_time_ms', 0)

            ai_feedback = ""
            if not passed:
                if user.consume_ai_hint():
                    ai_feedback = get_codo_ai_feedback(current_exercise, submitted_code, output_log, lang=lang)
                else:
                    ai_feedback = tr(
                        lang,
                        "Codo: Dnešný limit AI rád pre FREE účet je vyčerpaný. Aktivuj si EDU/PRO licenciu v obchode pre neobmedzené rady.",
                        "Codo: You've used today's AI hints for the FREE plan. Activate an EDU/PRO license in the shop for unlimited hints."
                    )

            Submission.objects.create(
                student=user,
                exercise=current_exercise,
                submitted_code=submitted_code,
                status=status_str,
                execution_time_ms=exec_time_ms,
                output_log=output_log,
                ai_tutor_feedback=ai_feedback
            )

            if passed and not already_passed:
                _reward_solved_exercise(request, user, lesson, current_exercise, previous_attempts)
            elif passed:
                messages.info(request, tr(lang,
                                          "Kód opäť prešiel všetkými testami (odmenu za túto úlohu si už získal).",
                                          "Your code passed again (you've already collected the reward for this task)."))
            else:
                messages.error(request, tr(lang,
                                           "Niektoré testy zlyhali. Pozri si výpis z konzoly a radu od AI tútora Codo nižšie.",
                                           "Some tests failed. Check the console output and Codo's hint below."))
            return redirect(f"{request.path}?exercise={current_exercise.id}#workbench")

        elif action == 'submit_quiz':
            questions = list(lesson.quiz_questions.all())
            wrong = [q for q in questions if request.POST.get(f"quiz_{q.id}") != q.correct_option]
            progress, _ = LessonProgress.objects.get_or_create(student=user, lesson=lesson)
            if not wrong and questions:
                if progress.quiz_passed:
                    messages.info(request, tr(lang, "Správne! Kvíz si už mal vyplnený (XP boli pripísané skôr).",
                                              "Correct! You already passed this quiz (XP were awarded earlier)."))
                else:
                    progress.quiz_passed = True
                    progress.save(update_fields=['quiz_passed'])
                    with transaction.atomic():
                        bonus = user.add_xp_and_check_level_up(20)
                        update_quests(user, Quest.MetricType.EARN_XP, 20)
                        new_badges = award_badges(user)
                    msg = tr(lang, "Kvíz vyplnený na 100 %! Získavaš +20 XP.", "Quiz aced! You earned +20 XP.")
                    if bonus:
                        msg += tr(lang, f" LEVEL UP! Bonus +{bonus} Doros!", f" LEVEL UP! Bonus +{bonus} Doros!")
                    messages.success(request, msg)
                    for badge in new_badges:
                        messages.success(request, tr(lang, f"Nový odznak: {badge.name_sk}",
                                                     f"New badge: {badge.name_en}"))
            else:
                messages.warning(request, tr(lang,
                                             f"Počet nesprávnych odpovedí: {len(wrong)}. Prečítaj si teóriu a skús to znova!",
                                             f"Wrong answers: {len(wrong)}. Re-read the theory and try again!"))
            return redirect(f"{request.path}#quiz")

    latest_submission = None
    hint_unlocked = False
    solved_ids = set(
        Submission.objects.filter(student=user, exercise__lesson=lesson, status=Submission.Status.PASSED)
        .values_list('exercise_id', flat=True)
    )
    attempts_count = 0
    if current_exercise:
        latest_submission = Submission.objects.filter(student=user, exercise=current_exercise).first()
        attempts_count = Submission.objects.filter(student=user, exercise=current_exercise).count()
        hint_unlocked = user.is_teacher() or current_exercise.hint_cost_doros == 0 or HintUnlock.objects.filter(
            student=user, exercise=current_exercise
        ).exists()

    reviewed_submission = None
    if current_exercise:
        reviewed_submission = Submission.objects.filter(
            student=user, exercise=current_exercise
        ).exclude(teacher_comment='').first()

    next_exercise = None
    if current_exercise and exercises:
        try:
            curr_idx = [e.id for e in exercises].index(current_exercise.id)
            if curr_idx + 1 < len(exercises):
                next_exercise = exercises[curr_idx + 1]
        except ValueError:
            pass

    is_current_passed = bool(
        latest_submission and latest_submission.status == Submission.Status.PASSED
    ) or (current_exercise and current_exercise.id in solved_ids)

    progress = LessonProgress.objects.filter(student=user, lesson=lesson).first()
    all_lessons = list(Lesson.objects.select_related('module').order_by('module__order', 'order'))
    idx = next((i for i, item in enumerate(all_lessons) if item.id == lesson.id), 0)
    prev_lesson = all_lessons[idx - 1] if idx > 0 else None
    next_lesson = all_lessons[idx + 1] if idx + 1 < len(all_lessons) else None

    module_lessons = list(lesson.module.lessons.order_by('order'))
    completed_lesson_ids = set(
        LessonProgress.objects.filter(student=user, is_completed=True).values_list('lesson_id', flat=True)
    )
    submission_history = list(
        Submission.objects.filter(student=user, exercise=current_exercise).order_by('-created_at')[:10]
    ) if current_exercise else []

    context = {
        'lesson': lesson,
        'exercises': exercises,
        'current_exercise': current_exercise,
        'next_exercise': next_exercise,
        'is_current_passed': is_current_passed,
        'latest_submission': latest_submission,
        'reviewed_submission': reviewed_submission,
        'attempts_count': attempts_count,
        'solved_ids': solved_ids,
        'hint_unlocked': hint_unlocked,
        'quiz_questions': lesson.quiz_questions.all(),
        'quiz_passed': bool(progress and progress.quiz_passed),
        'lesson_completed': bool(progress and progress.is_completed),
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'module_lessons': module_lessons,
        'completed_lesson_ids': completed_lesson_ids,
        'submission_history': submission_history,
        'ai_hints_remaining': user.ai_hints_remaining(),
    }
    return render(request, 'courses/lesson_detail.html', context)


@login_required
@require_POST
def unlock_hint(request, exercise_id):
    """Odomkne nápovedu k cvičeniu za Doros. Platí sa iba raz, operácia je atomická."""
    lang = request.user.preferred_language
    exercise = get_object_or_404(Exercise.objects.select_related('lesson', 'lesson__module'), id=exercise_id)
    if not exercise.lesson.is_published or not exercise.lesson.module.is_published:
        messages.error(request, tr(lang, "Tento obsah nie je publikovaný.", "This content is not published."))
        return redirect('dashboard')
    if exercise.lesson.module.is_pro_only and not request.user.has_pro_access():
        messages.warning(request, tr(lang, "Tento pokročilý modul vyžaduje Codoro PRO.", "This advanced module requires Codoro PRO."))
        return redirect('shop')
    target = f"/lesson/{exercise.lesson_id}/?exercise={exercise.id}#workbench"

    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=request.user.pk)
        if HintUnlock.objects.filter(student=user, exercise=exercise).exists():
            return redirect(target)
        cost = exercise.hint_cost_doros
        if user.doros < cost:
            messages.error(request, tr(lang,
                                       f"Na odomknutie nápovedy potrebuješ {cost} Doros.",
                                       f"You need {cost} Doros to unlock this hint."))
            return redirect(target)
        user.doros -= cost
        user.save(update_fields=['doros'])
        HintUnlock.objects.create(student=user, exercise=exercise, cost_paid=cost)
        if cost:
            DorosTransaction.objects.create(
                student=user, amount=-cost,
                reason_sk=f"Odomknutá nápoveda: {exercise.title_sk}",
                reason_en=f"Unlocked hint: {exercise.title_en}",
            )
    messages.info(request, tr(lang, f"Nápoveda odomknutá (-{cost} Doros).", f"Hint unlocked (-{cost} Doros)."))
    return redirect(target)


@login_required
def practice_arena(request):
    """Tréningová Aréna / Katalóg úloh s filtrovaním podľa náročnosti, modulu a stavu riešenia."""
    user = request.user
    lang = user.preferred_language

    difficulty = request.GET.get('difficulty', '').strip().upper()
    module_id = request.GET.get('module', '').strip()
    status = request.GET.get('status', '').strip().lower()
    q = sanitize_text(request.GET.get('q', ''), max_length=120)

    exercises_qs = Exercise.objects.select_related('lesson', 'lesson__module').all()

    if difficulty in ['EASY', 'MEDIUM', 'HARD']:
        exercises_qs = exercises_qs.filter(difficulty=difficulty)
    if module_id and module_id.isdigit():
        exercises_qs = exercises_qs.filter(lesson__module_id=int(module_id))
    if q:
        exercises_qs = exercises_qs.filter(
            Q(title_sk__icontains=q) |
            Q(title_en__icontains=q) |
            Q(instructions_sk__icontains=q) |
            Q(instructions_en__icontains=q)
        )

    solved_ids = set(
        Submission.objects.filter(student=user, status=Submission.Status.PASSED)
        .values_list('exercise_id', flat=True)
    )

    exercise_list = list(exercises_qs.order_by('lesson__module__order', 'lesson__order', 'order'))
    if status == 'solved':
        exercise_list = [e for e in exercise_list if e.id in solved_ids]
    elif status == 'unsolved':
        exercise_list = [e for e in exercise_list if e.id not in solved_ids]

    all_modules = Module.objects.order_by('order')
    total_exercises = Exercise.objects.count()
    total_solved = len(solved_ids)
    easy_count = Exercise.objects.filter(difficulty=Exercise.Difficulty.EASY).count()
    easy_solved = Exercise.objects.filter(difficulty=Exercise.Difficulty.EASY, id__in=solved_ids).count()
    medium_count = Exercise.objects.filter(difficulty=Exercise.Difficulty.MEDIUM).count()
    medium_solved = Exercise.objects.filter(difficulty=Exercise.Difficulty.MEDIUM, id__in=solved_ids).count()
    hard_count = Exercise.objects.filter(difficulty=Exercise.Difficulty.HARD).count()
    hard_solved = Exercise.objects.filter(difficulty=Exercise.Difficulty.HARD, id__in=solved_ids).count()

    context = {
        'exercises': exercise_list,
        'all_modules': all_modules,
        'solved_ids': solved_ids,
        'total_exercises': total_exercises,
        'total_solved': total_solved,
        'easy_count': easy_count,
        'easy_solved': easy_solved,
        'medium_count': medium_count,
        'medium_solved': medium_solved,
        'hard_count': hard_count,
        'hard_solved': hard_solved,
        'selected_difficulty': difficulty,
        'selected_module_id': int(module_id) if module_id.isdigit() else None,
        'selected_status': status,
        'search_query': q,
    }
    return render(request, 'courses/practice_arena.html', context)


@login_required
def cheat_sheets_view(request):
    """Interaktívne Python Ťaháky a Slovník pojmov (/cheatsheets/)."""
    user = request.user
    lang = getattr(user, 'preferred_language', 'sk')

    categories = []
    for cat in CHEATSHEET_CATEGORIES:
        cat_items = [it for it in CHEATSHEET_ITEMS if it['category'] == cat['id']]
        c_copy = dict(cat)
        c_copy['count'] = len(cat_items)
        categories.append(c_copy)

    context = {
        'categories': categories,
        'items': CHEATSHEET_ITEMS,
        'total_items_count': len(CHEATSHEET_ITEMS),
    }
    return render(request, 'courses/cheat_sheets.html', context)
