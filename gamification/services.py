"""
Servisná vrstva hernej ekonomiky Codoro.
Centralizuje pravidlá pre osobné questy, kolektívne triedne výzvy a odznaky,
aby ich mohli volať všetky moduly (courses, gamification, teacher_panel).
"""
from django.db import transaction
from django.db.models import Count

from .models import (
    Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution,
    DorosTransaction, Badge, StudentBadge, RewardPurchase
)


# ----------------------------------------------------------------------
# Osobné questy
# ----------------------------------------------------------------------
def get_quest_progress_for(user):
    """Vráti aktuálny progres všetkých aktívnych questov (vrátane automatického resetu obdobia)."""
    items = []
    for quest in Quest.objects.filter(is_active=True).order_by('period', 'id'):
        prog, _ = StudentQuestProgress.objects.get_or_create(student=user, quest=quest)
        prog.quest = quest
        prog.ensure_current_period()
        items.append(prog)
    return items


def update_quests(user, metric_type, amount=1):
    """Pripočíta progres do všetkých aktívnych questov s danou metrikou. Vráti zoznam práve splnených."""
    newly_completed = []
    for prog in get_quest_progress_for(user):
        if prog.is_completed or prog.quest.metric_type != metric_type:
            continue
        prog.current_value += amount
        if prog.current_value >= prog.quest.target_value:
            prog.current_value = prog.quest.target_value
            prog.is_completed = True
            newly_completed.append(prog)
        prog.save()
    return newly_completed


# ----------------------------------------------------------------------
# Kolektívne triedne výzvy
# ----------------------------------------------------------------------
def get_active_class_quest(school_class):
    """Aktuálna (nevypršaná alebo práve splnená) kolektívna výzva triedy."""
    if not school_class:
        return None
    for cq in ClassQuest.objects.filter(school_class=school_class).order_by('is_completed', '-deadline'):
        if not cq.is_expired():
            return cq
    return None


@transaction.atomic
def contribute_to_class_quest(user):
    """Pripíše 1 vyriešenú úlohu do kolektívnej výzvy triedy a pri splnení rozdelí odmeny."""
    if not user.school_class:
        return None
    from django.utils import timezone
    cq = ClassQuest.objects.select_for_update().filter(
        school_class=user.school_class, is_completed=False, deadline__gte=timezone.now()
    ).order_by('deadline').first()
    if not cq:
        return None

    cq.current_exercises_count += 1
    contrib, _ = ClassQuestContribution.objects.get_or_create(class_quest=cq, student=user)
    contrib.amount_contributed += 1
    contrib.save()

    if cq.current_exercises_count >= cq.target_exercises_count:
        cq.is_completed = True
    cq.save()

    if cq.is_completed and not cq.rewards_distributed:
        distribute_class_quest_rewards(cq)
    return cq


@transaction.atomic
def distribute_class_quest_rewards(cq):
    """
    Rozdelí odmenu podľa politiky výzvy:
    - ALL_STUDENTS: dostane ju každý študent triedy,
    - CONTRIBUTORS_ONLY: iba žiaci s príspevkom >= min_contribution_required.
    Vráti počet odmenených študentov.
    """
    cq = ClassQuest.objects.select_for_update().get(pk=cq.pk)
    if cq.rewards_distributed:
        return 0

    from accounts.models import User
    students = User.objects.filter(school_class=cq.school_class, role=User.Role.STUDENT)
    if cq.reward_policy == ClassQuest.RewardPolicy.CONTRIBUTORS_ONLY:
        eligible_ids = ClassQuestContribution.objects.filter(
            class_quest=cq, amount_contributed__gte=cq.min_contribution_required
        ).values_list('student_id', flat=True)
        students = students.filter(id__in=list(eligible_ids))

    count = 0
    for student in students.select_for_update():
        student.doros += cq.reward_doros_per_student
        student.save(update_fields=['doros'])
        DorosTransaction.objects.create(
            student=student,
            amount=cq.reward_doros_per_student,
            reason_sk=f"Splnená kolektívna výzva triedy: {cq.title_sk}",
            reason_en=f"Completed class quest: {cq.title_en}",
        )
        count += 1

    cq.rewards_distributed = True
    cq.save(update_fields=['rewards_distributed'])
    return count


# ----------------------------------------------------------------------
# Štatistiky študenta (profil, odznaky, certifikát)
# ----------------------------------------------------------------------
def get_student_stats(user):
    from courses.models import Submission, LessonProgress, Exercise, Lesson, Module

    submissions = list(
        Submission.objects.filter(student=user).order_by('created_at').values('exercise_id', 'status', 'created_at')
    )
    first_status = {}
    solved = set()
    for s in submissions:
        first_status.setdefault(s['exercise_id'], s['status'])
        if s['status'] == 'PASSED':
            solved.add(s['exercise_id'])
    first_try = sum(1 for ex_id, st in first_status.items() if st == 'PASSED')
    passed_count = sum(1 for s in submissions if s['status'] == 'PASSED')

    completed_lessons = set(
        LessonProgress.objects.filter(student=user, is_completed=True).values_list('lesson_id', flat=True)
    )
    quizzes_passed = LessonProgress.objects.filter(student=user, quiz_passed=True).count()

    module_progress = []
    for module in Module.objects.prefetch_related('lessons').order_by('order'):
        lesson_ids = [lesson.id for lesson in module.lessons.all()]
        done = len([lid for lid in lesson_ids if lid in completed_lessons])
        module_progress.append({
            'module': module,
            'total': len(lesson_ids),
            'done': done,
            'pct': int(done * 100 / len(lesson_ids)) if lesson_ids else 0,
            'is_complete': bool(lesson_ids) and done == len(lesson_ids),
        })

    total_attempts = len(submissions)
    return {
        'solved_count': len(solved),
        'total_exercises': Exercise.objects.count(),
        'attempts': total_attempts,
        'success_rate': int(passed_count * 100 / total_attempts) if total_attempts else 0,
        'first_try_count': first_try,
        'lessons_completed': len(completed_lessons),
        'total_lessons': Lesson.objects.count(),
        'quizzes_passed': quizzes_passed,
        'module_progress': module_progress,
        'completed_modules': [m for m in module_progress if m['is_complete']],
    }


# ----------------------------------------------------------------------
# Odznaky (Achievements)
# ----------------------------------------------------------------------
BADGE_DEFINITIONS = [
    # code, emoji, name_sk, name_en, desc_sk, desc_en, bonus
    ('FIRST_STEPS', '🐣', 'Prvé kroky', 'First Steps',
     'Vyrieš svoju prvú programátorskú úlohu.', 'Solve your first coding exercise.', 25),
    ('SHARPSHOOTER', '🎯', 'Ostrostrelec', 'Sharpshooter',
     'Vyrieš 5 úloh hneď na prvý pokus.', 'Solve 5 exercises on the first try.', 75),
    ('PROBLEM_SOLVER', '🧩', 'Riešiteľ problémov', 'Problem Solver',
     'Vyrieš 10 rôznych úloh.', 'Solve 10 different exercises.', 100),
    ('QUIZ_MASTER', '🧠', 'Majster kvízov', 'Quiz Master',
     'Vyplň 3 kvízy na 100 %.', 'Ace 3 lesson quizzes.', 50),
    ('MODULE_MASTER', '📚', 'Absolvent modulu', 'Module Graduate',
     'Dokonči všetky lekcie v jednom module.', 'Complete every lesson of a module.', 100),
    ('STREAK_7', '🔥', 'Týždňová séria', 'Week Streak',
     'Udrž sériu učenia 7 dní po sebe.', 'Keep a 7-day learning streak.', 100),
    ('LEVEL_5', '⚡', 'Level 5', 'Level 5',
     'Dosiahni 5. úroveň.', 'Reach level 5.', 100),
    ('SHOPPER', '🛍️', 'Prvý nákup', 'First Purchase',
     'Kúp si prvú odmenu v školskom obchode.', 'Buy your first reward in the class shop.', 20),
    ('TEAM_PLAYER', '🤝', 'Tímový hráč', 'Team Player',
     'Prispej do splnenej kolektívnej výzvy triedy.', 'Contribute to a completed class quest.', 75),
]


def ensure_badges_exist():
    for order, (code, emoji, n_sk, n_en, d_sk, d_en, bonus) in enumerate(BADGE_DEFINITIONS, start=1):
        Badge.objects.update_or_create(code=code, defaults={
            'name_sk': n_sk, 'name_en': n_en, 'description_sk': d_sk, 'description_en': d_en,
            'icon_name': emoji, 'bonus_doros': bonus, 'order': order,
        })


def _badge_criteria(user, stats):
    return {
        'FIRST_STEPS': stats['solved_count'] >= 1,
        'SHARPSHOOTER': stats['first_try_count'] >= 5,
        'PROBLEM_SOLVER': stats['solved_count'] >= 10,
        'QUIZ_MASTER': stats['quizzes_passed'] >= 3,
        'MODULE_MASTER': len(stats['completed_modules']) >= 1,
        'STREAK_7': max(user.longest_streak, user.current_streak) >= 7,
        'LEVEL_5': user.level >= 5,
        'SHOPPER': RewardPurchase.objects.filter(student=user).exists(),
        'TEAM_PLAYER': ClassQuestContribution.objects.filter(
            student=user, class_quest__is_completed=True, amount_contributed__gte=1
        ).exists(),
    }


@transaction.atomic
def award_badges(user):
    """Skontroluje všetky kritériá a udelí nové odznaky (vrátane bonusových Doros). Vráti zoznam nových odznakov."""
    if user.is_teacher():
        return []
    if Badge.objects.count() < len(BADGE_DEFINITIONS):
        ensure_badges_exist()

    owned = set(StudentBadge.objects.filter(student=user).values_list('badge__code', flat=True))
    criteria = _badge_criteria(user, get_student_stats(user))
    new_badges = []
    for badge in Badge.objects.exclude(code__in=owned):
        if criteria.get(badge.code):
            StudentBadge.objects.create(student=user, badge=badge)
            if badge.bonus_doros:
                user.doros += badge.bonus_doros
                DorosTransaction.objects.create(
                    student=user, amount=badge.bonus_doros,
                    reason_sk=f"Nový odznak: {badge.name_sk}",
                    reason_en=f"New badge: {badge.name_en}",
                )
            new_badges.append(badge)
    if new_badges:
        user.save(update_fields=['doros'])
    return new_badges


def badge_leaderboard_counts(user_ids):
    return dict(
        StudentBadge.objects.filter(student_id__in=user_ids)
        .values('student_id').annotate(c=Count('id')).values_list('student_id', 'c')
    )
