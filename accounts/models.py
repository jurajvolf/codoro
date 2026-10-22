from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import math


class SchoolClass(models.Model):
    """Model reprezentujúci školskú triedu (pre kolektívne questy a správu žiakov)."""
    name = models.CharField(max_length=50, verbose_name="Názov triedy (napr. IV.C)")
    join_code = models.CharField(max_length=12, unique=True, verbose_name="Kód na pripojenie")
    teacher = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='managed_classes',
        limit_choices_to={'role__in': ['TEACHER', 'ADMIN']},
        verbose_name="Triedny učiteľ / Vyučujúci"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.join_code})"


class User(AbstractUser):
    """Rozšírený používateľský model platformy Codoro."""

    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Študent'
        TEACHER = 'TEACHER', 'Učiteľ'
        ADMIN = 'ADMIN', 'Administrátor'

    class Language(models.TextChoices):
        SK = 'sk', 'Slovenčina'
        EN = 'en', 'English'

    class SubscriptionTier(models.TextChoices):
        FREE = 'FREE', 'Free (Základný)'
        PRO = 'PRO', 'Codoro PRO'
        EDU = 'EDU', 'Školská EDU licencia'

    # Prednastavené avatary (podpora ilustrovaných portrétov aj retro emoji)
    AVATAR_CHOICES = [
        ('student_alex', '👦 Alex (Programátor)'),
        ('student_mia', '👧 Mia (Data Scientist)'),
        ('student_sam', '🧑 Sam (Full-stack)'),
        ('cyber_ninja', '🥷 Cyber Coder'),
        ('codo', '🤖 Codo (AI Maskot)'),
        ('snake', '🐍 Pythonista'),
        ('fox', '🦊 Lišiak'),
        ('owl', '🦉 Sova'),
        ('panda', '🐼 Panda'),
        ('cat', '🐱 Hacker Cat'),
        ('rocket', '🚀 Inovátor'),
        ('ninja', '🥷 Ninja'),
        ('wizard', '🧙 Kód Magik'),
        ('alien', '👾 Cyber Alien'),
    ]
    AVATAR_COLORS = [
        ('indigo', '#4636F5'),
        ('cyan', '#0891B2'),
        ('emerald', '#059669'),
        ('amber', '#D97706'),
        ('rose', '#E11D48'),
        ('violet', '#7C3AED'),
    ]

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
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES, default='codo', verbose_name="Avatar")
    avatar_color = models.CharField(max_length=20, choices=AVATAR_COLORS, default='indigo', verbose_name="Farba avatara")

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
        Vypočíta level zo získaných XP podľa nelineárneho vzorca: XP = 100 * (Level - 1)^1.5.
        """
        if self.xp < 100:
            return 1
        return int((self.xp / 100) ** (2 / 3)) + 1

    def xp_for_next_level(self):
        """Vráti celkový počet XP potrebných na dosiahnutie ďalšej úrovne."""
        return int(100 * (self.level ** 1.5))

    def xp_for_current_level(self):
        """Vráti počet XP, od ktorého začína aktuálna úroveň (100 * (Level - 1)^1.5)."""
        return int(100 * ((self.level - 1) ** 1.5))

    def level_progress_pct(self):
        """Percentuálny postup v rámci aktuálnej úrovne (pre progress bar v profile a na dashboarde)."""
        start, end = self.xp_for_current_level(), self.xp_for_next_level()
        if end <= start:
            return 100
        return max(0, min(100, int((self.xp - start) * 100 / (end - start))))

    def xp_to_next_level(self):
        return max(0, self.xp_for_next_level() - self.xp)

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

    # ------------------------------------------------------------------
    # Denný Streak: registrácia aktivity, detekcia prerušenia a záchrana
    # ------------------------------------------------------------------
    def register_activity(self):
        """
        Zaznamená dnešnú aktivitu (vyriešená úloha) a predĺži sériu.
        Neukladá objekt - uloženie zabezpečí volajúci kód. Vráti True, ak sa séria zmenila.
        """
        today = timezone.localdate()
        if self.last_activity_date == today:
            return False
        if self.last_activity_date == today - timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
        self.last_activity_date = today
        self.longest_streak = max(self.longest_streak, self.current_streak)
        return True

    def refresh_streak_state(self):
        """
        Skontroluje, či študent nevynechal deň. Ak má v inventári zmrazenia (streak_freezes),
        spotrebujú sa na vynechané dni. Inak sa séria presunie do `lost_streak_value`
        a študent ju môže do 24 hodín zachrániť za Doros. Vráti True, ak došlo k zmene.
        """
        now = timezone.now()
        today = timezone.localdate()
        changed = False

        window = timedelta(hours=getattr(settings, 'STREAK_REPAIR_WINDOW_HOURS', 24))
        if self.lost_streak_value and self.streak_lost_at and now > self.streak_lost_at + window:
            self.lost_streak_value = 0
            self.streak_lost_at = None
            changed = True

        if self.current_streak > 0 and self.last_activity_date and self.last_activity_date < today - timedelta(days=1):
            missed_days = (today - self.last_activity_date).days - 1
            if self.streak_freezes >= missed_days:
                self.streak_freezes -= missed_days
                self.last_activity_date = today - timedelta(days=1)
            else:
                self.lost_streak_value = self.current_streak
                self.streak_lost_at = now
                self.current_streak = 0
            changed = True

        if changed:
            self.save(update_fields=[
                'current_streak', 'lost_streak_value', 'streak_lost_at',
                'streak_freezes', 'last_activity_date'
            ])
        return changed

    def streak_repair_deadline(self):
        if not self.streak_lost_at:
            return None
        return self.streak_lost_at + timedelta(hours=getattr(settings, 'STREAK_REPAIR_WINDOW_HOURS', 24))

    # ------------------------------------------------------------------
    # Freemium limit AI tútora Codo
    # ------------------------------------------------------------------
    def ai_hints_remaining(self):
        """Počet zostávajúcich AI rád na dnes. None = neobmedzene (PRO / EDU / učiteľ)."""
        if self.has_pro_access():
            return None
        limit = getattr(settings, 'FREE_DAILY_AI_HINTS', 5)
        used = self.daily_ai_hints_used if self.last_ai_hint_date == timezone.localdate() else 0
        return max(0, limit - used)

    def consume_ai_hint(self):
        """Spotrebuje 1 AI radu. Vráti False, ak FREE účet už vyčerpal denný limit."""
        if self.has_pro_access():
            return True
        today = timezone.localdate()
        if self.last_ai_hint_date != today:
            self.daily_ai_hints_used = 0
            self.last_ai_hint_date = today
        if self.daily_ai_hints_used >= getattr(settings, 'FREE_DAILY_AI_HINTS', 5):
            return False
        self.daily_ai_hints_used += 1
        self.save(update_fields=['daily_ai_hints_used', 'last_ai_hint_date'])
        return True

    def avatar_emoji(self):
        choice = dict(self.AVATAR_CHOICES).get(self.avatar, '👦')
        # Ak je to string v tvare "👦 Alex", extrahujeme prvý symbol
        return choice.split()[0] if choice else '👦'

    def get_avatar_url(self):
        """Vráti URL adresu obrázka avatara používateľa."""
        image_map = {
            'student_alex': '/static/img/avatars/student_alex.jpg',
            'student_mia': '/static/img/avatars/student_mia.jpg',
            'student_sam': '/static/img/avatars/student_sam.jpg',
            'cyber_ninja': '/static/img/avatars/cyber_ninja.jpg',
            'codo': '/static/img/avatars/codo.png',
        }
        if self.avatar in image_map:
            return image_map[self.avatar]
        return '/static/img/avatars/student_alex.jpg'

    def avatar_hex(self):
        return dict(self.AVATAR_COLORS).get(self.avatar_color, '#4636F5')

    def display_name(self):
        return self.get_full_name() or self.username

    def is_teacher(self):
        return self.role in [self.Role.TEACHER, self.Role.ADMIN] or self.is_superuser or self.is_staff

    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser or self.is_staff

    def has_pro_access(self):
        return self.subscription_tier in [self.SubscriptionTier.PRO, self.SubscriptionTier.EDU] or self.is_teacher() or self.is_admin()

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


class SchoolLicenseRequest(models.Model):
    """Oficiálna žiadosť školy / pedagóga o zaobstaranie školskej EDU licencie Codoro."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Čaká na spracovanie'
        APPROVED = 'APPROVED', 'Schválená (Aktívna)'
        REJECTED = 'REJECTED', 'Zamietnutá'

    school_name = models.CharField(max_length=150, verbose_name="Názov školy / Vzdelávacej inštitúcie")
    contact_name = models.CharField(max_length=100, verbose_name="Meno a priezvisko vyučujúceho")
    email = models.EmailField(verbose_name="Školská e-mailová adresa")
    phone = models.CharField(max_length=40, blank=True, verbose_name="Telefónny kontakt")
    estimated_students = models.PositiveIntegerField(default=30, verbose_name="Predpokladaný počet žiakov")
    note = models.TextField(blank=True, verbose_name="Zameranie odboru alebo poznámka")
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Stav žiadosti"
    )
    generated_license = models.ForeignKey(
        SubscriptionLicense,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='school_requests',
        verbose_name="Priradený licenčný kľúč"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Žiadosť o školskú licenciu"
        verbose_name_plural = "Žiadosti o školské licencie"

    def __str__(self):
        return f"{self.school_name} - {self.contact_name} ({self.get_status_display()})"