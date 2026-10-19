"""
MODUL 8: Ošetrovanie výnimiek, ladenie kódu a spracovanie súborov
Odhadovaný rozsah: 10 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 8,
    'title_sk': 'Ošetrovanie výnimiek, ladenie kódu a dátové prúdy',
    'title_en': 'Exception Handling, Code Debugging & Data Streams',
    'description_sk': 'Osvoj si profesionálne ošetrovanie chýb: rozdiely medzi syntaxou a runtime výnimkami, bloky try-except-else-finally, príkaz raise pre defenzívne programovanie a parsovanie CSV/log dát v pamäti.',
    'description_en': 'Master error handling: syntax vs runtime exceptions, try-except-else-finally blocks, custom exception raising, defensive input validation, and in-memory CSV/log data stream parsing.',
    'programming_language': 'python',
    'estimated_hours': 10,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'shield-check',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Syntaktické chyby vs. behové výnimky (Exceptions)',
            'title_en': 'Syntax Errors vs Runtime Exceptions',
            'summary_sk': 'Chyby pri parsovaní (SyntaxError), bežné behové výnimky: ValueError, TypeError, IndexError, KeyError, ZeroDivisionError.',
            'summary_en': 'Parse-time errors vs runtime exceptions: ValueError, TypeError, IndexError, KeyError, ZeroDivisionError.',
            'estimated_minutes': 45,
            'xp_reward': 25,
            'is_published': True,
            'content_sk': """### 8.1 Druhy chýb v Pythone

Chyby v programe delíme do dvoch hlavných kategórií:
1. **Syntaktické chyby (`SyntaxError`)**: Nastanú ešte pred spustením kódu, keď parser nerozumie zápisu (napr. chýbajúca dvojbodka `:` alebo neuzavretá zátvorka). Tieto chyby nemožno zachytiť cez `try-except`.
2. **Behové výnimky (Runtime Exceptions)**: Nastanú počas vykonávania kódu, keď je syntax v poriadku, ale operácia je neplatná:

| Výnimka | Príčina |
|---|---|
| `ZeroDivisionError` | Delenie nulou (`10 / 0`) |
| `ValueError` | Správny typ, ale neplatná hodnota (`int("abc")`) |
| `TypeError` | Neplatný dátový typ pre operáciu (`"text" + 5`) |
| `IndexError` | Prístup k neexistujúcemu indexu v zozname (`zoznam[99]`) |
| `KeyError` | Hľadanie neexistujúceho kľúča v slovníku (`d["neznámy"]`) |
""",
            'content_en': """### 8.1 Errors in Python

- `SyntaxError` occurs at compile-time when syntax is malformed.
- Runtime exceptions (`ValueError`, `TypeError`, `ZeroDivisionError`, `IndexError`, `KeyError`) halt execution unless caught.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá výnimka nastane pri pokuse vykonať `"5" + 10`?',
                    'question_en': 'Which exception is raised by `"5" + 10`?',
                    'option_a_sk': 'TypeError', 'option_a_en': 'TypeError',
                    'option_b_sk': 'ValueError', 'option_b_en': 'ValueError',
                    'option_c_sk': 'SyntaxError', 'option_c_en': 'SyntaxError',
                    'option_d_sk': 'ArithmeticError', 'option_d_en': 'ArithmeticError',
                    'correct_option': 'A',
                    'explanation_sk': 'Python nepodporuje implicitné sčítanie reťazca a čísla, preto vyvolá TypeError.',
                    'explanation_en': 'Incompatible types for operator + raises TypeError in Python.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Bezpečný konvertor čísel (Safe Int Parser)',
                    'title_en': 'Safe Integer Parser',
                    'instructions_sk': (
                        "Napíš funkciu `bezpecne_cele_cislo(text_hodnota, predvolena=0)`, ktorá sa pokúsi previesť `text_hodnota` na `int` pomocou `try-except`.\n"
                        "Ak nastane `(ValueError, TypeError)`, funkcia nezhavaruje, ale vráti hodnotu `predvolena`."
                    ),
                    'instructions_en': 'Write `bezpecne_cele_cislo(text_hodnota, predvolena=0)` parsing text to int safely with fallback.',
                    'starter_code': 'def bezpecne_cele_cislo(text_hodnota, predvolena=0):\n    pass\n',
                    'solution_code': 'def bezpecne_cele_cislo(text_hodnota, predvolena=0):\n    try:\n        return int(text_hodnota)\n    except (ValueError, TypeError):\n        return predvolena\n',
                    'explanation_sk': 'Využívame try-except pre ValueError a TypeError.',
                    'explanation_en': 'Catch both ValueError and TypeError returning fallback default.',
                    'hint_sk': 'try: return int(text_hodnota); except (ValueError, TypeError): return predvolena.',
                    'hint_en': 'try: return int(text_hodnota); except (ValueError, TypeError): return predvolena.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'bezpecne_cele_cislo("42")', 'expected_output': '42', 'test_code': 'assert bezpecne_cele_cislo("42") == 42', 'is_hidden': False},
                        {'input_data': 'bezpecne_cele_cislo("nie_je_cislo", 99)', 'expected_output': '99', 'test_code': 'assert bezpecne_cele_cislo("nie_je_cislo", 99) == 99', 'is_hidden': False},
                        {'input_data': 'bezpecne_cele_cislo(None, -1)', 'expected_output': '-1', 'test_code': 'assert bezpecne_cele_cislo(None, -1) == -1', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Zachytávanie výnimiek: try - except - else - finally',
            'title_en': 'Exception Handling: try - except - else - finally',
            'summary_sk': 'Štvorbloková štruktúra ošetrenia výnimiek, vetva else po úspechu, vetva finally pre cleanup.',
            'summary_en': 'Four-clause try-except-else-finally architecture and deterministic cleanup.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 8.2 Bloky `try - except - else - finally`

Pre robustné aplikácie ponúka Python kompletnú štvorblokovú štruktúru:

```python
try:
    # 1. Kód, ktorý môže vyvolať výnimku
    vysledok = a / b
except ZeroDivisionError as e:
    # 2. Vykoná sa LEN vtedy, ak nastala chyba
    print("Chyba: delenie nulou!")
else:
    # 3. Vykoná sa LEN vtedy, ak ŽIADNA chyba nenastala
    print(f"Výpočet úspešný: {vysledok}")
finally:
    # 4. Vykoná sa VŽDY (aj pri chybe, aj pri úspechu, aj pred returnom!)
    print("Upratovanie zdrojov (cleanup) dokončené.")
```
""",
            'content_en': """### 8.2 The try-except-else-finally Construct

- `try` runs monitored code
- `except` catches specific errors
- `else` runs only if no error occurred
- `finally` always runs regardless of outcome
""",
            'quizzes': [
                {
                    'question_sk': 'Kedy sa vykoná blok `finally:` v konštrukcii ošetrenia výnimiek?',
                    'question_en': 'When does the `finally:` block execute?',
                    'option_a_sk': 'Vždy, bez ohľadu na to, či výnimka nastala alebo nie', 'option_a_en': 'Always, regardless of whether an exception occurred',
                    'option_b_sk': 'Iba ak nastala výnimka', 'option_b_en': 'Only on exception',
                    'option_c_sk': 'Iba ak nenastala výnimka', 'option_c_en': 'Only if no exception',
                    'option_d_sk': 'Iba ak je v kóde return 0', 'option_d_en': 'Only on return 0',
                    'correct_option': 'A',
                    'explanation_sk': 'finally sa vykoná vždy – slúži na garantované zatvorenie súborov či sieťových spojení.',
                    'explanation_en': 'The finally clause is guaranteed to execute during exit.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Bezpečný kalkulátor delenia so stavovým kódom',
                    'title_en': 'Safe Division with Status Code',
                    'instructions_sk': (
                        "Napíš funkciu `bezpecne_delenie(a, b)`, ktorá sa pokúsi vydeliť $a / b$:\n"
                        "- Pri úspechu vráti dvojicu `(round(a / b, 2), \"OK\")`.\n"
                        "- Pri `ZeroDivisionError` vráti `(None, \"ZERO_DIVISION\")`.\n"
                        "- Pri `TypeError` vráti `(None, \"INVALID_TYPE\")`."
                    ),
                    'instructions_en': 'Write `bezpecne_delenie(a, b)` returning tuple (result, status) handling ZeroDivisionError and TypeError.',
                    'starter_code': 'def bezpecne_delenie(a, b):\n    pass\n',
                    'solution_code': 'def bezpecne_delenie(a, b):\n    try:\n        res = a / b\n        return (round(res, 2), "OK")\n    except ZeroDivisionError:\n        return (None, "ZERO_DIVISION")\n    except TypeError:\n        return (None, "INVALID_TYPE")\n',
                    'explanation_sk': 'Dve samostatné vetvy except pre špecifické ošetrenie delenia nulou a neplatného typu.',
                    'explanation_en': 'Separate except handlers returning structured tuple statuses.',
                    'hint_sk': 'try: return (round(a/b, 2), "OK"); except ZeroDivisionError: return (None, "ZERO_DIVISION"); except TypeError: return (None, "INVALID_TYPE").',
                    'hint_en': 'Handle ZeroDivisionError and TypeError with corresponding string codes.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'bezpecne_delenie(10, 2)', 'expected_output': '(5.0, "OK")', 'test_code': 'assert bezpecne_delenie(10, 2) == (5.0, "OK")', 'is_hidden': False},
                        {'input_data': 'bezpecne_delenie(10, 0)', 'expected_output': '(None, "ZERO_DIVISION")', 'test_code': 'assert bezpecne_delenie(10, 0) == (None, "ZERO_DIVISION")', 'is_hidden': False},
                        {'input_data': 'bezpecne_delenie("10", 2)', 'expected_output': '(None, "INVALID_TYPE")', 'test_code': 'assert bezpecne_delenie("10", 2) == (None, "INVALID_TYPE")', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Vyvolanie výnimky príkazom raise a defenzívna validácia',
            'title_en': 'Raising Exceptions (raise) & Defensive Validation',
            'summary_sk': 'Explicitné vyvolanie výnimky cez raise ValueError, validácia argumentov na začiatku funkcie.',
            'summary_en': 'Raising custom exceptions using raise, fail-fast defensive coding, and precondition assertion.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 8.3 Vyvolanie výnimiek príkazom `raise`

Pri tvorbe knižníc a backendu (napr. Django modelov) nechceme dovoliť spracovanie neplatných dát. Príkaz `raise` umožňuje vývojárovi explicitne signalizovať chybu:

```python
def nastav_vek(vek):
    if not isinstance(vek, int):
        raise TypeError("Vek musí byť celé číslo!")
    if vek < 0 or vek > 120:
        raise ValueError(f"Neplatný vek: {vek}. Musí byť v rozsahu 0-120.")
    return vek
```
Tomuto prístupu hovoríme **Fail-Fast** – program odhalí chybu okamžite na mieste vzniku, skôr než spôsobí tiché poškodenie databázy.
""",
            'content_en': """### 8.3 Raising Exceptions & Defensive Validation

Fail-fast architecture uses `raise ValueError(...)` to catch invalid inputs immediately.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktoré kľúčové slovo v Pythone slúži na manuálne vyvolanie výnimky?',
                    'question_en': 'Which Python keyword is used to manually trigger an exception?',
                    'option_a_sk': 'raise', 'option_a_en': 'raise',
                    'option_b_sk': 'throw', 'option_b_en': 'throw',
                    'option_c_sk': 'error', 'option_c_en': 'error',
                    'option_d_sk': 'catch', 'option_d_en': 'catch',
                    'correct_option': 'A',
                    'explanation_sk': 'V jazyku Python sa používa kľúčové slovo raise (v jazykoch ako Java či JavaScript je to throw).',
                    'explanation_en': 'Python uses raise to throw exceptions.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Validácia registrácie používateľa',
                    'title_en': 'User Registration Preconditions',
                    'instructions_sk': (
                        "Napíš funkciu `validuj_registraciu(meno, vek, email)`:\n"
                        "1. Ak `meno` nie je typu `str` alebo je prázdne po očistení medzier, vyvolaj `ValueError(\"Chybné meno\")`.\n"
                        "2. Ak `vek < 13`, vyvolaj `ValueError(\"Minimálny vek je 13\")`.\n"
                        "3. Ak v `email` chýba znak `'@'`, vyvolaj `ValueError(\"Neplatný email\")`.\n"
                        "4. Ak sú všetky údaje platné, vráti `True`."
                    ),
                    'instructions_en': 'Write `validuj_registraciu(meno, vek, email)` raising ValueError with descriptive messages or returning True.',
                    'starter_code': 'def validuj_registraciu(meno, vek, email):\n    pass\n',
                    'solution_code': 'def validuj_registraciu(meno, vek, email):\n    if not isinstance(meno, str) or not meno.strip():\n        raise ValueError("Chybné meno")\n    if vek < 13:\n        raise ValueError("Minimálny vek je 13")\n    if "@" not in email:\n        raise ValueError("Neplatný email")\n    return True\n',
                    'explanation_sk': 'Defenzívna validácia vstupov s vyvolaním ValueError.',
                    'explanation_en': 'Defensive input checking raising ValueError on contract violations.',
                    'hint_sk': 'Over podmienky postupne a použi raise ValueError("...").',
                    'hint_en': 'Validate each field sequentially and raise ValueError on error.',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'validuj_registraciu("Juraj", 18, "juraj@codoro.sk")', 'expected_output': 'True', 'test_code': 'assert validuj_registraciu("Juraj", 18, "juraj@codoro.sk") is True', 'is_hidden': False},
                        {'input_data': 'validuj_registraciu("", 18, "a@b.com")', 'expected_output': 'ValueError', 'test_code': 'try:\n    validuj_registraciu("", 18, "a@b.com")\n    assert False, "Malo vyvolať ValueError"\nexcept ValueError as e:\n    assert "meno" in str(e).lower()', 'is_hidden': False},
                        {'input_data': 'validuj_registraciu("Martin", 10, "m@b.com")', 'expected_output': 'ValueError', 'test_code': 'try:\n    validuj_registraciu("Martin", 10, "m@b.com")\n    assert False\nexcept ValueError:\n    pass', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Práca s dátovými prúdmi a parsovanie CSV/log dát v pamäti',
            'title_en': 'Data Streams & In-Memory CSV/Log Parsing',
            'summary_sk': 'Spracovanie riadkov textu, čistenie CSV záznamov bez nutnosti diskového I/O a záverečný projekt.',
            'summary_en': 'Stream text parsing, tokenization, CSV record extraction, and module capstone challenge.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 8.4 Spracovanie CSV a dátových prúdov

V dátovom inžinierstve a webovom vývoji často spracovávame viacriadkový textový prúd (napr. export z databázy alebo serverový log).

```python
csv_data = \"\"\"id,meno,doros
1,Juraj,350
2,Martin,520
3,Petra,410\"\"\"

riadky = csv_data.strip().split("\\n")
hlavicka = riadky[0].split(",")
for r in riadky[1:]:
    hodnoty = r.split(",")
    print(f"Študent {hodnoty[1]} má {hodnoty[2]} Doros")
```
""",
            'content_en': """### 8.4 In-Memory CSV & Stream Parsing

Processing multiline text feeds by splitting lines, tokenizing commas, and transforming into structured data.
""",
            'quizzes': [
                {
                    'question_sk': 'Akým spôsobom rozdelíme viacriadkový reťazec v Pythone na zoznam jednotlivých riadkov?',
                    'question_en': 'How do you split a multiline string into a list of lines in Python?',
                    'option_a_sk': 'text.splitlines() alebo text.split("\\n")', 'option_a_en': 'text.splitlines() or text.split("\\n")',
                    'option_b_sk': 'text.readlines()', 'option_b_en': 'text.readlines()',
                    'option_c_sk': 'text.to_lines()', 'option_c_en': 'text.to_lines()',
                    'option_d_sk': 'list(text)', 'option_d_en': 'list(text)',
                    'correct_option': 'A',
                    'explanation_sk': 'Metóda splitlines() alebo split("\\n") rozdelí text na riadky.',
                    'explanation_en': 'splitlines() handles universal newlines across operating systems.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'CSV Parsér transakcií v pamäti',
                    'title_en': 'In-Memory CSV Transaction Parser',
                    'instructions_sk': (
                        "Napíš funkciu `spocitaj_csv_doros(csv_text)`:\n"
                        "Vstupom je viacriadkový reťazec v tvare:\n"
                        "`\"id,student,amount\\n1,juraj,50\\n2,martin,100\\n3,juraj,-20\"`\n"
                        "Funkcia vráti celkový súčet stĺpca `amount` (kladné aj záporné hodnoty) ako celé číslo `int`.\n"
                        "Prvý riadok (hlavičku) preskoč. Chybné alebo prázdne riadky ignoruj."
                    ),
                    'instructions_en': 'Write `spocitaj_csv_doros(csv_text)` summing the integer amount column from in-memory CSV text.',
                    'starter_code': 'def spocitaj_csv_doros(csv_text):\n    pass\n',
                    'solution_code': 'def spocitaj_csv_doros(csv_text):\n    celkovo = 0\n    riadky = csv_text.strip().splitlines()\n    for r in riadky[1:]:\n        casti = r.strip().split(",")\n        if len(casti) == 3:\n            try:\n                celkovo += int(casti[2])\n            except ValueError:\n                pass\n    return celkovo\n',
                    'explanation_sk': 'Rozdelíme text na riadky, preskočíme hlavičku a bezpečne sčítame tretí stĺpec.',
                    'explanation_en': 'Split textlines, slice past header, safely parse third column to int with ValueError catch.',
                    'hint_sk': 'riadky = csv_text.strip().splitlines(); for r in riadky[1:]: celkovo += int(r.split(",")[2]).',
                    'hint_en': 'Iterate lines skipping header, split by comma, accumulate int(col[2]).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'spocitaj_csv_doros("id,student,amount\\n1,juraj,50\\n2,martin,100\\n3,juraj,-20")', 'expected_output': '130', 'test_code': 'assert spocitaj_csv_doros("id,student,amount\\n1,juraj,50\\n2,martin,100\\n3,juraj,-20") == 130', 'is_hidden': False},
                        {'input_data': 'spocitaj_csv_doros("id,student,amount")', 'expected_output': '0', 'test_code': 'assert spocitaj_csv_doros("id,student,amount") == 0', 'is_hidden': False},
                        {'input_data': 'spocitaj_csv_doros("id,student,amount\\n1,a,10\\n2,b,invalid\\n3,c,40")', 'expected_output': '50', 'test_code': 'assert spocitaj_csv_doros("id,student,amount\\n1,a,10\\n2,b,invalid\\n3,c,40") == 50', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
