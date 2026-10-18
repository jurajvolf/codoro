from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User, SchoolClass
from gamification.models import (
    RewardItem, RewardPurchase, DorosTransaction,
    ClassQuest, ClassQuestContribution, CoinDrop, CoinDropClaim
)


class GamificationShopTests(TestCase):
    """
    Testy skladového hospodárstva obchodu (Stock & Restock Marketplace):
    1. Úspešný nákup kupónu s odpočítaním Doros a znížením skladu.
    2. Zabránenie nákupu pri vypredanom sklade (current_stock = 0).
    3. Zabránenie nákupu pri nedostatku Doros.
    4. Automatické doplnenie skladu po uplynutí intervalu (check_and_restock).
    """

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='ucitel_jan', password='password123', role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='peter', password='password123', role='STUDENT', doros=500
        )
        self.reward = RewardItem.objects.create(
            title_sk='Nápoveda na písomke',
            title_en='Test Hint',
            description_sk='Učiteľ ti pošepká 1 radu.',
            description_en='Teacher will give 1 hint.',
            cost_doros=150,
            max_stock=2,
            current_stock=2,
            restock_period=RewardItem.RestockPeriod.DAILY,
            limit_per_student_per_period=1,
            created_by=self.teacher,
            is_active=True
        )

    def test_successful_reward_purchase(self):
        self.client.login(username='peter', password='password123')
        response = self.client.post(reverse('buy_reward', args=[self.reward.id]))
        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()
        self.reward.refresh_from_db()
        self.assertEqual(self.student.doros, 350)  # 500 - 150
        self.assertEqual(self.reward.current_stock, 1)

        purchase = RewardPurchase.objects.filter(student=self.student, reward=self.reward).first()
        self.assertIsNotNone(purchase)
        self.assertTrue(purchase.coupon_code.startswith('CDR-'))
        self.assertEqual(purchase.status, RewardPurchase.Status.PENDING)

        tx = DorosTransaction.objects.filter(student=self.student).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, -150)

    def test_out_of_stock_prevents_purchase(self):
        self.reward.current_stock = 0
        self.reward.save()

        self.client.login(username='peter', password='password123')
        response = self.client.post(reverse('buy_reward', args=[self.reward.id]))
        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()
        self.assertEqual(self.student.doros, 500)
        self.assertEqual(RewardPurchase.objects.count(), 0)

    def test_insufficient_doros_prevents_purchase(self):
        self.student.doros = 50
        self.student.save()

        self.client.login(username='peter', password='password123')
        response = self.client.post(reverse('buy_reward', args=[self.reward.id]))
        self.assertEqual(response.status_code, 302)

        self.student.refresh_from_db()
        self.assertEqual(self.student.doros, 50)
        self.assertEqual(RewardPurchase.objects.count(), 0)

    def test_automatic_restock_after_period(self):
        self.reward.current_stock = 0
        # Posunieme dátum posledného naskladnenia o 2 dni do minulosti
        self.reward.last_restocked_at = timezone.now() - timedelta(days=2)
        self.reward.save()

        self.reward.check_and_restock()
        self.reward.refresh_from_db()
        self.assertEqual(self.reward.current_stock, self.reward.max_stock)


class CollectiveClassQuestTests(TestCase):
    """Testy kolektívnych výziev triedy (ClassQuest)."""

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='ucitelka', password='password123', role='TEACHER'
        )
        self.school_class = SchoolClass.objects.create(
            name='IV.C', join_code='IVC-TEST', teacher=self.teacher
        )
        self.student = User.objects.create_user(
            username='filip', password='password123', role='STUDENT', school_class=self.school_class
        )
        self.class_quest = ClassQuest.objects.create(
            school_class=self.school_class,
            title_sk='Vyriešte 20 úloh za týždeň',
            title_en='Solve 20 tasks this week',
            target_exercises_count=20,
            current_exercises_count=10,
            reward_policy=ClassQuest.RewardPolicy.CONTRIBUTORS_ONLY,
            min_contribution_required=2,
            reward_doros_per_student=100,
            deadline=timezone.now() + timedelta(days=5)
        )

    def test_class_quest_progress_calculation(self):
        self.assertEqual(self.class_quest.progress_pct(), 50)
        self.assertFalse(self.class_quest.is_expired())

    def test_student_contribution_tracking(self):
        contrib, _ = ClassQuestContribution.objects.get_or_create(
            class_quest=self.class_quest, student=self.student
        )
        contrib.amount_contributed += 3
        contrib.save()

        self.assertEqual(contrib.amount_contributed, 3)
        self.assertTrue(contrib.amount_contributed >= self.class_quest.min_contribution_required)
