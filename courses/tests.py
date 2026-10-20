from django.test import TestCase
from accounts.models import User
from courses.models import Module, Lesson, Exercise, TestCase as ExTestCase, Submission
from courses.services import check_code_safety, evaluate_python_code, get_codo_ai_feedback


class SandboxSecurityTests(TestCase):
    """
    Testy bezpečnosti Python sandboxu Codoro:
    1. AST statická analýza zakázaných modulov, volaní a dunder atribútov.
    2. Izolovaný podproces s timeoutom (ochrana pred DoS nekonečným cyklom).
    3. Vyhodnocovanie testovacích prípadov (PASSED / FAILED / ERROR).
    """

    def test_ast_blocks_dangerous_imports(self):
        dangerous_snippets = [
            "import os\nos.system('echo hacked')",
            "import sys\nsys.exit(0)",
            "import subprocess\nsubprocess.run(['dir'])",
            "from shutil import rmtree",
            "import socket",
            "import ctypes",
            "from urllib import request",
        ]
        for snippet in dangerous_snippets:
            is_safe, error_msg = check_code_safety(snippet, lang='sk')
            self.assertFalse(is_safe, f"Snippet by mal byť zablokovaný: {snippet}")
            self.assertIn("Bezpečnostná ochrana Codoro", error_msg)

    def test_ast_blocks_dangerous_calls_and_dunders(self):
        dangerous_snippets = [
            "f = open('secret.txt', 'w')",
            "eval('2 + 2')",
            "exec('x = 5')",
            "mod = __import__('os')",
            "c = ().__class__.__bases__[0].__subclasses__()",
        ]
        for snippet in dangerous_snippets:
            is_safe, error_msg = check_code_safety(snippet, lang='sk')
            self.assertFalse(is_safe, f"Volanie by malo byť zablokované: {snippet}")

    def test_ast_allows_safe_python_code(self):
        safe_snippets = [
            "x = 5\ny = 10\nprint(x + y)",
            "def pozdrav(meno):\n    return f'Ahoj {meno}!'",
            "numbers = [1, 2, 3, 4, 5]\nsquares = [n**2 for n in numbers]",
            "import math\nprint(math.sqrt(16))",
        ]
        for snippet in safe_snippets:
            is_safe, error_msg = check_code_safety(snippet, lang='sk')
            self.assertTrue(is_safe, f"Bezpečný kód bol neprávom zablokovaný: {snippet} ({error_msg})")


class EvaluationEngineTests(TestCase):
    """Testy vyhodnocovania cvičení voči TestCase modelom."""

    def setUp(self):
        self.teacher = User.objects.create_user(
            username='profesor', password='password123', role='TEACHER'
        )
        self.student = User.objects.create_user(
            username='martin', password='password123', role='STUDENT'
        )
        self.module = Module.objects.create(
            title_sk='1. Základy Pythonu',
            title_en='1. Python Basics',
            order=1,
            programming_language='python'
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title_sk='Premenné a funkcie',
            title_en='Variables and Functions',
            order=1,
            xp_reward=25
        )
        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            title_sk='Súčet dvoch čísel',
            title_en='Sum of Two Numbers',
            instructions_sk='Vytvor funkciu sucet(a, b), ktorá vráti ich súčet.',
            instructions_en='Create a function sucet(a, b) that returns their sum.',
            starter_code='def sucet(a, b):\n    pass',
            solution_code='def sucet(a, b):\n    return a + b',
            order=1,
            xp_reward=50,
            doros_reward=20
        )
        # Test Case 1: verejný
        ExTestCase.objects.create(
            exercise=self.exercise,
            input_data='sucet(2, 3)',
            expected_output='5',
            test_code='assert sucet(2, 3) == 5',
            is_hidden=False
        )
        # Test Case 2: skrytý
        ExTestCase.objects.create(
            exercise=self.exercise,
            input_data='sucet(10, -5)',
            expected_output='5',
            test_code='assert sucet(10, -5) == 5',
            is_hidden=True
        )

    def test_correct_solution_passes_all_tests(self):
        student_code = "def sucet(a, b):\n    return a + b"
        passed, status, output_log = evaluate_python_code(self.exercise, student_code, lang='sk')
        self.assertTrue(passed)
        self.assertEqual(status, 'PASSED')
        self.assertIn("ÚSPEŠNÝ", output_log)
        self.assertIn("2/2 testov prešlo", output_log)

    def test_incorrect_solution_fails_gracefully(self):
        # Kód funguje pre 2, 3 ale nie pre záporné čísla
        student_code = "def sucet(a, b):\n    return 5 if a == 2 else 0"
        passed, status, output_log = evaluate_python_code(self.exercise, student_code, lang='sk')
        self.assertFalse(passed)
        self.assertEqual(status, 'FAILED')
        self.assertIn("ZLYHAL", output_log)
        self.assertIn("1/2 testov prešlo", output_log)

    def test_infinite_loop_triggers_timeout(self):
        # Nekonečný cyklus musí vypršať po timeoute bez zhodenia servera
        student_code = "while True:\n    pass"
        passed, status, output_log = evaluate_python_code(self.exercise, student_code, lang='sk')
        self.assertFalse(passed)
        self.assertEqual(status, 'ERROR')
        self.assertIn("Časový limit vypršal", output_log)

    def test_socratic_ai_tutor_fallback_without_api_key(self):
        # Fallback musí vrátiť užitočnú radu a nikdy nesmie spadnúť
        feedback = get_codo_ai_feedback(
            exercise=self.exercise,
            student_code="def sucet(a, b):\n    pass",
            error_log="AssertionError: 5 != None",
            lang='sk'
        )
        self.assertIsInstance(feedback, str)
        self.assertTrue(len(feedback) > 10)
        self.assertNotIn("def sucet(a, b):\n    return a + b", feedback, "AI nesmie vygenerovať hotové riešenie!")


class PracticeArenaAndLessonDetailTests(TestCase):
    """Testy pre Tréningovú Arénu a prepínanie úloh v lekcii."""

    def setUp(self):
        self.student = User.objects.create_user(
            username='student_arena', password='password123', role='STUDENT'
        )
        self.module = Module.objects.create(
            title_sk='Modul 1', title_en='Module 1', order=1, estimated_hours=10
        )
        self.lesson = Lesson.objects.create(
            module=self.module, title_sk='Lekcia 1', title_en='Lesson 1', order=1
        )
        self.ex1 = Exercise.objects.create(
            lesson=self.lesson, title_sk='Úloha 1 (Ľahká)', title_en='Task 1 (Easy)',
            difficulty=Exercise.Difficulty.EASY, order=1
        )
        self.ex2 = Exercise.objects.create(
            lesson=self.lesson, title_sk='Úloha 2 (Boss)', title_en='Task 2 (Boss)',
            difficulty=Exercise.Difficulty.HARD, order=2,
            explanation_sk='Vzorové vysvetlenie k úlohe 2',
            explanation_en='Model solution explanation for task 2'
        )

    def test_arena_requires_login(self):
        response = self.client.get('/arena/')
        self.assertEqual(response.status_code, 302)

    def test_arena_view_loads_for_student(self):
        self.client.login(username='student_arena', password='password123')
        response = self.client.get('/arena/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Úloha 1 (Ľahká)')
        self.assertContains(response, 'Úloha 2 (Boss)')
        self.assertEqual(response.context['total_exercises'], 2)

    def test_arena_filter_difficulty(self):
        self.client.login(username='student_arena', password='password123')
        response = self.client.get('/arena/?difficulty=HARD')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['exercises']), 1)
        self.assertEqual(response.context['exercises'][0].id, self.ex2.id)

    def test_arena_filter_status_solved_and_unsolved(self):
        self.client.login(username='student_arena', password='password123')
        # Označíme ex1 ako PASSED
        Submission.objects.create(
            student=self.student, exercise=self.ex1, status=Submission.Status.PASSED,
            submitted_code='x = 1'
        )
        # Filter: unsolved
        res_unsolved = self.client.get('/arena/?status=unsolved')
        self.assertEqual(len(res_unsolved.context['exercises']), 1)
        self.assertEqual(res_unsolved.context['exercises'][0].id, self.ex2.id)

        # Filter: solved
        res_solved = self.client.get('/arena/?status=solved')
        self.assertEqual(len(res_solved.context['exercises']), 1)
        self.assertEqual(res_solved.context['exercises'][0].id, self.ex1.id)

    def test_lesson_detail_exercise_switching_and_next_task(self):
        self.client.login(username='student_arena', password='password123')
        # Predvolene načíta ex1
        res = self.client.get(f'/lesson/{self.lesson.id}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.context['current_exercise'].id, self.ex1.id)
        self.assertEqual(res.context['next_exercise'].id, self.ex2.id)

        # Prepnutie na ex2 cez GET parameter
        res2 = self.client.get(f'/lesson/{self.lesson.id}/?exercise={self.ex2.id}')
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.context['current_exercise'].id, self.ex2.id)
        self.assertIsNone(res2.context['next_exercise'])

    def test_cheat_sheets_view(self):
        self.client.login(username='student_arena', password='password123')
        res = self.client.get('/cheatsheets/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('categories', res.context)
        self.assertIn('items', res.context)
        self.assertGreaterEqual(len(res.context['categories']), 6)
        self.assertGreaterEqual(len(res.context['items']), 20)

    def test_module_track_choices(self):
        self.assertEqual(self.module.track, Module.Track.FUNDAMENTALS)
        self.module.track = Module.Track.OOP
        self.module.save()
        self.assertEqual(Module.objects.get(id=self.module.id).track, Module.Track.OOP)

