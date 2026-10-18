from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class RewardItem(models.Model):
    """Položka v učiteľskom obchode s riadením skladových zásob a automatickým obnovovaním."""
    class RestockPeriod(models.TextChoices):
        DAILY = 'DAILY', 'Denne (každých 24 hodín)'
        WEEKLY = 'WEEKLY', 'Týždenne (každých 7 dní)'
        MONTHLY = 'MONTHLY', 'Mesačne (každých 30 dní)'
        MANUAL = 'MANUAL', 'Manuálne (iba učiteľom)'

    title_sk = models.CharField(max_length=150, verbose_name="Názov odmeny (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov odmeny (EN)")
    description_sk = models.TextField(verbose_name="Popis a podmienky uplatnenia (SK)")
    description_en = models.TextField(verbose_name="Popis a podmienky uplatnenia (EN)")
    cost_doros = models.PositiveIntegerField(verbose_name="Cena v Doros")
    icon_name = models.CharField(max_length=50, default="bi-gift", verbose_name="Ikona odmeny")

    # Skladové hospodárstvo (ochrana proti hromadnému vykúpeniu triedou)
    max_stock = models.PositiveIntegerField(default=2, verbose_name="Maximálny počet kusov na sklade")
    current_stock = models.PositiveIntegerField(default=2, verbose_name="Aktuálny počet kusov na sklade")
    restock_period = models.CharField(
        max_length=10,
        choices=RestockPeriod.choices,
        default=RestockPeriod.WEEKLY,
        verbose_name="Interval obnovenia zásob"
    )
    limit_per_student_per_period = models.PositiveIntegerField(
        default=1,
        verbose_name="Max. počet nákupov na 1 žiaka za obdobie"
    )
    last_restocked_at = models.DateTimeField(default=timezone.now, verbose_name="Posledné obnovenie skladu")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Vytvoril učiteľ"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktívna v obchode")

    def check_and_restock(self):
        """Automaticky skontroluje, či uplynul čas na obnovenie zásob, a doplní sklad."""
        now = timezone.now()
        should_restock = False

        if self.restock_period == self.RestockPeriod.DAILY and now >= self.last_restocked_at + timedelta(days=1):
            should_restock = True
        elif self.restock_period == self.RestockPeriod.WEEKLY and now >= self.last_restocked_at + timedelta(days=7):
            should_restock = True
        elif self.restock_period == self.RestockPeriod.MONTHLY and now >= self.last_restocked_at + timedelta(days=30):
            should_restock = True

        if should_restock:
            self.current_stock = self.max_stock
            self.last_restocked_at = now
            self.save()

    def __str__(self):
        return f"{self.title_sk} ({self.cost_doros} Doros | Sklad: {self.current_stock}/{self.max_stock})"


class RewardPurchase(models.Model):
    """Zakúpený kupón odmeny študentom, ktorý schvaľuje učiteľ."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Čaká na uplatnenie u učiteľa'
        REDEEMED = 'REDEEMED', 'Uplatnené / Schválené'
        REFUNDED = 'REFUNDED', 'Zamietnuté (Doros vrátené žiakovi)'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    reward = models.ForeignKey(RewardItem, on_delete=models.CASCADE, related_name='purchases')
    coupon_code = models.CharField(max_length=15, unique=True, verbose_name="Kód kupónu")
    cost_paid = models.PositiveIntegerField(verbose_name="Zaplatená suma v Doros")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    purchased_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_purchases'
    )

    def __str__(self):
        return f"Kupón {self.coupon_code} - {self.student.username} ({self.reward.title_sk})"


class DorosTransaction(models.Model):
    """Kompletný audit log (história peňaženky) každého pohybu meny Doros."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField(verbose_name="Suma (+ príjem / - výdavok)")
    reason_sk = models.CharField(max_length=255, verbose_name="Dôvod transakcie (SK)")
    reason_en = models.CharField(max_length=255, verbose_name="Dôvod transakcie (EN)")
    performed_by_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='issued_transactions',
        verbose_name="Manuálny zásah učiteľa"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        sign = "+" if self.amount > 0 else ""
        return f"{self.student.username}: {sign}{self.amount} Doros ({self.reason_sk})"


class Quest(models.Model):
    """Osobné výzvy pre študentov (Daily, Weekly, Monthly, prípadne od učiteľa)."""
    class QuestPeriod(models.TextChoices):
        DAILY = 'DAILY', 'Denný Quest (Daily)'
        WEEKLY = 'WEEKLY', 'Týždenný Quest (Weekly)'
        MONTHLY = 'MONTHLY', 'Mesačný Quest (Monthly)'
        TEACHER = 'TEACHER', 'Špeciálna výzva od učiteľa'

    class MetricType(models.TextChoices):
        SOLVE_EXERCISES = 'SOLVE_EXERCISES', 'Počet vyriešených cvičení'
        EARN_XP = 'EARN_XP', 'Získané množstvo XP'
        FIRST_TRY_SOLVES = 'FIRST_TRY_SOLVES', 'Cvičenia vyriešené na 1. pokus'
        COMPLETE_LESSONS = 'COMPLETE_LESSONS', 'Dokončené teoretické lekcie'

    title_sk = models.CharField(max_length=150)
    title_en = models.CharField(max_length=150)
    period = models.CharField(max_length=10, choices=QuestPeriod.choices, default=QuestPeriod.DAILY)
    metric_type = models.CharField(max_length=25, choices=MetricType.choices, default=MetricType.SOLVE_EXERCISES)
    target_value = models.PositiveIntegerField(default=3, verbose_name="Cieľová hodnota na splnenie")
    reward_doros = models.PositiveIntegerField(default=50, verbose_name="Odmena v Doros")
    reward_xp = models.PositiveIntegerField(default=30, verbose_name="Odmena v XP")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.get_period_display()}] {self.title_sk} (+{self.reward_doros} Doros)"


class StudentQuestProgress(models.Model):
    """Sledovanie plnenia osobných questov študentom."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quest_progress')
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    current_value = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    is_claimed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.quest.title_sk} ({self.current_value}/{self.quest.target_value})"


class ClassQuest(models.Model):
    """Kolektívne triedne výzvy (celá trieda spolupracuje na spoločnom cieli)."""
    class RewardPolicy(models.TextChoices):
        ALL_STUDENTS = 'ALL_STUDENTS', 'Celá trieda (všetci študenti v triede)'
        CONTRIBUTORS_ONLY = 'CONTRIBUTORS_ONLY', 'Iba zapojení študenti (s minimálnym príspevkom)'

    school_class = models.ForeignKey('accounts.SchoolClass', on_delete=models.CASCADE, related_name='class_quests')
    title_sk = models.CharField(max_length=150, verbose_name="Názov kolektívnej výzvy (SK)")
    title_en = models.CharField(max_length=150, verbose_name="Názov kolektívnej výzvy (EN)")
    period = models.CharField(max_length=10, choices=Quest.QuestPeriod.choices, default=Quest.QuestPeriod.WEEKLY)
    target_exercises_count = models.PositiveIntegerField(default=30, verbose_name="Spoločný cieľ (počet úloh za triedu)")
    current_exercises_count = models.PositiveIntegerField(default=0, verbose_name="Aktuálne splnené triedou")
    reward_policy = models.CharField(
        max_length=20,
        choices=RewardPolicy.choices,
        default=RewardPolicy.CONTRIBUTORS_ONLY,
        verbose_name="Pravidlo rozdelenia odmeny"
    )
    min_contribution_required = models.PositiveIntegerField(
        default=2,
        verbose_name="Minimálny počet úloh od žiaka pre nárok na odmenu"
    )
    reward_doros_per_student = models.PositiveIntegerField(default=200, verbose_name="Odmena Doros pre každého")
    deadline = models.DateTimeField(verbose_name="Čas ukončenia výzvy")
    is_completed = models.BooleanField(default=False)
    rewards_distributed = models.BooleanField(default=False)

    def __str__(self):
        return f"Triedny Quest ({self.school_class.name}): {self.title_sk} [{self.current_exercises_count}/{self.target_exercises_count}]"


class ClassQuestContribution(models.Model):
    """Zaznamenáva, koľkými úlohami konkrétny žiak prispel do kolektívneho questu triedy."""
    class_quest = models.ForeignKey(ClassQuest, on_delete=models.CASCADE, related_name='contributions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_contributed = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('class_quest', 'student')


class CoinDrop(models.Model):
    """Časované alebo náhodné Coin Dropy za aktivitu vytvárané učiteľom."""
    title_sk = models.CharField(max_length=100, default="Popoludňajší Doros Drop!")
    title_en = models.CharField(max_length=100, default="Afternoon Doros Drop!")
    school_class = models.ForeignKey(
        'accounts.SchoolClass',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Pre triedu (prázdne = pre všetkých)"
    )
    available_from = models.DateTimeField(verbose_name="Čas objavenia (napr. 16:00)")
    available_until = models.DateTimeField(verbose_name="Čas zmiznutia")
    max_claims = models.PositiveIntegerField(default=10, verbose_name="Max. počet žiakov, ktorí stihnú drop získať")
    min_doros = models.PositiveIntegerField(default=50, verbose_name="Minimálna náhodná odmena Doros")
    max_doros = models.PositiveIntegerField(default=150, verbose_name="Maximálna náhodná odmena Doros")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def is_currently_active(self):
        now = timezone.now()
        return self.available_from <= now <= self.available_until and self.claims.count() < self.max_claims

    def __str__(self):
        return f"{self.title_sk} ({self.available_from.strftime('%d.%m. %H:%M')})"


class CoinDropClaim(models.Model):
    """Záznam o tom, ktorý študent si vyzdvihol Coin Drop a koľko Doros mu padlo."""
    coin_drop = models.ForeignKey(CoinDrop, on_delete=models.CASCADE, related_name='claims')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount_won = models.PositiveIntegerField()
    claimed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coin_drop', 'student')


class Badge(models.Model):
    """Odznaky (Achievements) za špeciálne míľniky."""
    code = models.CharField(max_length=30, unique=True)
    name_sk = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_sk = models.CharField(max_length=255)
    description_en = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=50, default="bi-award-fill")
    bonus_doros = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.name_sk


class StudentBadge(models.Model):
    """Priradenie získaného odznaku študentovi."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'badge')