from django.db import models
from django.conf import settings


class Module(models.Model):
    """Vzdelávací modul / kapitola (napr. 1. Základy Pythonu, 2. Podmienky a cykly)."""
    class ProgrammingLanguage(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVASCRIPT = 'javascript', 'JavaScript (Pripravené na rozšírenie)'
        SQL = 'sql', 'SQL (Pripravené na rozšírenie)'

    title_sk = models.CharField(max_length=150, verbose_name="Názov modulu (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov modulu (EN)")
    description_sk = models.TextField(verbose_name="Popis modulu (SK)")
    description_en = models.TextField(verbose_name="Popis modulu (EN)")
    programming_language = models.CharField(
        max_length=20,
        choices=ProgrammingLanguage.choices,
        default=ProgrammingLanguage.PYTHON,
        verbose_name="Programovací jazyk"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie modulu")
    is_pro_only = models.BooleanField(default=False, verbose_name="Vyžaduje PRO/EDU účet")
    icon_name = models.CharField(max_length=50, default="bi-terminal", verbose_name="Ikona (Bootstrap Icons)")

    class Meta:
        ordering = ['order']
        verbose_name = "Modul"
        verbose_name_plural = "Moduly"

    def __str__(self):
        return f"{self.order}. {self.title_sk} ({self.get_programming_language_display()})"


class Lesson(models.Model):
    """Teoretická lekcia v rámci modulu."""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name="Modul")
    title_sk = models.CharField(max_length=150, verbose_name="Názov lekcie (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov lekcie (EN)")
    content_sk = models.TextField(verbose_name="Teoretický výklad v Markdowne (SK)")
    content_en = models.TextField(verbose_name="Teoretický výklad v Markdowne (EN)")
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie v module")
    xp_reward = models.PositiveIntegerField(default=15, verbose_name="Odmena XP za prečítanie")

    class Meta:
        ordering = ['module__order', 'order']
        verbose_name = "Lekcia"
        verbose_name_plural = "Lekcie"

    def __str__(self):
        return f"{self.module.order}.{self.order} {self.title_sk}"


class Exercise(models.Model):
    """Praktické programátorské cvičenie s automatickou kontrolou kódu."""
    class Difficulty(models.TextChoices):
        EASY = 'EASY', 'Ľahká'
        MEDIUM = 'MEDIUM', 'Stredná'
        HARD = 'HARD', 'Ťažká (Boss)'

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises', verbose_name="Lekcia")
    title_sk = models.CharField(max_length=150, verbose_name="Názov úlohy (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov úlohy (EN)")
    instructions_sk = models.TextField(verbose_name="Zadanie úlohy (SK)")
    instructions_en = models.TextField(verbose_name="Zadanie úlohy (EN)")
    starter_code = models.TextField(
        default="# Sem napíš svoj Python kód\n",
        verbose_name="Štartovací kód v editore"
    )
    solution_code = models.TextField(verbose_name="Vzorové riešenie (pre učiteľa a AI tútora Codo)")
    hint_sk = models.TextField(blank=True, verbose_name="Nápoveda (SK)")
    hint_en = models.TextField(blank=True, verbose_name="Nápoveda (EN)")
    hint_cost_doros = models.PositiveIntegerField(default=15, verbose_name="Cena nápovedy v Doros")
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.EASY)
    xp_reward = models.PositiveIntegerField(default=50, verbose_name="Odmena XP")
    doros_reward = models.PositiveIntegerField(default=20, verbose_name="Odmena Doros (na 1. pokus)")
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie cvičenia")

    class Meta:
        ordering = ['lesson', 'order']
        verbose_name = "Praktické cvičenie"
        verbose_name_plural = "Praktické cvičenia"

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.title_sk}"


class TestCase(models.Model):
    """Testovací prípad pre automatické vyhodnotenie študentského kódu."""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='test_cases', verbose_name="Cvičenie")
    input_data = models.TextField(blank=True, verbose_name="Vstupné dáta (stdin) alebo volanie funkcie")
    expected_output = models.TextField(verbose_name="Očakávaný výstup (stdout)")
    test_code = models.TextField(
        blank=True,
        verbose_name="Vlastný assert test (napr. assert sucet(2, 3) == 5)"
    )
    is_hidden = models.BooleanField(
        default=False,
        verbose_name="Skrytý test (ochrana proti natvrdo napísaným odpovediam)"
    )

    def __str__(self):
        return f"Test pre {self.exercise.title_sk} (Skrytý: {self.is_hidden})"


class Submission(models.Model):
    """História odovzdaných riešení študentov, AI rád a hodnotení od učiteľa."""
    class Status(models.TextChoices):
        PASSED = 'PASSED', 'Úspešné (Prešlo všetkými testami)'
        FAILED = 'FAILED', 'Neúspešné (Chyba v testoch)'
        ERROR = 'ERROR', 'Syntaktická alebo behová chyba'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Študent"
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions', verbose_name="Cvičenie")
    submitted_code = models.TextField(verbose_name="Odovzdaný kód študenta")
    status = models.CharField(max_length=10, choices=Status.choices, verbose_name="Výsledok kontroly")
    output_log = models.TextField(blank=True, verbose_name="Výpis z konzoly / Chybová hláška")
    ai_tutor_feedback = models.TextField(blank=True, verbose_name="Sokratovská rada od AI tútora Codo")
    teacher_comment = models.TextField(blank=True, verbose_name="Komentár od učiteľa (Code Review)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Čas odovzdania")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Odovzdané riešenie"
        verbose_name_plural = "Odovzdané riešenia"

    def __str__(self):
        return f"{self.student.username} - {self.exercise.title_sk} ({self.status})"


class QuizQuestion(models.Model):
    """Teoretická kvízová otázka na konci lekcie."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quiz_questions')
    question_sk = models.TextField(verbose_name="Otázka (SK)")
    question_en = models.TextField(verbose_name="Otázka (EN)")
    option_a_sk = models.CharField(max_length=200)
    option_a_en = models.CharField(max_length=200)
    option_b_sk = models.CharField(max_length=200)
    option_b_en = models.CharField(max_length=200)
    option_c_sk = models.CharField(max_length=200)
    option_c_en = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C')],
        verbose_name="Správna odpoveď"
    )

    def __str__(self):
        return f"Kvíz: {self.question_sk[:50]}..."


class LessonProgress(models.Model):
    """Sledovanie dokončených lekcií jednotlivými študentmi."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')