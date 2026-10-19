"""
MODUL 1: Úvod do algoritmizácie, premenné a základné dátové typy
Odhadovaný rozsah: 10 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 1,
    'title_sk': 'Úvod do algoritmizácie, premenné a základné dátové typy',
    'title_en': 'Introduction to Algoritmization, Variables & Data Types',
    'description_sk': 'Osvoj si základy syntaxe Pythonu, formátovaný výstup pomocou print(), deklaráciu premenných podľa PEP 8, základné dátové typy (int, float, str, bool) a pretypovanie.',
    'description_en': 'Master the fundamentals of Python syntax, formatted console output with print(), variable declarations following PEP 8, primitive data types (int, float, str, bool), and type casting.',
    'programming_language': 'python',
    'estimated_hours': 10,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'terminal',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Prvý program, funkcia print() a formátovanie výstupu',
            'title_en': 'First Program, print() Function & Output Formatting',
            'summary_sk': 'Syntax funkcie print(), parametre sep a end, jednoriadkové a viacriadkové komentáre.',
            'summary_en': 'Syntax of the print() function, sep and end arguments, single-line and multi-line comments.',
            'estimated_minutes': 45,
            'xp_reward': 25,
            'is_published': True,
            'content_sk': """### 1.1 Prvý program v Pythone

Vítaj v Codoro! Python patrí medzi celosvetovo najpopulárnejšie a najčitateľnejšie programovacie jazyky. Vznikol v roku 1991 pod vedením Guida van Rossuma s filozofiou: **"Čitateľnosť kódu je prvoradá"**.

#### Funkcia `print()`
Základným nástrojom na výpis textu a hodnôt do konzoly je vstavaná funkcia `print()`.

```python
print("Ahoj, svet programovania!")
print(42)
print("Codoro", "Python", 2027)
```

#### Parametre `sep` a `end`
Funkcia `print()` prijíma voliteľné pomenované parametre:
1. `sep` (separator) – reťazec vkladaný medzi jednotlivé argumenty (predvolená hodnota je medzera `' '`).
2. `end` – reťazec pripojený na koniec výpisu (predvolená hodnota je nový riadok `'\\n'`).

```python
# Úprava oddeľovača
print("2026", "10", "20", sep="-")  # Vypíše: 2026-10-20

# Zamedzenie odriadkovaniu
print("Načítavam", end="...")
print("Hotovo!")  # Vypíše: Načítavam...Hotovo!
```

#### Komentáre v kóde
Komentáre slúžia pre programátora na vysvetlenie logiky a interpret Pythonu ich úplne ignoruje:
- Jednoriadkový komentár začína znakom `#`.
- Viacriadkový komentár / docstring sa ohraničuje trojitými úvodzovkami `\"\"\"`.
""",
            'content_en': """### 1.1 First Program in Python

Welcome to Codoro! Python is one of the most readable and powerful programming languages in the world, created with the philosophy that **code readability counts**.

#### The `print()` Function
The primary built-in function for outputting data to the terminal is `print()`.

```python
print("Hello, world of programming!")
print(42)
print("Codoro", "Python", 2027)
```

#### The `sep` and `end` Keyword Arguments
1. `sep` (separator) defines the string inserted between arguments (default is `' '`).
2. `end` defines what is printed at the very end of the output (default is newline `'\\n'`).

```python
# Custom separator
print("2026", "10", "20", sep="-")  # Prints: 2026-10-20

# Continuous output
print("Loading", end="...")
print("Done!")  # Prints: Loading...Done!
```
""",
            'quizzes': [
                {
                    'question_sk': 'Aká je predvolená hodnota parametra `sep` vo funkcii `print()`?',
                    'question_en': 'What is the default value of the `sep` parameter in the `print()` function?',
                    'option_a_sk': 'Nový riadok (\\n)', 'option_a_en': 'Newline (\\n)',
                    'option_b_sk': 'Medzera (" ")', 'option_b_en': 'Space (" ")',
                    'option_c_sk': 'Čiarka (",")', 'option_c_en': 'Comma (",")',
                    'option_d_sk': 'Žiadny znak ("")', 'option_d_en': 'Empty string ("")',
                    'correct_option': 'B',
                    'explanation_sk': 'Funkcia print() štandardne oddeľuje viacero argumentov jednou medzerou.',
                    'explanation_en': 'print() separates multiple positional arguments with a single space by default.',
                },
                {
                    'question_sk': 'Ktorý znak sa v Pythone používa na jednoriadkový komentár?',
                    'question_en': 'Which symbol is used in Python for a single-line comment?',
                    'option_a_sk': '//', 'option_a_en': '//',
                    'option_b_sk': '/*', 'option_b_en': '/*',
                    'option_c_sk': '#', 'option_c_en': '#',
                    'option_d_sk': '--', 'option_d_en': '--',
                    'correct_option': 'C',
                    'explanation_sk': 'V Pythone označuje jednoriadkový komentár mriežka (#).',
                    'explanation_en': 'In Python, the hash character (#) marks a single-line comment.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Formátovaný výpis dátumu',
                    'title_en': 'Formatted Date Output',
                    'instructions_sk': 'Napíš funkciu `formatuj_datum(den, mesiac, rok)`, ktorá vráti reťazec dátumu v tvare `DD.MM.YYYY` s použitím pomlčky alebo bodky. Využi reťazcové formátovanie.',
                    'instructions_en': 'Write a function `formatuj_datum(den, mesiac, rok)` returning a date string in `DD.MM.YYYY` format.',
                    'starter_code': 'def formatuj_datum(den, mesiac, rok):\n    # Vráť naformátovaný dátum ako reťazec\n    pass\n',
                    'solution_code': 'def formatuj_datum(den, mesiac, rok):\n    return f"{den:02d}.{mesiac:02d}.{rok}"\n',
                    'explanation_sk': 'Použili sme f-string s formátovaním dvojciferného čísla doplneného nulou `:02d`.',
                    'explanation_en': 'We used an f-string with zero-padded two-digit formatting `:02d`.',
                    'hint_sk': 'Použi f-string v tvare f"{den:02d}.{mesiac:02d}.{rok}".',
                    'hint_en': 'Use an f-string formatted like f"{den:02d}.{mesiac:02d}.{rok}".',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'formatuj_datum(5, 4, 2027)', 'expected_output': '05.04.2027', 'test_code': 'assert formatuj_datum(5, 4, 2027) == "05.04.2027"', 'is_hidden': False},
                        {'input_data': 'formatuj_datum(24, 12, 2026)', 'expected_output': '24.12.2026', 'test_code': 'assert formatuj_datum(24, 12, 2026) == "24.12.2026"', 'is_hidden': False},
                        {'input_data': 'formatuj_datum(1, 1, 2030)', 'expected_output': '01.01.2030', 'test_code': 'assert formatuj_datum(1, 1, 2030) == "01.01.2030"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Premenné, pravidlá pomenovania PEP 8 a operátor priradenia',
            'title_en': 'Variables, PEP 8 Naming Conventions & Assignment',
            'summary_sk': 'Priraďovací operátor =, pamäťový model, konvencia snake_case a kľúčové slová.',
            'summary_en': 'Assignment operator =, Python memory references, snake_case convention, and reserved keywords.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 1.2 Premenné a konvencie PEP 8

Premenná v Pythone funguje ako **menovka (odkaz)** ukazujúca na konkrétny objekt v pamäti RAM.

#### Priraďovací operátor `=`
```python
meno_hraca = "Juraj"
skore = 150
skore = skore + 50  # Nová hodnota 200
```

#### Pravidlá pomenovania podľa oficiálneho štandardu PEP 8:
1. Názvy premenných a funkcií píšeme malými písmenami so slovami oddelenými podčiarkovníkom: `snake_case` (napr. `pocet_bodov`, `aktualny_streak`).
2. Názov nesmie začínať číslicou a nesmie obsahovať medzery ani špeciálne znaky (`$`, `@`, `-`).
3. Nesmie byť zhodný s **kľúčovými slovami** jazyka (`def`, `class`, `if`, `return`, `import`, atď.).
4. Konštanty píšeme veľkými písmenami: `MAX_LEVEL = 100`.

#### Skrátené operátory priradenia (Augmented Assignment)
- `x += 5` je ekvivalent `x = x + 5`
- `x -= 2` je ekvivalent `x = x - 2`
- `x *= 3` je ekvivalent `x = x * 3`
""",
            'content_en': """### 1.2 Variables and PEP 8 Conventions

In Python, a variable is a label or pointer referencing an object in memory.

#### Assignment Operator `=`
```python
player_name = "Juraj"
score = 150
score += 50  # Incremented to 200
```

#### PEP 8 Style Guide Rules:
1. Use `snake_case` for variables and functions (e.g., `user_count`, `active_streak`).
2. Cannot start with a digit, nor contain spaces or symbols.
3. Cannot be a reserved Python keyword (`def`, `return`, `for`, etc.).
4. Constants are written in all uppercase: `MAX_DOROS = 5000`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý z nasledujúcich názvov premenných je v súlade so štandardom PEP 8 pre Python?',
                    'question_en': 'Which of the following variable names complies with the PEP 8 style guide for Python?',
                    'option_a_sk': 'studentScore', 'option_a_en': 'studentScore',
                    'option_b_sk': 'student_score', 'option_b_en': 'student_score',
                    'option_c_sk': 'Student-Score', 'option_c_en': 'Student-Score',
                    'option_d_sk': '1_student_score', 'option_d_en': '1_student_score',
                    'correct_option': 'B',
                    'explanation_sk': 'Štandard PEP 8 pre bežné premenné vyžaduje štýl snake_case (malé písmená s podčiarkovníkmi).',
                    'explanation_en': 'PEP 8 specifies snake_case naming for variables and functions.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Kalkulačka hernej peňaženky',
                    'title_en': 'Game Wallet Balance Calculator',
                    'instructions_sk': 'Napíš funkciu `spocitaj_penazenku(zaklad, prijate, minutie)`, ktorá vezme počiatočný zostatok, pripočíta prijaté mince a odpočíta minuté. Výsledný zostatok vráť ako číslo.',
                    'instructions_en': 'Write a function `spocitaj_penazenku(zaklad, prijate, minutie)` that adds received coins and subtracts spent ones.',
                    'starter_code': 'def spocitaj_penazenku(zaklad, prijate, minutie):\n    pass\n',
                    'solution_code': 'def spocitaj_penazenku(zaklad, prijate, minutie):\n    return zaklad + prijate - minutie\n',
                    'explanation_sk': 'Základná aritmetická operácia sčítania a odčítania.',
                    'explanation_en': 'Simple addition and subtraction of integer parameters.',
                    'hint_sk': 'Použi vzorec zaklad + prijate - minutie a vráť hodnotu cez return.',
                    'hint_en': 'Use zaklad + prijate - minutie and return the value.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'spocitaj_penazenku(100, 50, 30)', 'expected_output': '120', 'test_code': 'assert spocitaj_penazenku(100, 50, 30) == 120', 'is_hidden': False},
                        {'input_data': 'spocitaj_penazenku(0, 80, 80)', 'expected_output': '0', 'test_code': 'assert spocitaj_penazenku(0, 80, 80) == 0', 'is_hidden': False},
                        {'input_data': 'spocitaj_penazenku(500, 250, 150)', 'expected_output': '600', 'test_code': 'assert spocitaj_penazenku(500, 250, 150) == 600', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Základné dátové typy a funkcia type()',
            'title_en': 'Primitive Data Types & the type() Function',
            'summary_sk': 'Celé čísla (int), desatinné čísla (float), reťazce (str), pravdivostné hodnoty (bool) a zistenie typu.',
            'summary_en': 'Integers (int), floating-point numbers (float), strings (str), booleans (bool), and dynamic type inspection.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 1.3 Základné dátové typy v Pythone

Každá hodnota v Pythone má priradený dátový typ, ktorý určuje, aké operácie s ňou možno vykonávať.

| Dátový typ | Popis | Príklad |
|---|---|---|
| `int` | Celé číslo ľubovoľnej veľkosti | `42`, `-7`, `1000000` |
| `float` | Desatinné číslo s plávajúcou rádovou čiarkou | `3.14159`, `-0.5`, `2.0` |
| `str` | Textový reťazec (uzatvorený v `'` alebo `"`) | `'Codoro'`, `"Python"` |
| `bool` | Logická pravdivostná hodnota | `True`, `False` |

#### Funkcia `type()`
Pomocou vstavanej funkcie `type()` dokážeme počas behu programu overiť dátový typ objektu:

```python
vek = 18
teplota = 36.6
autor = "Codo"
je_aktivny = True

print(type(vek))         # <class 'int'>
print(type(teplota))     # <class 'float'>
print(type(autor))       # <class 'str'>
print(type(je_aktivny))  # <class 'bool'>
```
""",
            'content_en': """### 1.3 Primitive Data Types in Python

Every value has a specific type defining memory layout and applicable operations.

| Type | Description | Example |
|---|---|---|
| `int` | Arbitrary precision integer | `42`, `-10` |
| `float` | Floating-point real number | `3.14`, `-0.25` |
| `str` | Unicode text string | `'Codoro'` |
| `bool` | Boolean truth value | `True`, `False` |

#### Checking Types with `type()`
```python
x = 100
print(type(x))  # <class 'int'>
```
""",
            'quizzes': [
                {
                    'question_sk': 'Aký dátový typ vráti výraz `type(3.0)`?',
                    'question_en': 'What data type does the expression `type(3.0)` evaluate to?',
                    'option_a_sk': 'int', 'option_a_en': 'int',
                    'option_b_sk': 'float', 'option_b_en': 'float',
                    'option_c_sk': 'number', 'option_c_en': 'number',
                    'option_d_sk': 'decimal', 'option_d_en': 'decimal',
                    'correct_option': 'B',
                    'explanation_sk': 'Číslo s desatinnou bodkou je v Pythone typu float.',
                    'explanation_en': 'Any number containing a decimal point is represented as a float in Python.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Identifikácia a prepočet typu',
                    'title_en': 'Type Checking & Calculations',
                    'instructions_sk': 'Napíš funkciu `popis_hodnoty(hodnota)`, ktorá vráti reťazec v tvare `"Typ: <meno_typu>, Hodnota: <hodnota>"`. Napríklad pre `42` vráti `"Typ: int, Hodnota: 42"`.',
                    'instructions_en': 'Write a function `popis_hodnoty(hodnota)` returning `"Typ: <type_name>, Hodnota: <value>"`.',
                    'starter_code': 'def popis_hodnoty(hodnota):\n    pass\n',
                    'solution_code': 'def popis_hodnoty(hodnota):\n    return f"Typ: {type(hodnota).__name__}, Hodnota: {hodnota}"\n',
                    'explanation_sk': 'Atribút `__name__` na type vráti čistý názov typu ako reťazec (`int`, `str`, `float`).',
                    'explanation_en': 'Accessing `type(val).__name__` provides a clean type name string.',
                    'hint_sk': 'Použi type(hodnota).__name__ vo vnútri f-stringu.',
                    'hint_en': 'Use type(hodnota).__name__ inside an f-string.',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'popis_hodnoty(42)', 'expected_output': 'Typ: int, Hodnota: 42', 'test_code': 'assert popis_hodnoty(42) == "Typ: int, Hodnota: 42"', 'is_hidden': False},
                        {'input_data': 'popis_hodnoty(3.14)', 'expected_output': 'Typ: float, Hodnota: 3.14', 'test_code': 'assert popis_hodnoty(3.14) == "Typ: float, Hodnota: 3.14"', 'is_hidden': False},
                        {'input_data': 'popis_hodnoty("Codo")', 'expected_output': 'Typ: str, Hodnota: Codo', 'test_code': 'assert popis_hodnoty("Codo") == "Typ: str, Hodnota: Codo"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Pretypovanie (Type Casting) a konverzia hodnôt',
            'title_en': 'Type Casting & Value Conversion',
            'summary_sk': 'Explicitná konverzia int(), float(), str(), bool() a ošetrenie chýb.',
            'summary_en': 'Explicit type casting using int(), float(), str(), bool(), and error prevention.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 1.4 Pretypovanie (Type Casting)

Často potrebujeme previesť hodnotu z jedného dátového typu na iný (napríklad text zadaný používateľom `"45"` previesť na číslo `45`). Tomuto procesu hovoríme **explicitné pretypovanie**.

#### Konverzné funkcie:
- `int("123")` -> `123` (prevedie reťazec alebo float na celé číslo, desatinnú časť odreže!)
- `float("3.14")` -> `3.14`
- `str(100)` -> `'100'`
- `bool(1)` -> `True`, `bool(0)` -> `False`

```python
vstup = "250"
doros = int(vstup)
spolu = doros + 50  # 300
```

Pozor: Ak sa pokúsime previesť neplatný reťazec na číslo (`int("ahoj")`), Python vyvolá výnimku `ValueError`.
""",
            'content_en': """### 1.4 Type Casting in Python

Converting values between types is called explicit casting.

- `int("10")` -> `10`
- `float("2.5")` -> `2.5`
- `str(99)` -> `'99'`
- `bool(0)` -> `False`
""",
            'quizzes': [
                {
                    'question_sk': 'Čo vráti výraz `int(7.89)` v jazyku Python?',
                    'question_en': 'What does `int(7.89)` evaluate to in Python?',
                    'option_a_sk': '8 (zaokrúhli nahor)', 'option_a_en': '8 (rounded up)',
                    'option_b_sk': '7 (odreže desatinnú časť)', 'option_b_en': '7 (truncated)',
                    'option_c_sk': 'Vyvolá ValueError', 'option_c_en': 'Raises ValueError',
                    'option_d_sk': '7.0', 'option_d_en': '7.0',
                    'correct_option': 'B',
                    'explanation_sk': 'Funkcia int() pri prevode z floatu nezaokrúhľuje, ale bez milosti oreže desatinnú časť smerom k nule.',
                    'explanation_en': 'int() truncates floating-point numbers towards zero rather than rounding.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Bezpečný súčet z textových vstupov',
                    'title_en': 'String Inputs Summation',
                    'instructions_sk': 'Napíš funkciu `scitaj_textove_cisla(a_str, b_str)`, ktorá vezme dva reťazce obsahujúce celé čísla, pretypuje ich na `int` a vráti ich celočíselný súčet.',
                    'instructions_en': 'Write a function `scitaj_textove_cisla(a_str, b_str)` converting two string numbers to integers and returning their sum.',
                    'starter_code': 'def scitaj_textove_cisla(a_str, b_str):\n    pass\n',
                    'solution_code': 'def scitaj_textove_cisla(a_str, b_str):\n    return int(a_str) + int(b_str)\n',
                    'explanation_sk': 'Pretypujeme oba reťazce cez int() a sčítame ich.',
                    'explanation_en': 'Convert both strings using int() and add them.',
                    'hint_sk': 'Použi int(a_str) + int(b_str).',
                    'hint_en': 'Use int(a_str) + int(b_str).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'scitaj_textove_cisla("10", "25")', 'expected_output': '35', 'test_code': 'assert scitaj_textove_cisla("10", "25") == 35', 'is_hidden': False},
                        {'input_data': 'scitaj_textove_cisla("-5", "15")', 'expected_output': '10', 'test_code': 'assert scitaj_textove_cisla("-5", "15") == 10', 'is_hidden': False},
                        {'input_data': 'scitaj_textove_cisla("100", "200")', 'expected_output': '300', 'test_code': 'assert scitaj_textove_cisla("100", "200") == 300', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Zhrnutie modulu a praktické mini-projekty s výpočtami',
            'title_en': 'Module Summary & Real-World Calculation Projects',
            'summary_sk': 'Komplexné precvičenie premenných, výpočtov cien s DPH a metriky postavy hráča.',
            'summary_en': 'Comprehensive practice with variables, VAT pricing calculations, and player RPG stats.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 1.5 Zhrnutie modulu 1: Základy a výpočty

V tomto module sme sa naučili:
- Štruktúru Python programu a prácu s `print()`.
- Premenné, priradenie hodnôt a štandard PEP 8 (`snake_case`).
- Štyri základné typy: `int`, `float`, `str`, `bool`.
- Pretypovanie pomocou konverzných funkcií.

V nasledujúcom cvičení si otestuješ prepojenie všetkých vedomostí na komplexnejšom výpočte.
""",
            'content_en': """### 1.5 Module 1 Summary: Basics & Arithmetic

In this module we explored:
- Python syntax and `print()` formatting.
- Variable memory models and PEP 8 guidelines.
- Primitive types: `int`, `float`, `str`, `bool`.
- Explicit type casting.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú hodnotu vráti výraz `bool("")` (prázdny reťazec)?',
                    'question_en': 'What does `bool("")` (empty string) evaluate to?',
                    'option_a_sk': 'True', 'option_a_en': 'True',
                    'option_b_sk': 'False', 'option_b_en': 'False',
                    'option_c_sk': 'None', 'option_c_en': 'None',
                    'option_d_sk': 'Chyba SyntaxError', 'option_d_en': 'SyntaxError',
                    'correct_option': 'B',
                    'explanation_sk': 'V Pythone je prázdny reťazec, nula a None považovaný za False (tzv. Falsy hodnota).',
                    'explanation_en': 'In Python, empty sequences, zero, and None evaluate to False (falsy values).',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet ceny tovaru s DPH a zľavou',
                    'title_en': 'Price Calculation with VAT and Discount',
                    'instructions_sk': (
                        "Napíš funkciu `vypocitaj_cenu_s_dph(zakladna_cena, percento_zlavy, dph_percento)`, ktorá:\n"
                        "1. Zníži základnú cenu o `percento_zlavy` (napr. 10 % z 100 je zľava 10, nová cena 90).\n"
                        "2. K zníženej cene pripočíta DPH podľa `dph_percento` (napr. 20 %).\n"
                        "3. Výslednú sumu zaokrúhli na 2 desatinné miesta pomocou funkcie `round(vysledok, 2)`."
                    ),
                    'instructions_en': 'Write a function `vypocitaj_cenu_s_dph(zakladna_cena, percento_zlavy, dph_percento)` applying discount and then VAT, rounded to 2 decimal places.',
                    'starter_code': 'def vypocitaj_cenu_s_dph(zakladna_cena, percento_zlavy, dph_percento):\n    pass\n',
                    'solution_code': 'def vypocitaj_cenu_s_dph(zakladna_cena, percento_zlavy, dph_percento):\n    cena_po_zlave = zakladna_cena * (1 - percento_zlavy / 100)\n    cena_s_dph = cena_po_zlave * (1 + dph_percento / 100)\n    return round(cena_s_dph, 2)\n',
                    'explanation_sk': 'Najprv aplikujeme zľavu koeficientom (1 - zlavy/100) a potom pripočítame DPH koeficientom (1 + dph/100).',
                    'explanation_en': 'Apply discount multiplier followed by VAT multiplier and round to 2 decimals.',
                    'hint_sk': 'Vzorec: zakladna_cena * (1 - percento_zlavy/100) * (1 + dph_percento/100).',
                    'hint_en': 'Formula: zakladna_cena * (1 - percento_zlavy/100) * (1 + dph_percento/100).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'vypocitaj_cenu_s_dph(100.0, 10.0, 20.0)', 'expected_output': '108.0', 'test_code': 'assert vypocitaj_cenu_s_dph(100.0, 10.0, 20.0) == 108.0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_cenu_s_dph(50.0, 0.0, 20.0)', 'expected_output': '60.0', 'test_code': 'assert vypocitaj_cenu_s_dph(50.0, 0.0, 20.0) == 60.0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_cenu_s_dph(89.90, 15.0, 23.0)', 'expected_output': '94.0', 'test_code': 'assert vypocitaj_cenu_s_dph(89.90, 15.0, 23.0) == 94.0', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
