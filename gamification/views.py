import random
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from .models import (
    RewardItem, RewardPurchase, DorosTransaction,
    StudentQuestProgress, CoinDrop, CoinDropClaim
)


@login_required
def shop_view(request):
    rewards = RewardItem.objects.filter(is_active=True)
    for item in rewards:
        item.check_and_restock()

    my_coupons = RewardPurchase.objects.filter(student=request.user).select_related('reward').order_by('-purchased_at')
    transactions = DorosTransaction.objects.filter(student=request.user)[:15]

    return render(request, 'gamification/shop.html', {
        'rewards': rewards,
        'my_coupons': my_coupons,
        'transactions': transactions,
    })


@login_required
@transaction.atomic
def buy_reward(request, reward_id):
    if request.method != 'POST':
        return redirect('shop')

    user = request.user
    reward = get_object_or_404(RewardItem.objects.select_for_update(), id=reward_id, is_active=True)
    reward.check_and_restock()

    if reward.current_stock <= 0:
        messages.error(request, "Táto odmena je momentálne vypredaná! Počkaj na ďalšie automatické obnovenie skladu.")
        return redirect('shop')

    if user.doros < reward.cost_doros:
        messages.error(request, "Nemáš dostatok mincí Doros na zakúpenie tejto odmeny.")
        return redirect('shop')

    # Kontrola osobného limitu na žiaka v aktuálnom období obnovy
    recent_purchases = RewardPurchase.objects.filter(
        student=user,
        reward=reward,
        purchased_at__gte=reward.last_restocked_at
    ).exclude(status=RewardPurchase.Status.REFUNDED).count()

    if recent_purchases >= reward.limit_per_student_per_period:
        messages.warning(request, f"Dosiahol si maximálny limit ({reward.limit_per_student_per_period} ks) pre túto odmenu v aktuálnom období.")
        return redirect('shop')

    # Odpočítanie skladu a mincí
    reward.current_stock -= 1
    reward.save()

    user.doros -= reward.cost_doros
    user.save()

    coupon_code = f"CDR-{uuid.uuid4().hex[:6].upper()}"
    RewardPurchase.objects.create(
        student=user,
        reward=reward,
        coupon_code=coupon_code,
        cost_paid=reward.cost_doros
    )

    DorosTransaction.objects.create(
        student=user,
        amount=-reward.cost_doros,
        reason_sk=f"Nákup odmeny: {reward.title_sk} (Kupón {coupon_code})",
        reason_en=f"Purchased reward: {reward.title_en} (Coupon {coupon_code})"
    )

    messages.success(request, f"🎁 Odmena zakúpená! Tvoj kód kupónu pre učiteľa je: {coupon_code}")
    return redirect('shop')


@login_required
@transaction.atomic
def claim_quest_reward(request, progress_id):
    if request.method == 'POST':
        prog = get_object_or_404(
            StudentQuestProgress.objects.select_for_update(),
            id=progress_id, student=request.user
        )
        if prog.is_completed and not prog.is_claimed:
            prog.is_claimed = True
            prog.save()

            user = request.user
            user.doros += prog.quest.reward_doros
            user.add_xp_and_check_level_up(prog.quest.reward_xp)
            user.save()

            DorosTransaction.objects.create(
                student=user,
                amount=prog.quest.reward_doros,
                reason_sk=f"Splnený Quest: {prog.quest.title_sk}",
                reason_en=f"Completed Quest: {prog.quest.title_en}"
            )
            messages.success(request, f"🏆 Odmena za Quest pripísaná: +{prog.quest.reward_doros} Doros a +{prog.quest.reward_xp} XP!")
    return redirect('dashboard')


@login_required
@transaction.atomic
def claim_coin_drop(request, drop_id):
    if request.method == 'POST':
        drop = get_object_or_404(CoinDrop.objects.select_for_update(), id=drop_id)
        user = request.user

        if CoinDropClaim.objects.filter(coin_drop=drop, student=user).exists():
            messages.warning(request, "Tento Coin Drop si si už vyzdvihol!")
            return redirect('dashboard')

        if not drop.is_currently_active():
            messages.error(request, "Neskorý klik! Tento Coin Drop už vypršal alebo ho vyzbierali spolužiaci.")
            return redirect('dashboard')

        won_amount = random.randint(drop.min_doros, drop.max_doros)
        CoinDropClaim.objects.create(coin_drop=drop, student=user, amount_won=won_amount)

        user.doros += won_amount
        user.save()

        DorosTransaction.objects.create(
            student=user,
            amount=won_amount,
            reason_sk=f"Chytený Coin Drop: {drop.title_sk}",
            reason_en=f"Claimed Coin Drop: {drop.title_en}"
        )
        messages.success(request, f"🎉 Blesková reakcia! Z Coin Dropu ti padlo +{won_amount} Doros!")
    return redirect('dashboard')