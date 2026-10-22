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


class TeacherRegistrationAndLicenseTests(TestCase):
    """Testy duálnej registrácie (študent / učiteľ), školskej licencie a žiadostí o pilotný kľúč."""

    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='pedagog_base', password='password123', role=User.Role.TEACHER
        )
        self.school_class = SchoolClass.objects.create(
            name='IV.C',
            join_code='IVC-TEST',
            teacher=self.teacher_user,
        )
        self.edu_license = SubscriptionLicense.objects.create(
            code='EDU-TEACHER-KEY',
            tier=User.SubscriptionTier.EDU,
            max_uses=30,
            current_uses=0,
            is_active=True
        )

    def test_student_registration_with_class_code(self):
        response = self.client.post(reverse('register'), {
            'role': 'STUDENT',
            'username': 'novy_ziak',
            'email': 'ziak@skola.sk',
            'password': 'Password123!',
            'class_code': 'IVC-TEST',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='novy_ziak')
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertEqual(user.school_class, self.school_class)

    def test_teacher_registration_with_valid_key(self):
        response = self.client.post(reverse('register'), {
            'role': 'TEACHER',
            'username': 'novy_ucitel',
            'first_name': 'Ján',
            'last_name': 'Kováč',
            'email': 'kovac@skola.sk',
            'password': 'Password123!',
            'school_license_key': 'EDU-TEACHER-KEY',
            'initial_class_name': 'III.B',
        })
        self.assertEqual(response.status_code, 302)
        teacher = User.objects.get(username='novy_ucitel')
        self.assertEqual(teacher.role, User.Role.TEACHER)
        self.assertEqual(teacher.subscription_tier, User.SubscriptionTier.EDU)
        self.assertTrue(teacher.is_staff)

        # Overenie vytvorenia triedy
        created_class = SchoolClass.objects.filter(teacher=teacher, name='III.B').first()
        self.assertIsNotNone(created_class)
        self.assertTrue(created_class.join_code.startswith('IIIB-'))

    def test_teacher_registration_with_pilot_fallback(self):
        # Ak učiteľ nemá kľúč, systém mu automaticky vygeneruje 30-dňový pilotný EDU kľúč
        response = self.client.post(reverse('register'), {
            'role': 'TEACHER',
            'username': 'pilot_ucitel',
            'first_name': 'Eva',
            'last_name': 'Biela',
            'email': 'biela@gymnazium.sk',
            'password': 'Password123!',
            'school_license_key': '',
            'initial_class_name': 'Sexta A',
        })
        self.assertEqual(response.status_code, 302)
        teacher = User.objects.get(username='pilot_ucitel')
        self.assertEqual(teacher.role, User.Role.TEACHER)
        self.assertEqual(teacher.subscription_tier, User.SubscriptionTier.EDU)

        # Pilotný kľúč bol automaticky vystavený v DB
        pilot_license = SubscriptionLicense.objects.filter(tier='EDU', max_uses=35).first()
        self.assertIsNotNone(pilot_license)

        # Trieda bola vytvorená
        created_class = SchoolClass.objects.filter(teacher=teacher, name='Sexta A').first()
        self.assertIsNotNone(created_class)

    def test_teacher_registration_invalid_key_fails(self):
        response = self.client.post(reverse('register'), {
            'role': 'TEACHER',
            'username': 'fake_ucitel',
            'email': 'fake@skola.sk',
            'password': 'Password123!',
            'school_license_key': 'NEEXISTUJUCI-KLUČ',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='fake_ucitel').exists())

    def test_get_license_portal_view(self):
        # GET
        response = self.client.get(reverse('get_license'))
        self.assertEqual(response.status_code, 200)

        # POST pre okamžité vygenerovanie pilotného EDU kľúča
        post_data = {
            'school_name': 'Stredná odborná škola technická',
            'school_city': 'Nižná',
            'contact_person': 'Ing. Peter Novák',
            'email': 'novak@skola-technicka.sk',
            'phone': '+421901234567',
            'expected_students': 35,
            'note': 'Pilotná výučba triedy programovania',
        }
        resp_post = self.client.post(reverse('get_license'), post_data)
        self.assertEqual(resp_post.status_code, 200)
        self.assertIn('generated_license', resp_post.context)

        from accounts.models import SchoolLicenseRequest
        req = SchoolLicenseRequest.objects.filter(email='novak@skola-technicka.sk').first()
        self.assertIsNotNone(req)
        self.assertEqual(req.status, SchoolLicenseRequest.Status.PENDING)
        self.assertIsNotNone(req.generated_license)
        self.assertTrue(req.generated_license.code.startswith('EDU-'))


class LanguageSwitchingTests(TestCase):
    """Testy prepínania jazyka (SK/EN) pre prihlásených aj neprihlásených používateľov."""

    def test_anonymous_user_switches_language(self):
        # 1. Počiatočná návšteva landing page má predvolene slovenčinu
        resp1 = self.client.get(reverse('landing_page'))
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp1.context['lang'], 'sk')
        self.assertContains(resp1, 'Nauč sa Python praxou')

        # 2. Kliknutie na prepínač na angličtinu (/lang/en/)
        resp_switch = self.client.get(reverse('switch_language', kwargs={'lang_code': 'en'}))
        self.assertEqual(resp_switch.status_code, 302)

        # 3. Následná návšteva zobrazí anglické texty
        resp2 = self.client.get(reverse('landing_page'))
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.context['lang'], 'en')
        self.assertContains(resp2, 'Learn Python by Doing')

        # 4. Prepnutie späť na slovenčinu (/lang/sk/)
        self.client.get(reverse('switch_language', kwargs={'lang_code': 'sk'}))
        resp3 = self.client.get(reverse('landing_page'))
        self.assertEqual(resp3.context['lang'], 'sk')
        self.assertContains(resp3, 'Nauč sa Python praxou')

    def test_authenticated_user_switches_language(self):
        user = User.objects.create_user(username='filip', password='heslo123', preferred_language='sk')
        self.client.login(username='filip', password='heslo123')

        # Prepnutie na EN
        self.client.get(reverse('switch_language', kwargs={'lang_code': 'en'}))
        user.refresh_from_db()
        self.assertEqual(user.preferred_language, 'en')

        # Dashboard v EN
        resp = self.client.get(reverse('dashboard'))
        self.assertEqual(resp.context['lang'], 'en')


class PublicPagesAndSEOTests(TestCase):
    def test_privacy_policy_page(self):
        resp = self.client.get(reverse('privacy_policy'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Zásady ochrany osobných údajov')

    def test_terms_of_service_page(self):
        resp = self.client.get(reverse('terms_of_service'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Všeobecné podmienky používania')

    def test_thank_you_page(self):
        resp = self.client.get(reverse('thank_you') + '?type=license')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Ďakujeme')

    def test_robots_txt(self):
        resp = self.client.get('/robots.txt')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/plain')
        self.assertIn('User-agent: *', resp.content.decode('utf-8'))
        self.assertIn('Sitemap:', resp.content.decode('utf-8'))

    def test_sitemap_xml(self):
        resp = self.client.get('/sitemap.xml')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/xml')
        self.assertIn('<urlset', resp.content.decode('utf-8'))
        self.assertIn('https://codoro.sk/welcome/', resp.content.decode('utf-8'))

    def test_custom_404_page(self):
        resp = self.client.get('/neexistujuca-stranka-test-404/')
        self.assertEqual(resp.status_code, 404)
        self.assertContains(resp, '404', status_code=404)
        self.assertContains(resp, 'PAGE_NOT_FOUND', status_code=404)


