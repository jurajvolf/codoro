from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from accounts.models import User, SchoolClass
from courses.models import Lesson, Exercise, TestCase, Submission
from gamification.models import (
    RewardItem, RewardPurchase, DorosTransaction, ClassQuest, CoinDrop, Quest
)
from courses.services import generate_exercise_with_ai, translate_to_english


def teacher_required(view_func):
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_teacher():
            messages.error(request, "Prístup povolený iba pre účet učiteľa.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped


@teacher_required
def teacher_dashboard(request):
    students = User.objects.filter(role=User.Role.STUDENT).select_related('school_class').order_by('-xp')
    pending_coupons = RewardPurchase.objects.filter(status=RewardPurchase.Status.PENDING).select_related('student', 'reward')
    rewards = RewardItem.objects.all()
    recent_submissions = Submission.objects.select_related('student', 'exercise')[:25]
    lessons = Lesson.objects.select_related('module').all()
    classes = SchoolClass.objects.all()
    active_drops = CoinDrop.objects.order_by('-available_from')[:5]
    all_quests = Quest.objects.all().order_by('period', '-id')
    class_quests = ClassQuest.objects.select_related('school_class').order_by('-deadline')[:10]

    return render(request, 'teacher_panel/dashboard.html', {
        'students': students,
        'pending_coupons': pending_coupons,
        'rewards': rewards,
        'recent_submissions': recent_submissions,
        'lessons': lessons,
        'classes': classes,
        'active_drops': active_drops,
        'all_quests': all_quests,
        'class_quests': class_quests,
    })


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
        decision = request.POST.get('decision')

        if purchase.status != RewardPurchase.Status.PENDING:
            return redirect('teacher_dashboard')

        purchase.processed_at = timezone.now()
        purchase.processed_by = request.user

        if decision == 'approve':
            purchase.status = RewardPurchase.Status.REDEEMED
            purchase.save()
            messages.success(request, f"Kupón {purchase.coupon_code} ({purchase.student.username}) bol schválený a uplatnený.")
        elif decision == 'refund':
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
    """Vytvorenie novej odmeny do obchodu s nastavením ceny, zásob a intervalu obnovy."""
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
        messages.success(request, f"🎁 Coin Drop '{title}' bol spustený na {duration_minutes} minút pre prvých {max_claims} študentov!")
    return redirect('teacher_dashboard')


@teacher_required
def create_exercise(request):
    """Pridanie nového praktického cvičenia v Pythone spolu s automatickým assert testom."""
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
    """API endpoint: Preloží zadanie cvičenia zo slovenčiny do angličtiny."""
    title_sk = request.GET.get('title_sk', '')
    instructions_sk = request.GET.get('instructions_sk', '')
    hint_sk = request.GET.get('hint_sk', '')
    data = translate_to_english({
        'title_en': title_sk,
        'instructions_en': instructions_sk,
        'hint_en': hint_sk,
    })
    return JsonResponse(data)