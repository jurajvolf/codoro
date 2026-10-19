"""
MODUL 7: Dátové štruktúry II – Slovníky, Množiny a JSON dáta
Odhadovaný rozsah: 12 hodín | Náročnosť: BEGINNER | Úroveň: FREE
"""

MODULE_DATA = {
    'order': 7,
    'title_sk': 'Dátové štruktúry II – Slovníky, Množiny a JSON dáta',
    'title_en': 'Data Structures II – Dictionaries, Sets & JSON',
    'description_sk': 'Nauč sa pracovať s hešovacími štruktúrami: asociatívnymi poľami (dict) s prístupom v O(1), bezpečnou metódou get(), množinami (set) a ich matematickými operáciami, ako aj parsovaním JSON dát.',
    'description_en': 'Master hash-based collections: key-value dictionaries (dict) with O(1) lookups, safe get() retrieval, unique sets, set theory operations, and JSON data parsing.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'BEGINNER',
    'is_pro_only': False,
    'icon_name': 'book',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Slovníky (dict): páry kľúč-hodnota a metóda get()',
            'title_en': 'Dictionaries: Key-Value Pairs & the get() Method',
            'summary_sk': 'Syntax zložených zátvoriek {}, hešovateľné kľúče, rýchlosť vyhľadávania O(1) a prevencia KeyError cez get().',
            'summary_en': 'Brace syntax {}, hashable keys, O(1) average lookup, and safe get() retrieval.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 7.1 Slovníky (`dict`) v Pythone

Slovník je asociatívne pole uchovávajúce **páry kľúč: hodnota**. Vďaka hešovacej tabuľke (Hash Map) je vyhľadanie hodnoty podľa kľúča bleskové: **$O(1)$** bez ohľadu na počet položiek!

```python
student = {
    "meno": "Juraj",
    "trieda": "IV.C",
    "doros": 350
}

# Prístup cez hranaté zátvorky (ak kľúč neexistuje, vyvolá KeyError!):
print(student["meno"])  # 'Juraj'

# Bezpečný prístup cez .get(kluc, default):
bonus = student.get("bonus", 0)  # Vráti 0, nevyvolá chybu!
```
Kľúčom v slovníku môže byť iba **nemenný (hashable)** typ: `str`, `int`, `tuple`.
""",
            'content_en': """### 7.1 Dictionaries in Python

Key-value pairs backed by hash tables for $O(1)$ average time lookups.

- `dict[key]` raises KeyError if missing.
- `dict.get(key, default)` returns fallback value safely.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý dátový typ NEMÔŽE byť použitý ako kľúč v slovníku (`dict`)?',
                    'question_en': 'Which data type CANNOT be used as a dictionary key?',
                    'option_a_sk': 'Zoznam (list)', 'option_a_en': 'List',
                    'option_b_sk': 'Reťazec (str)', 'option_b_en': 'String (str)',
                    'option_c_sk': 'Celé číslo (int)', 'option_c_en': 'Integer (int)',
                    'option_d_sk': 'N-tica obsahujúca iba čísla (tuple)', 'option_d_en': 'Tuple of numbers',
                    'correct_option': 'A',
                    'explanation_sk': 'Kľúče v slovníku musia byť nemenné (hashable). Zoznam je meniteľný (mutable), preto vyvolá TypeError: unhashable type.',
                    'explanation_en': 'Dictionary keys must be hashable. Lists are mutable and unhashable.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Prevodník mien a kurzový lístok',
                    'title_en': 'Currency Converter Lookup',
                    'instructions_sk': (
                        "Napíš funkciu `preved_menu(suma_eur, mena, kurzovy_listok)`, kde `kurzovy_listok` je slovník ako `{\"USD\": 1.08, \"CZK\": 25.2}`.\n"
                        "Funkcia vráti prepočítanú sumu (suma * kurz) zaokrúhlenú na 2 desatinné miesta.\n"
                        "Ak mena v kurzovom lístku nie je, vráti `None`."
                    ),
                    'instructions_en': 'Write `preved_menu(suma_eur, mena, kurzovy_listok)` returning converted currency rounded to 2 decimals or None if not found.',
                    'starter_code': 'def preved_menu(suma_eur, mena, kurzovy_listok):\n    pass\n',
                    'solution_code': 'def preved_menu(suma_eur, mena, kurzovy_listok):\n    kurz = kurzovy_listok.get(mena)\n    if kurz is None:\n        return None\n    return round(suma_eur * kurz, 2)\n',
                    'explanation_sk': 'Využívame metódu .get(mena) na bezpečné zistenie kurzu.',
                    'explanation_en': 'Safe dictionary lookup with get() and rounding.',
                    'hint_sk': 'kurz = kurzovy_listok.get(mena); if kurz is None: return None; return round(suma_eur * kurz, 2).',
                    'hint_en': 'kurz = kurzovy_listok.get(mena); if kurz is None: return None; return round(suma_eur * kurz, 2).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'preved_menu(100, "USD", {"USD": 1.08, "CZK": 25.2})', 'expected_output': '108.0', 'test_code': 'assert preved_menu(100, "USD", {"USD": 1.08, "CZK": 25.2}) == 108.0', 'is_hidden': False},
                        {'input_data': 'preved_menu(50, "GBP", {"USD": 1.08})', 'expected_output': 'None', 'test_code': 'assert preved_menu(50, "GBP", {"USD": 1.08}) is None', 'is_hidden': False},
                        {'input_data': 'preved_menu(20, "CZK", {"CZK": 25.333})', 'expected_output': '506.66', 'test_code': 'assert preved_menu(20, "CZK", {"CZK": 25.333}) == 506.66', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Iterovanie cez slovníky a Dict Comprehensions',
            'title_en': 'Dictionary Iteration & Dict Comprehensions',
            'summary_sk': 'Prechádzanie cez .keys(), .values(), .items() a generovanie slovníkov v jednom riadku.',
            'summary_en': 'Iterating keys(), values(), items() and syntax {k: v for k, v in ...}.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 7.2 Iterovanie a Dict Comprehensions

Pri prechádzaní slovníka máme tri možnosti:
1. `for k in d.keys():` – iba kľúče (rovnako funguje `for k in d:`).
2. `for v in d.values():` – iba hodnoty.
3. `for k, v in d.items():` – dvojice kľúč aj hodnota (najčastejšie).

```python
ceny = {"káva": 2.50, "čaj": 1.80, "koláč": 3.00}

for tovar, cena in ceny.items():
    print(f"{tovar}: {cena:.2f} €")
```

#### Dict Comprehensions:
`{novy_kluc: nova_hodnota for k, v in d.items() if podmienka}`

```python
# Zvýšenie všetkých cien o 10%:
nove_ceny = {k: round(v * 1.10, 2) for k, v in ceny.items()}
```
""",
            'content_en': """### 7.2 Dict Comprehensions & Iteration

Iterate keys, values, or items using `.items()`. Create new dictionaries with dict comprehension `{k: v for ...}`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá metóda slovníka vracia dvojice (kľúč, hodnota) vhodné na rozbalenie v cykle for?',
                    'question_en': 'Which dictionary method returns (key, value) pairs for unpacking in a for loop?',
                    'option_a_sk': '.items()', 'option_a_en': '.items()',
                    'option_b_sk': '.pairs()', 'option_b_en': '.pairs()',
                    'option_c_sk': '.entries()', 'option_c_en': '.entries()',
                    'option_d_sk': '.values()', 'option_d_en': '.values()',
                    'correct_option': 'A',
                    'explanation_sk': 'Metóda .items() vracia zobrazenie dvojíc (kľúč, hodnota).',
                    'explanation_en': '.items() returns dynamic view of key-value tuples.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Inverzný slovník (Otočenie kľúčov a hodnôt)',
                    'title_en': 'Invert Dictionary Mapping',
                    'instructions_sk': (
                        "Napíš funkciu `invertuj_slovnik(slovnik)`, ktorá otočí kľúče a hodnoty tak, že pôvodné hodnoty sa stanú kľúčmi a pôvodné kľúče ich hodnotami.\n"
                        "Predpokladaj, že všetky hodnoty sú unikátne a hashable. Použi Dict Comprehension."
                    ),
                    'instructions_en': 'Write `invertuj_slovnik(slovnik)` swapping keys and values using dict comprehension.',
                    'starter_code': 'def invertuj_slovnik(slovnik):\n    pass\n',
                    'solution_code': 'def invertuj_slovnik(slovnik):\n    return {v: k for k, v in slovnik.items()}\n',
                    'explanation_sk': 'Jednoduché dict comprehension prehodením v: k.',
                    'explanation_en': 'Compact dict comprehension mapping v: k over .items().',
                    'hint_sk': 'return {v: k for k, v in slovnik.items()}.',
                    'hint_en': 'return {v: k for k, v in slovnik.items()}.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'invertuj_slovnik({"sk": "Slovensko", "cz": "Cesko"})', 'expected_output': '{"Slovensko": "sk", "Cesko": "cz"}', 'test_code': 'assert invertuj_slovnik({"sk": "Slovensko", "cz": "Cesko"}) == {"Slovensko": "sk", "Cesko": "cz"}', 'is_hidden': False},
                        {'input_data': 'invertuj_slovnik({})', 'expected_output': '{}', 'test_code': 'assert invertuj_slovnik({}) == {}', 'is_hidden': False},
                        {'input_data': 'invertuj_slovnik({1: "one", 2: "two"})', 'expected_output': '{"one": 1, "two": 2}', 'test_code': 'assert invertuj_slovnik({1: "one", 2: "two"}) == {"one": 1, "two": 2}', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Vnorené slovníky a štruktúra JSON dát',
            'title_en': 'Nested Dictionaries & JSON Data Representation',
            'summary_sk': 'Práca s vnorenými štruktúrami, modul json (dumps, loads) a reprezentácia API dát.',
            'summary_en': 'Complex nested structures, python json module (dumps/loads), and API payload manipulation.',
            'estimated_minutes': 55,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 7.3 Vnorené slovníky a JSON

V modernej praxi webových aplikácií (napr. Django REST API) sú dáta reprezentované vo formáte **JSON (JavaScript Object Notation)**, čo v Pythone zodpovedá kombinácii vnorených slovníkov a zoznamov.

```python
skola = {
    "trieda": "IV.C",
    "studenti": [
        {"id": 1, "meno": "Juraj", "doros": 350},
        {"id": 2, "meno": "Martin", "doros": 520}
    ]
}

# Prístup do hĺbky:
print(skola["studenti"][0]["meno"])  # 'Juraj'
```

Vstavaný modul `json`:
- `json.dumps(obj)` – prevedie Python slovník na reťazec JSON.
- `json.loads(text)` – načíta reťazec JSON a prevedie ho na Python slovník.
""",
            'content_en': """### 7.3 Nested Dictionaries & JSON

Nested dictionaries represent hierarchical data matching JSON formatting. Module `json` provides `loads` and `dumps`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá funkcia modulu `json` prevedie reťazec JSON na Python slovník?',
                    'question_en': 'Which json module function deserializes a JSON string into a Python dict?',
                    'option_a_sk': 'json.loads()', 'option_a_en': 'json.loads()',
                    'option_b_sk': 'json.dumps()', 'option_b_en': 'json.dumps()',
                    'option_c_sk': 'json.parse()', 'option_c_en': 'json.parse()',
                    'option_d_sk': 'json.to_dict()', 'option_d_en': 'json.to_dict()',
                    'correct_option': 'A',
                    'explanation_sk': 'json.loads() (load string) načíta reťazec JSON do dátových typov Pythonu.',
                    'explanation_en': 'json.loads deserializes a string to Python objects.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Agregácia bodov študentov z API zoznamu',
                    'title_en': 'Student Points API Aggregator',
                    'instructions_sk': (
                        "Napíš funkciu `najlepsi_student(studenti_list)`, ktorá prijme zoznam slovníkov v tvare `[{\"meno\": \"Jano\", \"body\": 85}, ...]`.\n"
                        "Funkcia vráti meno študenta s najvyšším počtom bodov.\n"
                        "Ak je zoznam prázdny, vráti `None`."
                    ),
                    'instructions_en': 'Write `najlepsi_student(studenti_list)` returning name of student with max points, or None.',
                    'starter_code': 'def najlepsi_student(studenti_list):\n    pass\n',
                    'solution_code': 'def najlepsi_student(studenti_list):\n    if not studenti_list:\n        return None\n    top = max(studenti_list, key=lambda s: s.get("body", 0))\n    return top.get("meno")\n',
                    'explanation_sk': 'Používame vstavanú funkciu max s kľúčom key=lambda s: s.get("body", 0).',
                    'explanation_en': 'Find dictionary with max points using max() with key lambda.',
                    'hint_sk': 'if not studenti_list: return None; return max(studenti_list, key=lambda s: s["body"])["meno"].',
                    'hint_en': 'if not studenti_list: return None; return max(studenti_list, key=lambda s: s["body"])["meno"].',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'najlepsi_student([{"meno": "Juraj", "body": 95}, {"meno": "Martin", "body": 88}])', 'expected_output': 'Juraj', 'test_code': 'assert najlepsi_student([{"meno": "Juraj", "body": 95}, {"meno": "Martin", "body": 88}]) == "Juraj"', 'is_hidden': False},
                        {'input_data': 'najlepsi_student([])', 'expected_output': 'None', 'test_code': 'assert najlepsi_student([]) is None', 'is_hidden': False},
                        {'input_data': 'najlepsi_student([{"meno": "A", "body": 10}, {"meno": "B", "body": 100}])', 'expected_output': 'B', 'test_code': 'assert najlepsi_student([{"meno": "A", "body": 10}, {"meno": "B", "body": 100}]) == "B"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Množiny (set) a množinové operácie',
            'title_en': 'Sets & Mathematical Set Operations',
            'summary_sk': 'Unikátnosť prvkov, množinové zjednotenie |, prienik &, rozdiel - a symetrický rozdiel ^.',
            'summary_en': 'Uniqueness invariant, union |, intersection &, difference -, and symmetric difference ^.',
            'estimated_minutes': 50,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 7.4 Množiny (`set`) v Pythone

Množina je neusporiadaná kolekcia **unikátnych** prvkov. Ak do množiny vložíme duplicitné hodnoty, automaticky sa odstránia.

```python
cisla = {1, 2, 2, 3, 3, 3}
print(cisla)  # {1, 2, 3}
```

#### Množinové operácie:
- **Zjednotenie (`|` alebo `.union()`):** Všetky prvky z oboch množín.
- **Prienik (`&` alebo `.intersection()`):** Prvky spoločné pre obe množiny.
- **Rozdiel (`-` alebo `.difference()`):** Prvky prvej množiny, ktoré nie sú v druhej.
- **Symetrický rozdiel (`^` alebo `.symmetric_difference()`):** Prvky v jednej alebo druhej, ale nie v oboch.

```python
skupina_a = {"Python", "SQL", "Git"}
skupina_b = {"Python", "Django", "Docker"}

spolocne = skupina_a & skupina_b  # {'Python'}
```
""",
            'content_en': """### 7.4 Sets in Python

Sets hold unique unordered elements supporting mathematical operators:
- `|` Union
- `&` Intersection
- `-` Difference
- `^` Symmetric Difference
""",
            'quizzes': [
                {
                    'question_sk': 'Aký výsledok dá operácia `{1, 2, 3} & {2, 3, 4}`?',
                    'question_en': 'What is the result of `{1, 2, 3} & {2, 3, 4}`?',
                    'option_a_sk': '{2, 3}', 'option_a_en': '{2, 3}',
                    'option_b_sk': '{1, 2, 3, 4}', 'option_b_en': '{1, 2, 3, 4}',
                    'option_c_sk': '{1, 4}', 'option_c_en': '{1, 4}',
                    'option_d_sk': '{1}', 'option_d_en': '{1}',
                    'correct_option': 'A',
                    'explanation_sk': 'Operátor & predstavuje prienik (intersection), teda prvky prítomné v oboch množinách (2 a 3).',
                    'explanation_en': '& computes the intersection containing elements present in both sets.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Hľadanie spoločných priateľov (Prienik množín)',
                    'title_en': 'Mutual Friends Finder',
                    'instructions_sk': (
                        "Napíš funkciu `spolocni_priatelia(zoznam_a, zoznam_b)`, ktorá prijme dva zoznamy mien a vráti **zoradený zoznam** tých mien, ktoré sa nachádzajú v oboch zoznamoch.\n"
                        "Využi množinový prienik `set(zoznam_a) & set(zoznam_b)`."
                    ),
                    'instructions_en': 'Write `spolocni_priatelia(zoznam_a, zoznam_b)` returning sorted list of common elements using set intersection.',
                    'starter_code': 'def spolocni_priatelia(zoznam_a, zoznam_b):\n    pass\n',
                    'solution_code': 'def spolocni_priatelia(zoznam_a, zoznam_b):\n    prienik = set(zoznam_a) & set(zoznam_b)\n    return sorted(list(prienik))\n',
                    'explanation_sk': 'Prevedieme oba zoznamy na set, vykonáme prienik cez & a výsledok vrátime zoradený.',
                    'explanation_en': 'Convert lists to sets, intersect with &, sort with sorted().',
                    'hint_sk': 'return sorted(list(set(zoznam_a) & set(zoznam_b))).',
                    'hint_en': 'return sorted(list(set(zoznam_a) & set(zoznam_b))).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'spolocni_priatelia(["Juraj", "Martin", "Petra"], ["Eva", "Petra", "Juraj"])', 'expected_output': '["Juraj", "Petra"]', 'test_code': 'assert spolocni_priatelia(["Juraj", "Martin", "Petra"], ["Eva", "Petra", "Juraj"]) == ["Juraj", "Petra"]', 'is_hidden': False},
                        {'input_data': 'spolocni_priatelia(["A", "B"], ["C", "D"])', 'expected_output': '[]', 'test_code': 'assert spolocni_priatelia(["A", "B"], ["C", "D"]) == []', 'is_hidden': False},
                        {'input_data': 'spolocni_priatelia(["x", "y"], ["y", "z", "x"])', 'expected_output': '["x", "y"]', 'test_code': 'assert spolocni_priatelia(["x", "y"], ["y", "z", "x"]) == ["x", "y"]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Frekvenčná analýza textu a zhrnutie modulu',
            'title_en': 'Text Frequency Analysis & Module Summary',
            'summary_sk': 'Praktická dátová analytika: počítanie výskytov slov, frekvenčný slovník a záverečný projekt.',
            'summary_en': 'Real-world data analytics: word tokenization, occurrence counting, and capstone challenge.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 7.5 Frekvenčná analýza textu v Pythone

Jednou z najdôležitejších aplikácií slovníkov je **frekvenčná analýza** – zistenie početnosti výskytu jednotlivých položiek v datasete.

```python
slova = ["python", "kód", "python", "učenie", "kód", "python"]
pocty = {}

for s in slova:
    pocty[s] = pocty.get(s, 0) + 1

print(pocty)  # {'python': 3, 'kód': 2, 'učenie': 1}
```
""",
            'content_en': """### 7.5 Frequency Analysis in Python

Counting occurrences using dictionaries and the `dict.get(key, 0) + 1` idiom.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo robí konštrukcia `d[k] = d.get(k, 0) + 1` v cykle?',
                    'question_en': 'What does `d[k] = d.get(k, 0) + 1` accomplish inside an iteration?',
                    'option_a_sk': 'Inkrementuje počítadlo výskytov kľúča k (ak kľúč neexistoval, začne od 0 + 1 = 1)', 'option_a_en': 'Increments frequency counter for key k, initializing to 1 if absent',
                    'option_b_sk': 'Vymaže kľúč', 'option_b_en': 'Deletes key',
                    'option_c_sk': 'Nastaví hodnotu na 0', 'option_c_en': 'Resets value to 0',
                    'option_d_sk': 'Vytvorí nekonečný cyklus', 'option_d_en': 'Creates infinite loop',
                    'correct_option': 'A',
                    'explanation_sk': 'Je to štandardný Python idiom pre počítanie frekvencií bez rizika KeyError.',
                    'explanation_en': 'Standard idiomatic pattern for frequency tallying in Python.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Frekvenčný analyzátor slov v texte',
                    'title_en': 'Word Frequency Counter',
                    'instructions_sk': (
                        "Napíš funkciu `frekvencia_slov(veta)`, ktorá rozdelí vetu na slová (malými písmenami) a vráti slovník, kde kľúče sú slová a hodnoty sú počty ich výskytov.\n"
                        "Napr. pre `'pes macka pes pes'` vráti `{'pes': 3, 'macka': 1}`."
                    ),
                    'instructions_en': 'Write `frekvencia_slov(veta)` splitting lowercase sentence and returning dictionary of word frequencies.',
                    'starter_code': 'def frekvencia_slov(veta):\n    pass\n',
                    'solution_code': 'def frekvencia_slov(veta):\n    vysledok = {}\n    for slovo in veta.lower().split():\n        vysledok[slovo] = vysledok.get(slovo, 0) + 1\n    return vysledok\n',
                    'explanation_sk': 'Prevedieme text na malé písmená, rozdelíme cez split() a akumulujeme cez .get(slovo, 0) + 1.',
                    'explanation_en': 'Lowercase, split on whitespace, tally using get() fallback pattern.',
                    'hint_sk': 'vysledok = {}; for s in veta.lower().split(): vysledok[s] = vysledok.get(s, 0) + 1; return vysledok.',
                    'hint_en': 'vysledok = {}; for s in veta.lower().split(): vysledok[s] = vysledok.get(s, 0) + 1; return vysledok.',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'frekvencia_slov("pes macka pes pes")', 'expected_output': '{"pes": 3, "macka": 1}', 'test_code': 'assert frekvencia_slov("pes macka pes pes") == {"pes": 3, "macka": 1}', 'is_hidden': False},
                        {'input_data': 'frekvencia_slov("Codoro Codoro Codoro")', 'expected_output': '{"codoro": 3}', 'test_code': 'assert frekvencia_slov("Codoro Codoro Codoro") == {"codoro": 3}', 'is_hidden': False},
                        {'input_data': 'frekvencia_slov("jeden dva tri")', 'expected_output': '{"jeden": 1, "dva": 1, "tri": 1}', 'test_code': 'assert frekvencia_slov("jeden dva tri") == {"jeden": 1, "dva": 1, "tri": 1}', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
