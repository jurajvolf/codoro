import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase, QuizQuestion
from gamification.models import (
    RewardItem, Quest, ClassQuest, CoinDrop, Badge, DorosTransaction
)


def run_seed():
    print("🚀 Spúšťam napĺňanie databázy Codoro...")

    # 1. Vytvorenie učiteľa a študentov
    teacher, _ = User.objects.get_or_create(
        username='ucitel',
        defaults={
            'first_name': 'Markéta',
            'last_name': 'Brišová',
            'email': 'ucitel@codoro.sk',
            'role': User.Role.TEACHER,
            'subscription_tier': User.SubscriptionTier.EDU,
            'doros': 9999,
            'level': 20,
            'xp': 15000,
        }
    )
    teacher.set_password('heslo123')
    teacher.save()

    school_class, _ = SchoolClass.objects.get_or_create(
        join_code='IVC-2027',
        defaults={
            'name': 'IV.C - Informačno-mediálne technológie',
            'teacher': teacher
        }
    )

    student, _ = User.objects.get_or_create(
        username='student',
        defaults={
            'first_name': 'Juraj',
            'last_name': 'Volf',
            'email': 'student@codoro.sk',
            'role': User.Role.STUDENT,
            'school_class': school_class,
            'subscription_tier': User.SubscriptionTier.FREE,
            'doros': 350,
            'xp': 240,
            'level': 2,
            'current_streak': 4,
            'longest_streak': 7,
            'last_activity_date': timezone.now().date() - timedelta(days=1),
            'lost_streak_value': 9,
            'streak_lost_at': timezone.now() - timedelta(hours=5),
        }
    )
    student.set_password('heslo123')
    student.save()

    # Druhý spolužiak do rebríčka a kolektívneho questu
    classmate, _ = User.objects.get_or_create(
        username='martin_k',
        defaults={
            'first_name': 'Martin',
            'last_name': 'Kováč',
            'email': 'martin@codoro.sk',
            'role': User.Role.STUDENT,
            'school_class': school_class,
            'subscription_tier': User.SubscriptionTier.EDU,
            'doros': 520,
            'xp': 680,
            'level': 4,
            'current_streak': 6,
        }
    )
    classmate.set_password('heslo123')
    classmate.save()

    # 2. Školský licenčný kľúč na odomknutie EDU/PRO
    SubscriptionLicense.objects.get_or_create(
        code='EDU-2027-IVC',
        defaults={
            'tier': User.SubscriptionTier.EDU,
            'max_uses': 30,
            'current_uses': 1,
            'is_active': True
        }
    )

    # 3. Moduly, Lekcie, Cvičenia a Testovacie prípady (SK + EN)
    mod1, _ = Module.objects.get_or_create(
        order=1,
        defaults={
            'title_sk': 'Základy jazyka Python a premenné',
            'title_en': 'Python Basics and Variables',
            'description_sk': 'Zoznám sa so syntaxou Pythonu, výpisom do konzoly, premennými a základnými matematickými operáciami.',
            'description_en': 'Learn Python syntax, console output, variables, and basic math operations.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-terminal-fill'
        }
    )

    lesson1, _ = Lesson.objects.get_or_create(
        module=mod1,
        order=1,
        defaults={
            'title_sk': 'Výpis textu a práca s premennými',
            'title_en': 'Printing Text and Working with Variables',
            'content_sk': (
                "### Funkcia `print()` a premenné\n\n"
                "V jazyku Python používame na výpis hodnôt na obrazovku vstavanú funkciu `print()`.\n\n"
                "```python\n"
                "meno = 'Codoro'\n"
                "body = 100\n"
                "print(meno, body)\n"
                "```\n\n"
                "**Dôležité pravidlá:**\n"
                "- Python rozlišuje veľké a malé písmená (`body` a `Body` sú dve rôzne premenné).\n"
                "- Funkcie vytvárate pomocou kľúčového slova `def` a výsledok vraciate cez `return`."
            ),
            'content_en': (
                "### The `print()` Function and Variables\n\n"
                "In Python, we use the built-in `print()` function to display values on the screen.\n\n"
                "```python\n"
                "name = 'Codoro'\n"
                "points = 100\n"
                "print(name, points)\n"
                "```\n\n"
                "**Key rules:**\n"
                "- Python is case-sensitive.\n"
                "- Functions are defined using the `def` keyword and return values via `return`."
            ),
            'xp_reward': 25
        }
    )

    ex1, _ = Exercise.objects.get_or_create(
        lesson=lesson1,
        order=1,
        defaults={
            'title_sk': 'Výpočet odmeny v Doros',
            'title_en': 'Calculating Doros Reward',
            'instructions_sk': (
                "Napíš funkciu `vypocitaj_odmenu(ulohy, bonus)`, ktorá vráti celkový počet získaných mincí Doros.\n"
                "Za každú vyriešenú úlohu (`ulohy`) dostane študent **20 Doros** a k výsledku sa pripočíta hodnota `bonus`."
            ),
            'instructions_en': (
                "Write a function `vypocitaj_odmenu(ulohy, bonus)` that returns the total Doros earned.\n"
                "Each solved task (`ulohy`) gives **20 Doros**, plus the `bonus` value."
            ),
            'starter_code': "def vypocitaj_odmenu(ulohy, bonus):\n    # Sem napíš svoj výpočet a vráť výsledok cez return\n    pass\n",
            'solution_code': "def vypocitaj_odmenu(ulohy, bonus):\n    return ulohy * 20 + bonus\n",
            'hint_sk': "Vynásob parameter `ulohy` číslom 20, pripočítaj `bonus` a pred výraz daj kľúčové slovo `return`.",
            'hint_en': "Multiply `ulohy` by 20, add `bonus`, and use the `return` keyword.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 50,
            'doros_reward': 30
        }
    )

    TestCase.objects.get_or_create(
        exercise=ex1,
        test_code="assert vypocitaj_odmenu(3, 10) == 70, 'Pre (3, 10) má funkcia vrátiť 70'",
        defaults={'input_data': 'vypocitaj_odmenu(3, 10)', 'expected_output': '70', 'is_hidden': False}
    )
    TestCase.objects.get_or_create(
        exercise=ex1,
        test_code="assert vypocitaj_odmenu(0, 50) == 50, 'Pre (0, 50) má funkcia vrátiť 50'",
        defaults={'input_data': 'vypocitaj_odmenu(0, 50)', 'expected_output': '50', 'is_hidden': False}
    )
    TestCase.objects.get_or_create(
        exercise=ex1,
        test_code="assert vypocitaj_odmenu(10, 25) == 225, 'Skrytý test zlyhal'",
        defaults={'input_data': 'Skrytý test', 'expected_output': '225', 'is_hidden': True}
    )

    QuizQuestion.objects.get_or_create(
        lesson=lesson1,
        question_sk="Ktoré kľúčové slovo v jazyku Python slúži na definovanie vlastnej funkcie?",
        defaults={
            'question_en': "Which keyword in Python is used to define a custom function?",
            'option_a_sk': 'function', 'option_a_en': 'function',
            'option_b_sk': 'def', 'option_b_en': 'def',
            'option_c_sk': 'fun', 'option_c_en': 'fun',
            'correct_option': 'B'
        }
    )

    # Druhý modul: Podmienky a cykly
    mod2, _ = Module.objects.get_or_create(
        order=2,
        defaults={
            'title_sk': 'Podmienky, cykly a práca so zoznamami',
            'title_en': 'Conditions, Loops, and Lists',
            'description_sk': 'Nauč sa vetviť program pomocou if/else a spracovávať kolekcie dát cez cyklus for.',
            'description_en': 'Learn how to branch code using if/else and iterate over data with for loops.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-diagram-3-fill'
        }
    )

    lesson2, _ = Lesson.objects.get_or_create(
        module=mod2,
        order=1,
        defaults={
            'title_sk': 'Filtrovanie hodnôt pomocou cyklu for',
            'title_en': 'Filtering Values with a For Loop',
            'content_sk': (
                "### Prechádzanie zoznamu v Pythone\n\n"
                "Zoznam (`list`) uchováva viacero prvkov. Pomocou cyklu `for` a podmienky `if` vieme vybrať len tie prvky, ktoré spĺňajú podmienku:\n\n"
                "```python\n"
                "znamky = [1, 3, 1, 2, 1]\n"
                "jednotky = [z for z in znamky if z == 1]\n"
                "```"
            ),
            'content_en': (
                "### Iterating Over a List in Python\n\n"
                "A `list` stores multiple items. Using a `for` loop and an `if` condition, we can filter elements:\n\n"
                "```python\n"
                "grades = [1, 3, 1, 2, 1]\n"
                "best = [g for g in grades if g == 1]\n"
                "```"
            ),
            'xp_reward': 30
        }
    )

    ex2, _ = Exercise.objects.get_or_create(
        lesson=lesson2,
        order=1,
        defaults={
            'title_sk': 'Počet úspešných študentov',
            'title_en': 'Count Passing Students',
            'instructions_sk': (
                "Napíš funkciu `uspesni_studenti(body_zoznam)`, ktorá prijme zoznam bodov študentov z testu "
                "a vráti **počet** študentov, ktorí získali **aspoň 50 bodov** (t. j. `>= 50`)."
            ),
            'instructions_en': (
                "Write a function `uspesni_studenti(body_zoznam)` that takes a list of test scores "
                "and returns the **count** of students who scored **at least 50 points** (`>= 50`)."
            ),
            'starter_code': "def uspesni_studenti(body_zoznam):\n    # Vráť počet študentov s bodmi >= 50\n    pass\n",
            'solution_code': "def uspesni_studenti(body_zoznam):\n    return sum(1 for b in body_zoznam if b >= 50)\n",
            'hint_sk': "Vytvor si počítadlo `pocet = 0`, prebehni zoznam cez `for body in body_zoznam:` a ak `body >= 50`, zvýš `pocet += 1`.",
            'hint_en': "Create a counter `count = 0`, loop through `body_zoznam`, and increment when score `>= 50`.",
            'hint_cost_doros': 20,
            'difficulty': Exercise.Difficulty.MEDIUM,
            'xp_reward': 75,
            'doros_reward': 45
        }
    )

    TestCase.objects.get_or_create(
        exercise=ex2,
        test_code="assert uspesni_studenti([20, 50, 85, 49, 100]) == 3",
        defaults={'input_data': 'uspesni_studenti([20, 50, 85, 49, 100])', 'expected_output': '3', 'is_hidden': False}
    )
    TestCase.objects.get_or_create(
        exercise=ex2,
        test_code="assert uspesni_studenti([10, 20, 30]) == 0",
        defaults={'input_data': 'uspesni_studenti([10, 20, 30])', 'expected_output': '0', 'is_hidden': False}
    )

    # Tretí modul: PRO / EDU obsah
    Module.objects.get_or_create(
        order=3,
        defaults={
            'title_sk': 'Objektovo-orientované programovanie (OOP)',
            'title_en': 'Object-Oriented Programming (OOP)',
            'description_sk': 'Pokročilý modul: triedy, objekty, dedičnosť a zapuzdrenie v Pythone (Dostupné pre PRO / EDU licenciu).',
            'description_en': 'Advanced module: classes, objects, inheritance, and encapsulation in Python (PRO / EDU tier).',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': True,
            'icon_name': 'bi-boxes'
        }
    )

    # 4. Učiteľský obchod s odmenami a riadením zásob
    RewardItem.objects.get_or_create(
        title_sk='Žolík: Odpustenie domácej úlohy',
        defaults={
            'title_en': 'Joker: Homework Pass',
            'description_sk': 'Umožňuje vynechať 1 domácu úlohu bez straty bodov. Obmedzená zásoba pre triedu!',
            'description_en': 'Allows skipping 1 homework assignment without penalty. Limited class stock!',
            'cost_doros': 250,
            'icon_name': 'bi-shield-check',
            'max_stock': 2,
            'current_stock': 2,
            'restock_period': RewardItem.RestockPeriod.WEEKLY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    RewardItem.objects.get_or_create(
        title_sk='+10 % bodov k praktickej písomke',
        defaults={
            'title_en': '+10% Bonus Points on Practical Exam',
            'description_sk': 'Pripočíta 10 % bonusových bodov k najbližšiemu testu z programovania.',
            'description_en': 'Adds 10% bonus points to your next coding test.',
            'cost_doros': 500,
            'icon_name': 'bi-graph-up-arrow',
            'max_stock': 1,
            'current_stock': 1,
            'restock_period': RewardItem.RestockPeriod.MONTHLY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    RewardItem.objects.get_or_create(
        title_sk='Nápoveda od učiteľa počas písomky',
        defaults={
            'title_en': 'Teacher Hint During Test',
            'description_sk': 'Učiteľ ti počas praktického testu pomôže odhaliť 1 chybu v kóde (Obnovuje sa 2x denne).',
            'description_en': 'The teacher will help you debug 1 issue during a test (Restocks 2x daily).',
            'cost_doros': 180,
            'icon_name': 'bi-lightbulb-fill',
            'max_stock': 2,
            'current_stock': 2,
            'restock_period': RewardItem.RestockPeriod.DAILY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    # 5. Osobné Questy (Daily, Weekly, Monthly)
    Quest.objects.get_or_create(
        title_sk='Ranná rozcvička: Vyrieš 1 cvičenie',
        defaults={
            'title_en': 'Morning Warmup: Solve 1 Exercise',
            'period': Quest.QuestPeriod.DAILY,
            'metric_type': Quest.MetricType.SOLVE_EXERCISES,
            'target_value': 1,
            'reward_doros': 40,
            'reward_xp': 25
        }
    )
    Quest.objects.get_or_create(
        title_sk='Týždenný šprint: Nazbieraj 150 XP',
        defaults={
            'title_en': 'Weekly Sprint: Earn 150 XP',
            'period': Quest.QuestPeriod.WEEKLY,
            'metric_type': Quest.MetricType.EARN_XP,
            'target_value': 150,
            'reward_doros': 150,
            'reward_xp': 80
        }
    )
    Quest.objects.get_or_create(
        title_sk='Mesačný majster: Vyrieš 10 úloh na 1. pokus',
        defaults={
            'title_en': 'Monthly Master: Solve 10 Tasks on 1st Try',
            'period': Quest.QuestPeriod.MONTHLY,
            'metric_type': Quest.MetricType.FIRST_TRY_SOLVES,
            'target_value': 10,
            'reward_doros': 600,
            'reward_xp': 300
        }
    )

    # 6. Kolektívny triedny Quest pre IV.C
    ClassQuest.objects.get_or_create(
        school_class=school_class,
        title_sk='Spoločná výzva IV.C: 20 vyriešených úloh za týždeň',
        defaults={
            'title_en': 'IV.C Class Quest: 20 Solved Tasks This Week',
            'period': Quest.QuestPeriod.WEEKLY,
            'target_exercises_count': 20,
            'current_exercises_count': 14,
            'reward_policy': ClassQuest.RewardPolicy.CONTRIBUTORS_ONLY,
            'min_contribution_required': 1,
            'reward_doros_per_student': 200,
            'deadline': timezone.now() + timedelta(days=5)
        }
    )

    # 7. Aktívny Coin Drop (aby bol hneď viditeľný na Dashboarde)
    CoinDrop.objects.get_or_create(
        title_sk='Popoludňajší Bonus Drop za aktivitu!',
        defaults={
            'title_en': 'Afternoon Activity Bonus Drop!',
            'school_class': school_class,
            'available_from': timezone.now() - timedelta(minutes=15),
            'available_until': timezone.now() + timedelta(hours=12),
            'max_claims': 5,
            'min_doros': 40,
            'max_doros': 120,
            'created_by': teacher
        }
    )

    # 8. Ukážková transakcia v peňaženke
    if not DorosTransaction.objects.filter(student=student).exists():
        DorosTransaction.objects.create(
            student=student,
            amount=350,
            reason_sk='Štartovací bonus a odmeny za doterajšiu aktivitu',
            reason_en='Starter bonus and activity rewards'
        )

    print("✅ Databáza Codoro bola úspešne naplnená!")
    print("👉 Prihlásenie UČITEĽ:  meno: ucitel  | heslo: heslo123")
    print("👉 Prihlásenie ŠTUDENT: meno: student | heslo: heslo123")


if __name__ == '__main__':
    run_seed()