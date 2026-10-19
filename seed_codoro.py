import os
import sys
from datetime import timedelta

# Zaistenie UTF-8 výstupu v termináli Windows (rieši UnicodeEncodeError pre emoji)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.utils import timezone
from accounts.models import User, SchoolClass, SubscriptionLicense
from courses.models import Module, Lesson, Exercise, TestCase, QuizQuestion
from gamification.models import (
    RewardItem, Quest, ClassQuest, CoinDrop, Badge, DorosTransaction
)
from gamification.services import ensure_badges_exist


def run_seed():
    print("🚀 Spúšťam napĺňanie databázy Codoro...")

    # 1. Odznaky (Achievements)
    ensure_badges_exist()
    print("🎖️ Štandardné odznaky vytvorené.")

    # 2. Vytvorenie učiteľa a študentov
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
            'avatar': 'wizard',
            'avatar_color': 'indigo',
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
            'last_activity_date': timezone.localdate() - timedelta(days=1),
            'lost_streak_value': 9,
            'streak_lost_at': timezone.now() - timedelta(hours=5),
            'avatar': 'codo',
            'avatar_color': 'cyan',
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
            'longest_streak': 8,
            'avatar': 'fox',
            'avatar_color': 'amber',
        }
    )
    classmate.set_password('heslo123')
    classmate.save()

    # 3. Školský licenčný kľúč na odomknutie EDU/PRO
    SubscriptionLicense.objects.get_or_create(
        code='EDU-2027-IVC',
        defaults={
            'tier': User.SubscriptionTier.EDU,
            'max_uses': 30,
            'current_uses': 1,
            'is_active': True
        }
    )

    # ==================================================================
    # 4. KOMPLETNÝCH 6 MODULOV STREDOŠKOLSKÉHO KURZU PYTHONU (16 LEKCIÍ)
    # ==================================================================

    # ------------------------------------------------------------------
    # MODUL 1: Premenné a dátové typy
    # ------------------------------------------------------------------
    mod1, _ = Module.objects.update_or_create(
        order=1,
        defaults={
            'title_sk': '1. Premenné a dátové typy',
            'title_en': '1. Variables & Data Types',
            'description_sk': 'Zoznám sa so syntaxou Pythonu, výpisom do konzoly, premennými a základnými matematickými operáciami.',
            'description_en': 'Learn Python syntax, console output, variables, and basic math operations.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-terminal-fill'
        }
    )

    lesson1_1, _ = Lesson.objects.update_or_create(
        module=mod1,
        order=1,
        defaults={
            'title_sk': 'Premenné, funkcia print() a návrat hodnôt',
            'title_en': 'Variables, print() and return Values',
            'content_sk': (
                "### Základné pravidlá práce s premennými v Pythone\n\n"
                "Premenná slúži ako pomenované úložisko v pamäti. Do premennej priradíme hodnotu pomocou operátora `=`. "
                "Python je **dynamicky typovaný jazyk**, čo znamená, že typ premennej (`int`, `float`, `str`, `bool`) nemusíme písať ručne.\n\n"
                "```python\n"
                "nazov = 'Codoro'\n"
                "pocet_minci = 100\n"
                "aktivny = True\n"
                "print(nazov, pocet_minci)\n"
                "```\n\n"
                "**Funkcie a príkaz return:**\n"
                "V automatických testoch a cvičeniach Codoro píšeme kód do **funkcií**. "
                "Funkciu definujeme pomocou kľúčového slova `def` a výsledok vraciame cez `return` (nie iba cez `print()`!):\n\n"
                "```python\n"
                "def sucet(a, b):\n"
                "    return a + b\n"
                "```"
            ),
            'content_en': (
                "### Basic Rules of Variables in Python\n\n"
                "A variable is a named storage location. We assign values using the `=` operator. "
                "Python is **dynamically typed**, so we don't have to declare types (`int`, `float`, `str`, `bool`) manually.\n\n"
                "```python\n"
                "name = 'Codoro'\n"
                "coins = 100\n"
                "active = True\n"
                "print(name, coins)\n"
                "```\n\n"
                "**Functions and the return statement:**\n"
                "In Codoro exercises, functions are verified through unit tests. "
                "Functions are defined with `def` and results are returned using `return` (not just printed via `print()`!):\n\n"
                "```python\n"
                "def add(a, b):\n"
                "    return a + b\n"
                "```"
            ),
            'xp_reward': 25
        }
    )

    ex1_1, _ = Exercise.objects.update_or_create(
        lesson=lesson1_1,
        order=1,
        defaults={
            'title_sk': 'Výpočet odmeny v Doros',
            'title_en': 'Calculating Doros Reward',
            'instructions_sk': (
                "Napíš funkciu `vypocitaj_odmenu(ulohy, bonus)`, ktorá vráti celkový počet získaných mincí Doros.\n\n"
                "Za každú vyriešenú úlohu (`ulohy`) dostane študent **20 Doros** a k celkovému výsledku sa pripočíta jednorazový `bonus`."
            ),
            'instructions_en': (
                "Write a function `vypocitaj_odmenu(ulohy, bonus)` that returns the total Doros earned.\n\n"
                "Each solved task (`ulohy`) grants **20 Doros**, plus the one-time `bonus`."
            ),
            'starter_code': "def vypocitaj_odmenu(ulohy, bonus):\n    # Sem napíš svoj výpočet a vráť výsledok cez return\n    pass\n",
            'solution_code': "def vypocitaj_odmenu(ulohy, bonus):\n    return ulohy * 20 + bonus\n",
            'hint_sk': "Vynásob parameter `ulohy` číslom 20, pripočítaj `bonus` a použi kľúčové slovo `return`.",
            'hint_en': "Multiply `ulohy` by 20, add `bonus`, and use `return`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 50,
            'doros_reward': 30
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex1_1,
        test_code="assert vypocitaj_odmenu(3, 10) == 70, 'Pre (3, 10) má funkcia vrátiť 70'",
        defaults={'input_data': 'vypocitaj_odmenu(3, 10)', 'expected_output': '70', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex1_1,
        test_code="assert vypocitaj_odmenu(0, 50) == 50, 'Pre (0, 50) má funkcia vrátiť 50'",
        defaults={'input_data': 'vypocitaj_odmenu(0, 50)', 'expected_output': '50', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex1_1,
        test_code="assert vypocitaj_odmenu(10, 25) == 225, 'Skrytý test zlyhal'",
        defaults={'input_data': 'Skrytý test', 'expected_output': '225', 'is_hidden': True}
    )
    QuizQuestion.objects.update_or_create(
        lesson=lesson1_1,
        question_sk="Ktoré kľúčové slovo v jazyku Python slúži na vrátenie výsledku z funkcie?",
        defaults={
            'question_en': "Which keyword in Python is used to send a value back from a function?",
            'option_a_sk': 'print', 'option_a_en': 'print',
            'option_b_sk': 'return', 'option_b_en': 'return',
            'option_c_sk': 'give', 'option_c_en': 'give',
            'correct_option': 'B'
        }
    )

    lesson1_2, _ = Lesson.objects.update_or_create(
        module=mod1,
        order=2,
        defaults={
            'title_sk': 'Dátové typy a reťazce f-strings',
            'title_en': 'Data Types & f-strings Formatting',
            'content_sk': (
                "### Formátované reťazce (f-strings)\n\n"
                "Od verzie Python 3.6 je najefektívnejším spôsobom spájania textu a premenných tzv. **f-string**:\n\n"
                "```python\n"
                "meno = 'Codo'\n"
                "level = 5\n"
                "sprava = f'Hráč {meno} má úroveň {level}'\n"
                "```\n\n"
                "Výrazy vo vnútri zložených zátvoriek `{}` sa automaticky vyhodnotia a prevedú na text."
            ),
            'content_en': (
                "### Formatted String Literals (f-strings)\n\n"
                "Since Python 3.6, the cleanest way to embed expressions inside string literals is via **f-strings**:\n\n"
                "```python\n"
                "name = 'Codo'\n"
                "level = 5\n"
                "msg = f'Player {name} is at level {level}'\n"
                "```"
            ),
            'xp_reward': 25
        }
    )
    ex1_2, _ = Exercise.objects.update_or_create(
        lesson=lesson1_2,
        order=1,
        defaults={
            'title_sk': 'Formátovanie hernej vizitky',
            'title_en': 'Formatting Player Badge Card',
            'instructions_sk': (
                "Napíš funkciu `vytvor_profil(meno, level)`, ktorá vráti presný reťazec v tvare:\n"
                "`'Hráč MENO (Level LEVEL)'` pomocou f-stringu."
            ),
            'instructions_en': (
                "Write a function `vytvor_profil(meno, level)` returning `'Hráč MENO (Level LEVEL)'` using an f-string."
            ),
            'starter_code': "def vytvor_profil(meno, level):\n    # Použi f-string a vráť požadovaný text\n    pass\n",
            'solution_code': "def vytvor_profil(meno, level):\n    return f'Hráč {meno} (Level {level})'\n",
            'hint_sk': "Použi syntax `f'Hráč {meno} (Level {level})'`.",
            'hint_en': "Use the syntax `f'Hráč {meno} (Level {level})'`.",
            'hint_cost_doros': 10,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 45,
            'doros_reward': 25
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex1_2,
        test_code="assert vytvor_profil('Juraj', 2) == 'Hráč Juraj (Level 2)'",
        defaults={'input_data': "vytvor_profil('Juraj', 2)", 'expected_output': 'Hráč Juraj (Level 2)', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex1_2,
        test_code="assert vytvor_profil('Codo', 99) == 'Hráč Codo (Level 99)'",
        defaults={'input_data': "vytvor_profil('Codo', 99)", 'expected_output': 'Hráč Codo (Level 99)', 'is_hidden': False}
    )
    QuizQuestion.objects.update_or_create(
        lesson=lesson1_2,
        question_sk="Ktoré písmeno uvádzame pred úvodzovkami formátovaného reťazca?",
        defaults={
            'question_en': "Which letter prefixes a formatted string literal in Python?",
            'option_a_sk': 'f', 'option_a_en': 'f',
            'option_b_sk': 's', 'option_b_en': 's',
            'option_c_sk': 'str', 'option_c_en': 'str',
            'correct_option': 'A'
        }
    )

    lesson1_3, _ = Lesson.objects.update_or_create(
        module=mod1,
        order=3,
        defaults={
            'title_sk': 'Aritmetické operácie a celočíselné delenie',
            'title_en': 'Arithmetic Operations & Integer Division',
            'content_sk': (
                "### Celočíselné delenie (`//`) a zvyšok po delení (`%`)\n\n"
                "V Pythone máme dva špeciálne operátory delenia:\n"
                "- `//` celočíselné delenie: `7 // 2` je `3` (odsekne desatinnú časť)\n"
                "- `%` modulo (zvyšok po delení): `7 % 2` je `1`\n"
                "- `/` bežné delenie vždy vracia typ `float`: `7 / 2` je `3.5`"
            ),
            'content_en': (
                "### Integer Division (`//`) and Modulo (`%`)\n\n"
                "Python provides distinct division operators:\n"
                "- `//` floor division: `7 // 2` is `3`\n"
                "- `%` modulo remainder: `7 % 2` is `1`\n"
                "- `/` standard division always returns `float`: `7 / 2` is `3.5`"
            ),
            'xp_reward': 25
        }
    )
    ex1_3, _ = Exercise.objects.update_or_create(
        lesson=lesson1_3,
        order=1,
        defaults={
            'title_sk': 'Prevod sekúnd na celé minúty',
            'title_en': 'Convert Seconds to Full Minutes',
            'instructions_sk': (
                "Napíš funkciu `cele_minuty(sekundy)`, ktorá vráti počet **celých minút** v zadanom počte sekúnd pomocou operátora `//`."
            ),
            'instructions_en': (
                "Write a function `cele_minuty(sekundy)` returning the integer number of full minutes using `//`."
            ),
            'starter_code': "def cele_minuty(sekundy):\n    # Použi operátor // na prevod na minúty\n    pass\n",
            'solution_code': "def cele_minuty(sekundy):\n    return sekundy // 60\n",
            'hint_sk': "Vydeľ parameter `sekundy` číslom 60 cez celočíselné delenie `//`.",
            'hint_en': "Divide `sekundy` by 60 using integer division `//`.",
            'hint_cost_doros': 10,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 45,
            'doros_reward': 25
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex1_3,
        test_code="assert cele_minuty(125) == 2",
        defaults={'input_data': 'cele_minuty(125)', 'expected_output': '2', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex1_3,
        test_code="assert cele_minuty(60) == 1",
        defaults={'input_data': 'cele_minuty(60)', 'expected_output': '1', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex1_3,
        test_code="assert cele_minuty(59) == 0",
        defaults={'input_data': 'cele_minuty(59)', 'expected_output': '0', 'is_hidden': False}
    )

    # ------------------------------------------------------------------
    # MODUL 2: Podmienky a vetvenie programu
    # ------------------------------------------------------------------
    mod2, _ = Module.objects.update_or_create(
        order=2,
        defaults={
            'title_sk': '2. Podmienky a vetvenie programu',
            'title_en': '2. Conditions & Branching',
            'description_sk': 'Nauč sa rozhodovať v programe pomocou if, elif a else a logických operátorov and/or/not.',
            'description_en': 'Learn how to make decisions in your code using if, elif, else and logical operators.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-signpost-split-fill'
        }
    )

    lesson2_1, _ = Lesson.objects.update_or_create(
        module=mod2,
        order=1,
        defaults={
            'title_sk': 'Vetvenie programu cez if - elif - else',
            'title_en': 'Control Flow with if - elif - else',
            'content_sk': (
                "### Riadenie toku programu\n\n"
                "Podmienky umožňujú spustiť rôzne bloky kódu podľa toho, či je logický výraz pravdivý (`True`) alebo nepravdivý (`False`):\n\n"
                "```python\n"
                "skore = 85\n"
                "if skore >= 90:\n"
                "    znamka = 1\n"
                "elif skore >= 75:\n"
                "    znamka = 2\n"
                "else:\n"
                "    znamka = 3\n"
                "```\n\n"
                "**Porovnávacie operátory:**\n"
                "- `==` rovná sa (dve rovnátka! Jedno rovnátko `=` slúži na priradenie)\n"
                "- `!=` nerovná sa\n"
                "- `>`, `<`, `>=`, `<=` porovnanie čísel"
            ),
            'content_en': (
                "### Controlling Program Execution\n\n"
                "Conditions allow running different branches of code depending on boolean expressions (`True` / `False`):\n\n"
                "```python\n"
                "score = 85\n"
                "if score >= 90:\n"
                "    grade = 1\n"
                "elif score >= 75:\n"
                "    grade = 2\n"
                "else:\n"
                "    grade = 3\n"
                "```\n\n"
                "**Comparison operators:**\n"
                "- `==` equals (`=` is only for assignment)\n"
                "- `!=` not equals\n"
                "- `>`, `<`, `>=`, `<=` numeric comparisons"
            ),
            'xp_reward': 30
        }
    )

    ex2_1, _ = Exercise.objects.update_or_create(
        lesson=lesson2_1,
        order=1,
        defaults={
            'title_sk': 'Klasifikácia podľa bodov',
            'title_en': 'Grade Classification by Points',
            'instructions_sk': (
                "Napíš funkciu `ohodnot(body)`, ktorá vráti:\n"
                "- `'vyborne'` ak `body >= 90`\n"
                "- `'chvalitebne'` ak `body >= 75` (a menej ako 90)\n"
                "- `'dobre'` ak `body >= 50` (a menej ako 75)\n"
                "- `'nedostatocne'` pre menej ako 50 bodov"
            ),
            'instructions_en': (
                "Write a function `ohodnot(body)` that returns:\n"
                "- `'vyborne'` if `body >= 90`\n"
                "- `'chvalitebne'` if `body >= 75`\n"
                "- `'dobre'` if `body >= 50`\n"
                "- `'nedostatocne'` if below 50"
            ),
            'starter_code': "def ohodnot(body):\n    # Použi if, elif a else a vráť správny reťazec\n    pass\n",
            'solution_code': "def ohodnot(body):\n    if body >= 90:\n        return 'vyborne'\n    elif body >= 75:\n        return 'chvalitebne'\n    elif body >= 50:\n        return 'dobre'\n    return 'nedostatocne'\n",
            'hint_sk': "Začni najprísnejšou podmienkou `if body >= 90:` a postupuj nižšie cez `elif`.",
            'hint_en': "Start with the strictest boundary `if body >= 90:` and proceed downwards via `elif`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 50,
            'doros_reward': 30
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex2_1,
        test_code="assert ohodnot(95) == 'vyborne'",
        defaults={'input_data': 'ohodnot(95)', 'expected_output': 'vyborne', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_1,
        test_code="assert ohodnot(80) == 'chvalitebne'",
        defaults={'input_data': 'ohodnot(80)', 'expected_output': 'chvalitebne', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_1,
        test_code="assert ohodnot(49) == 'nedostatocne'",
        defaults={'input_data': 'ohodnot(49)', 'expected_output': 'nedostatocne', 'is_hidden': False}
    )

    lesson2_2, _ = Lesson.objects.update_or_create(
        module=mod2,
        order=2,
        defaults={
            'title_sk': 'Logické operátory and, or a párnosť',
            'title_en': 'Logical Operators and, or & Parity',
            'content_sk': (
                "### Logické spojky v Pythone\n\n"
                "- `and`: platí len vtedy, ak sú pravdivé **obidve** podmienky súčasne.\n"
                "- `or`: platí, ak je pravdivá **aspoň jedna** z podmienok.\n"
                "- `not`: neguje pravdivostnú hodnotu výrazu.\n\n"
                "Číslo je párne, ak po delení dvomi zostane zvyšok nula: `cislo % 2 == 0`."
            ),
            'content_en': (
                "### Logical Operators in Python\n\n"
                "- `and`: true only if **both** operands are true.\n"
                "- `or`: true if **at least one** operand is true.\n"
                "- `not`: negates the boolean value.\n\n"
                "A number is even if `number % 2 == 0`."
            ),
            'xp_reward': 30
        }
    )
    ex2_2, _ = Exercise.objects.update_or_create(
        lesson=lesson2_2,
        order=1,
        defaults={
            'title_sk': 'Kladné párne číslo',
            'title_en': 'Positive Even Number',
            'instructions_sk': (
                "Napíš funkciu `je_kladne_a_parne(cislo)`, ktorá vráti `True`, ak je číslo **väčšie ako 0** a zároveň **párne**. Inak vráti `False`."
            ),
            'instructions_en': (
                "Write a function `je_kladne_a_parne(cislo)` returning `True` if `cislo > 0` and even, otherwise `False`."
            ),
            'starter_code': "def je_kladne_a_parne(cislo):\n    # Použi operátor and a modulo %\n    pass\n",
            'solution_code': "def je_kladne_a_parne(cislo):\n    return cislo > 0 and cislo % 2 == 0\n",
            'hint_sk': "Spoj podmienku `cislo > 0` a `cislo % 2 == 0` operátorom `and`.",
            'hint_en': "Combine `cislo > 0` and `cislo % 2 == 0` with `and`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 50,
            'doros_reward': 30
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex2_2,
        test_code="assert je_kladne_a_parne(4) == True",
        defaults={'input_data': 'je_kladne_a_parne(4)', 'expected_output': 'True', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_2,
        test_code="assert je_kladne_a_parne(-4) == False",
        defaults={'input_data': 'je_kladne_a_parne(-4)', 'expected_output': 'False', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_2,
        test_code="assert je_kladne_a_parne(7) == False",
        defaults={'input_data': 'je_kladne_a_parne(7)', 'expected_output': 'False', 'is_hidden': False}
    )

    lesson2_3, _ = Lesson.objects.update_or_create(
        module=mod2,
        order=3,
        defaults={
            'title_sk': 'Vnorené podmienky a vstupné zľavy',
            'title_en': 'Nested Conditions & Ticket Pricing',
            'content_sk': (
                "### Kombinované rozhodovanie\n\n"
                "V praxi často kombinujeme vekové kategórie a status študenta. Správne poradie podmienok je kľúčom k prehľadnému kódu."
            ),
            'content_en': (
                "### Combined Decision Flow\n\n"
                "Combining numeric intervals with boolean attributes cleanly models real-world business logic."
            ),
            'xp_reward': 30
        }
    )
    ex2_3, _ = Exercise.objects.update_or_create(
        lesson=lesson2_3,
        order=1,
        defaults={
            'title_sk': 'Cena lístka do kina',
            'title_en': 'Cinema Ticket Price',
            'instructions_sk': (
                "Napíš funkciu `cena_listka(vek, je_student)`, ktorá určí cenu lístka v eurách:\n"
                "- Deti do 6 rokov (vek < 6): **0 eur** (zadarmo)\n"
                "- Študenti (ľubovoľný vek ak `je_student == True`) alebo seniori (vek >= 65): **5 eur**\n"
                "- Všetci ostatní: **10 eur**"
            ),
            'instructions_en': (
                "Write `cena_listka(vek, je_student)` returning ticket price: under 6 -> 0, students or seniors (>=65) -> 5, others -> 10."
            ),
            'starter_code': "def cena_listka(vek, je_student):\n    pass\n",
            'solution_code': "def cena_listka(vek, je_student):\n    if vek < 6:\n        return 0\n    elif je_student or vek >= 65:\n        return 5\n    return 10\n",
            'hint_sk': "Ako prvé skontroluj `if vek < 6: return 0`, potom `elif je_student or vek >= 65: return 5`.",
            'hint_en': "Check `if vek < 6:` first, then students and seniors.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.MEDIUM,
            'xp_reward': 60,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex2_3,
        test_code="assert cena_listka(4, False) == 0",
        defaults={'input_data': 'cena_listka(4, False)', 'expected_output': '0', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_3,
        test_code="assert cena_listka(17, True) == 5",
        defaults={'input_data': 'cena_listka(17, True)', 'expected_output': '5', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex2_3,
        test_code="assert cena_listka(30, False) == 10",
        defaults={'input_data': 'cena_listka(30, False)', 'expected_output': '10', 'is_hidden': False}
    )

    # ------------------------------------------------------------------
    # MODUL 3: Cykly for a while
    # ------------------------------------------------------------------
    mod3, _ = Module.objects.update_or_create(
        order=3,
        defaults={
            'title_sk': '3. Cykly for a while',
            'title_en': '3. For & While Loops',
            'description_sk': 'Opakuj príkazy pomocou cyklov, prechádzaj intervaly cez range() a nauč sa pracovať s akumulátormi.',
            'description_en': 'Repeat actions using loops, iterate over intervals with range(), and learn accumulators.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-arrow-repeat'
        }
    )

    lesson3_1, _ = Lesson.objects.update_or_create(
        module=mod3,
        order=1,
        defaults={
            'title_sk': 'Cykly for a funkcia range()',
            'title_en': 'For Loops and the range() Function',
            'content_sk': (
                "### Cyklus for a funkcia range()\n\n"
                "Ak vopred vieme, koľkokrát sa má kód zopakovať, používame cyklus `for` v spojení s funkciou `range()`:\n\n"
                "```python\n"
                "for i in range(5):        # i nadobudne hodnoty 0, 1, 2, 3, 4\n"
                "    print('Krok č.', i)\n"
                "```\n\n"
                "Funkcia `range(start, stop)` generuje čísla od `start` do `stop - 1` (horná hranica nie je zahrnutá!)."
            ),
            'content_en': (
                "### The for Loop and range() Function\n\n"
                "When we know the number of repetitions in advance, we combine `for` with `range()`:\n\n"
                "```python\n"
                "for i in range(5):        # generates 0, 1, 2, 3, 4\n"
                "    print('Step', i)\n"
                "```\n\n"
                "`range(start, stop)` generates integers from `start` to `stop - 1`."
            ),
            'xp_reward': 30
        }
    )

    ex3_1, _ = Exercise.objects.update_or_create(
        lesson=lesson3_1,
        order=1,
        defaults={
            'title_sk': 'Súčet čísel od 1 po n',
            'title_en': 'Sum of Numbers from 1 to n',
            'instructions_sk': (
                "Napíš funkciu `sucet_do(n)`, ktorá pomocou cyklu `for` sčíta všetky celé čísla od 1 po `n` (vrátane) a vráti celkový súčet.\n\n"
                "Napríklad pre `n = 4` vráti `1 + 2 + 3 + 4 = 10`."
            ),
            'instructions_en': (
                "Write a function `sucet_do(n)` that uses a `for` loop to sum integers from 1 up to `n` (inclusive) and returns the total.\n\n"
                "For example, for `n = 4` it returns `1 + 2 + 3 + 4 = 10`."
            ),
            'starter_code': "def sucet_do(n):\n    vysledok = 0\n    # Použi for cyklus a range(1, n + 1)\n    return vysledok\n",
            'solution_code': "def sucet_do(n):\n    vysledok = 0\n    for i in range(1, n + 1):\n        vysledok += i\n    return vysledok\n",
            'hint_sk': "Použi `range(1, n + 1)`, aby cyklus zahrnul aj číslo `n`.",
            'hint_en': "Use `range(1, n + 1)` so the upper bound includes `n`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 55,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex3_1,
        test_code="assert sucet_do(4) == 10",
        defaults={'input_data': 'sucet_do(4)', 'expected_output': '10', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex3_1,
        test_code="assert sucet_do(1) == 1",
        defaults={'input_data': 'sucet_do(1)', 'expected_output': '1', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex3_1,
        test_code="assert sucet_do(10) == 55",
        defaults={'input_data': 'sucet_do(10)', 'expected_output': '55', 'is_hidden': True}
    )

    lesson3_2, _ = Lesson.objects.update_or_create(
        module=mod3,
        order=2,
        defaults={
            'title_sk': 'Akumulátory a filtrovanie v cykle',
            'title_en': 'Accumulators & Filtering in Loops',
            'content_sk': (
                "### Akumulátor v cykle\n\n"
                "Akumulátor je premenná, do ktorej počas prechodu cyklom postupne pridávame hodnoty spĺňajúce zadané kritérium."
            ),
            'content_en': (
                "### Loop Accumulator Pattern\n\n"
                "An accumulator variable collects values across iterations that satisfy specific predicates."
            ),
            'xp_reward': 30
        }
    )
    ex3_2, _ = Exercise.objects.update_or_create(
        lesson=lesson3_2,
        order=1,
        defaults={
            'title_sk': 'Súčet párnych čísel do n',
            'title_en': 'Sum of Even Numbers up to n',
            'instructions_sk': (
                "Napíš funkciu `sucet_parnych(n)`, ktorá sčíta všetky **párne čísla** od 1 po `n` (vrátane) a vráti výsledok."
            ),
            'instructions_en': (
                "Write `sucet_parnych(n)` returning the sum of all even integers from 1 up to `n` (inclusive)."
            ),
            'starter_code': "def sucet_parnych(n):\n    pass\n",
            'solution_code': "def sucet_parnych(n):\n    return sum(i for i in range(1, n + 1) if i % 2 == 0)\n",
            'hint_sk': "Použi cyklus `for i in range(1, n + 1):` a pridaj podmienku `if i % 2 == 0:`.",
            'hint_en': "Iterate up to `n + 1` and filter with `i % 2 == 0`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 55,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex3_2,
        test_code="assert sucet_parnych(6) == 12",
        defaults={'input_data': 'sucet_parnych(6)', 'expected_output': '12', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex3_2,
        test_code="assert sucet_parnych(5) == 6",
        defaults={'input_data': 'sucet_parnych(5)', 'expected_output': '6', 'is_hidden': False}
    )

    lesson3_3, _ = Lesson.objects.update_or_create(
        module=mod3,
        order=3,
        defaults={
            'title_sk': 'Cyklus while a podmienka ukončenia',
            'title_en': 'While Loop & Termination Guard',
            'content_sk': (
                "### Cyklus while\n\n"
                "Cyklus `while` beží dovtedy, kým je jeho podmienka pravdivá. "
                "Používame ho, keď vopred nevieme presný počet opakovaní."
            ),
            'content_en': (
                "### The While Loop\n\n"
                "A `while` loop runs as long as its conditional guard evaluates to `True`."
            ),
            'xp_reward': 35
        }
    )
    ex3_3, _ = Exercise.objects.update_or_create(
        lesson=lesson3_3,
        order=1,
        defaults={
            'title_sk': 'Počet delení dvomi',
            'title_en': 'Count Divisions by Two',
            'instructions_sk': (
                "Napíš funkciu `pocet_deleni(n)`, ktorá pomocou cyklu `while` spočíta, koľkokrát možno číslo `n` celočíselne vydeliť dvomi bez zvyšku (pokiaľ je deliteľné)."
            ),
            'instructions_en': (
                "Write `pocet_deleni(n)` returning how many times `n` can be divided by 2 without remainder."
            ),
            'starter_code': "def pocet_deleni(n):\n    pass\n",
            'solution_code': "def pocet_deleni(n):\n    pocet = 0\n    while n > 0 and n % 2 == 0:\n        n //= 2\n        pocet += 1\n    return pocet\n",
            'hint_sk': "Použi `while n > 0 and n % 2 == 0:` a v tele zmenšuj `n //= 2` a pripočítavaj počítadlo.",
            'hint_en': "Use `while n > 0 and n % 2 == 0: n //= 2; count += 1`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.MEDIUM,
            'xp_reward': 60,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex3_3,
        test_code="assert pocet_deleni(16) == 4",
        defaults={'input_data': 'pocet_deleni(16)', 'expected_output': '4', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex3_3,
        test_code="assert pocet_deleni(12) == 2",
        defaults={'input_data': 'pocet_deleni(12)', 'expected_output': '2', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex3_3,
        test_code="assert pocet_deleni(7) == 0",
        defaults={'input_data': 'pocet_deleni(7)', 'expected_output': '0', 'is_hidden': False}
    )

    # ------------------------------------------------------------------
    # MODUL 4: Funkcie a rekurzia
    # ------------------------------------------------------------------
    mod4, _ = Module.objects.update_or_create(
        order=4,
        defaults={
            'title_sk': '4. Funkcie a rekurzia',
            'title_en': '4. Functions & Recursion',
            'description_sk': 'Dekompozícia problému na funkcie, parametre, predvolené hodnoty a princíp rekurzie.',
            'description_en': 'Decomposing tasks into functions, parameters, default arguments, and recursion.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-code-square'
        }
    )

    lesson4_1, _ = Lesson.objects.update_or_create(
        module=mod4,
        order=1,
        defaults={
            'title_sk': 'Funkcie s predvolenými parametrami',
            'title_en': 'Functions with Default Arguments',
            'content_sk': (
                "### Predvolené hodnoty argumentov\n\n"
                "V definícii funkcie môžeme parametrom priradiť predvolenú hodnotu. "
                "Ak volajúci tento argument nezadá, použije sa predvolená hodnota:\n\n"
                "```python\n"
                "def pozdrav(meno, prefix='Ahoj'):\n"
                "    return f'{prefix}, {meno}!'\n"
                "```"
            ),
            'content_en': (
                "### Default Argument Values\n\n"
                "Functions can specify defaults for trailing parameters:\n\n"
                "```python\n"
                "def greet(name, prefix='Hello'):\n"
                "    return f'{prefix}, {name}!'\n"
                "```"
            ),
            'xp_reward': 30
        }
    )
    ex4_1, _ = Exercise.objects.update_or_create(
        lesson=lesson4_1,
        order=1,
        defaults={
            'title_sk': 'Výpočet ceny s DPH',
            'title_en': 'Calculate Price with VAT',
            'instructions_sk': (
                "Napíš funkciu `vypocitaj_dph(cena, sadzba=20)`, ktorá vráti celkovú cenu vrátane DPH zaokrúhlenú na 2 desatinné miesta. "
                "Predvolená sadzba DPH je **20 %**."
            ),
            'instructions_en': (
                "Write `vypocitaj_dph(cena, sadzba=20)` returning total price with VAT rounded to 2 decimals."
            ),
            'starter_code': "def vypocitaj_dph(cena, sadzba=20):\n    pass\n",
            'solution_code': "def vypocitaj_dph(cena, sadzba=20):\n    return round(cena * (1 + sadzba / 100), 2)\n",
            'hint_sk': "Použi vzorec `round(cena * (1 + sadzba / 100), 2)`.",
            'hint_en': "Use `round(cena * (1 + sadzba / 100), 2)`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 55,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex4_1,
        test_code="assert vypocitaj_dph(100) == 120.0",
        defaults={'input_data': 'vypocitaj_dph(100)', 'expected_output': '120.0', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex4_1,
        test_code="assert vypocitaj_dph(100, 10) == 110.0",
        defaults={'input_data': 'vypocitaj_dph(100, 10)', 'expected_output': '110.0', 'is_hidden': False}
    )

    lesson4_2, _ = Lesson.objects.update_or_create(
        module=mod4,
        order=2,
        defaults={
            'title_sk': 'Rekurzia a základný prípad',
            'title_en': 'Recursion and the Base Case',
            'content_sk': (
                "### Čo je to rekurzia?\n\n"
                "Rekurzia je situácia, keď funkcia vo svojom tele volá samu seba na menšom podprobléme. "
                "Každá rekurzívna funkcia **musí** mať:\n"
                "1. **Základný prípad (Base Case):** podmienku, pri ktorej sa rekurzia zastaví a vráti konkrétnu hodnotu.\n"
                "2. **Rekurzívny krok:** volanie funkcie s argumentom posunutým bližšie k základnému prípadu.\n\n"
                "```python\n"
                "def faktorial(n):\n"
                "    if n <= 1:\n"
                "        return 1\n"
                "    return n * faktorial(n - 1)\n"
                "```"
            ),
            'content_en': (
                "### Understanding Recursion\n\n"
                "Recursion occurs when a function calls itself on a smaller sub-problem. "
                "Every recursive function **must** have a base case and a recursive step."
            ),
            'xp_reward': 35
        }
    )

    ex4_2, _ = Exercise.objects.update_or_create(
        lesson=lesson4_2,
        order=1,
        defaults={
            'title_sk': 'Faktoriál čísla rekurziou',
            'title_en': 'Factorial via Recursion',
            'instructions_sk': (
                "Napíš **rekurzívnu** funkciu `faktorial(n)`, ktorá vráti faktoriál čísla `n`.\n\n"
                "Pravidlá:\n"
                "- Pre `n <= 1` vráti `1` (základný prípad)\n"
                "- Pre `n > 1` vráti `n * faktorial(n - 1)`"
            ),
            'instructions_en': (
                "Write a **recursive** function `faktorial(n)` returning the factorial of `n`.\n\n"
                "Rules:\n"
                "- For `n <= 1` return `1` (base case)\n"
                "- For `n > 1` return `n * faktorial(n - 1)`"
            ),
            'starter_code': "def faktorial(n):\n    # Základný prípad: ak n <= 1 vráť 1\n    # Rekurzia: n * faktorial(n - 1)\n    pass\n",
            'solution_code': "def faktorial(n):\n    if n <= 1:\n        return 1\n    return n * faktorial(n - 1)\n",
            'hint_sk': "Nezabudni ošetriť `if n <= 1: return 1`, inak by rekurzia bežala donekonečna.",
            'hint_en': "Ensure `if n <= 1: return 1` is handled to prevent infinite recursion.",
            'hint_cost_doros': 20,
            'difficulty': Exercise.Difficulty.MEDIUM,
            'xp_reward': 70,
            'doros_reward': 40
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex4_2,
        test_code="assert faktorial(0) == 1",
        defaults={'input_data': 'faktorial(0)', 'expected_output': '1', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex4_2,
        test_code="assert faktorial(5) == 120",
        defaults={'input_data': 'faktorial(5)', 'expected_output': '120', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex4_2,
        test_code="assert faktorial(6) == 720",
        defaults={'input_data': 'faktorial(6)', 'expected_output': '720', 'is_hidden': True}
    )

    lesson4_3, _ = Lesson.objects.update_or_create(
        module=mod4,
        order=3,
        defaults={
            'title_sk': 'Fibonacciho postupnosť rekurzívne',
            'title_en': 'Recursive Fibonacci Sequence',
            'content_sk': (
                "### Dvojitá rekurzia: Fibonacci\n\n"
                "Každý člen Fibonacciho postupnosti je súčtom dvoch predchádzajúcich: `F(n) = F(n-1) + F(n-2)`."
            ),
            'content_en': (
                "### Double Recursion: Fibonacci\n\n"
                "Each term in the Fibonacci sequence equals the sum of the preceding two: `F(n) = F(n-1) + F(n-2)`."
            ),
            'xp_reward': 35
        }
    )
    ex4_3, _ = Exercise.objects.update_or_create(
        lesson=lesson4_3,
        order=1,
        defaults={
            'title_sk': 'Člen Fibonacciho postupnosti',
            'title_en': 'Fibonacci Sequence Term',
            'instructions_sk': (
                "Napíš funkciu `fibonacci(n)`, ktorá vráti n-tý člen postupnosti:\n"
                "- `n <= 0` vráti `0`\n"
                "- `n == 1` vráti `1`\n"
                "- inak vráti `fibonacci(n - 1) + fibonacci(n - 2)`"
            ),
            'instructions_en': (
                "Write `fibonacci(n)`: if n <= 0 return 0, n == 1 return 1, else sum of previous two."
            ),
            'starter_code': "def fibonacci(n):\n    pass\n",
            'solution_code': "def fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    return fibonacci(n - 1) + fibonacci(n - 2)\n",
            'hint_sk': "Ošetri dva základné prípady: `n <= 0` vráti 0 a `n == 1` vráti 1.",
            'hint_en': "Handle two base cases: 0 and 1.",
            'hint_cost_doros': 20,
            'difficulty': Exercise.Difficulty.MEDIUM,
            'xp_reward': 70,
            'doros_reward': 40
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex4_3,
        test_code="assert fibonacci(0) == 0",
        defaults={'input_data': 'fibonacci(0)', 'expected_output': '0', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex4_3,
        test_code="assert fibonacci(1) == 1",
        defaults={'input_data': 'fibonacci(1)', 'expected_output': '1', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex4_3,
        test_code="assert fibonacci(6) == 8",
        defaults={'input_data': 'fibonacci(6)', 'expected_output': '8', 'is_hidden': False}
    )

    # ------------------------------------------------------------------
    # MODUL 5: Zoznamy a slovníky
    # ------------------------------------------------------------------
    mod5, _ = Module.objects.update_or_create(
        order=5,
        defaults={
            'title_sk': '5. Zoznamy a slovníky',
            'title_en': '5. Lists & Dictionaries',
            'description_sk': 'Dátové štruktúry: zoznamy (list), n-tice (tuple), množiny (set) a kľúč-hodnota páry v slovníkoch (dict).',
            'description_en': 'Data structures: lists, tuples, sets, and key-value mapping with dictionaries.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': False,
            'icon_name': 'bi-collection-fill'
        }
    )

    lesson5_1, _ = Lesson.objects.update_or_create(
        module=mod5,
        order=1,
        defaults={
            'title_sk': 'Práca so zoznamami a filtrovanie dát',
            'title_en': 'List Manipulation & Data Filtering',
            'content_sk': (
                "### Zoznam (list) v Pythone\n\n"
                "Zoznam je usporiadaná, meniteľná kolekcia hodnôt indexovaná od `0`:\n\n"
                "```python\n"
                "ziaci = ['Anna', 'Boris', 'Cecilia']\n"
                "print(ziaci[0])       # 'Anna'\n"
                "ziaci.append('David') # pridanie na koniec\n"
                "dlzka = len(ziaci)    # 4\n"
                "```\n\n"
                "Zoznamy môžeme prechádzať cyklom `for prvok in zoznam:` a aplikovať podmienky na výber prvkov."
            ),
            'content_en': (
                "### Python Lists\n\n"
                "A list is an ordered, mutable sequence indexed from `0`:\n\n"
                "```python\n"
                "students = ['Anna', 'Boris', 'Cecilia']\n"
                "print(students[0])       # 'Anna'\n"
                "students.append('David') # append to end\n"
                "size = len(students)     # 4\n"
                "```"
            ),
            'xp_reward': 35
        }
    )

    ex5_1, _ = Exercise.objects.update_or_create(
        lesson=lesson5_1,
        order=1,
        defaults={
            'title_sk': 'Počet úspešných študentov',
            'title_en': 'Count Passing Students',
            'instructions_sk': (
                "Napíš funkciu `uspesni_studenti(body_zoznam)`, ktorá prijme zoznam bodov študentov z testu "
                "a vráti **počet** študentov, ktorí získali **aspoň 50 bodov** (t. j. `>= 50`)."
            ),
            'instructions_en': (
                "Write a function `uspesni_studenti(body_zoznam)` taking a list of test scores "
                "and returning the **count** of students who scored **at least 50 points** (`>= 50`)."
            ),
            'starter_code': "def uspesni_studenti(body_zoznam):\n    # Prejdi zoznam a spočítaj čísla >= 50\n    pass\n",
            'solution_code': "def uspesni_studenti(body_zoznam):\n    return sum(1 for b in body_zoznam if b >= 50)\n",
            'hint_sk': "Vytvor počítadlo `pocet = 0`, prejdi zoznam cez `for b in body_zoznam:` a pri `b >= 50` pripočítaj 1.",
            'hint_en': "Use a counter variable and loop through `body_zoznam` checking `>= 50`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 60,
            'doros_reward': 35
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex5_1,
        test_code="assert uspesni_studenti([20, 50, 85, 49, 100]) == 3",
        defaults={'input_data': 'uspesni_studenti([20, 50, 85, 49, 100])', 'expected_output': '3', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex5_1,
        test_code="assert uspesni_studenti([10, 20, 30]) == 0",
        defaults={'input_data': 'uspesni_studenti([10, 20, 30])', 'expected_output': '0', 'is_hidden': False}
    )

    lesson5_2, _ = Lesson.objects.update_or_create(
        module=mod5,
        order=2,
        defaults={
            'title_sk': 'Agregácia a rozptyl v zozname',
            'title_en': 'List Aggregation & Variance',
            'content_sk': (
                "### Vstavané funkcie pre zoznamy\n\n"
                "Python ponúka rýchle funkcie `max()`, `min()` a `sum()` pre numerické zoznamy."
            ),
            'content_en': (
                "### Built-in List Aggregations\n\n"
                "Python includes `max()`, `min()` and `sum()` for numeric sequences."
            ),
            'xp_reward': 35
        }
    )
    ex5_2, _ = Exercise.objects.update_or_create(
        lesson=lesson5_2,
        order=1,
        defaults={
            'title_sk': 'Rozpätie bodov v triede',
            'title_en': 'Score Range in Class',
            'instructions_sk': (
                "Napíš funkciu `rozpatie_bodov(zoznam)`, ktorá vráti rozdiel medzi najvyšším a najnižším číslom v zozname (`max - min`). "
                "Ak je zoznam prázdny, vráti `0`."
            ),
            'instructions_en': (
                "Write `rozpatie_bodov(zoznam)` returning difference between max and min. Return 0 if empty."
            ),
            'starter_code': "def rozpatie_bodov(zoznam):\n    pass\n",
            'solution_code': "def rozpatie_bodov(zoznam):\n    if not zoznam:\n        return 0\n    return max(zoznam) - min(zoznam)\n",
            'hint_sk': "Použi podmienku `if not zoznam: return 0` a potom `max(zoznam) - min(zoznam)`.",
            'hint_en': "Check if list is empty, then return max - min.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 55,
            'doros_reward': 30
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex5_2,
        test_code="assert rozpatie_bodov([20, 85, 40, 95]) == 75",
        defaults={'input_data': 'rozpatie_bodov([20, 85, 40, 95])', 'expected_output': '75', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex5_2,
        test_code="assert rozpatie_bodov([50]) == 0",
        defaults={'input_data': 'rozpatie_bodov([50])', 'expected_output': '0', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex5_2,
        test_code="assert rozpatie_bodov([]) == 0",
        defaults={'input_data': 'rozpatie_bodov([])', 'expected_output': '0', 'is_hidden': False}
    )

    lesson5_3, _ = Lesson.objects.update_or_create(
        module=mod5,
        order=3,
        defaults={
            'title_sk': 'Slovníky (dict) a vyhľadávanie hodnôt',
            'title_en': 'Dictionaries & Key-Value Lookup',
            'content_sk': (
                "### Slovník (dict) v Pythone\n\n"
                "Slovník mapuje unikátne kľúče na hodnoty: `farby = {'cervena': 'red', 'modra': 'blue'}`. "
                "Metóda `slovnik.get(kluc, default)` vráti predvolenú hodnotu, ak kľúč neexistuje."
            ),
            'content_en': (
                "### Dictionaries in Python\n\n"
                "Dictionaries map unique keys to values. `dict.get(key, default)` gracefully handles missing keys."
            ),
            'xp_reward': 35
        }
    )
    ex5_3, _ = Exercise.objects.update_or_create(
        lesson=lesson5_3,
        order=1,
        defaults={
            'title_sk': 'Prekladač programátorských farieb',
            'title_en': 'Color Name Translator',
            'instructions_sk': (
                "Napíš funkciu `preloz_farbu(farba_sk)`, ktorá pomocou slovníka preloží:\n"
                "- `'cervena'` -> `'red'`\n"
                "- `'modra'` -> `'blue'`\n"
                "- `'zelena'` -> `'green'`\n"
                "- pre akúkoľvek inú farbu vráti `'neznamy'`."
            ),
            'instructions_en': (
                "Write `preloz_farbu(farba_sk)` translating slovak color names to english via dict. Return 'neznamy' otherwise."
            ),
            'starter_code': "def preloz_farbu(farba_sk):\n    pass\n",
            'solution_code': "def preloz_farbu(farba_sk):\n    slovnik = {'cervena': 'red', 'modra': 'blue', 'zelena': 'green'}\n    return slovnik.get(farba_sk, 'neznamy')\n",
            'hint_sk': "Použi metódu `slovnik.get(farba_sk, 'neznamy')`.",
            'hint_en': "Use `dict.get(key, 'neznamy')`.",
            'hint_cost_doros': 15,
            'difficulty': Exercise.Difficulty.EASY,
            'xp_reward': 55,
            'doros_reward': 30
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex5_3,
        test_code="assert preloz_farbu('cervena') == 'red'",
        defaults={'input_data': "preloz_farbu('cervena')", 'expected_output': 'red', 'is_hidden': False}
    )
    TestCase.objects.update_or_create(
        exercise=ex5_3,
        test_code="assert preloz_farbu('fialova') == 'neznamy'",
        defaults={'input_data': "preloz_farbu('fialova')", 'expected_output': 'neznamy', 'is_hidden': False}
    )

    # ------------------------------------------------------------------
    # MODUL 6: Objektovo-orientované programovanie (OOP) - PRO/EDU
    # ------------------------------------------------------------------
    mod6, _ = Module.objects.update_or_create(
        order=6,
        defaults={
            'title_sk': '6. Objektovo-orientované programovanie (OOP)',
            'title_en': '6. Object-Oriented Programming (OOP)',
            'description_sk': 'Pokročilý modul pre PRO/EDU: triedy, objekty, konštruktor __init__, atribúty a dedičnosť.',
            'description_en': 'Advanced PRO/EDU module: classes, objects, __init__ constructor, attributes and inheritance.',
            'programming_language': Module.ProgrammingLanguage.PYTHON,
            'is_pro_only': True,
            'icon_name': 'bi-boxes'
        }
    )

    lesson6_1, _ = Lesson.objects.update_or_create(
        module=mod6,
        order=1,
        defaults={
            'title_sk': 'Triedy, inštancie a metóda __init__',
            'title_en': 'Classes, Instances and the __init__ Method',
            'content_sk': (
                "### Základy OOP v Pythone\n\n"
                "Trieda (`class`) predstavuje predpis (šablónu) a objekt je konkrétna inštancia vytvorená podľa tejto šablóny. "
                "Metóda `__init__` je konštruktor, ktorý sa zavolá automaticky pri vytvorení objektu:\n\n"
                "```python\n"
                "class Hrac:\n"
                "    def __init__(self, meno, doros=0):\n"
                "        self.meno = meno\n"
                "        self.doros = doros\n\n"
                "    def pridaj_doros(self, pocet):\n"
                "        self.doros += pocet\n"
                "        return self.doros\n"
                "```\n\n"
                "Parameter `self` odkazuje na konkrétnu inštanciu triedy, na ktorej metódu voláme."
            ),
            'content_en': (
                "### OOP Foundations in Python\n\n"
                "A `class` is a blueprint, and an object is an instance created from that blueprint. "
                "The `__init__` method is the constructor executed upon instantiation:\n\n"
                "```python\n"
                "class Player:\n"
                "    def __init__(self, name, doros=0):\n"
                "        self.name = name\n"
                "        self.doros = doros\n\n"
                "    def add_doros(self, amount):\n"
                "        self.doros += amount\n"
                "        return self.doros\n"
                "```"
            ),
            'xp_reward': 45
        }
    )

    ex6_1, _ = Exercise.objects.update_or_create(
        lesson=lesson6_1,
        order=1,
        defaults={
            'title_sk': 'Trieda Penazenka (Wallet)',
            'title_en': 'Wallet Class',
            'instructions_sk': (
                "Vytvor triedu `Penazenka` s týmito vlastnosťami:\n"
                "- Konštruktor `__init__(self, majitel, zostatok=0)`, ktorý uloží atribúty `majitel` a `zostatok`\n"
                "- Metódu `vloz(self, suma)`, ktorá pripočíta `suma` k `zostatok` a vráti nový zostatok\n"
                "- Metódu `vyber(self, suma)`, ktorá ak `suma <= zostatok`, odpočíta sumu a vráti `True`, inak vráti `False` (bez zmeny zostatku)"
            ),
            'instructions_en': (
                "Create a class `Penazenka` with:\n"
                "- `__init__(self, majitel, zostatok=0)` setting `majitel` and `zostatok`\n"
                "- `vloz(self, suma)` adding `suma` to `zostatok` and returning the new balance\n"
                "- `vyber(self, suma)`: if `suma <= zostatok`, subtract and return `True`, otherwise return `False`"
            ),
            'starter_code': (
                "class Penazenka:\n"
                "    def __init__(self, majitel, zostatok=0):\n"
                "        pass\n\n"
                "    def vloz(self, suma):\n"
                "        pass\n\n"
                "    def vyber(self, suma):\n"
                "        pass\n"
            ),
            'solution_code': (
                "class Penazenka:\n"
                "    def __init__(self, majitel, zostatok=0):\n"
                "        self.majitel = majitel\n"
                "        self.zostatok = zostatok\n\n"
                "    def vloz(self, suma):\n"
                "        self.zostatok += suma\n"
                "        return self.zostatok\n\n"
                "    def vyber(self, suma):\n"
                "        if suma <= self.zostatok:\n"
                "            self.zostatok -= suma\n"
                "            return True\n"
                "        return False\n"
            ),
            'hint_sk': "V `__init__` nastav `self.majitel = majitel` a `self.zostatok = zostatok`.",
            'hint_en': "In `__init__`, set `self.majitel = majitel` and `self.zostatok = zostatok`.",
            'hint_cost_doros': 25,
            'difficulty': Exercise.Difficulty.HARD,
            'xp_reward': 90,
            'doros_reward': 50
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex6_1,
        test_code=(
            "p = Penazenka('Juraj', 100)\n"
            "assert p.majitel == 'Juraj'\n"
            "assert p.zostatok == 100\n"
            "assert p.vloz(50) == 150\n"
            "assert p.vyber(80) == True\n"
            "assert p.zostatok == 70\n"
            "assert p.vyber(100) == False\n"
            "assert p.zostatok == 70"
        ),
        defaults={'input_data': 'Penazenka("Juraj", 100) operácie', 'expected_output': 'True', 'is_hidden': False}
    )

    lesson6_2, _ = Lesson.objects.update_or_create(
        module=mod6,
        order=2,
        defaults={
            'title_sk': 'Dedičnosť tried a rozširovanie správania',
            'title_en': 'Class Inheritance & Extending Behavior',
            'content_sk': (
                "### Dedičnosť (Inheritance)\n\n"
                "Dedičnosť umožňuje novej triede prevziať všetky metódy a vlastnosti existujúcej triedy:\n\n"
                "```python\n"
                "class SporiaciUcet(Penazenka):\n"
                "    def __init__(self, majitel, zostatok=0, urok=5):\n"
                "        super().__init__(majitel, zostatok)\n"
                "        self.urok = urok\n"
                "```"
            ),
            'content_en': (
                "### Class Inheritance\n\n"
                "Inheritance lets a derived class inherit and extend methods and attributes from a base class."
            ),
            'xp_reward': 50
        }
    )
    ex6_2, _ = Exercise.objects.update_or_create(
        lesson=lesson6_2,
        order=1,
        defaults={
            'title_sk': 'Trieda SporiaciUcet',
            'title_en': 'SavingsAccount Class',
            'instructions_sk': (
                "Vytvor triedu `SporiaciUcet`, ktorá **dedí z triedy Penazenka**:\n"
                "- Konštruktor `__init__(self, majitel, zostatok=0, urok=5)` zavolá `super().__init__(majitel, zostatok)` a uloží `self.urok = urok`\n"
                "- Metóda `pripis_urok(self)` pripočíta k `self.zostatok` úrok (`self.zostatok * (self.urok / 100)`) a vráti nový zostatok"
            ),
            'instructions_en': (
                "Create `SporiaciUcet` inheriting from `Penazenka` with `pripis_urok` adding interest."
            ),
            'starter_code': (
                "class SporiaciUcet(Penazenka):\n"
                "    def __init__(self, majitel, zostatok=0, urok=5):\n"
                "        pass\n\n"
                "    def pripis_urok(self):\n"
                "        pass\n"
            ),
            'solution_code': (
                "class SporiaciUcet(Penazenka):\n"
                "    def __init__(self, majitel, zostatok=0, urok=5):\n"
                "        super().__init__(majitel, zostatok)\n"
                "        self.urok = urok\n\n"
                "    def pripis_urok(self):\n"
                "        urok_suma = self.zostatok * (self.urok / 100)\n"
                "        self.zostatok += urok_suma\n"
                "        return self.zostatok\n"
            ),
            'hint_sk': "Použi `super().__init__(majitel, zostatok)` na inicializáciu rodičovskej triedy.",
            'hint_en': "Use `super().__init__(majitel, zostatok)`.",
            'hint_cost_doros': 25,
            'difficulty': Exercise.Difficulty.HARD,
            'xp_reward': 95,
            'doros_reward': 55
        }
    )
    TestCase.objects.update_or_create(
        exercise=ex6_2,
        test_code=(
            "s = SporiaciUcet('Juraj', 200, 10)\n"
            "assert s.majitel == 'Juraj'\n"
            "assert s.zostatok == 200\n"
            "assert s.pripis_urok() == 220.0\n"
            "assert s.vyber(100) == True\n"
            "assert s.zostatok == 120.0"
        ),
        defaults={'input_data': 'SporiaciUcet("Juraj", 200, 10) operácie', 'expected_output': 'True', 'is_hidden': False}
    )

    # ==================================================================
    # 5. UČITEĽSKÝ OBCHOD S ODMENAMI A SKLADOVÝM HOSPODÁRSTVOM
    # ==================================================================
    RewardItem.objects.update_or_create(
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

    RewardItem.objects.update_or_create(
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

    RewardItem.objects.update_or_create(
        title_sk='Nápoveda od učiteľa počas písomky',
        defaults={
            'title_en': 'Teacher Hint During Test',
            'description_sk': 'Učiteľ ti počas praktického testu pomôže odhaliť 1 chybu v kóde (Obnovuje sa denne).',
            'description_en': 'The teacher will help you debug 1 issue during a test (Restocks daily).',
            'cost_doros': 180,
            'icon_name': 'bi-lightbulb-fill',
            'max_stock': 2,
            'current_stock': 2,
            'restock_period': RewardItem.RestockPeriod.DAILY,
            'limit_per_student_per_period': 1,
            'created_by': teacher
        }
    )

    # ==================================================================
    # 6. OSOBNÉ QUESTY (DAILY, WEEKLY, MONTHLY)
    # ==================================================================
    Quest.objects.update_or_create(
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
    Quest.objects.update_or_create(
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
    Quest.objects.update_or_create(
        title_sk='Mesačný majster: Vyrieš 5 úloh na 1. pokus',
        defaults={
            'title_en': 'Monthly Master: Solve 5 Tasks on 1st Try',
            'period': Quest.QuestPeriod.MONTHLY,
            'metric_type': Quest.MetricType.FIRST_TRY_SOLVES,
            'target_value': 5,
            'reward_doros': 400,
            'reward_xp': 200
        }
    )

    # ==================================================================
    # 7. KOLEKTÍVNY TRIEDNY QUEST PRE IV.C
    # ==================================================================
    ClassQuest.objects.update_or_create(
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

    # ==================================================================
    # 8. AKTÍVNY COIN DROP
    # ==================================================================
    CoinDrop.objects.update_or_create(
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

    # 9. Úvodná transakcia v peňaženke
    if not DorosTransaction.objects.filter(student=student).exists():
        DorosTransaction.objects.create(
            student=student,
            amount=350,
            reason_sk='Štartovací bonus a odmeny za doterajšiu aktivitu',
            reason_en='Starter bonus and activity rewards'
        )

    print("✅ Databáza Codoro bola úspešne naplnená všetkými 6 modulmi, odznakmi a odmenami!")
    print("👉 Prihlásenie UČITEĽ:  meno: ucitel  | heslo: heslo123")
    print("👉 Prihlásenie ŠTUDENT: meno: student | heslo: heslo123")


if __name__ == '__main__':
    run_seed()