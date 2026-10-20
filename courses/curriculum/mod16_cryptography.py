"""
MODUL 16: Kryptografia a kyberbezpečnosť v Pythone
Odhadovaný rozsah: 12 hodín | Náročnosť: INTERMEDIATE | Úroveň: FREE | Track: MATURITA_PREP
"""

MODULE_DATA = {
    'order': 16,
    'track': 'MATURITA_PREP',
    'title_sk': 'Kryptografia a kyberbezpečnosť v Pythone',
    'title_en': 'Cryptography & Cybersecurity in Python',
    'description_sk': 'Praktická kybernetická bezpečnosť a šifrovanie: Caesarova a Vigenèrova šifra, ord() a chr(), bitové operácie XOR, jednosmerné kryptografické hašovanie cez hashlib (SHA-256) a sofistikovaná kontrola sily a entropie hesiel.',
    'description_en': 'Practical cybersecurity and encryption in Python: Caesar and Vigenere ciphers, ord() and chr(), bitwise XOR, one-way cryptographic hashing with hashlib (SHA-256), and password complexity audits.',
    'programming_language': 'python',
    'estimated_hours': 12,
    'difficulty_level': 'INTERMEDIATE',
    'is_pro_only': False,
    'icon_name': 'shield-lock',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Klasická substitučná kryptografia: Caesarova šifra',
            'title_en': 'Classical Substitution Cryptography: Caesar Cipher',
            'summary_sk': 'Funkcie ord() a chr(), modulárna aritmetika % 26, šifrovanie a dešifrovanie Caesarovej šifry.',
            'summary_en': 'ord() and chr() functions, modular arithmetic % 26, Caesar encryption and decryption.',
            'estimated_minutes': 45,
            'xp_reward': 30,
            'is_published': True,
            'content_sk': """### 16.1 Caesarova posuvná šifra

Caesarova šifra je jedna z najstarších známych šifier. Každé písmeno v otvorenom texte sa posunie o pevný počet pozícií $k$ v abecede:
$$C = (P + k) \\pmod{26}$$

#### Funkcie `ord()` a `chr()`
- `ord('A')` vráti ASCII kód znaku (pre `'A'` je to 65, pre `'Z'` 90).
- `chr(65)` prevedie číselný kód späť na znak `'A'`.

```python
def caesar_znak(ch, posun):
    if 'A' <= ch <= 'Z':
        return chr((ord(ch) - 65 + posun) % 26 + 65)
    elif 'a' <= ch <= 'z':
        return chr((ord(ch) - 97 + posun) % 26 + 97)
    return ch
```

> ⚠️ **Častá chyba na maturite:**
> Zabudnutie na modulo `% 26` pri prechode cez koniec abecedy. Ak písmeno `'Z'` posunieme o 1 bez modula, dostaneme znak `'['` namiesto `'A'`!
""",
            'content_en': """### 16.1 Caesar Cipher in Python

Use `ord()` and `chr()` with `% 26` alphabet wrapping.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú hodnotu vráti `ord("B") - ord("A")`?',
                    'question_en': 'What does `ord("B") - ord("A")` evaluate to?',
                    'option_a_sk': '1', 'option_a_en': '1',
                    'option_b_sk': '65', 'option_b_en': '65',
                    'option_c_sk': '0', 'option_c_en': '0',
                    'option_d_sk': 'Chyba typu', 'option_d_en': 'TypeError',
                    'correct_option': 'A',
                    'explanation_sk': 'Kód "B" je 66, "A" je 65, ich rozdiel je presne 1.',
                    'explanation_en': '66 - 65 = 1.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Caesarovo šifrovanie textu',
                    'title_en': 'Caesar Text Encryption',
                    'instructions_sk': 'Napíš funkciu `caesar_zasifruj(text, posun)`: posunie všetky písmená anglickej abecedy (veľké aj malé) o hodnotu `posun`. Ostatné znaky (medzery, čísla, interpunkciu) ponechá bezo zmeny.',
                    'instructions_en': 'Write function `caesar_zasifruj(text, posun)` shifting English letters by offset while keeping others intact.',
                    'starter_code': 'def caesar_zasifruj(text, posun):\n    # Zašifruj text Caesarovou šifrou\n    pass\n',
                    'solution_code': (
                        'def caesar_zasifruj(text, posun):\n'
                        '    vysledok = []\n'
                        '    for ch in text:\n'
                        '        if "A" <= ch <= "Z":\n'
                        '            vysledok.append(chr((ord(ch) - 65 + posun) % 26 + 65))\n'
                        '        elif "a" <= ch <= "z":\n'
                        '            vysledok.append(chr((ord(ch) - 97 + posun) % 26 + 97))\n'
                        '        else:\n'
                        '            vysledok.append(ch)\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Aplikovali sme posun modulo 26 pre veľké a malé písmená.',
                    'explanation_en': 'Applied modulo 26 shift preserving case and non-letters.',
                    'hint_sk': 'Použi (ord(ch) - 65 + posun) % 26 + 65 pre veľké písmená.',
                    'hint_en': 'Use ord() and chr() with modulo 26.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'caesar_zasifruj("Ahoj", 3)', 'expected_output': '"Dkrm"', 'test_code': 'assert caesar_zasifruj("Ahoj", 3) == "Dkrm"', 'is_hidden': False},
                        {'input_data': 'caesar_zasifruj("XYZ", 3)', 'expected_output': '"ABC"', 'test_code': 'assert caesar_zasifruj("XYZ", 3) == "ABC"', 'is_hidden': False},
                        {'input_data': 'caesar_zasifruj("Codoro 2027!", 1)', 'expected_output': '"Dpepsp 2027!"', 'test_code': 'assert caesar_zasifruj("Codoro 2027!", 1) == "Dpepsp 2027!"', 'is_hidden': True},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Caesarovo dešifrovanie textu',
                    'title_en': 'Caesar Text Decryption',
                    'instructions_sk': 'Napíš funkciu `caesar_odsifruj(sifra, posun)`: obnoví pôvodný text zašifrovaný so zadaným posunom.',
                    'instructions_en': 'Write function `caesar_odsifruj(sifra, posun)` decrypting Caesar cipher text.',
                    'starter_code': 'def caesar_odsifruj(sifra, posun):\n    # Dešifruj text posunom späť\n    pass\n',
                    'solution_code': (
                        'def caesar_odsifruj(sifra, posun):\n'
                        '    vysledok = []\n'
                        '    for ch in sifra:\n'
                        '        if "A" <= ch <= "Z":\n'
                        '            vysledok.append(chr((ord(ch) - 65 - posun) % 26 + 65))\n'
                        '        elif "a" <= ch <= "z":\n'
                        '            vysledok.append(chr((ord(ch) - 97 - posun) % 26 + 97))\n'
                        '        else:\n'
                        '            vysledok.append(ch)\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Dešifrovanie je posun v opačnom smere: - posun.',
                    'explanation_en': 'Decryption reverses the shift offset: - posun.',
                    'hint_sk': 'Použi opačný posun: - posun.',
                    'hint_en': 'Shift in reverse direction.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'caesar_odsifruj("Dkrm", 3)', 'expected_output': '"Ahoj"', 'test_code': 'assert caesar_odsifruj("Dkrm", 3) == "Ahoj"', 'is_hidden': False},
                        {'input_data': 'caesar_odsifruj("ABC", 3)', 'expected_output': '"XYZ"', 'test_code': 'assert caesar_odsifruj("ABC", 3) == "XYZ"', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Brute-force kryptoanalýza Caesarovej šifry',
                    'title_en': 'Brute-Force Caesar Cryptanalysis',
                    'instructions_sk': (
                        "Napíš funkciu `caesar_brute_force(sifra)`:\n"
                        "Keďže abeceda má len 26 písmen, Caesarovu šifru možno dešifrovať hrubou silou.\n"
                        "Funkcia vráti zoznam všetkých 26 možných dešifrovaných variantov pre posuny 0 až 25: `[(posun, text), ...]`."
                    ),
                    'instructions_en': 'Write function `caesar_brute_force(sifra)` generating all 26 possible shift candidates.',
                    'starter_code': 'def caesar_brute_force(sifra):\n    # Vygeneruj 26 variantov dešifrovania\n    pass\n',
                    'solution_code': (
                        'def caesar_brute_force(sifra):\n'
                        '    moznosti = []\n'
                        '    for k in range(26):\n'
                        '        dekod = []\n'
                        '        for ch in sifra:\n'
                        '            if "A" <= ch <= "Z":\n'
                        '                dekod.append(chr((ord(ch) - 65 - k) % 26 + 65))\n'
                        '            elif "a" <= ch <= "z":\n'
                        '                dekod.append(chr((ord(ch) - 97 - k) % 26 + 97))\n'
                        '            else:\n'
                        '                dekod.append(ch)\n'
                        '        moznosti.append((k, "".join(dekod)))\n'
                        '    return moznosti\n'
                    ),
                    'explanation_sk': 'Vytvorili sme všetkých 26 dešifrovaní pre k in range(26).',
                    'explanation_en': 'Generated all 26 variants using brute-force search.',
                    'hint_sk': 'Cyklus for k in range(26): dešifruj text s posunom k.',
                    'hint_en': 'Iterate k from 0 to 25.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'caesar_brute_force("Khoor")',
                            'expected_output': 'List of 26 candidates, shift 3 is Hello',
                            'test_code': (
                                'res = caesar_brute_force("Khoor")\n'
                                'assert len(res) == 26\n'
                                'assert res[3] == (3, "Hello")\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Polyalfabetická Vigenèrova šifra a kľúčové slová',
            'title_en': 'Polyalphabetic Vigenère Cipher & Key Stream',
            'summary_sk': 'Princíp Vigenèrovej tabuľky, opakovanie kľúča a ochrana pred frekvenčnou analýzou.',
            'summary_en': 'Vigenère tableau principle, keystream expansion, and frequency analysis resilience.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 16.2 Vigenèrova šifra

Na rozdiel od Caesara používa Vigenèrova šifra **premenlivý posun** definovaný heslom/kľúčom:
$$C_i = (P_i + K_i) \\pmod{26}$$

Tým sa výrazne sťažuje frekvenčná analýza, pretože to isté písmeno (napr. `'E'`) sa v rôznych pozíciách zašifruje rôznymi znakmi.
""",
            'content_en': """### 16.2 Polyalphabetic Vigenère Cipher

Encrypt using repeating keyword streams to thwart basic frequency analysis.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo je Vigenèrova šifra bezpečnejšia než jednoduchá Caesarova šifra?',
                    'question_en': 'Why is the Vigenère cipher more secure than Caesar?',
                    'option_a_sk': 'Pretože používa viacero rôznych posunov podľa kľúča, čo ničí frekvenčnú analýzu', 'option_a_en': 'It applies multiple shifts per keyword, disrupting letter frequency analysis',
                    'option_b_sk': 'Pretože používa 256-bitový kľúč', 'option_b_en': 'Uses 256-bit key',
                    'option_c_sk': 'Pretože beží v Pythone', 'option_c_en': 'Runs in Python',
                    'option_d_sk': 'Pretože mení dĺžku správy', 'option_d_en': 'Changes message length',
                    'correct_option': 'A',
                    'explanation_sk': 'Polyalfabetická povaha šifry zabraňuje jednoduchému dekódovaniu cez výskyt najčastejších písmen.',
                    'explanation_en': 'Polyalphabetic substitution flattens statistical letter frequency spikes.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Generovanie prúdu kľúča (Keystream)',
                    'title_en': 'Keystream Generator',
                    'instructions_sk': 'Napíš funkciu `generuj_kluc(text, kluc)`, ktorá zopakuje písmená z `kluc` tak, aby zodpovedali presnej dĺžke reťazca `text` (všetko uppercase). Napr. text="HELLO", kluc="KEY" -> "KEYKE". Ak je kluc prázdny, vráti `""`.',
                    'instructions_en': 'Write function `generuj_kluc(text, kluc)` repeating keyword to match text length.',
                    'starter_code': 'def generuj_kluc(text, kluc):\n    # Vygeneruj opakujúci sa prúd kľúča\n    pass\n',
                    'solution_code': (
                        'def generuj_kluc(text, kluc):\n'
                        '    if not kluc or not text:\n'
                        '        return ""\n'
                        '    k = kluc.upper()\n'
                        '    vysledok = []\n'
                        '    for i in range(len(text)):\n'
                        '        vysledok.append(k[i % len(k)])\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Použili sme indexovanie cez i % len(k) na cyklické opakovanie kľúča.',
                    'explanation_en': 'Used modulo indexing i % len(k) to cycle keystream.',
                    'hint_sk': 'Použi i % len(k) v cykle cez dĺžku textu.',
                    'hint_en': 'Cycle with modulo index.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'generuj_kluc("HELLO", "KEY")', 'expected_output': '"KEYKE"', 'test_code': 'assert generuj_kluc("HELLO", "KEY") == "KEYKE"', 'is_hidden': False},
                        {'input_data': 'generuj_kluc("PYTHON", "CODORO")', 'expected_output': '"CODORO"', 'test_code': 'assert generuj_kluc("PYTHON", "CODORO") == "CODORO"', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Zašifrovanie textu Vigenèrovou šifrou',
                    'title_en': 'Vigenère Text Encryption',
                    'instructions_sk': 'Napíš funkciu `vigenere_zasifruj(text, kluc)`: zašifruje iba veľké písmená textu (všetko preveď na uppercase a nealfabetické znaky ponechaj) s posunom určeným kľúčom (A=0, B=1, ... Z=25).',
                    'instructions_en': 'Write function `vigenere_zasifruj(text, kluc)` encrypting uppercase letters via Vigenere cipher.',
                    'starter_code': 'def vigenere_zasifruj(text, kluc):\n    # Zašifruj text Vigenèrovou šifrou\n    pass\n',
                    'solution_code': (
                        'def vigenere_zasifruj(text, kluc):\n'
                        '    if not kluc:\n'
                        '        return text\n'
                        '    k = kluc.upper()\n'
                        '    vysledok = []\n'
                        '    k_idx = 0\n'
                        '    for ch in text.upper():\n'
                        '        if "A" <= ch <= "Z":\n'
                        '            shift = ord(k[k_idx % len(k)]) - 65\n'
                        '            vysledok.append(chr((ord(ch) - 65 + shift) % 26 + 65))\n'
                        '            k_idx += 1\n'
                        '        else:\n'
                        '            vysledok.append(ch)\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Posúvame iba písmená A-Z o shift = ord(k[k_idx % len(k)]) - 65.',
                    'explanation_en': 'Shifted letters by key position in alphabet.',
                    'hint_sk': 'Inkrementuj k_idx iba pre písmená A-Z.',
                    'hint_en': 'Advance key index only on letters.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'vigenere_zasifruj("ATTACK AT DAWN", "LEMON")', 'expected_output': '"LXFOPV EF RNHR"', 'test_code': 'assert vigenere_zasifruj("ATTACK AT DAWN", "LEMON") == "LXFOPV EF RNHR"', 'is_hidden': False},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Dešifrovanie Vigenèrovej šifry',
                    'title_en': 'Vigenère Text Decryption',
                    'instructions_sk': 'Napíš funkciu `vigenere_odsifruj(sifra, kluc)`: zrekonštruuje pôvodný text (uppercase) z Vigenèrovej šifry.',
                    'instructions_en': 'Write function `vigenere_odsifruj(sifra, kluc)` decrypting Vigenere ciphertext.',
                    'starter_code': 'def vigenere_odsifruj(sifra, kluc):\n    # Dešifruj text Vigenèrovou šifrou\n    pass\n',
                    'solution_code': (
                        'def vigenere_odsifruj(sifra, kluc):\n'
                        '    if not kluc:\n'
                        '        return sifra\n'
                        '    k = kluc.upper()\n'
                        '    vysledok = []\n'
                        '    k_idx = 0\n'
                        '    for ch in sifra.upper():\n'
                        '        if "A" <= ch <= "Z":\n'
                        '            shift = ord(k[k_idx % len(k)]) - 65\n'
                        '            vysledok.append(chr((ord(ch) - 65 - shift) % 26 + 65))\n'
                        '            k_idx += 1\n'
                        '        else:\n'
                        '            vysledok.append(ch)\n'
                        '    return "".join(vysledok)\n'
                    ),
                    'explanation_sk': 'Opačný posun modulo 26: (ord(ch) - 65 - shift) % 26 + 65.',
                    'explanation_en': 'Reversed shift modulo 26.',
                    'hint_sk': 'Použi - shift namiesto + shift.',
                    'hint_en': 'Subtract shift offset.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'vigenere_odsifruj("LXFOPV EF RNHR", "LEMON")', 'expected_output': '"ATTACK AT DAWN"', 'test_code': 'assert vigenere_odsifruj("LXFOPV EF RNHR", "LEMON") == "ATTACK AT DAWN"', 'is_hidden': False},
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Kryptografické hašovacie funkcie a overovanie integrity (hashlib)',
            'title_en': 'Cryptographic Hashing & Integrity Verification (hashlib)',
            'summary_sk': 'Vlastnosti kryptografického hašu (jednosmernosť, lavínový efekt), SHA-256, soľ (Salt) a hexdigest().',
            'summary_en': 'One-way hash properties, avalanche effect, SHA-256, password salting and hexdigest().',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 16.3 Hašovanie s modulom `hashlib`

Kryptografický haš je jednosmerná matematická funkcia, ktorá pre ľubovoľne dlhý vstup vytvorí odtlačok pevnej dĺžky (tzv. **Digest / Hash**).

#### Kľúčové vlastnosti:
1. **Jednosmernosť (Pre-image resistance)**: z hašu nie je možné spätne vypočítať pôvodnú správu.
2. **Determinizmus**: rovnaký vstup vždy vygeneruje identický haš.
3. **Lavínový efekt (Avalanche effect)**: zmena jediného písmena v správe kompletne zmení celý výsledný haš.

```python
import hashlib

sprava = "heslo123"
# SHA-256 generuje 64 hexadecimálnych znakov (256 bitov)
hash_obj = hashlib.sha256(sprava.encode('utf-8'))
print(hash_obj.hexdigest())
```

#### Solenie hesiel (Salt)
Proti útokom pomocou predpočítaných tabuliek (Rainbow tables) sa pred hašovaním k heslu pripája náhodný reťazec – tzv. **soľ (salt)**.
""",
            'content_en': """### 16.3 Cryptographic Hashing with hashlib

Compute SHA-256 digests, verify message integrity, and apply password salting.
""",
            'quizzes': [
                {
                    'question_sk': 'Čo znamená lavínový efekt (avalanche effect) pri kryptografickom hašovaní?',
                    'question_en': 'What is the avalanche effect in cryptographic hashing?',
                    'option_a_sk': 'Aj nepatrná zmena jedného bitu na vstupe spôsobí dramatickú zmenu celého výsledného hašu', 'option_a_en': 'Even a tiny change of one input bit drastically changes the entire hash digest',
                    'option_b_sk': 'Hašovanie spôsobí pád servera', 'option_b_en': 'Hashing crashes server',
                    'option_c_sk': 'Rýchlosť výpočtu exponenciálne klesá', 'option_c_en': 'Performance degrades exponentially',
                    'option_d_sk': 'Haš sa automaticky zväčšuje', 'option_d_en': 'Hash size grows',
                    'correct_option': 'A',
                    'explanation_sk': 'Lavínový efekt zaručuje nepredvídateľnosť a odolnosť voči štatistickým útokom.',
                    'explanation_en': 'Avalanche effect guarantees thorough dispersion of input entropy.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet SHA-256 hašu textu',
                    'title_en': 'Compute SHA-256 Digest',
                    'instructions_sk': 'Napíš funkciu `vypocitaj_sha256(text)`: zakóduje text do UTF-8 a vráti 64-znakový hexadecimálny SHA-256 odtlačok.',
                    'instructions_en': 'Write function `vypocitaj_sha256(text)` returning hex sha256 string.',
                    'starter_code': 'import hashlib\n\ndef vypocitaj_sha256(text):\n    # Vráť SHA-256 hash\n    pass\n',
                    'solution_code': (
                        'import hashlib\n\n'
                        'def vypocitaj_sha256(text):\n'
                        '    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()\n'
                    ),
                    'explanation_sk': 'Použili sme hashlib.sha256(b).hexdigest().',
                    'explanation_en': 'Computed sha256 hexdigest of encoded string.',
                    'hint_sk': 'Použi hashlib.sha256(text.encode("utf-8")).hexdigest().',
                    'hint_en': 'Encode utf-8 and call hexdigest().',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {'input_data': 'vypocitaj_sha256("heslo123")', 'expected_output': 'hash', 'test_code': 'assert vypocitaj_sha256("heslo123") == "c666504a3ad3e23297a701d418728b74f4b1d7d079eeae6a7a932fa5a7114674"', 'is_hidden': False},
                        {'input_data': 'len(vypocitaj_sha256("test"))', 'expected_output': '64', 'test_code': 'assert len(vypocitaj_sha256("test")) == 64', 'is_hidden': False},
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Overenie integrity digitálnej správy',
                    'title_en': 'Verify Digital Message Integrity',
                    'instructions_sk': 'Napíš funkciu `over_integritu(sprava_text, ocakavany_hash)`: vypočíta SHA-256 odtlačok zo správy a porovná ho s očakávaným hašom (case-insensitive). Vráti `True`, ak je správa neporušená, inak `False`.',
                    'instructions_en': 'Write function `over_integritu(sprava_text, ocakavany_hash)` verifying SHA-256 checksum match.',
                    'starter_code': 'import hashlib\n\ndef over_integritu(sprava_text, ocakavany_hash):\n    # Over integritu správy\n    pass\n',
                    'solution_code': (
                        'import hashlib\n\n'
                        'def over_integritu(sprava_text, ocakavany_hash):\n'
                        '    aktualny = hashlib.sha256(sprava_text.encode("utf-8")).hexdigest().lower()\n'
                        '    return aktualny == ocakavany_hash.strip().lower()\n'
                    ),
                    'explanation_sk': 'Vypočítali sme hash a porovnali v lowercase formáte.',
                    'explanation_en': 'Compared lowercase sha256 checksums.',
                    'hint_sk': 'Vypočítaj hexdigest().lower() a porovnaj s ocakavany_hash.strip().lower().',
                    'hint_en': 'Compare lowercased digests.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'over_integritu("Codoro 2027", "8472...")',
                            'expected_output': 'True/False',
                            'test_code': (
                                'import hashlib\n'
                                'h = hashlib.sha256(b"Codoro 2027").hexdigest()\n'
                                'assert over_integritu("Codoro 2027", h) is True\n'
                                'assert over_integritu("Zmeneny text", h) is False\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Bezpečné solené hašovanie hesla (Salting)',
                    'title_en': 'Salted Password Hashing',
                    'instructions_sk': (
                        "Napíš funkciu `hasuj_heslo_sol(heslo, sol)`:\n"
                        "Zloží reťazec v tvare `f'{sol}:{heslo}'`, vypočíta z neho SHA-256 a vráti výsledok v tvare:\n"
                        "`f'{sol}${digest}'`.\n"
                        "Tento formát sa v moderných autentifikačných systémoch používa na uloženie soli spolu s hašom do databázy."
                    ),
                    'instructions_en': 'Write function `hasuj_heslo_sol(heslo, sol)` returning salted formatted string `{sol}${sha256}`.',
                    'starter_code': 'import hashlib\n\ndef hasuj_heslo_sol(heslo, sol):\n    # Vráť soľou zabezpečený hash\n    pass\n',
                    'solution_code': (
                        'import hashlib\n\n'
                        'def hasuj_heslo_sol(heslo, sol):\n'
                        '    kombinacia = f"{sol}:{heslo}".encode("utf-8")\n'
                        '    digest = hashlib.sha256(kombinacia).hexdigest()\n'
                        '    return f"{sol}${digest}"\n'
                    ),
                    'explanation_sk': 'Spojili sme soľ a heslo, vypočítali SHA-256 a spojili cez dolár $.',
                    'explanation_en': 'Combined salt:password, computed sha256 and formatted as salt$digest.',
                    'hint_sk': 'Zakóduj f"{sol}:{heslo}".encode() a vráť f"{sol}${digest}".',
                    'hint_en': 'Hash f"{sol}:{heslo}" and format with dollar sign.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'hasuj_heslo_sol("tajne", "random_salt")',
                            'expected_output': 'random_salt$digest',
                            'test_code': (
                                'res = hasuj_heslo_sol("tajne", "salt123")\n'
                                'assert res.startswith("salt123$")\n'
                                'assert len(res.split("$")[1]) == 64\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Bitové operácie XOR a audit bezpečnosti hesiel',
            'title_en': 'Bitwise XOR & Password Strength Auditing',
            'summary_sk': 'Bitový operátor XOR ^, symetrická bitová šifra, entropia hesla, kontrola zložitosti.',
            'summary_en': 'Bitwise XOR ^, symmetric stream cipher, password entropy and complexity evaluation.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 16.4 Bitový operátor XOR a audit hesiel

Operátor XOR (`^`) má unikátnu vlastnosť symetrie:
$$(A \\oplus B) \\oplus B = A$$
Vďaka tomu je tá istá operácia zároveň šifrovaním aj dešifrovaním!

```python
# XOR šifrovanie jedného znaku
znak = ord('A')  # 65 (01000001)
kluc = 42        # (00101010)
sifra = znak ^ kluc
povodny = sifra ^ kluc  # 65 ('A')
```
""",
            'content_en': """### 16.4 Bitwise XOR & Password Security

Explore XOR symmetry and implement strong password strength scoring.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú vlastnosť má bitová operácia XOR `(A ^ B) ^ B`?',
                    'question_en': 'What does `(A ^ B) ^ B` evaluate to?',
                    'option_a_sk': 'A (vráti pôvodnú hodnotu A)', 'option_a_en': 'A (returns original value A)',
                    'option_b_sk': 'B', 'option_b_en': 'B',
                    'option_c_sk': '0', 'option_c_en': '0',
                    'option_d_sk': '1', 'option_d_en': '1',
                    'correct_option': 'A',
                    'explanation_sk': 'Dvojitá aplikácia operátora XOR s rovnakým kľúčom vráti pôvodnú hodnotu.',
                    'explanation_en': 'XOR is self-inverting when reapplied with same key.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'XOR šifrovanie reťazca s jednobajtovým kľúčom',
                    'title_en': 'Single-Byte XOR Cipher',
                    'instructions_sk': 'Napíš funkciu `xor_sifra(text, kluc_int)`: pre každý znak textu vykoná bitovú operáciu `ord(ch) ^ kluc_int` a vráti nový reťazec zložený z takto transformovaných znakov.',
                    'instructions_en': 'Write function `xor_sifra(text, kluc_int)` applying bitwise XOR to each character ordinal.',
                    'starter_code': 'def xor_sifra(text, kluc_int):\n    # Vykonaj XOR šifrovanie\n    pass\n',
                    'solution_code': (
                        'def xor_sifra(text, kluc_int):\n'
                        '    return "".join(chr(ord(ch) ^ kluc_int) for ch in text)\n'
                    ),
                    'explanation_sk': 'Použili sme chr(ord(ch) ^ kluc_int) pre každý znak.',
                    'explanation_en': 'Applied chr(ord(ch) ^ kluc_int) in comprehension.',
                    'hint_sk': 'Použi "".join(chr(ord(c) ^ kluc_int) for c in text).',
                    'hint_en': 'Join chr(ord(c) ^ key).',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 35,
                    'doros_reward': 15,
                    'test_cases': [
                        {
                            'input_data': 'xor_sifra(xor_sifra("Ahoj", 42), 42)',
                            'expected_output': '"Ahoj"',
                            'test_code': 'assert xor_sifra(xor_sifra("Ahoj", 42), 42) == "Ahoj"',
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Bodové hodnotenie sily hesla (0 - 100 bodov)',
                    'title_en': 'Password Strength Scorer (0 - 100)',
                    'instructions_sk': (
                        "Napíš funkciu `ohodnot_heslo(heslo)`:\n"
                        "Vypočíta bodové skóre sily hesla:\n"
                        "- Za každé písmeno dĺžky získa 4 body (max 40 bodov),\n"
                        "- Obsahuje aspoň 1 malé písmeno: +15 bodov,\n"
                        "- Obsahuje aspoň 1 veľké písmeno: +15 bodov,\n"
                        "- Obsahuje aspoň 1 číslicu: +15 bodov,\n"
                        "- Obsahuje aspoň 1 špeciálny znak (nie alnum): +15 bodov.\n"
                        "Výsledné skóre ohranič na rozsah 0 až 100 bodov."
                    ),
                    'instructions_en': 'Write function `ohodnot_heslo(heslo)` scoring password strength from 0 to 100.',
                    'starter_code': 'def ohodnot_heslo(heslo):\n    # Ohodnoť heslo 0 - 100\n    pass\n',
                    'solution_code': (
                        'def ohodnot_heslo(heslo):\n'
                        '    if not heslo:\n'
                        '        return 0\n'
                        '    body = min(40, len(heslo) * 4)\n'
                        '    if any(c.islower() for c in heslo):\n'
                        '        body += 15\n'
                        '    if any(c.isupper() for c in heslo):\n'
                        '        body += 15\n'
                        '    if any(c.isdigit() for c in heslo):\n'
                        '        body += 15\n'
                        '    if any(not c.isalnum() for c in heslo):\n'
                        '        body += 15\n'
                        '    return min(100, body)\n'
                    ),
                    'explanation_sk': 'Otestovali sme dĺžku, lowercase, uppercase, čísla a špeciálne znaky.',
                    'explanation_en': 'Scored length, lowercase, uppercase, digits and special symbols.',
                    'hint_sk': 'Použi any(c.islower()), any(c.isupper()), any(c.isdigit()), any(not c.isalnum()).',
                    'hint_en': 'Check char types using any().',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {'input_data': 'ohodnot_heslo("P@ssw0rd2027")', 'expected_output': '100', 'test_code': 'assert ohodnot_heslo("P@ssw0rd2027") == 100', 'is_hidden': False},
                        {'input_data': 'ohodnot_heslo("heslo")', 'expected_output': '35', 'test_code': 'assert ohodnot_heslo("heslo") == 35', 'is_hidden': False},
                        {'input_data': 'ohodnot_heslo("")', 'expected_output': '0', 'test_code': 'assert ohodnot_heslo("") == 0', 'is_hidden': True},
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Striktný validátor bezpečnosti hesla',
                    'title_en': 'Strict Security Password Policy Validator',
                    'instructions_sk': (
                        "Napíš funkciu `je_bezpecne_heslo(heslo)`:\n"
                        "Vráti `True`, iba ak:\n"
                        "1. Dĺžka je aspoň 8 znakov,\n"
                        "2. Obsahuje aspoň 1 veľké, 1 malé písmeno, 1 číslicu a 1 špeciálny znak,\n"
                        "3. Neobsahuje zakázané slabé podreťazce (case-insensitive): `'123'`, `'password'`, `'admin'`, `'heslo'`.\n"
                        "Inak vráti `False`."
                    ),
                    'instructions_en': 'Write function `je_bezpecne_heslo(heslo)` enforcing strict password policy and blacklists.',
                    'starter_code': 'def je_bezpecne_heslo(heslo):\n    # Over bezpečnostnú politiku hesiel\n    pass\n',
                    'solution_code': (
                        'def je_bezpecne_heslo(heslo):\n'
                        '    if not heslo or len(heslo) < 8:\n'
                        '        return False\n'
                        '    lower_heslo = heslo.lower()\n'
                        '    for zakazane in ["123", "password", "admin", "heslo"]:\n'
                        '        if zakazane in lower_heslo:\n'
                        '            return False\n'
                        '    has_lower = any(c.islower() for c in heslo)\n'
                        '    has_upper = any(c.isupper() for c in heslo)\n'
                        '    has_digit = any(c.isdigit() for c in heslo)\n'
                        '    has_special = any(not c.isalnum() for c in heslo)\n'
                        '    return has_lower and has_upper and has_digit and has_special\n'
                    ),
                    'explanation_sk': 'Overili sme minimálnu dĺžku 8 znakov, prítomnosť 4 typov znakov a zoznam zakázaných slov.',
                    'explanation_en': 'Asserted length >= 8, all 4 character classes and common password blacklist.',
                    'hint_sk': 'Over dĺžku >= 8, zákaz slov "123", "password", "admin", "heslo" a 4 kategórie znakov.',
                    'hint_en': 'Enforce minimum length, blacklist checks, and 4 character classes.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {'input_data': 'je_bezpecne_heslo("Codoro#2027!")', 'expected_output': 'True', 'test_code': 'assert je_bezpecne_heslo("Codoro#2027!") is True', 'is_hidden': False},
                        {'input_data': 'je_bezpecne_heslo("Heslo123!")', 'expected_output': 'False (obsahuje heslo a 123)', 'test_code': 'assert je_bezpecne_heslo("Heslo123!") is False', 'is_hidden': False},
                        {'input_data': 'je_bezpecne_heslo("Kratke1!")', 'expected_output': 'False (menej ako 8 znakov)', 'test_code': 'assert je_bezpecne_heslo("Kratke1!") is False', 'is_hidden': True},
                    ]
                }
            ]
        }
    ]
}
