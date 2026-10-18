from django.test import TestCase
from django.urls import reverse
from accounts.models import User, SchoolClass
from courses.models import Module, Lesson, Exercise, Submission
from gamification.models import RewardItem, RewardPurchase


class TeacherPanelPermissionAndReviewTests(TestCase):
    """
    Testy administrátorského rozhrania učiteľa (Teacher Studio):
    1. Ochrana prístupu: žiak nemá prístup k Teacher Studiu (redirect).
    2. Učiteľ má plný prístup k ovládaciemu panelu triedy.
    3. Pridanie slovného hodnotenia (Code Review) ku konkrétnemu odovzdanému riešeniu žiaka.
    4. Schválenie a zamietnutie kupónu učiteľom s refundáciou mincí.
    """

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='pan_ucitel', password='password123', role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='ondrej', password='password123', role='STUDENT', doros=200
        )
        self.school_class = SchoolClass.objects.create(
            name='IV.C', join_code='IVC-DEMO', teacher=self.teacher
        )
        self.student.school_class = self.school_class
        self.student.save()

        self.module = Module.objects.create(title_sk='Modul', title_en='Module', order=1)
        self.lesson = Lesson.objects.create(module=self.module, title_sk='Lekcia', title_en='Lesson', order=1)
        self.exercise = Exercise.objects.create(lesson=self.lesson, title_sk='Úloha', title_en='Exercise', order=1)
        self.submission = Submission.objects.create(
            student=self.student,
            exercise=self.exercise,
            submitted_code="print('Hello World')",
            status='PASSED',
            output_log="OK"
        )
        self.reward = RewardItem.objects.create(
            title_sk='Odpustenie DÚ',
            title_en='Forgive HW',
            cost_doros=100,
            created_by=self.teacher
        )
        self.purchase = RewardPurchase.objects.create(
            student=self.student,
            reward=self.reward,
            coupon_code='CDR-TEST99',
            cost_paid=100,
            status=RewardPurchase.Status.PENDING
        )

    def test_student_cannot_access_teacher_panel(self):
        self.client.login(username='ondrej', password='password123')
        response = self.client.get(reverse('teacher_dashboard'))
        # Študent je presmerovaný na dashboard so správou o nepovolenom prístupe
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('dashboard'), response.url)

    def test_teacher_can_access_teacher_panel(self):
        self.client.login(username='pan_ucitel', password='password123')
        response = self.client.get(reverse('teacher_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_teacher_code_review_comment(self):
        self.client.login(username='pan_ucitel', password='password123')
        response = self.client.post(
            reverse('comment_submission', args=[self.submission.id]),
            {'teacher_comment': 'Výborná a čistá práca, správne odsadenie!'}
        )
        self.assertEqual(response.status_code, 302)

        self.submission.refresh_from_db()
        self.assertEqual(self.submission.teacher_comment, 'Výborná a čistá práca, správne odsadenie!')

    def test_teacher_rejects_and_refunds_coupon(self):
        self.client.login(username='pan_ucitel', password='password123')
        response = self.client.post(
            reverse('process_coupon', args=[self.purchase.id]),
            {'decision': 'refund'}
        )
        self.assertEqual(response.status_code, 302)

        self.purchase.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.purchase.status, RewardPurchase.Status.REFUNDED)
        self.assertEqual(self.student.doros, 300)  # 200 + 100 vrátených
