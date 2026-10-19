"""
MODUL 3: Vetvenie programu a rozhodovacia logika
Odhadovaný rozsah: 10 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 3,
    'title_sk': 'Vetvenie programu a rozhodovacia logika',
    'title_en': 'Control Flow & Decision Logic',
    'description_sk': 'Nauč sa riadiť beh programu pomocou podmienok if, elif, else, vnorených podmienok, ternárneho operátora, konceptu Truthy/Falsy a konštrukcie match-case.',
    'description_en': 'Master code execution branching with if, elif, else statements, nested conditions, ternary operators, Truthy/Falsy evaluations, and modern match-case patterns.',
    'programming_language': 'python',
    'estimated_hours': 10,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'diagram-split',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Podmienka if a bloková štruktúra kódu (Indentation)',
            'title_en': 'The if Statement & Code Indentation Rules',
            'summary_sk': 'Syntax podmienky if, odsadenie 4 medzerami (PEP 8) a vykonávanie blokov kódu.',
            'summary_en': 'Syntax of if statement, PEP 8 4-space indentation standard, and block scopes.',
            'estimated_minutes': 45,
            'xp_reward': 25,
            'is_published': True,
            'content_sk': """### 3.1 Podmienka `if` a odsadenie kódu

V Pythone sa na ohraničenie blokov kódu nepoužívajú zložené zátvorky `{}` (ako v C++ či Java), ale **odsadenie (Indentation)**.

Podľa štandardu PEP 8 sa používa presne **4 medzery** na úroveň odsadenia.

```python
skore = 85

if skore >= 50:
    print("Test úspešne zvládnutý!")
    print("Získavaš odznak Codoro.")

print("Tento riadok sa vykoná vždy.")
```

Ak je výraz za `if` pravdivý (`True`), vykonajú sa všetky odsadené príkazy.
""",
            'content_en': """### 3.1 The if Statement & Code Indentation

Python enforces code blocks through strict indentation (4 spaces per level) instead of curly braces.

```python
score = 85
if score >= 50:
    print("Passed!")
```
""",
            'quizzes': [
                {
                    'question_sk': 'Akú chybu vyvolá Python, ak vynecháš odsadenie riadku pod podmienkou if?',
                    'question_en': 'What exception does Python raise when indentation is missing under an if statement?',
                    'option_a_sk': 'IndentationError', 'option_a_en': 'IndentationError',
                    'option_b_sk': 'SyntaxError', 'option_b_en': 'SyntaxError',
                    'option_c_sk': 'TypeError', 'option_c_en': 'TypeError',
                    'option_d_sk': 'ValueError', 'option_d_en': 'ValueError',
                    'correct_option': 'A',
                    'explanation_sk': 'Python striktne kontroluje štruktúru odsadenia a vyvolá špecifickú chybu IndentationError.',
                    'explanation_en': 'Python raises an IndentationError when block indentation is missing or inconsistent.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Kontrola plnoletosti hráča',
                    'title_en': 'Player Age Verification',
                    'instructions_sk': 'Napíš funkciu `moze_hrat_turnaj(vek)`, ktorá vráti reťazec `"POVOLENÉ"`, ak je vek aspoň 15 rokov. V opačnom prípade vráti `"ZAMIETNUTÉ"`.',
                    'instructions_en': 'Write a function `moze_hrat_turnaj(vek)` returning `"POVOLENÉ"` if age >= 15, else `"ZAMIETNUTÉ"`.',
                    'starter_code': 'def moze_hrat_turnaj(vek):\n    pass\n',
                    'solution_code': 'def moze_hrat_turnaj(vek):\n    if vek >= 15:\n        return "POVOLENÉ"\n    return "ZAMIETNUTÉ"\n',
                    'explanation_sk': 'Základná podmienka if s včasným návratom (Early Return).',
                    'explanation_en': 'Simple if statement combined with early return pattern.',
                    'hint_sk': 'Over `if vek >= 15: return "POVOLENÉ"` a inak vráť "ZAMIETNUTÉ".',
                    'hint_en': 'Check `if vek >= 15: return "POVOLENÉ"` otherwise return "ZAMIETNUTÉ".',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'moze_hrat_turnaj(15)', 'expected_output': 'POVOLENÉ', 'test_code': 'assert moze_hrat_turnaj(15) == "POVOLENÉ"', 'is_hidden': False},
                        {'input_data': 'moze_hrat_turnaj(14)', 'expected_output': 'ZAMIETNUTÉ', 'test_code': 'assert moze_hrat_turnaj(14) == "ZAMIETNUTÉ"', 'is_hidden': False},
                        {'input_data': 'moze_hrat_turnaj(20)', 'expected_output': 'POVOLENÉ', 'test_code': 'assert moze_hrat_turnaj(20) == "POVOLENÉ"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Dvojcestné a viaccestné vetvenie (if - elif - else)',
            'title_en': 'Multi-Way Branching (if - elif - else)',
            'summary_sk': 'Konštrukcia if-elif-else, poradie vyhodnocovania vetiev a predvolená vetva else.',
            'summary_en': 'The if-elif-else construct, cascading condition evaluation, and fallback else branch.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 3.2 Viaccestné vetvenie: `if - elif - else`

Keď máme viac než dva možné stavy, použijeme kľúčové slovo `elif` (skratka z *else if*).

```python
body = 78

if body >= 90:
    znamka = "A"
elif body >= 80:
    znamka = "B"
elif body >= 70:
    znamka = "C"
elif body >= 60:
    znamka = "D"
elif body >= 50:
    znamka = "E"
else:
    znamka = "Fx"
```

Dôležité: Vyhodnocuje sa zhora nadol. Hneď ako je prvá podmienka splnená, jej blok sa vykoná a všetky ďalšie vetvy `elif` a `else` sa preskočia!
""",
            'content_en': """### 3.2 Cascading Branching: `if - elif - else`

Multiple alternative branches are evaluated sequentially from top to bottom.

```python
if points >= 90:
    grade = "A"
elif points >= 80:
    grade = "B"
else:
    grade = "F"
```
""",
            'quizzes': [
                {
                    'question_sk': 'Koľko blokov `elif` môže nasledovať za jednou podmienkou `if`?',
                    'question_en': 'How many `elif` blocks can follow a single `if` statement?',
                    'option_a_sk': 'Maximálne 1', 'option_a_en': 'At most 1',
                    'option_b_sk': 'Maximálne 10', 'option_b_en': 'At most 10',
                    'option_c_sk': 'Ľubovoľný počet', 'option_c_en': 'Unlimited',
                    'option_d_sk': 'Presne toľko, koľko je kľúčových slov', 'option_d_en': 'Finite count',
                    'correct_option': 'C',
                    'explanation_sk': 'V Pythone môže za if nasledovať ľubovoľný počet vetiev elif.',
                    'explanation_en': 'An if block can have an arbitrary number of elif branches.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Klasifikátor školskej známky',
                    'title_en': 'School Grade Classifier',
                    'instructions_sk': (
                        "Napíš funkciu `urci_znamku(percenta)`, ktorá vráti známku ako celé číslo od 1 do 5:\n"
                        "- 90 % a viac: `1`\n"
                        "- 75 % až 89 %: `2`\n"
                        "- 60 % až 74 %: `3`\n"
                        "- 50 % až 59 %: `4`\n"
                        "- menej ako 50 %: `5`"
                    ),
                    'instructions_en': 'Write `urci_znamku(percenta)` returning an integer grade from 1 to 5.',
                    'starter_code': 'def urci_znamku(percenta):\n    pass\n',
                    'solution_code': 'def urci_znamku(percenta):\n    if percenta >= 90:\n        return 1\n    elif percenta >= 75:\n        return 2\n    elif percenta >= 60:\n        return 3\n    elif percenta >= 50:\n        return 4\n    else:\n        return 5\n',
                    'explanation_sk': 'Používame kaskádové porovnanie percentuálnych pásiem.',
                    'explanation_en': 'Sequentially evaluate upper percentage boundaries with elif.',
                    'hint_sk': 'Začni od 90 a pokračuj nadol: if percenta >= 90: return 1 ...',
                    'hint_en': 'Start from 90 downwards: if percenta >= 90: return 1 ...',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'urci_znamku(95)', 'expected_output': '1', 'test_code': 'assert urci_znamku(95) == 1', 'is_hidden': False},
                        {'input_data': 'urci_znamku(74)', 'expected_output': '3', 'test_code': 'assert urci_znamku(74) == 3', 'is_hidden': False},
                        {'input_data': 'urci_znamku(49)', 'expected_output': '5', 'test_code': 'assert urci_znamku(49) == 5', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Vnorené podmienky a zložité logické výrazy',
            'title_en': 'Nested Conditions & Complex Boolean Expressions',
            'summary_sk': 'Vnorenie if do iného if, eliminácia hlbokého vnorenia a zreťazené porovnania.',
            'summary_en': 'Nesting if statements, guard clauses refactoring, and chained comparisons in Python.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 3.3 Vnorené podmienky a zreťazené porovnania

V Pythone môžeme vložiť blok `if` do vnútra iného bloku `if`.

#### Zreťazené porovnanie (Python špecialita):
Namiesto `if x >= 0 and x <= 100:` môžeme v Pythone napísať elegantne:
```python
if 0 <= x <= 100:
    print("Číslo je v povolenom intervale 0-100")
```

#### Guard Clauses (Ochranné podmienky):
Namiesto hlbokého vnorenia (tzv. "Pyramid of Doom") je osvedčenou praxou overiť chybové stavy hneď na začiatku funkcie a ukončiť ju:

```python
def prihlasenie(meno, heslo):
    if not meno:
        return "Chýba meno"
    if len(heslo) < 8:
        return "Príliš krátke heslo"
    return "Prihlásený"
```
""",
            'content_en': """### 3.3 Nested Conditions & Chained Comparisons

Python supports mathematical chained comparisons like `0 <= x <= 100`. Guard clauses prevent nested pyramids of doom.
""",
            'quizzes': [
                {
                    'question_sk': 'Je výraz `10 < x < 20` v jazyku Python syntakticky platný?',
                    'question_en': 'Is the expression `10 < x < 20` syntactically valid in Python?',
                    'option_a_sk': 'Áno, je to zreťazené porovnanie ekvivalentné s (10 < x and x < 20)', 'option_a_en': 'Yes, it is equivalent to (10 < x and x < 20)',
                    'option_b_sk': 'Nie, Python vyžaduje zátvorky', 'option_b_en': 'No, requires parentheses',
                    'option_c_sk': 'Nie, musí sa použiť &&', 'option_c_en': 'No, must use &&',
                    'option_d_sk': 'Iba v Pythone 2', 'option_d_en': 'Only in Python 2',
                    'correct_option': 'A',
                    'explanation_sk': 'Python natívne podporuje reťazenie porovnávacích operátorov podľa matematického zápisu.',
                    'explanation_en': 'Python natively supports chained comparison operators.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Validátor hesla s bezpečnostnými pravidlami',
                    'title_en': 'Password Policy Validator',
                    'instructions_sk': (
                        "Napíš funkciu `validuj_heslo(heslo)`, ktorá vráti `True`, len ak heslo spĺňa:\n"
                        "1. Dĺžku aspoň 8 znakov (`len(heslo) >= 8`).\n"
                        "2. Obsahuje aspoň jednu číslicu (over pomocou `any(c.isdigit() for c in heslo)`).\n"
                        "3. Neobsahuje medzeru (`' ' not in heslo`).\n"
                        "Inak vráti `False`."
                    ),
                    'instructions_en': 'Write `validuj_heslo(heslo)` returning `True` if length >= 8, has digit, and has no space.',
                    'starter_code': 'def validuj_heslo(heslo):\n    pass\n',
                    'solution_code': 'def validuj_heslo(heslo):\n    if len(heslo) < 8:\n        return False\n    if " " in heslo:\n        return False\n    if not any(c.isdigit() for c in heslo):\n        return False\n    return True\n',
                    'explanation_sk': 'Používame guard clauses pre každé porušené pravidlo.',
                    'explanation_en': 'Implement guard clauses checking length, whitespace, and digit presence.',
                    'hint_sk': 'Použi len(heslo) >= 8 and (" " not in heslo) and any(c.isdigit() for c in heslo).',
                    'hint_en': 'Use len(heslo) >= 8 and (" " not in heslo) and any(c.isdigit() for c in heslo).',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'validuj_heslo("Heslo123")', 'expected_output': 'True', 'test_code': 'assert validuj_heslo("Heslo123") is True', 'is_hidden': False},
                        {'input_data': 'validuj_heslo("kratke1")', 'expected_output': 'False', 'test_code': 'assert validuj_heslo("kratke1") is False', 'is_hidden': False},
                        {'input_data': 'validuj_heslo("Heslo Bez Cislic")', 'expected_output': 'False', 'test_code': 'assert validuj_heslo("Heslo Bez Cislic") is False', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Ternárny operátor a pravdivostné hodnoty (Truthy / Falsy)',
            'title_en': 'Ternary Operator & Truthy/Falsy Evaluation',
            'summary_sk': 'Jednoriadkový if-else ternárny výraz a čo všetko sa vyhodnotí ako nepravda v Pythone.',
            'summary_en': 'One-line conditional expressions (ternary operator) and Python truth value testing rules.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 3.4 Ternárny operátor a Truthy / Falsy

#### Ternárny operátor (podmienený výraz)
Umožňuje zapísať jednoduché priradenie na základe podmienky do jedného riadku:

```python
# Syntax: hodnota_ak_true if podmienka else hodnota_ak_false
stav = "Plnoletý" if vek >= 18 else "Maloletý"
```

#### Pravdivostné hodnoty objektov (Truthy vs. Falsy)
V Pythone má každý objekt prirodzenú pravdivostnú hodnotu. Nasledujúce hodnoty sa v podmienke vyhodnotia ako **False (Falsy)**:
- `None`
- `False`
- Číselná nula: `0`, `0.0`
- Prázdne postupnosti a kolekcie: `""`, `[]`, `()`, `{}`

Všetky ostatné hodnoty (čísla rôzne od nuly, neprázdne texty, zoznamy) sú **True (Truthy)**!

```python
meno = "Codo"
if meno:  # Ekvivalent if len(meno) > 0:
    print(f"Ahoj {meno}")
```
""",
            'content_en': """### 3.4 Ternary Operator & Truthy/Falsy

```python
status = "Admin" if is_admin else "User"
```

Falsy values in Python: `None`, `False`, `0`, `""`, `[]`, `{}`, `()`. Everything else is Truthy.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá z nasledujúcich hodnôt sa v podmienke `if hodnota:` vyhodnotí ako True?',
                    'question_en': 'Which of the following evaluates to True in an `if value:` check?',
                    'option_a_sk': '"" (prázdny reťazec)', 'option_a_en': '"" (empty string)',
                    'option_b_sk': '0', 'option_b_en': '0',
                    'option_c_sk': '"0" (reťazec obsahujúci znak nuly)', 'option_c_en': '"0" (string containing zero)',
                    'option_d_sk': 'None', 'option_d_en': 'None',
                    'correct_option': 'C',
                    'explanation_sk': '"0" je neprázdny reťazec, preto je Truthy (vyhodnotí sa na True).',
                    'explanation_en': '"0" is a non-empty string and therefore evaluates as Truthy.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Jednoriadkový status používateľa',
                    'title_en': 'Inline User Status Formatter',
                    'instructions_sk': 'Napíš funkciu `formatuj_stav_uctu(doros, je_pro)`, ktorá pomocou ternárneho operátora vráti `"VIP"` ak `je_pro` je `True`, inak vráti `"BOHÁČ"` ak má aspoň 1000 Doros, inak vráti `"ŠTANDARD"`.',
                    'instructions_en': 'Write `formatuj_stav_uctu(doros, je_pro)` returning `"VIP"`, `"BOHÁČ"`, or `"ŠTANDARD"`.',
                    'starter_code': 'def formatuj_stav_uctu(doros, je_pro):\n    pass\n',
                    'solution_code': 'def formatuj_stav_uctu(doros, je_pro):\n    return "VIP" if je_pro else ("BOHÁČ" if doros >= 1000 else "ŠTANDARD")\n',
                    'explanation_sk': 'Zreťazený ternárny výraz v jednom riadku.',
                    'explanation_en': 'Chained ternary expressions for compact categorical classification.',
                    'hint_sk': 'Použi: "VIP" if je_pro else ("BOHÁČ" if doros >= 1000 else "ŠTANDARD").',
                    'hint_en': 'Use: "VIP" if je_pro else ("BOHÁČ" if doros >= 1000 else "ŠTANDARD").',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'formatuj_stav_uctu(500, True)', 'expected_output': 'VIP', 'test_code': 'assert formatuj_stav_uctu(500, True) == "VIP"', 'is_hidden': False},
                        {'input_data': 'formatuj_stav_uctu(1500, False)', 'expected_output': 'BOHÁČ', 'test_code': 'assert formatuj_stav_uctu(1500, False) == "BOHÁČ"', 'is_hidden': False},
                        {'input_data': 'formatuj_stav_uctu(300, False)', 'expected_output': 'ŠTANDARD', 'test_code': 'assert formatuj_stav_uctu(300, False) == "ŠTANDARD"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Porovnávanie vzorov match-case a zhrnutie modulu',
            'title_en': 'Structural Pattern Matching (match-case) & Summary',
            'summary_sk': 'Moderná syntax match-case zavedená v Pythone 3.10 a záverečný komplexný projekt.',
            'summary_en': 'Structural pattern matching with match-case (Python 3.10+) and module capstone exercise.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 3.5 Štrukturálne porovnávanie vzorov: `match - case`

Od verzie Python 3.10 je k dispozícii moderná konštrukcia `match - case` (obdoba `switch - case` z iných jazykov, no s podporou pokročilého pattern matchingu).

```python
http_status = 404

match http_status:
    case 200:
        sprava = "OK"
    case 400:
        sprava = "Bad Request"
    case 404:
        sprava = "Not Found"
    case 500:
        sprava = "Server Error"
    case _:
        sprava = "Neznámy kód"  # Podtržník _ funguje ako predvolený default
```
""",
            'content_en': """### 3.5 Structural Pattern Matching (match-case)

Python 3.10 introduced `match - case`:

```python
match command:
    case "start":
        run()
    case _:
        fallback()
```
""",
            'quizzes': [
                {
                    'question_sk': 'Akú úlohu plní podčiarkovník `_` vo vetve `case _:`?',
                    'question_en': 'What role does underscore `_` play in a `case _:` branch?',
                    'option_a_sk': 'Predvolená vetva (Wildcard / Default fallback), ak sa žiadny vzor nezhoduje', 'option_a_en': 'Default wildcard match',
                    'option_b_sk': 'Vyvolá výnimku', 'option_b_en': 'Raises an error',
                    'option_c_sk': 'Odkazuje na premennú _', 'option_c_en': 'References variable _',
                    'option_d_sk': 'Ukončí interpret Pythonu', 'option_d_en': 'Terminates python',
                    'correct_option': 'A',
                    'explanation_sk': 'Podčiarkovník v konštrukcii match-case slúži ako univerzálny zástupný znak (wildcard) pre defaultnú vetvu.',
                    'explanation_en': 'The wildcard pattern `_` acts as default fallback when no previous cases match.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Parser príkazov herného robota',
                    'title_en': 'Game Bot Command Parser',
                    'instructions_sk': (
                        "Napíš funkciu `spracuj_prikaz(prikaz)`, ktorá podľa reťazca vráti:\n"
                        "- `'SEVER'`, `'JUH'`, `'VYCHOD'`, `'ZAPAD'` -> vráti `'POHYB'`\n"
                        "- `'UTOK'`, `'OBRANA'` -> vráti `'BOJ'`\n"
                        "- `'INVENTAR'`, `'STATUS'` -> vráti `'INFO'`\n"
                        "- akýkoľvek iný príkaz -> vráti `'NEZNÁMY PRÍKAZ'`\n"
                        "Vstupný príkaz neošetruj na veľkosť písmen manuálne, použi `.upper()`."
                    ),
                    'instructions_en': 'Write `spracuj_prikaz(prikaz)` mapping direction, combat, info commands, or returning `"NEZNÁMY PRÍKAZ"`.',
                    'starter_code': 'def spracuj_prikaz(prikaz):\n    pass\n',
                    'solution_code': 'def spracuj_prikaz(prikaz):\n    cmd = prikaz.strip().upper()\n    match cmd:\n        case "SEVER" | "JUH" | "VYCHOD" | "ZAPAD":\n            return "POHYB"\n        case "UTOK" | "OBRANA":\n            return "BOJ"\n        case "INVENTAR" | "STATUS":\n            return "INFO"\n        case _:\n            return "NEZNÁMY PRÍKAZ"\n',
                    'explanation_sk': 'Používame match-case so zjednotením vzorov cez zvislú čiaru | (or vzory).',
                    'explanation_en': 'Using match-case with multi-pattern OR syntax `|` and `case _:` default.',
                    'hint_sk': 'Použi match cmd: case "SEVER" | "JUH" ...',
                    'hint_en': 'Use match cmd: case "SEVER" | "JUH" ...',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'spracuj_prikaz("sever")', 'expected_output': 'POHYB', 'test_code': 'assert spracuj_prikaz("sever") == "POHYB"', 'is_hidden': False},
                        {'input_data': 'spracuj_prikaz("UTOK")', 'expected_output': 'BOJ', 'test_code': 'assert spracuj_prikaz("UTOK") == "BOJ"', 'is_hidden': False},
                        {'input_data': 'spracuj_prikaz("inventar")', 'expected_output': 'INFO', 'test_code': 'assert spracuj_prikaz("inventar") == "INFO"', 'is_hidden': False},
                        {'input_data': 'spracuj_prikaz("skoc")', 'expected_output': 'NEZNÁMY PRÍKAZ', 'test_code': 'assert spracuj_prikaz("skoc") == "NEZNÁMY PRÍKAZ"', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
