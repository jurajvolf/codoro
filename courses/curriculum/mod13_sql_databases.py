"""
MODUL 13: Práca s relačnými databázami a SQL v Pythone (sqlite3 :memory:)
Odhadovaný rozsah: 14 hodín | Náročnosť: ADVANCED | Úroveň: PRO / EDU | Track: ALGORITHMS_AND_DATA
"""

MODULE_DATA = {
    'order': 13,
    'track': 'ALGORITHMS_AND_DATA',
    'title_sk': 'Práca s relačnými databázami a SQL v Pythone (sqlite3 :memory:)',
    'title_en': 'Relational Databases & SQL in Python (sqlite3 :memory:)',
    'description_sk': 'Kompletný sprievodca relačnými databázami v Pythone: in-memory sqlite3 databázy, DDL príkazy CREATE TABLE, parametrizované INSERT dotazy s ochranou proti SQL Injection, filtrovanie cez SELECT a WHERE, prepojenia JOIN a agregačné funkcie GROUP BY.',
    'description_en': 'Comprehensive guide to relational databases in Python: in-memory sqlite3, DDL CREATE TABLE, parameterized queries protecting against SQL Injection, SELECT, WHERE, relational JOINs and GROUP BY aggregations.',
    'programming_language': 'python',
    'estimated_hours': 14,
    'difficulty_level': 'ADVANCED',
    'is_pro_only': True,
    'icon_name': 'database',
    'is_published': True,
    'lessons': [
        {
            'order': 1,
            'title_sk': 'Pripojenie k in-memory SQLite databáze a tvorba tabuliek (DDL)',
            'title_en': 'Connecting to In-Memory SQLite & Creating Tables (DDL)',
            'summary_sk': 'sqlite3.connect(":memory:"), objekt Cursor, execute(), dátové typy SQLite a CREATE TABLE.',
            'summary_en': 'sqlite3.connect(":memory:"), Cursor object, execute(), SQLite data types and CREATE TABLE.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 13.1 Vstavaná databáza SQLite v Pythone

Python obsahuje priamo vo svojej štandardnej knižnici modul `sqlite3`. Pre cvičenia, automatizované testy a rýchle prototypy je ideálna tzv. **in-memory databáza**:
```python
import sqlite3

# Vytvorenie databázy existujúcej iba v operačnej pamäti RAM
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
```

#### Dátové typy v SQLite:
- `INTEGER` – celočíselné hodnoty
- `REAL` – desatinné čísla s plávajúcou rádovou čiarkou
- `TEXT` – textové reťazce v kódovaní UTF-8
- `BLOB` – binárne dáta
- `NULL` – chýbajúca hodnota

#### Tvorba tabuľky (Data Definition Language - DDL)
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS studenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meno TEXT NOT NULL,
        vek INTEGER CHECK(vek >= 0),
        priemer REAL DEFAULT 1.0
    );
''')
conn.commit()
```

> ⚠️ **Častá chyba na maturite:**
> Zabudnutie zavolať `conn.commit()` po modifikácii dát (INSERT, UPDATE, DELETE). Bez commitu sa zmeny neuložia a po ukončení spojenia sa zahodia! (Pri DDL príkazoch ako CREATE TABLE SQLite robí commit automaticky, ale pri manipulácii s dátami je commit nevyhnutný).
""",
            'content_en': """### 13.1 SQLite In-Memory Database in Python

Learn `sqlite3.connect(":memory:")`, cursors, DDL `CREATE TABLE` and commits.
""",
            'quizzes': [
                {
                    'question_sk': 'Akú výhodu má pripojenie k databáze cez `sqlite3.connect(":memory:")`?',
                    'question_en': 'What is the primary benefit of `sqlite3.connect(":memory:")`?',
                    'option_a_sk': 'Databáza beží bleskovo v RAM pamäti bez vytvárania dočasných súborov na disku', 'option_a_en': 'Runs purely in RAM without creating disk files',
                    'option_b_sk': 'Dokáže sa pripojiť na vzdialený cloud server', 'option_b_en': 'Connects to remote clouds',
                    'option_c_sk': 'Nevyžaduje inštaláciu Pythonu', 'option_c_en': 'Requires no Python',
                    'option_d_sk': 'Automaticky prekladá Python do C++', 'option_d_en': 'Translates Python to C++',
                    'correct_option': 'A',
                    'explanation_sk': 'In-memory SQLite je ideálna pre unit testy a izolované sandbox prostredia.',
                    'explanation_en': 'In-memory databases provide ultra-fast isolated execution.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Vytvorenie tabuľky študentov',
                    'title_en': 'Create Students Table',
                    'instructions_sk': (
                        "Napíš funkciu `vytvor_tabulku_studenti(conn)`:\n"
                        "Pomocou spojenia `conn` vytvor tabuľku s názvom `studenti` so stĺpcami:\n"
                        "- `id` (INTEGER PRIMARY KEY AUTOINCREMENT),\n"
                        "- `meno` (TEXT NOT NULL),\n"
                        "- `vek` (INTEGER NOT NULL).\n"
                        "Funkcia vráti `True` po úspešnom vykonaní."
                    ),
                    'instructions_en': 'Write function `vytvor_tabulku_studenti(conn)` executing CREATE TABLE studenti (id, meno, vek) and returning True.',
                    'starter_code': 'import sqlite3\n\ndef vytvor_tabulku_studenti(conn):\n    # Vytvor tabuľku pomocou cursor.execute\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def vytvor_tabulku_studenti(conn):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("""\n'
                        '        CREATE TABLE IF NOT EXISTS studenti (\n'
                        '            id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                        '            meno TEXT NOT NULL,\n'
                        '            vek INTEGER NOT NULL\n'
                        '        );\n'
                        '    """)\n'
                        '    conn.commit()\n'
                        '    return True\n'
                    ),
                    'explanation_sk': 'Vytvorili sme kurzor, vykonali CREATE TABLE IF NOT EXISTS a potvrdili commitom.',
                    'explanation_en': 'Created cursor, executed CREATE TABLE IF NOT EXISTS, and committed.',
                    'hint_sk': 'Použi cur = conn.cursor() a cur.execute("CREATE TABLE IF NOT EXISTS studenti ...").',
                    'hint_en': 'Use cursor.execute with CREATE TABLE.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'vytvor_tabulku_studenti(sqlite3.connect(":memory:"))',
                            'expected_output': 'True',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'assert vytvor_tabulku_studenti(c) is True\n'
                                'cur = c.cursor()\n'
                                'cur.execute("SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'studenti\'")\n'
                                'assert cur.fetchone() is not None\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Overenie existencie tabuľky v databáze',
                    'title_en': 'Check Table Existence',
                    'instructions_sk': (
                        "Napíš funkciu `tabulka_existuje(conn, nazov_tabulky)`:\n"
                        "Funkcia sa opýta na systémovú tabuľku `sqlite_master` dotazom:\n"
                        "`SELECT 1 FROM sqlite_master WHERE type='table' AND name=?`\n"
                        "Vráti `True`, ak tabuľka existuje, inak vráti `False`."
                    ),
                    'instructions_en': 'Write function `tabulka_existuje(conn, nazov_tabulky)` checking table in sqlite_master.',
                    'starter_code': 'import sqlite3\n\ndef tabulka_existuje(conn, nazov_tabulky):\n    # Over existenciu tabuľky\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def tabulka_existuje(conn, nazov_tabulky):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("SELECT 1 FROM sqlite_master WHERE type=\'table\' AND name=?", (nazov_tabulky,))\n'
                        '    return cur.fetchone() is not None\n'
                    ),
                    'explanation_sk': 'Použili sme dotaz do sqlite_master s parametrom (nazov_tabulky,).',
                    'explanation_en': 'Queried sqlite_master with parameterized tuple.',
                    'hint_sk': 'Použi cur.execute("... name=?", (nazov_tabulky,)) a over cur.fetchone().',
                    'hint_en': 'Use parameterized tuple and check if fetchone() is not None.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'tabulka_existuje(c, "studenti")',
                            'expected_output': 'True/False',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'assert tabulka_existuje(c, "studenti") is False\n'
                                'c.execute("CREATE TABLE studenti (id INT)")\n'
                                'assert tabulka_existuje(c, "studenti") is True\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Inicializácia schémy e-shopu s cudzím kľúčom',
                    'title_en': 'Initialize E-Shop Schema with Foreign Key',
                    'instructions_sk': (
                        "Napíš funkciu `inicializuj_eshop(conn)`:\n"
                        "Vytvorí dve tabuľky:\n"
                        "1. `zakaznici` (id INTEGER PRIMARY KEY, email TEXT UNIQUE, meno TEXT)\n"
                        "2. `objednavky` (id INTEGER PRIMARY KEY, zakaznik_id INTEGER, suma REAL, FOREIGN KEY(zakaznik_id) REFERENCES zakaznici(id))\n"
                        "Funkcia vráti `True`."
                    ),
                    'instructions_en': 'Write function `inicializuj_eshop(conn)` creating zakaznici and objednavky with foreign key.',
                    'starter_code': 'import sqlite3\n\ndef inicializuj_eshop(conn):\n    # Vytvor relačné tabuľky\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def inicializuj_eshop(conn):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("""\n'
                        '        CREATE TABLE IF NOT EXISTS zakaznici (\n'
                        '            id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                        '            email TEXT UNIQUE NOT NULL,\n'
                        '            meno TEXT NOT NULL\n'
                        '        );\n'
                        '    """)\n'
                        '    cur.execute("""\n'
                        '        CREATE TABLE IF NOT EXISTS objednavky (\n'
                        '            id INTEGER PRIMARY KEY AUTOINCREMENT,\n'
                        '            zakaznik_id INTEGER NOT NULL,\n'
                        '            suma REAL NOT NULL,\n'
                        '            FOREIGN KEY(zakaznik_id) REFERENCES zakaznici(id)\n'
                        '        );\n'
                        '    """)\n'
                        '    conn.commit()\n'
                        '    return True\n'
                    ),
                    'explanation_sk': 'Vytvorili sme obe relačné tabuľky s definíciou cudzieho kľúča.',
                    'explanation_en': 'Created both relational tables with foreign key constraint.',
                    'hint_sk': 'Použi dva CREATE TABLE príkazy a FOREIGN KEY(zakaznik_id) REFERENCES zakaznici(id).',
                    'hint_en': 'Execute both statements and commit.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'inicializuj_eshop(conn)',
                            'expected_output': 'True',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'assert inicializuj_eshop(c) is True\n'
                                'cur = c.cursor()\n'
                                'cur.execute("SELECT count(*) FROM sqlite_master WHERE type=\'table\' AND name IN (\'zakaznici\', \'objednavky\')")\n'
                                'assert cur.fetchone()[0] == 2\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 2,
            'title_sk': 'Vkladanie dát a ochrana pred SQL Injection',
            'title_en': 'Data Insertion & SQL Injection Defense',
            'summary_sk': 'INSERT INTO, parametrizované dotazy s ?, executemany(), lastrowid a prevencia zraniteľností.',
            'summary_en': 'INSERT INTO, parameterized ? queries, executemany(), lastrowid and vulnerability prevention.',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 13.2 Bezpečné vkladanie dát a SQL Injection

Najväčšou bezpečnostnou chybou pri práci s databázami je skladanie SQL dotazov pomocou obyčajného spájania reťazcov alebo f-stringov:

```python
# ❌ KRITICKÁ ZRANITEĽNOSŤ (SQL INJECTION):
# Ak používateľ zadá meno: "'; DROP TABLE studenti; --"
cursor.execute(f"INSERT INTO studenti (meno) VALUES ('{user_input}')")
```

#### ✅ Riešenie: Parametrizované dotazy s `?`
Databázový engine automaticky ošetrí a sanitizuje parametre oddelene od SQL príkazu:
```python
cursor.execute("INSERT INTO studenti (meno, vek) VALUES (?, ?)", (meno, vek))
conn.commit()
print("ID nového záznamu:", cursor.lastrowid)
```

#### Hromadné vkladanie cez `executemany()`
Pre vloženie stoviek záznamov naraz použijeme `executemany`:
```python
studenti = [("Juraj", 18), ("Martin", 19), ("Lucia", 18)]
cursor.executemany("INSERT INTO studenti (meno, vek) VALUES (?, ?)", studenti)
conn.commit()
```
""",
            'content_en': """### 13.2 Parameterized Queries & SQL Injection Defense

Never interpolate strings into SQL. Always pass parameters via `?` tuples.
""",
            'quizzes': [
                {
                    'question_sk': 'Prečo je prísne zakázané skladať SQL dotazy cez f-stringy typu `f"SELECT * FROM users WHERE name=\'{name}\'"`?',
                    'question_en': 'Why is building SQL via f-strings strictly forbidden?',
                    'option_a_sk': 'Vystavuje systém zraniteľnosti SQL Injection, útočník môže ukradnúť alebo zmazať dáta', 'option_a_en': 'Exposes the system to SQL Injection, allowing data theft or drop table',
                    'option_b_sk': 'f-stringy nefungujú s databázou', 'option_b_en': 'f-strings fail in databases',
                    'option_c_sk': 'Databáza nepodporuje úvodzovky', 'option_c_en': 'Quotes are not supported',
                    'option_d_sk': 'Znižuje to rozlíšenie monitora', 'option_d_en': 'Reduces screen resolution',
                    'correct_option': 'A',
                    'explanation_sk': 'Parametrizované dotazy s ? striktne oddeľujú kód príkazu od používateľských dát.',
                    'explanation_en': 'Parameterized placeholders safely separate commands from untrusted inputs.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Bezpečné vloženie jedného študenta',
                    'title_en': 'Secure Single Student Insert',
                    'instructions_sk': (
                        "Napíš funkciu `vloz_studenta(conn, meno, vek)`:\n"
                        "Vykoná bezpečný parametrizovaný dotaz `INSERT INTO studenti (meno, vek) VALUES (?, ?)`.\n"
                        "Zavolá `conn.commit()` a vráti vygenerované `id` (cez `cursor.lastrowid`)."
                    ),
                    'instructions_en': 'Write function `vloz_studenta(conn, meno, vek)` executing parameterized INSERT and returning cursor.lastrowid.',
                    'starter_code': 'import sqlite3\n\ndef vloz_studenta(conn, meno, vek):\n    # Vlož študenta a vráť lastrowid\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def vloz_studenta(conn, meno, vek):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("INSERT INTO studenti (meno, vek) VALUES (?, ?)", (meno, vek))\n'
                        '    conn.commit()\n'
                        '    return cur.lastrowid\n'
                    ),
                    'explanation_sk': 'Použili sme execute s parametrom (meno, vek), zavolali commit a vrátili lastrowid.',
                    'explanation_en': 'Executed parameterized tuple, committed, and returned lastrowid.',
                    'hint_sk': 'Použi cur.execute("... VALUES (?, ?)", (meno, vek)) a return cur.lastrowid.',
                    'hint_en': 'Use parameterized tuple and return cur.lastrowid.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'vloz_studenta(conn, "Juraj", 18)',
                            'expected_output': '1',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE studenti (id INTEGER PRIMARY KEY AUTOINCREMENT, meno TEXT, vek INT)")\n'
                                'id1 = vloz_studenta(c, "Juraj", 18)\n'
                                'assert id1 == 1\n'
                                'id2 = vloz_studenta(c, "Martin", 19)\n'
                                'assert id2 == 2\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Hromadné vloženie záznamov (executemany)',
                    'title_en': 'Batch Insert via executemany',
                    'instructions_sk': (
                        "Napíš funkciu `vloz_zoznam_studentov(conn, zoznam_dvojic)`:\n"
                        "`zoznam_dvojic` obsahuje n-tice `[(meno1, vek1), (meno2, vek2), ...]`. \n"
                        "Pomocou metódy `cursor.executemany()` vlož všetky záznamy do tabuľky `studenti`, urob commit a vráti počet vložených riadkov (`cursor.rowcount`)."
                    ),
                    'instructions_en': 'Write function `vloz_zoznam_studentov(conn, zoznam_dvojic)` using executemany and returning cursor.rowcount.',
                    'starter_code': 'import sqlite3\n\ndef vloz_zoznam_studentov(conn, zoznam_dvojic):\n    # Hromadný insert cez executemany\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def vloz_zoznam_studentov(conn, zoznam_dvojic):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.executemany("INSERT INTO studenti (meno, vek) VALUES (?, ?)", zoznam_dvojic)\n'
                        '    conn.commit()\n'
                        '    return cur.rowcount\n'
                    ),
                    'explanation_sk': 'Metóda executemany optimalizovane vloží celý zoznam záznamov v jednej dávke.',
                    'explanation_en': 'executemany batch inserts all tuples efficiently.',
                    'hint_sk': 'Použi cur.executemany("INSERT INTO studenti (meno, vek) VALUES (?, ?)", zoznam_dvojic).',
                    'hint_en': 'Call cur.executemany with parameters and return cur.rowcount.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'vloz_zoznam_studentov(c, [("A", 18), ("B", 19), ("C", 18)])',
                            'expected_output': '3',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE studenti (id INTEGER PRIMARY KEY AUTOINCREMENT, meno TEXT, vek INT)")\n'
                                'count = vloz_zoznam_studentov(c, [("A", 18), ("B", 19), ("C", 18)])\n'
                                'assert count == 3\n'
                                'assert c.execute("SELECT count(*) FROM studenti").fetchone()[0] == 3\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Vloženie s ochranou proti duplicitám (INSERT OR IGNORE)',
                    'title_en': 'Deduplicated Insert (INSERT OR IGNORE)',
                    'instructions_sk': (
                        "Napíš funkciu `vloz_zakaznika_bezpecne(conn, email, meno)`:\n"
                        "Tabuľka `zakaznici` má unikátny stĺpec `email`. Pomocou príkazu `INSERT OR IGNORE INTO zakaznici (email, meno) VALUES (?, ?)` vlož zákazníka.\n"
                        "Ak bol záznam reálne vložený, vráti `True`. Ak bol ignorovaný kvôli duplicite e-mailu, vráti `False`."
                    ),
                    'instructions_en': 'Write function `vloz_zakaznika_bezpecne(conn, email, meno)` using INSERT OR IGNORE and returning True if added, False if duplicate.',
                    'starter_code': 'import sqlite3\n\ndef vloz_zakaznika_bezpecne(conn, email, meno):\n    # Vlož s kontrolou duplicity\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def vloz_zakaznika_bezpecne(conn, email, meno):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("INSERT OR IGNORE INTO zakaznici (email, meno) VALUES (?, ?)", (email, meno))\n'
                        '    conn.commit()\n'
                        '    return cur.rowcount > 0\n'
                    ),
                    'explanation_sk': 'Ak sqlite narazí na duplicitu v unikátnom stĺpci pri INSERT OR IGNORE, rowcount bude 0.',
                    'explanation_en': 'On conflict with INSERT OR IGNORE, cur.rowcount is 0.',
                    'hint_sk': 'Použi cur.execute("INSERT OR IGNORE ...") a skontroluj cur.rowcount > 0.',
                    'hint_en': 'Check if cur.rowcount > 0.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'vloz_zakaznika_bezpecne(c, "a@b.com", "Juraj")',
                            'expected_output': 'True then False for duplicate',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE zakaznici (id INTEGER PRIMARY KEY, email TEXT UNIQUE, meno TEXT)")\n'
                                'assert vloz_zakaznika_bezpecne(c, "a@b.com", "Juraj") is True\n'
                                'assert vloz_zakaznika_bezpecne(c, "a@b.com", "Juraj 2") is False\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 3,
            'title_sk': 'Výber dát (SELECT), filtrovanie (WHERE) a stránkovanie',
            'title_en': 'Data Querying (SELECT), Filtering (WHERE) & Pagination',
            'summary_sk': 'SELECT, WHERE, ORDER BY, LIMIT, OFFSET, metódy fetchone(), fetchall(), fetchmany().',
            'summary_en': 'SELECT, WHERE, ORDER BY, LIMIT, OFFSET, cursor fetchone(), fetchall(), fetchmany().',
            'estimated_minutes': 50,
            'xp_reward': 35,
            'is_published': True,
            'content_sk': """### 13.3 Výber a filtrovanie dát (SELECT & WHERE)

Dáta z databázy vyberáme pomocou príkazu `SELECT`.

#### Metódy kurzora na čítanie výsledkov:
- `cursor.fetchone()` – vráti nasledujúci 1 riadok ako `tuple` alebo `None`
- `cursor.fetchall()` – vráti všetky zodpovedajúce riadky ako zoznam `list[tuple]`
- `cursor.fetchmany(size)` – vráti dávku `size` riadkov

```python
# Výber študentov starších ako 18 rokov zoradených podľa mena
cursor.execute("SELECT id, meno, vek FROM studenti WHERE vek >= ? ORDER BY meno ASC", (18,))
vysledky = cursor.fetchall()
for row in vysledky:
    print(f"ID: {row[0]}, Meno: {row[1]}, Vek: {row[2]}")
```

#### Stránkovanie pomocou `LIMIT` a `OFFSET`
Pri zobrazení veľkých datasetov neprenášame milióny riadkov naraz, ale stránkujeme:
```python
# Stránka 2 (záznamy 11 až 20)
page_size = 10
page_num = 2
offset = (page_num - 1) * page_size
cursor.execute("SELECT * FROM studenti ORDER BY id LIMIT ? OFFSET ?", (page_size, offset))
```
""",
            'content_en': """### 13.3 SELECT, WHERE, ORDER BY & Pagination

Retrieve rows using `fetchall()`, `fetchone()` and paginate with `LIMIT` & `OFFSET`.
""",
            'quizzes': [
                {
                    'question_sk': 'Ktorá metóda kurzora vráti všetky zodpovedajúce riadky dotazu naraz ako zoznam n-tíc?',
                    'question_en': 'Which cursor method returns all matching query rows at once as a list of tuples?',
                    'option_a_sk': 'cursor.fetchall()', 'option_a_en': 'cursor.fetchall()',
                    'option_b_sk': 'cursor.get_all()', 'option_b_en': 'cursor.get_all()',
                    'option_c_sk': 'cursor.to_list()', 'option_c_en': 'cursor.to_list()',
                    'option_d_sk': 'cursor.select()', 'option_d_en': 'cursor.select()',
                    'correct_option': 'A',
                    'explanation_sk': 'cursor.fetchall() vráti list[tuple] so všetkými nájdenými záznamami.',
                    'explanation_en': 'cursor.fetchall() returns list of row tuples.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Získanie všetkých mien študentov',
                    'title_en': 'Get All Student Names',
                    'instructions_sk': (
                        "Napíš funkciu `ziskaj_vsetky_mena(conn)`:\n"
                        "Vyberie stĺpec `meno` zo všetkých riadkov tabuľky `studenti` zoradených abecedne (`ORDER BY meno ASC`).\n"
                        "Vráti čistý zoznam reťazcov `list[str]` (napr. `['Adam', 'Juraj', 'Zuzana']`)."
                    ),
                    'instructions_en': 'Write function `ziskaj_vsetky_mena(conn)` returning list of student names sorted alphabetically.',
                    'starter_code': 'import sqlite3\n\ndef ziskaj_vsetky_mena(conn):\n    # Vyber mená zoradené abecedne\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def ziskaj_vsetky_mena(conn):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("SELECT meno FROM studenti ORDER BY meno ASC")\n'
                        '    return [row[0] for row in cur.fetchall()]\n'
                    ),
                    'explanation_sk': 'Použili sme SELECT meno ORDER BY meno ASC a vybrali prvý prvok z každej n-tice.',
                    'explanation_en': 'Selected name, sorted ASC, unpacked row[0].',
                    'hint_sk': 'Použi cur.execute("SELECT meno FROM studenti ORDER BY meno ASC") a [r[0] for r in cur.fetchall()].',
                    'hint_en': 'Unpack row[0] from fetchall().',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'ziskaj_vsetky_mena(c)',
                            'expected_output': "['Juraj', 'Martin']",
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE studenti (meno TEXT)")\n'
                                'c.execute("INSERT INTO studenti VALUES (\'Martin\'), (\'Juraj\')")\n'
                                'assert ziskaj_vsetky_mena(c) == ["Juraj", "Martin"]\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Filtrovanie podľa vekového rozsahu',
                    'title_en': 'Filter by Age Range',
                    'instructions_sk': (
                        "Napíš funkciu `studenti_v_rozsahu(conn, min_vek, max_vek)`:\n"
                        "Vyberie z tabuľky `studenti` riadky, kde `vek >= min_vek` a `vek <= max_vek`.\n"
                        "Vráti zoznam slovníkov `[{'id': ..., 'meno': ..., 'vek': ...}, ...]`, zoradený podľa veku zostupne (`ORDER BY vek DESC`)."
                    ),
                    'instructions_en': 'Write function `studenti_v_rozsahu(conn, min_vek, max_vek)` returning dicts of students in age range.',
                    'starter_code': 'import sqlite3\n\ndef studenti_v_rozsahu(conn, min_vek, max_vek):\n    # Vyfiltruj študentov\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def studenti_v_rozsahu(conn, min_vek, max_vek):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("SELECT id, meno, vek FROM studenti WHERE vek >= ? AND vek <= ? ORDER BY vek DESC", (min_vek, max_vek))\n'
                        '    return [{"id": r[0], "meno": r[1], "vek": r[2]} for r in cur.fetchall()]\n'
                    ),
                    'explanation_sk': 'Použili sme parametrizovaný SELECT a namapovali n-tice do slovníkov.',
                    'explanation_en': 'Mapped fetched tuples into dictionary representations.',
                    'hint_sk': 'Použi cur.execute("... WHERE vek >= ? AND vek <= ? ORDER BY vek DESC", (min_vek, max_vek)).',
                    'hint_en': 'Use parameterized tuple and list comprehension.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'studenti_v_rozsahu(c, 18, 19)',
                            'expected_output': 'List of dicts',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE studenti (id INT, meno TEXT, vek INT)")\n'
                                'c.execute("INSERT INTO studenti VALUES (1, \'Ján\', 17), (2, \'Juraj\', 18), (3, \'Martin\', 19)")\n'
                                'res = studenti_v_rozsahu(c, 18, 19)\n'
                                'assert len(res) == 2\n'
                                'assert res[0]["meno"] == "Martin" and res[0]["vek"] == 19\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Stránkovanie výsledkov (Pagination)',
                    'title_en': 'Query Result Pagination',
                    'instructions_sk': (
                        "Napíš funkciu `ziskaj_stranku(conn, cislo_stranky, velkost_stranky)`:\n"
                        "Parametre: `cislo_stranky` (1-indexované, napr. 1 pre prvú stranu), `velkost_stranky`.\n"
                        "Vráti zoznam mien `list[str]` z tabuľky `studenti`, zoradených podľa `id ASC`, zodpovedajúcich danej stránke s využitím `LIMIT` a `OFFSET`."
                    ),
                    'instructions_en': 'Write function `ziskaj_stranku(conn, cislo_stranky, velkost_stranky)` implementing LIMIT and OFFSET pagination.',
                    'starter_code': 'import sqlite3\n\ndef ziskaj_stranku(conn, cislo_stranky, velkost_stranky):\n    # Vypočítaj offset a vyber stránku\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def ziskaj_stranku(conn, cislo_stranky, velkost_stranky):\n'
                        '    offset = max(0, (cislo_stranky - 1) * velkost_stranky)\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("SELECT meno FROM studenti ORDER BY id ASC LIMIT ? OFFSET ?", (velkost_stranky, offset))\n'
                        '    return [r[0] for r in cur.fetchall()]\n'
                    ),
                    'explanation_sk': 'Vypočítali sme offset = (cislo_stranky - 1) * velkost a aplikovali LIMIT ? OFFSET ?.',
                    'explanation_en': 'Computed offset and applied LIMIT ? OFFSET ?.',
                    'hint_sk': 'Vzorec pre offset: (cislo_stranky - 1) * velkost_stranky.',
                    'hint_en': 'Formula for offset: (page - 1) * page_size.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'ziskaj_stranku(c, 2, 2)',
                            'expected_output': "['C', 'D']",
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE studenti (id INT, meno TEXT)")\n'
                                'c.execute("INSERT INTO studenti VALUES (1,\'A\'), (2,\'B\'), (3,\'C\'), (4,\'D\'), (5,\'E\')")\n'
                                'assert ziskaj_stranku(c, 1, 2) == ["A", "B"]\n'
                                'assert ziskaj_stranku(c, 2, 2) == ["C", "D"]\n'
                                'assert ziskaj_stranku(c, 3, 2) == ["E"]\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        },
        {
            'order': 4,
            'title_sk': 'Relačné spojenia (JOIN) a agregácie (GROUP BY)',
            'title_en': 'Relational JOINs & Aggregations (GROUP BY)',
            'summary_sk': 'INNER JOIN, LEFT JOIN, agregačné funkcie COUNT(), SUM(), AVG(), MIN(), MAX(), zoskupovanie GROUP BY a HAVING.',
            'summary_en': 'INNER JOIN, LEFT JOIN, aggregate functions COUNT(), SUM(), AVG(), GROUP BY and HAVING clauses.',
            'estimated_minutes': 55,
            'xp_reward': 40,
            'is_published': True,
            'content_sk': """### 13.4 Relačné prepojenia tabuliek (JOIN) a agregácie

V reálnom relačnom modeli sú entity rozdelené do viacerých normalizovaných tabuliek.

#### 1. Relačné spojenie `INNER JOIN`
Prepojí záznamy z dvoch tabuliek na základe spoločného kľúča:
```python
query = '''
    SELECT s.meno, t.nazov_triedy
    FROM studenti s
    JOIN triedy t ON s.trieda_id = t.id
'''
cursor.execute(query)
```

#### 2. Agregačné funkcie
- `COUNT(*)` – počet záznamov
- `AVG(stlpce)` – aritmetický priemer
- `SUM(stlpce)` – súčet hodnôt
- `MIN()`, `MAX()` – najmenšia a najväčšia hodnota

#### 3. Zoskupovanie dát `GROUP BY`
Zoskupí záznamy podľa vybranej kategórie a spočíta pre každú skupinu agregácie:
```python
# Počet študentov a priemerný vek v každej triede
query = '''
    SELECT t.nazov_triedy, COUNT(s.id), AVG(s.vek)
    FROM triedy t
    LEFT JOIN studenti s ON t.id = s.trieda_id
    GROUP BY t.id
    ORDER BY COUNT(s.id) DESC
'''
```
""",
            'content_en': """### 13.4 Relational JOINs & Aggregations

Combine tables with `JOIN` and aggregate metrics with `GROUP BY`.
""",
            'quizzes': [
                {
                    'question_sk': 'Aký je rozdiel medzi klauzulami `WHERE` a `HAVING` v jazyku SQL?',
                    'question_en': 'What is the difference between WHERE and HAVING clauses in SQL?',
                    'option_a_sk': 'WHERE filtruje jednotlivé riadky pred zoskupením, HAVING filtruje agregované skupiny po GROUP BY', 'option_a_en': 'WHERE filters rows before grouping, HAVING filters aggregated groups after GROUP BY',
                    'option_b_sk': 'Nie je v nich rozdiel', 'option_b_en': 'There is no difference',
                    'option_c_sk': 'HAVING sa používa iba v MySQL, WHERE v SQLite', 'option_c_en': 'Dialect differences only',
                    'option_d_sk': 'WHERE funguje iba na čísla', 'option_d_en': 'WHERE only applies to numbers',
                    'correct_option': 'A',
                    'explanation_sk': 'Klauzula WHERE filtruje riadky pred agregáciou, HAVING vyhodnocuje agregačné podmienky (napr. HAVING COUNT(*) > 5).',
                    'explanation_en': 'WHERE applies pre-aggregation, HAVING applies post-aggregation.',
                }
            ],
            'exercises': [
                {
                    'order': 1,
                    'title_sk': 'Výpočet celkovej sumy objednávok zákazníka',
                    'title_en': 'Compute Customer Total Order Value',
                    'instructions_sk': (
                        "Napíš funkciu `suma_objednavok_zakaznika(conn, zakaznik_id)`:\n"
                        "Tabuľka `objednavky` obsahuje stĺpce `zakaznik_id` a `suma`.\n"
                        "Vráti celkový súčet (SUM) objednávok pre daného zákazníka. Ak zákazník nemá žiadne objednávky, vráti `0.0`."
                    ),
                    'instructions_en': 'Write function `suma_objednavok_zakaznika(conn, zakaznik_id)` returning total sum of orders or 0.0.',
                    'starter_code': 'import sqlite3\n\ndef suma_objednavok_zakaznika(conn, zakaznik_id):\n    # Vypočítaj celkovú sumu\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def suma_objednavok_zakaznika(conn, zakaznik_id):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("SELECT SUM(suma) FROM objednavky WHERE zakaznik_id = ?", (zakaznik_id,))\n'
                        '    val = cur.fetchone()[0]\n'
                        '    return float(val) if val is not None else 0.0\n'
                    ),
                    'explanation_sk': 'Použili sme SELECT SUM(suma) a ošetrili None hodnotu pri nulovom počte objednávok.',
                    'explanation_en': 'Used SUM(suma) and converted potential None to 0.0.',
                    'hint_sk': 'SELECT SUM(suma) WHERE zakaznik_id = ? a ošetri if val is not None.',
                    'hint_en': 'Handle None return with 0.0 default.',
                    'hint_cost_doros': 10,
                    'difficulty': 'EASY',
                    'xp_reward': 40,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'suma_objednavok_zakaznika(c, 1)',
                            'expected_output': '75.5',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE objednavky (zakaznik_id INT, suma REAL)")\n'
                                'c.execute("INSERT INTO objednavky VALUES (1, 50.0), (1, 25.5), (2, 100.0)")\n'
                                'assert suma_objednavok_zakaznika(c, 1) == 75.5\n'
                                'assert suma_objednavok_zakaznika(c, 99) == 0.0\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 2,
                    'title_sk': 'Prepojenie tabuliek cez INNER JOIN',
                    'title_en': 'Table Relational INNER JOIN',
                    'instructions_sk': (
                        "Napíš funkciu `objednavky_s_menami(conn)`:\n"
                        "Tabuľka `zakaznici` (id, meno) a `objednavky` (id, zakaznik_id, suma).\n"
                        "Pomocou `INNER JOIN` vráti zoznam n-tíc `[(meno_zakaznika, suma), ...]` zoradený podľa `suma DESC`."
                    ),
                    'instructions_en': 'Write function `objednavky_s_menami(conn)` performing INNER JOIN between orders and customers.',
                    'starter_code': 'import sqlite3\n\ndef objednavky_s_menami(conn):\n    # Prepoj zákazníkov a objednávky cez JOIN\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def objednavky_s_menami(conn):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("""\n'
                        '        SELECT z.meno, o.suma\n'
                        '        FROM objednavky o\n'
                        '        JOIN zakaznici z ON o.zakaznik_id = z.id\n'
                        '        ORDER BY o.suma DESC\n'
                        '    """)\n'
                        '    return cur.fetchall()\n'
                    ),
                    'explanation_sk': 'Spojili sme tabuľky cez JOIN na kľúči zakaznik_id = zakaznici.id a zoradili podľa sumy.',
                    'explanation_en': 'Joined tables on customer ID and ordered by order total descending.',
                    'hint_sk': 'Použi SELECT z.meno, o.suma FROM objednavky o JOIN zakaznici z ON o.zakaznik_id = z.id.',
                    'hint_en': 'Use INNER JOIN on primary and foreign keys.',
                    'hint_cost_doros': 10,
                    'difficulty': 'MEDIUM',
                    'xp_reward': 45,
                    'doros_reward': 20,
                    'test_cases': [
                        {
                            'input_data': 'objednavky_s_menami(c)',
                            'expected_output': "[('Martin', 200.0), ('Juraj', 50.0)]",
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE zakaznici (id INT, meno TEXT)")\n'
                                'c.execute("CREATE TABLE objednavky (id INT, zakaznik_id INT, suma REAL)")\n'
                                'c.execute("INSERT INTO zakaznici VALUES (1, \'Juraj\'), (2, \'Martin\')")\n'
                                'c.execute("INSERT INTO objednavky VALUES (10, 1, 50.0), (11, 2, 200.0)")\n'
                                'assert objednavky_s_menami(c) == [("Martin", 200.0), ("Juraj", 50.0)]\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                },
                {
                    'order': 3,
                    'title_sk': 'Dátová agregácia a štatistika predajov (GROUP BY)',
                    'title_en': 'Sales Analytics via GROUP BY',
                    'instructions_sk': (
                        "Napíš funkciu `statistika_kategorii(conn)`:\n"
                        "Tabuľka `produkty` obsahuje stĺpce `nazov`, `kategoria`, `cena`.\n"
                        "Funkcia vráti slovník v tvare `{'kategoria': {'pocet': int, 'celkova_suma': float, 'priemerna_cena': float}}`.\n"
                        "`celkova_suma` a `priemerna_cena` zaokrúhli na 2 desatinné miesta."
                    ),
                    'instructions_en': 'Write function `statistika_kategorii(conn)` grouping products by category and calculating count, sum, and average.',
                    'starter_code': 'import sqlite3\n\ndef statistika_kategorii(conn):\n    # Zoskup produkty podľa kategórie\n    pass\n',
                    'solution_code': (
                        'import sqlite3\n\n'
                        'def statistika_kategorii(conn):\n'
                        '    cur = conn.cursor()\n'
                        '    cur.execute("""\n'
                        '        SELECT kategoria, COUNT(*), SUM(cena), AVG(cena)\n'
                        '        FROM produkty\n'
                        '        GROUP BY kategoria\n'
                        '    """)\n'
                        '    vysledok = {}\n'
                        '    for row in cur.fetchall():\n'
                        '        kat, pocet, suma, priemer = row\n'
                        '        vysledok[kat] = {\n'
                        '            "pocet": pocet,\n'
                        '            "celkova_suma": round(float(suma), 2),\n'
                        '            "priemerna_cena": round(float(priemer), 2)\n'
                        '        }\n'
                        '    return vysledok\n'
                    ),
                    'explanation_sk': 'Použili sme GROUP BY kategoria s funkciami COUNT(*), SUM(cena) a AVG(cena).',
                    'explanation_en': 'Grouped by category with COUNT, SUM and AVG, rounding float numbers.',
                    'hint_sk': 'Použi SELECT kategoria, COUNT(*), SUM(cena), AVG(cena) FROM produkty GROUP BY kategoria.',
                    'hint_en': 'Select category and aggregates grouped by category.',
                    'hint_cost_doros': 15,
                    'difficulty': 'HARD',
                    'xp_reward': 55,
                    'doros_reward': 25,
                    'test_cases': [
                        {
                            'input_data': 'statistika_kategorii(c)',
                            'expected_output': 'Dictionary of category metrics',
                            'test_code': (
                                'import sqlite3\n'
                                'c = sqlite3.connect(":memory:")\n'
                                'c.execute("CREATE TABLE produkty (nazov TEXT, kategoria TEXT, cena REAL)")\n'
                                'c.execute("INSERT INTO produkty VALUES (\'Kniha 1\', \'Knihy\', 10.0), (\'Kniha 2\', \'Knihy\', 20.0), (\'Mobil\', \'Elektronika\', 300.0)")\n'
                                'stats = statistika_kategorii(c)\n'
                                'assert stats["Knihy"]["pocet"] == 2\n'
                                'assert stats["Knihy"]["celkova_suma"] == 30.0\n'
                                'assert stats["Knihy"]["priemerna_cena"] == 15.0\n'
                                'assert stats["Elektronika"]["pocet"] == 1\n'
                            ),
                            'is_hidden': False
                        }
                    ]
                }
            ]
        }
    ]
}
