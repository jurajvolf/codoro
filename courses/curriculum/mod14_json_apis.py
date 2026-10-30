"""
MODUL 14: Spracovanie JSON dát, REST API štruktúry a dátová analytika
Odhadovaný rozsah: 12 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU | Track: ALGORITHMS_AND_DATA
"""

MODULE_DATA = {
    'order': 14,
    'track': 'ALGORITHMS_AND_DATA',
    'title_sk': 'Spracovanie JSON dát, REST API štruktúry a dátová analytika',
    'title_en': 'JSON Data Processing, REST API Structures & Analytics',
    'description_sk': 'Nauč sa serializovať a deserializovať JSON dáta pomocou modulu json, spracovávať štruktúrované REST API odpovede (payloads, chybové stavy, paginácia) a realizovať dátovú analytiku nad komplexnými JSON datasetmi.',
    'description_en': 'Master JSON serialization and deserialization with the json module, parse structured REST API responses, handle pagination, and perform data analytics on nested JSON datasets.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'braces',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Serializácia a deserializácia v module json (loads & dumps)',
            'title_en': 'Serialization & Deserialization with json (loads & dumps)',
            'summary_sk': 'json.loads(), json.dumps(), parametre indent, ensure_ascii, sort_keys a zachytávanie JSONDecodeError.',
            'summary_en': 'json.loads(), json.dumps(), indent, ensure_ascii, sort_keys, and handling JSONDecodeError.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 14.1 Formát JSON a modul `json` v Pythone

**JSON** (JavaScript Object Notation) je najrozšírenejší textový formát na výmenu dát medzi servermi, webovými aplikáciami a mikroslužbami.

#### Dva základné smery prevodu:
1. **Deserializácia (Parsing)**: prevod reťazca JSON na Python objekt (`dict`, `list`):
   - `json.loads(retazec)` – load string
2. **Serializácia**: prevod Python objektu na JSON reťazec:
   - `json.dumps(objekt)` – dump string

#### Prehľad mapovania typov:
| JSON typ | Python typ |
| :--- | :--- |
| `object` (`{}`) | `dict` |
| `array` (`[]`) | `list` |
| `string` | `str` |
| `number` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

```python
import json

data = {"meno": "Juraj", "vek": 18, "admin": False, "zaluby": ["kódovanie", "matematika"]}

# Serializácia do pekne formátovaného JSON
json_text = json.dumps(data, indent=2, ensure_ascii=False)
print(json_text)

# Deserializácia späť na slovník
obj = json.loads(json_text)
print(obj["meno"])  # 'Juraj'
```

> **Častá chyba v praxi:**
> Pozor na `ensure_ascii=False`. Ak v Pythone serializujete slovenské znaky (napr. `"Bratislava"` alebo `"Košice"`), bez tohto parametra ich Python prevedie na unicode escape kódy typu `\\u0161`. Pre čistý UTF-8 výstup vždy nastavte `ensure_ascii=False`.
""",
            'content_en': """### 14.1 JSON Module in Python

Use `json.loads()` for string deserialization and `json.dumps()` with `ensure_ascii=False` and `indent=2`.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú hodnotu vráti `json.loads("null")` v Pythone?',
                    'question_en': 'What does `json.loads("null")` evaluate to in Python?',
                    'option_a_sk': 'None', 'option_a_en': 'None',
                    'option_b_sk': '"" (prázdny reťazec)', 'option_b_en': '"" (empty string)',
                    'option_c_sk': '0', 'option_c_en': '0',
                    'option_d_sk': 'Vyvolá chybu', 'option_d_en': 'Raises an error',
                    'correct_option': 'A',
                    'explanation_sk': 'Hodnota null v JSON sa v Pythone mapuje na vstavanú konštantu None.',
                    'explanation_en': 'JSON null translates directly to Python None.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Prevod slovníka na JSON reťazec',
                    'title_en': 'Convert Dictionary to JSON String',
                    'instructions_sk': 'Napíš funkciu `slovnik_na_json(data)`, ktorá prevedie Python slovník na JSON reťazec s parametrami `ensure_ascii=False` a `sort_keys=True`.',
                    'instructions_en': 'Write function `slovnik_na_json(data)` returning JSON string with `ensure_ascii=False` and `sort_keys=True`.',
                    'starter_code': 'import json\n\ndef slovnik_na_json(data):\n    # Serializuj na JSON\n    pass\n',
                    'solution_code': 'import json\n\ndef slovnik_na_json(data):\n    return json.dumps(data, ensure_ascii=False, sort_keys=True)\n',
                    'explanation_sk': 'Použili sme json.dumps s ensure_ascii=False a zoradením kľúčov sort_keys=True.',
                    'explanation_en': 'We used json.dumps with UTF-8 preservation and sorted keys.',
                    'hint_sk': 'Použi json.dumps(data, ensure_ascii=False, sort_keys=True).',
                    'hint_en': 'Use json.dumps with requested arguments.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'slovnik_na_json({"b": 2, "a": 1})', 'expected_output': '\'{"a": 1, "b": 2}\'', 'test_code': 'assert slovnik_na_json({"b": 2, "a": 1}) == \'{"a": 1, "b": 2}\'', 'is_hidden': False},
                        {'input_data': 'slovnik_na_json({"mesto": "Žilina"})', 'expected_output': '\'{"mesto": "Žilina"}\'', 'test_code': 'assert slovnik_na_json({"mesto": "Žilina"}) == \'{"mesto": "Žilina"}\'', 'is_hidden': False},
                        {'input_data': 'slovnik_na_json({})', 'expected_output': '\'{}\'', 'test_code': 'assert slovnik_na_json({}) == "{}"', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Bezpečné načítanie JSON s ošetrením chýb',
                    'title_en': 'Safe JSON Parsing with Error Handling',
                    'instructions_sk': 'Napíš funkciu `bezpecny_json_load(json_str)`, ktorá sa pokúsi načítať JSON pomocou `json.loads()`. Ak je reťazec neplatný (vyvolá `json.JSONDecodeError` alebo `TypeError`), funkcia zachytí výnimku a vráti `None`.',
                    'instructions_en': 'Write function `bezpecny_json_load(json_str)` returning parsed object or None on JSONDecodeError.',
                    'starter_code': 'import json\n\ndef bezpecny_json_load(json_str):\n    # Ošetri chybu parsovania\n    pass\n',
                    'solution_code': 'import json\n\ndef bezpecny_json_load(json_str):\n    try:\n        return json.loads(json_str)\n    except (json.JSONDecodeError, TypeError):\n        return None\n',
                    'explanation_sk': 'Použili sme try/except pre zachytenie JSONDecodeError a TypeError.',
                    'explanation_en': 'Caught JSONDecodeError and TypeError returning None gracefully.',
                    'hint_sk': 'Použi try: return json.loads(json_str) except (json.JSONDecodeError, TypeError): return None.',
                    'hint_en': 'Wrap loads in try/except block.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'bezpecny_json_load(\'{"kurz": "Python"}\')', 'expected_output': "{'kurz': 'Python'}", 'test_code': 'assert bezpecny_json_load(\'{"kurz": "Python"}\') == {"kurz": "Python"}', 'is_hidden': False},
                        {'input_data': 'bezpecny_json_load("Neplatný json")', 'expected_output': 'None', 'test_code': 'assert bezpecny_json_load("Neplatný json") is None', 'is_hidden': False},
                        {'input_data': 'bezpecny_json_load("[1, 2, 3]")', 'expected_output': '[1, 2, 3]', 'test_code': 'assert bezpecny_json_load("[1, 2, 3]") == [1, 2, 3]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Formátovač JSON s vlastným odsadením',
                    'title_en': 'Pretty-Printer with Custom Indent',
                    'instructions_sk': 'Napíš funkciu `formatuj_json(json_str, odsadenie=4)`, ktorá načíta zadaný JSON reťazec a vráti ho späť formátovaný so zadaným počtom medzier odsadenia (`indent`) a zoradenými kľúčmi. Ak je vstup neplatný, vráti pôvodný reťazec.',
                    'instructions_en': 'Write function `formatuj_json(json_str, odsadenie=4)` returning pretty formatted JSON or original text on error.',
                    'starter_code': 'import json\n\ndef formatuj_json(json_str, odsadenie=4):\n    # Formátuj JSON reťazec\n    pass\n',
                    'solution_code': (
                        'import json\n\n'
                        'def formatuj_json(json_str, odsadenie=4):\n'
                        '    try:\n'
                        '        obj = json.loads(json_str)\n'
                        '        return json.dumps(obj, indent=odsadenie, sort_keys=True, ensure_ascii=False)\n'
                        '    except Exception:\n'
                        '        return json_str\n'
                    ),
                    'explanation_sk': 'Načítali sme dáta a opätovne serializovali s požadovaným odsadením a zoraďovaním.',
                    'explanation_en': 'Deserialized and re-serialized with indent and sorted keys.',
                    'hint_sk': 'Použi json.loads a následne json.dumps s indent=odsadenie.',
                    'hint_en': 'Call json.loads then json.dumps with indent parameter.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'formatuj_json(\'{"b":2,"a":1}\', odsadenie=2)',
                            'expected_output': 'Formatted string',
                            'test_code': 'assert formatuj_json(\'{"b":2,"a":1}\', odsadenie=2) == \'{\\n  "a": 1,\\n  "b": 2\\n}\'',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'formatuj_json("chybny json")',
                            'expected_output': '"chybny json"',
                            'test_code': 'assert formatuj_json("chybny json") == "chybny json"',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Validácia štruktúry a kľúčov JSON dát',
            'title_en': 'JSON Data Structure & Schema Validation',
            'summary_sk': 'Defenzívna validácia kľúčov, povinné polia, kontrola typov hodnôt a čistenie vstupov.',
            'summary_en': 'Defensive validation of required keys, data type checks, and input normalization.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 14.2 Validácia dátovej schémy JSON objektov

Dáta prijaté z vonkajších zdrojov (používateľské vstupy, API tretích strán) nesmieme nikdy považovať za bezpečné ani kompletné bez overenia schémy.

#### Stratégia defenzívneho overovania:
1. Kontrola prítomnosti všetkých povinných kľúčov (`required_keys`)
2. Kontrola dátových typov jednotlivých hodnôt (`isinstance(value, expected_type)`)
3. Kontrola povolených rozsahov (napr. vek $\\ge 0$, cena $> 0$)

```python
def validuj_pouzivatela(obj):
    if not isinstance(obj, dict):
        return False, "Dáta musia byť slovník"
    
    povinne = {"id": int, "email": str, "aktivny": bool}
    for kluc, typ in povinne.items():
        if kluc not in obj:
            return False, f"Chýba povinné pole: {kluc}"
        if not isinstance(obj[kluc], typ):
            return False, f"Pole {kluc} musí byť typu {typ.__name__}"
            
    return True, "Schéma je v poriadku"
```
""",
            'content_en': """### 14.2 Schema & Key Validation

Assert required dictionary keys and value types before persisting to database.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá metóda slovníka je najvhodnejšia na bezpečné čítanie voliteľných hodnôt bez vyvolania KeyError?',
                    'question_en': 'Which dictionary method safely reads optional values without KeyError?',
                    'option_a_sk': 'dict.get(key, default)', 'option_a_en': 'dict.get(key, default)',
                    'option_b_sk': 'dict[key]', 'option_b_en': 'dict[key]',
                    'option_c_sk': 'dict.find(key)', 'option_c_en': 'dict.find(key)',
                    'option_d_sk': 'dict.has(key)', 'option_d_en': 'dict.has(key)',
                    'correct_option': 'A',
                    'explanation_sk': 'dict.get(key, default) vráti predvolenú hodnotu, ak kľúč v slovníku neexistuje.',
                    'explanation_en': 'dict.get() gracefully returns default on missing keys.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Extrakcia e-mailov z poľa používateľov',
                    'title_en': 'Extract Emails from User Array',
                    'instructions_sk': 'Napíš funkciu `extrahuj_emaily(pouzivatelia_zoznam)`, ktorá prijme zoznam slovníkov používateľov a vráti zoznam e-mailových adries tých používateľov, ktorí majú nastavené `"aktivny": True`. Ak používateľ nemá pole email, preskoč ho.',
                    'instructions_en': 'Write function `extrahuj_emaily(pouzivatelia_zoznam)` returning emails of users where `"aktivny": True`.',
                    'starter_code': 'def extrahuj_emaily(pouzivatelia_zoznam):\n    # Vyber e-maily aktívnych používateľov\n    pass\n',
                    'solution_code': (
                        'def extrahuj_emaily(pouzivatelia_zoznam):\n'
                        '    emaily = []\n'
                        '    for u in pouzivatelia_zoznam:\n'
                        '        if u.get("aktivny") is True and "email" in u:\n'
                        '            emaily.append(u["email"])\n'
                        '    return emaily\n'
                    ),
                    'explanation_sk': 'Overili sme podmienku u.get("aktivny") is True a prítomnosť kľúča email.',
                    'explanation_en': 'Filtered for active users with valid email key.',
                    'hint_sk': 'Použi u.get("aktivny") is True a u.get("email").',
                    'hint_en': 'Use dict.get("aktivny") is True.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {
                            'input_data': 'extrahuj_emaily([{"email": "a@codoro.sk", "aktivny": True}, {"email": "b@codoro.sk", "aktivny": False}])',
                            'expected_output': "['a@codoro.sk']",
                            'test_code': 'assert extrahuj_emaily([{"email": "a@codoro.sk", "aktivny": True}, {"email": "b@codoro.sk", "aktivny": False}]) == ["a@codoro.sk"]',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'extrahuj_emaily([])',
                            'expected_output': '[]',
                            'test_code': 'assert extrahuj_emaily([]) == []',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Validátor povinnej schémy produktu',
                    'title_en': 'Product Schema Validator',
                    'instructions_sk': (
                        "Napíš funkciu `validuj_produkt(produkt_dict)`:\n"
                        "Overí, že slovník obsahuje:\n"
                        "1. `id` typu `int` (kladné číslo > 0),\n"
                        "2. `nazov` typu `str` (neprázdny reťazec po strip),\n"
                        "3. `cena` typu `int` alebo `float` (nezáporná >= 0.0).\n"
                        "Vráti `True`, ak je schéma platná, inak `False`."
                    ),
                    'instructions_en': 'Write function `validuj_produkt(produkt_dict)` checking id (int > 0), nazov (non-empty str), and cena (number >= 0).',
                    'starter_code': 'def validuj_produkt(produkt_dict):\n    # Over schému produktu\n    pass\n',
                    'solution_code': (
                        'def validuj_produkt(produkt_dict):\n'
                        '    if not isinstance(produkt_dict, dict):\n'
                        '        return False\n'
                        '    pid = produkt_dict.get("id")\n'
                        '    if not isinstance(pid, int) or pid <= 0:\n'
                        '        return False\n'
                        '    nazov = produkt_dict.get("nazov")\n'
                        '    if not isinstance(nazov, str) or not nazov.strip():\n'
                        '        return False\n'
                        '    cena = produkt_dict.get("cena")\n'
                        '    if not isinstance(cena, (int, float)) or isinstance(cena, bool) or cena < 0:\n'
                        '        return False\n'
                        '    return True\n'
                    ),
                    'explanation_sk': 'Skontrolovali sme typy, prítomnosť a hraničné podmienky pre id, nazov a cenu.',
                    'explanation_en': 'Checked types, string emptiness and positive numerical bounds.',
                    'hint_sk': 'Over isinstance(pid, int) and pid > 0 a podobne pre nazov a cenu.',
                    'hint_en': 'Assert isinstance for each field.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'validuj_produkt({"id": 1, "nazov": "Klávesnica", "cena": 49.99})', 'expected_output': 'True', 'test_code': 'assert validuj_produkt({"id": 1, "nazov": "Klávesnica", "cena": 49.99}) is True', 'is_hidden': False},
                        {'input_data': 'validuj_produkt({"id": 0, "nazov": "Zlé ID", "cena": 10})', 'expected_output': 'False', 'test_code': 'assert validuj_produkt({"id": 0, "nazov": "Zlé ID", "cena": 10}) is False', 'is_hidden': False},
                        {'input_data': 'validuj_produkt({"id": 2, "nazov": "   ", "cena": 10})', 'expected_output': 'False', 'test_code': 'assert validuj_produkt({"id": 2, "nazov": "   ", "cena": 10}) is False', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Dátový čistič a dopĺňač predvolených hodnôt',
                    'title_en': 'Data Sanitizer & Default Value Filler',
                    'instructions_sk': (
                        "Napíš funkciu `ocisti_nastavenia(vstupny_dict)`:\n"
                        "Prijme slovník používateľských nastavení a vráti nový slovník, v ktorom:\n"
                        "- kľúč `tema` nastaví na hodnotu zo vstupu, ak je 'light' alebo 'dark', inak predvolí `'dark'`,\n"
                        "- kľúč `jazyk` nastaví na hodnotu zo vstupu, ak je 'sk' alebo 'en', inak predvolí `'sk'`,\n"
                        "- kľúč `notifikacie` nastaví na bool hodnotu zo vstupu, inak predvolí `True`."
                    ),
                    'instructions_en': 'Write function `ocisti_nastavenia(vstupny_dict)` sanitizing settings dict with defaults.',
                    'starter_code': 'def ocisti_nastavenia(vstupny_dict):\n    # Dopln predvolené hodnoty\n    pass\n',
                    'solution_code': (
                        'def ocisti_nastavenia(vstupny_dict):\n'
                        '    d = vstupny_dict or {}\n'
                        '    tema = d.get("tema")\n'
                        '    jazyk = d.get("jazyk")\n'
                        '    notif = d.get("notifikacie")\n'
                        '    return {\n'
                        '        "tema": tema if tema in ("light", "dark") else "dark",\n'
                        '        "jazyk": jazyk if jazyk in ("sk", "en") else "sk",\n'
                        '        "notifikacie": bool(notif) if isinstance(notif, bool) else True\n'
                        '    }\n'
                    ),
                    'explanation_sk': 'Bezpečne sme skontrolovali povolené hodnoty a priradili defaulty.',
                    'explanation_en': 'Validated whitelist options and applied sensible defaults.',
                    'hint_sk': 'Použi ternárny operátor x if x in ("light", "dark") else "dark".',
                    'hint_en': 'Use ternary fallback expressions.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'ocisti_nastavenia({"tema": "light", "jazyk": "en"})',
                            'expected_output': "{'tema': 'light', 'jazyk': 'en', 'notifikacie': True}",
                            'test_code': 'assert ocisti_nastavenia({"tema": "light", "jazyk": "en"}) == {"tema": "light", "jazyk": "en", "notifikacie": True}',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'ocisti_nastavenia({})',
                            'expected_output': "{'tema': 'dark', 'jazyk': 'sk', 'notifikacie': True}",
                            'test_code': 'assert ocisti_nastavenia({}) == {"tema": "dark", "jazyk": "sk", "notifikacie": True}',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Spracovanie REST API odpovedí a chybových stavov',
            'title_en': 'REST API Response Structures & Error Handling',
            'summary_sk': 'HTTP status kódy (200, 201, 400, 401, 404, 500), formát envelopes {status, data, error} a paginácia.',
            'summary_en': 'HTTP status codes, response envelopes, pagination metadata and error parsing.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 14.3 Štruktúry REST API odpovedí

REST API komunikácia štandardne vracia odpovede vo formáte tzv. **Envelope pattern**:

#### Úspešná odpoveď (HTTP 200 OK):
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "student_id": 42,
    "xp": 1500
  },
  "pagination": {
    "page": 1,
    "total_pages": 5
  }
}
```

#### Chybová odpoveď (HTTP 404 Not Found / 400 Bad Request):
```json
{
  "status": "error",
  "code": 404,
  "error": {
    "message": "Cvičenie s ID 999 neexistuje.",
    "code": "EXERCISE_NOT_FOUND"
  }
}
```
""",
            'content_en': """### 14.3 REST API Payloads & Envelopes

Handle REST API response structures, error codes and paginated items.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorý rozsah trojciferných HTTP kódov označuje úspešné vybavenie požiadavky serverom?',
                    'question_en': 'Which HTTP status code range indicates success?',
                    'option_a_sk': '200 – 299', 'option_a_en': '200 – 299',
                    'option_b_sk': '400 – 499', 'option_b_en': '400 – 499',
                    'option_c_sk': '500 – 599', 'option_c_en': '500 – 599',
                    'option_d_sk': '100 – 199', 'option_d_en': '100 – 199',
                    'correct_option': 'A',
                    'explanation_sk': 'Kódy 2xx (200 OK, 201 Created, 204 No Content) indikujú úspech.',
                    'explanation_en': '2xx HTTP codes designate successful requests.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Zostavenie štandardnej REST API odpovede',
                    'title_en': 'Build Standard REST API Envelope',
                    'instructions_sk': 'Napíš funkciu `vytvor_api_odpoved(data, status_kod=200)`, ktorá vráti slovník v tvare `{"status": "success" ak status_kod < 400 else "error", "code": status_kod, "payload": data}`.',
                    'instructions_en': 'Write function `vytvor_api_odpoved(data, status_kod=200)` returning standard API dictionary response envelope.',
                    'starter_code': 'def vytvor_api_odpoved(data, status_kod=200):\n    # Vytvor obálku odpovede\n    pass\n',
                    'solution_code': (
                        'def vytvor_api_odpoved(data, status_kod=200):\n'
                        '    status = "success" if status_kod < 400 else "error"\n'
                        '    return {"status": status, "code": status_kod, "payload": data}\n'
                    ),
                    'explanation_sk': 'Podľa status_kod sme určili status a zostavili slovník.',
                    'explanation_en': 'Determined success/error status and assembled dict.',
                    'hint_sk': 'Použi "success" if status_kod < 400 else "error".',
                    'hint_en': 'Use ternary to set success or error.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vytvor_api_odpoved({"id": 1}, 200)', 'expected_output': "{'status': 'success', 'code': 200, 'payload': {'id': 1}}", 'test_code': 'assert vytvor_api_odpoved({"id": 1}, 200) == {"status": "success", "code": 200, "payload": {"id": 1}}', 'is_hidden': False},
                        {'input_data': 'vytvor_api_odpoved("Not found", 404)', 'expected_output': "{'status': 'error', 'code': 404, 'payload': 'Not found'}", 'test_code': 'assert vytvor_api_odpoved("Not found", 404) == {"status": "error", "code": 404, "payload": "Not found"}', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Extrakcia položiek z paginovanej odpovede',
                    'title_en': 'Extract Items from Paginated Payload',
                    'instructions_sk': 'Napíš funkciu `ziskaj_polozky_stranky(api_json_str)`, ktorá deserializuje JSON reťazec paginovanej odpovede a vráti dvojicu `(items, has_next)`. Kľúč `items` je zoznam a `has_next` je boolean (porovnanie `current_page < total_pages`). Ak kľúče chýbajú, vráti `([], False)`.',
                    'instructions_en': 'Write function `ziskaj_polozky_stranky(api_json_str)` returning `(items, has_next)` from paginated payload.',
                    'starter_code': 'import json\n\ndef ziskaj_polozky_stranky(api_json_str):\n    # Extrahuje items a boolean has_next\n    pass\n',
                    'solution_code': (
                        'import json\n\n'
                        'def ziskaj_polozky_stranky(api_json_str):\n'
                        '    try:\n'
                        '        d = json.loads(api_json_str)\n'
                        '        items = d.get("items", [])\n'
                        '        page = d.get("page", 1)\n'
                        '        total_pages = d.get("total_pages", 1)\n'
                        '        return (items, page < total_pages)\n'
                        '    except Exception:\n'
                        '        return ([], False)\n'
                    ),
                    'explanation_sk': 'Parsovali sme JSON, vytiahli items a porovnali page < total_pages.',
                    'explanation_en': 'Parsed JSON, extracted items list and verified page < total_pages.',
                    'hint_sk': 'Použi d.get("items", []) a porovnaj d.get("page") < d.get("total_pages").',
                    'hint_en': 'Extract items and compare page with total_pages.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'ziskaj_polozky_stranky(\'{"items": [1, 2], "page": 1, "total_pages": 3}\')', 'expected_output': '([1, 2], True)', 'test_code': 'assert ziskaj_polozky_stranky(\'{"items": [1, 2], "page": 1, "total_pages": 3}\') == ([1, 2], True)', 'is_hidden': False},
                        {'input_data': 'ziskaj_polozky_stranky(\'{"items": [3], "page": 3, "total_pages": 3}\')', 'expected_output': '([3], False)', 'test_code': 'assert ziskaj_polozky_stranky(\'{"items": [3], "page": 3, "total_pages": 3}\') == ([3], False)', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Unifikovaný parser chybových správ',
                    'title_en': 'Unified REST Error Message Parser',
                    'instructions_sk': (
                        "Rôzne REST API vracajú chybové správy v rôznych štruktúrach:\n"
                        "1. `{'error': 'Text chyby'}`\n"
                        "2. `{'error': {'message': 'Text chyby'}}`\n"
                        "3. `{'detail': 'Text chyby'}`\n"
                        "4. `{'errors': ['Prvá chyba', 'Druhá chyba']}`\n"
                        "Napíš funkciu `ziskaj_chybovu_spravu(api_dict)`, ktorá zanalyzuje slovník a vráti reťazec chyby. Ak žiadny tvar nesedí, vráti `'Neznáma chyba'`."
                    ),
                    'instructions_en': 'Write function `ziskaj_chybovu_spravu(api_dict)` normalizing errors from diverse API schemas.',
                    'starter_code': 'def ziskaj_chybovu_spravu(api_dict):\n    # Nájdi chybovú správu v slovníku\n    pass\n',
                    'solution_code': (
                        'def ziskaj_chybovu_spravu(api_dict):\n'
                        '    if not isinstance(api_dict, dict):\n'
                        '        return "Neznáma chyba"\n'
                        '    err = api_dict.get("error")\n'
                        '    if isinstance(err, str):\n'
                        '        return err\n'
                        '    if isinstance(err, dict) and "message" in err:\n'
                        '        return str(err["message"])\n'
                        '    if "detail" in api_dict and isinstance(api_dict["detail"], str):\n'
                        '        return api_dict["detail"]\n'
                        '    errors = api_dict.get("errors")\n'
                        '    if isinstance(errors, list) and len(errors) > 0:\n'
                        '        return str(errors[0])\n'
                        '    return "Neznáma chyba"\n'
                    ),
                    'explanation_sk': 'Postupne sme otestovali všetky 4 bežné REST formáty chýb.',
                    'explanation_en': 'Sequentially tested all 4 standard REST error envelope patterns.',
                    'hint_sk': 'Postupne over err ako str, err["message"], detail a errors[0].',
                    'hint_en': 'Check error string, error.message, detail, and errors[0].',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'ziskaj_chybovu_spravu({"error": "Prístup odopretý"})', 'expected_output': '"Prístup odopretý"', 'test_code': 'assert ziskaj_chybovu_spravu({"error": "Prístup odopretý"}) == "Prístup odopretý"', 'is_hidden': False},
                        {'input_data': 'ziskaj_chybovu_spravu({"error": {"message": "Token exspiroval"}})', 'expected_output': '"Token exspiroval"', 'test_code': 'assert ziskaj_chybovu_spravu({"error": {"message": "Token exspiroval"}}) == "Token exspiroval"', 'is_hidden': False},
                        {'input_data': 'ziskaj_chybovu_spravu({"errors": ["Prvý", "Druhý"]})', 'expected_output': '"Prvý"', 'test_code': 'assert ziskaj_chybovu_spravu({"errors": ["Prvý", "Druhý"]}) == "Prvý"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Dátová analytika a agregácia z JSON datasetu',
            'title_en': 'Data Analytics & Aggregation on JSON Datasets',
            'summary_sk': 'Spracovanie rozsiahlych datasetov, filtrovanie, výpočty metrik, generovanie sumárnych reportov.',
            'summary_en': 'Large dataset processing, filtering, KPI calculations, and summary report generation.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 14.4 Dátová analytika nad JSON datasetmi

Python je špičkovým jazykom pre dátovú analytiku. V tejto lekcii sa naučíme z agregovaného JSON datasetu vypočítať kľúčové metriky (KPI).

```python
dataset = [
    {"produkt": "Monitor 4K", "kategoria": "Elektronika", "cena": 350.0, "kusov": 3},
    {"produkt": "Myš", "kategoria": "Elektronika", "cena": 25.0, "kusov": 10},
    {"produkt": "Stôl", "kategoria": "Nábytok", "cena": 150.0, "kusov": 2}
]

# Výpočet celkových tržieb
trzby = sum(item["cena"] * item["kusov"] for item in dataset)
print("Celkové tržby:", trzby)
```
""",
            'content_en': """### 14.4 JSON Analytics & Metric Extraction

Calculate sums, averages and categorical KPIs from in-memory JSON data collections.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je najčistejší spôsob výpočtu celkovej sumy cien položiek v zozname slovníkov `items`?',
                    'question_en': 'What is the most idiomatic way to sum item prices in list of dicts?',
                    'option_a_sk': 'sum(x["cena"] for x in items)', 'option_a_en': 'sum(x["cena"] for x in items)',
                    'option_b_sk': 'items.sum("cena")', 'option_b_en': 'items.sum("cena")',
                    'option_c_sk': 'for cyklus s globálnou premennou', 'option_c_en': 'for loop with global variable',
                    'option_d_sk': 'json.sum(items)', 'option_d_en': 'json.sum(items)',
                    'correct_option': 'A',
                    'explanation_sk': 'Generátorový výraz odovzdaný do vstavanej funkcie sum() je rýchly a pamäťovo efektívny.',
                    'explanation_en': 'Generator expression passed to sum() is idiomatic and memory efficient.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Celkový objem finančných transakcií',
                    'title_en': 'Total Transaction Volume',
                    'instructions_sk': 'Napíš funkciu `spocitaj_transakcie(transakcie_zoznam)`, kde každá položka má kľúč `"suma"` (číslo). Funkcia vráti celkový súčet zaokrúhlený na 2 desatinné miesta.',
                    'instructions_en': 'Write function `spocitaj_transakcie(transakcie_zoznam)` returning total rounded sum of `"suma"` values.',
                    'starter_code': 'def spocitaj_transakcie(transakcie_zoznam):\n    # Spočítaj sumu transakcií\n    pass\n',
                    'solution_code': 'def spocitaj_transakcie(transakcie_zoznam):\n    return round(sum(item.get("suma", 0.0) for item in transakcie_zoznam), 2)\n',
                    'explanation_sk': 'Použili sme sum s generátorovým výrazom a zaokrúhlili na 2 miesta.',
                    'explanation_en': 'Summed items using generator and rounded to 2 places.',
                    'hint_sk': 'Použi round(sum(x.get("suma", 0.0) for x in transakcie_zoznam), 2).',
                    'hint_en': 'Use sum generator and round.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'spocitaj_transakcie([{"suma": 10.5}, {"suma": 20.25}])', 'expected_output': '30.75', 'test_code': 'assert spocitaj_transakcie([{"suma": 10.5}, {"suma": 20.25}]) == 30.75', 'is_hidden': False},
                        {'input_data': 'spocitaj_transakcie([])', 'expected_output': '0.0', 'test_code': 'assert spocitaj_transakcie([]) == 0.0', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Kľúčové metriky e-shopu (KPI Summary)',
                    'title_en': 'E-Shop Key Performance Indicators (KPI)',
                    'instructions_sk': (
                        "Napíš funkciu `analyzuj_objednavky(objednavky)`:\n"
                        "Každá objednávka obsahuje kľúče `id` a `suma`.\n"
                        "Funkcia vráti slovník v tvare:\n"
                        "`{'pocet': int, 'celkovo': float, 'priemer': float, 'max': float}`.\n"
                        "Čísla zaokrúhli na 2 desatinné miesta. Ak je zoznam prázdny, vráti `{'pocet': 0, 'celkovo': 0.0, 'priemer': 0.0, 'max': 0.0}`."
                    ),
                    'instructions_en': 'Write function `analyzuj_objednavky(objednavky)` returning count, total, average, and max order values.',
                    'starter_code': 'def analyzuj_objednavky(objednavky):\n    # Vypočítaj metriky\n    pass\n',
                    'solution_code': (
                        'def analyzuj_objednavky(objednavky):\n'
                        '    if not objednavky:\n'
                        '        return {"pocet": 0, "celkovo": 0.0, "priemer": 0.0, "max": 0.0}\n'
                        '    sumy = [float(x.get("suma", 0.0)) for x in objednavky]\n'
                        '    celkovo = sum(sumy)\n'
                        '    pocet = len(sumy)\n'
                        '    return {\n'
                        '        "pocet": pocet,\n'
                        '        "celkovo": round(celkovo, 2),\n'
                        '        "priemer": round(celkovo / pocet, 2),\n'
                        '        "max": round(max(sumy), 2)\n'
                        '    }\n'
                    ),
                    'explanation_sk': 'Vypočítali sme sum, len, avg a max s ošetrením prázdneho vstupu.',
                    'explanation_en': 'Calculated count, sum, average, and max with empty dataset handling.',
                    'hint_sk': 'Ošetri prázdny zoznam if not objednavky a použi sum(), max() a delenie.',
                    'hint_en': 'Guard against empty list, compute sum, len, max.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'analyzuj_objednavky([{"id": 1, "suma": 100.0}, {"id": 2, "suma": 50.0}])',
                            'expected_output': "{'pocet': 2, 'celkovo': 150.0, 'priemer': 75.0, 'max': 100.0}",
                            'test_code': 'assert analyzuj_objednavky([{"id": 1, "suma": 100.0}, {"id": 2, "suma": 50.0}]) == {"pocet": 2, "celkovo": 150.0, "priemer": 75.0, "max": 100.0}',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'analyzuj_objednavky([])',
                            'expected_output': "{'pocet': 0, 'celkovo': 0.0, 'priemer': 0.0, 'max': 0.0}",
                            'test_code': 'assert analyzuj_objednavky([]) == {"pocet": 0, "celkovo": 0.0, "priemer": 0.0, "max": 0.0}',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Kategorizácia a hľadanie najvýnosnejšej kategórie',
                    'title_en': 'Category Aggregation & Top Category Finder',
                    'instructions_sk': (
                        "Napíš funkciu `najlepsia_kategoria(predaje)`:\n"
                        "Zoznam obsahuje položky `[{'kategoria': str, 'trzba': float}, ...]`.\n"
                        "Funkcia spočíta celkovú tržbu pre každú kategóriu a vráti dvojicu `(nazov_top_kategorie, celkova_trzba_zaokruhlena_na_2_desatinne)`.\n"
                        "Ak je zoznam prázdny, vráti `(None, 0.0)`."
                    ),
                    'instructions_en': 'Write function `najlepsia_kategoria(predaje)` aggregating revenue by category and returning `(top_category, total_revenue)`.',
                    'starter_code': 'def najlepsia_kategoria(predaje):\n    # Nájdi kategóriu s najvyššou tržbou\n    pass\n',
                    'solution_code': (
                        'def najlepsia_kategoria(predaje):\n'
                        '    if not predaje:\n'
                        '        return (None, 0.0)\n'
                        '    kategorie = {}\n'
                        '    for p in predaje:\n'
                        '        kat = p.get("kategoria", "Ostatné")\n'
                        '        trzba = float(p.get("trzba", 0.0))\n'
                        '        kategorie[kat] = kategorie.get(kat, 0.0) + trzba\n'
                        '    top_kat = max(kategorie.items(), key=lambda item: item[1])\n'
                        '    return (top_kat[0], round(top_kat[1], 2))\n'
                    ),
                    'explanation_sk': 'Agregovali sme tržby do slovníka a pomocou max(kategorie.items(), key=lambda ...) našli top.',
                    'explanation_en': 'Aggregated into dict and determined maximum key by revenue value.',
                    'hint_sk': 'Použi slovník na sčítanie tržieb a max(kategorie.items(), key=lambda x: x[1]).',
                    'hint_en': 'Use dict accumulator and max with lambda key.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'najlepsia_kategoria([{"kategoria": "Knihy", "trzba": 40.0}, {"kategoria": "Elektronika", "trzba": 300.0}, {"kategoria": "Knihy", "trzba": 25.0}])',
                            'expected_output': "('Elektronika', 300.0)",
                            'test_code': 'assert najlepsia_kategoria([{"kategoria": "Knihy", "trzba": 40.0}, {"kategoria": "Elektronika", "trzba": 300.0}, {"kategoria": "Knihy", "trzba": 25.0}]) == ("Elektronika", 300.0)',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'najlepsia_kategoria([])',
                            'expected_output': '(None, 0.0)',
                            'test_code': 'assert najlepsia_kategoria([]) == (None, 0.0)',
                            'is_hidden': False
                        }
                    ]
                }
            ]
        }
    ]
}
