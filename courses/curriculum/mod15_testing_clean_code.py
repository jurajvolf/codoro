"""
MODUL 15: Automatizované testovanie softvéru (assert, unittest, TDD) a čistý kód
Odhadovaný rozsah: 10 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU | Track: ALGORITHMS_AND_DATA
"""

MODULE_DATA = {
    'order': 15,
    'track': 'ALGORITHMS_AND_DATA',
    'title_sk': 'Automatizované testovanie softvéru (assert, unittest, TDD) a čistý kód',
    'title_en': 'Automated Software Testing (assert, unittest, TDD) & Clean Code',
    'description_sk': 'Princípy profesionálneho testovania v Pythone: príkaz assert, vstavaný rámec unittest, testovacie prípady TestCase, metodológia Test-Driven Development (TDD), odhaľovanie hraničných stavov (Edge Cases) a štandard PEP 8.',
    'description_en': 'Professional Python testing practices: the assert statement, unittest framework, TestCase assertions, Test-Driven Development (TDD) lifecycle, boundary edge case testing, and PEP 8 clean code.',
    'programming_language': 'python',
    'estimated_hours': 10,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'check-circle',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Príkaz assert a základy unit testovania',
            'title_en': 'The assert Statement & Unit Testing Basics',
            'summary_sk': 'Syntax príkazu assert, AssertionError, overovanie predpokladov a invariantov.',
            'summary_en': 'Syntax of assert, AssertionError, verifying preconditions and class invariants.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 15.1 Príkaz `assert` v Pythone

Základným stavebným kameňom overovania kódu v Pythone je kľúčové slovo `assert`.

#### Syntax:
```python
assert podmienka, "Chybová správa pri nesplnení podmienky"
```
Ak je podmienka `True`, program pokračuje bez prerušenia. Ak je podmienka `False`, Python okamžite vyvolá výnimku `AssertionError`.

#### Praktické využitie:
```python
def vypocitaj_dph(cena, sadzba=20):
    assert cena >= 0, "Cena nemôže byť záporná"
    assert 0 <= sadzba <= 100, "Sadzba DPH musí byť medzi 0 a 100 %"
    return round(cena * (sadzba / 100), 2)
```

> **Častá chyba v praxi:**
> Písanie zátvoriek okolo assert výrazu: `assert(cena >= 0, "Chyba")`. V Pythone nie je assert funkcia, ale príkaz! Dvojica v zátvorkách vytvorí neprázdnu n-ticu `tuple`, ktorá sa v booleovskom kontexte **vždy vyhodnotí ako True**, takže test nikdy nezlyhá! Správne: `assert podmienka, sprava` (bez vonkajších zátvoriek).
""",
            'content_en': """### 15.1 The assert Statement

Assert checks conditions and raises `AssertionError` if false. Never put parentheses around the statement.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo sa stane, ak napíšete `assert (x > 0, "Chyba")` so zátvorkami okolo oboch argumentov?',
                    'question_en': 'What happens if you write `assert (x > 0, "Error")` with parentheses around both arguments?',
                    'option_a_sk': 'Výraz sa vyhodnotí ako neprázdna n-tica (tuple), ktorá je vždy pravdivá (True), takže test nikdy neodhalí chybu', 'option_a_en': 'It evaluates as a non-empty tuple which is always True, meaning it never catches errors',
                    'option_b_sk': 'Python vyvolá SyntaxError', 'option_b_en': 'Python raises SyntaxError',
                    'option_c_sk': 'Je to odporúčaný zápis podľa PEP 8', 'option_c_en': 'Recommended by PEP 8',
                    'option_d_sk': 'Assert sa automaticky vypne', 'option_d_en': 'Assert disables itself',
                    'correct_option': 'A',
                    'explanation_sk': 'V Pythone je assert príkaz, nie funkcia. Zátvorky vytvoria n-ticu (bool, str), ktorá je ako pravdivá.',
                    'explanation_en': 'Parentheses construct a tuple which evaluates to truthy.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Overenie nezápornosti vkladu',
                    'title_en': 'Assert Non-Negative Deposit',
                    'instructions_sk': 'Napíš funkciu `vloz_peniaze(aktualny_zostatok, vklad)`, ktorá pomocou `assert vklad > 0, "Vklad musí byť kladný"` overí výšku vkladu a vráti nový zostatok `aktualny_zostatok + vklad`.',
                    'instructions_en': 'Write function `vloz_peniaze(aktualny_zostatok, vklad)` asserting positive deposit and returning updated balance.',
                    'starter_code': 'def vloz_peniaze(aktualny_zostatok, vklad):\n    # Over vklad cez assert a vráť zostatok\n    pass\n',
                    'solution_code': (
                        'def vloz_peniaze(aktualny_zostatok, vklad):\n'
                        '    assert vklad > 0, "Vklad musí byť kladný"\n'
                        '    return aktualny_zostatok + vklad\n'
                    ),
                    'explanation_sk': 'Použili sme assert na overenie kladného vkladu.',
                    'explanation_en': 'Asserted positive deposit and returned updated balance.',
                    'hint_sk': 'Použi assert vklad > 0, "Vklad musí byť kladný".',
                    'hint_en': 'Assert vklad > 0.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vloz_peniaze(100, 50)', 'expected_output': '150', 'test_code': 'assert vloz_peniaze(100, 50) == 150', 'is_hidden': False},
                        {
                            'input_data': 'vloz_peniaze(100, -10)',
                            'expected_output': 'AssertionError',
                            'test_code': (
                                'try:\n'
                                '    vloz_peniaze(100, -10)\n'
                                '    assert False, "Mala nastať AssertionError"\n'
                                'except AssertionError:\n'
                                '    pass\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Bezpečný podiel dvoch čísel',
                    'title_en': 'Safe Division with Precondition',
                    'instructions_sk': 'Napíš funkciu `bezpecny_podiel(delenec, delitel)`, ktorá pomocou `assert delitel != 0, "Deliteľ nesmie byť nula"` overí deliteľ a vráti podiel `delenec / delitel` zaokrúhlený na 4 desatinné miesta.',
                    'instructions_en': 'Write function `bezpecny_podiel(delenec, delitel)` asserting non-zero denominator and returning rounded quotient.',
                    'starter_code': 'def bezpecny_podiel(delenec, delitel):\n    # Over deliteľa cez assert\n    pass\n',
                    'solution_code': (
                        'def bezpecny_podiel(delenec, delitel):\n'
                        '    assert delitel != 0, "Deliteľ nesmie byť nula"\n'
                        '    return round(delenec / delitel, 4)\n'
                    ),
                    'explanation_sk': 'Použili sme assert delitel != 0 a funkciu round.',
                    'explanation_en': 'Asserted delitel != 0 and rounded.',
                    'hint_sk': 'Použi assert delitel != 0 a round(delenec / delitel, 4).',
                    'hint_en': 'Assert denominator is non-zero.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'bezpecny_podiel(10, 2)', 'expected_output': '5.0', 'test_code': 'assert bezpecny_podiel(10, 2) == 5.0', 'is_hidden': False},
                        {
                            'input_data': 'bezpecny_podiel(10, 0)',
                            'expected_output': 'AssertionError',
                            'test_code': (
                                'try:\n'
                                '    bezpecny_podiel(10, 0)\n'
                                '    assert False, "Mala nastať AssertionError"\n'
                                'except AssertionError:\n'
                                '    pass\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Overenie invariantov bankového účtu',
                    'title_en': 'Bank Account Invariant Verification',
                    'instructions_sk': (
                        "Napíš funkciu `over_invarianty_uctu(ucet_dict)`:\n"
                        "Overí platnosť invariantov bankového účtu cez príkazy assert:\n"
                        "1. `isinstance(ucet_dict, dict)`,\n"
                        "2. `ucet_dict['id'] > 0` (kladné ID),\n"
                        "3. `ucet_dict['zostatok'] >= 0` (zostatok nesmie ísť do nepovoleného debetu),\n"
                        "4. `ucet_dict['mena'] in ('EUR', 'USD')`.\n"
                        "Ak všetky asserty prejdú, funkcia vráti `True`. Pri chybe zlyhá s AssertionError."
                    ),
                    'instructions_en': 'Write function `over_invarianty_uctu(ucet_dict)` asserting account invariant properties.',
                    'starter_code': 'def over_invarianty_uctu(ucet_dict):\n    # Over invarianty uctu cez assert\n    pass\n',
                    'solution_code': (
                        'def over_invarianty_uctu(ucet_dict):\n'
                        '    assert isinstance(ucet_dict, dict), "Účet musí byť slovník"\n'
                        '    assert ucet_dict.get("id", 0) > 0, "ID musí byť kladné"\n'
                        '    assert ucet_dict.get("zostatok", -1) >= 0, "Zostatok nesmie byť záporný"\n'
                        '    assert ucet_dict.get("mena") in ("EUR", "USD"), "Nepodporovaná mena"\n'
                        '    return True\n'
                    ),
                    'explanation_sk': 'Otestovali sme všetky invarianty bankového systému pomocou assertov.',
                    'explanation_en': 'Verified all system invariants with descriptive assert statements.',
                    'hint_sk': 'Postupne napíš 4 asserty pre typ, id, zostatok a menu.',
                    'hint_en': 'Write 4 assert statements.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'over_invarianty_uctu({"id": 1, "zostatok": 500, "mena": "EUR"})', 'expected_output': 'True', 'test_code': 'assert over_invarianty_uctu({"id": 1, "zostatok": 500, "mena": "EUR"}) is True', 'is_hidden': False},
                        {
                            'input_data': 'over_invarianty_uctu({"id": 1, "zostatok": -50, "mena": "EUR"})',
                            'expected_output': 'AssertionError',
                            'test_code': (
                                'try:\n'
                                '    over_invarianty_uctu({"id": 1, "zostatok": -50, "mena": "EUR"})\n'
                                '    assert False\n'
                                'except AssertionError:\n'
                                '    pass\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Vstavaný testovací rámec unittest a TestCase',
            'title_en': 'The Built-In unittest Framework & TestCase',
            'summary_sk': 'Modul unittest, trieda TestCase, metódy assertEqual, assertTrue, assertFalse, assertRaises.',
            'summary_en': 'unittest module, TestCase class, assertEqual, assertTrue, assertFalse and assertRaises.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 15.2 Modul `unittest` v Pythone

Pre komplexné testovanie aplikácií poskytuje Python vstavaný modul `unittest` (inšpirovaný JUnitom).

#### Štruktúra testovacieho prípadu:
```python
import unittest

def scitaj(a, b):
    return a + b

class TestKalkulacka(unittest.TestCase):
    def test_scitanie_kladnych(self):
        self.assertEqual(scitaj(2, 3), 5)
        
    def test_scitanie_zapornych(self):
        self.assertEqual(scitaj(-1, -1), -2)
        
    def test_delenie_nulou_vyvola_chybu(self):
        with self.assertRaises(ZeroDivisionError):
            _ = 10 / 0
```
""",
            'content_en': """### 15.2 The unittest Framework

Learn TestCase, `assertEqual`, `assertTrue`, and testing exceptions with `assertRaises`.
""",
            'quizzes': [
                {
                    'question_sk': 'Akým prefixom musí začínať názov metódy v triede `unittest.TestCase`, aby ju test runner automaticky spustil?',
                    'question_en': 'What prefix must a TestCase method have to be auto-discovered by the test runner?',
                    'option_a_sk': 'test_', 'option_a_en': 'test_',
                    'option_b_sk': 'check_', 'option_b_en': 'check_',
                    'option_c_sk': 'run_', 'option_c_en': 'run_',
                    'option_d_sk': 'assert_', 'option_d_en': 'assert_',
                    'correct_option': 'A',
                    'explanation_sk': 'Test runner v unittest spúšťa iba metódy začínajúce reťazcom test_.',
                    'explanation_en': 'Only methods prefixed with test_ are executed.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Implementácia testovacej funkcie porovnania',
                    'title_en': 'Assertion Equivalence Check',
                    'instructions_sk': 'Napíš funkciu `otestuj_rovnost(skutocna, ocakavana)`, ktorá porovná dve hodnoty. Ak sa rovnajú, vráti `True`. Ak sa nerovnajú, vráti chybový reťazec v tvare `"FAILED: {skutocna} != {ocakavana}"`.',
                    'instructions_en': 'Write function `otestuj_rovnost(skutocna, ocakavana)` returning True on match or error string.',
                    'starter_code': 'def otestuj_rovnost(skutocna, ocakavana):\n    # Porovnaj hodnoty\n    pass\n',
                    'solution_code': (
                        'def otestuj_rovnost(skutocna, ocakavana):\n'
                        '    if skutocna == ocakavana:\n'
                        '        return True\n'
                        '    return f"FAILED: {skutocna} != {ocakavana}"\n'
                    ),
                    'explanation_sk': 'Jednoduchá kontrola ekvivalencie imitujúca správanie assertEqual.',
                    'explanation_en': 'Basic assertion simulator mimicking assertEqual.',
                    'hint_sk': 'Použi if skutocna == ocakavana: return True else return f"FAILED: ...".',
                    'hint_en': 'Compare values and return formatted string on mismatch.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'otestuj_rovnost(5, 5)', 'expected_output': 'True', 'test_code': 'assert otestuj_rovnost(5, 5) is True', 'is_hidden': False},
                        {'input_data': 'otestuj_rovnost(4, 5)', 'expected_output': '"FAILED: 4 != 5"', 'test_code': 'assert otestuj_rovnost(4, 5) == "FAILED: 4 != 5"', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Testovacia sada kalkulačky (Mini Test Runner)',
                    'title_en': 'Calculator Mini Test Runner',
                    'instructions_sk': (
                        "Napíš funkciu `spusti_testy(kalkulacka_fn, testovacie_pripady)`:\n"
                        "`testovacie_pripady` je zoznam trojíc `[(a, b, ocakavany_vysledok), ...]`. \n"
                        "Funkcia otestuje volanie `kalkulacka_fn(a, b)` pre každý prípad a vráti slovník:\n"
                        "`{'passed': pocet_uspesnych, 'failed': pocet_zlyhanych}`."
                    ),
                    'instructions_en': 'Write function `spusti_testy(kalkulacka_fn, testovacie_pripady)` evaluating cases and returning passed/failed counts.',
                    'starter_code': 'def spusti_testy(kalkulacka_fn, testovacie_pripady):\n    # Spusti testovaciu sadu\n    pass\n',
                    'solution_code': (
                        'def spusti_testy(kalkulacka_fn, testovacie_pripady):\n'
                        '    passed = 0\n'
                        '    failed = 0\n'
                        '    for a, b, expected in testovacie_pripady:\n'
                        '        try:\n'
                        '            if kalkulacka_fn(a, b) == expected:\n'
                        '                passed += 1\n'
                        '            else:\n'
                        '                failed += 1\n'
                        '        except Exception:\n'
                        '            failed += 1\n'
                        '    return {"passed": passed, "failed": failed}\n'
                    ),
                    'explanation_sk': 'Iterovali sme cez testovacie prípady s odchytom výnimiek a počítali úspechy/neúspechy.',
                    'explanation_en': 'Iterated cases with exception shielding, accumulating pass/fail totals.',
                    'hint_sk': 'Prechádzaj zoznam v cykle a porovnávaj kalkulacka_fn(a, b) == expected.',
                    'hint_en': 'Loop over cases and check equality.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'spusti_testy(lambda a, b: a + b, [(1, 2, 3), (2, 2, 5)])',
                            'expected_output': "{'passed': 1, 'failed': 1}",
                            'test_code': 'assert spusti_testy(lambda a, b: a + b, [(1, 2, 3), (2, 2, 5)]) == {"passed": 1, "failed": 1}',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Overenie vyvolania očakávanej výnimky',
                    'title_en': 'Verify Expected Exception Raising',
                    'instructions_sk': (
                        "Napíš funkciu `over_vyvolanie_chyby(funkcia, argumenty, ocakavana_chyba)`:\n"
                        "`argumenty` je zoznam alebo n-tica argumentov.\n"
                        "Funkcia zavolá `funkcia(*argumenty)`.\n"
                        "- Ak volanie vyvolá presne výnimku `ocakavana_chyba` (alebo jej podtriedu), vráti `True`.\n"
                        "- Ak volanie prebehne bez chyby, alebo vyvolá inú výnimku, vráti `False`."
                    ),
                    'instructions_en': 'Write function `over_vyvolanie_chyby(funkcia, argumenty, ocakavana_chyba)` returning True if expected exception is raised.',
                    'starter_code': 'def over_vyvolanie_chyby(funkcia, argumenty, ocakavana_chyba):\n    # Over vyvolanie výnimky\n    pass\n',
                    'solution_code': (
                        'def over_vyvolanie_chyby(funkcia, argumenty, ocakavana_chyba):\n'
                        '    try:\n'
                        '        funkcia(*argumenty)\n'
                        '        return False\n'
                        '    except ocakavana_chyba:\n'
                        '        return True\n'
                        '    except Exception:\n'
                        '        return False\n'
                    ),
                    'explanation_sk': 'Použili sme try s cieleným odchytom ocakavana_chyba.',
                    'explanation_en': 'Used targeted except block for ocakavana_chyba.',
                    'hint_sk': 'Použi try: funkcia(*argumenty); return False except ocakavana_chyba: return True.',
                    'hint_en': 'Catch expected exception and return True.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'over_vyvolanie_chyby(lambda a, b: a / b, [10, 0], ZeroDivisionError)',
                            'expected_output': 'True',
                            'test_code': 'assert over_vyvolanie_chyby(lambda a, b: a / b, [10, 0], ZeroDivisionError) is True',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'over_vyvolanie_chyby(lambda a, b: a / b, [10, 2], ZeroDivisionError)',
                            'expected_output': 'False',
                            'test_code': 'assert over_vyvolanie_chyby(lambda a, b: a / b, [10, 2], ZeroDivisionError) is False',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Test-Driven Development (TDD) – cyklus Red, Green, Refactor',
            'title_en': 'Test-Driven Development (TDD) – Red, Green, Refactor',
            'summary_sk': 'Metodológia TDD, písanie testov pred kódom, inkrementálny vývoj a refaktoring.',
            'summary_en': 'TDD methodology, writing tests before code, incremental development and refactoring.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 15.3 Metodológia TDD (Test-Driven Development)

TDD obracia tradičný vývoj naruby: **Najprv napíšeme test, až potom produkčný kód**.

#### Cyklus TDD (Red - Green - Refactor):
1. **Red**: Napíšeme zlyhávajúci test pre funkciu, ktorá ešte neexistuje.
2. **Green**: Napíšeme minimálny kód nutný na to, aby test prešiel.
3. **Refactor**: Vylepšíme a vyčistíme kód bez zmeny jeho vonkajšieho správania.
""",
            'content_en': """### 15.3 TDD Lifecycle

Write tests first, watch them fail (Red), implement minimum logic (Green), then optimize (Refactor).
""",
            'quizzes': [
                {
                    'question_sk': 'Čo je prvým krokom v cykle Test-Driven Development (TDD)?',
                    'question_en': 'What is the first phase in the TDD cycle?',
                    'option_a_sk': 'Napísanie zlyhávajúceho automatizovaného testu (Red)', 'option_a_en': 'Writing a failing automated test (Red)',
                    'option_b_sk': 'Optimalizácia výkonu databázy', 'option_b_en': 'Database optimization',
                    'option_c_sk': 'Napísanie celej produkčnej triedy', 'option_c_en': 'Writing the production class',
                    'option_d_sk': 'Deployment na produkciu', 'option_d_en': 'Production deployment',
                    'correct_option': 'A',
                    'explanation_sk': 'TDD vždy začína fázou RED – vytvorením zlyhávajúceho testu, ktorý definuje požiadavku.',
                    'explanation_en': 'TDD begins with a failing test defining requirements.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'TDD: Overovač palindrómov',
                    'title_en': 'TDD: Palindrome Checker',
                    'instructions_sk': 'Napíš funkciu `je_palindrom(slovo)`, ktorá overí, či sa slovo číta rovnako spredu aj zozadu (ignoruje veľkosť písmen a medzery). Vráti `True` ak áno, inak `False`.',
                    'instructions_en': 'Write function `je_palindrom(slovo)` checking case-insensitive and space-insensitive palindromes.',
                    'starter_code': 'def je_palindrom(slovo):\n    # Over palindróm\n    pass\n',
                    'solution_code': (
                        'def je_palindrom(slovo):\n'
                        '    cistene = "".join(ch.lower() for ch in str(slovo) if ch.isalnum())\n'
                        '    return cistene == cistene[::-1]\n'
                    ),
                    'explanation_sk': 'Vyčistili sme alfanumerické znaky na lowercase a porovnali s reverzom [::-1].',
                    'explanation_en': 'Normalized alnums to lowercase and verified equality with slice reversal.',
                    'hint_sk': 'Použi "".join(c.lower() for c in s if c.isalnum()) a porovnaj s reverzom.',
                    'hint_en': 'Filter alnum characters and compare with [::-1].',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'je_palindrom("Radar")', 'expected_output': 'True', 'test_code': 'assert je_palindrom("Radar") is True', 'is_hidden': False},
                        {'input_data': 'je_palindrom("Kanoe")', 'expected_output': 'False', 'test_code': 'assert je_palindrom("Kanoe") is False', 'is_hidden': False},
                        {'input_data': 'je_palindrom("Jelenovi pivo nelej")', 'expected_output': 'True', 'test_code': 'assert je_palindrom("Jelenovi pivo nelej") is True', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'TDD: Klasický algoritmus FizzBuzz',
                    'title_en': 'TDD: Classic FizzBuzz Algorithm',
                    'instructions_sk': 'Napíš funkciu `fizz_buzz(n)`: ak je n deliteľné 15, vráti `"FizzBuzz"`. Ak je deliteľné 3, vráti `"Fizz"`. Ak 5, vráti `"Buzz"`. Inak vráti číslo ako reťazec `str(n)`.',
                    'instructions_en': 'Write function `fizz_buzz(n)` returning FizzBuzz, Fizz, Buzz, or string representation.',
                    'starter_code': 'def fizz_buzz(n):\n    # Implementuj FizzBuzz pravidlá\n    pass\n',
                    'solution_code': (
                        'def fizz_buzz(n):\n'
                        '    if n % 15 == 0:\n'
                        '        return "FizzBuzz"\n'
                        '    if n % 3 == 0:\n'
                        '        return "Fizz"\n'
                        '    if n % 5 == 0:\n'
                        '        return "Buzz"\n'
                        '    return str(n)\n'
                    ),
                    'explanation_sk': 'Pravidlá sme otestovali v poradí 15 -> 3 -> 5 -> str(n).',
                    'explanation_en': 'Checked divisibility in priority order.',
                    'hint_sk': 'Najprv over deliteľnosť 15 (alebo 3 and 5), až potom 3 a 5 zvlášť.',
                    'hint_en': 'Check 15 first.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'fizz_buzz(15)', 'expected_output': '"FizzBuzz"', 'test_code': 'assert fizz_buzz(15) == "FizzBuzz"', 'is_hidden': False},
                        {'input_data': 'fizz_buzz(9)', 'expected_output': '"Fizz"', 'test_code': 'assert fizz_buzz(9) == "Fizz"', 'is_hidden': False},
                        {'input_data': 'fizz_buzz(10)', 'expected_output': '"Buzz"', 'test_code': 'assert fizz_buzz(10) == "Buzz"', 'is_hidden': False},
                        {'input_data': 'fizz_buzz(7)', 'expected_output': '"7"', 'test_code': 'assert fizz_buzz(7) == "7"', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'TDD: Prevodník rímskych číslic na celé čísla',
                    'title_en': 'TDD: Roman to Integer Converter',
                    'instructions_sk': 'Napíš funkciu `rimske_na_cislo(rimske)`: prevedie rímske číslo (napr. "IV" -> 4, "IX" -> 9, "LVIII" -> 58, "MCMXCIV" -> 1994) na celé číslo `int`. Hodnoty symbolov: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.',
                    'instructions_en': 'Write function `rimske_na_cislo(rimske)` converting Roman numeral string to integer.',
                    'starter_code': 'def rimske_na_cislo(rimske):\n    # Preveď rímske číslice na int\n    pass\n',
                    'solution_code': (
                        'def rimske_na_cislo(rimske):\n'
                        '    hodnoty = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}\n'
                        '    celkovo = 0\n'
                        '    predchadzajuca = 0\n'
                        '    for znak in reversed(rimske.upper()):\n'
                        '        hodnota = hodnoty.get(znak, 0)\n'
                        '        if hodnota < predchadzajuca:\n'
                        '            celkovo -= hodnota\n'
                        '        else:\n'
                        '            celkovo += hodnota\n'
                        '        predchadzajuca = hodnota\n'
                        '    return celkovo\n'
                    ),
                    'explanation_sk': 'Iterovali sme odzadu: ak je aktuálna hodnota menšia ako predchádzajúca, odčítame, inak pripočítame.',
                    'explanation_en': 'Iterated in reverse: subtract if less than previous, else add.',
                    'hint_sk': 'Prechádzaj reťazec odzadu pomocou reversed(rimske).',
                    'hint_en': 'Iterate reversed string and subtract when smaller than right neighbor.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'rimske_na_cislo("IV")', 'expected_output': '4', 'test_code': 'assert rimske_na_cislo("IV") == 4', 'is_hidden': False},
                        {'input_data': 'rimske_na_cislo("IX")', 'expected_output': '9', 'test_code': 'assert rimske_na_cislo("IX") == 9', 'is_hidden': False},
                        {'input_data': 'rimske_na_cislo("MCMXCIV")', 'expected_output': '1994', 'test_code': 'assert rimske_na_cislo("MCMXCIV") == 1994', 'is_hidden': False},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Hraničné stavy (Edge Cases) a čistý kód podľa PEP 8',
            'title_en': 'Boundary Edge Cases & PEP 8 Clean Code',
            'summary_sk': 'Nulové vstupy, prázdne kontajnery, typové anomálie, princípy Clean Code a PEP 8.',
            'summary_en': 'Zero inputs, empty containers, type anomalies, Clean Code principles and PEP 8.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 15.4 Hraničné stavy a PEP 8

Až 80 % chýb v softvérovom inžinierstve nevzniká v bežnom toku (tzv. Happy Path), ale v **hraničných stavoch (Edge Cases)**:
1. Prázdny reťazec `""` alebo prázdny zoznam `[]`
2. Nula `0`, záporné čísla, extrémne veľké čísla
3. Hodnota `None` na vstupe
4. Dátové pretečenia a delenie nulou
""",
            'content_en': """### 15.4 Edge Cases & Clean Code

Test empty collections, zero divisors, negative values, and adhere to PEP 8 standards.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo znamená zásada "Happy Path" pri testovaní?',
                    'question_en': 'What does "Happy Path" refer to in software testing?',
                    'option_a_sk': 'Scenár, kde používateľ zadá správne a očakávané dáta a všetko prebehne bez chýb', 'option_a_en': 'Scenario where user enters valid expected inputs and execution succeeds',
                    'option_b_sk': 'Testovanie s veselou hudbou', 'option_b_en': 'Testing with music',
                    'option_c_sk': 'Automatické generovanie UI', 'option_c_en': 'Auto UI generation',
                    'option_d_sk': 'Testovanie len na Vianoce', 'option_d_en': 'Holiday testing only',
                    'correct_option': 'A',
                    'explanation_sk': 'Happy path je ideálny scenár bez chýb a anomálií.',
                    'explanation_en': 'Happy path describes the default error-free flow.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Bezpečný medián s hraničnými stavmi',
                    'title_en': 'Safe Median Handling Edge Cases',
                    'instructions_sk': 'Napíš funkciu `bezpecny_median(zoznam_cisel)`: pre prázdny zoznam vráti `None`. Pre nepárny počet vráti strednú hodnotu po zoradení. Pre párny počet vráti priemer dvoch stredných hodnôt.',
                    'instructions_en': 'Write function `bezpecny_median(zoznam_cisel)` returning median or None for empty list.',
                    'starter_code': 'def bezpecny_median(zoznam_cisel):\n    # Vypočítaj medián s ošetrením prázdneho zoznamu\n    pass\n',
                    'solution_code': (
                        'def bezpecny_median(zoznam_cisel):\n'
                        '    if not zoznam_cisel:\n'
                        '        return None\n'
                        '    s = sorted(zoznam_cisel)\n'
                        '    n = len(s)\n'
                        '    mid = n // 2\n'
                        '    if n % 2 == 1:\n'
                        '        return float(s[mid])\n'
                        '    return (s[mid - 1] + s[mid]) / 2.0\n'
                    ),
                    'explanation_sk': 'Ošetrili sme prázdny vstup, zoradili a rozlíšili párnu a nepárnu dĺžku.',
                    'explanation_en': 'Handled empty list, sorted and calculated median for odd/even lengths.',
                    'hint_sk': 'Zoraď zoznam sorted(zoznam_cisel) a nájdi stred n // 2.',
                    'hint_en': 'Sort list and inspect mid index.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'bezpecny_median([3, 1, 2])', 'expected_output': '2.0', 'test_code': 'assert bezpecny_median([3, 1, 2]) == 2.0', 'is_hidden': False},
                        {'input_data': 'bezpecny_median([1, 2, 3, 4])', 'expected_output': '2.5', 'test_code': 'assert bezpecny_median([1, 2, 3, 4]) == 2.5', 'is_hidden': False},
                        {'input_data': 'bezpecny_median([])', 'expected_output': 'None', 'test_code': 'assert bezpecny_median([]) is None', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Defenzívny normalizátor vstupov',
                    'title_en': 'Defensive Input Normalizer',
                    'instructions_sk': 'Napíš funkciu `normalizuj_meno(meno_vstup)`: ošetrí vstup (ak nie je reťazec alebo je po strip prázdny, vráti `"Anonym"`). Inak vráti orezaný reťazec vo formáte Title Case (napr. `"  jUraj volf  "` -> `"Juraj Volf"`).',
                    'instructions_en': 'Write function `normalizuj_meno(meno_vstup)` sanitizing input to Title Case or returning "Anonym".',
                    'starter_code': 'def normalizuj_meno(meno_vstup):\n    # Normalizuj meno na Title Case\n    pass\n',
                    'solution_code': (
                        'def normalizuj_meno(meno_vstup):\n'
                        '    if not isinstance(meno_vstup, str):\n'
                        '        return "Anonym"\n'
                        '    cistene = meno_vstup.strip()\n'
                        '    if not cistene:\n'
                        '        return "Anonym"\n'
                        '    return cistene.title()\n'
                    ),
                    'explanation_sk': 'Overili sme typ, orezali medzery a aplikovali metódu .title().',
                    'explanation_en': 'Checked type, trimmed whitespaces and applied title formatting.',
                    'hint_sk': 'Over isinstance(s, str), s.strip() a použi s.title().',
                    'hint_en': 'Check string type and return s.strip().title().',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'normalizuj_meno("  juraj volf  ")', 'expected_output': '"Juraj Volf"', 'test_code': 'assert normalizuj_meno("  juraj volf  ") == "Juraj Volf"', 'is_hidden': False},
                        {'input_data': 'normalizuj_meno(None)', 'expected_output': '"Anonym"', 'test_code': 'assert normalizuj_meno(None) == "Anonym"', 'is_hidden': False},
                        {'input_data': 'normalizuj_meno("   ")', 'expected_output': '"Anonym"', 'test_code': 'assert normalizuj_meno("   ") == "Anonym"', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Robustný parser ISO dátumov s kontrolou limitov',
                    'title_en': 'Robust ISO Date Parser with Boundary Checks',
                    'instructions_sk': (
                        "Napíš funkciu `parsuj_iso_datum(datum_str)`:\n"
                        "Prijme reťazec v tvare `YYYY-MM-DD`.\n"
                        "Overí, že:\n"
                        "- Rok je v rozsahu 1900 až 2100,\n"
                        "- Mesiac je v rozsahu 1 až 12,\n"
                        "- Deň je v rozsahu 1 až 31 (a pre február max 29).\n"
                        "Ak je dátum platný, vráti slovník `{'rok': int, 'mesiac': int, 'den': int}`. Inak vráti `None`."
                    ),
                    'instructions_en': 'Write function `parsuj_iso_datum(datum_str)` returning parsed date dictionary or None on validation failure.',
                    'starter_code': 'def parsuj_iso_datum(datum_str):\n    # Parsuj a validuj ISO dátum\n    pass\n',
                    'solution_code': (
                        'def parsuj_iso_datum(datum_str):\n'
                        '    if not isinstance(datum_str, str):\n'
                        '        return None\n'
                        '    casti = datum_str.strip().split("-")\n'
                        '    if len(casti) != 3:\n'
                        '        return None\n'
                        '    try:\n'
                        '        r, m, d = int(casti[0]), int(casti[1]), int(casti[2])\n'
                        '    except ValueError:\n'
                        '        return None\n'
                        '    if not (1900 <= r <= 2100):\n'
                        '        return None\n'
                        '    if not (1 <= m <= 12):\n'
                        '        return None\n'
                        '    max_dni = 29 if m == 2 else (30 if m in (4, 6, 9, 11) else 31)\n'
                        '    if not (1 <= d <= max_dni):\n'
                        '        return None\n'
                        '    return {"rok": r, "mesiac": m, "den": d}\n'
                    ),
                    'explanation_sk': 'Overili sme správny formát, rozsah rokov, mesiacov a limit dní pre jednotlivé mesiace.',
                    'explanation_en': 'Validated split parts, range constraints and month day capacities.',
                    'hint_sk': 'Rozdeľ podľa "-" a over r, m, d.',
                    'hint_en': 'Split by dash and check month day limits.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'parsuj_iso_datum("2027-04-15")', 'expected_output': "{'rok': 2027, 'mesiac': 4, 'den': 15}", 'test_code': 'assert parsuj_iso_datum("2027-04-15") == {"rok": 2027, "mesiac": 4, "den": 15}', 'is_hidden': False},
                        {'input_data': 'parsuj_iso_datum("2027-02-30")', 'expected_output': 'None', 'test_code': 'assert parsuj_iso_datum("2027-02-30") is None', 'is_hidden': False},
                        {'input_data': 'parsuj_iso_datum("neplatny")', 'expected_output': 'None', 'test_code': 'assert parsuj_iso_datum("neplatny") is None', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
