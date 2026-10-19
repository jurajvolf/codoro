"""
MODUL 5: Funkcie, modularita a rekurzívne algoritmy
Odhadovaný rozsah: 14 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 5,
    'title_sk': 'Funkcie, modularita a rekurzívne algoritmy',
    'title_en': 'Functions, Modularity & Recursive Algorithms',
    'description_sk': 'Nauč sa písať znovupoužiteľný, čistý a modulárny kód. Spoznaj definíciu funkcií (def), návratové hodnoty (return), predvolené argumenty, scope premenných, *args/**kwargs, lambda výrazy a princíp rekurzie.',
    'description_en': 'Master reusable, clean, and modular programming. Learn function definitions (def), return values, default/keyword arguments, variable scope, *args/**kwargs, lambdas, and recursion.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'code-slash',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Definícia funkcie (def), parametre a príkaz return',
            'title_en': 'Function Definition (def), Parameters & return Statement',
            'summary_sk': 'Kľúčové slovo def, formálne parametre vs. skutočné argumenty, príkaz return a None.',
            'summary_en': 'Function definition syntax, formal parameters vs arguments, return statements and implicit None.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 5.1 Funkcie v Pythone

Funkcia je pomenovaný blok kódu navrhnutý na vykonanie konkrétnej úlohy. Zabraňuje opakovaniu kódu (princíp **DRY – Don't Repeat Yourself**).

#### Definícia a volanie:
```python
def pozdrav(meno):
    return f"Ahoj {meno}, vitaj v Codoro!"

sprava = pozdrav("Juraj")
print(sprava)
```

#### Príkaz `return` vs. `print()`:
- `print()` iba zobrazí text na obrazovke používateľa, no hodnota sa stratí.
- `return` odovzdá vypočítanú hodnotu volajúcemu kódu (umožňuje ďalšie výpočty a automatické testovanie).
- Ak funkcia neobsahuje `return`, automaticky vracia hodnotu `None`.
""",
            'content_en': """### 5.1 Functions in Python

Functions encapsulate code blocks for reuse according to the DRY principle.

- `return` sends a computed result back to the caller.
- Functions lacking a return statement implicitly return `None`.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo vráti funkcia v Pythone, ak v jej tele nie je uvedený žiadny príkaz `return`?',
                    'question_en': 'What does a Python function return when no `return` statement is reached?',
                    'option_a_sk': 'None', 'option_a_en': 'None',
                    'option_b_sk': '0', 'option_b_en': '0',
                    'option_c_sk': 'False', 'option_c_en': 'False',
                    'option_d_sk': 'Prázdny reťazec ""', 'option_d_en': 'Empty string ""',
                    'correct_option': 'A',
                    'explanation_sk': 'V Pythone každá funkcia bez explicitného returnu implicitne vráti objekt None.',
                    'explanation_en': 'In Python, functions terminate with an implicit return None if unspecified.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet objemu a povrchu kvádra',
                    'title_en': 'Cuboid Volume and Surface Area',
                    'instructions_sk': 'Napíš funkciu `kvader_metriky(a, b, c)`, ktorá pre zadané tri rozmery vráti dvojicu (tuple) v tvare `(objem, povrch)`. Vzorce: $V = a \\cdot b \\cdot c$, $S = 2(ab + bc + ac)$.',
                    'instructions_en': 'Write `kvader_metriky(a, b, c)` returning tuple `(objem, povrch)`.',
                    'starter_code': 'def kvader_metriky(a, b, c):\n    pass\n',
                    'solution_code': 'def kvader_metriky(a, b, c):\n    v = a * b * c\n    s = 2 * (a * b + b * c + a * c)\n    return (v, s)\n',
                    'explanation_sk': 'Aplikujeme matematické vzorce a vrátime dvojprvkovú n-ticu (tuple).',
                    'explanation_en': 'Compute volume and surface area, returning a 2-tuple.',
                    'hint_sk': 'objem = a * b * c; povrch = 2 * (a*b + b*c + a*c); return (objem, povrch).',
                    'hint_en': 'volume = a * b * c; surface = 2 * (a*b + b*c + a*c); return (volume, surface).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'kvader_metriky(2, 3, 4)', 'expected_output': '(24, 52)', 'test_code': 'assert kvader_metriky(2, 3, 4) == (24, 52)', 'is_hidden': False},
                        {'input_data': 'kvader_metriky(1, 1, 1)', 'expected_output': '(1, 6)', 'test_code': 'assert kvader_metriky(1, 1, 1) == (1, 6)', 'is_hidden': False},
                        {'input_data': 'kvader_metriky(5, 10, 2)', 'expected_output': '(100, 160)', 'test_code': 'assert kvader_metriky(5, 10, 2) == (100, 160)', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Predvolené hodnoty a pomenované argumenty',
            'title_en': 'Default Values & Keyword Arguments',
            'summary_sk': 'Nastavenie predvolených parametrov (def f(x=10)), pozicionálne vs. pomenované argumenty.',
            'summary_en': 'Default parameter values, positional vs. keyword arguments, and mutable default trap.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 5.2 Predvolené a pomenované argumenty

Parametrom funkcie môžeme nastaviť predvolenú hodnotu, ktorá sa použije, ak volajúci tento argument nezadá:

```python
def pripis_doros(zostatok, odmena=50):
    return zostatok + odmena

print(pripis_doros(100))      # 150 (použije predvolených 50)
print(pripis_doros(100, 20))  # 120 (vlastná hodnota)
```

#### Pozor na zradné meniteľné predvolené hodnoty!
NIKDY nenastavujte ako predvolenú hodnotu prázdny zoznam `def f(zoznam=[]):`! Zoznam sa vytvorí iba raz pri načítaní funkcie a bude sa zdieľať medzi všetkými volaniami. Správny spôsob je `def f(zoznam=None): if zoznam is None: zoznam = []`.
""",
            'content_en': """### 5.2 Default Values & Keyword Arguments

Parameters can define defaults: `def send_alert(msg, priority="NORMAL"):`. Beware mutable default arguments like `[]` or `{}`!
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo sa neodporúča použiť meniteľný objekt (napr. prázdny zoznam []) ako predvolenú hodnotu parametra?',
                    'question_en': 'Why should mutable objects like [] never be used as default argument values in Python?',
                    'option_a_sk': 'Pretože zoznam sa vytvorí iba raz pri definícii funkcie a modifikácie sa budú prenášať do ďalších volaní', 'option_a_en': 'Because the default list is bound at function definition time and shared across subsequent calls',
                    'option_b_sk': 'Pretože to spôsobí SyntaxError', 'option_b_en': 'Because it raises SyntaxError',
                    'option_c_sk': 'Pretože Python nepodporuje zoznamy vo funkciách', 'option_c_en': 'Because lists are unsupported',
                    'option_d_sk': 'Pretože zaberie príliš veľa RAM', 'option_d_en': 'Excessive memory usage',
                    'correct_option': 'A',
                    'explanation_sk': 'V Pythone sa predvolené hodnoty vyhodnocujú v čase definície funkcie (def), preto je mutable default objekt zdieľaný.',
                    'explanation_en': 'Default parameter values are evaluated once when the function is defined, making mutable defaults persistent.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Generátor profilového textu s voliteľnými parametrami',
                    'title_en': 'Profile Generator with Defaults',
                    'instructions_sk': (
                        "Napíš funkciu `vytvor_profil(meno, rola=\"Študent\", rank=\"Novice\")`, ktorá vráti reťazec:\n"
                        "`\"[MENO] ([ROLA]) - Rank: [RANK]\"`.\n"
                        "Napr. pre `vytvor_profil(\"Juraj\")` vráti:\n"
                        "`\"Juraj (Študent) - Rank: Novice\"`."
                    ),
                    'instructions_en': 'Write `vytvor_profil(meno, rola="Študent", rank="Novice")` returning formatted profile string.',
                    'starter_code': 'def vytvor_profil(meno, rola="Študent", rank="Novice"):\n    pass\n',
                    'solution_code': 'def vytvor_profil(meno, rola="Študent", rank="Novice"):\n    return f"{meno} ({rola}) - Rank: {rank}"\n',
                    'explanation_sk': 'Používame f-string so zadanými alebo predvolenými hodnotami parametrov.',
                    'explanation_en': 'Use f-string embedding default or provided keyword parameters.',
                    'hint_sk': 'Použi f"{meno} ({rola}) - Rank: {rank}".',
                    'hint_en': 'Use f"{meno} ({rola}) - Rank: {rank}".',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vytvor_profil("Juraj")', 'expected_output': 'Juraj (Študent) - Rank: Novice', 'test_code': 'assert vytvor_profil("Juraj") == "Juraj (Študent) - Rank: Novice"', 'is_hidden': False},
                        {'input_data': 'vytvor_profil("Codo", rola="AI Tútor", rank="Master")', 'expected_output': 'Codo (AI Tútor) - Rank: Master', 'test_code': 'assert vytvor_profil("Codo", rola="AI Tútor", rank="Master") == "Codo (AI Tútor) - Rank: Master"', 'is_hidden': False},
                        {'input_data': 'vytvor_profil("Markéta", rola="Učiteľ")', 'expected_output': 'Markéta (Učiteľ) - Rank: Novice', 'test_code': 'assert vytvor_profil("Markéta", rola="Učiteľ") == "Markéta (Učiteľ) - Rank: Novice"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Oblasť platnosti premenných (Scope) a čisté funkcie',
            'title_en': 'Variable Scope (Local vs Global) & Pure Functions',
            'summary_sk': 'Lokálne vs. globálne premenné, pravidlo LEGB, vedľajšie účinky a princíp čistých funkcií.',
            'summary_en': 'Local vs global variables, the LEGB resolution rule, side effects, and pure function concepts.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 5.3 Oblasť platnosti premenných (Scope) a LEGB pravidlo

Premenné vytvorené vo vnútri funkcie sú **lokálne** – existujú iba počas behu funkcie a zvonku k nim nie je prístup.

#### Pravidlo hľadania premenných (LEGB):
1. **L**ocal – lokálne premenné funkcie.
2. **E**nclosing – premenné obklopujúcej funkcie (pri vnorených funkciách).
3. **G**lobal – premenné na úrovni celého modulu.
4. **B**uilt-in – vstavané funkcie Pythonu (`len`, `print`, `sum`).

#### Čisté funkcie (Pure Functions):
Čistá funkcia spĺňa dve vlastnosti:
1. Pre rovnaké vstupné argumenty vráti **vždy rovnaký výsledok**.
2. Nemá žiadne **vedľajšie účinky (Side Effects)** – nemení globálne premenné ani nemodifikuje vstupné objekty.
""",
            'content_en': """### 5.3 Variable Scope (LEGB) & Pure Functions

Python resolves names using the LEGB hierarchy: Local -> Enclosing -> Global -> Built-in. Pure functions avoid side-effects and guarantee deterministic outputs.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo znamená skratka LEGB v jazyku Python?',
                    'question_en': 'What does the acronym LEGB stand for in Python name resolution?',
                    'option_a_sk': 'Local, Enclosing, Global, Built-in', 'option_a_en': 'Local, Enclosing, Global, Built-in',
                    'option_b_sk': 'Loop, Exit, Go, Break', 'option_b_en': 'Loop, Exit, Go, Break',
                    'option_c_sk': 'List, Element, Group, Byte', 'option_c_en': 'List, Element, Group, Byte',
                    'option_d_sk': 'Level, Experience, Gold, Bonus', 'option_d_en': 'Level, Experience, Gold, Bonus',
                    'correct_option': 'A',
                    'explanation_sk': 'LEGB opisuje poradie prehľadávania menných priestorov: Local -> Enclosing -> Global -> Built-in.',
                    'explanation_en': 'LEGB defines the exact order Python inspects scope namespaces.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Čistá normalizácia dát bez vedľajších účinkov',
                    'title_en': 'Pure Function Data Normalizer',
                    'instructions_sk': (
                        "Napíš čistú funkciu `normalizuj_zoznam(cisla)`, ktorá vráti **nový zoznam**, kde je každé číslo vydelené maximálnou hodnotou v zozname (zaokrúhlené na 3 desatinné miesta cez `round()`).\n"
                        "Funkcia NESMIE modifikovať pôvodný vstupný zoznam! Ak je zoznam prázdny alebo je maximum 0, vráti prázdny zoznam `[]`."
                    ),
                    'instructions_en': 'Write pure function `normalizuj_zoznam(cisla)` dividing elements by max value rounded to 3 decimals without mutating input.',
                    'starter_code': 'def normalizuj_zoznam(cisla):\n    pass\n',
                    'solution_code': 'def normalizuj_zoznam(cisla):\n    if not cisla:\n        return []\n    m = max(cisla)\n    if m == 0:\n        return []\n    return [round(x / m, 3) for x in cisla]\n',
                    'explanation_sk': 'Vytvárame nový zoznam pomocou list comprehension, pôvodný zoznam zostáva nedotknutý.',
                    'explanation_en': 'Construct a fresh list with list comprehension preserving input immutability.',
                    'hint_sk': 'm = max(cisla); return [round(x / m, 3) for x in cisla].',
                    'hint_en': 'm = max(cisla); return [round(x / m, 3) for x in cisla].',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'normalizuj_zoznam([10, 20, 50, 100])', 'expected_output': '[0.1, 0.2, 0.5, 1.0]', 'test_code': 'assert normalizuj_zoznam([10, 20, 50, 100]) == [0.1, 0.2, 0.5, 1.0]', 'is_hidden': False},
                        {'input_data': 'normalizuj_zoznam([])', 'expected_output': '[]', 'test_code': 'assert normalizuj_zoznam([]) == []', 'is_hidden': False},
                        {'input_data': 'normalizuj_zoznam([3, 6, 9])', 'expected_output': '[0.333, 0.667, 1.0]', 'test_code': 'assert normalizuj_zoznam([3, 6, 9]) == [0.333, 0.667, 1.0]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Variabilné argumenty (*args, **kwargs) a anonymné lambda funkcie',
            'title_en': 'Variable Arguments (*args, **kwargs) & lambda Functions',
            'summary_sk': 'Prijatie ľubovoľného počtu pozicionálnych a kľúčových argumentov, syntax lambda parametre: vyraz.',
            'summary_en': 'Arbitrary arguments (*args, **kwargs) unpacking and one-line anonymous lambda expressions.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 5.4 `*args`, `**kwargs` a `lambda` funkcie

#### Variabilný počet argumentov:
- `*args` – zabalí ľubovoľný počet pozičných argumentov do **n-tice (tuple)**.
- `**kwargs` – zabalí ľubovoľný počet pomenovaných argumentov do **slovníka (dict)**.

```python
def celkovy_sucet(*args):
    return sum(args)

print(celkovy_sucet(10, 20, 30))  # 60
```

#### Anonymné funkcie (`lambda`):
Krátke jednoriadkové funkcie bez mena:
```python
# Syntax: lambda parametre: vyraz
dvojnasobok = lambda x: x * 2
print(dvojnasobok(5))  # 10
```
Často sa používajú pri triedení: `zoznam.sort(key=lambda x: x['vek'])`.
""",
            'content_en': """### 5.4 `*args`, `**kwargs` and `lambda`

- `*args` collects extra positional arguments into a tuple.
- `**kwargs` collects extra keyword arguments into a dict.
- `lambda` creates concise anonymous functions: `lambda x, y: x + y`.
""",
            'quizzes': [
                {
                    'question_sk': 'Do akej dátovej štruktúry Python zabalí argumenty prijaté cez `*args`?',
                    'question_en': 'What data structure does Python use to pack arguments passed via `*args`?',
                    'option_a_sk': 'N-tica (tuple)', 'option_a_en': 'Tuple',
                    'option_b_sk': 'Zoznam (list)', 'option_b_en': 'List',
                    'option_c_sk': 'Slovník (dict)', 'option_c_en': 'Dictionary',
                    'option_d_sk': 'Množina (set)', 'option_d_en': 'Set',
                    'correct_option': 'A',
                    'explanation_sk': '*args zbalí ľubovoľný počet pozičných argumentov do nemenného tuple.',
                    'explanation_en': '*args unpacks into a tuple of positional arguments.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Flexibilná kalkulačka priemeru (*args)',
                    'title_en': 'Flexible Average Calculator (*args)',
                    'instructions_sk': (
                        "Napíš funkciu `vypocitaj_flexi_priemer(*cisla)`, ktorá prijme ľubovoľný počet číselných argumentov a vráti ich aritmetický priemer zaokrúhlený na 2 desatinné miesta.\n"
                        "Ak nie je zadaný ani jeden argument, vráti `0.0`."
                    ),
                    'instructions_en': 'Write `vypocitaj_flexi_priemer(*cisla)` accepting arbitrary numbers via *args and returning mean rounded to 2 decimals.',
                    'starter_code': 'def vypocitaj_flexi_priemer(*cisla):\n    pass\n',
                    'solution_code': 'def vypocitaj_flexi_priemer(*cisla):\n    if not cisla:\n        return 0.0\n    return round(sum(cisla) / len(cisla), 2)\n',
                    'explanation_sk': 'Spracujeme n-ticu cisla vytvorenú cez *args.',
                    'explanation_en': 'Process packed tuple arguments checking emptiness before computing mean.',
                    'hint_sk': 'if not cisla: return 0.0; return round(sum(cisla) / len(cisla), 2).',
                    'hint_en': 'if not cisla: return 0.0; return round(sum(cisla) / len(cisla), 2).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vypocitaj_flexi_priemer(10, 20, 30)', 'expected_output': '20.0', 'test_code': 'assert vypocitaj_flexi_priemer(10, 20, 30) == 20.0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_flexi_priemer()', 'expected_output': '0.0', 'test_code': 'assert vypocitaj_flexi_priemer() == 0.0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_flexi_priemer(5, 7, 9, 11)', 'expected_output': '8.0', 'test_code': 'assert vypocitaj_flexi_priemer(5, 7, 9, 11) == 8.0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Rekurzia v Pythone: princíp, rekurzívny krok a algoritmy',
            'title_en': 'Recursion in Python: Base Cases & Algorithms',
            'summary_sk': 'Princíp rekurzie (funkcia volá samu seba), bázový stav (Base Case), faktoriál, Fibonacci a GCD.',
            'summary_en': 'Recursive function design, base case vs recursive step, call stack, factorial, Fibonacci, and GCD.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 5.5 Rekurzia v Pythone

**Rekurzia** je programátorská technika, pri ktorej funkcia volá samú seba za účelom vyriešenia menšieho podproblému.

#### Každá správna rekurzívna funkcia MUSÍ obsahovať dve časti:
1. **Základný prípad (Base Case)**: Podmienka, pri ktorej sa rekurzia zastaví a vráti konkrétny výsledok bez ďalšieho rekurzívneho volania.
2. **Rekurzívny krok (Recursive Step)**: Funkcia zavolá samú seba s argumentom zmenšeným smerom k základnému prípadu.

```python
def factorial(n):
    # 1. Základný prípad
    if n <= 1:
        return 1
    # 2. Rekurzívny krok
    return n * factorial(n - 1)
```

Bez základného prípadu dôjde k pretečeniu zásobníka volaní: `RecursionError: maximum recursion depth exceeded`.
""",
            'content_en': """### 5.5 Recursion in Python

A recursive function calls itself to solve smaller sub-problems. It strictly requires a base case to prevent stack overflow.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo sa stane, ak v rekurzívnej funkcii vynecháš základný prípad (Base Case)?',
                    'question_en': 'What happens if a recursive function lacks a base case?',
                    'option_a_sk': 'Python vyvolá výnimku RecursionError po dosiahnutí limitu hĺbky rekurzie', 'option_a_en': 'Python raises RecursionError after exceeding maximum call depth',
                    'option_b_sk': 'Funkcia vráti 0', 'option_b_en': 'Returns 0',
                    'option_c_sk': 'Počítač sa reštartuje', 'option_c_en': 'Computer restarts',
                    'option_d_sk': 'Kód sa automaticky zmení na cyklus while', 'option_d_en': 'Automatically transforms to while',
                    'correct_option': 'A',
                    'explanation_sk': 'Bez ukončovacej podmienky sa funkcia volá donekonečna, až kým nenarazí na limit zásobníka (štandardne 1000 volaní) a vyvolá RecursionError.',
                    'explanation_en': 'Infinite recursive calls exhaust Python call stack causing RecursionError.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Euklidov algoritmus pre najväčší spoločný deliteľ (GCD)',
                    'title_en': 'Euclidean Algorithm for Greatest Common Divisor',
                    'instructions_sk': (
                        "Napíš čistú rekurzívnu funkciu `rekurzivne_gcd(a, b)`, ktorá vypočíta najväčší spoločný deliteľ dvoch čísel podľa Euklidovho algoritmu:\n"
                        "- Základný prípad: ak $b == 0$, výsledkom je $a$.\n"
                        "- Rekurzívny krok: vráť `rekurzivne_gcd(b, a % b)`."
                    ),
                    'instructions_en': 'Write recursive `rekurzivne_gcd(a, b)` computing greatest common divisor: base case b == 0 returns a, else recurse on (b, a % b).',
                    'starter_code': 'def rekurzivne_gcd(a, b):\n    pass\n',
                    'solution_code': 'def rekurzivne_gcd(a, b):\n    if b == 0:\n        return a\n    return rekurzivne_gcd(b, a % b)\n',
                    'explanation_sk': 'Klasický Euklidov algoritmus implementovaný v dvoch riadkoch elegantnou rekurziou.',
                    'explanation_en': 'Two-line recursive implementation of the Euclidean algorithm.',
                    'hint_sk': 'if b == 0: return a; return rekurzivne_gcd(b, a % b).',
                    'hint_en': 'if b == 0: return a; return rekurzivne_gcd(b, a % b).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'rekurzivne_gcd(48, 18)', 'expected_output': '6', 'test_code': 'assert rekurzivne_gcd(48, 18) == 6', 'is_hidden': False},
                        {'input_data': 'rekurzivne_gcd(100, 25)', 'expected_output': '25', 'test_code': 'assert rekurzivne_gcd(100, 25) == 25', 'is_hidden': False},
                        {'input_data': 'rekurzivne_gcd(1071, 462)', 'expected_output': '21', 'test_code': 'assert rekurzivne_gcd(1071, 462) == 21', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
