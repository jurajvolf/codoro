"""
MODUL 4: Cykly, iterácie a spracovanie postupností
Odhadovaný rozsah: 14 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 4,
    'title_sk': 'Cykly, iterácie a spracovanie postupností',
    'title_en': 'Loops, Iterations & Sequence Processing',
    'description_sk': 'Nauč sa efektívne opakovať operácie pomocou cyklov for a while, generátora range(), akumulačných vzorov, riadenia behu cez break/continue a 2D vnorených cyklov.',
    'description_en': 'Master iteration through for and while loops, range() generators, accumulator patterns, control flow with break/continue/else, and nested 2D loops.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'arrow-repeat',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Cyklus for a generátor číselných radov range()',
            'title_en': 'The for Loop & the range() Sequence Generator',
            'summary_sk': 'Iterácia cez postupnosti, syntax range(stop), range(start, stop), range(start, stop, step).',
            'summary_en': 'Iterating collections, range(stop), range(start, stop), range(start, stop, step) variants.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 4.1 Cyklus `for` a funkcia `range()`

Cyklus `for` v Pythone slúži na prechádzanie (iterovanie) cez prvky akejkoľvek postupnosti.

#### Generátor `range()`
Vytvára postupnosť celých čísel na požiadanie (lazy evaluation):
1. `range(stop)` – od 0 do `stop - 1`. Napr. `range(5)` -> `0, 1, 2, 3, 4`.
2. `range(start, stop)` – od `start` do `stop - 1`. Napr. `range(2, 6)` -> `2, 3, 4, 5`.
3. `range(start, stop, step)` – s vlastným krokom (môže byť aj záporný!). Napr. `range(10, 0, -2)` -> `10, 8, 6, 4, 2`.

```python
for i in range(1, 6):
    print(f"Krok č. {i}")
```
""",
            'content_en': """### 4.1 The for Loop and `range()`

In Python, `for` iterates over iterable objects.

- `range(5)` yields 0..4
- `range(2, 6)` yields 2..5
- `range(10, 0, -2)` yields 10, 8, 6, 4, 2
""",
            'quizzes': [
                {
                    'question_sk': 'Koľkokrát sa vykoná telo cyklu `for i in range(1, 10, 2):`?',
                    'question_en': 'How many times does the body of `for i in range(1, 10, 2):` execute?',
                    'option_a_sk': '5-krát (čísla 1, 3, 5, 7, 9)', 'option_a_en': '5 times (numbers 1, 3, 5, 7, 9)',
                    'option_b_sk': '9-krát', 'option_b_en': '9 times',
                    'option_c_sk': '4-krát', 'option_c_en': '4 times',
                    'option_d_sk': '10-krát', 'option_d_en': '10 times',
                    'correct_option': 'A',
                    'explanation_sk': 'Hodnoty i budú postupne 1, 3, 5, 7, 9, čo je spolu presne 5 iterácií.',
                    'explanation_en': 'The generated sequence consists of 1, 3, 5, 7, 9, exactly 5 iterations.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Súčet párnych čísel v intervale',
                    'title_en': 'Sum of Even Numbers in Range',
                    'instructions_sk': 'Napíš funkciu `sucet_parnych(od, do_hodnota)`, ktorá pomocou cyklu `for` spočíta a vráti súčet všetkých párnych čísel od `od` po `do_hodnota` (vrátane oboch hraníc).',
                    'instructions_en': 'Write `sucet_parnych(od, do_hodnota)` calculating the sum of even integers in inclusive range.',
                    'starter_code': 'def sucet_parnych(od, do_hodnota):\n    pass\n',
                    'solution_code': 'def sucet_parnych(od, do_hodnota):\n    sucet = 0\n    for cislo in range(od, do_hodnota + 1):\n        if cislo % 2 == 0:\n            sucet += cislo\n    return sucet\n',
                    'explanation_sk': 'Iterujeme od začiatku po do_hodnota + 1 a pripočítavame čísla s nulovým zvyškom po delení 2.',
                    'explanation_en': 'Iterate through range(od, do_hodnota + 1) and accumulate even numbers.',
                    'hint_sk': 'Inicializuj sucet = 0 a v cykle for cislo in range(od, do_hodnota + 1): if cislo % 2 == 0: sucet += cislo.',
                    'hint_en': 'Initialize sum = 0 and inside loop check if cislo % 2 == 0.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'sucet_parnych(1, 10)', 'expected_output': '30', 'test_code': 'assert sucet_parnych(1, 10) == 30', 'is_hidden': False},
                        {'input_data': 'sucet_parnych(4, 4)', 'expected_output': '4', 'test_code': 'assert sucet_parnych(4, 4) == 4', 'is_hidden': False},
                        {'input_data': 'sucet_parnych(10, 20)', 'expected_output': '90', 'test_code': 'assert sucet_parnych(10, 20) == 90', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Akumulátory, počítadlá a hľadanie min/max hodnôt',
            'title_en': 'Accumulators, Counters & Min/Max Extrema',
            'summary_sk': 'Základné algoritmické vzory: sčítanie do sumy, počítanie výskytov a hľadanie extrému.',
            'summary_en': 'Core algorithmic patterns: summation, frequency counting, and manual extrema search.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 4.2 Akumulačné vzory v cykloch

V algoritmizácii sa neustále stretávame s tromi základnými vzormi:
1. **Akumulátor (Súčet)**: Premenná nastavená pred cyklom na 0, do ktorej pripočítavame hodnoty.
2. **Počítadlo (Counter)**: Premenná nastavená na 0, ktorú inkrementujeme o 1 pri splnení podmienky.
3. **Hľadanie extrému (Min / Max)**: Premenná nastavená na prvý prvok alebo nekonečno, ktorú prepíšeme pri nájdení lepšej hodnoty.

```python
cisla = [14, 5, 29, 3, 42]
najvacsie = cisla[0]

for c in cisla:
    if c > najvacsie:
        najvacsie = c
print("Maximum:", najvacsie)  # 42
```
""",
            'content_en': """### 4.2 Accumulator and Counter Patterns

Standard programming idioms:
- Sum accumulator initialized to 0.
- Counter incrementing upon criteria.
- Min/Max tracker initialized to first element.
""",
            'quizzes': [
                {
                    'question_sk': 'Na akú počiatočnú hodnotu je najlepšie nastaviť premennú pri hľadaní minima v neprázdnom zozname čísel?',
                    'question_en': 'What initial value is safest when searching for minimum in a non-empty list of numbers?',
                    'option_a_sk': '0', 'option_a_en': '0',
                    'option_b_sk': 'Prvý prvok zoznamu (zoznam[0]) alebo float("inf")', 'option_b_en': 'First element list[0] or float("inf")',
                    'option_c_sk': '-1', 'option_c_en': '-1',
                    'option_d_sk': 'None', 'option_d_en': 'None',
                    'correct_option': 'B',
                    'explanation_sk': 'Nastavenie na 0 by zlyhalo, ak by boli všetky čísla v zozname kladné (napr. 10, 20). Prvý prvok alebo nekonečno zaručí správnosť.',
                    'explanation_en': 'Setting 0 fails if all values are positive. Using list[0] or float("inf") guarantees correctness.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Štatistika herných skóre',
                    'title_en': 'Player Game Scores Aggregator',
                    'instructions_sk': (
                        "Napíš funkciu `analyzuj_skore(zoznam_skore)`, ktorá vráti trojicu (tuple) v tvare `(pocet, sucet, priemer)`:\n"
                        "- Ak je zoznam prázdny, vráti `(0, 0, 0.0)`.\n"
                        "- Priemer zaokrúhli na 2 desatinné miesta cez `round(priemer, 2)`."
                    ),
                    'instructions_en': 'Write `analyzuj_skore(zoznam_skore)` returning tuple `(pocet, sucet, priemer)`.',
                    'starter_code': 'def analyzuj_skore(zoznam_skore):\n    pass\n',
                    'solution_code': 'def analyzuj_skore(zoznam_skore):\n    if not zoznam_skore:\n        return (0, 0, 0.0)\n    pocet = len(zoznam_skore)\n    sucet = sum(zoznam_skore)\n    priemer = round(sucet / pocet, 2)\n    return (pocet, sucet, priemer)\n',
                    'explanation_sk': 'Ošetríme prázdny vstup guard clause a vypočítame dĺžku, súčet a zaokrúhlený priemer.',
                    'explanation_en': 'Guard clause against empty list, aggregate count, sum, and rounded mean.',
                    'hint_sk': 'Over `if not zoznam_skore: return (0, 0, 0.0)` a potom spočítaj len() a sum().',
                    'hint_en': 'Check empty list first, then compute len(), sum(), round().',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'analyzuj_skore([10, 20, 30])', 'expected_output': '(3, 60, 20.0)', 'test_code': 'assert analyzuj_skore([10, 20, 30]) == (3, 60, 20.0)', 'is_hidden': False},
                        {'input_data': 'analyzuj_skore([])', 'expected_output': '(0, 0, 0.0)', 'test_code': 'assert analyzuj_skore([]) == (0, 0, 0.0)', 'is_hidden': False},
                        {'input_data': 'analyzuj_skore([5, 10, 15, 22])', 'expected_output': '(4, 52, 13.0)', 'test_code': 'assert analyzuj_skore([5, 10, 15, 22]) == (4, 52, 13.0)', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Podmienený cyklus while a prevencia nekonečných cyklov',
            'title_en': 'The while Loop & Preventing Infinite Loops',
            'summary_sk': 'Cykly s neznámym počtom opakovaní, zmena riadiacej premennej a bezpečnostné limity.',
            'summary_en': 'Indefinite iteration with while loops, loop variant modifications, and guard timeouts.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 4.3 Podmienený cyklus `while`

Cyklus `while` opakuje blok príkazov, kým je podmienka pravdivá (`True`). Používa sa vtedy, keď **vopred nepoznáme presný počet opakovaní**.

```python
energia = 100
kroky = 0

while energia > 0:
    energia -= 25
    kroky += 1

print(f"Hráč spravil {kroky} krokov.")
```

#### Pozor na nekonečný cyklus (Infinite Loop)!
Ak v tele cyklu nezmeníme premenné ovplyvňujúce podmienku, cyklus nikdy neskončí a zamrzne program.
""",
            'content_en': """### 4.3 The while Loop

Repeats commands while a condition remains True. Always ensure the terminating condition is reachable to avoid infinite execution.
""",
            'quizzes': [
                {
                    'question_sk': 'Kedy je vhodnejšie použiť cyklus `while` namiesto cyklu `for`?',
                    'question_en': 'When is a while loop preferred over a for loop?',
                    'option_a_sk': 'Keď vopred nevieme, koľko iterácií bude potrebných, ale poznáme ukončovaciu podmienku', 'option_a_en': 'When iteration count is unknown beforehand but terminating condition is known',
                    'option_b_sk': 'Keď chceme iterovať cez zoznam', 'option_b_en': 'When iterating lists',
                    'option_c_sk': 'Keď je v kóde viac ako 5 premenných', 'option_c_en': 'When code has >5 variables',
                    'option_d_sk': 'while je vždy rýchlejší ako for', 'option_d_en': 'while is always faster',
                    'correct_option': 'A',
                    'explanation_sk': 'while sa používa pri podmienenom opakovaní (napr. čítanie dát kým nepríde koniec súboru, herná slučka kým hráč žije).',
                    'explanation_en': 'while is ideal for event loops and indefinite repetition until a state change occurs.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Ciferný súčet čísla',
                    'title_en': 'Sum of Digits via while loop',
                    'instructions_sk': 'Napíš funkciu `ciferny_sucet(cislo)`, ktorá pomocou cyklu `while`, operátora `% 10` a celočíselného delenia `// 10` spočíta a vráti súčet cifier celého nezáporného čísla. Napr. pre `1234` vráti `10`.',
                    'instructions_en': 'Write `ciferny_sucet(cislo)` using while loop with % 10 and // 10 to sum all digits.',
                    'starter_code': 'def ciferny_sucet(cislo):\n    pass\n',
                    'solution_code': 'def ciferny_sucet(cislo):\n    sucet = 0\n    c = abs(cislo)\n    while c > 0:\n        sucet += c % 10\n        c //= 10\n    return sucet\n',
                    'explanation_sk': 'V každom kroku získame poslednú cifru cez c % 10 a číslo skrátime cez c //= 10.',
                    'explanation_en': 'Extract last digit with modulo 10 and reduce integer via integer division by 10.',
                    'hint_sk': 'V cykle while c > 0: sucet += c % 10; c //= 10.',
                    'hint_en': 'Loop while c > 0: sum += c % 10; c //= 10.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'ciferny_sucet(1234)', 'expected_output': '10', 'test_code': 'assert ciferny_sucet(1234) == 10', 'is_hidden': False},
                        {'input_data': 'ciferny_sucet(7)', 'expected_output': '7', 'test_code': 'assert ciferny_sucet(7) == 7', 'is_hidden': False},
                        {'input_data': 'ciferny_sucet(98765)', 'expected_output': '35', 'test_code': 'assert ciferny_sucet(98765) == 35', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Riadenie behu cyklu: príkazy break, continue a vetva else',
            'title_en': 'Loop Control Flow: break, continue & loop else',
            'summary_sk': 'Okamžité vyskočenie z cyklu cez break, preskočenie iterácie cez continue a vetva else pri cykle.',
            'summary_en': 'Early termination via break, skipping steps with continue, and the unique for-else construct.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 4.4 Riadenie behu cyklu: `break`, `continue` a `else`

#### Príkaz `break`
Okamžite predčasne ukončí celý cyklus a pokračuje kódom za cyklom:
```python
for cislo in range(1, 100):
    if cislo == 5:
        break  # Skončí pri 5
```

#### Príkaz `continue`
Okamžite preskočí zvyšok aktuálnej iterácie a prejde na ďalší krok cyklu:
```python
for cislo in range(1, 6):
    if cislo == 3:
        continue  # Preskočí trojku
    print(cislo)  # Vypíše: 1, 2, 4, 5
```

#### Vetva `else` pri cykloch (Python špecialita!)
Blok `else:` za cyklom sa vykoná **len vtedy, ak cyklus prebehol celý a NEBOL prerušený príkazom `break`**. To sa geniálne hodí na hľadanie prvku:
```python
for x in zoznam:
    if x == hladany:
        print("Nájdené!")
        break
else:
    print("Prvok sa nenašiel!")
```
""",
            'content_en': """### 4.4 Flow Control: break, continue, and loop else

- `break` exits the enclosing loop immediately.
- `continue` skips to the next iteration.
- `else` on a loop executes only if the loop completed naturally without hitting `break`.
""",
            'quizzes': [
                {
                    'question_sk': 'Kedy sa vykoná vetva `else` priradená k cyklu `for`?',
                    'question_en': 'When does the `else` clause of a `for` loop execute?',
                    'option_a_sk': 'Vždy po skončení cyklu', 'option_a_en': 'Always after loop ends',
                    'option_b_sk': 'Iba vtedy, ak cyklus skončil normálne a NEBOL prerušený príkazom break', 'option_b_en': 'Only if loop finished naturally without encountering break',
                    'option_c_sk': 'Iba vtedy, ak cyklus obsahoval chybu', 'option_c_en': 'Only upon error',
                    'option_d_sk': 'Iba ak sa vykoná continue', 'option_d_en': 'Only if continue was called',
                    'correct_option': 'B',
                    'explanation_sk': 'Vetva else za cyklom sa v Pythone vykoná len vtedy, ak cyklus nebol predčasne ukončený príkazom break.',
                    'explanation_en': 'A loop else block triggers only when exhaustion occurs without a break statement.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Test prvočíselnosti (Prime Number Checker)',
                    'title_en': 'Prime Number Checker with break',
                    'instructions_sk': (
                        "Napíš funkciu `je_prvocislo(n)`, ktorá vráti `True`, ak je číslo $n$ prvočíslo (celé číslo väčšie ako 1 deliteľné iba jednotkou a samým sebou).\n"
                        "Použi cyklus `for d in range(2, int(n**0.5) + 1):` a príkaz `break`."
                    ),
                    'instructions_en': 'Write `je_prvocislo(n)` checking if integer n > 1 is prime.',
                    'starter_code': 'def je_prvocislo(n):\n    pass\n',
                    'solution_code': 'def je_prvocislo(n):\n    if n < 2:\n        return False\n    for d in range(2, int(n**0.5) + 1):\n        if n % d == 0:\n            return False\n    return True\n',
                    'explanation_sk': 'Čísla menšie ako 2 nie sú prvočísla. Následne overujeme deliteľnosť do odmocniny z n.',
                    'explanation_en': 'Trial division algorithm testing divisors up to floor(sqrt(n)).',
                    'hint_sk': 'Over n < 2 a potom deliteľnosť cez if n % d == 0: return False.',
                    'hint_en': 'Check n < 2, then loop and if n % d == 0 return False.',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'je_prvocislo(7)', 'expected_output': 'True', 'test_code': 'assert je_prvocislo(7) is True', 'is_hidden': False},
                        {'input_data': 'je_prvocislo(12)', 'expected_output': 'False', 'test_code': 'assert je_prvocislo(12) is False', 'is_hidden': False},
                        {'input_data': 'je_prvocislo(97)', 'expected_output': 'True', 'test_code': 'assert je_prvocislo(97) is True', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Vnorené cykly, 2D mriežky a zhrnutie modulu',
            'title_en': 'Nested 2D Loops, Grids & Module Summary',
            'summary_sk': 'Vnorené for cykly pre riadky a stĺpce, generovanie násobilky a komplexná maturitná úloha.',
            'summary_en': 'Nested for loops for matrix rows/columns, multiplication tables, and capstone challenge.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 4.5 Vnorené cykly (2D matice a mriežky)

Keď vložíme jeden cyklus do druhého, vonkajší cyklus reprezentuje **riadky** a vnútorný cyklus **stĺpce**.

```python
for riadok in range(1, 4):
    for stlpec in range(1, 4):
        print(f"{riadok * stlpec:2d}", end=" ")
    print()  # Nový riadok po dokončení stĺpcov
```

Výstup:
```
 1  2  3 
 2  4  6 
 3  6  9 
```
Časová zložitosť takéhoto algoritmu je $O(n \\times m)$.
""",
            'content_en': """### 4.5 Nested Loops and 2D Grids

Outer loop controls rows while inner loop controls columns.
""",
            'quizzes': [
                {
                    'question_sk': 'Ak vonkajší cyklus beží 5-krát a vnútorný cyklus 4-krát, koľkokrát sa vykoná telo vnútorného cyklu?',
                    'question_en': 'If outer loop runs 5 times and inner loop runs 4 times, how many total executions occur?',
                    'option_a_sk': '20-krát (5 * 4)', 'option_a_en': '20 times (5 * 4)',
                    'option_b_sk': '9-krát (5 + 4)', 'option_b_en': '9 times (5 + 4)',
                    'option_c_sk': '5-krát', 'option_c_en': '5 times',
                    'option_d_sk': '16-krát', 'option_d_en': '16 times',
                    'correct_option': 'A',
                    'explanation_sk': 'Pri vnorených cykloch sa celkový počet opakovaní rovná súčinu počtov opakovaní: 5 * 4 = 20.',
                    'explanation_en': 'Total operations equal product of iterations: 5 * 4 = 20.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Generátor šachovnice (Chessboard Matrix)',
                    'title_en': 'Chessboard Grid Generator',
                    'instructions_sk': (
                        "Napíš funkciu `generuj_sachovnicu(n)`, kde $n$ je veľkosť strany mriežky.\n"
                        "Funkcia vráti zoznam zoznamov (2D maticu) veľkosti $n \\times n$, kde políčka striedajú hodnoty 1 a 0.\n"
                        "Ak je `(riadok + stlpec) % 2 == 0`, hodnota je `1`, inak `0`.\n"
                        "Napr. pre $n=2$ vráti `[[1, 0], [0, 1]]`."
                    ),
                    'instructions_en': 'Write `generuj_sachovnicu(n)` returning an n-by-n matrix where cell is 1 if (r+c)%2==0 else 0.',
                    'starter_code': 'def generuj_sachovnicu(n):\n    pass\n',
                    'solution_code': 'def generuj_sachovnicu(n):\n    matica = []\n    for r in range(n):\n        riadok = []\n        for c in range(n):\n            riadok.append(1 if (r + c) % 2 == 0 else 0)\n        matica.append(riadok)\n    return matica\n',
                    'explanation_sk': 'Používame vnorené for cykly pre riadky a stĺpce s paritným pravidlom šachovnice.',
                    'explanation_en': 'Nested for loops assembling row lists with parity-based alternating 1 and 0 values.',
                    'hint_sk': 'Použi dva cykly: for r in range(n): a for c in range(n): riadok.append(1 if (r+c)%2==0 else 0).',
                    'hint_en': 'Use two nested loops: for r in range(n): for c in range(n): append 1 if (r+c)%2==0 else 0.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'generuj_sachovnicu(2)', 'expected_output': '[[1, 0], [0, 1]]', 'test_code': 'assert generuj_sachovnicu(2) == [[1, 0], [0, 1]]', 'is_hidden': False},
                        {'input_data': 'generuj_sachovnicu(3)', 'expected_output': '[[1, 0, 1], [0, 1, 0], [1, 0, 1]]', 'test_code': 'assert generuj_sachovnicu(3) == [[1, 0, 1], [0, 1, 0], [1, 0, 1]]', 'is_hidden': False},
                        {'input_data': 'generuj_sachovnicu(1)', 'expected_output': '[[1]]', 'test_code': 'assert generuj_sachovnicu(1) == [[1]]', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
