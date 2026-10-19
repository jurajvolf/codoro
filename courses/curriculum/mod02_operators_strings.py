"""
MODUL 2: Operátory, matematické výrazy a pokročilá práca s reťazcami
Odhadovaný rozsah: 12 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 2,
    'title_sk': 'Operátory, matematické výrazy a práca s reťazcami',
    'title_en': 'Operators, Mathematical Expressions & String Manipulation',
    'description_sk': 'Získaj istotu v aritmetických operáciách (//, %, **), logických spojkách (and, or, not), indexovaní reťazcov a ich rezaní (slicing), ako aj najdôležitejších textových metódach.',
    'description_en': 'Master arithmetic operators (//, %, **), boolean logic (and, or, not), string indexing, slicing [start:stop:step], and essential string manipulation methods.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'calculator',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Aritmetické operátory, celočíselné delenie a zvyšok po delení',
            'title_en': 'Arithmetic Operators, Floor Division & Modulo',
            'summary_sk': 'Klasické delenie /, celočíselné delenie //, operátor modulo % a umocňovanie **.',
            'summary_en': 'Float division /, floor division //, modulo %, exponentiation ** and precedence.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 2.1 Aritmetické operátory v Pythone

Python podporuje všetky štandardné matematické operácie s rešpektovaním matematickej priority operátorov.

| Operátor | Operácia | Príklad | Výsledok |
|---|---|---|---|
| `+` | Sčítanie | `7 + 3` | `10` |
| `-` | Odčítanie | `10 - 4` | `6` |
| `*` | Násobenie | `6 * 7` | `42` |
| `/` | Bežné delenie (vždy vracia `float`!) | `7 / 2` | `3.5` |
| `//` | Celočíselné delenie (Floor Division) | `7 // 2` | `3` |
| `%` | Zvyšok po delení (Modulo) | `7 % 2` | `1` |
| `**` | Umocňovanie (Power) | `2 ** 8` | `256` |

#### Praktické využitie operátora modulo `%`:
- Overenie párnosti čísla: `cislo % 2 == 0` (ak je zvyšok 0, číslo je párne).
- Prevod minút na hodiny a minúty:
```python
celkove_minuty = 145
hodiny = celkove_minuty // 60   # 2 hodiny
zvysne_minuty = celkove_minuty % 60  # 25 minút
```
""",
            'content_en': """### 2.1 Arithmetic Operators in Python

Python provides standard and integer-specific arithmetic operators.

- `/` always produces a `float` (`10 / 2` -> `5.0`).
- `//` discards the fractional part (`10 // 3` -> `3`).
- `%` computes the remainder (`10 % 3` -> `1`).
- `**` performs exponentiation (`3 ** 3` -> `27`).
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je výsledok výrazu `17 % 5` v Pythone?',
                    'question_en': 'What is the result of `17 % 5` in Python?',
                    'option_a_sk': '3', 'option_a_en': '3',
                    'option_b_sk': '2', 'option_b_en': '2',
                    'option_c_sk': '3.4', 'option_c_en': '3.4',
                    'option_d_sk': '1', 'option_d_en': '1',
                    'correct_option': 'B',
                    'explanation_sk': '17 delené 5 je 3 a zvyšok je 2 (3 * 5 + 2 = 17).',
                    'explanation_en': '17 divided by 5 is 3 with a remainder of 2.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Prevodník sekúnd na časový formát',
                    'title_en': 'Seconds to Time Formatter',
                    'instructions_sk': 'Napíš funkciu `sekundy_na_cas(sekundy)`, ktorá prevedie celkový počet sekúnd na textový formát `"HH:MM:SS"`. Napríklad `3665` sekúnd je `"01:01:05"`.',
                    'instructions_en': 'Write a function `sekundy_na_cas(sekundy)` converting total seconds to `"HH:MM:SS"`.',
                    'starter_code': 'def sekundy_na_cas(sekundy):\n    pass\n',
                    'solution_code': 'def sekundy_na_cas(sekundy):\n    hodiny = sekundy // 3600\n    zvysok = sekundy % 3600\n    minuty = zvysok // 60\n    sek = zvysok % 60\n    return f"{hodiny:02d}:{minuty:02d}:{sek:02d}"\n',
                    'explanation_sk': 'Celočíselným delením 3600 získame hodiny, zo zvyšku delením 60 minúty a zvyšok sú sekundy.',
                    'explanation_en': 'Divide by 3600 for hours, then remainder by 60 for minutes, leaving residual seconds.',
                    'hint_sk': 'Použi hodiny = sekundy // 3600 a zvysok = sekundy % 3600.',
                    'hint_en': 'Use hours = sekundy // 3600 and remainder = sekundy % 3600.',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'sekundy_na_cas(3665)', 'expected_output': '01:01:05', 'test_code': 'assert sekundy_na_cas(3665) == "01:01:05"', 'is_hidden': False},
                        {'input_data': 'sekundy_na_cas(60)', 'expected_output': '00:01:00', 'test_code': 'assert sekundy_na_cas(60) == "00:01:00"', 'is_hidden': False},
                        {'input_data': 'sekundy_na_cas(7322)', 'expected_output': '02:02:02', 'test_code': 'assert sekundy_na_cas(7322) == "02:02:02"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Porovnávacie a logické operátory',
            'title_en': 'Comparison & Boolean Logic Operators',
            'summary_sk': 'Operátory ==, !=, <, >, <=, >= a logické spojky and, or, not.',
            'summary_en': 'Comparison operators ==, !=, <, >, <=, >= and boolean operators and, or, not.',
            'estimated_minutes': 45,
            'xp_reward': 25,
            'is_published': True,
            'content_sk': """### 2.2 Porovnávanie a boolovská logika

Porovnávacie operátory porovnávajú dve hodnoty a výsledkom je vždy `True` alebo `False`.

- `==` rovnosť (POZOR: jedno `=` je priradenie!)
- `!=` nerovnosť
- `<`, `>`, `<=`, `>=` menší, väčší, menší/rovný, väčší/rovný

#### Logické spojky:
- `and` – vráti `True`, len ak sú **obe** podmienky pravdivé.
- `or` – vráti `True`, ak je aspoň **jedna** podmienka pravdivá.
- `not` – negácia (obráti `True` na `False` a naopak).

```python
vek = 17
ma_suhlas = True

moze_vstupit = (vek >= 18) or ma_suhlas  # True
```
""",
            'content_en': """### 2.2 Comparison and Boolean Logic

Comparison operators evaluate expressions to boolean `True` or `False`.

- `==` Equality
- `!=` Inequality
- `and`, `or`, `not` Logical conjunction, disjunction, and negation.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú hodnotu vráti výraz `not (True and False)`?',
                    'question_en': 'What does `not (True and False)` evaluate to?',
                    'option_a_sk': 'True', 'option_a_en': 'True',
                    'option_b_sk': 'False', 'option_b_en': 'False',
                    'option_c_sk': 'None', 'option_c_en': 'None',
                    'option_d_sk': 'SyntaxError', 'option_d_en': 'SyntaxError',
                    'correct_option': 'A',
                    'explanation_sk': 'True and False je False, a not False je True.',
                    'explanation_en': 'True and False is False; negating it with not yields True.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Overenie nároku na zľavu študenta',
                    'title_en': 'Student Discount Eligibility',
                    'instructions_sk': 'Napíš funkciu `ma_narok_na_zlavu(vek, je_student, ma_isic)`, ktorá vráti `True`, ak má osoba menej ako 18 rokov, ALEBO ak je študent a zároveň vlastní platný ISIC preukaz.',
                    'instructions_en': 'Write a function `ma_narok_na_zlavu(vek, je_student, ma_isic)` returning `True` if under 18 or a student with valid ISIC.',
                    'starter_code': 'def ma_narok_na_zlavu(vek, je_student, ma_isic):\n    pass\n',
                    'solution_code': 'def ma_narok_na_zlavu(vek, je_student, ma_isic):\n    return (vek < 18) or (je_student and ma_isic)\n',
                    'explanation_sk': 'Kombinácia podmienok s prioritou operátora and pred or.',
                    'explanation_en': 'Logical combination where and binds tighter than or.',
                    'hint_sk': 'Použi return (vek < 18) or (je_student and ma_isic).',
                    'hint_en': 'Use return (vek < 18) or (je_student and ma_isic).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'ma_narok_na_zlavu(16, False, False)', 'expected_output': 'True', 'test_code': 'assert ma_narok_na_zlavu(16, False, False) is True', 'is_hidden': False},
                        {'input_data': 'ma_narok_na_zlavu(21, True, True)', 'expected_output': 'True', 'test_code': 'assert ma_narok_na_zlavu(21, True, True) is True', 'is_hidden': False},
                        {'input_data': 'ma_narok_na_zlavu(21, True, False)', 'expected_output': 'False', 'test_code': 'assert ma_narok_na_zlavu(21, True, False) is False', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Indexovanie a rezanie reťazcov (String Slicing)',
            'title_en': 'String Indexing & Slicing [start:stop:step]',
            'summary_sk': 'Indexovanie od nuly, záporné indexy zozadu a syntax [start:stop:step].',
            'summary_en': 'Zero-based indexing, negative reverse indexing, and the [start:stop:step] slicing syntax.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 2.3 Indexovanie a Slicing v Pythone

Reťazec (`str`) je usporiadaná postupnosť znakov. Jednotlivé znaky môžeme vyberať pomocou indexu v hranatých zátvorkách `[]`.

```
Index:    0   1   2   3   4   5
Znak:     C   o   d   o   r   o
Záporný: -6  -5  -4  -3  -2  -1
```

```python
text = "Codoro"
print(text[0])   # 'C'
print(text[-1])  # 'o' (posledný znak)
```

#### Rezanie reťazcov: `[start:stop:step]`
- `start` – počiatočný index (vrátane)
- `stop` – koncový index (okrem neho!)
- `step` – krok (voliteľný, predvolený 1)

```python
jazyk = "Python"
print(jazyk[0:2])   # 'Py'
print(jazyk[2:])    # 'thon' (od indexu 2 do konca)
print(jazyk[:4])    # 'Pyth' (od začiatku po index 4)
print(jazyk[::-1])  # 'nohtyP' (obrátenie reťazca!)
```
""",
            'content_en': """### 2.3 String Indexing and Slicing

Strings are immutable zero-indexed sequences of characters.

- `text[0]` first character
- `text[-1]` last character
- `text[start:stop:step]` sub-string extraction
- `text[::-1]` reverse string trick
""",
            'quizzes': [
                {
                    'question_sk': 'Čo vráti výraz `"Bratislava"[0:5]`?',
                    'question_en': 'What does `"Bratislava"[0:5]` return?',
                    'option_a_sk': '"Brati"', 'option_a_en': '"Brati"',
                    'option_b_sk': '"Bratis"', 'option_b_en': '"Bratis"',
                    'option_c_sk': '"Brat"', 'option_c_en': '"Brat"',
                    'option_d_sk': '"ratis"', 'option_d_en': '"ratis"',
                    'correct_option': 'A',
                    'explanation_sk': 'Indexy 0, 1, 2, 3, 4 tvoria znaky B-r-a-t-i (index 5 sa do rezu nezahŕňa).',
                    'explanation_en': 'Slice indices 0 through 4 include the 5 letters B-r-a-t-i.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Detektor palindrómov',
                    'title_en': 'Palindrome Checker',
                    'instructions_sk': 'Napíš funkciu `je_palindrom(slovo)`, ktorá vráti `True`, ak sa dané slovo číta rovnako spredu aj zozadu (napr. "radar", "kajak"). Ignoruj veľkosť písmen pomocou `.lower()`.',
                    'instructions_en': 'Write a function `je_palindrom(slovo)` returning `True` if the word reads identically backwards.',
                    'starter_code': 'def je_palindrom(slovo):\n    pass\n',
                    'solution_code': 'def je_palindrom(slovo):\n    ciste = slovo.lower()\n    return ciste == ciste[::-1]\n',
                    'explanation_sk': 'Slovo prevedieme na malé písmená a porovnáme s jeho obráteným rezom [::-1].',
                    'explanation_en': 'Lowercase the string and check equality with its reversed slice [::-1].',
                    'hint_sk': 'Použi ciste = slovo.lower() a porovnaj ciste == ciste[::-1].',
                    'hint_en': 'Use ciste = slovo.lower() and check ciste == ciste[::-1].',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'je_palindrom("Radar")', 'expected_output': 'True', 'test_code': 'assert je_palindrom("Radar") is True', 'is_hidden': False},
                        {'input_data': 'je_palindrom("Python")', 'expected_output': 'False', 'test_code': 'assert je_palindrom("Python") is False', 'is_hidden': False},
                        {'input_data': 'je_palindrom("kajak")', 'expected_output': 'True', 'test_code': 'assert je_palindrom("kajak") is True', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Vstavané metódy reťazcov',
            'title_en': 'Built-in String Methods',
            'summary_sk': 'Metódy upper(), lower(), strip(), replace(), split(), join() a find().',
            'summary_en': 'String methods upper(), lower(), strip(), replace(), split(), join(), and find().',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 2.4 Vstavané metódy reťazcov

Reťazce v Pythone sú **nemenné (immutable)**. To znamená, že žiadna metóda nemení pôvodný reťazec, ale vracia **nový** upravený reťazec.

#### Kľúčové metódy:
1. `text.upper()` / `text.lower()` – zmena veľkosti písmen.
2. `text.strip()` – odstránenie bielych znakov (medzier, tabulátorov) zo začiatku a konca.
3. `text.replace(stary, novy)` – nahradenie výskytov podreťazca.
4. `text.split(oddelovac)` – rozdelenie reťazca na zoznam podľa oddeľovača.
5. `oddelovac.join(zoznam)` – spojenie zoznamu reťazcov do jedného.
6. `text.find(hladany)` – index prvého výskytu (-1 ak sa nenájde).

```python
vstup = "  janko.hrasko@skola.sk  "
cisty = vstup.strip().lower()
casti = cisty.split("@")  # ['janko.hrasko', 'skola.sk']
```
""",
            'content_en': """### 2.4 Built-in String Methods

Strings are immutable; methods return a modified new string.

- `strip()` trims leading and trailing whitespace.
- `replace(old, new)` replaces substrings.
- `split(sep)` splits string into a list.
- `sep.join(list)` concatenates list elements.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo vráti metóda `text.find("x")`, ak sa znak "x" v texte nenachádza?',
                    'question_en': 'What does `text.find("x")` return if "x" is not found in the string?',
                    'option_a_sk': 'None', 'option_a_en': 'None',
                    'option_b_sk': 'False', 'option_b_en': 'False',
                    'option_c_sk': '-1', 'option_c_en': '-1',
                    'option_d_sk': 'Vyvolá ValueError', 'option_d_en': 'Raises ValueError',
                    'correct_option': 'C',
                    'explanation_sk': 'Metóda find() vráti -1, ak hľadaný reťazec neexistuje (na rozdiel od metódy index(), ktorá vyvolá výnimku).',
                    'explanation_en': 'find() returns -1 on failure, whereas index() raises a ValueError.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Generátor používateľských mien (Username Sanitizer)',
                    'title_en': 'Username Sanitizer',
                    'instructions_sk': (
                        "Napíš funkciu `vytvor_pouzivatelske_meno(cele_meno)`, ktorá:\n"
                        "1. Odstráni medzery na začiatku a konci.\n"
                        "2. Prevedie text na malé písmená.\n"
                        "3. Nahradí všetky vnútorné medzery podčiarkovníkom `_`.\n"
                        "Napr. pre `'  Juraj Volf  '` vráti `'juraj_volf'`."
                    ),
                    'instructions_en': 'Write a function `vytvor_pouzivatelske_meno(cele_meno)` trimming whitespace, lowercasing, and replacing spaces with underscores.',
                    'starter_code': 'def vytvor_pouzivatelske_meno(cele_meno):\n    pass\n',
                    'solution_code': 'def vytvor_pouzivatelske_meno(cele_meno):\n    return cele_meno.strip().lower().replace(" ", "_")\n',
                    'explanation_sk': 'Zreťazenie metód: strip() odstráni krajné medzery, lower() zmenší písmená a replace() nahradí medzery za _.',
                    'explanation_en': 'Method chaining: strip() -> lower() -> replace(" ", "_").',
                    'hint_sk': 'Použi cele_meno.strip().lower().replace(" ", "_").',
                    'hint_en': 'Use cele_meno.strip().lower().replace(" ", "_").',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vytvor_pouzivatelske_meno("  Juraj Volf  ")', 'expected_output': 'juraj_volf', 'test_code': 'assert vytvor_pouzivatelske_meno("  Juraj Volf  ") == "juraj_volf"', 'is_hidden': False},
                        {'input_data': 'vytvor_pouzivatelske_meno("Martin Kovac")', 'expected_output': 'martin_kovac', 'test_code': 'assert vytvor_pouzivatelske_meno("Martin Kovac") == "martin_kovac"', 'is_hidden': False},
                        {'input_data': 'vytvor_pouzivatelske_meno("  Peter Jan Novak  ")', 'expected_output': 'peter_jan_novak', 'test_code': 'assert vytvor_pouzivatelske_meno("  Peter Jan Novak  ") == "peter_jan_novak"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Moderné formátovanie textu a zhrnutie modulu',
            'title_en': 'Advanced String Formatting & Module Summary',
            'summary_sk': 'Zarovnávanie textu vo f-stringoch, šírka poľa, desatinné miesta a komplexná výzva.',
            'summary_en': 'Field padding, alignment, precision specifiers in f-strings, and comprehensive challenge.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 2.5 Formátovacie špecifikátory vo f-stringoch

F-stringy ponúkajú mimoriadne silnú syntax za dvojbodkou `:`:

- `{cislo:.2f}` – zaokrúhlenie desatinného čísla na 2 miesta.
- `{text:>15}` – zarovnanie textu doprava na šírku 15 znakov.
- `{text:<15}` – zarovnanie doľava.
- `{cislo:05d}` – doplnenie celého čísla nulami spredu na 5 miest.

```python
cena = 19.9
kod = 42
print(f"Položka: CDR-{kod:04d} | Cena: {cena:8.2f} EUR")
# Výstup: Položka: CDR-0042 | Cena:    19.90 EUR
```
""",
            'content_en': """### 2.5 Advanced f-string Format Specifiers

Use format specifiers after a colon `:` inside f-strings:

- `{x:.2f}` 2 decimal places float
- `{x:04d}` 4-digit zero-padded integer
- `{x:>10}` right-align with width 10
""",
            'quizzes': [
                {
                    'question_sk': 'Aký reťazec vyprodukuje výraz `f"{7:03d}"`?',
                    'question_en': 'What string does `f"{7:03d}"` produce?',
                    'option_a_sk': '"007"', 'option_a_en': '"007"',
                    'option_b_sk': '"700"', 'option_b_en': '"700"',
                    'option_c_sk': '"3.7"', 'option_c_en': '"3.7"',
                    'option_d_sk': '"7"', 'option_d_en': '"7"',
                    'correct_option': 'A',
                    'explanation_sk': 'Formát :03d znamená celé číslo s minimálnou šírkou 3 znaky doplnené nulami zľava.',
                    'explanation_en': ':03d specifies a decimal integer padded with zeros to width 3.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Formátovač študentského ID odznaku',
                    'title_en': 'Student ID Badge Formatter',
                    'instructions_sk': (
                        "Napíš funkciu `formatuj_odznak(id_cislo, trieda, body)`, ktorá vráti reťazec v presnom tvare:\n"
                        "`\"ID-[0000] | TRIEDA: [TRIEDA] | BODY: [BODY.00]\"`.\n"
                        "Napr. pre `formatuj_odznak(7, \"iv.c\", 85.5)` vráti:\n"
                        "`\"ID-0007 | TRIEDA: IV.C | BODY: 85.50\"`."
                    ),
                    'instructions_en': 'Write `formatuj_odznak(id_cislo, trieda, body)` returning formatted student badge string.',
                    'starter_code': 'def formatuj_odznak(id_cislo, trieda, body):\n    pass\n',
                    'solution_code': 'def formatuj_odznak(id_cislo, trieda, body):\n    return f"ID-{id_cislo:04d} | TRIEDA: {trieda.upper()} | BODY: {body:.2f}"\n',
                    'explanation_sk': 'Využívame formátovače :04d pre ID, .upper() pre triedu a :.2f pre body.',
                    'explanation_en': 'Format specifiers :04d, :.2f combined with upper() string method.',
                    'hint_sk': 'Použi f"ID-{id_cislo:04d} | TRIEDA: {trieda.upper()} | BODY: {body:.2f}".',
                    'hint_en': 'Use f"ID-{id_cislo:04d} | TRIEDA: {trieda.upper()} | BODY: {body:.2f}".',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'formatuj_odznak(7, "iv.c", 85.5)', 'expected_output': 'ID-0007 | TRIEDA: IV.C | BODY: 85.50', 'test_code': 'assert formatuj_odznak(7, "iv.c", 85.5) == "ID-0007 | TRIEDA: IV.C | BODY: 85.50"', 'is_hidden': False},
                        {'input_data': 'formatuj_odznak(142, "iii.a", 100.0)', 'expected_output': 'ID-0142 | TRIEDA: III.A | BODY: 100.00', 'test_code': 'assert formatuj_odznak(142, "iii.a", 100.0) == "ID-0142 | TRIEDA: III.A | BODY: 100.00"', 'is_hidden': False},
                        {'input_data': 'formatuj_odznak(9999, "septima", 0.0)', 'expected_output': 'ID-9999 | TRIEDA: SEPTIMA | BODY: 0.00', 'test_code': 'assert formatuj_odznak(9999, "septima", 0.0) == "ID-9999 | TRIEDA: SEPTIMA | BODY: 0.00"', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
