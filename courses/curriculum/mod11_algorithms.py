"""
MODUL 11: Klasické algoritmy, časová zložitosť a matematika
Odhadovaný rozsah: 14 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU
"""

MODULE_DATA = {
    'order': 11,
    'title_sk': 'Klasické algoritmy, časová zložitosť a matematika',
    'title_en': 'Classic Algorithms, Time Complexity & Mathematics',
    'description_sk': 'Akademické a priemyselné algoritmické základy: Big-O notácia, binárne vyhľadávanie O(log n), triediace algoritmy (Bubble/Merge/Quick), Eratostenovo sito na prvočísla, kryptografická Caesarova šifra a validácia Luhnovho algoritmu.',
    'description_en': 'Computer science foundations: Big-O asymptotic complexity, binary search, comparison sorts, divide-and-conquer (Merge/Quick), Sieve of Eratosthenes, Caesar cipher, and Luhn checksum validation.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'cpu',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Časová a pamäťová zložitosť (Big-O Notácia)',
            'title_en': 'Time & Space Complexity (Big-O Notation)',
            'summary_sk': 'Asymptotická zložitosť algoritmov, porovnanie tried O(1), O(log n), O(n), O(n log n), O(n^2).',
            'summary_en': 'Asymptotic growth analysis, orders of magnitude O(1), O(log n), O(n), O(n log n), O(n^2).',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 11.1 Úvod do Big-O notácie

**Big-O notácia** popisuje, ako rastie čas vykonávania (alebo spotreba pamäte) algoritmu v závislosti od veľkosti vstupných dát $n$.

| Notácia | Názov | Príklad operácie |
|---|---|---|
| $O(1)$ | Konštantná | Prístup k prvku zoznamu podľa indexu `zoznam[i]`, slovník `.get()` |
| $O(\\log n)$ | Logaritmická | Binárne vyhľadávanie v utriedenom zozname |
| $O(n)$ | Lineárna | Jednoduchý for cyklus prechádzajúci zoznam, hľadanie minima |
| $O(n \\log n)$ | Linearitmická | Efektívne triedenie (Timsort v Pythone, Merge Sort, QuickSort) |
| $O(n^2)$ | Kvadratická | Dva vnorené for cykly (Bubble Sort) |
| $O(2^n)$ | Exponenciálna | Naivný rekurzívny výpočet Fibonacciho čísel |

Cieľom softvérového inžiniera je navrhovať algoritmy s čo najnižšou zložitosťou.
""",
            'content_en': """### 11.1 Big-O Asymptotic Complexity

Big-O measures the upper bound of operational growth as input size $n$ scales towards infinity.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá z nasledujúcich časových zložitostí je najefektívnejšia (najrýchlejšia) pre veľké vstupy n?',
                    'question_en': 'Which time complexity class is the most efficient for large n?',
                    'option_a_sk': 'O(1)', 'option_a_en': 'O(1)',
                    'option_b_sk': 'O(n)', 'option_b_en': 'O(n)',
                    'option_c_sk': 'O(n^2)', 'option_c_en': 'O(n^2)',
                    'option_d_sk': 'O(log n)', 'option_d_en': 'O(log n)',
                    'correct_option': 'A',
                    'explanation_sk': 'Konštantná zložitosť O(1) trvá rovnaký čas bez ohľadu na to, či má vstup 10 alebo 10 miliónov prvkov.',
                    'explanation_en': 'Constant time O(1) executes in fixed steps independent of input volume.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Efektívny výpočet dvoch súčtov (Two Sum v O(n))',
                    'title_en': 'Two Sum Problem in O(n)',
                    'instructions_sk': (
                        "Klasická interview úloha: Napíš funkciu `two_sum(cisla, ciel)`, ktorá vráti dvojicu indexov `(i, j)` dvoch rôznych čísel, ktorých súčet je rovný `ciel`.\n"
                        "Použi hešovaciu tabuľku (slovník) tak, aby algoritmus bežal v lineárnom čase $O(n)$ namiesto pomalého $O(n^2)$ vnoreného cyklu!\n"
                        "Ak riešenie neexistuje, vráti `None`."
                    ),
                    'instructions_en': 'Write `two_sum(cisla, ciel)` in O(n) time using dictionary lookup returning index tuple (i, j) or None.',
                    'starter_code': 'def two_sum(cisla, ciel):\n    pass\n',
                    'solution_code': 'def two_sum(cisla, ciel):\n    videnie = {}\n    for i, c in enumerate(cisla):\n        doplnok = ciel - c\n        if doplnok in videnie:\n            return (videnie[doplnok], i)\n        videnie[c] = i\n    return None\n',
                    'explanation_sk': 'Používame hešovaciu mapu hodnota -> index, vďaka čomu hľadáme doplnok v O(1).',
                    'explanation_en': 'Single pass hash map lookup storing seen value to index, achieving O(n) total time.',
                    'hint_sk': 'videnie = {}; for i, c in enumerate(cisla): if (ciel - c) in videnie: return (videnie[ciel - c], i).',
                    'hint_en': 'Hash seen numbers: if target - num in seen return (seen[target - num], i).',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'two_sum([2, 7, 11, 15], 9)', 'expected_output': '(0, 1)', 'test_code': 'assert two_sum([2, 7, 11, 15], 9) == (0, 1)', 'is_hidden': False},
                        {'input_data': 'two_sum([3, 2, 4], 6)', 'expected_output': '(1, 2)', 'test_code': 'assert two_sum([3, 2, 4], 6) == (1, 2)', 'is_hidden': False},
                        {'input_data': 'two_sum([1, 2, 3], 10)', 'expected_output': 'None', 'test_code': 'assert two_sum([1, 2, 3], 10) is None', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Vyhľadávacie algoritmy: Sekvenčné vs. Binárne vyhľadávanie',
            'title_en': 'Search Algorithms: Linear vs. Binary Search',
            'summary_sk': 'Sekvenčné prehľadávanie O(n), princíp binárneho delenia intervalu (Binary Search) v O(log n).',
            'summary_en': 'Linear sequential search O(n) vs logarithmic binary divide-and-conquer search O(log n).',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 11.2 Binárne vyhľadávanie (Binary Search)

V neutriedenom zozname musíme prejsť každý prvok postupne: **sekvenčné vyhľadávanie** má zložitosť $O(n)$.

Ak je však zoznam **vopred utriedený**, môžeme použiť **binárne vyhľadávanie** so zložitosťou **$O(\\log n)$**:
1. Pozrieme sa na prostredný prvok.
2. Ak je hľadané číslo menšie, zahodíme celú pravú polovicu.
3. Ak je väčšie, zahodíme celú ľavú polovicu.
4. V každom kroku zmenšíme prehľadávaný priestor na polovicu!

V zozname s 1 000 000 prvkami nájde binárne vyhľadávanie výsledok na najviac **20 porovnaní**!
""",
            'content_en': """### 11.2 Binary Search

Binary search operates in $O(\\log n)$ on sorted arrays by repeatedly halving the search interval.
""",
            'quizzes': [
                {
                    'question_sk': 'Aká je základná podmienka, aby sme na zozname mohli použiť binárne vyhľadávanie?',
                    'question_en': 'What prerequisite is required to execute a binary search on a list?',
                    'option_a_sk': 'Zoznam musí byť vopred zoradený (utriedený)', 'option_a_en': 'The list must be strictly sorted',
                    'option_b_sk': 'Zoznam musí obsahovať iba párne čísla', 'option_b_en': 'List must only contain even numbers',
                    'option_c_sk': 'Dĺžka zoznamu musí byť mocninou 2', 'option_c_en': 'Length must be a power of two',
                    'option_d_sk': 'V zozname nesmú byť záporné čísla', 'option_d_en': 'No negative numbers allowed',
                    'correct_option': 'A',
                    'explanation_sk': 'Princíp vyradenia polovice intervalu funguje len na usporiadanej postupnosti.',
                    'explanation_en': 'Halving intervals relies entirely on total monotonic ordering.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Implementácia binárneho vyhľadávania',
                    'title_en': 'Binary Search Implementation',
                    'instructions_sk': (
                        "Implementuj funkciu `binarne_vyhladavanie(zoradeny_zoznam, ciel)`:\n"
                        "- Využi ukazovatele `vlavo = 0` a `vpravo = len(zoradeny_zoznam) - 1`.\n"
                        "- V cykle `while vlavo <= vpravo` vypočítaj stred `stred = (vlavo + vpravo) // 2`.\n"
                        "- Ak prvok nájdeš, vráti jeho index.\n"
                        "- Ak prvok v zozname nie je, vráti `-1`."
                    ),
                    'instructions_en': 'Implement `binarne_vyhladavanie(zoradeny_zoznam, ciel)` returning item index or -1 in O(log n).',
                    'starter_code': 'def binarne_vyhladavanie(zoradeny_zoznam, ciel):\n    pass\n',
                    'solution_code': 'def binarne_vyhladavanie(zoradeny_zoznam, ciel):\n    vlavo = 0\n    vpravo = len(zoradeny_zoznam) - 1\n    while vlavo <= vpravo:\n        stred = (vlavo + vpravo) // 2\n        if zoradeny_zoznam[stred] == ciel:\n            return stred\n        elif zoradeny_zoznam[stred] < ciel:\n            vlavo = stred + 1\n        else:\n            vpravo = stred - 1\n    return -1\n',
                    'explanation_sk': 'Klasická iteratívna implementácia binárneho vyhľadávania.',
                    'explanation_en': 'Iterative binary search maintaining left and right pointers.',
                    'hint_sk': 'vlavo = 0; vpravo = len(zoradeny_zoznam) - 1; while vlavo <= vpravo: stred = (vlavo + vpravo) // 2.',
                    'hint_en': 'Two pointers tracking boundaries with midpoint calculation.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'binarne_vyhladavanie([2, 5, 8, 12, 16, 23, 38], 16)', 'expected_output': '4', 'test_code': 'assert binarne_vyhladavanie([2, 5, 8, 12, 16, 23, 38], 16) == 4', 'is_hidden': False},
                        {'input_data': 'binarne_vyhladavanie([1, 3, 5], 4)', 'expected_output': '-1', 'test_code': 'assert binarne_vyhladavanie([1, 3, 5], 4) == -1', 'is_hidden': False},
                        {'input_data': 'binarne_vyhladavanie([10, 20, 30, 40, 50], 10)', 'expected_output': '0', 'test_code': 'assert binarne_vyhladavanie([10, 20, 30, 40, 50], 10) == 0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Základné triediace algoritmy: Bubble Sort a porovnania',
            'title_en': 'Sorting Algorithms: Bubble Sort & Comparisons',
            'summary_sk': 'Princíp bublinkového triedenia (Bubble Sort), výmena susedných prvkov a kvadratická zložitosť O(n^2).',
            'summary_en': 'Bubble sort mechanics, adjacent element comparisons, in-place swaps, and quadratic runtime O(n^2).',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 11.3 Bubble Sort (Bublinkové triedenie)

Bubble Sort patrí medzi najjednoduchšie triediace algoritmy. Prechádza zoznam a porovnáva každé dva susedné prvky. Ak sú v nesprávnom poradí, vymení ich.

Najväčšie prvky postupne "vybublávajú" na koniec zoznamu ako bubliny vo vode.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        vymena = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                vymena = True
        if not vymena:
            break  # Optimalizácia: ak neprebehla výmena, zoznam je už utriedený!
    return arr
```
Časová zložitosť v najhoršom prípade je **$O(n^2)$**.
""",
            'content_en': """### 11.3 Bubble Sort

Simple $O(n^2)$ comparison sort repeatedly swapping adjacent out-of-order elements until settled.
""",
            'quizzes': [
                {
                    'question_sk': 'Aká je časová zložitosť algoritmu Bubble Sort v najhoršom prípade?',
                    'question_en': 'What is the worst-case time complexity of Bubble Sort?',
                    'option_a_sk': 'O(n^2)', 'option_a_en': 'O(n^2)',
                    'option_b_sk': 'O(n log n)', 'option_b_en': 'O(n log n)',
                    'option_c_sk': 'O(n)', 'option_c_en': 'O(n)',
                    'option_d_sk': 'O(1)', 'option_d_en': 'O(1)',
                    'correct_option': 'A',
                    'explanation_sk': 'Pretože obsahuje dva vnorené cykly idúce do n, počet porovnaní je úmerný n * (n - 1) / 2, teda O(n^2).',
                    'explanation_en': 'Nested loops result in quadratic comparisons: O(n^2).',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Počítadlo výmen v Bubble Sorte',
                    'title_en': 'Bubble Sort Swap Counter',
                    'instructions_sk': (
                        "Napíš funkciu `spocitaj_bubble_vymeny(zoznam)`, ktorá neutriedený zoznam utriedi vzostupne pomocou Bubble Sortu a vráti **počet výmen** (swaps), ktoré musel algoritmus vykonať.\n"
                        "Vstupný zoznam nemeň priamo (vytvor si kópiu)."
                    ),
                    'instructions_en': 'Write `spocitaj_bubble_vymeny(zoznam)` running bubble sort and returning total swap count.',
                    'starter_code': 'def spocitaj_bubble_vymeny(zoznam):\n    pass\n',
                    'solution_code': 'def spocitaj_bubble_vymeny(zoznam):\n    arr = list(zoznam)\n    n = len(arr)\n    vymeny = 0\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                vymeny += 1\n    return vymeny\n',
                    'explanation_sk': 'Pri každom splnení podmienky arr[j] > arr[j+1] inkrementujeme počítadlo výmen.',
                    'explanation_en': 'Execute bubble sort while maintaining a counter incremented on every adjacent swap.',
                    'hint_sk': 'if arr[j] > arr[j+1]: arr[j], arr[j+1] = arr[j+1], arr[j]; vymeny += 1.',
                    'hint_en': 'Increment counter on every swap.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'spocitaj_bubble_vymeny([5, 1, 4, 2, 8])', 'expected_output': '4', 'test_code': 'assert spocitaj_bubble_vymeny([5, 1, 4, 2, 8]) == 4', 'is_hidden': False},
                        {'input_data': 'spocitaj_bubble_vymeny([1, 2, 3])', 'expected_output': '0', 'test_code': 'assert spocitaj_bubble_vymeny([1, 2, 3]) == 0', 'is_hidden': False},
                        {'input_data': 'spocitaj_bubble_vymeny([3, 2, 1])', 'expected_output': '3', 'test_code': 'assert spocitaj_bubble_vymeny([3, 2, 1]) == 3', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Efektívne triedenie: Merge Sort a vlastné kľúče triedenia',
            'title_en': 'Efficient Sorting: Merge Sort & Custom Sort Keys',
            'summary_sk': 'Princíp Rozdeľ a panuj (Divide and Conquer), Merge Sort v O(n log n) a radenie cez key=lambda.',
            'summary_en': 'Divide and conquer paradigm, guaranteed O(n log n) Merge Sort, and Python lambda sort keys.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 11.4 Merge Sort a vlastné kľúče triedenia

**Merge Sort** využíva stratégiu **Rozdeľ a panuj (Divide & Conquer)**:
1. Rozdelí zoznam na dve polovice.
2. Rekurzívne utriedi každú polovicu.
3. Zleje (merge) dve utriedené polovice do jedného celku v čase $O(n)$.

Vďaka tomu má garantovanú zložitosť **$O(n \\log n)$** aj v najhoršom prípade!

#### Vlastné kľúče triedenia v Pythone (`key=lambda`):
```python
hraci = [
    {"meno": "Juraj", "skore": 250},
    {"meno": "Martin", "skore": 410},
    {"meno": "Petra", "skore": 180}
]

# Zoradenie zostupne podľa skóre:
hraci.sort(key=lambda h: h["skore"], reverse=True)
```
""",
            'content_en': """### 11.4 Merge Sort & Custom Key Sorting

Merge Sort guarantees $O(n \\log n)$ worst-case complexity by recursively splitting and merging halves. In Python, customize ordering with `sorted(arr, key=lambda x: ...)`.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú stratégiu algoritmického návrhu využíva triediaci algoritmus Merge Sort?',
                    'question_en': 'What algorithmic design paradigm does Merge Sort utilize?',
                    'option_a_sk': 'Rozdeľ a panuj (Divide and Conquer)', 'option_a_en': 'Divide and Conquer',
                    'option_b_sk': 'Hladný algoritmus (Greedy)', 'option_b_en': 'Greedy approach',
                    'option_c_sk': 'Hrubá sila (Brute Force)', 'option_c_en': 'Brute Force',
                    'option_d_sk': 'Dynamické programovanie', 'option_d_en': 'Dynamic programming',
                    'correct_option': 'A',
                    'explanation_sk': 'Merge sort rekurzívne rozdeľuje problém na menšie polovice a následne ich spája.',
                    'explanation_en': 'Merge Sort recursively splits inputs until subproblems are trivial, then merges.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Zoradenie rebríčka študentov s viacerými kritériami',
                    'title_en': 'Multi-Criteria Leaderboard Sort',
                    'instructions_sk': (
                        "Napíš funkciu `zorad_rebricek(studenti)`:\n"
                        "Vstupom je zoznam slovníkov `[{\"meno\": \"A\", \"xp\": 100, \"doros\": 50}, ...]`.\n"
                        "Zoraď študentov primárne podľa `xp` zostupne. Ak majú dvaja rovnaké XP, zoraď ich sekundárne podľa `doros` zostupne.\n"
                        "Použi vstavanú funkciu `sorted()` s `key=lambda` vracajúcou n-ticu `(-s['xp'], -s['doros'])`."
                    ),
                    'instructions_en': 'Write `zorad_rebricek(studenti)` sorting descending by XP, then descending by Doros using lambda tuple key.',
                    'starter_code': 'def zorad_rebricek(studenti):\n    pass\n',
                    'solution_code': 'def zorad_rebricek(studenti):\n    return sorted(studenti, key=lambda s: (-s.get("xp", 0), -s.get("doros", 0)))\n',
                    'explanation_sk': 'Využívame záporné znamienko v tuple kľúči pre zostupné radenie čísel.',
                    'explanation_en': 'Tuple sort key with negative values cleanly reverses multi-column ordering.',
                    'hint_sk': 'return sorted(studenti, key=lambda s: (-s["xp"], -s["doros"])).',
                    'hint_en': 'return sorted(studenti, key=lambda s: (-s["xp"], -s["doros"])).',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'zorad_rebricek([{"meno": "A", "xp": 100, "doros": 20}, {"meno": "B", "xp": 200, "doros": 10}, {"meno": "C", "xp": 100, "doros": 50}])', 'expected_output': '[{"meno": "B", "xp": 200, "doros": 10}, {"meno": "C", "xp": 100, "doros": 50}, {"meno": "A", "xp": 100, "doros": 20}]', 'test_code': 'res = zorad_rebricek([{"meno": "A", "xp": 100, "doros": 20}, {"meno": "B", "xp": 200, "doros": 10}, {"meno": "C", "xp": 100, "doros": 50}])\nassert [s["meno"] for s in res] == ["B", "C", "A"]', 'is_hidden': False},
                        {'input_data': 'zorad_rebricek([])', 'expected_output': '[]', 'test_code': 'assert zorad_rebricek([]) == []', 'is_hidden': False},
                        {'input_data': 'zorad_rebricek([{"meno": "X", "xp": 500, "doros": 0}])', 'expected_output': '[{"meno": "X", "xp": 500, "doros": 0}]', 'test_code': 'assert len(zorad_rebricek([{"meno": "X", "xp": 500, "doros": 0}])) == 1', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Číselné a kryptografické algoritmy: Eratostenes, Caesar a Luhn',
            'title_en': 'Number Theory & Crypto: Eratosthenes, Caesar & Luhn',
            'summary_sk': 'Generovanie prvočísel sitom Eratostena, posunová Caesarova šifra a kontrolný súčet kreditných kariet Luhn.',
            'summary_en': 'Sieve of Eratosthenes prime generation, modular Caesar cipher substitution, and Luhn checksum formula.',
            'estimated_minutes': 60,
            'xp_reward': 45,
            'is_published': True,
            'content_sk': """### 11.5 Aplikovaná kryptografia a teória čísel

#### 1. Eratostenovo sito (Sieve of Eratosthenes)
Najrýchlejší klasický algoritmus na nájdenie všetkých prvočísel do limitu $N$ so zložitosťou $O(N \\log \\log N)$.

#### 2. Caesarova šifra (Caesar Cipher)
Substitučná šifra posúvajúca písmená v abecede o fixný kľúč $k$ pomocou modulárnej aritmetiky:
$c = (p + k) \\pmod{26}$.

#### 3. Luhnov algoritmus (Luhn Checksum)
Globálny bankový štandard (ISO/IEC 7812) na overenie validity čísiel kreditných kariet a identifikačných kódov:
- Zdvojenie každej druhej číslice sprava doľava.
- Ak je výsledok $> 9$, odpočíta sa 9.
- Celkový súčet musí byť deliteľný 10 (`suma % 10 == 0`).
""",
            'content_en': """### 11.5 Applied Cryptography & Luhn Checksum

Industrial mathematical algorithms: Sieve of Eratosthenes for prime tables, Caesar cipher modular rotations, and Luhn formula credit card checksum validation.
""",
            'quizzes': [
                {
                    'question_sk': 'Na čo slúži Luhnov algoritmus v reálnom bankovom softvéri?',
                    'question_en': 'What is the Luhn algorithm used for in commercial banking software?',
                    'option_a_sk': 'Na overenie matematickej validity a prevenciu preklepov v číslach kreditných kariet', 'option_a_en': 'To validate credit card numbers and detect mistyped digits',
                    'option_b_sk': 'Na šifrovanie hesla', 'option_b_en': 'Encrypting passwords',
                    'option_c_sk': 'Na výpočet úrokov hypotéky', 'option_c_en': 'Mortgage interest',
                    'option_d_sk': 'Na generovanie náhodných čísel', 'option_d_en': 'Random number generation',
                    'correct_option': 'A',
                    'explanation_sk': 'Luhnov algoritmus je overovací kontrolný vzorec (checksum) na detekciu preklepov.',
                    'explanation_en': 'The Luhn formula is a checksum formula used to validate identification numbers.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Implementácia Caesarovej šifry',
                    'title_en': 'Caesar Cipher Encoder',
                    'instructions_sk': (
                        "Napíš funkciu `caesar_sifra(text, posun)`, ktorá zašifruje text posunom písmen v abecede o hodnotu `posun` (1 až 25).\n"
                        "- Zachovaj veľkosť písmen (veľké písmeno zostane veľké, malé zostane malé).\n"
                        "- Znaky mimo anglickej abecedy (medzery, čísla, interpunkciu) ponechaj bezo zmeny.\n"
                        "Využi funkcie `ord()` a `chr()`."
                    ),
                    'instructions_en': 'Write `caesar_sifra(text, posun)` encoding English alphabet letters while preserving case and symbols.',
                    'starter_code': 'def caesar_sifra(text, posun):\n    pass\n',
                    'solution_code': 'def caesar_sifra(text, posun):\n    vysledok = []\n    for char in text:\n        if "a" <= char <= "z":\n            novy = chr((ord(char) - ord("a") + posun) % 26 + ord("a"))\n            vysledok.append(novy)\n        elif "A" <= char <= "Z":\n            novy = chr((ord(char) - ord("A") + posun) % 26 + ord("A"))\n            vysledok.append(novy)\n        else:\n            vysledok.append(char)\n    return "".join(vysledok)\n',
                    'explanation_sk': 'Využívame ord() na získanie ASCII kódu, modulárnu aritmetiku % 26 a chr() na návrat znaku.',
                    'explanation_en': 'Map ASCII codepoints through modulo 26 shifts using ord() and chr().',
                    'hint_sk': 'chr((ord(char) - ord("a") + posun) % 26 + ord("a")).',
                    'hint_en': 'chr((ord(char) - ord("a") + posun) % 26 + ord("a")).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'caesar_sifra("Hello, World!", 3)', 'expected_output': 'Khoor, Zruog!', 'test_code': 'assert caesar_sifra("Hello, World!", 3) == "Khoor, Zruog!"', 'is_hidden': False},
                        {'input_data': 'caesar_sifra("xyz", 1)', 'expected_output': 'yza', 'test_code': 'assert caesar_sifra("xyz", 1) == "yza"', 'is_hidden': False},
                        {'input_data': 'caesar_sifra("Codoro 2027", 5)', 'expected_output': 'Htitwt 2027', 'test_code': 'assert caesar_sifra("Codoro 2027", 5) == "Htitwt 2027"', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
