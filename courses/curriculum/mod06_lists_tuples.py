"""
MODUL 6: Dátové štruktúry I – Zoznamy, N-tice a matice
Odhadovaný rozsah: 14 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 6,
    'title_sk': 'Dátové štruktúry I – Zoznamy, N-tice a matice',
    'title_en': 'Data Structures I – Lists, Tuples & Matrices',
    'description_sk': 'Zoznám sa s fundamentálnymi sekvenčnými typmi Pythonu: meniteľnými zoznamami (list), nemennými n-ticami (tuple), metódami manipulácie, vstavanými funkciami enumerate/zip, list comprehensions a 2D maticami.',
    'description_en': 'Explore core sequential structures: mutable lists, immutable tuples, manipulation methods, enumerate/zip utilities, list comprehensions, and 2D matrix representations.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'collection',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Zoznamy (list): vytváranie, mutabilita a slicing',
            'title_en': 'Lists: Creation, Mutability & Slicing',
            'summary_sk': 'Syntax hranatých zátvoriek [], mutabilita prvkov v pamäti, indexovanie a podzoznamy.',
            'summary_en': 'List literal syntax [], in-place element mutation, indexing, and sub-list slicing.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 6.1 Zoznamy (`list`) v Pythone

Zoznam je usporiadaná, **meniteľná (mutable)** kolekcia prvkov, ktoré môžu byť ľubovoľného typu.

```python
inventar = ["meč", "štít", "elixír"]
print(inventar[0])  # 'meč'

# Mutabilita: prvky môžeme priamo prepísať
inventar[1] = "zlatý štít"
print(inventar)  # ['meč', 'zlatý štít', 'elixír']
```

Zoznamy podporujú rovnaký slicing `[start:stop:step]` ako reťazce:
```python
cisla = [0, 1, 2, 3, 4, 5]
print(cisla[1:4])  # [1, 2, 3]
```
""",
            'content_en': """### 6.1 Lists in Python

Lists are ordered, mutable sequences defined via square brackets `[]`.

```python
items = ["sword", "shield"]
items[0] = "axe"  # in-place modification
```
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je hlavný rozdiel medzi reťazcom (`str`) a zoznamom (`list`) z hľadiska pamäte?',
                    'question_en': 'What is the key difference between str and list regarding memory mutation?',
                    'option_a_sk': 'Zoznam je meniteľný (mutable), reťazec je nemenný (immutable)', 'option_a_en': 'List is mutable, string is immutable',
                    'option_b_sk': 'Reťazec je meniteľný, zoznam je nemenný', 'option_b_en': 'String is mutable, list is immutable',
                    'option_c_sk': 'V zozname nemôžu byť čísla', 'option_c_en': 'Lists cannot store numbers',
                    'option_d_sk': 'Medzi nimi nie je žiaden rozdiel', 'option_d_en': 'No difference',
                    'correct_option': 'A',
                    'explanation_sk': 'Prvky v zozname môžeme prepisovať (list je mutable), zatiaľ čo reťazec po vytvorení nie je možné v pamäti meniť (str je immutable).',
                    'explanation_en': 'Lists support item assignment, whereas strings raise TypeError when modified.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výmena prvého a posledného prvku',
                    'title_en': 'Swap First and Last Element',
                    'instructions_sk': (
                        "Napíš funkciu `vymen_krajne_prvky(zoznam)`, ktorá prijme zoznam a vráti **nový zoznam**, kde sú prvý a posledný prvok navzájom vymenené.\n"
                        "Ak má zoznam menej ako 2 prvky, vráti jeho kópiu bezo zmeny."
                    ),
                    'instructions_en': 'Write `vymen_krajne_prvky(zoznam)` returning a new list with first and last elements swapped.',
                    'starter_code': 'def vymen_krajne_prvky(zoznam):\n    pass\n',
                    'solution_code': 'def vymen_krajne_prvky(zoznam):\n    if len(zoznam) < 2:\n        return list(zoznam)\n    kopia = list(zoznam)\n    kopia[0], kopia[-1] = kopia[-1], kopia[0]\n    return kopia\n',
                    'explanation_sk': 'Vytvoríme kópiu cez list() a vymeníme prvky pomocou viacnásobného priradenia.',
                    'explanation_en': 'Copy list, then perform pythonic tuple swap: kopia[0], kopia[-1] = kopia[-1], kopia[0].',
                    'hint_sk': 'kopia = list(zoznam); kopia[0], kopia[-1] = kopia[-1], kopia[0]; return kopia.',
                    'hint_en': 'kopia = list(zoznam); kopia[0], kopia[-1] = kopia[-1], kopia[0]; return kopia.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vymen_krajne_prvky([1, 2, 3, 4])', 'expected_output': '[4, 2, 3, 1]', 'test_code': 'assert vymen_krajne_prvky([1, 2, 3, 4]) == [4, 2, 3, 1]', 'is_hidden': False},
                        {'input_data': 'vymen_krajne_prvky([42])', 'expected_output': '[42]', 'test_code': 'assert vymen_krajne_prvky([42]) == [42]', 'is_hidden': False},
                        {'input_data': 'vymen_krajne_prvky(["a", "b", "c"])', 'expected_output': '["c", "b", "a"]', 'test_code': 'assert vymen_krajne_prvky(["a", "b", "c"]) == ["c", "b", "a"]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Metódy zoznamov: append, extend, pop, remove a sort',
            'title_en': 'List Methods: append, extend, pop, remove & sort',
            'summary_sk': 'Pridávanie prvkov (append vs. extend), odstraňovanie (pop vs. remove) a triedenie zoznamov.',
            'summary_en': 'Adding items (append vs extend), removal (pop vs remove), in-place sorting and reversals.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 6.2 Najdôležitejšie metódy zoznamov

1. `zoznam.append(prvok)` – pridá jeden prvok na koniec zoznamu ($O(1)$).
2. `zoznam.extend(iny_zoznam)` – pridá všetky prvky inej kolekcie na koniec.
3. `zoznam.insert(index, prvok)` – vloží prvok na zadanú pozíciu ($O(n)$).
4. `zoznam.pop(index=-1)` – odstráni a vráti prvok (štandardne posledný).
5. `zoznam.remove(hodnota)` – nájde a vymaže prvý výskyt zadanej hodnoty.
6. `zoznam.sort()` – zoradí zoznam na mieste (in-place) pomocou Timsort algoritmu.
7. `zoznam.reverse()` – obráti poradie prvkov na mieste.

```python
body = [10, 50, 20]
body.append(40)     # [10, 50, 20, 40]
body.sort()         # [10, 20, 40, 50]
vybrate = body.pop()  # 50
```
""",
            'content_en': """### 6.2 Key List Methods

- `append(x)` adds item to tail
- `extend(iterable)` unpacks sequence to tail
- `pop()` removes and returns last item
- `remove(val)` deletes first occurrence of val
- `sort()` in-place Timsort ascending
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je rozdiel medzi `zoznam.append([1, 2])` a `zoznam.extend([1, 2])`?',
                    'question_en': 'What is the difference between `append([1, 2])` and `extend([1, 2])`?',
                    'option_a_sk': 'append pridá celý podzoznam ako 1 prvok; extend pridá čísla 1 a 2 ako dva samostatné prvky', 'option_a_en': 'append adds the list as a single nested element; extend unpacks both numbers as separate items',
                    'option_b_sk': 'Sú to úplné synonymá', 'option_b_en': 'They are identical',
                    'option_c_sk': 'extend funguje iba na text', 'option_c_en': 'extend works only on strings',
                    'option_d_sk': 'append vyvolá chybu pri zozname', 'option_d_en': 'append raises error',
                    'correct_option': 'A',
                    'explanation_sk': 'append vloží argument presne ako jeden objekt (aj keby to bol zoznam), extend ho rozbalí.',
                    'explanation_en': 'append inserts the object verbatim; extend iterates the collection and appends elements individually.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Filtrovanie a zoradenie unikátnych čísel',
                    'title_en': 'Unique Elements Filter & Sort',
                    'instructions_sk': (
                        "Napíš funkciu `filtruj_a_zorad(zoznam)`, ktorá vezme zoznam čísel a vráti nový zoznam, ktorý:\n"
                        "1. Obsahuje iba kladné čísla ($> 0$).\n"
                        "2. Neobsahuje duplicity (každé číslo je tam najviac raz).\n"
                        "3. Je zoradený vzostupne."
                    ),
                    'instructions_en': 'Write `filtruj_a_zorad(zoznam)` returning sorted list of unique positive numbers.',
                    'starter_code': 'def filtruj_a_zorad(zoznam):\n    pass\n',
                    'solution_code': 'def filtruj_a_zorad(zoznam):\n    kladne = set(x for x in zoznam if x > 0)\n    return sorted(list(kladne))\n',
                    'explanation_sk': 'Prevodom na množinu set odstránime duplicity a sorted() vráti zoradený zoznam.',
                    'explanation_en': 'Filter positive values into a set to eliminate duplicates and sort with sorted().',
                    'hint_sk': 'Použi set(x for x in zoznam if x > 0) a vráť sorted(list(...)).',
                    'hint_en': 'Use set(x for x in zoznam if x > 0) and return sorted(list(...)).',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'filtruj_a_zorad([5, -2, 10, 5, 0, 3, -1])', 'expected_output': '[3, 5, 10]', 'test_code': 'assert filtruj_a_zorad([5, -2, 10, 5, 0, 3, -1]) == [3, 5, 10]', 'is_hidden': False},
                        {'input_data': 'filtruj_a_zorad([-5, -10])', 'expected_output': '[]', 'test_code': 'assert filtruj_a_zorad([-5, -10]) == []', 'is_hidden': False},
                        {'input_data': 'filtruj_a_zorad([1, 1, 1, 1])', 'expected_output': '[1]', 'test_code': 'assert filtruj_a_zorad([1, 1, 1, 1]) == [1]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Funkcie enumerate(), zip() a vstavané agregácie',
            'title_en': 'enumerate(), zip() & Built-in Aggregations',
            'summary_sk': 'Získanie indexu a hodnoty cez enumerate(), párovanie zoznamov cez zip() a funkcie min/max/sum/len.',
            'summary_en': 'Indexed iteration with enumerate(), multi-list parallel iteration via zip(), and aggregations.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 6.3 `enumerate()`, `zip()` a agregácie

#### `enumerate(zoznam, start=0)`
Umožňuje iterovať cez hodnoty a zároveň mať k dispozícii ich poradové číslo (index) bez manuálneho počítadla:
```python
ziaci = ["Juraj", "Martin", "Petra"]
for index, meno in enumerate(ziaci, start=1):
    print(f"{index}. žiak: {meno}")
```

#### `zip(zoznam1, zoznam2)`
Spája korešpondujúce prvky z viacerých zoznamov do dvojíc:
```python
predmety = ["Python", "Matematika", "Fyzika"]
znamky = [1, 2, 1]

for p, z in zip(predmety, znamky):
    print(f"{p}: {z}")
```
""",
            'content_en': """### 6.3 `enumerate()`, `zip()` and Aggregations

- `enumerate(iterable, start=0)` produces (index, item) pairs.
- `zip(seq1, seq2)` iterates through sequences in lockstep.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo vráti výraz `list(zip(["A", "B"], [1, 2]))`?',
                    'question_en': 'What does `list(zip(["A", "B"], [1, 2]))` produce?',
                    'option_a_sk': '[("A", 1), ("B", 2)]', 'option_a_en': '[("A", 1), ("B", 2)]',
                    'option_b_sk': '["A1", "B2"]', 'option_b_en': '["A1", "B2"]',
                    'option_c_sk': '{"A": 1, "B": 2}', 'option_c_en': '{"A": 1, "B": 2}',
                    'option_d_sk': '[["A", "B"], [1, 2]]', 'option_d_en': '[["A", "B"], [1, 2]]',
                    'correct_option': 'A',
                    'explanation_sk': 'Funkcia zip() spája prvky z rovnakých indexov do n-tíc (tuples).',
                    'explanation_en': 'zip() packs pairwise items into tuples.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet váženého priemeru známok',
                    'title_en': 'Weighted Average Grade Calculator',
                    'instructions_sk': (
                        "Napíš funkciu `vazeny_priemer(znamky, vahy)`, ktorá prijme dva zoznamy rovnakej dĺžky (známky a ich váhy).\n"
                        "Vážený priemer je definovaný ako $\\frac{\\sum (znamka \\cdot vaha)}{\\sum vaha}$.\n"
                        "Použi funkciu `zip()`. Výsledok zaokrúhli na 2 desatinné miesta. Ak je zoznam prázdny alebo je súčet váh 0, vráti `0.0`."
                    ),
                    'instructions_en': 'Write `vazeny_priemer(znamky, vahy)` calculating weighted average rounded to 2 decimals using zip().',
                    'starter_code': 'def vazeny_priemer(znamky, vahy):\n    pass\n',
                    'solution_code': 'def vazeny_priemer(znamky, vahy):\n    if not znamky or not vahy or sum(vahy) == 0:\n        return 0.0\n    sucin = sum(z * v for z, v in zip(znamky, vahy))\n    return round(sucin / sum(vahy), 2)\n',
                    'explanation_sk': 'Využívame zip na prepojenie známok s váhami a výpočet váženého súčtu.',
                    'explanation_en': 'Compute dot product of grades and weights divided by total weight.',
                    'hint_sk': 'sucin = sum(z * v for z, v in zip(znamky, vahy)); return round(sucin / sum(vahy), 2).',
                    'hint_en': 'sucin = sum(z * v for z, v in zip(znamky, vahy)); return round(sucin / sum(vahy), 2).',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'vazeny_priemer([1, 2, 3], [1, 2, 1])', 'expected_output': '2.0', 'test_code': 'assert vazeny_priemer([1, 2, 3], [1, 2, 1]) == 2.0', 'is_hidden': False},
                        {'input_data': 'vazeny_priemer([1, 5], [10, 1])', 'expected_output': '1.36', 'test_code': 'assert vazeny_priemer([1, 5], [10, 1]) == 1.36', 'is_hidden': False},
                        {'input_data': 'vazeny_priemer([], [])', 'expected_output': '0.0', 'test_code': 'assert vazeny_priemer([], []) == 0.0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Generátory zoznamov (List Comprehensions)',
            'title_en': 'List Comprehensions',
            'summary_sk': 'Syntax [výraz for prvok in kolekcia if podmienka], elegancia a rýchlosť v Pythone.',
            'summary_en': 'Syntactic sugar [expr for item in iterable if condition], performance, and clarity.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 6.4 List Comprehensions (Generovanie zoznamov)

List comprehension je jeden z najobľúbenejších a najviac "pythonických" nástrojov. Umožňuje nahradiť viacriadkový cyklus `for` jedným vysoko čitateľným riadkom.

#### Štandardná syntax:
`[vyraz for prvok in postupnost if podmienka]`

```python
# Klasický zápis (3 riadky):
stvorce = []
for x in range(1, 6):
    stvorce.append(x ** 2)

# Pythonický zápis (1 riadok):
stvorce = [x ** 2 for x in range(1, 6)]
print(stvorce)  # [1, 4, 9, 16, 25]

# S filtrovaním:
parne_stvorce = [x ** 2 for x in range(1, 10) if x % 2 == 0]
```
List comprehensions sú implementované v C, preto sú **rýchlejšie** než bežné manuálne volanie `.append()`.
""",
            'content_en': """### 6.4 List Comprehensions

Transform and filter sequences concisely:

```python
squares = [x ** 2 for x in range(10) if x % 2 == 0]
```
""",
            'quizzes': [
                {
                    'question_sk': 'Aký zoznam vytvorí výraz `[len(s) for s in ["pes", "macka", "had"]]`?',
                    'question_en': 'What list does `[len(s) for s in ["pes", "macka", "had"]]` create?',
                    'option_a_sk': '[3, 5, 3]', 'option_a_en': '[3, 5, 3]',
                    'option_b_sk': '[1, 2, 3]', 'option_b_en': '[1, 2, 3]',
                    'option_c_sk': '["3", "5", "3"]', 'option_c_en': '["3", "5", "3"]',
                    'option_d_sk': '11', 'option_d_en': '11',
                    'correct_option': 'A',
                    'explanation_sk': 'len("pes") je 3, len("macka") je 5, len("had") je 3.',
                    'explanation_en': 'Computes string lengths for each word: [3, 5, 3].',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Filtrovanie dĺžky slov cez List Comprehension',
                    'title_en': 'Word Length Filter with List Comprehension',
                    'instructions_sk': (
                        "Napíš funkciu `dlhe_slova_velkymi(text, min_dlzka)`, ktorá rozdelí vstupný reťazec na slová (pomocou `.split()`) a vráti zoznam tých slov, ktoré majú aspoň `min_dlzka` znakov, prevedených na VEĽKÉ PÍSMENÁ (`.upper()`).\n"
                        "Použi List Comprehension."
                    ),
                    'instructions_en': 'Write `dlhe_slova_velkymi(text, min_dlzka)` returning uppercase words having at least min_dlzka letters.',
                    'starter_code': 'def dlhe_slova_velkymi(text, min_dlzka):\n    pass\n',
                    'solution_code': 'def dlhe_slova_velkymi(text, min_dlzka):\n    return [w.upper() for w in text.split() if len(w) >= min_dlzka]\n',
                    'explanation_sk': 'Jednoriadkový list comprehension s filtrovaním dĺžky a transformáciou na upper().',
                    'explanation_en': 'One-liner list comprehension applying upper() and len() filter.',
                    'hint_sk': 'return [w.upper() for w in text.split() if len(w) >= min_dlzka].',
                    'hint_en': 'return [w.upper() for w in text.split() if len(w) >= min_dlzka].',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'dlhe_slova_velkymi("Codoro je skvela vzdelavacia platforma", 6)', 'expected_output': '["CODORO", "SKVELA", "VZDELAVACIA", "PLATFORMA"]', 'test_code': 'assert dlhe_slova_velkymi("Codoro je skvela vzdelavacia platforma", 6) == ["CODORO", "SKVELA", "VZDELAVACIA", "PLATFORMA"]', 'is_hidden': False},
                        {'input_data': 'dlhe_slova_velkymi("ja a ty", 3)', 'expected_output': '[]', 'test_code': 'assert dlhe_slova_velkymi("ja a ty", 3) == []', 'is_hidden': False},
                        {'input_data': 'dlhe_slova_velkymi("Python algoritmy", 7)', 'expected_output': '["ALGORITMY"]', 'test_code': 'assert dlhe_slova_velkymi("Python algoritmy", 7) == ["ALGORITMY"]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'N-tice (tuple), rozbaľovanie a 2D matice',
            'title_en': 'Tuples, Unpacking & 2D Matrices',
            'summary_sk': 'Nemenné n-tice (), tuple unpacking, reprezentácia tabuliek cez matice a capstone projekt.',
            'summary_en': 'Immutable tuples, tuple unpacking, row-column matrices, and capstone challenge.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 6.5 N-tice (`tuple`) a 2D matice

`tuple` je nemenná (immutable) sekvencia hodnôt uzatvorená v okrúhlych zátvorkách `()`. Je pamäťovo úspornejšia než zoznam a chráni dáta pred náhodnou zmenou.

#### Tuple Unpacking (Rozbaľovanie):
```python
suradnice = (10, 20)
x, y = suradnice  # x = 10, y = 20
```

#### Transpozícia 2D matice:
Matica je zoznam riadkov: `[[1, 2], [3, 4]]`. Jej otočenie (stĺpce sa stanú riadkami) sa v Pythone dá elegantne zapísať pomocou `zip(*matica)`:
```python
m = [[1, 2, 3], [4, 5, 6]]
transponovana = [list(stlpec) for stlpec in zip(*m)]
# [[1, 4], [2, 5], [3, 6]]
```
""",
            'content_en': """### 6.5 Tuples & 2D Matrices

Tuples are immutable sequence types. Matrix transposition in Python is idiomatically performed with `zip(*matrix)`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý zápis vytvorí jednoprvkový tuple s číslom 5 v Pythone?',
                    'question_en': 'Which syntax creates a 1-element tuple containing 5 in Python?',
                    'option_a_sk': '(5,)', 'option_a_en': '(5,)',
                    'option_b_sk': '(5)', 'option_b_en': '(5)',
                    'option_c_sk': '[5]', 'option_c_en': '[5]',
                    'option_d_sk': 'tuple(5)', 'option_d_en': 'tuple(5)',
                    'correct_option': 'A',
                    'explanation_sk': 'Čiarka je v Pythone kľúčová: (5) je iba číslo v zátvorke, zatiaľ čo (5,) je jednoprvkový tuple.',
                    'explanation_en': 'A trailing comma is mandatory for single-element tuples: (5,).',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Transpozícia matice (Matrix Transposition)',
                    'title_en': 'Matrix Transpose Function',
                    'instructions_sk': (
                        "Napíš funkciu `transponuj_maticu(matica)`, ktorá prijme 2D zoznam (maticu s rozmermi $R \\times S$) a vráti novú maticu s rozmermi $S \\times R$, kde riadky a stĺpce sú zamenené.\n"
                        "Ak je matica prázdna, vráti `[]`."
                    ),
                    'instructions_en': 'Write `transponuj_maticu(matica)` transposing an R x C matrix into a C x R matrix.',
                    'starter_code': 'def transponuj_maticu(matica):\n    pass\n',
                    'solution_code': 'def transponuj_maticu(matica):\n    if not matica or not matica[0]:\n        return []\n    return [list(stlpec) for stlpec in zip(*matica)]\n',
                    'explanation_sk': 'Využívame operátor rozbalenia *matica a zip na otočenie riadkov na stĺpce.',
                    'explanation_en': 'Idiomatic matrix transpose using zip(*matrix) converted back to nested lists.',
                    'hint_sk': 'if not matica: return []; return [list(col) for col in zip(*matica)].',
                    'hint_en': 'if not matica: return []; return [list(col) for col in zip(*matica)].',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'transponuj_maticu([[1, 2, 3], [4, 5, 6]])', 'expected_output': '[[1, 4], [2, 5], [3, 6]]', 'test_code': 'assert transponuj_maticu([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]', 'is_hidden': False},
                        {'input_data': 'transponuj_maticu([[1, 2], [3, 4]])', 'expected_output': '[[1, 3], [2, 4]]', 'test_code': 'assert transponuj_maticu([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]', 'is_hidden': False},
                        {'input_data': 'transponuj_maticu([])', 'expected_output': '[]', 'test_code': 'assert transponuj_maticu([]) == []', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
