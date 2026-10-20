import json
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase as ExerciseTestCase, Submission


class SuperAdminPanelTests(TestCase):
    """Komplexné testy pre SuperAdmin Portál a Support Helpdesk."""

    def setUp(self):
        self.client = Client()

        # 1. SuperAdmin používateľ
        self.admin = User.objects.create_superuser(
            username='admin_test',
            password='password123',
            email='admin@codoro.sk',
            role=User.Role.ADMIN
        )

        # 2. Učiteľ
        self.teacher = User.objects.create_user(
            username='teacher_test',
            password='password123',
            role=User.Role.TEACHER
        )

        # 3. Študent
        self.student = User.objects.create_user(
            username='student_test',
            password='oldpassword123',
            role=User.Role.STUDENT,
            xp=250,
            level=2,
            doros=100,
            current_streak=5,
            daily_ai_hints_used=4
        )

        # 4. Školská trieda
        self.school_class = SchoolClass.objects.create(
            name='IV.C - IMT',
            join_code='IVC-TEST',
            teacher=self.teacher
        )

        # 5. Modul a cvičenie
        self.module = Module.objects.create(
            title_sk='Základy',
            title_en='Basics',
            order=1,
            is_pro_only=False,
            is_published=True
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title_sk='Premenné',
            title_en='Variables',
            order=1,
            content_sk='Teória...',
            content_en='Theory...'
        )
        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            title_sk='Úloha 1',
            title_en='Task 1',
            order=1,
            starter_code='x = 1',
            solution_code='x = 2'
        )

    def test_unauthenticated_user_redirected(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_student_forbidden_from_admin_panel(self):
        self.client.login(username='student_test', password='oldpassword123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_teacher_forbidden_without_admin_role(self):
        self.client.login(username='teacher_test', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_admin_can_access_dashboard(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertContains(response, "Centrálna administrácia")
        # Overenie aj v angličtine
        self.admin.preferred_language = 'en'
        self.admin.save()
        resp_en = self.client.get(reverse('admin_dashboard'))
        self.assertContains(resp_en, "Platform Control Center")

    def test_admin_reset_user_password(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(
            reverse('admin_user_set_password', args=[self.student.id]),
            {'action': 'set', 'new_password': 'NewSecurePass2027!'}
        )
        self.assertEqual(response.status_code, 302)

        # Overíme, že sa študent vie prihlásiť s novým heslom
        self.client.logout()
        login_success = self.client.login(username='student_test', password='NewSecurePass2027!')
        self.assertTrue(login_success)

    def test_admin_auto_generate_password(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(
            reverse('admin_user_set_password', args=[self.student.id]),
            {'action': 'generate'}
        )
        self.assertEqual(response.status_code, 302)
        # Používateľ má zmenené heslo (staré už nefunguje)
        self.student.refresh_from_db()
        self.assertFalse(self.student.check_password('oldpassword123'))

    def test_admin_repair_streak(self):
        self.client.login(username='admin_test', password='password123')
        self.student.lost_streak_value = 14
        self.student.streak_lost_at = timezone.now()
        self.student.save()

        response = self.client.post(
            reverse('admin_user_streak', args=[self.student.id]),
            {'streak_value': 14}
        )
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.current_streak, 14)
        self.assertEqual(self.student.lost_streak_value, 0)
        self.assertIsNone(self.student.streak_lost_at)

    def test_admin_adjust_economy(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(
            reverse('admin_user_economy', args=[self.student.id]),
            {'doros_change': 150, 'xp_change': 300, 'reason': 'Support bonus'}
        )
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.doros, 250)
        self.assertEqual(self.student.xp, 550)

    def test_admin_reset_ai_hints_limit(self):
        self.client.login(username='admin_test', password='password123')
        self.assertEqual(self.student.daily_ai_hints_used, 4)
        response = self.client.post(reverse('admin_user_reset_ai', args=[self.student.id]))
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.daily_ai_hints_used, 0)

    def test_admin_assign_school_class(self):
        self.client.login(username='admin_test', password='password123')
        self.assertIsNone(self.student.school_class)
        response = self.client.post(
            reverse('admin_user_assign_class', args=[self.student.id]),
            {'school_class_id': self.school_class.id}
        )
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.school_class, self.school_class)

    def test_admin_toggle_user_active(self):
        self.client.login(username='admin_test', password='password123')
        self.assertTrue(self.student.is_active)
        response = self.client.post(reverse('admin_user_toggle_active', args=[self.student.id]))
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)

    def test_admin_cannot_block_self(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.post(reverse('admin_user_toggle_active', args=[self.admin.id]))
        self.assertEqual(response.status_code, 302)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_admin_create_and_assign_license(self):
        self.client.login(username='admin_test', password='password123')

        # 1. Vytvorenie licencie
        response = self.client.post(reverse('admin_license_create'), {
            'tier': 'PRO',
            'max_uses': 10,
            'code': 'PRO-TEST-999'
        })
        self.assertEqual(response.status_code, 302)
        lic = SubscriptionLicense.objects.get(code='PRO-TEST-999')
        self.assertEqual(lic.tier, 'PRO')

        # 2. Priame priradenie študentovi
        response2 = self.client.post(reverse('admin_license_quick_assign'), {
            'username': 'student_test',
            'license_id': lic.id
        })
        self.assertEqual(response2.status_code, 302)
        self.student.refresh_from_db()
        lic.refresh_from_db()
        self.assertEqual(self.student.subscription_tier, 'PRO')
        self.assertEqual(lic.current_uses, 1)

    def test_admin_module_toggle_pro(self):
        self.client.login(username='admin_test', password='password123')
        self.assertFalse(self.module.is_pro_only)
        response = self.client.post(reverse('admin_module_toggle_pro', args=[self.module.id]))
        self.assertEqual(response.status_code, 302)
        self.module.refresh_from_db()
        self.assertTrue(self.module.is_pro_only)

    def test_admin_export_backup_json(self):
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(reverse('admin_export_backup_json'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        payload = json.loads(response.content)
        self.assertIn('users', payload)
        self.assertIn('school_classes', payload)
        self.assertIn('licenses', payload)
        self.assertIn('modules_summary', payload)
