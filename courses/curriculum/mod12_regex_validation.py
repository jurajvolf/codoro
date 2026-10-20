"""
MODUL 12: Regulárne výrazy (re), validácia vstupov a parsovanie logov
Odhadovaný rozsah: 10 hodín | Náročnosť: INTERMEDIATE | Úroveň: FREE | Track: ALGORITHMS_AND_DATA
"""

MODULE_DATA = {
    'order': 12,
    'track': 'ALGORITHMS_AND_DATA',
    'title_sk': 'Regulárne výrazy (re), validácia vstupov a parsovanie logov',
    'title_en': 'Regular Expressions (re), Input Validation & Log Parsing',
    'description_sk': 'Nauč sa pracovať s knižnicou re: metódy search, match, findall, sub, regulárne vzory, znakové triedy, kvantifikátory, validácia e-mailov, telefónov, IBAN a parsovanie systémových logov.',
    'description_en': 'Master Python re module: search, match, findall, sub, patterns, quantifiers, character classes, email, phone and IBAN validation, and log parsing with capture groups.',
    'programming_language': 'python',
    'estimated_hours': 10,
    'difficulty_level': 'INTERMEDIATE',
    'is_pro_only': False,
    'icon_name': 'search',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Základy regexu v Pythone: modul re a vyhľadávanie vzorov',
            'title_en': 'Regex Fundamentals in Python: re module & Pattern Search',
            'summary_sk': 'Úvod do modulu re, raw stringy r"", funkcie search(), match() a findall().',
            'summary_en': 'Introduction to re module, raw strings r"", functions search(), match() and findall().',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 12.1 Úvod do regulárnych výrazov v Pythone

Regulárny výraz (skrátene **Regex**) je reťazec definujúci vyhľadávací vzor. V Pythone sa na prácu s regexmi používa vstavaný modul `re`.

#### Raw reťazce (`r"..."`)
Pri zápise regulárnych výrazov vždy používame tzv. **raw reťazce** s prefixom `r`. Tým zamedzíme nechcenej interpretácii spätných lomiek (`\\`) ako escape sekvencií Pythonu:

```python
import re

# Správny zápis pre regex hľadajúci číslicu
pattern = r"\\d+"
```

#### Prehľad základných funkcií modulu `re`:
| Funkcia | Účel | Návratová hodnota |
| :--- | :--- | :--- |
| `re.search(pattern, text)` | Nájde prvý výskyt vzoru kdekoľvek v texte | `Match` objekt alebo `None` |
| `re.match(pattern, text)` | Overí, či text začína vzorom od prvého znaku | `Match` objekt alebo `None` |
| `re.findall(pattern, text)`| Nájde všetky neprekrývajúce sa výskyty | Zoznam reťazcov `list[str]` |
| `re.sub(pattern, repl, text)`| Nahradí výskyty vzoru novým reťazcom | Upravený reťazec `str` |

#### Praktická ukážka vyhľadávania:
```python
import re

text = "Študent Juraj získal 95 bodov a Martin získal 88 bodov."

# Nájdenie všetkých čísel
body = re.findall(r"\\d+", text)
print(body)  # ['95', '88']

# Hľadanie prvého výskytu
match = re.search(r"(\\w+)\\s+získal", text)
if match:
    print("Meno:", match.group(1))  # 'Juraj'
```

> ⚠️ **Častá chyba na maturite:**
> Záména `re.match()` a `re.search()`. Funkcia `re.match()` testuje vzor **iba od úplného začiatku reťazca** (od indexu 0). Ak vzor leží v strede vety, `match()` vráti `None`, zatiaľ čo `search()` ho nájde kdekoľvek!
""",
            'content_en': """### 12.1 Regular Expressions in Python

A regular expression (Regex) is a sequence of characters that specifies a search pattern. In Python, regex operations are provided by the built-in `re` module.

Always use raw strings (`r"..."`) to prevent Python from interpreting backslashes as escape characters.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je rozdiel medzi `re.search()` a `re.match()`?',
                    'question_en': 'What is the difference between `re.search()` and `re.match()`?',
                    'option_a_sk': 're.match testuje iba začiatok reťazca, re.search hľadá v celom texte', 'option_a_en': 're.match only tests string start, re.search searches entire text',
                    'option_b_sk': 're.search vracia vždy zoznam, re.match vracia reťazec', 'option_b_en': 're.search returns list, re.match returns str',
                    'option_c_sk': 'Nie je v nich žiaden rozdiel', 'option_c_en': 'There is no difference',
                    'option_d_sk': 're.match ignoruje veľkosť písmen', 'option_d_en': 're.match is case-insensitive',
                    'correct_option': 'A',
                    'explanation_sk': 're.match() je zakotvený na začiatku reťazca, zatiaľ čo re.search() prehľadáva reťazec kdekoľvek.',
                    'explanation_en': 're.match() matches from start, re.search() finds pattern anywhere.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Extrakcia všetkých čísel z reťazca',
                    'title_en': 'Extract All Numbers from String',
                    'instructions_sk': 'Napíš funkciu `extrahuj_cisla(text)`, ktorá pomocou modulu `re` nájde všetky celočíselné hodnoty v texte a vráti ich ako zoznam celých čísel `list[int]`.',
                    'instructions_en': 'Write function `extrahuj_cisla(text)` that extracts all integer values using `re` and returns `list[int]`.',
                    'starter_code': 'import re\n\ndef extrahuj_cisla(text):\n    # Nájdi všetky čísla a preveď na int\n    pass\n',
                    'solution_code': 'import re\n\ndef extrahuj_cisla(text):\n    return [int(x) for x in re.findall(r"\\d+", text)]\n',
                    'explanation_sk': 'Použili sme re.findall(r"\\d+", text) a previedli nájdené reťazce na celé čísla int.',
                    'explanation_en': 'We used re.findall(r"\\d+", text) and converted matching substrings to integers.',
                    'hint_sk': 'Použi re.findall(r"\\d+", text) a list comprehension [int(x) for x in ...].',
                    'hint_en': 'Use re.findall(r"\\d+", text) and [int(x) for x in ...].',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'extrahuj_cisla("Cena 15 EUR a zľava 3 EUR")', 'expected_output': '[15, 3]', 'test_code': 'assert extrahuj_cisla("Cena 15 EUR a zľava 3 EUR") == [15, 3]', 'is_hidden': False},
                        {'input_data': 'extrahuj_cisla("Žiadne hodnoty")', 'expected_output': '[]', 'test_code': 'assert extrahuj_cisla("Žiadne hodnoty") == []', 'is_hidden': False},
                        {'input_data': 'extrahuj_cisla("Rok 2027 mesiac 4 deň 15")', 'expected_output': '[2027, 4, 15]', 'test_code': 'assert extrahuj_cisla("Rok 2027 mesiac 4 deň 15") == [2027, 4, 15]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Hľadanie výskytu kľúčového slova',
                    'title_en': 'Find Keyword Occurrence',
                    'instructions_sk': 'Napíš funkciu `obsahuje_chybu(log_riadok)`, ktorá vráti `True`, ak reťazec obsahuje slovo "ERROR" alebo "CRITICAL" (case-insensitive, t. j. bez ohľadu na veľkosť písmen), inak vráti `False`.',
                    'instructions_en': 'Write function `obsahuje_chybu(log_riadok)` returning `True` if it contains "ERROR" or "CRITICAL" case-insensitively, else `False`.',
                    'starter_code': 'import re\n\ndef obsahuje_chybu(log_riadok):\n    # Over výskyt ERROR alebo CRITICAL\n    pass\n',
                    'solution_code': 'import re\n\ndef obsahuje_chybu(log_riadok):\n    return bool(re.search(r"\\b(ERROR|CRITICAL)\\b", log_riadok, re.IGNORECASE))\n',
                    'explanation_sk': 'Použili sme re.search s príznakom re.IGNORECASE a ohraničením slova \\b.',
                    'explanation_en': 'We used re.search with re.IGNORECASE flag and word boundaries \\b.',
                    'hint_sk': 'Použi re.search(r"\\b(ERROR|CRITICAL)\\b", log_riadok, re.IGNORECASE).',
                    'hint_en': 'Use re.search(r"\\b(ERROR|CRITICAL)\\b", log_riadok, re.IGNORECASE).',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'obsahuje_chybu("[2026-10-20] [error] connection failed")', 'expected_output': 'True', 'test_code': 'assert obsahuje_chybu("[2026-10-20] [error] connection failed") is True', 'is_hidden': False},
                        {'input_data': 'obsahuje_chybu("[2026-10-20] [INFO] system running")', 'expected_output': 'False', 'test_code': 'assert obsahuje_chybu("[2026-10-20] [INFO] system running") is False', 'is_hidden': False},
                        {'input_data': 'obsahuje_chybu("CRITICAL database timeout")', 'expected_output': 'True', 'test_code': 'assert obsahuje_chybu("CRITICAL database timeout") is True', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Cenzúra citlivých údajov (re.sub)',
                    'title_en': 'Sanitize Sensitive Digits (re.sub)',
                    'instructions_sk': 'Napíš funkciu `cenzuruj_rodne_cisla(text)`, ktorá nahradí všetky 6- až 10-ciferné číselné postupnosti (oddelené prípadne lomítkom, napr. 050412/1234 alebo 0504121234) reťazcom `[CENZUROVANÉ]`.',
                    'instructions_en': 'Write function `cenzuruj_rodne_cisla(text)` replacing 6 to 10 digit sequences with optional slash by `[CENZUROVANÉ]`.',
                    'starter_code': 'import re\n\ndef cenzuruj_rodne_cisla(text):\n    # Nahraď rodné čísla pomocou re.sub\n    pass\n',
                    'solution_code': 'import re\n\ndef cenzuruj_rodne_cisla(text):\n    return re.sub(r"\\b\\d{6}/?\\d{3,4}\\b", "[CENZUROVANÉ]", text)\n',
                    'explanation_sk': 'Použili sme re.sub so vzorom \\b\\d{6}/?\\d{3,4}\\b, ktorý presne pokrýva formát rodného čísla.',
                    'explanation_en': 'We used re.sub with regex matching national ID number format.',
                    'hint_sk': 'Použi re.sub(r"\\b\\d{6}/?\\d{3,4}\\b", "[CENZUROVANÉ]", text).',
                    'hint_en': 'Use re.sub(r"\\b\\d{6}/?\\d{3,4}\\b", "[CENZUROVANÉ]", text).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'cenzuruj_rodne_cisla("Klient s RC 050412/1234 overený.")', 'expected_output': '"Klient s RC [CENZUROVANÉ] overený."', 'test_code': 'assert cenzuruj_rodne_cisla("Klient s RC 050412/1234 overený.") == "Klient s RC [CENZUROVANÉ] overený."', 'is_hidden': False},
                        {'input_data': 'cenzuruj_rodne_cisla("Kód objednávky 42")', 'expected_output': '"Kód objednávky 42"', 'test_code': 'assert cenzuruj_rodne_cisla("Kód objednávky 42") == "Kód objednávky 42"', 'is_hidden': False},
                        {'input_data': 'cenzuruj_rodne_cisla("RC 9912314321 bez lomitka")', 'expected_output': '"RC [CENZUROVANÉ] bez lomitka"', 'test_code': 'assert cenzuruj_rodne_cisla("RC 9912314321 bez lomitka") == "RC [CENZUROVANÉ] bez lomitka"', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Znakové triedy, kvantifikátory a metaznaky',
            'title_en': 'Character Classes, Quantifiers & Metacharacters',
            'summary_sk': 'Znakové triedy [], negácia [^], kvantifikátory *, +, ?, {m,n} a kotvy ^ a $.',
            'summary_en': 'Character classes [], negation [^], quantifiers *, +, ?, {m,n} and anchors ^ and $.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 12.2 Znakové triedy a kvantifikátory

#### Špeciálne sekvencie
- `\\d` – akákoľvek číslica `[0-9]`
- `\\D` – akýkoľvek znak okrem číslice `[^0-9]`
- `\\w` – alfanumerický znak (písmeno, číslo, podtržník) `[a-zA-Z0-9_]`
- `\\s` – biely znak (medzera, tabulátor, nový riadok) `[ \\t\\n\\r]`
- `.` – akýkoľvek znak okrem nového riadku

#### Kvantifikátory (počty opakovaní)
| Kvantifikátor | Význam | Príklad |
| :--- | :--- | :--- |
| `*` | 0 alebo viackrát (chamtivý) | `a*` nájde "", "a", "aaa" |
| `+` | 1 alebo viackrát | `a+` nájde "a", "aaa" |
| `?` | 0 alebo 1-krát (voliteľný) | `https?` nájde "http" aj "https" |
| `{n}` | Presne n-krát | `\\d{4}` nájde rok "2027" |
| `{min,max}` | V rozsahu min až max | `\\w{3,8}` nájde slovo dĺžky 3 až 8 |

```python
import re

# Nájdenie slov začínajúcich veľkým písmenom
text = "Bratislava je hlavné mesto Slovenska."
mena = re.findall(r"\\b[A-ZÁČĎÉÍĽŇÓŠŤÚÝŽ][a-záčďéíľňóšťúýž]+\\b", text)
print(mena)  # ['Bratislava', 'Slovenska']
```

> ⚠️ **Častá chyba na maturite:**
> Pozor na "chamtivosť" (greedy) kvantifikátorov `*` a `+`. Štandardne zaberú najdlhší možný úsek textu. Ak chceme negreedy (lazy) režim, pridáme za kvantifikátor otáznik: `.*?`.
""",
            'content_en': """### 12.2 Character Classes & Quantifiers

Master \\d, \\w, \\s, character sets [], and repeat counts {m,n}, *, +, ?.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo označuje kvantifikátor `\\d{4}` v regulárnom výraze?',
                    'question_en': 'What does `\\d{4}` specify in a regex?',
                    'option_a_sk': 'Presne štyri číslice za sebou', 'option_a_en': 'Exactly four digits in sequence',
                    'option_b_sk': 'Najviac štyri číslice', 'option_b_en': 'At most four digits',
                    'option_c_sk': 'Číslo štyri', 'option_c_en': 'The number four',
                    'option_d_sk': 'Štyri ľubovoľné písmená', 'option_d_en': 'Four arbitrary letters',
                    'correct_option': 'A',
                    'explanation_sk': '{4} vyžaduje presne 4 opakovania predchádzajúceho znaku/triedy.',
                    'explanation_en': '{4} requires exactly 4 occurrences of the preceding element.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Extrakcia hashtagov zo sociálnej siete',
                    'title_en': 'Extract Hashtags from Text',
                    'instructions_sk': 'Napíš funkciu `extrahuj_hashtagy(text)`, ktorá nájde všetky hashtagy začínajúce znakom `#` nasledovaným aspoň jedným alfanumerickým znakom `[a-zA-Z0-9_]`. Vráti zoznam nájdených reťazcov vrátane mriežky.',
                    'instructions_en': 'Write function `extrahuj_hashtagy(text)` returning all hashtags starting with `#` followed by alnum chars.',
                    'starter_code': 'import re\n\ndef extrahuj_hashtagy(text):\n    # Nájdi hashtagy\n    pass\n',
                    'solution_code': 'import re\n\ndef extrahuj_hashtagy(text):\n    return re.findall(r"#[a-zA-Z0-9_]+", text)\n',
                    'explanation_sk': 'Vzor #[a-zA-Z0-9_]+ alebo #\\w+ zachytí mriežku a nasledujúce znaky.',
                    'explanation_en': 'Pattern #[a-zA-Z0-9_]+ captures hash and trailing word chars.',
                    'hint_sk': 'Použi re.findall(r"#[a-zA-Z0-9_]+", text).',
                    'hint_en': 'Use re.findall(r"#[a-zA-Z0-9_]+", text).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'extrahuj_hashtagy("Učím sa #python a #codoro_2027")', 'expected_output': "['#python', '#codoro_2027']", 'test_code': 'assert extrahuj_hashtagy("Učím sa #python a #codoro_2027") == ["#python", "#codoro_2027"]', 'is_hidden': False},
                        {'input_data': 'extrahuj_hashtagy("Text bez označenia")', 'expected_output': '[]', 'test_code': 'assert extrahuj_hashtagy("Text bez označenia") == []', 'is_hidden': False},
                        {'input_data': 'extrahuj_hashtagy("#maturita #2027")', 'expected_output': "['#maturita', '#2027']", 'test_code': 'assert extrahuj_hashtagy("#maturita #2027") == ["#maturita", "#2027"]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Validácia PSČ Slovenskej republiky',
                    'title_en': 'Slovak Postal Code Validator',
                    'instructions_sk': 'Napíš funkciu `je_platne_psc(psc_str)`, ktorá overí, či je zadaný reťazec platným slovenským PSČ: 5 číslic, voliteľne rozdelených medzerou za 3. číslicou (napr. "02743" alebo "027 43"). Reťazec nesmie obsahovať žiadne znaky navyše pred ani za kódom.',
                    'instructions_en': 'Write function `je_platne_psc(psc_str)` validating Slovak zip codes (5 digits with optional space after 3rd digit).',
                    'starter_code': 'import re\n\ndef je_platne_psc(psc_str):\n    # Over formát PSČ\n    pass\n',
                    'solution_code': 'import re\n\ndef je_platne_psc(psc_str):\n    return bool(re.fullmatch(r"\\d{3}\\s?\\d{2}", psc_str.strip()))\n',
                    'explanation_sk': 'Použili sme re.fullmatch s kotvením na celý reťazec a voliteľnou medzerou \\s?.',
                    'explanation_en': 'We used re.fullmatch with optional whitespace \\s?.',
                    'hint_sk': 'Použi re.fullmatch(r"\\d{3}\\s?\\d{2}", psc_str.strip()).',
                    'hint_en': 'Use re.fullmatch(r"\\d{3}\\s?\\d{2}", psc_str.strip()).',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'je_platne_psc("027 43")', 'expected_output': 'True', 'test_code': 'assert je_platne_psc("027 43") is True', 'is_hidden': False},
                        {'input_data': 'je_platne_psc("02743")', 'expected_output': 'True', 'test_code': 'assert je_platne_psc("02743") is True', 'is_hidden': False},
                        {'input_data': 'je_platne_psc("1234")', 'expected_output': 'False', 'test_code': 'assert je_platne_psc("1234") is False', 'is_hidden': False},
                        {'input_data': 'je_platne_psc("027 435")', 'expected_output': 'False', 'test_code': 'assert je_platne_psc("027 435") is False', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Extrakcia hodnôt HTML značiek',
                    'title_en': 'Extract HTML Tag Values',
                    'instructions_sk': 'Napíš funkciu `extrahuj_odkazy(html_text)`, ktorá pomocou regexu nájde všetky hodnoty atribútu `href="..."` v HTML texte a vráti ich ako zoznam URL reťazcov.',
                    'instructions_en': 'Write function `extrahuj_odkazy(html_text)` extracting all `href="..."` URLs.',
                    'starter_code': 'import re\n\ndef extrahuj_odkazy(html_text):\n    # Nájdi URL adresy v href\n    pass\n',
                    'solution_code': 'import re\n\ndef extrahuj_odkazy(html_text):\n    return re.findall(r\'href=["\\\'](.*?)["\\\']\', html_text)\n',
                    'explanation_sk': 'Použili sme re.findall s lazy kvantifikátorom (.*?) v úvodzovkách.',
                    'explanation_en': 'We used re.findall with lazy capture (.*?) inside quotes.',
                    'hint_sk': 'Použi re.findall(r\'href=["\\\'](.*?)["\\\']\', html_text).',
                    'hint_en': 'Use re.findall with non-greedy capture group.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'extrahuj_odkazy(\'<a href="https://codoro.sk">Home</a> a <a href="https://python.org">Python</a>\')', 'expected_output': "['https://codoro.sk', 'https://python.org']", 'test_code': 'assert extrahuj_odkazy(\'<a href="https://codoro.sk">Home</a> a <a href="https://python.org">Python</a>\') == ["https://codoro.sk", "https://python.org"]', 'is_hidden': False},
                        {'input_data': 'extrahuj_odkazy("<p>Bez linku</p>")', 'expected_output': '[]', 'test_code': 'assert extrahuj_odkazy("<p>Bez linku</p>") == []', 'is_hidden': False},
                        {'input_data': 'extrahuj_odkazy("<link href=\'/static/style.css\'>")', 'expected_output': "['/static/style.css']", 'test_code': 'assert extrahuj_odkazy("<link href=\'/static/style.css\'>") == ["/static/style.css"]', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Validácia reálnych dát: e-maily, telefónne čísla a IBAN',
            'title_en': 'Production Data Validation: Emails, Phone Numbers & IBAN',
            'summary_sk': 'Kotvenie ^ a $, funkcia fullmatch(), validácia e-mailov podľa RFC, telefónnych čísel a bankových účtov IBAN.',
            'summary_en': 'Anchors ^ and $, fullmatch() method, email validation, Slovak phone numbers and IBAN accounts.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 12.3 Validácia produkčných formátov údajov

Pri webových formulároch a registráciách je nutné overiť správny formát zadaných údajov pred zápisom do databázy.

#### Funkcia `re.fullmatch()`
Funkcia `re.fullmatch(pattern, string)` overuje, či vzor zodpovedá **celému reťazcu od začiatku po koniec** (ekvivalent použitia kotiev `^` a `$`).

#### 1. Validácia e-mailu
```python
import re

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"

def je_email(text):
    return bool(re.fullmatch(EMAIL_REGEX, text.strip()))
```

#### 2. Validácia telefónneho čísla (SR)
Slovenské čísla majú buď formát `+421 9XX XXX XXX` alebo národný `09XX XXX XXX`:
```python
PHONE_REGEX = r"^(?:\\+421|0)\\s?9\\d{2}\\s?\\d{3}\\s?\\d{3}$"
```

#### 3. Slovenský IBAN (International Bank Account Number)
Slovenský IBAN má 24 znakov, začína kódom `SK` nasledovaným 22 číslicami:
```python
IBAN_REGEX = r"^SK\\d{22}$"
```

> ⚠️ **Častá chyba na maturite:**
> Zabudnutie na znak `^` (začiatok) a `$` (koniec) pri použití `re.search()`. Ak vzor neukotvíte, reťazec `"neplatny_email@domena.sk_a_dalsi_odpad"` by cez `search` prešiel ako platný! Preto na validáciu formulárov vždy používajte `re.fullmatch()`.
""",
            'content_en': """### 12.3 Real-World Form Validation

Use `re.fullmatch()` to assert the entire string satisfies the expression without trailing garbage.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo je na validáciu formulárových polí vhodnejšie použiť `re.fullmatch()` namiesto `re.search()`?',
                    'question_en': 'Why is `re.fullmatch()` preferred over `re.search()` for form inputs?',
                    'option_a_sk': 'Pretože overuje celý reťazec a nepovolí neplatný text pred ani za vzorom', 'option_a_en': 'It checks the entire string and rejects leading/trailing garbage',
                    'option_b_sk': 'Pretože fullmatch je 10× rýchlejší', 'option_b_en': 'Because fullmatch is 10x faster',
                    'option_c_sk': 'Pretože fullmatch automaticky šifruje dáta', 'option_c_en': 'Because it encrypts data',
                    'option_d_sk': 'Pretože search nefunguje s číslami', 'option_d_en': 'Search does not work with digits',
                    'correct_option': 'A',
                    'explanation_sk': 're.fullmatch() vyžaduje zhodu na 100 % dĺžky reťazca.',
                    'explanation_en': 're.fullmatch() guarantees whole-string adherence.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Validácia e-mailovej adresy',
                    'title_en': 'Validate Email Address',
                    'instructions_sk': 'Napíš funkciu `je_platny_email(email)`, ktorá pomocou `re.fullmatch` overí, či reťazec zodpovedá štandardnému tvaru e-mailu: používateľské meno (písmená, čísla, bodka, podtržník, pomlčka), zavináč `@`, doména 2. úrovne a koncovka s aspoň 2 písmenami.',
                    'instructions_en': 'Write function `je_platny_email(email)` validating standard email format via `re.fullmatch`.',
                    'starter_code': 'import re\n\ndef je_platny_email(email):\n    # Over e-mailovú adresu\n    pass\n',
                    'solution_code': 'import re\n\ndef je_platny_email(email):\n    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"\n    return bool(re.fullmatch(pattern, email.strip()))\n',
                    'explanation_sk': 'Použili sme re.fullmatch s overením používateľskej časti, zavináča, domény a TLD.',
                    'explanation_en': 'We used re.fullmatch with user, domain and top-level domain checks.',
                    'hint_sk': 'Použi vzor r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$".',
                    'hint_en': 'Use r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$".',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'je_platny_email("student@codoro.sk")', 'expected_output': 'True', 'test_code': 'assert je_platny_email("student@codoro.sk") is True', 'is_hidden': False},
                        {'input_data': 'je_platny_email("neplatny_email_bez_zavinaca.sk")', 'expected_output': 'False', 'test_code': 'assert je_platny_email("neplatny_email_bez_zavinaca.sk") is False', 'is_hidden': False},
                        {'input_data': 'je_platny_email("juraj.volf@skola.edu")', 'expected_output': 'True', 'test_code': 'assert je_platny_email("juraj.volf@skola.edu") is True', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Validácia a normalizácia telefónneho čísla',
                    'title_en': 'Validate & Normalize Phone Number',
                    'instructions_sk': 'Napíš funkciu `normalizuj_telefon(cislo_str)`, ktorá overí slovenské telefónne číslo vo formáte `+4219XXXXXXXX` alebo `09XXXXXXXX` (medzery ignoruje). Ak je číslo platné, vráti ho v medzinárodnom tvare `+4219XXXXXXXX` bez medzier. Ak je neplatné, vráti `None`.',
                    'instructions_en': 'Write function `normalizuj_telefon(cislo_str)` verifying Slovak numbers and returning `+4219XXXXXXXX` or `None`.',
                    'starter_code': 'import re\n\ndef normalizuj_telefon(cislo_str):\n    # Over a normalizuj na +421...\n    pass\n',
                    'solution_code': 'import re\n\ndef normalizuj_telefon(cislo_str):\n    cistene = re.sub(r"\\s+", "", cislo_str.strip())\n    if re.fullmatch(r"\\+4219\\d{8}", cistene):\n        return cistene\n    elif re.fullmatch(r"09\\d{8}", cistene):\n        return "+421" + cistene[1:]\n    return None\n',
                    'explanation_sk': 'Najprv sme odstránili medzery pomocou re.sub, overili dĺžku 9 číslic za predvoľbou a zjednotili na +421.',
                    'explanation_en': 'Stripped whitespaces, validated 9 digits following prefix and normalized to +421.',
                    'hint_sk': 'Odstráň medzery re.sub(r"\\s+", "", s) a over match r"\\+4219\\d{8}" alebo r"09\\d{8}".',
                    'hint_en': 'Remove spaces and match prefix variants.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'normalizuj_telefon("0905 123 456")', 'expected_output': '"+421905123456"', 'test_code': 'assert normalizuj_telefon("0905 123 456") == "+421905123456"', 'is_hidden': False},
                        {'input_data': 'normalizuj_telefon("+421 911 222 333")', 'expected_output': '"+421911222333"', 'test_code': 'assert normalizuj_telefon("+421 911 222 333") == "+421911222333"', 'is_hidden': False},
                        {'input_data': 'normalizuj_telefon("123456")', 'expected_output': 'None', 'test_code': 'assert normalizuj_telefon("123456") is None', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Validácia slovenského IBAN bankového účtu',
                    'title_en': 'Validate Slovak IBAN Bank Account',
                    'instructions_sk': 'Napíš funkciu `je_platny_sk_iban(iban_str)`, ktorá overí slovenský IBAN: začína reťazcom "SK" a nasleduje presne 22 číslic (medzery medzi blokmi po 4 znakoch sú povolené). Vráti `True` ak je kód platný, inak `False`.',
                    'instructions_en': 'Write function `je_platny_sk_iban(iban_str)` verifying SK IBAN (SK + 22 digits, spaces permitted).',
                    'starter_code': 'import re\n\ndef je_platny_sk_iban(iban_str):\n    # Over slovenský IBAN\n    pass\n',
                    'solution_code': 'import re\n\ndef je_platny_sk_iban(iban_str):\n    cisty = re.sub(r"\\s+", "", iban_str.strip().upper())\n    return bool(re.fullmatch(r"SK\\d{22}", cisty))\n',
                    'explanation_sk': 'Odstránili sme medzery, previedli na veľké písmená a overili vzor SK\\d{22}.',
                    'explanation_en': 'Sanitized spaces, uppercased and asserted SK\\d{22}.',
                    'hint_sk': 'Odstráň medzery re.sub(r"\\s+", "", s.upper()) a použi re.fullmatch(r"SK\\d{22}", s).',
                    'hint_en': 'Remove spaces, uppercase and check re.fullmatch(r"SK\\d{22}", s).',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'je_platny_sk_iban("SK31 1200 0000 0019 8742 6378")', 'expected_output': 'True', 'test_code': 'assert je_platny_sk_iban("SK31 1200 0000 0019 8742 6378") is True', 'is_hidden': False},
                        {'input_data': 'je_platny_sk_iban("CZ3112000000001987426378")', 'expected_output': 'False', 'test_code': 'assert je_platny_sk_iban("CZ3112000000001987426378") is False', 'is_hidden': False},
                        {'input_data': 'je_platny_sk_iban("SK123456")', 'expected_output': 'False', 'test_code': 'assert je_platny_sk_iban("SK123456") is False', 'is_hidden': True},
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Parsovanie systémových logov pomocou regex skupín',
            'title_en': 'Log Parsing with Regex Capture Groups',
            'summary_sk': 'Pomenované zachytávacie skupiny (?P<name>...), metóda groupdict() a analýza dát z logov.',
            'summary_en': 'Named capture groups (?P<name>...), groupdict() method, and security log parsing.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 12.4 Pomenované regex skupiny a parsovanie logov

Zachytávacie skupiny v zátvorkách `(...)` umožňujú z nájdeného reťazca vyňať jednotlivé sémantické časti.

#### Pomenované skupiny `(?P<nazov>...)`
Namiesto číslovania skupín indexmi `group(1)`, `group(2)` je v profesionálnej praxi štandardom pomenovať skupiny pomocou syntaxe `(?P<nazov_skupiny>...)`. Výsledok potom získame priamo ako slovník cez `.groupdict()`:

```python
import re

log_line = "2026-10-20 14:32:05 [WARNING] User jurvox: Failed login attempt"

pattern = r"^(?P<timestamp>\\d{4}-\\d{2}-\\d{2}\\s+\\d{2}:\\d{2}:\\d{2})\\s+\\[(?P<level>\\w+)\\]\\s+(?P<message>.*)$"

match = re.match(pattern, log_line)
if match:
    data = match.groupdict()
    print(data['timestamp'])  # '2026-10-20 14:32:05'
    print(data['level'])      # 'WARNING'
    print(data['message'])    # 'User jurvox: Failed login attempt'
```

#### Praktický význam v kyberbezpečnosti
Správcovia sietí a bezpečnostní analytici takto denne parsujú milióny záznamov webových serverov (Nginx, Apache), firewallov a SSH prístupov s cieľom odhaliť pokusy o brute-force útok alebo SQL Injection.
""",
            'content_en': """### 12.4 Named Capture Groups & Log Analysis

Use `(?P<key>...)` and `.groupdict()` for robust parsing of system logs and telemetry.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá metóda Match objektu vráti všetky pomenované skupiny priamo ako slovník `dict`?',
                    'question_en': 'Which Match method returns all named groups directly as a dictionary?',
                    'option_a_sk': 'match.groupdict()', 'option_a_en': 'match.groupdict()',
                    'option_b_sk': 'match.as_dict()', 'option_b_en': 'match.as_dict()',
                    'option_c_sk': 'match.to_dict()', 'option_c_en': 'match.to_dict()',
                    'option_d_sk': 'match.groups_dict()', 'option_d_en': 'match.groups_dict()',
                    'correct_option': 'A',
                    'explanation_sk': 'Metóda match.groupdict() vracia kľúče a hodnoty všetkých pomenovaných skupín.',
                    'explanation_en': 'match.groupdict() returns mapping of named groups.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Extrakcia IP adresy z logu',
                    'title_en': 'Extract IP Address from Log',
                    'instructions_sk': 'Napíš funkciu `extrahuj_ip_adresy(log_text)`, ktorá pomocou regexu nájde všetky IPv4 adresy v tvare `X.X.X.X` (kde X je 1 až 3 číslice) a vráti ich ako zoznam reťazcov.',
                    'instructions_en': 'Write function `extrahuj_ip_adresy(log_text)` extracting all IPv4 addresses.',
                    'starter_code': 'import re\n\ndef extrahuj_ip_adresy(log_text):\n    # Nájdi IPv4 adresy\n    pass\n',
                    'solution_code': 'import re\n\ndef extrahuj_ip_adresy(log_text):\n    return re.findall(r"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b", log_text)\n',
                    'explanation_sk': 'Použili sme re.findall so vzorom pre 4 oktety oddelené bodkou.',
                    'explanation_en': 'We matched four decimal octets separated by dots.',
                    'hint_sk': 'Použi re.findall(r"\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b", log_text).',
                    'hint_en': 'Match four digit blocks with dots.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'extrahuj_ip_adresy("Pripojenie z 192.168.1.1 a 10.0.0.5 úspešné")', 'expected_output': "['192.168.1.1', '10.0.0.5']", 'test_code': 'assert extrahuj_ip_adresy("Pripojenie z 192.168.1.1 a 10.0.0.5 úspešné") == ["192.168.1.1", "10.0.0.5"]', 'is_hidden': False},
                        {'input_data': 'extrahuj_ip_adresy("Žiadna adresa")', 'expected_output': '[]', 'test_code': 'assert extrahuj_ip_adresy("Žiadna adresa") == []', 'is_hidden': False},
                        {'input_data': 'extrahuj_ip_adresy("Host 127.0.0.1 localhost")', 'expected_output': "['127.0.0.1']", 'test_code': 'assert extrahuj_ip_adresy("Host 127.0.0.1 localhost") == ["127.0.0.1"]', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Parsovanie HTTP prístupového riadku',
                    'title_en': 'Parse HTTP Access Log Line',
                    'instructions_sk': 'Napíš funkciu `parsuj_http_poziadavku(riadok)`, ktorá z reťazca v tvare `"GET /courses/python HTTP/1.1"` extrahuje metódu a cestu. Vráti slovník `{"metoda": ..., "cesta": ...}` alebo `None`, ak formát nezodpovedá.',
                    'instructions_en': 'Write function `parsuj_http_poziadavku(riadok)` returning `{"metoda": ..., "cesta": ...}` or `None`.',
                    'starter_code': 'import re\n\ndef parsuj_http_poziadavku(riadok):\n    # Parsuj HTTP metódu a cestu\n    pass\n',
                    'solution_code': 'import re\n\ndef parsuj_http_poziadavku(riadok):\n    m = re.match(r"^(?P<metoda>[A-Z]+)\\s+(?P<cesta>/\\S*)\\s+HTTP/\\d\\.\\d$", riadok.strip())\n    return m.groupdict() if m else None\n',
                    'explanation_sk': 'Použili sme re.match s pomenovanými skupinami (?P<metoda>...) a (?P<cesta>...).',
                    'explanation_en': 'We used re.match with named groups method and path.',
                    'hint_sk': 'Použi re.match(r"^(?P<metoda>[A-Z]+)\\s+(?P<cesta>/\\S*)\\s+HTTP/\\d\\.\\d$", riadok.strip()).',
                    'hint_en': 'Use named groups in re.match.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'parsuj_http_poziadavku("GET /api/v1/lessons HTTP/1.1")', 'expected_output': "{'metoda': 'GET', 'cesta': '/api/v1/lessons'}", 'test_code': 'assert parsuj_http_poziadavku("GET /api/v1/lessons HTTP/1.1") == {"metoda": "GET", "cesta": "/api/v1/lessons"}', 'is_hidden': False},
                        {'input_data': 'parsuj_http_poziadavku("POST /login HTTP/2.0")', 'expected_output': "{'metoda': 'POST', 'cesta': '/login'}", 'test_code': 'assert parsuj_http_poziadavku("POST /login HTTP/2.0") == {"metoda": "POST", "cesta": "/login"}', 'is_hidden': False},
                        {'input_data': 'parsuj_http_poziadavku("Zlý formát")', 'expected_output': 'None', 'test_code': 'assert parsuj_http_poziadavku("Zlý formát") is None', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Komplexný analyzátor logov zlyhaných prihlásení',
                    'title_en': 'Failed Login Security Log Analyzer',
                    'instructions_sk': (
                        "Napíš funkciu `analyzuj_utoky(zoznam_riadkov)`:\n"
                        "Zoznam obsahuje riadky systémového logu v tvare `TIMESTAMP [LEVEL] IP: USER - SPRAVA`.\n"
                        "Funkcia vyhľadá riadky obsahujúce úroveň `FAILED_LOGIN` a vráti slovník, kde kľúčom je IP adresa a hodnotou počet neúspešných pokusov o prihlásenie z danej IP adresy."
                    ),
                    'instructions_en': 'Write function `analyzuj_utoky(zoznam_riadkov)` tallying failed login attempts per IP address in dictionary.',
                    'starter_code': 'import re\n\ndef analyzuj_utoky(zoznam_riadkov):\n    # Analyzuj zlyhané prihlásenia podľa IP\n    pass\n',
                    'solution_code': (
                        'import re\n\n'
                        'def analyzuj_utoky(zoznam_riadkov):\n'
                        '    vysledky = {}\n'
                        '    pattern = r"\\[FAILED_LOGIN\\]\\s+(?P<ip>\\d{1,3}(?:\\.\\d{1,3}){3})"\n'
                        '    for riadok in zoznam_riadkov:\n'
                        '        m = re.search(pattern, riadok)\n'
                        '        if m:\n'
                        '            ip = m.group("ip")\n'
                        '            vysledky[ip] = vysledky.get(ip, 0) + 1\n'
                        '    return vysledky\n'
                    ),
                    'explanation_sk': 'Pre každý riadok sme vyhľadali zhodu s [FAILED_LOGIN] a inkrementovali počítadlo pre nájdenú IP adresu.',
                    'explanation_en': 'Extracted IP from FAILED_LOGIN lines and accumulated occurrences in dict.',
                    'hint_sk': 'Použi re.search(r"\\[FAILED_LOGIN\\]\\s+(?P<ip>\\d{1,3}(?:\\.\\d{1,3}){3})", r) a slovník na počítanie.',
                    'hint_en': 'Match FAILED_LOGIN and IP, aggregate counts in dict.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'analyzuj_utoky(["2026-10-20 [FAILED_LOGIN] 192.168.1.50: root - Bad password", "2026-10-20 [INFO] 10.0.0.1: admin - OK", "2026-10-20 [FAILED_LOGIN] 192.168.1.50: admin - Bad password"])',
                            'expected_output': "{'192.168.1.50': 2}",
                            'test_code': 'assert analyzuj_utoky(["2026-10-20 [FAILED_LOGIN] 192.168.1.50: root - Bad password", "2026-10-20 [INFO] 10.0.0.1: admin - OK", "2026-10-20 [FAILED_LOGIN] 192.168.1.50: admin - Bad password"]) == {"192.168.1.50": 2}',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'analyzuj_utoky(["Všetko v poriadku"])',
                            'expected_output': '{}',
                            'test_code': 'assert analyzuj_utoky(["Všetko v poriadku"]) == {}',
                            'is_hidden': False
                        },
                        {
                            'input_data': 'analyzuj_utoky(["[FAILED_LOGIN] 1.1.1.1: a - err", "[FAILED_LOGIN] 2.2.2.2: b - err"])',
                            'expected_output': "{'1.1.1.1': 1, '2.2.2.2': 1}",
                            'test_code': 'assert analyzuj_utoky(["[FAILED_LOGIN] 1.1.1.1: a - err", "[FAILED_LOGIN] 2.2.2.2: b - err"]) == {"1.1.1.1": 1, "2.2.2.2": 1}',
                            'is_hidden': True
                        }
                    ]
                }
            ]
        }
    ]
}
