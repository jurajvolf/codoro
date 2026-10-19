"""
MODUL 9: Objektovo-orientované programovanie I – Triedy a zapuzdrenie
Odhadovaný rozsah: 12 hodín | Náročnosť: INTERMEDIATE | Úroveň: PRO / EDU
"""

MODULE_DATA = {
    'order': 9,
    'title_sk': 'Objektovo-orientované programovanie I – Triedy a zapuzdrenie',
    'title_en': 'Object-Oriented Programming I – Classes & Encapsulation',
    'description_sk': 'Vstúp do sveta priemyselného softvérového inžinierstva: triedy (class), inštancie, konštruktor __init__, parameter self, inštančné vs. triedne atribúty (@classmethod, @staticmethod) a zapuzdrenie s @property.',
    'description_en': 'Enter enterprise software engineering: class blueprints, object instances, __init__ constructor, self reference, class/static methods, and encapsulation using @property decorators.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'INTERMEDIATE',
    'is_pro_only': True,
    'icon_name': 'box',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Paradigma OOP: trieda ako predpis a objekt v pamäti',
            'title_en': 'OOP Paradigm: Class Blueprint & In-Memory Objects',
            'summary_sk': 'Rozdiel medzi procedurálnym a objektovým programovaním, definícia class a vytvorenie inštancie.',
            'summary_en': 'Procedural vs OOP programming, class definitions, and object instantiation.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 9.1 Úvod do Objektovo-orientovaného programovania (OOP)

OOP je programovacia paradigma, v ktorej program modelujeme ako súbor vzájomne komunikujúcich **objektov**. Každý objekt v sebe spája:
1. **Dáta (Stav / Atribúty)** – napr. meno, vek, zostatok Doros.
2. **Správanie (Funkcie / Metódy)** – napr. nákup odmeny, odovzdanie úlohy.

#### Analógia:
- **Trieda (`class`)** je architektonický plán (pečiatka, recept).
- **Objekt (Inštancia)** je reálny postavený dom (odtlačok pečiatky, koláč).

```python
class Hrac:
    pass  # Prázdna definícia triedy

hrac1 = Hrac()  # Vytvorenie inštancie
hrac2 = Hrac()
print(isinstance(hrac1, Hrac))  # True
```
""",
            'content_en': """### 9.1 Introduction to Object-Oriented Programming (OOP)

OOP bundles state (attributes) and behavior (methods) into objects instantiated from classes.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je vzťah medzi triedou (class) a objektom (inštanciou)?',
                    'question_en': 'What is the relationship between a class and an object?',
                    'option_a_sk': 'Trieda je predpis (šablóna) a objekt je konkrétna inštancia vytvorená v pamäti podľa tejto triedy', 'option_a_en': 'A class is a blueprint, and an object is an in-memory instance created from it',
                    'option_b_sk': 'Sú to úplné synonymá', 'option_b_en': 'They are identical synonyms',
                    'option_c_sk': 'Objekt existuje iba v databáze, trieda v kóde', 'option_c_en': 'Object exists in database, class in code',
                    'option_d_sk': 'Trieda je funkcia, objekt je premenná', 'option_d_en': 'Class is function, object is variable',
                    'correct_option': 'A',
                    'explanation_sk': 'Trieda definuje štruktúru a vlastnosti, objekt je konkrétna entita vytvorená v pamäti.',
                    'explanation_en': 'Class serves as blueprint; object is concrete allocated instance.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Vytvorenie triedy a inštancií herného avatara',
                    'title_en': 'Game Avatar Class Instantiation',
                    'instructions_sk': (
                        "Definuj triedu `Avatar` s metódou `__init__(self, nickname, skin)`.\n"
                        "Atribúty ulož do `self.nickname` a `self.skin`.\n"
                        "Pridaj metódu `predstav_sa(self)`, ktorá vráti reťazec `\"Ahoj, ja som [nickname] so skinom [skin]!\"`."
                    ),
                    'instructions_en': 'Define class `Avatar` with `__init__(self, nickname, skin)` and `predstav_sa(self)`.',
                    'starter_code': 'class Avatar:\n    # Implementuj __init__ a predstav_sa\n    pass\n',
                    'solution_code': 'class Avatar:\n    def __init__(self, nickname, skin):\n        self.nickname = nickname\n        self.skin = skin\n    def predstav_sa(self):\n        return f"Ahoj, ja som {self.nickname} so skinom {self.skin}!"\n',
                    'explanation_sk': 'Základná definícia triedy s konštruktorom a inštančnou metódou.',
                    'explanation_en': 'Basic class blueprint storing instance attributes and returning formatted string.',
                    'hint_sk': 'def __init__(self, nickname, skin): self.nickname = nickname; self.skin = skin.',
                    'hint_en': 'def __init__(self, nickname, skin): self.nickname = nickname; self.skin = skin.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'a = Avatar("Codo", "Cyberpunk"); a.predstav_sa()', 'expected_output': 'Ahoj, ja som Codo so skinom Cyberpunk!', 'test_code': 'a = Avatar("Codo", "Cyberpunk")\nassert a.predstav_sa() == "Ahoj, ja som Codo so skinom Cyberpunk!"', 'is_hidden': False},
                        {'input_data': 'a = Avatar("Hero", "Retro"); a.nickname', 'expected_output': 'Hero', 'test_code': 'a = Avatar("Hero", "Retro")\nassert a.nickname == "Hero"', 'is_hidden': False},
                        {'input_data': 'a = Avatar("Bot", "Stealth"); a.predstav_sa()', 'expected_output': 'Ahoj, ja som Bot so skinom Stealth!', 'test_code': 'a = Avatar("Bot", "Stealth")\nassert a.predstav_sa() == "Ahoj, ja som Bot so skinom Stealth!"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Konštruktor __init__ a parameter self',
            'title_en': 'Constructor __init__ & the self Parameter',
            'summary_sk': 'Inicializácia objektov, magická metóda __init__ a význam explicitného self v Pythone.',
            'summary_en': 'Instance initialization with __init__, explicit self parameter binding, and instance namespaces.',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 9.2 Konštruktor `__init__` a `self`

Keď vytvoríme inštanciu triedy (napr. `p = Penazenka(100)`), Python automaticky zavolá metódu `__init__` (tzv. inicializátor alebo konštruktor).

#### Čo znamená `self`?
Parameter `self` je referencia na **konkrétnu inštanciu**, na ktorej bola metóda zavolaná. Umožňuje každému objektu pristupovať k vlastným dátam:

```python
class Penazenka:
    def __init__(self, pociatocny_stav=0):
        self.doros = pociatocny_stav  # Inštančný atribút

    def pripis(self, suma):
        self.doros += suma

p1 = Penazenka(50)
p2 = Penazenka(200)

p1.pripis(30)
print(p1.doros)  # 80
print(p2.doros)  # 200 (nezmenené!)
```
""",
            'content_en': """### 9.2 The __init__ Constructor and self

`__init__` initializes newly minted object state. `self` points to the calling instance.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú úlohu plní prvý parameter `self` v inštančných metódach Pythonu?',
                    'question_en': 'What purpose does the first parameter `self` serve in Python instance methods?',
                    'option_a_sk': 'Odkazuje na konkrétnu inštanciu triedy, nad ktorou sa metóda volá', 'option_a_en': 'References the specific instance on which the method is invoked',
                    'option_b_sk': 'Je to kľúčové slovo pre globálne premenné', 'option_b_en': 'Keyword for globals',
                    'option_c_sk': 'Umožňuje rekurziu', 'option_c_en': 'Enables recursion',
                    'option_d_sk': 'Musí mať vždy hodnotu None', 'option_d_en': 'Always holds None',
                    'correct_option': 'A',
                    'explanation_sk': 'Python pri volaní objekt.metoda() automaticky odovzdá daný objekt ako prvý argument self.',
                    'explanation_en': 'Python automatically passes the target instance as the first argument to instance methods.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Simulátor bankového účtu (BankAccount)',
                    'title_en': 'Bank Account Simulator',
                    'instructions_sk': (
                        "Vytvor triedu `Ucet` s konštruktorom `__init__(self, majitel, zostatok=0)`.\n"
                        "Pridaj metódy:\n"
                        "- `vklad(self, suma)`: pripočíta sumu a vráti nový zostatok.\n"
                        "- `vyber(self, suma)`: ak je na účte dostatok peňazí, odpočíta sumu a vráti `True`. Inak zostatok nezmení a vráti `False`."
                    ),
                    'instructions_en': 'Create class `Ucet` with `vklad(self, suma)` and `vyber(self, suma)` with balance checks.',
                    'starter_code': 'class Ucet:\n    pass\n',
                    'solution_code': 'class Ucet:\n    def __init__(self, majitel, zostatok=0):\n        self.majitel = majitel\n        self.zostatok = zostatok\n    def vklad(self, suma):\n        self.zostatok += suma\n        return self.zostatok\n    def vyber(self, suma):\n        if self.zostatok >= suma:\n            self.zostatok -= suma\n            return True\n        return False\n',
                    'explanation_sk': 'Inštančné metódy modifikujú stav atribútu self.zostatok a overujú podmienky.',
                    'explanation_en': 'Methods mutate self.zostatok verifying withdrawal solvency.',
                    'hint_sk': 'V metóde vyber over: if self.zostatok >= suma: self.zostatok -= suma; return True; return False.',
                    'hint_en': 'In vyber check: if self.zostatok >= suma: self.zostatok -= suma; return True; return False.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'u = Ucet("Juraj", 100); u.vklad(50); u.zostatok', 'expected_output': '150', 'test_code': 'u = Ucet("Juraj", 100)\nu.vklad(50)\nassert u.zostatok == 150', 'is_hidden': False},
                        {'input_data': 'u = Ucet("Martin", 100); u.vyber(150)', 'expected_output': 'False', 'test_code': 'u = Ucet("Martin", 100)\nassert u.vyber(150) is False\nassert u.zostatok == 100', 'is_hidden': False},
                        {'input_data': 'u = Ucet("Petra", 50); u.vyber(50)', 'expected_output': 'True', 'test_code': 'u = Ucet("Petra", 50)\nassert u.vyber(50) is True\nassert u.zostatok == 0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Inštančné atribúty vs. Triedne atribúty (@classmethod a @staticmethod)',
            'title_en': 'Class Attributes, @classmethod & @staticmethod',
            'summary_sk': 'Zdieľané triedne premenné, metódy viazané na triedu (cls) a nezávislé pomocné statické metódy.',
            'summary_en': 'Shared class variables, classmethods bound to cls, and utility staticmethods.',
            'estimated_minutes': 55,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 9.3 Triedne atribúty a dekorátory

1. **Inštančný atribút (`self.x`)**: Patrí konkrétnemu objektu, každý objekt má vlastnú kópiu.
2. **Triedny atribút (`Trieda.x`)**: Zdieľaný medzi **všetkými** inštanciami danej triedy.

#### Dekorátory `@classmethod` a `@staticmethod`:
- `@classmethod` – prijíma ako prvý parameter `cls` (samotnú triedu). Často slúži ako alternatívny konštruktor (Factory Method).
- `@staticmethod` – neprijíma ani `self`, ani `cls`. Je to čistá pomocná funkcia umiestnená v triede pre logickú prehľadnosť.

```python
class Student:
    pocet_ziakov = 0  # Triedny atribút

    def __init__(self, meno):
        self.meno = meno
        Student.pocet_ziakov += 1

    @classmethod
    def get_pocet(cls):
        return cls.pocet_ziakov

    @staticmethod
    def je_platne_meno(meno):
        return len(meno) >= 2
```
""",
            'content_en': """### 9.3 Class Attributes, @classmethod & @staticmethod

Class variables are shared among all instances. `@classmethod` operates on `cls`, while `@staticmethod` has no instance/class binding.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je prvý parameter metódy označenej dekorátorom `@classmethod`?',
                    'question_en': 'What is the first parameter of a method decorated with `@classmethod`?',
                    'option_a_sk': 'cls (odkaz na samotnú triedu)', 'option_a_en': 'cls (reference to the class itself)',
                    'option_b_sk': 'self (odkaz na inštanciu)', 'option_b_en': 'self (instance reference)',
                    'option_c_sk': 'None', 'option_c_en': 'None',
                    'option_d_sk': 'class', 'option_d_en': 'class',
                    'correct_option': 'A',
                    'explanation_sk': 'Triedna metóda dostáva ako prvý argument odkaz na triedu, konvenčne pomenovaný cls.',
                    'explanation_en': 'Class methods receive the class object as their first argument, conventionally named cls.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Počítadlo inštancií a alternatívny konštruktor',
                    'title_en': 'Instance Counter & Factory Constructor',
                    'instructions_sk': (
                        "Vytvor triedu `Kurz`:\n"
                        "1. Obsahuje triedny atribút `pocet_kurzov = 0`.\n"
                        "2. `__init__(self, nazov, hodiny)`: uloží atribúty a zvýši `Kurz.pocet_kurzov` o 1.\n"
                        "3. `@classmethod z_textu(cls, retazec)`: alternatívny konštruktor, ktorý rozdelí text v tvare `\"Python;40\"` a vráti novú inštanciu `cls(nazov, int(hodiny))`."
                    ),
                    'instructions_en': 'Create class `Kurz` tracking `pocet_kurzov` and implementing `@classmethod z_textu(cls, retazec)`.',
                    'starter_code': 'class Kurz:\n    pass\n',
                    'solution_code': 'class Kurz:\n    pocet_kurzov = 0\n    def __init__(self, nazov, hodiny):\n        self.nazov = nazov\n        self.hodiny = hodiny\n        Kurz.pocet_kurzov += 1\n    @classmethod\n    def z_textu(cls, retazec):\n        nazov, hod = retazec.split(";")\n        return cls(nazov, int(hod))\n',
                    'explanation_sk': 'Používame triedny atribút pre evidenciu inštancií a classmethod ako továreň (factory).',
                    'explanation_en': 'Class variable acts as global instance counter; classmethod parses serialized string.',
                    'hint_sk': 'nazov, hod = retazec.split(";"); return cls(nazov, int(hod)).',
                    'hint_en': 'nazov, hod = retazec.split(";"); return cls(nazov, int(hod)).',
                    'hint_cost_doros': 15,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 50,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'Kurz.pocet_kurzov = 0; k = Kurz.z_textu("Python;40"); (k.nazov, k.hodiny, Kurz.pocet_kurzov)', 'expected_output': '("Python", 40, 1)', 'test_code': 'Kurz.pocet_kurzov = 0\nk = Kurz.z_textu("Python;40")\nassert (k.nazov, k.hodiny, Kurz.pocet_kurzov) == ("Python", 40, 1)', 'is_hidden': False},
                        {'input_data': 'k2 = Kurz("Django", 20); Kurz.pocet_kurzov', 'expected_output': '2', 'test_code': 'k2 = Kurz("Django", 20)\nassert Kurz.pocet_kurzov == 2', 'is_hidden': False},
                        {'input_data': 'k3 = Kurz.z_textu("SQL;15"); k3.hodiny', 'expected_output': '15', 'test_code': 'k3 = Kurz.z_textu("SQL;15")\nassert k3.hodiny == 15', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Zapuzdrenie (Encapsulation), privátne atribúty a dekorátor @property',
            'title_en': 'Encapsulation, Private Attributes & @property',
            'summary_sk': 'Konvencie _chraneny a __sukromny (Name Mangling), riadený prístup cez getter a setter (@property).',
            'summary_en': 'Encapsulation principles, _protected and __private name mangling, getters and setters with @property.',
            'estimated_minutes': 60,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 9.4 Zapuzdrenie a dekorátor `@property`

**Zapuzdrenie (Encapsulation)** chráni vnútorný stav objektu pred neoprávneným zásahom zvonku.

#### Úrovne viditeľnosti v Pythone:
- `verejny` – bežný prístup odkiaľkoľvek.
- `_chraneny` – jeden podčiarkovník je dohoda medzi programátormi: "Interný detail, nemeň zvonku!".
- `__sukromny` – dva podčiarkovníky aktivujú tzv. **Name Mangling** (prepísanie na `_Trieda__sukromny`).

#### Pythonické gettery a settery pomocou `@property`:
```python
class Hrac:
    def __init__(self, hp):
        self._hp = hp

    @property
    def hp(self):
        # Getter: pristupujeme ako k premennej hrac.hp
        return self._hp

    @hp.setter
    def hp(self, hodnota):
        # Setter: overí validitu pred zápisom
        if hodnota < 0:
            self._hp = 0
        else:
            self._hp = min(100, hodnota)
```
""",
            'content_en': """### 9.4 Encapsulation and @property

Python implements controlled attribute access using `@property` getters and `@prop.setter` methods without breaking existing API dot syntax.
""",
            'quizzes': [
                {
                    'question_sk': 'Ako sa volá mechanizmus, ktorým Python prepíše atribút s dvoma podčiarkovníkmi (napr. `__heslo`) na tvar `_Trieda__heslo`?',
                    'question_en': 'What is Python mechanism that mangles double leading underscore attributes called?',
                    'option_a_sk': 'Name Mangling', 'option_a_en': 'Name Mangling',
                    'option_b_sk': 'Encapsulation Shield', 'option_b_en': 'Encapsulation Shield',
                    'option_c_sk': 'Private Wrapper', 'option_c_en': 'Private Wrapper',
                    'option_d_sk': 'Memory Protection', 'option_d_en': 'Memory Protection',
                    'correct_option': 'A',
                    'explanation_sk': 'Mechanizmus Name Mangling zabraňuje nechcenému prepísaniu privátneho atribútu v podtriedach.',
                    'explanation_en': 'Name mangling transforms __attr into _ClassName__attr to prevent accidental namespace collisions.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Teplomer s riadeným prístupom cez @property',
                    'title_en': 'Thermometer with Validated Properties',
                    'instructions_sk': (
                        "Vytvor triedu `Teplomer`:\n"
                        "1. `__init__(self, celsius=0.0)`: nastaví počiatočnú teplotu cez setter.\n"
                        "2. Getter `@property celsius(self)`: vráti `self._celsius`.\n"
                        "3. Setter `@celsius.setter`: ak je nová teplota nižšia ako absolútna nula ($-273.15$ °C), vyvolá `ValueError(\"Teplota pod absolútnou nulou!\")`. Inak ju uloží do `self._celsius`.\n"
                        "4. Getter `@property fahrenheit(self)`: vráti teplotu prepočítanú na stupne Fahrenheita podľa vzorca: $F = C \\cdot 1.8 + 32$ zaokrúhlenú na 2 desatinné miesta."
                    ),
                    'instructions_en': 'Create `Teplomer` class with validated `@property celsius` (raising ValueError below -273.15) and computed `@property fahrenheit`.',
                    'starter_code': 'class Teplomer:\n    pass\n',
                    'solution_code': 'class Teplomer:\n    def __init__(self, celsius=0.0):\n        self.celsius = celsius\n    @property\n    def celsius(self):\n        return self._celsius\n    @celsius.setter\n    def celsius(self, value):\n        if value < -273.15:\n            raise ValueError("Teplota pod absolútnou nulou!")\n        self._celsius = float(value)\n    @property\n    def fahrenheit(self):\n        return round(self._celsius * 1.8 + 32, 2)\n',
                    'explanation_sk': 'Využívame zapuzdrenie cez @property a @celsius.setter s validáciou fyzikálneho limitu.',
                    'explanation_en': 'Encapsulation with property getter, validated setter, and computed Fahrenheit conversion.',
                    'hint_sk': 'if value < -273.15: raise ValueError("..."); self._celsius = float(value).',
                    'hint_en': 'if value < -273.15: raise ValueError("..."); self._celsius = float(value).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 't = Teplomer(25.0); (t.celsius, t.fahrenheit)', 'expected_output': '(25.0, 77.0)', 'test_code': 't = Teplomer(25.0)\nassert (t.celsius, t.fahrenheit) == (25.0, 77.0)', 'is_hidden': False},
                        {'input_data': 't = Teplomer(); t.celsius = -300', 'expected_output': 'ValueError', 'test_code': 't = Teplomer()\ntry:\n    t.celsius = -300\n    assert False, "Malo vyvolať ValueError"\nexcept ValueError:\n    pass', 'is_hidden': False},
                        {'input_data': 't = Teplomer(0.0); t.fahrenheit', 'expected_output': '32.0', 'test_code': 't = Teplomer(0.0)\nassert t.fahrenheit == 32.0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Komplexný OOP projekt: Herný inventár a ekonomika postavy',
            'title_en': 'OOP Capstone Project: Character Inventory & Economy',
            'summary_sk': 'Prepojenie tried, objektovej interakcie a manažmentu položiek v praxi.',
            'summary_en': 'Multi-class coordination, item management, and character inventory architecture.',
            'estimated_minutes': 60,
            'xp_reward': 45,
            'is_published': True,
            'content_sk': """### 9.5 Prepojenie objektov v systéme

V skutočných aplikáciách objekty spolupracujú: trieda `Postava` môže obsahovať inštanciu triedy `Inventar`, ktorá obsahuje zoznam objektov `Polozka`.

V nasledujúcom cvičení vytvoríš ucelený mini-systém tried modelujúci hernú ekonomiku.
""",
            'content_en': """### 9.5 Object Collaboration & Systems Design

Classes collaborating together: Character, Inventory, and Item objects interacting cleanly.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo predstavuje vzťah "Has-A" v objektovo-orientovanom návrhu?',
                    'question_en': 'What does a "Has-A" relationship represent in object-oriented design?',
                    'option_a_sk': 'Kompozíciu / agregáciu (objekt obsahuje referenciu na iný objekt)', 'option_a_en': 'Composition / aggregation (an object holds a reference to another object)',
                    'option_b_sk': 'Dedičnosť tried', 'option_b_en': 'Inheritance',
                    'option_c_sk': 'SyntaxError', 'option_c_en': 'SyntaxError',
                    'option_d_sk': 'Výnimku v Pythone', 'option_d_en': 'Python exception',
                    'correct_option': 'A',
                    'explanation_sk': 'Vzťah Has-A vyjadruje vlastníctvo (Hráč MÁ Inventár, Auto MÁ Motor).',
                    'explanation_en': 'Has-A denotes composition where one class instance contains another.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Herný inventár s váhovým limitom',
                    'title_en': 'Weight-Limited Character Inventory',
                    'instructions_sk': (
                        "Vytvor triedu `Inventar` s konštruktorom `__init__(self, max_nosnost)`:\n"
                        "- Atribút `self.max_nosnost` a prázdny zoznam `self.polozky = []`.\n"
                        "- Metóda `pridaj_polozku(self, nazov, vaha)`: ak by po pridaní celková váha presiahla `max_nosnost`, vráti `False` a položku nepridá. Inak pridá dvojicu `(nazov, vaha)` a vráti `True`.\n"
                        "- `@property celkova_vaha(self)`: vráti aktuálny súčet váh všetkých položiek."
                    ),
                    'instructions_en': 'Create `Inventar` with `max_nosnost`, `pridaj_polozku(nazov, vaha)`, and `@property celkova_vaha`.',
                    'starter_code': 'class Inventar:\n    pass\n',
                    'solution_code': 'class Inventar:\n    def __init__(self, max_nosnost):\n        self.max_nosnost = max_nosnost\n        self.polozky = []\n    @property\n    def celkova_vaha(self):\n        return sum(v for _, v in self.polozky)\n    def pridaj_polozku(self, nazov, vaha):\n        if self.celkova_vaha + vaha > self.max_nosnost:\n            return False\n        self.polozky.append((nazov, vaha))\n        return True\n',
                    'explanation_sk': 'Objektové zapuzdrenie pravidiel inventára a váhového limitu.',
                    'explanation_en': 'Object state management validating weight limits before appending tuples.',
                    'hint_sk': 'sum(v for _, v in self.polozky); if self.celkova_vaha + vaha > self.max_nosnost: return False.',
                    'hint_en': 'sum(v for _, v in self.polozky); if self.celkova_vaha + vaha > self.max_nosnost: return False.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 70,
                    'doros_reward': 35,
                    'test_cases': [
                        {'input_data': 'inv = Inventar(10); inv.pridaj_polozku("Meč", 4); inv.celkova_vaha', 'expected_output': '4', 'test_code': 'inv = Inventar(10)\nassert inv.pridaj_polozku("Meč", 4) is True\nassert inv.celkova_vaha == 4', 'is_hidden': False},
                        {'input_data': 'inv = Inventar(10); inv.pridaj_polozku("Meč", 4); inv.pridaj_polozku("Brnenie", 7)', 'expected_output': 'False', 'test_code': 'inv = Inventar(10)\ninv.pridaj_polozku("Meč", 4)\nassert inv.pridaj_polozku("Brnenie", 7) is False\nassert inv.celkova_vaha == 4', 'is_hidden': False},
                        {'input_data': 'inv = Inventar(5); inv.pridaj_polozku("Elixír", 5); inv.celkova_vaha', 'expected_output': '5', 'test_code': 'inv = Inventar(5)\nassert inv.pridaj_polozku("Elixír", 5) is True\nassert inv.celkova_vaha == 5', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
