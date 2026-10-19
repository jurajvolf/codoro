"""
MODUL 10: Objektovo-orientované programovanie II – Dedičnosť a polymorfizmus
Odhadovaný rozsah: 12 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU
"""

MODULE_DATA = {
    'order': 10,
    'title_sk': 'OOP II – Dedičnosť, polymorfizmus a dunder metódy',
    'title_en': 'OOP II – Inheritance, Polymorphism & Dunder Methods',
    'description_sk': 'Pokročilé koncepty objektového návrhu: dedičnosť (Inheritance), volanie super(), prekrývanie metód (Overriding), polymorfizmus, magické metódy (__str__, __len__, __eq__) a moderné dataclasses.',
    'description_en': 'Advanced OOP design: class inheritance hierarchies, super() delegation, method overriding, runtime polymorphism, dunder methods (__str__, __eq__, etc.), and dataclasses.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'layers',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Dedičnosť tried (Inheritance) a funkcia super()',
            'title_en': 'Class Inheritance & the super() Function',
            'summary_sk': 'Vzťah Is-A, odvodenie podtriedy class Dieta(Rodica), dedenie atribútov a volanie konštruktora super().__init__().',
            'summary_en': 'Is-A class relationships, subclassing syntax, attribute inheritance, and constructor chaining with super().',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 10.1 Dedičnosť v Pythone

**Dedičnosť (Inheritance)** umožňuje vytvoriť novú triedu (podtriedu / derived class), ktorá prevezme atribúty a metódy existujúcej triedy (nadradenej triedy / base class).

Vyjadruje vzťah typu **"Is-A"** (Pes JE Zviera, Učiteľ JE Používateľ).

#### Volanie rodičovského konštruktora cez `super()`:
```python
class Pouzivatel:
    def __init__(self, username, email):
        self.username = username
        self.email = email

class Student(Pouzivatel):
    def __init__(self, username, email, trieda):
        # Zavoláme rodiča, aby inicializoval username a email
        super().__init__(username, email)
        self.trieda = trieda  # Vlastný atribút podtriedy
```
""",
            'content_en': """### 10.1 Class Inheritance and super()

Subclasses inherit parent methods and attributes. `super().__init__(...)` delegates initialization up the hierarchy.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo robí funkcia `super()` v tele podtriedy?',
                    'question_en': 'What does `super()` accomplish within a subclass?',
                    'option_a_sk': 'Poskytuje prístup k metódam a konštruktoru nadradenej (rodičovskej) triedy', 'option_a_en': 'Provides access to parent class methods and constructors',
                    'option_b_sk': 'Vymaže rodičovskú triedu', 'option_b_en': 'Deletes parent class',
                    'option_c_sk': 'Umožňuje vytvoriť statickú premennú', 'option_c_en': 'Creates static variable',
                    'option_d_sk': 'Spôsobí reštart interpretu', 'option_d_en': 'Restarts runtime',
                    'correct_option': 'A',
                    'explanation_sk': 'super() vráti proxy objekt delegujúci volania metód na rodičovskú triedu v MRO reťazci.',
                    'explanation_en': 'super() returns a proxy object delegating method calls to parent classes in the MRO.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Hierarchia herných postáv (Bojovník a Kúzelník)',
                    'title_en': 'Game Character Hierarchy',
                    'instructions_sk': (
                        "Vytvor základnú triedu `Postava(meno, hp)` so základnou metódou `info(self)` vracajúcou `\"[meno]: [hp] HP\"`.\n"
                        "Vytvor odvodenú triedu `Kuzelnik(Postava)`, ktorá v `__init__` prijme `meno, hp, mana`, zavolá `super().__init__(meno, hp)` a uloží `self.mana`.\n"
                        "V `Kuzelnik` prepíš metódu `info(self)` tak, aby vrátila `\"[meno]: [hp] HP | [mana] Mana\"`."
                    ),
                    'instructions_en': 'Create base class `Postava` and derived `Kuzelnik` with super().__init__ and overridden `info()`.',
                    'starter_code': 'class Postava:\n    pass\n\nclass Kuzelnik(Postava):\n    pass\n',
                    'solution_code': 'class Postava:\n    def __init__(self, meno, hp):\n        self.meno = meno\n        self.hp = hp\n    def info(self):\n        return f"{self.meno}: {self.hp} HP"\n\nclass Kuzelnik(Postava):\n    def __init__(self, meno, hp, mana):\n        super().__init__(meno, hp)\n        self.mana = mana\n    def info(self):\n        return f"{self.meno}: {self.hp} HP | {self.mana} Mana"\n',
                    'explanation_sk': 'Demonštrácia dedičnosti, volania super() a preťaženia metódy info.',
                    'explanation_en': 'Subclassing with constructor chaining and customized information rendering.',
                    'hint_sk': 'super().__init__(meno, hp); self.mana = mana.',
                    'hint_en': 'super().__init__(meno, hp); self.mana = mana.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'p = Postava("Bojovnik", 100); p.info()', 'expected_output': 'Bojovnik: 100 HP', 'test_code': 'p = Postava("Bojovnik", 100)\nassert p.info() == "Bojovnik: 100 HP"', 'is_hidden': False},
                        {'input_data': 'k = Kuzelnik("Gandalf", 80, 150); k.info()', 'expected_output': 'Gandalf: 80 HP | 150 Mana', 'test_code': 'k = Kuzelnik("Gandalf", 80, 150)\nassert k.info() == "Gandalf: 80 HP | 150 Mana"', 'is_hidden': False},
                        {'input_data': 'isinstance(k, Postava)', 'expected_output': 'True', 'test_code': 'assert isinstance(k, Postava) is True', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Prekrývanie metód (Method Overriding) a polymorfizmus',
            'title_en': 'Method Overriding & Runtime Polymorphism',
            'summary_sk': 'Princíp polymorfizmu (mnohotvárnosti), jednotné rozhranie pre rôzne podtriedy a Duck Typing.',
            'summary_en': 'Polymorphism concept, unified interfaces across heterogeneous objects, and Python Duck Typing.',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 10.2 Polymorfizmus a Duck Typing

**Polymorfizmus** (mnohotvárnosť) znamená schopnosť pracovať s rôznymi objektmi cez **rovnaké rozhranie**, pričom každý objekt zareaguje podľa svojej vlastnej implementácie.

V Pythone platí filozofia **Duck Typing**: *"Ak to kváka ako kačka a chodí ako kačka, je to pre nás kačka."*

```python
class Kruh:
    def __init__(self, r): self.r = r
    def obsah(self): return 3.14159 * self.r ** 2

class Stvorec:
    def __init__(self, a): self.a = a
    def obsah(self): return self.a ** 2

# Polymorfné spracovanie:
utvary = [Kruh(5), Stvorec(4), Kruh(2)]
for u in utvary:
    print(f"Obsah: {u.obsah():.2f}")
```
Kód volajúci `u.obsah()` nemusí vedieť, o aký konkrétny geometrický útvar ide!
""",
            'content_en': """### 10.2 Polymorphism & Duck Typing

Heterogeneous objects sharing a common method contract can be treated uniformly without type checks.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo znamená výrok "Duck Typing" v ekosystéme jazyka Python?',
                    'question_en': 'What does "Duck Typing" mean in the Python ecosystem?',
                    'option_a_sk': 'Typ objektu nie je určený jeho dedičnosťou, ale prítomnosťou potrebných metód a atribútov', 'option_a_en': 'An object suitability is determined by the presence of methods rather than its explicit class hierarchy',
                    'option_b_sk': 'Že program funguje iba pre zvieratá', 'option_b_en': 'Applies only to animals',
                    'option_c_sk': 'Že Python kontroluje typy pri kompilácii', 'option_c_en': 'Static type check',
                    'option_d_sk': 'Je to zastaraná vlastnosť Pythonu 1', 'option_d_en': 'Deprecated feature',
                    'correct_option': 'A',
                    'explanation_sk': 'Duck Typing: dôležité je, či objekt dokáže vykonať požadovanú operáciu, nie to, z akej triedy dedí.',
                    'explanation_en': 'Duck typing focuses on interface capabilities rather than explicit inheritance pedigree.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Polymorfný výpočet miezd zamestnancov',
                    'title_en': 'Polymorphic Payroll System',
                    'instructions_sk': (
                        "Vytvor triedy pre mzdový systém:\n"
                        "1. `TppZamestnanec(meno, fixny_plat)` s metódou `vypocitaj_mzdu(self)` vracajúcou `fixny_plat`.\n"
                        "2. `Dohodar(meno, odpracovane_hodiny, sadzba_za_hodinu)` s metódou `vypocitaj_mzdu(self)` vracajúcou `odpracovane_hodiny * sadzba_za_hodinu`.\n"
                        "3. Funkciu `celkove_mzdove_naklady(zamestnanci_list)`, ktorá polymorfne sčíta mzdy všetkých zamestnancov v zozname."
                    ),
                    'instructions_en': 'Implement classes `TppZamestnanec` and `Dohodar` with `vypocitaj_mzdu()` and a sum function.',
                    'starter_code': 'class TppZamestnanec:\n    pass\n\nclass Dohodar:\n    pass\n\ndef celkove_mzdove_naklady(zamestnanci_list):\n    pass\n',
                    'solution_code': 'class TppZamestnanec:\n    def __init__(self, meno, fixny_plat):\n        self.meno = meno\n        self.fixny_plat = fixny_plat\n    def vypocitaj_mzdu(self):\n        return self.fixny_plat\n\nclass Dohodar:\n    def __init__(self, meno, odpracovane_hodiny, sadzba_za_hodinu):\n        self.meno = meno\n        self.odpracovane_hodiny = odpracovane_hodiny\n        self.sadzba_za_hodinu = sadzba_za_hodinu\n    def vypocitaj_mzdu(self):\n        return self.odpracovane_hodiny * self.sadzba_za_hodinu\n\ndef celkove_mzdove_naklady(zamestnanci_list):\n    return sum(z.vypocitaj_mzdu() for z in zamestnanci_list)\n',
                    'explanation_sk': 'Polymorfné volanie metódy vypocitaj_mzdu() pre rôzne triedy.',
                    'explanation_en': 'Polymorphic invocation of common method signature over heterogeneous employee list.',
                    'hint_sk': 'return sum(z.vypocitaj_mzdu() for z in zamestnanci_list).',
                    'hint_en': 'return sum(z.vypocitaj_mzdu() for z in zamestnanci_list).',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 't = TppZamestnanec("Jano", 1500); d = Dohodar("Fero", 40, 15); celkove_mzdove_naklady([t, d])', 'expected_output': '2100', 'test_code': 't = TppZamestnanec("Jano", 1500)\nd = Dohodar("Fero", 40, 15)\nassert celkove_mzdove_naklady([t, d]) == 2100', 'is_hidden': False},
                        {'input_data': 'celkove_mzdove_naklady([])', 'expected_output': '0', 'test_code': 'assert celkove_mzdove_naklady([]) == 0', 'is_hidden': False},
                        {'input_data': 'celkove_mzdove_naklady([TppZamestnanec("A", 1000), TppZamestnanec("B", 2000)])', 'expected_output': '3000', 'test_code': 'assert celkove_mzdove_naklady([TppZamestnanec("A", 1000), TppZamestnanec("B", 2000)]) == 3000', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Magické (Dunder) metódy: __str__, __len__, __eq__ a preťažovanie',
            'title_en': 'Dunder Methods: __str__, __len__, __eq__ & Operator Overloading',
            'summary_sk': 'Dvojité podčiarkovníky, čitateľný výpis __str__, dĺžka __len__, rovnosť __eq__, porovnávanie __lt__.',
            'summary_en': 'Special double-underscore methods, string representation, equality, ordering, and operator overloading.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 10.3 Dunder (Special) metódy v Pythone

Názvy začínajúce a končiace dvoma podčiarkovníkmi (napr. `__init__`) sa v komunite nazývajú **Dunder** (Double Underscore) metódy. Umožňujú objektu zapojiť sa do vstavaných operátorov Pythonu!

#### Kľúčové dunder metódy:
1. `__str__(self)` – reťazcová reprezentácia pre používateľa (`str(obj)`, `print(obj)`).
2. `__repr__(self)` – technická reprezentácia pre vývojára a ladič (`repr(obj)`).
3. `__len__(self)` – volá sa pri funkcii `len(obj)`.
4. `__eq__(self, other)` – preťažuje operátor rovnosti `obj == other`.
5. `__lt__(self, other)` – operátor menší než `obj < other` (umožňuje `sorted()`).
6. `__add__(self, other)` – operátor sčítania `obj + other`.

```python
class Minca:
    def __init__(self, pocet): self.pocet = pocet
    def __str__(self): return f"{self.pocet} Doros"
    def __add__(self, other): return Minca(self.pocet + other.pocet)

m1 = Minca(50)
m2 = Minca(30)
print(m1 + m2)  # 80 Doros
```
""",
            'content_en': """### 10.3 Magic / Dunder Methods

Hooking into Python built-in operators: `__str__`, `__len__`, `__eq__`, `__add__`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá dunder metóda sa automaticky zavolá pri vykonaní príkazu `print(objekt)`?',
                    'question_en': 'Which dunder method is automatically invoked by `print(obj)`?',
                    'option_a_sk': '__str__', 'option_a_en': '__str__',
                    'option_b_sk': '__print__', 'option_b_en': '__print__',
                    'option_c_sk': '__display__', 'option_c_en': '__display__',
                    'option_d_sk': '__show__', 'option_d_en': '__show__',
                    'correct_option': 'A',
                    'explanation_sk': 'print() a str() automaticky volajú dunder metódu __str__ definovanú v triede.',
                    'explanation_en': 'print() delegates string formatting to __str__().',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Vektor v 2D priestore s dunder metódami',
                    'title_en': '2D Vector with Operator Overloading',
                    'instructions_sk': (
                        "Vytvor triedu `Vektor2D(x, y)` implementujúcu dunder metódy:\n"
                        "1. `__str__(self)`: vráti `\"(x, y)\"` (napr. `\"(3, 4)\"`).\n"
                        "2. `__add__(self, other)`: vráti novú inštanciu `Vektor2D(self.x + other.x, self.y + other.y)`.\n"
                        "3. `__eq__(self, other)`: vráti `True`, ak majú rovnaké súradnice `x` aj `y`.\n"
                        "4. `__len__(self)`: vráti celočíselnú euklidovskú dĺžku vektora: `int((self.x**2 + self.y**2)**0.5)`."
                    ),
                    'instructions_en': 'Implement class `Vektor2D` with __str__, __add__, __eq__, and __len__ operators.',
                    'starter_code': 'class Vektor2D:\n    pass\n',
                    'solution_code': 'class Vektor2D:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __str__(self):\n        return f"({self.x}, {self.y})"\n    def __add__(self, other):\n        return Vektor2D(self.x + other.x, self.y + other.y)\n    def __eq__(self, other):\n        if not isinstance(other, Vektor2D):\n            return False\n        return self.x == other.x and self.y == other.y\n    def __len__(self):\n        return int((self.x**2 + self.y**2)**0.5)\n',
                    'explanation_sk': 'Kompletná implementácia matematického operátora + a funkcií str, eq, len cez dunder metódy.',
                    'explanation_en': 'Full vector operator overloading with __str__, __add__, __eq__, and __len__.',
                    'hint_sk': 'def __add__(self, other): return Vektor2D(self.x + other.x, self.y + other.y).',
                    'hint_en': 'def __add__(self, other): return Vektor2D(self.x + other.x, self.y + other.y).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'v1 = Vektor2D(3, 4); str(v1)', 'expected_output': '(3, 4)', 'test_code': 'v1 = Vektor2D(3, 4)\nassert str(v1) == "(3, 4)"', 'is_hidden': False},
                        {'input_data': 'v1 = Vektor2D(1, 2); v2 = Vektor2D(3, 4); v3 = v1 + v2; str(v3)', 'expected_output': '(4, 6)', 'test_code': 'v1 = Vektor2D(1, 2)\nv2 = Vektor2D(3, 4)\nassert str(v1 + v2) == "(4, 6)"', 'is_hidden': False},
                        {'input_data': 'v = Vektor2D(3, 4); len(v)', 'expected_output': '5', 'test_code': 'v = Vektor2D(3, 4)\nassert len(v) == 5', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Dátové triedy (@dataclass) a moderná architektúra',
            'title_en': 'Data Classes (@dataclass) & Clean Architecture',
            'summary_sk': 'Automatické generovanie __init__, __repr__ a __eq__ cez modul dataclasses.',
            'summary_en': 'Clean boilerplate reduction with dataclasses module and immutability controls.',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 10.4 Dátové triedy (`@dataclass`)

Od verzie Python 3.7 ponúka štandardná knižnica dekorátor `@dataclass` z modulu `dataclasses`. Automaticky vygeneruje metódy `__init__`, `__repr__` a `__eq__` podľa typových anotácií:

```python
from dataclasses import dataclass

@dataclass
class QuestItem:
    nazov: str
    doros_odmena: int
    aktivny: bool = True

q1 = QuestItem("Vyrieš 3 úlohy", 50)
q2 = QuestItem("Vyrieš 3 úlohy", 50)

print(q1)          # QuestItem(nazov='Vyrieš 3 úlohy', doros_odmena=50, aktivny=True)
print(q1 == q2)    # True (automatické overenie zhody atribútov!)
```
Ušetrí desiatky riadkov stereotypného kódu pri tvorbe DTO (Data Transfer Objects) modelov.
""",
            'content_en': """### 10.4 Dataclasses in Python

`@dataclass` eliminates boilerplate by generating `__init__`, `__repr__`, and `__eq__` automatically.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktoré dunder metódy automaticky vygeneruje dekorátor `@dataclass`?',
                    'question_en': 'Which dunder methods does `@dataclass` generate by default?',
                    'option_a_sk': '__init__, __repr__ a __eq__', 'option_a_en': '__init__, __repr__, and __eq__',
                    'option_b_sk': '__len__ a __getitem__', 'option_b_en': '__len__ and __getitem__',
                    'option_c_sk': 'Iba __del__', 'option_c_en': 'Only __del__',
                    'option_d_sk': '__add__ a __sub__', 'option_d_en': '__add__ and __sub__',
                    'correct_option': 'A',
                    'explanation_sk': '@dataclass predvolene vygeneruje konštruktor, pekný výpis a porovnávanie rovnosti.',
                    'explanation_en': '@dataclass synthesizes constructor, string representation, and equality comparison.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Dataclass študentskej licencie',
                    'title_en': 'Student License Dataclass',
                    'instructions_sk': (
                        "Importuj `from dataclasses import dataclass` a vytvor triedu `@dataclass class Licencia` s poliami:\n"
                        "- `kod: str`\n"
                        "- `tier: str = \"EDU\"`\n"
                        "- `max_pouziti: int = 30`\n"
                        "- `aktualne_pouzitia: int = 0`\n"
                        "Pridaj metódu `aktivuj(self)`: ak je `aktualne_pouzitia < max_pouziti`, zvýši počítadlo o 1 a vráti `True`. Inak vráti `False`."
                    ),
                    'instructions_en': 'Create `@dataclass class Licencia` with fields, defaults, and `aktivuj(self)` method.',
                    'starter_code': 'from dataclasses import dataclass\n\n# Implementuj Licencia\n',
                    'solution_code': 'from dataclasses import dataclass\n\n@dataclass\nclass Licencia:\n    kod: str\n    tier: str = "EDU"\n    max_pouziti: int = 30\n    aktualne_pouzitia: int = 0\n    def aktivuj(self):\n        if self.aktualne_pouzitia < self.max_pouziti:\n            self.aktualne_pouzitia += 1\n            return True\n        return False\n',
                    'explanation_sk': 'Dekorátor @dataclass s voliteľnou metódou aktivuj a predvolenými hodnotami.',
                    'explanation_en': 'Dataclass with type hints and domain logic activation counter.',
                    'hint_sk': 'if self.aktualne_pouzitia < self.max_pouziti: self.aktualne_pouzitia += 1; return True.',
                    'hint_en': 'if self.aktualne_pouzitia < self.max_pouziti: self.aktualne_pouzitia += 1; return True.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'lic = Licencia("EDU-2027", max_pouziti=2); (lic.aktivuj(), lic.aktivuj(), lic.aktivuj())', 'expected_output': '(True, True, False)', 'test_code': 'lic = Licencia("EDU-2027", max_pouziti=2)\nassert (lic.aktivuj(), lic.aktivuj(), lic.aktivuj()) == (True, True, False)', 'is_hidden': False},
                        {'input_data': 'lic = Licencia("PRO-KEY"); lic.tier', 'expected_output': 'EDU', 'test_code': 'lic = Licencia("PRO-KEY")\nassert lic.tier == "EDU"', 'is_hidden': False},
                        {'input_data': 'lic = Licencia("X", aktualne_pouzitia=30); lic.aktivuj()', 'expected_output': 'False', 'test_code': 'lic = Licencia("X", aktualne_pouzitia=30)\nassert lic.aktivuj() is False', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
