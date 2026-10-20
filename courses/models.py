from django.db import models
from django.conf import settings


class Module(models.Model):
    """Vzdelávací modul / kapitola (napr. 1. Základy Pythonu, 2. Podmienky a cykly)."""
    class ProgrammingLanguage(models.TextChoices):
        PYTHON = 'python', 'Python'
        JAVASCRIPT = 'javascript', 'JavaScript (Pripravené na rozšírenie)'
        SQL = 'sql', 'SQL (Pripravené na rozšírenie)'

    class Difficulty(models.TextChoices):
        BEGINNER = 'BEGINNER', 'Začiatočník / Beginner'
        INTERMEDIATE = 'INTERMEDIATE', 'Mierne pokročilý / Intermediate'
        ADVANCED = 'ADVANCED', 'Pokročilý / Advanced'

    class Track(models.TextChoices):
        FUNDAMENTALS = 'FUNDAMENTALS', '1. Základy a Logika'
        DATA_STRUCTURES = 'DATA_STRUCTURES', '2. Funkcie a Dátové štruktúry'
        OOP = 'OOP', '3. OOP a Softvérové inžinierstvo'
        ALGORITHMS_AND_DATA = 'ALGORITHMS_AND_DATA', '4. Algoritmy, Dáta a Bezpečnosť'
        MATURITA_PREP = 'MATURITA_PREP', '5. Maturitný špeciál a Projekty'

    title_sk = models.CharField(max_length=150, verbose_name="Názov modulu (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov modulu (EN)")
    description_sk = models.TextField(verbose_name="Popis modulu (SK)")
    description_en = models.TextField(verbose_name="Popis modulu (EN)")
    track = models.CharField(
        max_length=30,
        choices=Track.choices,
        default=Track.FUNDAMENTALS,
        verbose_name="Kariérna cesta (Track)"
    )
    programming_language = models.CharField(
        max_length=20,
        choices=ProgrammingLanguage.choices,
        default=ProgrammingLanguage.PYTHON,
        verbose_name="Programovací jazyk"
    )
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie modulu")
    estimated_hours = models.PositiveIntegerField(default=10, verbose_name="Odhadovaný počet hodín štúdia")
    difficulty_level = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
        verbose_name="Úroveň náročnosti"
    )
    is_pro_only = models.BooleanField(default=False, verbose_name="Vyžaduje PRO/EDU účet")
    icon_name = models.CharField(max_length=50, default="bi-terminal", verbose_name="Ikona (Bootstrap Icons)")
    is_published = models.BooleanField(default=True, verbose_name="Publikovaný modul")

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
    summary_sk = models.CharField(max_length=300, blank=True, verbose_name="Krátke zhrnutie (SK)")
    summary_en = models.CharField(max_length=300, blank=True, verbose_name="Krátke zhrnutie (EN)")
    content_sk = models.TextField(verbose_name="Teoretický výklad v Markdowne (SK)")
    content_en = models.TextField(verbose_name="Teoretický výklad v Markdowne (EN)")
    estimated_minutes = models.PositiveIntegerField(default=45, verbose_name="Odhadovaný čas (minúty)")
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie v module")
    xp_reward = models.PositiveIntegerField(default=15, verbose_name="Odmena XP za prečítanie")
    is_published = models.BooleanField(default=True, verbose_name="Publikovaná lekcia")

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
    explanation_sk = models.TextField(blank=True, verbose_name="Vysvetlenie vzorového riešenia (SK)")
    explanation_en = models.TextField(blank=True, verbose_name="Vysvetlenie vzorového riešenia (EN)")
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
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie testu")

    class Meta:
        ordering = ['exercise', 'order', 'id']

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
    execution_time_ms = models.PositiveIntegerField(default=0, verbose_name="Čas behu v ms")
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
    option_d_sk = models.CharField(max_length=200, blank=True)
    option_d_en = models.CharField(max_length=200, blank=True)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        verbose_name="Správna odpoveď"
    )
    explanation_sk = models.TextField(blank=True, verbose_name="Vysvetlenie správnej odpovede (SK)")
    explanation_en = models.TextField(blank=True, verbose_name="Vysvetlenie správnej odpovede (EN)")
    order = models.PositiveIntegerField(default=1, verbose_name="Poradie otázky")

    class Meta:
        ordering = ['lesson', 'order', 'id']

    def __str__(self):
        return f"Kvíz: {self.question_sk[:50]}..."


class LessonProgress(models.Model):
    """Sledovanie dokončených lekcií jednotlivými študentmi."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    quiz_passed = models.BooleanField(default=False, verbose_name="Kvíz úspešne vyplnený (XP pripísané)")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'lesson')


class HintUnlock(models.Model):
    """Záznam o odomknutej (zaplatenej) nápovede - študent platí za nápovedu k úlohe iba raz."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hint_unlocks')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='hint_unlocks')
    cost_paid = models.PositiveIntegerField(default=0, verbose_name="Zaplatená cena v Doros")
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exercise')
        verbose_name = "Odomknutá nápoveda"
        verbose_name_plural = "Odomknuté nápovedy"

    def __str__(self):
        return f"{self.student.username} - nápoveda k {self.exercise.title_sk} ({self.cost_paid} Doros)"