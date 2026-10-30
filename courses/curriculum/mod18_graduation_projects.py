"""
MODUL 18: Komplexné záverečné Boss Projekty a certifikačná skúška
Kariérna cesta: 5. Maturitný špeciál a Projekty (MATURITA_PREP)
Odhadovaný rozsah: 16 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU
"""

MODULE_DATA = {
    'order': 18,
    'track': 'MATURITA_PREP',
    'title_sk': 'Komplexné záverečné Boss Projekty a certifikačná skúška',
    'title_en': 'Final Capstone Boss Projects & Certification Exam',
    'description_sk': 'Zavŕšenie celého štúdia Codoro Python Developer: komplexné softvérové mini-systémy integrujúce OOP, dátové štruktúry, ošetrenie chýb, prácu so súbormi a algoritmické myslenie do portfólia.',
    'description_en': 'The ultimate capstone of Codoro Python Developer curriculum: comprehensive software engines combining OOP, data structures, defensive error handling, file parsing, and algorithmic problem-solving.',
    'programming_language': 'python',
    'estimated_hours': 16,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'trophy',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Projekt 1: Elektronická žiacka knižka a štatistický analyzátor',
            'title_en': 'Project 1: Electronic Gradebook & Academic Analytics',
            'summary_sk': 'Štatistický analyzátor triedy, vážené priemery, vyznamenania a generovanie reportu.',
            'summary_en': 'Academic gradebook analytics, weighted GPA, honors classification, and reporting.',
            'estimated_minutes': 75,
            'xp_reward': 60,
            'is_published': True,
            'content_sk': """### 18.1 Projekt: Školský analyzátor známok a štatistika úspešnosti

V tomto praktickom projekte navrhneme objektový model pre triedneho učiteľa, ktorý eviduje známky žiakov z jednotlivých predmetov, počíta vážené priemery a určuje, ktorí študenti prospeli s vyznamenaním.

#### 1. Architektúra dátového modelu

| Trieda / Metóda | Vstupné parametre | Návratová hodnota | Účel |
| :--- | :--- | :--- | :--- |
| `ZiackaKnizka()` | žiadne | Inštancia | Inicializuje slovník známok `{predmet: [známky]}` |
| `pridaj_znamku(predmet, z)` | `str`, `int` (1-5) | `bool` | Zvaliduje rozsah 1 až 5 a zapíše známku |
| `priemer_predmetu(predmet)` | `str` | `float` alebo `None` | Priemer známok daného predmetu na 2 des. miesta |
| `celkovy_priemer()` | žiadne | `float` | Celkový priemer zo všetkých predmetov dohromady |

#### 2. Kódový vzor: Bezpečná evidencia známok
```python
class ZiackaKnizka:
    def __init__(self):
        # Kľúč je názov predmetu, hodnota je zoznam celočíselných známok
        self.znamky = {}

    def pridaj_znamku(self, predmet: str, znamka: int) -> bool:
        if not isinstance(znamka, int) or not (1 <= znamka <= 5):
            return False
        if predmet not in self.znamky:
            self.znamky[predmet] = []
        self.znamky[predmet].append(znamka)
        return True
```

> **Častá chyba v praxi:**
> Delenie nulou pri výpočte priemeru, ak študent nemá zapísanú žiadnu známku. Pred volaním `sum(znamky) / len(znamky)` vždy skontroluj, či `len(znamky) > 0`!

#### 3. Zhrnutie kľúčových konceptov
- Použitie slovníka zoznamov na reprezentáciu relácie 1:N (jeden predmet má mnoho známok).
- Defenzívna validácia zabraňuje zápisu neplatných známok (napr. 0 alebo 6).
- Bezpečné zaokrúhľovanie metódou `round(priemer, 2)`.
""",
            'content_en': """### 18.1 Project: Academic Gradebook Analytics Engine

Build a structured school gradebook engine tracking per-subject grades, computing weighted GPA, and filtering honor roll students.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú výhodu má reprezentácia známok študenta pomocou slovníka `{"predmet": [znamky]}` namiesto plochého zoznamu?',
                    'question_en': 'What advantage does structuring grades as `{"subject": [grades]}` offer over flat lists?',
                    'option_a_sk': 'Umožňuje separátny výpočet priemerov pre jednotlivé predmety v O(1) vyhľadávaní',
                    'option_a_en': 'Enables per-subject average calculations with O(1) key indexing',
                    'option_b_sk': 'Šetrí registre procesora',
                    'option_b_en': 'Saves CPU registers',
                    'option_c_sk': 'Eliminuje potrebu funkcií',
                    'option_c_en': 'Eliminates functions',
                    'option_d_sk': 'Automaticky synchronizuje dáta na cloud',
                    'option_d_en': 'Cloud sync',
                    'correct_option': 'A',
                    'explanation_sk': 'Slovníková štruktúra logicky oddeľuje známky podľa predmetu a umožňuje okamžitý prístup v čase O(1).',
                    'explanation_en': 'Structured mapping separates domain namespaces for modular analytics.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Úloha 1 (Ľahká): Výpočet aritmetického priemeru',
                    'title_en': 'Exercise 1 (Easy): Arithmetic Mean Calculation',
                    'instructions_sk': 'Napíš funkciu `spocitaj_priemer(znamky)`, ktorá vráti aritmetický priemer zoznamu čísel zaokrúhlený na 2 desatinné miesta. Ak je zoznam prázdny, vráti `0.0`.',
                    'instructions_en': 'Write `spocitaj_priemer(znamky)` returning rounded float average to 2 decimal places or 0.0 if empty.',
                    'starter_code': 'def spocitaj_priemer(znamky):\n    pass\n',
                    'solution_code': 'def spocitaj_priemer(znamky):\n    if not znamky:\n        return 0.0\n    return round(sum(znamky) / len(znamky), 2)\n',
                    'explanation_sk': 'Základná agregácia sum() a len() s ošetrením prázdneho zoznamu.',
                    'explanation_en': 'Sum and length aggregation handling empty lists.',
                    'hint_sk': 'if not znamky: return 0.0; return round(sum(znamky)/len(znamky), 2)',
                    'hint_en': 'Check for empty list first.',
                    'hint_cost_doros': 5,
                    'difficulty': 'EASY',
                    'xp_reward': 25,
                    'doros_reward': 10,
                    'test_cases': [
                        {'input_data': 'spocitaj_priemer([1, 2, 3, 4, 5])', 'expected_output': '3.0', 'test_code': 'assert spocitaj_priemer([1, 2, 3, 4, 5]) == 3.0', 'is_hidden': False},
                        {'input_data': 'spocitaj_priemer([])', 'expected_output': '0.0', 'test_code': 'assert spocitaj_priemer([]) == 0.0', 'is_hidden': False},
                        {'input_data': 'spocitaj_priemer([1, 1, 2])', 'expected_output': '1.33', 'test_code': 'assert spocitaj_priemer([1, 1, 2]) == 1.33', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Úloha 2 (Stredná): Zoradenie študentov podľa priemeru',
                    'title_en': 'Exercise 2 (Medium): Ranking Students by Average',
                    'instructions_sk': 'Napíš funkciu `zorad_podla_priemeru(studenti)`: parameter je zoznam n-tíc `[("Meno", [znamky])]`. Funkcia vráti nový zoznam mien zoradených vzostupne podľa ich priemeru známok (od najlepšieho, t.j. najnižší priemer prvý).',
                    'instructions_en': 'Write `zorad_podla_priemeru(studenti)` sorting student names ascending by GPA.',
                    'starter_code': 'def zorad_podla_priemeru(studenti):\n    pass\n',
                    'solution_code': 'def zorad_podla_priemeru(studenti):\n    def get_avg(item):\n        znamky = item[1]\n        return sum(znamky) / len(znamky) if znamky else 5.0\n    zoradeni = sorted(studenti, key=get_avg)\n    return [meno for meno, _ in zoradeni]\n',
                    'explanation_sk': 'Použitie funkcie sorted() s kľúčom počítajúcim priemer študenta.',
                    'explanation_en': 'Sorting tuples using key extractor returning float average.',
                    'hint_sk': 'Použi sorted(studenti, key=lambda s: sum(s[1])/len(s[1])) a vytiahni mená.',
                    'hint_en': 'Use sorted with custom key extractor.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'zorad_podla_priemeru([("Peter", [1, 1]), ("Ján", [2, 3]), ("Anna", [1, 2])])', 'expected_output': '["Peter", "Anna", "Ján"]', 'test_code': 'assert zorad_podla_priemeru([("Peter", [1, 1]), ("Ján", [2, 3]), ("Anna", [1, 2])]) == ["Peter", "Anna", "Ján"]', 'is_hidden': False},
                        {'input_data': 'zorad_podla_priemeru([("B", [3]), ("A", [1])])', 'expected_output': '["A", "B"]', 'test_code': 'assert zorad_podla_priemeru([("B", [3]), ("A", [1])]) == ["A", "B"]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Úloha 3 (Boss Výzva): Engine žiackej knižky s validáciou',
                    'title_en': 'Exercise 3 (Boss Challenge): Full Gradebook Engine Class',
                    'instructions_sk': (
                        "Vytvor triedu `ZiackaKnizka`:\n"
                        "1. `__init__(self)`: inicializuje prázdny slovník `self.znamky = {}` (kľúč = predmet, hodnota = zoznam známok `[int]`).\n"
                        "2. `pridaj_znamku(self, predmet, znamka)`: ak je známka celé číslo v rozsahu 1 až 5, pridá ju k predmetu a vráti `True`. Inak vráti `False`.\n"
                        "3. `priemer_predmetu(self, predmet)`: vráti zaokrúhlený priemer známok daného predmetu na 2 desatinné miesta. Ak predmet nemá známky, vráti `None`.\n"
                        "4. `celkovy_priemer(self)`: vráti zaokrúhlený priemer zo VŠETKÝCH známok vo všetkých predmetoch na 2 desatinné miesta. Ak nie sú žiadne známky, vráti `0.0`."
                    ),
                    'instructions_en': 'Implement class `ZiackaKnizka` with `pridaj_znamku`, `priemer_predmetu`, and `celkovy_priemer`.',
                    'starter_code': 'class ZiackaKnizka:\n    pass\n',
                    'solution_code': 'class ZiackaKnizka:\n    def __init__(self):\n        self.znamky = {}\n    def pridaj_znamku(self, predmet, znamka):\n        if not isinstance(znamka, int) or not (1 <= znamka <= 5):\n            return False\n        if predmet not in self.znamky:\n            self.znamky[predmet] = []\n        self.znamky[predmet].append(znamka)\n        return True\n    def priemer_predmetu(self, predmet):\n        zozn = self.znamky.get(predmet)\n        if not zozn:\n            return None\n        return round(sum(zozn) / len(zozn), 2)\n    def celkovy_priemer(self):\n        vsetky = []\n        for z in self.znamky.values():\n            vsetky.extend(z)\n        if not vsetky:\n            return 0.0\n        return round(sum(vsetky) / len(vsetky), 2)\n',
                    'explanation_sk': 'Komplexná práca so slovníkom zoznamov, validáciou rozsahov 1-5 a celkovou agregáciou.',
                    'explanation_en': 'Structured mapping of lists, boundary verification, and nested aggregations.',
                    'hint_sk': 'self.znamky.setdefault(predmet, []).append(znamka).',
                    'hint_en': 'self.znamky.setdefault(predmet, []).append(znamka).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 80,
                    'doros_reward': 40,
                    'test_cases': [
                        {'input_data': 'zk = ZiackaKnizka(); zk.pridaj_znamku("Python", 1); zk.pridaj_znamku("Python", 2); zk.priemer_predmetu("Python")', 'expected_output': '1.5', 'test_code': 'zk = ZiackaKnizka()\nzk.pridaj_znamku("Python", 1)\nzk.pridaj_znamku("Python", 2)\nassert zk.priemer_predmetu("Python") == 1.5', 'is_hidden': False},
                        {'input_data': 'zk = ZiackaKnizka(); zk.pridaj_znamku("Mat", 6)', 'expected_output': 'False', 'test_code': 'zk = ZiackaKnizka()\nassert zk.pridaj_znamku("Mat", 6) is False', 'is_hidden': False},
                        {'input_data': 'zk = ZiackaKnizka(); zk.pridaj_znamku("A", 1); zk.pridaj_znamku("B", 3); zk.celkovy_priemer()', 'expected_output': '2.0', 'test_code': 'zk = ZiackaKnizka()\nzk.pridaj_znamku("A", 1)\nzk.pridaj_znamku("B", 3)\nassert zk.celkovy_priemer() == 2.0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Projekt 2: E-shop nákupný košík s kupónmi a riadením zásob',
            'title_en': 'Project 2: E-Commerce Shopping Cart with Inventory and Coupons',
            'summary_sk': 'Objektový model e-shopu, riadenie zásob, uplatnenie promo kódu a DPH.',
            'summary_en': 'E-commerce cart domain modeling, stock inventory locks, discount coupons, and tax calculation.',
            'estimated_minutes': 75,
            'xp_reward': 60,
            'is_published': True,
            'content_sk': """### 18.2 Projekt: E-shop Cart Engine a promo kupóny

Internetový obchod potrebuje robustný systém na správu košíka. Systém musí spoľahlivo spočítať medzisúčet, overiť dostupnosť na sklade a aplikovať percentuálne či fixné zľavy bez rizika zápornej konečnej ceny.

#### 1. Architektúra výpočtu košíka

| Komponent | Vstupy | Očakávaný výsledok |
| :--- | :--- | :--- |
| Položka v košíku | `nazov`, `cena`, `pocet` | Záznam o cene a množstve |
| Medzisúčet (Subtotal) | sum(cena × kusy) | Hrubá cena pred zľavou |
| Zľavový kupón | `percento` (0 - 100) | `medzisucet * (1 - zlava / 100)` |
| Minimálna cena | max(0.0, vypocet) | Zabezpečenie proti preplateniu |

#### 2. Kódový vzor: Bezpečný výpočet zľavy
```python
def aplikuj_zlavu(medzisucet: float, percento: float) -> float:
    if percento < 0 or percento > 100:
        raise ValueError("Neplatné percento zľavy")
    konecna_cena = medzisucet * (1 - percento / 100.0)
    return round(max(0.0, konecna_cena), 2)
```

> **Častá chyba v praxi:**
> Zaokrúhľovanie peňažných súm príliš skoro v medzivýpočtoch. To spôsobuje halierové nezrovnalosti. Zaokrúhľuj pomocou `round(..., 2)` až výslednú hodnotu!

#### 3. Zhrnutie
- Reprezentácia košíka pomocou slovníka `self.polozky = {nazov: (cena, kusy)}`.
- Správna aggregácia súčtu položiek pomocou generátorového výrazu.
- Ochrana proti zápornej cene cez `max(0.0, vysledok)`.
""",
            'content_en': """### 18.2 Project: E-Commerce Shopping Cart Engine

Build checkout engine calculating subtotal, validating inventory limits, applying percentage coupons, and computing final invoices.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo je dôležité počítať peňažné sumy s desatinným zaokrúhlením až na samom konci výpočtového reťazca?',
                    'question_en': 'Why should rounding occur at the end of financial calculations?',
                    'option_a_sk': 'Aby sa predišlo kumulácii chýb spôsobených predčasným zaokrúhľovaním medzivýsledkov',
                    'option_a_en': 'To prevent error accumulation from intermediate truncations',
                    'option_b_sk': 'Pretože funkcia round() spomaľuje procesor',
                    'option_b_en': 'round is slow',
                    'option_c_sk': 'Pretože to vyžaduje formát JSON',
                    'option_c_en': 'JSON requirement',
                    'option_d_sk': 'Nemá to žiadny vplyv na výsledok',
                    'option_d_en': 'No difference',
                    'correct_option': 'A',
                    'explanation_sk': 'Predčasné zaokrúhľovanie v každom kroku spôsobuje kumuláciu nepresností v účtovníctve.',
                    'explanation_en': 'Premature rounding compounds numerical drift in financial calculations.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Úloha 1 (Ľahká): Aplikácia percentuálneho kupónu',
                    'title_en': 'Exercise 1 (Easy): Percentage Discount Coupon',
                    'instructions_sk': 'Napíš funkciu `aplikuj_kupon(cena, percento_zlavy)`: odpočíta zľavu z ceny a vráti zaokrúhlenú cenu na 2 desatinné miesta. Ak je výsledok záporný, vráti `0.0`.',
                    'instructions_en': 'Write `aplikuj_kupon(cena, percento_zlavy)` returning discounted price bounded at 0.0.',
                    'starter_code': 'def aplikuj_kupon(cena, percento_zlavy):\n    pass\n',
                    'solution_code': 'def aplikuj_kupon(cena, percento_zlavy):\n    vysledok = cena * (1 - percento_zlavy / 100.0)\n    return round(max(0.0, vysledok), 2)\n',
                    'explanation_sk': 'Výpočet zľavy s ochranou proti zápornej cene pomocou max().',
                    'explanation_en': 'Discount calculation with max(0.0, ...) boundary guard.',
                    'hint_sk': 'max(0.0, cena * (1 - percento_zlavy/100))',
                    'hint_en': 'Calculate percentage and clamp with max(0.0, ...).',
                    'hint_cost_doros': 5,
                    'difficulty': 'EASY',
                    'xp_reward': 25,
                    'doros_reward': 10,
                    'test_cases': [
                        {'input_data': 'aplikuj_kupon(100.0, 20)', 'expected_output': '80.0', 'test_code': 'assert aplikuj_kupon(100.0, 20) == 80.0', 'is_hidden': False},
                        {'input_data': 'aplikuj_kupon(50.0, 110)', 'expected_output': '0.0', 'test_code': 'assert aplikuj_kupon(50.0, 110) == 0.0', 'is_hidden': False},
                        {'input_data': 'aplikuj_kupon(33.33, 10)', 'expected_output': '30.0', 'test_code': 'assert aplikuj_kupon(33.33, 10) == 30.0', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Úloha 2 (Stredná): Overenie skladových zásob',
                    'title_en': 'Exercise 2 (Medium): Inventory Stock Check',
                    'instructions_sk': 'Napíš funkciu `over_sklad(sklad, kosik)`: `sklad` je slovník `{produkt: pocet_na_sklade}`, `kosik` je slovník `{produkt: ziadany_pocet}`. Funkcia vráti zoznam produktov, ktorých je v košíku viac ako na sklade (alebo na sklade vôbec nie sú). Ak je všetko na sklade, vráti prázdny zoznam `[]`.',
                    'instructions_en': 'Write `over_sklad(sklad, kosik)` returning list of out-of-stock or deficit items.',
                    'starter_code': 'def over_sklad(sklad, kosik):\n    pass\n',
                    'solution_code': 'def over_sklad(sklad, kosik):\n    chybajuce = []\n    for prod, qty in kosik.items():\n        dostupne = sklad.get(prod, 0)\n        if qty > dostupné:\n            chybajuce.append(prod)\n    return chybajuce\n',
                    'explanation_sk': 'Porovnanie požadovaného množstva s dostupnými zásobami v sklade.',
                    'explanation_en': 'Dictionary comparison identifying requested items exceeding stock inventory.',
                    'hint_sk': 'for prod, qty in kosik.items(): if qty > sklad.get(prod, 0): ...',
                    'hint_en': 'Compare quantities with sklad.get(prod, 0).',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'over_sklad({"kniha": 5, "pero": 2}, {"kniha": 3, "pero": 5})', 'expected_output': '["pero"]', 'test_code': 'assert over_sklad({"kniha": 5, "pero": 2}, {"kniha": 3, "pero": 5}) == ["pero"]', 'is_hidden': False},
                        {'input_data': 'over_sklad({"kniha": 5}, {"kniha": 2})', 'expected_output': '[]', 'test_code': 'assert over_sklad({"kniha": 5}, {"kniha": 2}) == []', 'is_hidden': False},
                        {'input_data': 'over_sklad({"a": 1}, {"b": 1})', 'expected_output': '["b"]', 'test_code': 'assert over_sklad({"a": 1}, {"b": 1}) == ["b"]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Úloha 3 (Boss Výzva): Trieda nákupného košíka s kupónom',
                    'title_en': 'Exercise 3 (Boss Challenge): Shopping Cart Class',
                    'instructions_sk': (
                        "Vytvor triedu `Kosik`:\n"
                        "1. `__init__(self)`: `self.polozky = {}` (kľúč = názov, hodnota = `(cena_za_kus, pocet_kusov)`).\n"
                        "2. `pridaj(self, nazov, cena, kusov=1)`: pridá alebo navýši počet kusov danej položky.\n"
                        "3. `medzisucet(self)`: vráti celkovú cenu všetkých položiek pred zľavou.\n"
                        "4. `vypocitaj_celkovo(self, percento_zlavy=0)`: odpočíta zľavu z medzisúčtu a vráti výsledok zaokrúhlený na 2 desatinné miesta. Cena nesmie byť záporná (minimum 0.0)."
                    ),
                    'instructions_en': 'Implement class `Kosik` with `pridaj`, `medzisucet`, and `vypocitaj_celkovo(percento_zlavy)`.',
                    'starter_code': 'class Kosik:\n    pass\n',
                    'solution_code': 'class Kosik:\n    def __init__(self):\n        self.polozky = {}\n    def pridaj(self, nazov, cena, kusov=1):\n        if nazov in self.polozky:\n            stara_cena, stary_pocet = self.polozky[nazov]\n            self.polozky[nazov] = (cena, stary_pocet + kusov)\n        else:\n            self.polozky[nazov] = (cena, kusov)\n    def medzisucet(self):\n        return sum(cena * kusov for cena, kusov in self.polozky.values())\n    def vypocitaj_celkovo(self, percento_zlavy=0):\n        sub = self.medzisucet()\n        zlava = sub * (percento_zlavy / 100)\n        vysledok = max(0.0, sub - zlava)\n        return round(vysledok, 2)\n',
                    'explanation_sk': 'Skladový manažment cien a kusov položiek v košíku s aplikáciou zľavy.',
                    'explanation_en': 'Item pricing tracking quantity and computing discount bounded at 0.0.',
                    'hint_sk': 'sub = self.medzisucet(); return round(max(0.0, sub * (1 - percento_zlavy/100)), 2).',
                    'hint_en': 'sub = self.medzisucet(); return round(max(0.0, sub * (1 - percento_zlavy/100)), 2).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 80,
                    'doros_reward': 40,
                    'test_cases': [
                        {'input_data': 'k = Kosik(); k.pridaj("Kniha", 10.0, 2); k.pridaj("Pero", 2.0, 5); k.medzisucet()', 'expected_output': '30.0', 'test_code': 'k = Kosik()\nk.pridaj("Kniha", 10.0, 2)\nk.pridaj("Pero", 2.0, 5)\nassert k.medzisucet() == 30.0', 'is_hidden': False},
                        {'input_data': 'k = Kosik(); k.pridaj("Tričko", 100.0, 1); k.vypocitaj_celkovo(20)', 'expected_output': '80.0', 'test_code': 'k = Kosik()\nk.pridaj("Tričko", 100.0, 1)\nassert k.vypocitaj_celkovo(20) == 80.0', 'is_hidden': False},
                        {'input_data': 'k = Kosik(); k.vypocitaj_celkovo()', 'expected_output': '0.0', 'test_code': 'k = Kosik()\nassert k.vypocitaj_celkovo() == 0.0', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Projekt 3: Bezpečnostný incident manager a sieťový analyzátor',
            'title_en': 'Project 3: Security Incident Manager & Network Log Analyzer',
            'summary_sk': 'Monitorovanie sieťových logov, detekcia brute-force útokov a blacklistovanie IP adries.',
            'summary_en': 'Network log inspection, brute-force attack heuristics, IP blacklisting, and alert reporting.',
            'estimated_minutes': 75,
            'xp_reward': 60,
            'is_published': True,
            'content_sk': """### 18.3 Projekt: Bezpečnostný incident manager a parsovanie logov

Kybernetická bezpečnosť vyžaduje neustály audit logov servera. V tomto projekte implementujeme systém, ktorý sleduje neúspešné pokusy o prihlásenie a automaticky blokuje útočníkov.

#### 1. Architektúra detektora útokov

| Funkcia / Metóda | Vstup | Výstup | Popis |
| :--- | :--- | :--- | :--- |
| `parsuj_ip_a_port(adresa)` | `"192.168.1.1:8080"` | `("192.168.1.1", 8080)` | Rozdelenie sieťového soketu |
| `detekuj_bruteforce(logy, limit)` | Zoznam záznamov, prah | Zoznam IP adries | Nájde IP s $\\ge$ limit neúspešnými pokusmi |
| `IncidentManager()` | Inštancia | Objekt | Evidencia incidentov a blacklist |

#### 2. Kódový vzor: Frekvenčná analýza podozrivých IP
```python
def detekuj_utocnikov(logy: list[dict], threshold: int = 3) -> list[str]:
    neúspešné = {}
    for entry in logy:
        if entry.get("status") == "FAILED":
            ip = entry.get("ip")
            neúspešné[ip] = neúspešné.get(ip, 0) + 1
    return [ip for ip, cnt in neúspešné.items() if cnt >= threshold]
```

> **Častá chyba v praxi:**
> Zlyhanie pri rozdeľovaní reťazca IP:port, ak port nie je celé číslo. Vždy over `port.isdigit()` alebo preveď cez `int()` s ošetrením `ValueError`!

#### 3. Zhrnutie
- Rýchle vyhľadávanie a agregácia udalostí pomocou slovníka.
- Filtrovanie zoznamu podľa frekvenčného prahu (Threshold).
- Správa stavu zoznamu zablokovaných adries cez množinu `set()`.
""",
            'content_en': """### 18.3 Project: Security Incident Manager

Build network log analyzer identifying brute-force failed login patterns and blacklisting malicious IP addresses.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú dátovú štruktúru je v Pythone najvhodnejšie použiť na ukladanie zablokovaných IP adries (Blacklist)?',
                    'question_en': 'Which Python data structure is ideal for storing blacklisted IP addresses?',
                    'option_a_sk': 'Množinu set(), pretože overenie "ip in blacklist" prebieha v priemernom čase O(1)',
                    'option_a_en': 'set(), because membership testing "ip in blacklist" runs in O(1) average time',
                    'option_b_sk': 'Zoznam list(), pretože zoznam je najdlhší',
                    'option_b_en': 'list(), because lists are longer',
                    'option_c_sk': 'N-ticu tuple(), pretože sa nedá meniť',
                    'option_c_en': 'tuple(), because immutable',
                    'option_d_sk': 'Reťazec str()',
                    'option_d_en': 'str() string',
                    'correct_option': 'A',
                    'explanation_sk': 'Hašovacia tabuľka množiny set() umožňuje okamžité O(1) overenie blokovania aj pre milióny IP adries.',
                    'explanation_en': 'Set hash lookup guarantees constant time O(1) query verification.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Úloha 1 (Ľahká): Rozdelenie IP adresy a portu',
                    'title_en': 'Exercise 1 (Easy): Parse Socket IP and Port',
                    'instructions_sk': 'Napíš funkciu `parsuj_ip_a_port(adresa)`: reťazec v tvare `"IP:PORT"` (napr. `"192.168.1.1:8080"`). Funkcia vráti dvojicu `(ip_str, port_int)`. Ak reťazec neobsahuje dvojbodku, vráti `None`.',
                    'instructions_en': 'Write `parsuj_ip_a_port(adresa)` returning tuple (ip_str, port_int) or None.',
                    'starter_code': 'def parsuj_ip_a_port(adresa):\n    pass\n',
                    'solution_code': 'def parsuj_ip_a_port(adresa):\n    if ":" not in adresa:\n        return None\n    ip, port_str = adresa.rsplit(":", 1)\n    try:\n        return (ip, int(port_str))\n    except ValueError:\n        return None\n',
                    'explanation_sk': 'Rozdelenie reťazca cez rsplit(":", 1) a konverzia portu na int.',
                    'explanation_en': 'String split extracting IP string and integer socket port.',
                    'hint_sk': 'if ":" not in adresa: return None; ip, p = adresa.rsplit(":", 1); return (ip, int(p))',
                    'hint_en': 'Use rsplit(":", 1) and int().',
                    'hint_cost_doros': 5,
                    'difficulty': 'EASY',
                    'xp_reward': 25,
                    'doros_reward': 10,
                    'test_cases': [
                        {'input_data': 'parsuj_ip_a_port("10.0.0.1:443")', 'expected_output': '("10.0.0.1", 443)', 'test_code': 'assert parsuj_ip_a_port("10.0.0.1:443") == ("10.0.0.1", 443)', 'is_hidden': False},
                        {'input_data': 'parsuj_ip_a_port("localhost")', 'expected_output': 'None', 'test_code': 'assert parsuj_ip_a_port("localhost") is None', 'is_hidden': False},
                        {'input_data': 'parsuj_ip_a_port("192.168.0.1:80")', 'expected_output': '("192.168.0.1", 80)', 'test_code': 'assert parsuj_ip_a_port("192.168.0.1:80") == ("192.168.0.1", 80)', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Úloha 2 (Stredná): Detekcia brute-force neúspešných pokusov',
                    'title_en': 'Exercise 2 (Medium): Detect Brute-Force Logins',
                    'instructions_sk': 'Napíš funkciu `detekuj_bruteforce(logy, limit=3)`: `logy` je zoznam slovníkov `[{"ip": "1.2.3.4", "uspech": False}, ...]`. Funkcia vráti zoznam unikátnych IP adries (abecedne zoradený), ktoré majú počet neúspešných pokusov (`uspech == False`) väčší alebo rovný číslu `limit`.',
                    'instructions_en': 'Write `detekuj_bruteforce(logy, limit=3)` returning sorted list of malicious IPs with >= limit failures.',
                    'starter_code': 'def detekuj_bruteforce(logy, limit=3):\n    pass\n',
                    'solution_code': 'def detekuj_bruteforce(logy, limit=3):\n    pocitadla = {}\n    for entry in logy:\n        if not entry.get("uspech", True):\n            ip = entry.get("ip")\n            if ip:\n                pocitadla[ip] = pocitadla.get(ip, 0) + 1\n    utocnici = [ip for ip, cnt in pocitadla.items() if cnt >= limit]\n    return sorted(utocnici)\n',
                    'explanation_sk': 'Frekvenčná analýza neúspešných udalostí a zoradenie výsledkov.',
                    'explanation_en': 'Frequency counter mapping IP failures against threshold.',
                    'hint_sk': 'Ak not entry["uspech"]: pocitadla[ip] = pocitadla.get(ip, 0) + 1. Na záver sorted().',
                    'hint_en': 'Count failures per IP and return sorted keys exceeding limit.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'detekuj_bruteforce([{"ip": "1.1.1.1", "uspech": False}, {"ip": "1.1.1.1", "uspech": False}, {"ip": "1.1.1.1", "uspech": False}, {"ip": "2.2.2.2", "uspech": False}], limit=3)', 'expected_output': '["1.1.1.1"]', 'test_code': 'assert detekuj_bruteforce([{"ip": "1.1.1.1", "uspech": False}, {"ip": "1.1.1.1", "uspech": False}, {"ip": "1.1.1.1", "uspech": False}, {"ip": "2.2.2.2", "uspech": False}], limit=3) == ["1.1.1.1"]', 'is_hidden': False},
                        {'input_data': 'detekuj_bruteforce([{"ip": "3.3.3.3", "uspech": True}], limit=1)', 'expected_output': '[]', 'test_code': 'assert detekuj_bruteforce([{"ip": "3.3.3.3", "uspech": True}], limit=1) == []', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Úloha 3 (Boss Výzva): Komplexná trieda IncidentManager',
                    'title_en': 'Exercise 3 (Boss Challenge): IncidentManager Class',
                    'instructions_sk': (
                        "Vytvor triedu `IncidentManager`:\n"
                        "1. `__init__(self)`: `self.blacklist = set()` a `self.incidenty = []`.\n"
                        "2. `zablokuj_ip(self, ip)`: pridá IP adresu do množiny blacklistu.\n"
                        "3. `je_zablokovana(self, ip)`: vráti `True`, ak sa IP nachádza v blackliste, inak `False`.\n"
                        "4. `zaznamenaj(self, ip, sprava)`: ak je IP zablokovaná, ignoruje záznam a vráti `False`. Inak pridá slovník `{\"ip\": ip, \"sprava\": sprava}` do zoznamu incidentov a vráti `True`.\n"
                        "5. `pocet_incidentov(self)`: vráti dĺžku zoznamu zaznamenaných incidentov."
                    ),
                    'instructions_en': 'Implement class `IncidentManager` managing blacklisted IP set and recorded incidents.',
                    'starter_code': 'class IncidentManager:\n    pass\n',
                    'solution_code': 'class IncidentManager:\n    def __init__(self):\n        self.blacklist = set()\n        self.incidenty = []\n    def zablokuj_ip(self, ip):\n        self.blacklist.add(ip)\n    def je_zablokovana(self, ip):\n        return ip in self.blacklist\n    def zaznamenaj(self, ip, sprava):\n        if self.je_zablokovana(ip):\n            return False\n        self.incidenty.append({"ip": ip, "sprava": sprava})\n        return True\n    def pocet_incidentov(self):\n        return len(self.incidenty)\n',
                    'explanation_sk': 'Správa množiny set() pre O(1) blacklistovanie a ukladanie incidentov.',
                    'explanation_en': 'Set membership checks combined with incident logging list.',
                    'hint_sk': 'Použi self.blacklist.add(ip) a self.blacklist obsahuje ip cez in.',
                    'hint_en': 'Use set.add and in operator.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 80,
                    'doros_reward': 40,
                    'test_cases': [
                        {'input_data': 'im = IncidentManager(); im.zablokuj_ip("1.2.3.4"); im.je_zablokovana("1.2.3.4")', 'expected_output': 'True', 'test_code': 'im = IncidentManager()\nim.zablokuj_ip("1.2.3.4")\nassert im.je_zablokovana("1.2.3.4") is True', 'is_hidden': False},
                        {'input_data': 'im = IncidentManager(); im.zablokuj_ip("1.2.3.4"); im.zaznamenaj("1.2.3.4", "Test")', 'expected_output': 'False', 'test_code': 'im = IncidentManager()\nim.zablokuj_ip("1.2.3.4")\nassert im.zaznamenaj("1.2.3.4", "Test") is False', 'is_hidden': False},
                        {'input_data': 'im = IncidentManager(); im.zaznamenaj("5.5.5.5", "Alert"); im.pocet_incidentov()', 'expected_output': '1', 'test_code': 'im = IncidentManager()\nassert im.zaznamenaj("5.5.5.5", "Alert") is True\nassert im.pocet_incidentov() == 1', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Projekt 4: Transakčný bankový ledger s auditom a rollbackom',
            'title_en': 'Project 4: Bank Transaction Ledger & Audit Trail',
            'summary_sk': 'Nemenný auditný záznam, história transakcií, detekcia neoprávnených pohybov a rollback.',
            'summary_en': 'Immutable audit ledgers, double-entry tracking, overdraft guards, and state replay.',
            'estimated_minutes': 75,
            'xp_reward': 60,
            'is_published': True,
            'content_sk': """### 18.4 Projekt: Auditovateľný bankový ledger

Finančné inštitúcie nikdy nemenia zostatok prepísaním jedného čísla v pamäti. Každý pohyb musí byť zaznamenaný ako **nemenná transakcia (Append-Only Ledger)** s typom operácie a sumou.

#### 1. Špecifikácia rozhrania bankového ledgeru

| Metóda | Vstupné parametre | Výnimky | Účel |
| :--- | :--- | :--- | :--- |
| `BankovyLedger(ucet_id)` | `str` | - | Vytvorí ledger pre zadaný účet |
| `zaznamenaj(typ, suma)` | `'VKLAD'` / `'VYBER'`, `int` | `ValueError` | Validuje zostatok a zapíše transakciu |
| `sumar_typov()` | žiadne | - | Vráti slovník `{"VKLAD": X, "VYBER": Y}` |
| `pocet_operacii()` | žiadne | - | Vráti celkový počet realizovaných transakcií |

#### 2. Kódový vzor: Append-Only Transakcie
```python
class BankovyLedger:
    def __init__(self, ucet_id: str):
        self.ucet_id = ucet_id
        self.transakcie = []
        self.zostatok = 0

    def vklad(self, suma: int) -> int:
        if suma <= 0:
            raise ValueError("Suma vkladu musí byť kladná")
        self.transakcie.append({"typ": "VKLAD", "suma": suma})
        self.zostatok += suma
        return self.zostatok
```

> **Častá chyba v praxi:**
> Dovolanie záporného zostatku (overdraft) bez explicitného povolenia debetu. Pri výbere vždy skontroluj `if self.zostatok < suma: raise ValueError("Nedostatočný zostatok")`!

#### 3. Zhrnutie
- Princíp append-only logu zabezpečuje auditovateľnosť celej histórie účtu.
- Použitie výnimiek `ValueError` pri porušení obchodných pravidiel.
- Agregácia súhrnov cez generátory s filtrovaním typu transakcie.
""",
            'content_en': """### 18.4 Project: Immutable Audit Ledger

Financial engines track every debit and credit as immutable transaction audit entries with overdraft protection.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo moderné finančné a databázové systémy používajú transakčný žurnál (Ledger)?',
                    'question_en': 'Why do enterprise financial engines maintain an append-only transaction ledger?',
                    'option_a_sk': 'Zabezpečuje 100% auditovateľnosť, sledovateľnosť histórie a prevenciu podvodov',
                    'option_a_en': 'Provides full auditability, historical traceability, and fraud resistance',
                    'option_b_sk': 'Šetrí miesto na disku',
                    'option_b_en': 'Reduces disk footprint',
                    'option_c_sk': 'Zjednodušuje CSS štýly',
                    'option_c_en': 'Simplifies CSS',
                    'option_d_sk': 'Zabraňuje pripojeniu k internetu',
                    'option_d_en': 'Blocks internet connection',
                    'correct_option': 'A',
                    'explanation_sk': 'Append-only ledger garantuje, že žiadnu minulosť nemožno zmazať bez stopy.',
                    'explanation_en': 'Append-only logs guarantee verifiable immutability and compliance.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Úloha 1 (Ľahká): Validácia kódu krajiny v IBAN',
                    'title_en': 'Exercise 1 (Easy): Validate IBAN Country Prefix',
                    'instructions_sk': 'Napíš funkciu `validuj_iban_kod(iban)`: vráti `True`, ak reťazec `iban` začína dvojicou veľkých písmen reprezentujúcich kód krajiny (napr. `"SK"`, `"CZ"`, `"DE"`) a má celkovú dĺžku aspoň 15 znakov. Inak vráti `False`.',
                    'instructions_en': 'Write `validuj_iban_kod(iban)` returning True if IBAN starts with 2 uppercase letters and is at least 15 chars long.',
                    'starter_code': 'def validuj_iban_kod(iban):\n    pass\n',
                    'solution_code': 'def validuj_iban_kod(iban):\n    if not isinstance(iban, str) or len(iban) < 15:\n        return False\n    prefix = iban[:2]\n    return prefix.isalpha() and prefix.isupper()\n',
                    'explanation_sk': 'Kontrola dĺžky a overenie dvoch veľkých písmen na začiatku.',
                    'explanation_en': 'Length check and uppercase prefix validation.',
                    'hint_sk': 'len(iban) >= 15 and iban[:2].isalpha() and iban[:2].isupper()',
                    'hint_en': 'Check length >= 15 and isupper().',
                    'hint_cost_doros': 5,
                    'difficulty': 'EASY',
                    'xp_reward': 25,
                    'doros_reward': 10,
                    'test_cases': [
                        {'input_data': 'validuj_iban_kod("SK8902000000001234567890")', 'expected_output': 'True', 'test_code': 'assert validuj_iban_kod("SK8902000000001234567890") is True', 'is_hidden': False},
                        {'input_data': 'validuj_iban_kod("sk123456789012345")', 'expected_output': 'False', 'test_code': 'assert validuj_iban_kod("sk123456789012345") is False', 'is_hidden': False},
                        {'input_data': 'validuj_iban_kod("SK123")', 'expected_output': 'False', 'test_code': 'assert validuj_iban_kod("SK123") is False', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Úloha 2 (Stredná): Výpočet zloženého úročenia',
                    'title_en': 'Exercise 2 (Medium): Compound Interest Calculator',
                    'instructions_sk': 'Napíš funkciu `vypocitaj_urok(istina, rocna_sadzba, roky)`: vypočíta konečnú sumu pri ročnom zloženom úročení podľa vzorca $K = istina \\times (1 + \\frac{rocna\\_sadzba}{100})^{roky}$. Vráti hodnotu zaokrúhlenú na 2 desatinné miesta.',
                    'instructions_en': 'Write `vypocitaj_urok(istina, rocna_sadzba, roky)` calculating compound interest.',
                    'starter_code': 'def vypocitaj_urok(istina, rocna_sadzba, roky):\n    pass\n',
                    'solution_code': 'def vypocitaj_urok(istina, rocna_sadzba, roky):\n    konecna = istina * ((1 + rocna_sadzba / 100.0) ** roky)\n    return round(konecna, 2)\n',
                    'explanation_sk': 'Finančný výpočet zloženého úročenia pomocou mocniny **.',
                    'explanation_en': 'Compound interest exponential power calculation.',
                    'hint_sk': 'istina * ((1 + rocna_sadzba / 100) ** roky)',
                    'hint_en': 'Use ** exponent operator.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vypocitaj_urok(1000, 5, 2)', 'expected_output': '1102.5', 'test_code': 'assert vypocitaj_urok(1000, 5, 2) == 1102.5', 'is_hidden': False},
                        {'input_data': 'vypocitaj_urok(500, 10, 1)', 'expected_output': '550.0', 'test_code': 'assert vypocitaj_urok(500, 10, 1) == 550.0', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Úloha 3 (Boss Výzva): Bankový ledger s históriou a kontrolou solvency',
                    'title_en': 'Exercise 3 (Boss Challenge): Bank Ledger System',
                    'instructions_sk': (
                        "Vytvor triedu `BankovyLedger`:\n"
                        "1. `__init__(self, ucet_id)`: nastaví `self.ucet_id`, zoznam `self.transakcie = []` a `self.zostatok = 0`.\n"
                        "2. `zaznamenaj(self, typ, suma)`: `typ` je `'VKLAD'` alebo `'VYBER'`. Pri `'VYBER'` skontroluj, či je na účte dostatok peňazí (ak nie, vyvolaj `ValueError(\"Nedostatočný zostatok\")`). Pridá slovník `{\"typ\": typ, \"suma\": suma}` do zoznamu a aktualizuje `zostatok`.\n"
                        "3. `pocet_operacii(self)`: vráti celkový počet úspešných transakcií.\n"
                        "4. `sumar_typov(self)`: vráti slovník `{\"VKLAD\": celkovo_vklady, \"VYBER\": celkovo_vybery}`."
                    ),
                    'instructions_en': 'Implement class `BankovyLedger` recording deposits/withdrawals, enforcing non-negative balances, and aggregating ledger summaries.',
                    'starter_code': 'class BankovyLedger:\n    pass\n',
                    'solution_code': 'class BankovyLedger:\n    def __init__(self, ucet_id):\n        self.ucet_id = ucet_id\n        self.transakcie = []\n        self.zostatok = 0\n    def zaznamenaj(self, typ, suma):\n        if suma <= 0:\n            raise ValueError("Suma musí byť kladná")\n        if typ == "VYBER":\n            if self.zostatok < suma:\n                raise ValueError("Nedostatočný zostatok")\n            self.zostatok -= suma\n        elif typ == "VKLAD":\n            self.zostatok += suma\n        else:\n            raise ValueError("Neznámy typ transakcie")\n        self.transakcie.append({"typ": typ, "suma": suma})\n        return self.zostatok\n    def pocet_operacii(self):\n        return len(self.transakcie)\n    def sumar_typov(self):\n        vklady = sum(t["suma"] for t in self.transakcie if t["typ"] == "VKLAD")\n        vybery = sum(t["suma"] for t in self.transakcie if t["typ"] == "VYBER")\n        return {"VKLAD": vklady, "VYBER": vybery}\n',
                    'explanation_sk': 'Transakčný ledger s kontrolou solvency a súhrnnou bilanciou.',
                    'explanation_en': 'Append-only ledger validating non-negative balances and computing category totals.',
                    'hint_sk': 'if typ == "VYBER" and self.zostatok < suma: raise ValueError("...").',
                    'hint_en': 'Validate balance before decrementing, append audit record to list.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 80,
                    'doros_reward': 40,
                    'test_cases': [
                        {'input_data': 'b = BankovyLedger("SK-01"); b.zaznamenaj("VKLAD", 100); b.zaznamenaj("VYBER", 30); b.zostatok', 'expected_output': '70', 'test_code': 'b = BankovyLedger("SK-01")\nb.zaznamenaj("VKLAD", 100)\nb.zaznamenaj("VYBER", 30)\nassert b.zostatok == 70', 'is_hidden': False},
                        {'input_data': 'b = BankovyLedger("SK-02"); b.zaznamenaj("VYBER", 50)', 'expected_output': 'ValueError', 'test_code': 'b = BankovyLedger("SK-02")\ntry:\n    b.zaznamenaj("VYBER", 50)\n    assert False, "Malo vyvolať ValueError"\nexcept ValueError:\n    pass', 'is_hidden': False},
                        {'input_data': 'b = BankovyLedger("SK-03"); b.zaznamenaj("VKLAD", 200); b.sumar_typov()', 'expected_output': '{"VKLAD": 200, "VYBER": 0}', 'test_code': 'b = BankovyLedger("SK-03")\nb.zaznamenaj("VKLAD", 200)\nassert b.sumar_typov() == {"VKLAD": 200, "VYBER": 0}', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Záverečná certifikačná skúška: Codoro Python Master Developer',
            'title_en': 'Final Certification Exam: Codoro Python Master Developer',
            'summary_sk': 'Záverečný komplexný test pokrývajúci celé kurikulum (všetkých 18 modulov).',
            'summary_en': 'Comprehensive capstone exam synthesizing all 18 curriculum modules.',
            'estimated_minutes': 90,
            'xp_reward': 100,
            'is_published': True,
            'content_sk': """### 18.5 Záverečná certifikačná skúška Codoro

Gratulujeme k dosiahnutiu záverečnej lekcie vzdelávacej platformy Codoro! Absolvoval si 18 komplexných modulov moderného Pythonu pokrývajúcich 5 kariérnych ciest:
1. **Základy a logika:** algoritmizácia, dátové typy, výrazy, podmienky, cykly
2. **Funkcie a dátové štruktúry:** funkcie, lambda, rekurzia, zoznamy, n-tice, slovníky, množiny, výnimky a súbory
3. **OOP a softvérové inžinierstvo:** triedy, objekty, dunder metódy, dedičnosť, polymorfizmus, dataclasses
4. **Algoritmy, dáta a bezpečnosť:** Big-O, binárne vyhľadávanie, quicksort, regulárne výrazy, SQL v Pythone, REST API a JSON, automatizované testovanie (TDD)
5. **Záverečné projekty a certifikácia:** kryptografia, pokročilé priemyselné zadania a capstone softvérové enginy

#### Prehľad záverečných kritérií
Po úspešnom vyriešení záverečnej skúšky sa v tvojom študentskom profile sprístupní oficiálny certifikát **Codoro Certified Python Developer** pripravený k tlači a overeniu!

> **Častá chyba v praxi a na technických pohovoroch:**
> Podcenenie hraničných prípadov (Edge Cases): prázdny vstupný zoznam, nesprávne dátové typy, delenie nulou. Skutočný softvérový inžinier navrhuje kód defenzívne a odolný voči chybám používateľa!

#### Zhrnutie
- Syntéza všetkých konceptov programovacieho jazyka Python.
- Pripravenosť na samostatný profesionálny vývoj a inžiniersku prax.
- Získanie certifikátu s unikátnym overovacím ID.
""",
            'content_en': """### 18.5 Final Capstone Certification

Congratulations on completing all 18 modules of the Codoro Python Developer curriculum!
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý princíp softvérového návrhu odporúča, aby funkcie a triedy mali iba jednu dobre definovanú zodpovednosť?',
                    'question_en': 'Which software design principle states that a function or class should do one thing well?',
                    'option_a_sk': 'Single Responsibility Principle (SRP)',
                    'option_a_en': 'Single Responsibility Principle (SRP)',
                    'option_b_sk': 'Maximum Speed Principle',
                    'option_b_en': 'Maximum Speed Principle',
                    'option_c_sk': 'Global State Rule',
                    'option_c_en': 'Global State Rule',
                    'option_d_sk': 'Big-O Minimizer',
                    'option_d_en': 'Big-O Minimizer',
                    'correct_option': 'A',
                    'explanation_sk': 'Princíp jednej zodpovednosti (SRP zo SOLID) je základom modulárneho a čistého kódu.',
                    'explanation_en': 'Single Responsibility Principle dictates focused, modular components.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Úloha 1 (Ľahká): Vyhodnotenie jednej otázky testu',
                    'title_en': 'Exercise 1 (Easy): Evaluate Single Quiz Question',
                    'instructions_sk': 'Napíš funkciu `vyhodnot_otazku(odpoved, spravna)`: porovná reťazce bez ohľadu na veľkosť písmen a biele znaky po stranách (`strip().upper()`). Vráti `True`, ak sa zhodujú, inak `False`.',
                    'instructions_en': 'Write `vyhodnot_otazku(odpoved, spravna)` comparing strings case-insensitively and trimmed.',
                    'starter_code': 'def vyhodnot_otazku(odpoved, spravna):\n    pass\n',
                    'solution_code': 'def vyhodnot_otazku(odpoved, spravna):\n    if not isinstance(odpoved, str) or not isinstance(spravna, str):\n        return False\n    return odpoved.strip().upper() == spravna.strip().upper()\n',
                    'explanation_sk': 'Normalizácia reťazcov pomocou strip() a upper() pred porovnaním.',
                    'explanation_en': 'Normalized string comparison using strip and upper.',
                    'hint_sk': 'odpoved.strip().upper() == spravna.strip().upper()',
                    'hint_en': 'Normalize using strip() and upper().',
                    'hint_cost_doros': 5,
                    'difficulty': 'EASY',
                    'xp_reward': 25,
                    'doros_reward': 10,
                    'test_cases': [
                        {'input_data': 'vyhodnot_otazku(" a ", "A")', 'expected_output': 'True', 'test_code': 'assert vyhodnot_otazku(" a ", "A") is True', 'is_hidden': False},
                        {'input_data': 'vyhodnot_otazku("b", "C")', 'expected_output': 'False', 'test_code': 'assert vyhodnot_otazku("b", "C") is False', 'is_hidden': False},
                        {'input_data': 'vyhodnot_otazku("Python ", "PYTHON")', 'expected_output': 'True', 'test_code': 'assert vyhodnot_otazku("Python ", "PYTHON") is True', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Úloha 2 (Stredná): Analýza úspešnosti triedy v teste',
                    'title_en': 'Exercise 2 (Medium): Class Test Success Analytics',
                    'instructions_sk': 'Napíš funkciu `analyzuj_uspesnost(vysledky)`: parameter je zoznam percentuálnych výsledkov študentov `[int alebo float]`. Funkcia vráti slovník `{"priemer": float, "uspesnych": int, "neuspesnych": int}`, kde úspešný študent má skóre $\\ge 50.0$. Ak je zoznam prázdny, vráti `{"priemer": 0.0, "uspesnych": 0, "neuspesnych": 0}`. Priemer zaokrúhli na 2 desatinné miesta.',
                    'instructions_en': 'Write `analyzuj_uspesnost(vysledky)` returning summary dict of average, passing (>=50), and failing count.',
                    'starter_code': 'def analyzuj_uspesnost(vysledky):\n    pass\n',
                    'solution_code': 'def analyzuj_uspesnost(vysledky):\n    if not vysledky:\n        return {"priemer": 0.0, "uspesnych": 0, "neuspesnych": 0}\n    uspesni = sum(1 for v in vysledky if v >= 50.0)\n    neuspesni = len(vysledky) - uspesni\n    priemer = round(sum(vysledky) / len(vysledky), 2)\n    return {"priemer": priemer, "uspesnych": uspesni, "neuspesnych": neuspesni}\n',
                    'explanation_sk': 'Štatistické rozdelenie a výpočet priemeru triedy.',
                    'explanation_en': 'Class analytics counting passing and failing students and computing mean.',
                    'hint_sk': 'uspesni = sum(1 for v in vysledky if v >= 50.0); priemer = round(sum(vysledky)/len(vysledky), 2)',
                    'hint_en': 'Aggregate passing students with generator count.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'analyzuj_uspesnost([80, 40, 90, 30])', 'expected_output': '{"priemer": 60.0, "uspesnych": 2, "neuspesnych": 2}', 'test_code': 'assert analyzuj_uspesnost([80, 40, 90, 30]) == {"priemer": 60.0, "uspesnych": 2, "neuspesnych": 2}', 'is_hidden': False},
                        {'input_data': 'analyzuj_uspesnost([])', 'expected_output': '{"priemer": 0.0, "uspesnych": 0, "neuspesnych": 0}', 'test_code': 'assert analyzuj_uspesnost([]) == {"priemer": 0.0, "uspesnych": 0, "neuspesnych": 0}', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Úloha 3 (Boss Skúška): Certifikačný evaluátor záverečného testu',
                    'title_en': 'Exercise 3 (Boss Exam): Certification Evaluator Engine',
                    'instructions_sk': (
                        "Záverečná úloha pre certifikát: Napíš funkciu `vyhodnot_skusku(odpovede, kluc_spravnych)`:\n"
                        "- `odpovede` je slovník `{\"uloha_1\": \"A\", \"uloha_2\": \"B\", ...}`.\n"
                        "- `kluc_spravnych` je slovník správnych odpovedí rovnakého formátu.\n"
                        "Funkcia spočíta úspešnosť v percentách (správne / celkový počet kľúčov v kľúči * 100).\n"
                        "Vráti trojicu `(pocet_spravnych, celkovo_otazok, zaokruhlene_percenta)`.\n"
                        "Napr. pre 3 správne zo 4 vráti `(3, 4, 75.0)`. Pre prázdny kľúč správnych odpovedí vráti `(0, 0, 0.0)`."
                    ),
                    'instructions_en': 'Write `vyhodnot_skusku(odpovede, kluc_spravnych)` returning tuple (correct_count, total_count, percentage).',
                    'starter_code': 'def vyhodnot_skusku(odpovede, kluc_spravnych):\n    pass\n',
                    'solution_code': 'def vyhodnot_skusku(odpovede, kluc_spravnych):\n    if not kluc_spravnych:\n        return (0, 0, 0.0)\n    spravne = 0\n    celkovo = len(kluc_spravnych)\n    for otazka, odpoved in kluc_spravnych.items():\n        if odpovede.get(otazka) == odpoved:\n            spravne += 1\n    percenta = round((spravne / celkovo) * 100, 2)\n    return (spravne, celkovo, percenta)\n',
                    'explanation_sk': 'Komplexné porovnanie slovníkových kľúčov a percentuálna štatistika úspešnosti.',
                    'explanation_en': 'Dictionary evaluation comparing answers against answer key with percentage calculation.',
                    'hint_sk': 'for k, v in kluc_spravnych.items(): if odpovede.get(k) == v: spravne += 1.',
                    'hint_en': 'Compare answers against answer key dictionary and round percentage.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 100,
                    'doros_reward': 50,
                    'test_cases': [
                        {'input_data': 'vyhodnot_skusku({"q1": "A", "q2": "B", "q3": "C"}, {"q1": "A", "q2": "B", "q3": "D"})', 'expected_output': '(2, 3, 66.67)', 'test_code': 'assert vyhodnot_skusku({"q1": "A", "q2": "B", "q3": "C"}, {"q1": "A", "q2": "B", "q3": "D"}) == (2, 3, 66.67)', 'is_hidden': False},
                        {'input_data': 'vyhodnot_skusku({"q1": "A"}, {"q1": "A"})', 'expected_output': '(1, 1, 100.0)', 'test_code': 'assert vyhodnot_skusku({"q1": "A"}, {"q1": "A"}) == (1, 1, 100.0)', 'is_hidden': False},
                        {'input_data': 'vyhodnot_skusku({}, {"q1": "A", "q2": "B"})', 'expected_output': '(0, 2, 0.0)', 'test_code': 'assert vyhodnot_skusku({}, {"q1": "A", "q2": "B"}) == (0, 2, 0.0)', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
