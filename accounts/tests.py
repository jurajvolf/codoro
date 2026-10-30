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
        self.assertFalse(teacher.is_staff)
        self.assertFalse(teacher.is_admin())

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

    def test_registration_weak_password_fails(self):
        # Pokus o registráciu so slabým heslom (krátke, bez číslic a špeciálnych znakov)
        response = self.client.post(reverse('register'), {
            'role': 'STUDENT',
            'username': 'slabos_ziak',
            'email': 'slabos@skola.sk',
            'password': 'slabe',
            'class_code': 'IVC-TEST',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='slabos_ziak').exists())

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
    def test_custom_404_page(self):
        resp = self.client.get('/neexistujuca-stranka-test-404/')
        self.assertEqual(resp.status_code, 404)
        self.assertContains(resp, '404', status_code=404)
        self.assertContains(resp, 'PAGE_NOT_FOUND', status_code=404)


class PasswordResetTests(TestCase):
    """Testy kompletného toku obnovy zabudnutého hesla (meno/email, token, zmena hesla)."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='peter_test',
            email='peter@codoro.sk',
            password='oldpassword123'
        )

    def test_request_password_reset_page_renders(self):
        resp = self.client.get(reverse('password_reset'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'identity')

    def test_request_reset_by_username_sends_email(self):
        from django.core import mail
        resp = self.client.post(reverse('password_reset'), {'identity': 'peter_test'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('peter@codoro.sk', mail.outbox[0].to)
        self.assertIn('password-reset-confirm', mail.outbox[0].body)

    def test_request_reset_by_email_sends_email(self):
        from django.core import mail
        resp = self.client.post(reverse('password_reset'), {'identity': 'peter@codoro.sk'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('peter@codoro.sk', mail.outbox[0].to)

    def test_request_reset_nonexistent_user_safe(self):
        from django.core import mail
        resp = self.client.post(reverse('password_reset'), {'identity': 'nikto_neexistuje'})
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 0)

    def test_password_reset_confirm_flow(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        # GET confirm page
        confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
        resp = self.client.get(confirm_url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context['validlink'])

        # 1. POST weak password (no digits, no special char)
        resp_weak = self.client.post(confirm_url, {
            'password': 'WeakPassword',
            'password_confirm': 'WeakPassword'
        })
        self.assertEqual(resp_weak.status_code, 200)

        # 2. POST mismatched password
        resp_bad = self.client.post(confirm_url, {
            'password': 'StrongPassword123!',
            'password_confirm': 'DifferentPassword123!'
        })
        self.assertEqual(resp_bad.status_code, 200)

        # 3. POST valid strong new password
        resp_ok = self.client.post(confirm_url, {
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!'
        })
        self.assertEqual(resp_ok.status_code, 302)
        self.assertRedirects(resp_ok, reverse('password_reset_complete'))

        # Verify old password no longer works, new password works
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('oldpassword123'))
        self.assertTrue(self.user.check_password('StrongPassword123!'))

    def test_password_reset_rejects_previous_3_passwords(self):
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.auth.tokens import default_token_generator

        # 1. Pôvodné heslo je v histórii
        self.user.record_password_change('FirstSecretPass1!')
        self.user.record_password_change('SecondSecretPass2!')
        self.user.record_password_change('ThirdSecretPass3!')

        # Vygenerujeme nový reset token
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        confirm_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})

        # Pokus o nastavenie hesla zhodného s ThirdSecretPass3! (aktuálne heslo)
        resp_cur = self.client.post(confirm_url, {
            'password': 'ThirdSecretPass3!',
            'password_confirm': 'ThirdSecretPass3!'
        })
        self.assertEqual(resp_cur.status_code, 200)
        self.assertContains(resp_cur, 'posledn')

        # Pokus o nastavenie hesla zhodného so SecondSecretPass2! (1. z histórie)
        resp_hist1 = self.client.post(confirm_url, {
            'password': 'SecondSecretPass2!',
            'password_confirm': 'SecondSecretPass2!'
        })
        self.assertEqual(resp_hist1.status_code, 200)
        self.assertContains(resp_hist1, 'posledn')

        # Pokus o nastavenie hesla zhodného s FirstSecretPass1! (2. z histórie)
        resp_hist2 = self.client.post(confirm_url, {
            'password': 'FirstSecretPass1!',
            'password_confirm': 'FirstSecretPass1!'
        })
        self.assertEqual(resp_hist2.status_code, 200)
        self.assertContains(resp_hist2, 'posledn')

        # Nové, úplne odlišné silné heslo musí prejsť
        resp_fresh = self.client.post(confirm_url, {
            'password': 'BrandNewStrongPass4!',
            'password_confirm': 'BrandNewStrongPass4!'
        })
        self.assertEqual(resp_fresh.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BrandNewStrongPass4!'))




class SecurityAndMobileUXTests(TestCase):
    """
    FÁZA 26: Testy bezpečnosti (OWASP, CSP hlavičky, Rate Limiting, Honeypot,
    Open Redirect, Row-Level Security, šifrovanie dát, validácia uploadov)
    a mobilnej responzivity.
    """

    def setUp(self):
        from django.core.cache import cache
        cache.clear()
        self.student = User.objects.create_user(
            username='sec_student', password='Password123!', role=User.Role.STUDENT
        )

    def tearDown(self):
        from django.core.cache import cache
        cache.clear()

    def test_security_headers_present_on_responses(self):
        resp = self.client.get(reverse('landing_page'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Content-Security-Policy', resp.headers)
        self.assertIn("frame-ancestors 'none'", resp.headers['Content-Security-Policy'])
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(resp.headers.get('Referrer-Policy'), 'strict-origin-when-cross-origin')
        self.assertIn('Permissions-Policy', resp.headers)
        self.assertEqual(resp.headers.get('Cross-Origin-Opener-Policy'), 'same-origin')

    def test_honeypot_blocks_bot_login_and_registration(self):
        # Bot vyplní skryté pole website_url pri prihlásení
        resp_login = self.client.post(reverse('login'), {
            'username': 'sec_student',
            'password': 'Password123!',
            'website_url': 'http://spam-bot.example.com',
        })
        self.assertEqual(resp_login.status_code, 200)
        self.assertFalse(resp_login.wsgi_request.user.is_authenticated)

        # Bot vyplní skryté pole website_url pri registrácii
        resp_reg = self.client.post(reverse('register'), {
            'role': 'STUDENT',
            'username': 'bot_account',
            'email': 'bot@spam.com',
            'password': 'Password123!',
            'website_url': 'http://spam-bot.example.com',
        })
        self.assertEqual(resp_reg.status_code, 200)
        self.assertFalse(User.objects.filter(username='bot_account').exists())

    def test_login_rate_limiting_blocks_brute_force(self):
        for _ in range(10):
            self.client.post(reverse('login'), {
                'username': 'sec_student',
                'password': 'WrongPassword!',
            })
        # 11. pokus musí byť zablokovaný rate limiterom (HTTP 429 Too Many Requests) aj so správnym heslom
        resp = self.client.post(reverse('login'), {
            'username': 'sec_student',
            'password': 'Password123!',
        })
        self.assertEqual(resp.status_code, 429)
        self.assertFalse(resp.wsgi_request.user.is_authenticated)

    def test_open_redirect_protection_on_language_switch(self):
        resp = self.client.get(reverse('switch_language', kwargs={'lang_code': 'en'}) + '?next=https://evil-phishing.com')
        self.assertEqual(resp.status_code, 302)
        self.assertNotIn('evil-phishing.com', resp['Location'])

    def test_row_level_security_prevents_cross_teacher_student_access(self):
        teacher_a = User.objects.create_user(username='teacher_a', password='Password123!', role=User.Role.TEACHER)
        teacher_b = User.objects.create_user(username='teacher_b', password='Password123!', role=User.Role.TEACHER)
        class_a = SchoolClass.objects.create(name='IV.A', join_code='IVA-RLS', teacher=teacher_a)
        class_b = SchoolClass.objects.create(name='IV.B', join_code='IVB-RLS', teacher=teacher_b)

        student_b = User.objects.create_user(
            username='student_in_b', password='Password123!', role=User.Role.STUDENT, school_class=class_b
        )

        # Teacher A sa pokúsi zobraziť detail študenta z triedy Teacher B (IDOR pokus)
        self.client.login(username='teacher_a', password='Password123!')
        resp = self.client.get(reverse('teacher_student_detail', kwargs={'student_id': student_b.id}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('teacher_dashboard'))

    def test_admin_route_protected_against_students(self):
        self.client.login(username='sec_student', password='Password123!')
        resp = self.client.get('/admin/')
        self.assertEqual(resp.status_code, 302)

    def test_safe_int_and_encrypt_decrypt_helpers(self):
        from accounts.security import (
            safe_int, sanitize_text, encrypt_sensitive_data, decrypt_sensitive_data, validate_uploaded_file
        )
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.assertEqual(safe_int('not-a-number', default=42), 42)
        self.assertEqual(safe_int('999999', default=10, min_val=1, max_val=100), 100)
        self.assertEqual(sanitize_text('Hello\x00World', max_length=20), 'HelloWorld')

        # Šifrovanie a dešifrovanie citlivých údajov
        secret_note = 'Citlivý záznam študenta IV.C'
        token = encrypt_sensitive_data(secret_note)
        self.assertNotEqual(token, secret_note)
        self.assertEqual(decrypt_sensitive_data(token), secret_note)
        self.assertIsNone(decrypt_sensitive_data(token + 'tampered'))

        # Validácia nahrávaných súborov (Magic Bytes & Extension Allowlist)
        bad_file = SimpleUploadedFile('malware.exe', b'MZ\x90\x00\x03', content_type='application/octet-stream')
        ok_bad, _ = validate_uploaded_file(bad_file)
        self.assertFalse(ok_bad)

        fake_png = SimpleUploadedFile('avatar.png', b'not-a-real-png-header', content_type='image/png')
        ok_fake, _ = validate_uploaded_file(fake_png)
        self.assertFalse(ok_fake)

        valid_png = SimpleUploadedFile('avatar.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', content_type='image/png')
        ok_valid, _ = validate_uploaded_file(valid_png)
        self.assertTrue(ok_valid)

    def test_teacher_cannot_access_superadmin_panel(self):
        teacher = User.objects.create_user(
            username='teacher_audit_test',
            password='Password123!',
            role=User.Role.TEACHER,
            subscription_tier=User.SubscriptionTier.EDU,
            is_staff=False
        )
        self.assertFalse(teacher.is_admin())
        self.client.login(username='teacher_audit_test', password='Password123!')
        resp = self.client.get('/admin-panel/')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('dashboard'))

    def test_repair_streak_requires_post(self):
        self.client.login(username='sec_student', password='Password123!')
        self.student.lost_streak_value = 5
        self.student.doros = 500
        self.student.save()

        get_resp = self.client.get(reverse('repair_streak'))
        self.assertEqual(get_resp.status_code, 405)

        post_resp = self.client.post(reverse('repair_streak'))
        self.assertEqual(post_resp.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.doros, 300)
        self.assertEqual(self.student.current_streak, 5)

    def test_password_reset_does_not_leak_token_in_session(self):
        resp = self.client.post(reverse('password_reset'), {
            'identity': 'sec_student',
            'website_url': ''
        })
        self.assertEqual(resp.status_code, 302)
        self.assertIsNone(self.client.session.get('dev_reset_url'))

        done_resp = self.client.get(reverse('password_reset_done'))
        self.assertNotIn('dev_reset_url', done_resp.context or {})
        self.assertNotIn('password-reset-confirm', done_resp.content.decode('utf-8'))
