from django.test import TestCase
from django.urls import reverse
from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase as CourseTestCase, Submission, QuizQuestion
from gamification.models import RewardItem, RewardPurchase, ClassQuest, ClassQuestContribution, Quest


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
            max_stock=3,
            current_stock=1,
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
        self.assertEqual(self.student.doros, 300)

    def test_teacher_approves_coupon(self):
        self.client.login(username='pan_ucitel', password='password123')
        response = self.client.post(
            reverse('process_coupon', args=[self.purchase.id]),
            {'decision': 'approve'}
        )
        self.assertEqual(response.status_code, 302)
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.status, RewardPurchase.Status.REDEEMED)


class TeacherCMSStudioTests(TestCase):
    """Komplexné testy pre Phase 6 CMS Štúdio (Moduly, Lekcie, Cvičenia, Testy, Kvízy, Odmeny a Triedy)."""

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='profesor_codo', password='password123', role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='student_jakub', password='password123', role='STUDENT', doros=50
        )
        self.school_class = SchoolClass.objects.create(
            name='IV.C', join_code='IVC-2027', teacher=self.teacher
        )
        self.student.school_class = self.school_class
        self.student.save()
        self.client.login(username='profesor_codo', password='password123')

    def test_cms_module_crud_and_reorder(self):
        # 1. Create module
        create_resp = self.client.post(reverse('cms_module_create'), {
            'title_sk': 'Nový Modul',
            'title_en': 'New Module',
            'description_sk': 'Popis modulu',
            'description_en': 'Module description',
            'programming_language': 'python',
            'estimated_hours': 14,
            'difficulty_level': 'BEGINNER',
            'is_published': 'on',
        })
        self.assertEqual(create_resp.status_code, 302)
        module = Module.objects.get(title_sk='Nový Modul')
        self.assertEqual(module.estimated_hours, 14)
        self.assertTrue(module.is_published)
        self.assertFalse(module.is_pro_only)

        # 2. Toggle PRO
        self.client.post(reverse('cms_module_toggle_pro', args=[module.id]))
        module.refresh_from_db()
        self.assertTrue(module.is_pro_only)

        # 3. Toggle Publish
        self.client.post(reverse('cms_module_toggle_publish', args=[module.id]))
        module.refresh_from_db()
        self.assertFalse(module.is_published)

        # 4. Edit module
        self.client.post(reverse('cms_module_edit', args=[module.id]), {
            'title_sk': 'Upravený Modul',
            'title_en': 'Edited Module',
            'description_sk': 'Nový popis',
            'description_en': 'New desc',
            'programming_language': 'python',
            'estimated_hours': 16,
            'difficulty_level': 'INTERMEDIATE',
            'is_published': 'on',
        })
        module.refresh_from_db()
        self.assertEqual(module.title_sk, 'Upravený Modul')
        self.assertEqual(module.estimated_hours, 16)

        # 5. Reorder module
        mod2 = Module.objects.create(title_sk='Druhý Modul', title_en='Mod 2', order=2)
        self.client.post(reverse('cms_module_reorder', args=[mod2.id, 'up']))
        mod2.refresh_from_db()
        module.refresh_from_db()
        self.assertEqual(mod2.order, 1)
        self.assertEqual(module.order, 2)

        # 6. Delete module
        del_resp = self.client.post(reverse('cms_module_delete', args=[module.id]))
        self.assertEqual(del_resp.status_code, 302)
        self.assertFalse(Module.objects.filter(id=module.id).exists())

    def test_cms_lesson_crud_and_duplication(self):
        module = Module.objects.create(title_sk='Algoritmy', title_en='Algorithms', order=1)

        # 1. Create lesson
        self.client.post(reverse('cms_lesson_create', args=[module.id]), {
            'title_sk': 'Úvod do cyklov',
            'title_en': 'Introduction to loops',
            'summary_sk': 'Základy while a for cyklov',
            'summary_en': 'Basics of loops',
            'content_sk': '### Cyklus while\nPríklad kódu...',
            'content_en': '### While loop\nExample code...',
            'estimated_minutes': 45,
            'xp_reward': 50,
            'is_published': 'on',
        })
        lesson = Lesson.objects.get(title_sk='Úvod do cyklov')
        self.assertEqual(lesson.module, module)
        self.assertEqual(lesson.estimated_minutes, 45)

        # 2. Duplicate lesson
        dup_resp = self.client.post(reverse('cms_lesson_duplicate', args=[lesson.id]))
        self.assertEqual(dup_resp.status_code, 302)
        duplicated = Lesson.objects.filter(title_sk__icontains='Kópia').first()
        self.assertIsNotNone(duplicated)
        self.assertEqual(duplicated.module, module)

        # 3. Edit lesson
        self.client.post(reverse('cms_lesson_edit', args=[lesson.id]), {
            'title_sk': 'Upravené cykly',
            'title_en': 'Edited loops',
            'summary_sk': 'Upravené zhrnutie',
            'summary_en': 'Edited summary',
            'content_sk': 'Nový Markdown obsah',
            'content_en': 'New Markdown content',
            'estimated_minutes': 60,
            'xp_reward': 70,
            'is_published': 'on',
        })
        lesson.refresh_from_db()
        self.assertEqual(lesson.title_sk, 'Upravené cykly')
        self.assertEqual(lesson.xp_reward, 70)

        # 4. Delete lesson
        self.client.post(reverse('cms_lesson_delete', args=[lesson.id]))
        self.assertFalse(Lesson.objects.filter(id=lesson.id).exists())

    def test_cms_quiz_crud(self):
        module = Module.objects.create(title_sk='Modul', title_en='Module', order=1)
        lesson = Lesson.objects.create(module=module, title_sk='Lekcia', title_en='Lesson', order=1)

        # 1. Create Quiz
        self.client.post(reverse('cms_quiz_create', args=[lesson.id]), {
            'question_sk': 'Aký dátový typ vráti type(42)?',
            'question_en': 'What data type does type(42) return?',
            'option_a_sk': 'int',
            'option_a_en': 'int',
            'option_b_sk': 'float',
            'option_b_en': 'float',
            'option_c_sk': 'str',
            'option_c_en': 'str',
            'correct_option': 'A',
            'explanation_sk': '42 je celé číslo, teda int.',
            'explanation_en': '42 is an integer, so int.',
        })
        quiz = QuizQuestion.objects.get(lesson=lesson)
        self.assertEqual(quiz.correct_option, 'A')

        # 2. Edit Quiz
        self.client.post(reverse('cms_quiz_edit', args=[quiz.id]), {
            'question_sk': 'Aký dátový typ vráti type("42")?',
            'question_en': 'What does type("42") return?',
            'option_a_sk': 'str',
            'option_a_en': 'str',
            'option_b_sk': 'int',
            'option_b_en': 'int',
            'option_c_sk': 'bool',
            'option_c_en': 'bool',
            'correct_option': 'A',
            'explanation_sk': 'Je v úvodzovkách, takže str.',
            'explanation_en': 'It is in quotes, so str.',
        })
        quiz.refresh_from_db()
        self.assertEqual(quiz.question_sk, 'Aký dátový typ vráti type("42")?')

        # 3. Delete Quiz
        self.client.post(reverse('cms_quiz_delete', args=[quiz.id]))
        self.assertFalse(QuizQuestion.objects.filter(id=quiz.id).exists())

    def test_cms_exercise_and_testcase_crud(self):
        module = Module.objects.create(title_sk='Modul', title_en='Module', order=1)
        lesson = Lesson.objects.create(module=module, title_sk='Lekcia', title_en='Lesson', order=1)

        # 1. Create Exercise
        self.client.post(reverse('cms_exercise_create', args=[lesson.id]), {
            'title_sk': 'Súčet dvoch čísel',
            'title_en': 'Sum of two numbers',
            'instructions_sk': 'Napíš funkciu `sucet(a, b)`',
            'instructions_en': 'Write function `sucet(a, b)`',
            'starter_code': 'def sucet(a, b):\n    pass\n',
            'solution_code': 'def sucet(a, b):\n    return a + b\n',
            'explanation_sk': 'Použi operátor +.',
            'explanation_en': 'Use + operator.',
            'hint_sk': 'return a + b',
            'hint_en': 'return a + b',
            'hint_cost_doros': 10,
            'difficulty': 'EASY',
            'xp_reward': 40,
            'doros_reward': 20,
        })
        exercise = Exercise.objects.get(lesson=lesson)
        self.assertEqual(exercise.title_sk, 'Súčet dvoch čísel')

        # 2. Create TestCase
        self.client.post(reverse('cms_testcase_create', args=[exercise.id]), {
            'input_data': 'a=2, b=3',
            'expected_output': '5',
            'test_code': 'assert sucet(2, 3) == 5',
        })
        tc = CourseTestCase.objects.get(exercise=exercise)
        self.assertEqual(tc.expected_output, '5')

        # 3. Edit TestCase
        self.client.post(reverse('cms_testcase_edit', args=[tc.id]), {
            'input_data': 'a=10, b=20',
            'expected_output': '30',
            'test_code': 'assert sucet(10, 20) == 30',
            'is_hidden': 'on',
        })
        tc.refresh_from_db()
        self.assertTrue(tc.is_hidden)
        self.assertEqual(tc.expected_output, '30')

        # 4. Delete TestCase
        self.client.post(reverse('cms_testcase_delete', args=[tc.id]))
        self.assertFalse(CourseTestCase.objects.filter(id=tc.id).exists())

        # 5. Delete Exercise
        self.client.post(reverse('cms_exercise_delete', args=[exercise.id]))
        self.assertFalse(Exercise.objects.filter(id=exercise.id).exists())

    def test_cms_test_solution_ajax(self):
        # Test teacher live sandbox test runner
        resp = self.client.post(
            reverse('cms_test_solution'),
            data={
                'solution_code': 'def double(x):\n    return x * 2\n',
                'custom_test_cases': '[{"test_code": "assert double(5) == 10"}]'
            }
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['passed'])
        self.assertEqual(data['status'], 'PASSED')
        self.assertIn('execution_time_ms', data)

        # Test failing code
        resp_fail = self.client.post(
            reverse('cms_test_solution'),
            data={
                'solution_code': 'def double(x):\n    return x + 1\n',
                'custom_test_cases': '[{"test_code": "assert double(5) == 10"}]'
            }
        )
        data_fail = resp_fail.json()
        self.assertFalse(data_fail['passed'])

    def test_reward_restock_and_toggle(self):
        reward = RewardItem.objects.create(
            title_sk='Extra žolík',
            title_en='Extra Joker',
            cost_doros=250,
            max_stock=5,
            current_stock=0,
            is_active=True,
            created_by=self.teacher
        )
        # Restock
        self.client.post(reverse('cms_reward_restock', args=[reward.id]))
        reward.refresh_from_db()
        self.assertEqual(reward.current_stock, 5)

        # Toggle Active
        self.client.post(reverse('cms_reward_toggle_active', args=[reward.id]))
        reward.refresh_from_db()
        self.assertFalse(reward.is_active)

        # Delete Reward
        self.client.post(reverse('cms_reward_delete', args=[reward.id]))
        self.assertFalse(RewardItem.objects.filter(id=reward.id).exists())

    def test_class_quest_distribution(self):
        cq = ClassQuest.objects.create(
            school_class=self.school_class,
            title_sk='Triedny šprint',
            title_en='Class sprint',
            target_exercises_count=10,
            reward_doros_per_student=75,
            min_contribution_required=1,
            reward_policy=ClassQuest.RewardPolicy.ALL_STUDENTS,
            deadline=User.objects.first().date_joined  # past
        )
        initial_doros = self.student.doros

        # Trigger distribute
        resp = self.client.post(reverse('cms_classquest_distribute', args=[cq.id]))
        self.assertEqual(resp.status_code, 302)

        cq.refresh_from_db()
        self.student.refresh_from_db()
        self.assertTrue(cq.rewards_distributed)
        self.assertEqual(self.student.doros, initial_doros + 75)

    def test_school_class_and_license_creation(self):
        # 1. Create SchoolClass
        self.client.post(reverse('cms_class_create'), {
            'name': 'III.A',
            'join_code': 'IIIA-2027',
        })
        self.assertTrue(SchoolClass.objects.filter(join_code='IIIA-2027').exists())

        # 2. Create Subscription License
        self.client.post(reverse('cms_license_create'), {
            'tier': 'EDU',
            'max_uses': 40,
            'code': 'EDU-SPECIAL-2027',
        })
        lic = SubscriptionLicense.objects.filter(code='EDU-SPECIAL-2027').first()
        self.assertIsNotNone(lic)
        self.assertEqual(lic.max_uses, 40)
        self.assertEqual(lic.tier, 'EDU')
