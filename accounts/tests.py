from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import User, SchoolClass, SubscriptionLicense


class UserLevelAndGamificationTests(TestCase):
    """
    Testy matematického modelu progresie (Rovnica 1 zo zadania práce):
    XP = 100 * (Level - 1)^1.5
    a prideľovania odmien Doros pri level-upe.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='jakub', password='password123', xp=0, level=1, doros=50
        )

    def test_level_progression_formula(self):
        # Na začiatku XP 0 -> Level 1
        self.assertEqual(self.user.calculate_level_from_xp(), 1)
        self.assertEqual(self.user.xp_for_next_level(), 100)

        # Pri 100 XP -> Level 2
        self.user.xp = 100
        self.assertEqual(self.user.calculate_level_from_xp(), 2)

        # Pri 283 XP -> Level 3 (pretože 100 * 2^1.5 ≈ 282.84)
        self.user.xp = 285
        self.assertEqual(self.user.calculate_level_from_xp(), 3)

    def test_level_up_awards_bonus_doros(self):
        initial_doros = self.user.doros
        # Pridáme 150 XP, čo používateľa posunie z Levelu 1 na Level 2
        # Odmena za Level 2 je: 2 * 50 = 100 Doros
        bonus = self.user.add_xp_and_check_level_up(150)
        self.assertEqual(self.user.level, 2)
        self.assertEqual(bonus, 100)
        self.assertEqual(self.user.doros, initial_doros + 100)


class DailyStreakTests(TestCase):
    """Testy dennej série (Streak), jej vyhasnutia a záchrany za 200 Doros."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='simona', password='password123', doros=300
        )

    def test_register_activity_extends_streak(self):
        today = timezone.localdate()
        self.user.last_activity_date = today - timedelta(days=1)
        self.user.current_streak = 3

        changed = self.user.register_activity()
        self.assertTrue(changed)
        self.assertEqual(self.user.current_streak, 4)
        self.assertEqual(self.user.last_activity_date, today)

    def test_missed_day_triggers_streak_loss_window(self):
        today = timezone.localdate()
        self.user.last_activity_date = today - timedelta(days=2)
        self.user.current_streak = 5
        self.user.streak_freezes = 0

        changed = self.user.refresh_streak_state()
        self.assertTrue(changed)
        self.assertEqual(self.user.current_streak, 0)
        self.assertEqual(self.user.lost_streak_value, 5)
        self.assertIsNotNone(self.user.streak_lost_at)

    def test_streak_repair_view_restores_streak(self):
        self.client.login(username='simona', password='password123')
        self.user.lost_streak_value = 7
        self.user.current_streak = 0
        self.user.streak_lost_at = timezone.now()
        self.user.doros = 300
        self.user.save()

        response = self.client.post(reverse('repair_streak'))
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.current_streak, 7)
        self.assertEqual(self.user.lost_streak_value, 0)
        self.assertEqual(self.user.doros, 100)  # 300 - 200 = 100


class SubscriptionLicenseTests(TestCase):
    """Testy aktivácie školských licencií EDU a limitov AI tútora."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='tomas', password='password123', subscription_tier='FREE'
        )
        self.license = SubscriptionLicense.objects.create(
            code='EDU-2027-TEST',
            tier='EDU',
            max_uses=5,
            current_uses=0,
            is_active=True
        )

    def test_license_activation_upgrades_tier(self):
        self.client.login(username='tomas', password='password123')
        response = self.client.post(reverse('activate_license'), {'license_code': 'EDU-2027-TEST'})
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.license.refresh_from_db()
        self.assertEqual(self.user.subscription_tier, 'EDU')
        self.assertEqual(self.license.current_uses, 1)

    def test_free_user_ai_hint_daily_limits(self):
        self.assertEqual(self.user.ai_hints_remaining(), 5)
        for _ in range(5):
            allowed = self.user.consume_ai_hint()
            self.assertTrue(allowed)

        # 6. pokus v ten istý deň musí byť zamietnutý
        self.assertFalse(self.user.consume_ai_hint())
        self.assertEqual(self.user.ai_hints_remaining(), 0)

        # PRO a EDU účty majú neobmedzené rady
        self.user.subscription_tier = 'PRO'
        self.user.save()
        self.assertIsNone(self.user.ai_hints_remaining())
        self.assertTrue(self.user.consume_ai_hint())
