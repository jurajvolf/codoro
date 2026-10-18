from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import math


class SchoolClass(models.Model):
    """Model reprezentujúci školskú triedu (pre kolektívne questy a správu žiakov)."""
    name = models.CharField(max_length=50, verbose_name="Názov triedy (napr. IV.C)")
    join_code = models.CharField(max_length=12, unique=True, verbose_name="Kód na pripojenie")
    teacher = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='managed_classes',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name="Triedny učiteľ / Vyucujúci"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.join_code})"


class User(AbstractUser):
    """Rozšírený používateľský model platformy Codoro."""

    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Študent'
        TEACHER = 'TEACHER', 'Učiteľ'

    class Language(models.TextChoices):
        SK = 'sk', 'Slovenčina'
        EN = 'en', 'English'

    class SubscriptionTier(models.TextChoices):
        FREE = 'FREE', 'Free (Základný)'
        PRO = 'PRO', 'Codoro PRO'
        EDU = 'EDU', 'Školská EDU licencia'

    # 1. Rola, trieda a lokalizácia
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name="Rola používateľa"
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Školská trieda"
    )
    preferred_language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.SK,
        verbose_name="Jazyk rozhrania"
    )

    # 2. Predplatné a limity AI tútora Codo
    subscription_tier = models.CharField(
        max_length=10,
        choices=SubscriptionTier.choices,
        default=SubscriptionTier.FREE,
        verbose_name="Úroveň predplatného"
    )
    daily_ai_hints_used = models.PositiveIntegerField(default=0, verbose_name="Dnes použité AI rady")
    last_ai_hint_date = models.DateField(null=True, blank=True)

    # 3. Gamifikácia: XP, Level a mena Doros
    xp = models.PositiveIntegerField(default=0, verbose_name="Skúsenostné body (XP)")
    level = models.PositiveIntegerField(default=1, verbose_name="Aktuálna úroveň (Level)")
    doros = models.PositiveIntegerField(default=50, verbose_name="Mena Doros")

    # 4. Gamifikácia: Denný Streak a jeho záchrana
    current_streak = models.PositiveIntegerField(default=0, verbose_name="Aktuálny denný Streak")
    longest_streak = models.PositiveIntegerField(default=0, verbose_name="Najdlhší Streak")
    last_activity_date = models.DateField(null=True, blank=True, verbose_name="Dátum poslednej aktivity")
    streak_freezes = models.PositiveIntegerField(default=0, verbose_name="Počet zmrazení Streaku v inventári")
    lost_streak_value = models.PositiveIntegerField(default=0, verbose_name="Hodnota vyhasnutého Streaku na opravu")
    streak_lost_at = models.DateTimeField(null=True, blank=True, verbose_name="Čas straty Streaku")

    def calculate_level_from_xp(self):
        """
        Vypočíta level zo získaných XP podľa vzorca: XP = 100 * (Level - 1)^1.5
        (Tento vzorec uvedieme v 2. kapitole maturitnej práce).
        """
        if self.xp < 100:
            return 1
        return int((self.xp / 100) ** (2 / 3)) + 1

    def xp_for_next_level(self):
        """Vráti celkový počet XP potrebných na dosiahnutie ďalšej úrovne."""
        return int(100 * (self.level ** 1.5))

    def add_xp_and_check_level_up(self, amount):
        """Pridá XP a ak študent postúpi na nový level, automaticky mu pripíše bonusové Doros."""
        self.xp += amount
        new_level = self.calculate_level_from_xp()
        reward_doros = 0

        if new_level > self.level:
            # Odmena za každý dosiahnutý level: Nový Level * 50 Doros
            for lvl in range(self.level + 1, new_level + 1):
                reward_doros += lvl * 50
            self.level = new_level
            self.doros += reward_doros

        self.save()
        return reward_doros

    def is_teacher(self):
        return self.role == self.Role.TEACHER or self.is_superuser

    def has_pro_access(self):
        return self.subscription_tier in [self.SubscriptionTier.PRO, self.SubscriptionTier.EDU] or self.is_teacher()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()} - Lvl {self.level})"


class SubscriptionLicense(models.Model):
    """Licenčné kľúče, ktoré môže učiteľ alebo škola vygenerovať na aktiváciu EDU/PRO účtu."""
    code = models.CharField(max_length=20, unique=True, verbose_name="Licenčný kľúč (napr. EDU-2027-X89B)")
    tier = models.CharField(
        max_length=10,
        choices=User.SubscriptionTier.choices,
        default=User.SubscriptionTier.EDU
    )
    max_uses = models.PositiveIntegerField(default=30, verbose_name="Maximálny počet aktivácií (veľkosť triedy)")
    current_uses = models.PositiveIntegerField(default=0, verbose_name="Počet doterajších aktivácií")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.current_uses}/{self.max_uses})"