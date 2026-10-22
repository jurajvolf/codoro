"""
MODUL 17: Praktické priemyselné zadania a inžinierske algoritmy
Odhadovaný rozsah: 14 hodín | Náročnosť: INTERMEDIATE | Úroveň: FREE | Track: MATURITA_PREP
"""

MODULE_DATA = {
    'order': 17,
    'track': 'MATURITA_PREP',
    'title_sk': 'Praktické priemyselné zadania a algoritmy z praxe',
    'title_en': 'Real-World Practical Algorithmic Challenges',
    'description_sk': 'Reálne priemyselné a inžinierske výzvy pre odbor Informačno-mediálne technológie a Elektrotechniku: spracovanie fyzikálnych senzorických meraní, štatistika triedy, kolízny plánovač rozvrhov, bezstratová RLE kompresia a integrita sieťových paketov.',
    'description_en': 'Real industrial and engineering challenges tailored for IMT and Electrical Engineering: sensor processing, classroom grade analytics, schedule collision detection, lossless RLE data compression, and network packet checksums.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'INTERMEDIATE',
    'is_pro_only': False,
    'icon_name': 'mortarboard',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Spracovanie elektrotechnických meraní a filtrovanie šumu',
            'title_en': 'Electrical Engineering Measurements & Noise Filtering',
            'summary_sk': 'Ohmov zákon, elektrický výkon P = U·I, práca W = P·t a filtrácia odľahlých hodnôt.',
            'summary_en': 'Ohm\'s law, electric power P = U*I, energy W = P*t, and sensor outlier filtering.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 17.1 Výpočty v elektrotechnike a spracovanie meraní

V odbore elektrotechniky a IMT patrí spracovanie dát zo senzorov a mikrokontrolérov (ESP32, Arduino, Raspberry Pi) medzi základné praktické zručnosti.

#### Ohmov zákon
$$R = \\frac{U}{I}$$
Kde $U$ je napätie vo voltoch (V), $I$ je prúd v ampéroch (A) a $R$ je odpor v ohmoch ($\\Omega$).

#### Elektrický výkon a spotreba energie
$$P = U \\cdot I \\quad [\\text{W}]$$
$$W = P \\cdot t \\quad [\\text{J}] = \\frac{P \\cdot t}{3600 \\cdot 1000} \\quad [\\text{kWh}]$$

#### Filtrovanie šumu senzorov
Merania z reálnych senzorov obsahujú náhodné výkyvy a špičky (šum). Jednoduchým a efektívnym algoritmom je **kĺzavý priemer (Moving Average)** alebo vyradenie hodnôt, ktoré sa od priemerného trendu líšia o viac ako stanovená tolerancia.
""",
            'content_en': """### 17.1 Sensor Processing in Electrical Engineering

Apply Ohm's law, calculate electrical energy, and filter sensor spikes.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký elektrický výkon odoberá obvod pri napätí 230 V a prúde 2 A?',
                    'question_en': 'What electrical power is consumed at 230 V and 2 A?',
                    'option_a_sk': '460 W', 'option_a_en': '460 W',
                    'option_b_sk': '115 W', 'option_b_en': '115 W',
                    'option_c_sk': '232 W', 'option_c_en': '232 W',
                    'option_d_sk': '4600 W', 'option_d_en': '4600 W',
                    'correct_option': 'A',
                    'explanation_sk': 'P = U * I = 230 * 2 = 460 Wattov.',
                    'explanation_en': 'P = U * I = 230 * 2 = 460 W.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet elektrického odporu (Ohmov zákon)',
                    'title_en': 'Electrical Resistance (Ohm\'s Law)',
                    'instructions_sk': 'Napíš funkciu `vypocitaj_odpor(napatie_v, prud_a)`: vráti elektrický odpor v ohmoch zaokrúhlený na 2 desatinné miesta. Ak je prúd menší alebo rovný 0, vyvolá `ValueError("Prúd musí byť kladný")`.',
                    'instructions_en': 'Write function `vypocitaj_odpor(napatie_v, prud_a)` returning resistance rounded to 2 places or raising ValueError if current <= 0.',
                    'starter_code': 'def vypocitaj_odpor(napatie_v, prud_a):\n    # Vypočítaj odpor R = U / I\n    pass\n',
                    'solution_code': (
                        'def vypocitaj_odpor(napatie_v, prud_a):\n'
                        '    if prud_a <= 0:\n'
                        '        raise ValueError("Prúd musí byť kladný")\n'
                        '    return round(napatie_v / prud_a, 2)\n'
                    ),
                    'explanation_sk': 'Ošetrili sme kladnosť prúdu a vypočítali R = U / I.',
                    'explanation_en': 'Checked positive current and computed R = U / I.',
                    'hint_sk': 'Ak prud_a <= 0: raise ValueError(...) inak return round(napatie_v / prud_a, 2).',
                    'hint_en': 'Raise ValueError if current <= 0, else return round(U / I, 2).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vypocitaj_odpor(12.0, 0.5)', 'expected_output': '24.0', 'test_code': 'assert vypocitaj_odpor(12.0, 0.5) == 24.0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_odpor(230.0, 1.5)', 'expected_output': '153.33', 'test_code': 'assert vypocitaj_odpor(230.0, 1.5) == 153.33', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Výpočet výkonu a spotrebovanej energie v kWh',
                    'title_en': 'Power & Energy Consumption in kWh',
                    'instructions_sk': (
                        "Napíš funkciu `spotreba_energie(napatie_v, prud_a, cas_minuty)`:\n"
                        "Vypočíta:\n"
                        "- výkon `vykon_w = napatie * prud`,\n"
                        "- spotrebovanú energiu `kwh = (vykon_w * (cas_minuty / 60)) / 1000`.\n"
                        "Vráti slovník `{'vykon_w': float, 'energia_kwh': float}` zaokrúhlený na 3 desatinné miesta."
                    ),
                    'instructions_en': 'Write function `spotreba_energie(napatie_v, prud_a, cas_minuty)` returning dict of power in watts and energy in kWh.',
                    'starter_code': 'def spotreba_energie(napatie_v, prud_a, cas_minuty):\n    # Vypočítaj výkon a energiu v kWh\n    pass\n',
                    'solution_code': (
                        'def spotreba_energie(napatie_v, prud_a, cas_minuty):\n'
                        '    w = napatie_v * prud_a\n'
                        '    kwh = (w * (cas_minuty / 60.0)) / 1000.0\n'
                        '    return {"vykon_w": round(w, 3), "energia_kwh": round(kwh, 3)}\n'
                    ),
                    'explanation_sk': 'Vypočítali sme výkon vo Watoch a prepočítali na kilowatthodiny.',
                    'explanation_en': 'Computed watts and converted to kilowatt-hours.',
                    'hint_sk': 'kwh = (vykon_w * (cas_minuty / 60.0)) / 1000.0.',
                    'hint_en': 'Convert minutes to hours then divide by 1000.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'spotreba_energie(230, 10, 120)',
                            'expected_output': "{'vykon_w': 2300.0, 'energia_kwh': 4.6}",
                            'test_code': 'assert spotreba_energie(230, 10, 120) == {"vykon_w": 2300.0, "energia_kwh": 4.6}',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Filtrovanie špičiek a odľahlých hodnôt meraní',
                    'title_en': 'Sensor Noise & Outlier Filter',
                    'instructions_sk': (
                        "Napíš funkciu `filtruj_merania(zoznam_hodnot, max_odchylka=5.0)`:\n"
                        "1. Vypočíta priemernú hodnotu všetkých čísel v zozname.\n"
                        "2. Vyfiltruje iba tie hodnoty, ktorých absolútny rozdiel od priemeru je `<= max_odchylka` (`abs(x - priemer) <= max_odchylka`).\n"
                        "3. Vráti novú priemernú hodnotu zo zostávajúcich očistených hodnôt zaokrúhlenú na 2 desatinné miesta. Ak je zoznam prázdny, vráti `0.0`."
                    ),
                    'instructions_en': 'Write function `filtruj_merania(zoznam_hodnot, max_odchylka=5.0)` filtering values exceeding deviation from mean.',
                    'starter_code': 'def filtruj_merania(zoznam_hodnot, max_odchylka=5.0):\n    # Vyfiltruj odľahlé hodnoty a vráť nový priemer\n    pass\n',
                    'solution_code': (
                        'def filtruj_merania(zoznam_hodnot, max_odchylka=5.0):\n'
                        '    if not zoznam_hodnot:\n'
                        '        return 0.0\n'
                        '    priemer1 = sum(zoznam_hodnot) / len(zoznam_hodnot)\n'
                        '    ocistene = [x for x in zoznam_hodnot if abs(x - priemer1) <= max_odchylka]\n'
                        '    if not ocistene:\n'
                        '        return 0.0\n'
                        '    return round(sum(ocistene) / len(ocistene), 2)\n'
                    ),
                    'explanation_sk': 'Vypočítali sme priemer, vyselektovali hodnoty v tolerancii a prepočítali očistený priemer.',
                    'explanation_en': 'Calculated mean, pruned outlier anomalies, and recomputed clean mean.',
                    'hint_sk': 'abs(x - priemer) <= max_odchylka v list comprehension.',
                    'hint_en': 'Filter values within absolute deviation limit.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'filtruj_merania([10.0, 10.2, 9.8, 100.0, 10.1], max_odchylka=10.0)',
                            'expected_output': '10.025 -> 10.03',
                            'test_code': 'assert filtruj_merania([10.0, 10.2, 9.8, 100.0, 10.1], max_odchylka=10.0) == 10.03',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'filtruj_merania([])',
                            'expected_output': '0.0',
                            'test_code': 'assert filtruj_merania([]) == 0.0',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Štatistika triedy: vážený priemer a modus známok',
            'title_en': 'Class Analytics: Weighted Average & Grade Mode',
            'summary_sk': 'Vážený aritmetický priemer, štatistický modus (najčastejšia hodnota) a klasifikácia.',
            'summary_en': 'Weighted average calculations, statistical mode, and grade classification.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 17.2 Štatistické vyhodnotenie školskej triedy

Pri klasifikácii na strednej škole má každá písomka inú váhu (napr. polročná písomka váha 3, bleskovka váha 1).

#### Vážený priemer:
$$\\bar{x}_w = \\frac{\\sum_{i=1}^{n} (z_i \\cdot w_i)}{\\sum_{i=1}^{n} w_i}$$

#### Štatistický modus:
Hodnota, ktorá sa v súbore vyskytuje s najvyššou frekvenciou.
""",
            'content_en': """### 17.2 Classroom Grade Statistics

Calculate weighted GPA and statistical mode for grading reports.
""",
            'quizzes': [
                {
                    'question_sk': 'Ak študent dostal známku 1 s váhou 3 a známku 3 s váhou 1, aký je jeho vážený priemer?',
                    'question_en': 'Grade 1 with weight 3 and grade 3 with weight 1 gives what weighted average?',
                    'option_a_sk': '1.50', 'option_a_en': '1.50',
                    'option_b_sk': '2.00', 'option_b_en': '2.00',
                    'option_c_sk': '1.00', 'option_c_en': '1.00',
                    'option_d_sk': '2.50', 'option_d_en': '2.50',
                    'correct_option': 'A',
                    'explanation_sk': '(1 * 3 + 3 * 1) / (3 + 1) = 6 / 4 = 1.50.',
                    'explanation_en': '(1*3 + 3*1) / 4 = 1.50.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet váženého priemeru známok',
                    'title_en': 'Compute Weighted Grade Average',
                    'instructions_sk': 'Napíš funkciu `vazeny_priemer(znamky_vahy)`: prijme zoznam dvojíc `[(znamka, vaha), ...]`. Vráti vážený priemer zaokrúhlený na 2 desatinné miesta. Ak je zoznam prázdny alebo je celková váha 0, vráti `0.0`.',
                    'instructions_en': 'Write function `vazeny_priemer(znamky_vahy)` returning weighted average rounded to 2 places.',
                    'starter_code': 'def vazeny_priemer(znamky_vahy):\n    # Vypočítaj vážený priemer\n    pass\n',
                    'solution_code': (
                        'def vazeny_priemer(znamky_vahy):\n'
                        '    if not znamky_vahy:\n'
                        '        return 0.0\n'
                        '    citatel = sum(z * w for z, w in znamky_vahy)\n'
                        '    menovatel = sum(w for _, w in znamky_vahy)\n'
                        '    if menovatel == 0:\n'
                        '        return 0.0\n'
                        '    return round(citatel / menovatel, 2)\n'
                    ),
                    'explanation_sk': 'Spočítali sme vážený súčet a podelili celkovou váhou.',
                    'explanation_en': 'Summed weighted values and divided by sum of weights.',
                    'hint_sk': 'sum(z * w) / sum(w).',
                    'hint_en': 'Calculate sum(z * w) / sum(w).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vazeny_priemer([(1, 3), (3, 1)])', 'expected_output': '1.5', 'test_code': 'assert vazeny_priemer([(1, 3), (3, 1)]) == 1.5', 'is_hidden': False},
                        {'input_data': 'vazeny_priemer([(2, 1), (2, 2)])', 'expected_output': '2.0', 'test_code': 'assert vazeny_priemer([(2, 1), (2, 2)]) == 2.0', 'is_hidden': False},
                        {'input_data': 'vazeny_priemer([])', 'expected_output': '0.0', 'test_code': 'assert vazeny_priemer([]) == 0.0', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Hľadanie najčastejšej známky (Modus)',
                    'title_en': 'Find Grade Mode (Most Frequent)',
                    'instructions_sk': 'Napíš funkciu `modus_znamok(znamky)`: vráti známku (1 až 5), ktorá sa v zozname vyskytuje najčastejšie. Ak má viacero známok rovnaký maximálny počet výskytov, vráti tú menšiu (lepšiu známku). Ak je zoznam prázdny, vráti `None`.',
                    'instructions_en': 'Write function `modus_znamok(znamky)` returning most frequent grade, tie-breaking by smaller grade.',
                    'starter_code': 'def modus_znamok(znamky):\n    # Nájdi modus známok\n    pass\n',
                    'solution_code': (
                        'def modus_znamok(znamky):\n'
                        '    if not znamky:\n'
                        '        return None\n'
                        '    pocitadlo = {}\n'
                        '    for z in znamky:\n'
                        '        pocitadlo[z] = pocitadlo.get(z, 0) + 1\n'
                        '    # Triedenie podľa počtu zostupne, a pri zhode podľa známky vzostupne\n'
                        '    zoradene = sorted(pocitadlo.items(), key=lambda item: (-item[1], item[0]))\n'
                        '    return zoradene[0][0]\n'
                    ),
                    'explanation_sk': 'Spočítali sme výskyty a zoradili podľa (-pocet, znamka).',
                    'explanation_en': 'Counted frequencies and sorted by (-count, grade).',
                    'hint_sk': 'Použi slovník na počítanie výskytov a sorted(key=lambda x: (-pocet, znamka)).',
                    'hint_en': 'Sort by negative frequency then grade value.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'modus_znamok([1, 2, 2, 3, 2, 1])', 'expected_output': '2', 'test_code': 'assert modus_znamok([1, 2, 2, 3, 2, 1]) == 2', 'is_hidden': False},
                        {'input_data': 'modus_znamok([1, 1, 2, 2])', 'expected_output': '1 (lepšia známka)', 'test_code': 'assert modus_znamok([1, 1, 2, 2]) == 1', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Komplexný klasifikačný report triedy',
                    'title_en': 'Comprehensive Class Report Generator',
                    'instructions_sk': (
                        "Napíš funkciu `klasifikacny_report(ziaci_znamky)`:\n"
                        "`ziaci_znamky` je slovník `{'Meno': [znamky]}`.\n"
                        "Funkcia vráti report ako slovník:\n"
                        "- `'priemery'`: slovník `{'Meno': zaokruhleny_priemer_na_2_miesta}`,\n"
                        "- `'vyznamenani'`: zoznam mien žiakov s priemerom <= 1.50 zoradených abecedne,\n"
                        "- `'najlepsi_ziak'`: meno žiaka s najnižším priemerom (pri zhode prvé abecedne)."
                    ),
                    'instructions_en': 'Write function `klasifikacny_report(ziaci_znamky)` analyzing student grades, honors, and valedictorian.',
                    'starter_code': 'def klasifikacny_report(ziaci_znamky):\n    # Vygeneruj klasifikačný report\n    pass\n',
                    'solution_code': (
                        'def klasifikacny_report(ziaci_znamky):\n'
                        '    if not ziaci_znamky:\n'
                        '        return {"priemery": {}, "vyznamenani": [], "najlepsi_ziak": None}\n'
                        '    priemery = {}\n'
                        '    for meno, znamky in ziaci_znamky.items():\n'
                        '        priemery[meno] = round(sum(znamky) / len(znamky), 2) if znamky else 0.0\n'
                        '    vyznamenani = sorted([m for m, p in priemery.items() if p <= 1.50 and p > 0])\n'
                        '    najlepsi = sorted(priemery.items(), key=lambda x: (x[1], x[0]))[0][0]\n'
                        '    return {\n'
                        '        "priemery": priemery,\n'
                        '        "vyznamenani": vyznamenani,\n'
                        '        "najlepsi_ziak": najlepsi\n'
                        '    }\n'
                    ),
                    'explanation_sk': 'Vypočítali sme priemery, vyfiltrovali vyznamenaných a našli premianta triedy.',
                    'explanation_en': 'Calculated GPAs, filtered honors, and picked top ranking student.',
                    'hint_sk': 'Prejdi slovník, spočítaj sum/len pre každého a zoraď.',
                    'hint_en': 'Compute average per student and sort honors.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'klasifikacny_report({"Juraj": [1, 1, 2], "Martin": [2, 3, 2]})',
                            'expected_output': 'Dict with Juraj in vyznamenani and as best',
                            'test_code': (
                                'rep = klasifikacny_report({"Juraj": [1, 1, 2], "Martin": [2, 3, 2]})\n'
                                'assert rep["priemery"]["Juraj"] == 1.33\n'
                                'assert rep["vyznamenani"] == ["Juraj"]\n'
                                'assert rep["najlepsi_ziak"] == "Juraj"\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Detekcia kolízií v čase a plánovač rozvrhu',
            'title_en': 'Interval Collision Detection & Schedule Planner',
            'summary_sk': 'Reprezentácia časových intervalov, prekrývanie (Overlapping intervals) a detekcia konfliktov v rozvrhu.',
            'summary_en': 'Time interval representation, overlapping intervals algorithm, and schedule collision resolution.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 17.3 Algoritmus detekcie časových kolízií

Dva časové intervaly $[A_{\\text{start}}, A_{\\text{end}}]$ a $[B_{\\text{start}}, B_{\\text{end}}]$ sa **prekrývajú práve vtedy, keď**:
$$A_{\\text{start}} < B_{\\text{end}} \\quad \\text{a} \\quad B_{\\text{start}} < A_{\\text{end}}$$

Tento jednoduchý matematický vzťah je základom rozvrhových systémov, kalendárov a herných kolíznych enginov.
""",
            'content_en': """### 17.3 Interval Collision Algorithm

Two intervals overlap if and only if `startA < endB and startB < endA`.
""",
            'quizzes': [
                {
                    'question_sk': 'Prekrývajú sa intervaly (8:00 - 10:00) a (10:00 - 12:00)?',
                    'question_en': 'Do intervals (8:00 - 10:00) and (10:00 - 12:00) overlap?',
                    'option_a_sk': 'Nie, pretože koniec prvého sa rovná začiatku druhého (dotýkajú sa, ale neprekrývajú)', 'option_a_en': 'No, because end of first equals start of second (touching, not overlapping)',
                    'option_b_sk': 'Áno, kolidujú o 10:00', 'option_b_en': 'Yes, collide at 10:00',
                    'option_c_sk': 'Závisí od dňa v týždni', 'option_c_en': 'Depends on day',
                    'option_d_sk': 'Vyvolá to výnimku', 'option_d_en': 'Raises exception',
                    'correct_option': 'A',
                    'explanation_sk': 'Ak start2 >= end1, intervaly sa neprekrývajú.',
                    'explanation_en': 'Touching boundaries do not constitute an overlap.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Detekcia prekrytia dvoch časových intervalov',
                    'title_en': 'Detect Two Interval Overlap',
                    'instructions_sk': 'Napíš funkciu `koliduju_intervaly(start1, end1, start2, end2)`: vráti `True`, ak sa intervaly ostro prekrývajú (`start1 < end2 and start2 < end1`), inak vráti `False`.',
                    'instructions_en': 'Write function `koliduju_intervaly(start1, end1, start2, end2)` returning True on interval overlap.',
                    'starter_code': 'def koliduju_intervaly(start1, end1, start2, end2):\n    # Over prekrytie intervalov\n    pass\n',
                    'solution_code': (
                        'def koliduju_intervaly(start1, end1, start2, end2):\n'
                        '    return start1 < end2 and start2 < end1\n'
                    ),
                    'explanation_sk': 'Aplikovali sme podmienku vzájomného prekrytia.',
                    'explanation_en': 'Applied interval collision formula.',
                    'hint_sk': 'return start1 < end2 and start2 < end1.',
                    'hint_en': 'Return start1 < end2 and start2 < end1.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'koliduju_intervaly(8, 10, 9, 11)', 'expected_output': 'True', 'test_code': 'assert koliduju_intervaly(8, 10, 9, 11) is True', 'is_hidden': False},
                        {'input_data': 'koliduju_intervaly(8, 10, 10, 12)', 'expected_output': 'False', 'test_code': 'assert koliduju_intervaly(8, 10, 10, 12) is False', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Kontrola kolízií v dennom rozvrhu učiteľa',
                    'title_en': 'Teacher Daily Schedule Collision Check',
                    'instructions_sk': (
                        "Napíš funkciu `ma_rozvrh_koliziu(zoznam_hodin)`:\n"
                        "`zoznam_hodin` obsahuje dvojice `[(start, end), ...]`.\n"
                        "Funkcia overí, či existuje akákoľvek dvojica hodín, ktorá sa prekrýva. Ak áno, vráti `True`, inak `False`."
                    ),
                    'instructions_en': 'Write function `ma_rozvrh_koliziu(zoznam_hodin)` detecting if any pairs in schedule collide.',
                    'starter_code': 'def ma_rozvrh_koliziu(zoznam_hodin):\n    # Nájdi kolíziu v rozvrhu\n    pass\n',
                    'solution_code': (
                        'def ma_rozvrh_koliziu(zoznam_hodin):\n'
                        '    n = len(zoznam_hodin)\n'
                        '    for i in range(n):\n'
                        '        for j in range(i + 1, n):\n'
                        '            s1, e1 = zoznam_hodin[i]\n'
                        '            s2, e2 = zoznam_hodin[j]\n'
                        '            if s1 < e2 and s2 < e1:\n'
                        '                return True\n'
                        '    return False\n'
                    ),
                    'explanation_sk': 'Porovnali sme každú dvojicu hodín na prekrytie.',
                    'explanation_en': 'Compared all interval pairs for overlap.',
                    'hint_sk': 'Dvojitý cyklus for i in range(n): for j in range(i+1, n): testuj kolíziu.',
                    'hint_en': 'Nested loop testing interval pairs.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'ma_rozvrh_koliziu([(8, 10), (10, 12), (12, 14)])', 'expected_output': 'False', 'test_code': 'assert ma_rozvrh_koliziu([(8, 10), (10, 12), (12, 14)]) is False', 'is_hidden': False},
                        {'input_data': 'ma_rozvrh_koliziu([(8, 10), (9, 11)])', 'expected_output': 'True', 'test_code': 'assert ma_rozvrh_koliziu([(8, 10), (9, 11)]) is True', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Rezervačný systém učební bez kolízií',
                    'title_en': 'Classroom Reservation Engine',
                    'instructions_sk': (
                        "Napíš funkciu `rezervuj_ucebnu(ucebne_rozvrhy, start, end)`:\n"
                        "`ucebne_rozvrhy` je slovník `{'Ucebna_1': [(s, e), ...], 'Ucebna_2': [...]}`.\n"
                        "Funkcia nájde prvú učebňu (v abecednom poradí názvov), ktorá nemá v intervale `(start, end)` žiadnu kolíziu.\n"
                        "Ak takú nájde, pridá interval do jej rozvrhu a vráti názov učebne. Ak sú všetky obsadené, vráti `None`."
                    ),
                    'instructions_en': 'Write function `rezervuj_ucebnu(ucebne_rozvrhy, start, end)` booking first available room sorted alphabetically.',
                    'starter_code': 'def rezervuj_ucebnu(ucebne_rozvrhy, start, end):\n    # Nájdi voľnú učebňu\n    pass\n',
                    'solution_code': (
                        'def rezervuj_ucebnu(ucebne_rozvrhy, start, end):\n'
                        '    for ucebna in sorted(ucebne_rozvrhy.keys()):\n'
                        '        obsadene = ucebne_rozvrhy[ucebna]\n'
                        '        kolizia = any(start < e and s < end for s, e in obsadene)\n'
                        '        if not kolizia:\n'
                        '            obsadene.append((start, end))\n'
                        '            return ucebna\n'
                        '    return None\n'
                    ),
                    'explanation_sk': 'Prešli sme učebne abecedne, overili kolíziu a pridali novú rezerváciu.',
                    'explanation_en': 'Checked room schedule availability in alphabetical order.',
                    'hint_sk': 'Prechádzaj sorted(ucebne_rozvrhy.keys()) a over kolíziu pre každú.',
                    'hint_en': 'Iterate sorted rooms and check any collision.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'rezervuj_ucebnu({"LAB_A": [(8, 10)], "LAB_B": []}, 8, 10)',
                            'expected_output': '"LAB_B"',
                            'test_code': 'assert rezervuj_ucebnu({"LAB_A": [(8, 10)], "LAB_B": []}, 8, 10) == "LAB_B"',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Bezstratová kompresia dát: Algoritmus RLE',
            'title_en': 'Lossless Data Compression: RLE Algorithm',
            'summary_sk': 'Princíp Run-Length Encoding (RLE), kódovanie sérií opakujúcich sa znakov a dekompresia.',
            'summary_en': 'Run-Length Encoding principles, sequential run encoding, and bitstream decompression.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 17.4 RLE kompresia (Run-Length Encoding)

RLE je základný bezstratový kompresný algoritmus. Ak sa v dátach opakujú rovnaké znaky za sebou, nahradí ich dvojicou **(počet, znak)**:
- Vstup: `"WWWWWWAAAAABBB"`
- Výstup: `"6W5A3B"`
""",
            'content_en': """### 17.4 Run-Length Encoding (RLE)

Compress repetitive character sequences into count-char pairs.
""",
            'quizzes': [
                {
                    'question_sk': 'Na aký typ dát je RLE kompresia najúčinnejšia?',
                    'question_en': 'For what type of data is RLE compression most effective?',
                    'option_a_sk': 'Dáta s dlhými sériami opakujúcich sa hodnôt (napr. jednoduchá grafika, bitmapy)', 'option_a_en': 'Data with long consecutive runs of identical values (bitmaps, icons)',
                    'option_b_sk': 'Náhodné čísla', 'option_b_en': 'Random numbers',
                    'option_c_sk': 'Už zašifrované dáta', 'option_c_en': 'Encrypted ciphertext',
                    'option_d_sk': 'Slovníky', 'option_d_en': 'Dictionaries',
                    'correct_option': 'A',
                    'explanation_sk': 'RLE exceluje pri dlhých sekvenciách rovnakých pixelov alebo znakov.',
                    'explanation_en': 'RLE compresses long identical sequences efficiently.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'RLE kompresia textu',
                    'title_en': 'RLE String Compression',
                    'instructions_sk': 'Napíš funkciu `rle_komprimuj(text)`: zakóduje reťazec do RLE formátu (napr. "AAABBC" -> "3A2B1C"). Pre prázdny reťazec vráti `""`.',
                    'instructions_en': 'Write function `rle_komprimuj(text)` encoding strings into RLE count-char format.',
                    'starter_code': 'def rle_komprimuj(text):\n    # Zakóduj text cez RLE\n    pass\n',
                    'solution_code': (
                        'def rle_komprimuj(text):\n'
                        '    if not text:\n'
                        '        return ""\n'
                        '    vysledok = []\n'
                        '    aktualny = text[0]\n'
                        '    pocet = 1\n'
                        '    for ch in text[1:]:\n'
                        '        if ch == aktualny:\n'
                        '            pocet += 1\n'
                        '        else:\n'
                        '            vysledok.append(f"{pocet}{aktualny}")\n'
                        '            aktualny = ch\n'
                        '            pocet = 1\n'
                        '    vysledok.append(f"{pocet}{aktualny}")\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Počítali sme dĺžku série aktuálneho znaku a pri zmene zapísali počet a znak.',
                    'explanation_en': 'Tracked consecutive character runs and appended count + char.',
                    'hint_sk': 'Udržuj premenné aktualny_znak a pocet v cykle cez text.',
                    'hint_en': 'Track current char and count accumulator.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'rle_komprimuj("AAABBBCC")', 'expected_output': '"3A3B2C"', 'test_code': 'assert rle_komprimuj("AAABBBCC") == "3A3B2C"', 'is_hidden': False},
                        {'input_data': 'rle_komprimuj("")', 'expected_output': '""', 'test_code': 'assert rle_komprimuj("") == ""', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'RLE dekompresia textu',
                    'title_en': 'RLE String Decompression',
                    'instructions_sk': 'Napíš funkciu `rle_dekomprimuj(rle_text)`: zrekonštruuje pôvodný reťazec (napr. "3A2B1C" -> "AAABBC").',
                    'instructions_en': 'Write function `rle_dekomprimuj(rle_text)` reconstructing uncompressed string from RLE format.',
                    'starter_code': 'import re\n\ndef rle_dekomprimuj(rle_text):\n    # Dekóduj RLE reťazec\n    pass\n',
                    'solution_code': (
                        'import re\n\n'
                        'def rle_dekomprimuj(rle_text):\n'
                        '    if not rle_text:\n'
                        '        return ""\n'
                        '    vysledok = []\n'
                        '    for pocet, znak in re.findall(r"(\\d+)([a-zA-Z])", rle_text):\n'
                        '        vysledok.append(znak * int(pocet))\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Pomocou regexu sme vytiahli dvojice (pocet, znak) a vynásobili znaky.',
                    'explanation_en': 'Extracted count-char pairs via regex and expanded strings.',
                    'hint_sk': 'Použi re.findall(r"(\\d+)([a-zA-Z])", rle_text).',
                    'hint_en': 'Use regex to extract count and char pairs.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'rle_dekomprimuj("3A3B2C")', 'expected_output': '"AAABBBCC"', 'test_code': 'assert rle_dekomprimuj("3A3B2C") == "AAABBBCC"', 'is_hidden': False},
                        {'input_data': 'rle_dekomprimuj("")', 'expected_output': '""', 'test_code': 'assert rle_dekomprimuj("") == ""', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Výpočet kompresného pomeru a úspory pamäte',
                    'title_en': 'Compute Compression Ratio & Savings',
                    'instructions_sk': (
                        "Napíš funkciu `kompresny_report(povodny_text)`:\n"
                        "1. Zakóduje text pomocou RLE.\n"
                        "2. Vypočíta percentuálnu úsporu: `(1 - len(komprimovany) / len(povodny)) * 100`.\n"
                        "Vráti slovník `{'povodna_dlzka': int, 'nova_dlzka': int, 'uspora_pct': float}` zaokrúhlený na 2 miesta.\n"
                        "Ak je text prázdny, vráti `{'povodna_dlzka': 0, 'nova_dlzka': 0, 'uspora_pct': 0.0}`."
                    ),
                    'instructions_en': 'Write function `kompresny_report(povodny_text)` calculating size reduction metrics.',
                    'starter_code': 'def kompresny_report(povodny_text):\n    # Vypočítaj úsporu RLE\n    pass\n',
                    'solution_code': (
                        'def kompresny_report(povodny_text):\n'
                        '    if not povodny_text:\n'
                        '        return {"povodna_dlzka": 0, "nova_dlzka": 0, "uspora_pct": 0.0}\n'
                        '    # RLE kompresia\n'
                        '    vysledok = []\n'
                        '    aktualny = povodny_text[0]\n'
                        '    pocet = 1\n'
                        '    for ch in povodny_text[1:]:\n'
                        '        if ch == aktualny:\n'
                        '            pocet += 1\n'
                        '        else:\n'
                        '            vysledok.append(f"{pocet}{aktualny}")\n'
                        '            aktualny = ch\n'
                        '            pocet = 1\n'
                        '    vysledok.append(f"{pocet}{aktualny}")\n'
                        '    komprimovany = "".join(vysledok)\n'
                        '    l1 = len(povodny_text)\n'
                        '    l2 = len(komprimovany)\n'
                        '    uspora = round((1.0 - (l2 / l1)) * 100.0, 2)\n'
                        '    return {"povodna_dlzka": l1, "nova_dlzka": l2, "uspora_pct": uspora}\n'
                    ),
                    'explanation_sk': 'Komprimovali sme text a vypočítali percentuálnu zmenu dĺžky.',
                    'explanation_en': 'Encoded and computed percentage size delta.',
                    'hint_sk': 'uspora = round((1.0 - (l2 / l1)) * 100.0, 2).',
                    'hint_en': 'Calculate percentage delta.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'kompresny_report("AAAAAAAAAA")',
                            'expected_output': "{'povodna_dlzka': 10, 'nova_dlzka': 3, 'uspora_pct': 70.0}",
                            'test_code': 'assert kompresny_report("AAAAAAAAAA") == {"povodna_dlzka": 10, "nova_dlzka": 3, "uspora_pct": 70.0}',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 5,
            'title_sk': 'Sieťové protokoly: štruktúra paketov a kontrolný súčet (Checksum)',
            'title_en': 'Network Protocols: Packet Frames & Checksums',
            'summary_sk': 'Simulácia sieťových paketov, hlavička, telo, CRC/Checksum overenie a detekcia poškodenia dát.',
            'summary_en': 'Network packet simulation, header metadata, payload data, and checksum error detection.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 17.5 Sieťové pakety a kontrolný súčet

Pri prenose dát v počítačových sieťach (TCP/IP, UDP) je každá správa rozdelená na pakety obsahujúce:
1. **Hlavičku (Header)** – metadáta (odosielateľ, príjemca, číslo paketu, dĺžka)
2. **Užitočné zaťaženie (Payload)** – prenášané dáta
3. **Kontrolný súčet (Checksum)** – hodnota na detekciu poškodenia pri prenose

```python
# XOR Checksum
def vypocitaj_checksum(payload_bytes):
    cs = 0
    for b in payload_bytes:
        cs ^= b
    return cs
```
""",
            'content_en': """### 17.5 Network Packets & Checksum Validation

Build packet frames with headers and verify payload integrity using checksum calculations.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je hlavný účel kontrolného súčtu (Checksum) v sieťovom pakete?',
                    'question_en': 'What is the primary function of a packet checksum?',
                    'option_a_sk': 'Detegovať, či sa dáta pri prenose cez sieť nepoškodili chybou na prenosovej trase', 'option_a_en': 'Detect whether transmitted data was corrupted in transit',
                    'option_b_sk': 'Zrýchliť internetové pripojenie', 'option_b_en': 'Speed up network connection',
                    'option_c_sk': 'Šifrovať heslo používateľa', 'option_c_en': 'Encrypt user password',
                    'option_d_sk': 'Zväčšiť veľkosť paketu', 'option_d_en': 'Enlarge packet size',
                    'correct_option': 'A',
                    'explanation_sk': 'Kontrolný súčet overuje integritu prenesených bajtov.',
                    'explanation_en': 'Checksum validates transmission integrity.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet parity (Even Parity Bit)',
                    'title_en': 'Compute Even Parity Bit',
                    'instructions_sk': 'Napíš funkciu `vypocitaj_paritu(bajt_int)`: vráti `0`, ak má číslo v binárnom zápise párny počet jednotiek, inak vráti `1`.',
                    'instructions_en': 'Write function `vypocitaj_paritu(bajt_int)` returning 0 if binary representation has even number of 1s, else 1.',
                    'starter_code': 'def vypocitaj_paritu(bajt_int):\n    # Vypočítaj paritný bit\n    pass\n',
                    'solution_code': (
                        'def vypocitaj_paritu(bajt_int):\n'
                        '    pocet_jednotiek = bin(bajt_int).count("1")\n'
                        '    return 0 if pocet_jednotiek % 2 == 0 else 1\n'
                    ),
                    'explanation_sk': 'Spočítali sme jednotky v binárnom reťazci bin(n).count("1").',
                    'explanation_en': 'Counted set bits in binary string.',
                    'hint_sk': 'Použi bin(bajt_int).count("1") % 2.',
                    'hint_en': 'Use bin().count("1") modulo 2.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vypocitaj_paritu(3)', 'expected_output': '0 (bin 11 má 2 jednotky)', 'test_code': 'assert vypocitaj_paritu(3) == 0', 'is_hidden': False},
                        {'input_data': 'vypocitaj_paritu(7)', 'expected_output': '1 (bin 111 má 3 jednotky)', 'test_code': 'assert vypocitaj_paritu(7) == 1', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Zostavenie rámca sieťového paketu',
                    'title_en': 'Assemble Network Packet Frame',
                    'instructions_sk': (
                        "Napíš funkciu `zostav_paket(odosielatel, prijemca, payload)`:\n"
                        "Vypočíta XOR checksum z payloadu (XOR všetkých kódov `ord(c)` v payload). Ak je payload prázdny, checksum je 0.\n"
                        "Vráti reťazec v tvare:\n"
                        "`f'FROM:{odosielatel}|TO:{prijemca}|LEN:{len(payload)}|CS:{checksum}|DATA:{payload}'`."
                    ),
                    'instructions_en': 'Write function `zostav_paket(odosielatel, prijemca, payload)` assembling structured packet frame with XOR checksum.',
                    'starter_code': 'def zostav_paket(odosielatel, prijemca, payload):\n    # Zostav sieťový paket\n    pass\n',
                    'solution_code': (
                        'def zostav_paket(odosielatel, prijemca, payload):\n'
                        '    cs = 0\n'
                        '    for ch in payload:\n'
                        '        cs ^= ord(ch)\n'
                        '    return f"FROM:{odosielatel}|TO:{prijemca}|LEN:{len(payload)}|CS:{cs}|DATA:{payload}"\n'
                    ),
                    'explanation_sk': 'Spočítali sme XOR checksum dát a naformátovali paketový reťazec.',
                    'explanation_en': 'Computed XOR checksum of payload and assembled frame string.',
                    'hint_sk': 'Vypočítaj cs ^= ord(ch) a vráti naformátovaný reťazec.',
                    'hint_en': 'XOR character ordinals and format string.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'zostav_paket("client", "server", "PING")',
                            'expected_output': 'Packet string',
                            'test_code': 'assert zostav_paket("client", "server", "PING") == f"FROM:client|TO:server|LEN:4|CS:{ord(\'P\')^ord(\'I\')^ord(\'N\')^ord(\'G\')}|DATA:PING"',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Overenie integrity prijatého sieťového paketu',
                    'title_en': 'Verify Received Network Packet Frame',
                    'instructions_sk': (
                        "Napíš funkciu `over_paket(paket_str)`:\n"
                        "Rozloží paket podľa oddeľovača `|`.\n"
                        "Overí, že:\n"
                        "1. Dĺžka `LEN` sedí s dĺžkou dát za `DATA:`,\n"
                        "2. Kontrolný súčet `CS` sedí s prepočítaným XOR checksumom dát.\n"
                        "Ak je paket neporušený, vráti payload reťazec. Ak je poškodený, vráti `None`."
                    ),
                    'instructions_en': 'Write function `over_paket(paket_str)` verifying length and XOR checksum matching or returning None.',
                    'starter_code': 'def over_paket(paket_str):\n    # Over integritu paketu\n    pass\n',
                    'solution_code': (
                        'def over_paket(paket_str):\n'
                        '    try:\n'
                        '        casti = paket_str.split("|")\n'
                        '        d = {}\n'
                        '        for c in casti:\n'
                        '            k, v = c.split(":", 1)\n'
                        '            d[k] = v\n'
                        '        payload = d["DATA"]\n'
                        '        ocakavana_dlzka = int(d["LEN"])\n'
                        '        ocakavany_cs = int(d["CS"])\n'
                        '        if len(payload) != ocakavana_dlzka:\n'
                        '            return None\n'
                        '        skutocny_cs = 0\n'
                        '        for ch in payload:\n'
                        '            skutocny_cs ^= ord(ch)\n'
                        '        if skutocny_cs != ocakavany_cs:\n'
                        '            return None\n'
                        '        return payload\n'
                    '    except Exception:\n'
                    '        return None\n'
                    ),
                    'explanation_sk': 'Rozparsovali sme hlavičku paketu a skontrolovali dĺžku a XOR checksum.',
                    'explanation_en': 'Parsed header tokens, verified payload length and recalculated XOR checksum.',
                    'hint_sk': 'Rozdeľ podľa "|" a porovnaj LEN a recalculovaný XOR CS.',
                    'hint_en': 'Split by pipe, parse fields and check recalculated checksum.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'over_paket("FROM:a|TO:b|LEN:2|CS:3|DATA:OK")',
                            'expected_output': 'OK or None depending on cs match',
                            'test_code': (
                                'p_ok = f"FROM:a|TO:b|LEN:2|CS:{ord(\'O\')^ord(\'K\')}|DATA:OK"\n'
                                'assert over_paket(p_ok) == "OK"\n'
                                'p_corrupt = f"FROM:a|TO:b|LEN:2|CS:999|DATA:OK"\n'
                                'assert over_paket(p_corrupt) is None\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        }
    ]
}
