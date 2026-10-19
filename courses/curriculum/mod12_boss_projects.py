"""
MODUL 12: Praktické projekty a algoritmické Boss výzvy
Odhadovaný rozsah: 12 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU
"""

MODULE_DATA = {
    'order': 12,
    'title_sk': 'Praktické projekty a algoritmické Boss výzvy',
    'title_en': 'Real-World Projects & Algorithmic Boss Challenges',
    'description_sk': 'Zavŕšenie celého štúdia Codoro Python Developer: komplexné reálne mini-systémy integrujúce OOP, dátové štruktúry, ošetrenie chýb a algoritmické myslenie do portfólia.',
    'description_en': 'The ultimate capstone of Codoro Python Developer curriculum: comprehensive real-world mini-engines combining OOP, data structures, exception safety, and algorithmic problem-solving.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'trophy',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Projekt 1: Elektronická žiacka knižka a analyzátor známok',
            'title_en': 'Project 1: Electronic Gradebook & Class Analytics',
            'summary_sk': 'Štatistický analyzátor triedy, vážené priemery, vyznamenania a generovanie reportu.',
            'summary_en': 'Academic gradebook analytics, weighted grade GPA, honors classification, and reporting.',
            'estimated_minutes': 60,
            'xp_reward': 50,
            'is_published': True,
            'content_sk': """### 12.1 Projekt: Školský analyzátor známok

V tomto projekte vytvoríš engine pre triedneho učiteľa, ktorý zo záznamov známok študentov vypočíta priemer celej triedy, nájde najlepšieho študenta a vygeneruje zoznam žiakov s vyznamenaním (priemer $\\le 1.50$).
""",
            'content_en': """### 12.1 Project: School Gradebook Analytics Engine

Build an electronic gradebook engine computing class averages, identifying valedictorian, and filtering students with honors.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú výhodu má reprezentácia známok študenta pomocou slovníka `{"predmet": [znamky]}` namiesto plochého zoznamu?',
                    'question_en': 'What advantage does structuring grades as `{"subject": [grades]}` offer over flat lists?',
                    'option_a_sk': 'Umožňuje separátny výpočet priemerov pre jednotlivé predmety v O(1) vyhľadávaní', 'option_a_en': 'Enables per-subject average calculations with O(1) key indexing',
                    'option_b_sk': 'Šetrí pamäť CPU', 'option_b_en': 'Saves CPU registers',
                    'option_c_sk': 'Eliminuje potrebu funkcií', 'option_c_en': 'Eliminates functions',
                    'option_d_sk': 'Automaticky ukladá do cloudu', 'option_d_en': 'Cloud sync',
                    'correct_option': 'A',
                    'explanation_sk': 'Slovníková štruktúra logicky oddeľuje známky podľa predmetu a umožňuje cielenú analytiku.',
                    'explanation_en': 'Structured mapping separates domain namespaces for modular analytics.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Boss Výzva: Engine žiackej knižky',
                    'title_en': 'Boss Challenge: Gradebook Engine',
                    'instructions_sk': (
                        "Vytvor triedu `ZiackaKnizka`:\n"
                        "1. `__init__(self)`: inicializuje prázdny slovník `self.znamky = {}` (kľúč = predmet, hodnota = zoznam známok `[int]`).\n"
                        "2. `pridaj_znamku(self, predmet, znamka)`: ak je známka v rozsahu 1 až 5, pridá ju k predmetu a vráti `True`. Inak vráti `False`.\n"
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
            'title_sk': 'Projekt 2: E-shop nákupný košík s kupónmi a skladom',
            'title_en': 'Project 2: E-Commerce Cart Engine with Coupons',
            'summary_sk': 'Objektový model e-shopu, riadenie zásob, uplatnenie promo kódu a DPH.',
            'summary_en': 'E-commerce cart domain modeling, stock inventory locks, discount coupons, and tax calculation.',
            'estimated_minutes': 60,
            'xp_reward': 50,
            'is_published': True,
            'content_sk': """### 12.2 Projekt: E-shop Engine a zľavové kupóny

V tomto projekte navrhneš jadro internetového obchodu, ktoré počíta medzisúčet položiek, aplikuje percentuálny alebo fixný promo kupón a garantuje, že cena nikdy neklesne pod nulu.
""",
            'content_en': """### 12.2 Project: E-Commerce Cart Engine

Build checkout engine calculating subtotal, applying percentage coupons, and computing tax.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo je dôležité počítať peňažné sumy s desatinným zaokrúhlením až na samom konci výpočtového reťazca?',
                    'question_en': 'Why should rounding occur at the end of financial calculations?',
                    'option_a_sk': 'Aby sa predišlo kumulácii chýb spôsobených predčasným zaokrúhľovaním medzivýsledkov', 'option_a_en': 'To prevent error accumulation from intermediate truncations',
                    'option_b_sk': 'Pretože round() je pomalá funkcia', 'option_b_en': 'round is slow',
                    'option_c_sk': 'Pretože to vyžaduje formát JSON', 'option_c_en': 'JSON requirement',
                    'option_d_sk': 'Nemá to žiadny vplyv', 'option_d_en': 'No difference',
                    'correct_option': 'A',
                    'explanation_sk': 'Zaokrúhľovanie v každom kroku spôsobuje nepresnosti ("halierové chyby") v účtovníctve.',
                    'explanation_en': 'Premature rounding compounds numerical drift in financial calculations.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Boss Výzva: Nákupný košík s kupónom',
                    'title_en': 'Boss Challenge: Shopping Cart with Coupon',
                    'instructions_sk': (
                        "Vytvor triedu `Kosik`:\n"
                        "1. `__init__(self)`: `self.polozky = {}` (názov -> cena_za_kus, pocet_kusov).\n"
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
            'title_sk': 'Projekt 3: Textový kompresor RLE (Run-Length Encoding)',
            'title_en': 'Project 3: RLE Text Compression Engine',
            'summary_sk': 'Bezztrátová kompresia dát, kódovanie behov znakov (RLE kompresor a dekompresor).',
            'summary_en': 'Lossless data compression using Run-Length Encoding and inverse decompression.',
            'estimated_minutes': 60,
            'xp_reward': 50,
            'is_published': True,
            'content_sk': """### 12.3 Projekt: Kompresor dát Run-Length Encoding (RLE)

**Run-Length Encoding (RLE)** je klasický bezztrátový kompresný algoritmus. Ak sa rovnaký znak opakuje viackrát za sebou, zapíše sa ako počet výskytov nasledovaný daným znakom:

`"AAAAABBBCCDAA"` -> `"5A3B2C1D2A"`

Využíva sa v grafických formátoch (BMP, TIFF, faxový prenos).
""",
            'content_en': """### 12.3 Project: Run-Length Encoding (RLE)

Lossless compression replacing repeated consecutive runs with frequency counters.
""",
            'quizzes': [
                {
                    'question_sk': 'Pre aký typ dát je kompresia RLE najvhodnejšia?',
                    'question_en': 'For what type of data is RLE compression most effective?',
                    'option_a_sk': 'Pre dáta s dlhými súvislými blokmi rovnakých znakov či pixelov (napr. jednoduché schémy)', 'option_a_en': 'Data featuring long runs of repeated identical tokens',
                    'option_b_sk': 'Pre náhodný šum', 'option_b_en': 'Random noise',
                    'option_c_sk': 'Pre šifrované heslá', 'option_c_en': 'Encrypted ciphertext',
                    'option_d_sk': 'Pre audio nahrávky', 'option_d_en': 'Acoustic audio',
                    'correct_option': 'A',
                    'explanation_sk': 'RLE exceluje pri dlhých opakovaniach; pri náhodnom texte naopak dĺžku zdvojnásobí.',
                    'explanation_en': 'RLE minimizes storage when homogeneous runs exceed token metadata size.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Boss Výzva: RLE Kompresor a Dekompresor',
                    'title_en': 'Boss Challenge: RLE Encoder and Decoder',
                    'instructions_sk': (
                        "Napíš dve funkcie:\n"
                        "1. `rle_encode(text)`: zakóduje napr. `'AAAB'` na `'3A1B'`. Pre prázdny reťazec vráti `''`.\n"
                        "2. `rle_decode(kodovany)`: zrekonštruuje pôvodný reťazec napr. z `'3A1B'` na `'AAAB'` (predpokladaj jednociferné alebo viacdielne čísla, pre jednoduchosť formát [číslo][znak])."
                    ),
                    'instructions_en': 'Implement `rle_encode(text)` and `rle_decode(kodovany)`.',
                    'starter_code': 'def rle_encode(text):\n    pass\n\ndef rle_decode(kodovany):\n    pass\n',
                    'solution_code': 'def rle_encode(text):\n    if not text:\n        return ""\n    vysledok = []\n    pocet = 1\n    for i in range(1, len(text)):\n        if text[i] == text[i - 1]:\n            pocet += 1\n        else:\n            vysledok.append(f"{pocet}{text[i - 1]}")\n            pocet = 1\n    vysledok.append(f"{pocet}{text[-1]}")\n    return "".join(vysledok)\n\ndef rle_decode(kodovany):\n    if not kodovany:\n        return ""\n    vysledok = []\n    num_str = ""\n    for char in kodovany:\n        if char.isdigit():\n            num_str += char\n        else:\n            pocet = int(num_str)\n            vysledok.append(char * pocet)\n            num_str = ""\n    return "".join(vysledok)\n',
                    'explanation_sk': 'Klasická implementácia kódovania behov a spätného dekódovania.',
                    'explanation_en': 'Linear scan encoding runs and multi-digit decoding stream assembly.',
                    'hint_sk': 'Pri encode sleduj aktuálny znak a počítadlo. Pri decode akumuluj číslice do num_str kým nenarazíš na písmeno.',
                    'hint_en': 'Accumulate count for consecutive chars, parse multi-digit counts during decode.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 80,
                    'doros_reward': 40,
                    'test_cases': [
                        {'input_data': 'rle_encode("AAAAABBBCCDAA")', 'expected_output': '5A3B2C1D2A', 'test_code': 'assert rle_encode("AAAAABBBCCDAA") == "5A3B2C1D2A"', 'is_hidden': False},
                        {'input_data': 'rle_decode("5A3B2C1D2A")', 'expected_output': 'AAAAABBBCCDAA', 'test_code': 'assert rle_decode("5A3B2C1D2A") == "AAAAABBBCCDAA"', 'is_hidden': False},
                        {'input_data': 'rle_encode("")', 'expected_output': '', 'test_code': 'assert rle_encode("") == ""', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Projekt 4: Transakčný bankový ledger s auditom',
            'title_en': 'Project 4: Bank Ledger with Audit History',
            'summary_sk': 'Nemenný auditný záznam, história transakcií, detekcia neoprávnených pohybov a rollback.',
            'summary_en': 'Immutable audit ledgers, double-entry tracking, overdraft guards, and state replay.',
            'estimated_minutes': 60,
            'xp_reward': 50,
            'is_published': True,
            'content_sk': """### 12.4 Projekt: Auditovateľný bankový ledger

Finančné inštitúcie nikdy nemenia zostatok len prepísaním čísla. Každá zmena musí byť zaznamenaná ako **nemenná transakcia (Ledger Record)** s časovou pečiatkou, typom operácie a sumou.
""",
            'content_en': """### 12.4 Project: Immutable Audit Ledger

Financial engines track every debit and credit as immutable transaction audit entries.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo moderné finančné a databázové systémy používajú transakčný žurnál (Ledger)?',
                    'question_en': 'Why do enterprise financial engines maintain an append-only transaction ledger?',
                    'option_a_sk': 'Zabezpečuje 100% auditovateľnosť, sledovateľnosť histórie a prevenciu podvodov', 'option_a_en': 'Provides full auditability, historical traceability, and fraud resistance',
                    'option_b_sk': 'Šetrí miesto na disku', 'option_b_en': 'Reduces disk footprint',
                    'option_c_sk': 'Zjednodušuje CSS štýly', 'option_c_en': 'Simplifies CSS',
                    'option_d_sk': 'Zabraňuje pripojeniu k internetu', 'option_d_en': 'Blocks internet connection',
                    'correct_option': 'A',
                    'explanation_sk': 'Append-only ledger garantuje, že žiadnu minulosť nemožno zmazať bez stopy.',
                    'explanation_en': 'Append-only logs guarantee verifiable immutability and compliance.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Boss Výzva: Bankový ledger s históriou',
                    'title_en': 'Boss Challenge: Bank Ledger System',
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
            'summary_sk': 'Záverečný komplexný test pokrývajúci celé kurikulum (všetkých 12 modulov).',
            'summary_en': 'Comprehensive capstone exam synthesizing all 12 curriculum modules.',
            'estimated_minutes': 90,
            'xp_reward': 100,
            'is_published': True,
            'content_sk': """### 12.5 Záverečná certifikačná skúška Codoro

Gratulujeme k dosiahnutiu záverečnej lekcie! Prešiel si 12 modulmi moderného Pythonu:
1. Algoritmizácia a premenné
2. Operátory a reťazce
3. Rozhodovacia logika
4. Cykly a iterácie
5. Funkcie a rekurzia
6. Zoznamy a matice
7. Slovníky a množiny
8. Výnimky a prúdy
9. OOP základy a zapuzdrenie
10. Dedičnosť a polymorfizmus
11. Algoritmy a časová zložitosť
12. Komplexné softvérové projekty

Po úspešnom vyriešení záverečnej úlohy získaš oficiálny odznak **Codoro Python Developer** a odomkne sa generovanie certifikátu v tvojom profile!
""",
            'content_en': """### 12.5 Final Capstone Certification

Congratulations on completing all 12 modules of Codoro Python curriculum! Solve the final master challenge to claim your Python Developer Certification.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý princíp softvérového návrhu odporúča, aby funkcie a metódy robili iba jednu vec a robili ju poriadne?',
                    'question_en': 'Which software design principle states that a function or class should do one thing well?',
                    'option_a_sk': 'Single Responsibility Principle (SRP)', 'option_a_en': 'Single Responsibility Principle (SRP)',
                    'option_b_sk': 'Maximum Speed Principle', 'option_b_en': 'Maximum Speed Principle',
                    'option_c_sk': 'Global State Rule', 'option_c_en': 'Global State Rule',
                    'option_d_sk': 'Big-O Minimizer', 'option_d_en': 'Big-O Minimizer',
                    'correct_option': 'A',
                    'explanation_sk': 'Princíp jednej zodpovednosti (SRP zo SOLID) je základom čistého kódu.',
                    'explanation_en': 'Single Responsibility Principle dictates focused, modular components.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Záverečná Boss Skúška: Certifikačný evaluátor riešení',
                    'title_en': 'Final Boss Exam: Certification Solution Evaluator',
                    'instructions_sk': (
                        "Záverečná úloha pre certifikát: Napíš funkciu `vyhodnot_skusku(odpovede, kluc_spravnych)`:\n"
                        "- `odpovede` je slovník `{\"uloha_1\": \"A\", \"uloha_2\": \"B\", ...}`.\n"
                        "- `kluc_spravnych` je slovník správnych odpovedí rovnakého formátu.\n"
                        "Funkcia spočíta úspešnosť v percentách (správne / celkový počet kľúčov v kľúči * 100).\n"
                        "Vráti trojicu `(pocet_spravnych, celkovo_otazok, zaokruhlene_percenta)`.\n"
                        "Napr. pre 3 správne zo 4 vráti `(3, 4, 75.0)`."
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
