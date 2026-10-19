================================================================================
CODORO - MASTER PROJECT CONTEXT & SPECIFICATION (PRE ANTIGRAVITY IDE AGENT)
================================================================================

1. OFICIÁLNE ZADANIE MATURITNEJ PRÁCE A IDENTIFIKÁCIA PROJEKTU
--------------------------------------------------------------------------------
- Číslo a názov témy: Téma č. 22 (trieda IV.C) - Webová platforma na výučbu Pythonu s registráciou používateľov
- Podtitul projektu: Návrh a implementácia gamifikovaného vzdelávacieho systému Codoro
- Študijný odbor: 2697 K mechanik elektrotechnik / čka - oblasť vzdelávania Informačno-mediálne technológie
- Forma práce: B - obhajoba vlastného projektu (PČOZ MS v zmysle vyhlášky MŠVVaŠ SR 224/2022 Z. z. podľa § 15 odst. 11 písm. b)
- Škola: Spojená škola, Hattalova 471, 027 43 Nižná (Organizačná zložka SOŠ Technická), rok obhajoby 2027
- Konzultant maturitnej práce: Mgr. Markéta Brišová
- Autor projektu: Juraj Volf
- Lokálna cesta projektu: C:\Users\jurvox\codoro
- GitHub repozitár: https://github.com/jurajvolf/codoro.git
- Oficiálny text zadania: Webová aplikácia slúžiaca ako vzdelávacia platforma na výučbu programovania v jazyku Python. Registrovaní používatelia majú prístup k lekciám a praktickým cvičeniam, systém umožňuje kontrolu ich riešení. Učiteľ má samostatné administrátorské rozhranie na správu obsahu a používateľov. Nástroje a technológie: webový framework (Python/Django), databáza (SQLite/PostgreSQL), HTML/CSS/JavaScript, systém autentifikácie používateľov.


2. IDENTITA ZNAČKY "CODORO" A KONKURENČNÉ VÝHODY (USP PRE OBHAJOBU)
--------------------------------------------------------------------------------
- Názov platformy: Codoro
  * Pôvod slova: Spojenie slov "Code" (kód), "Oro" (zlato po španielsky - odkaz na hernú ekonomiku) a techniky efektívneho učenia "Pomodoro" / tréningového centra "Dojo".
  * Rešerš ochranných známok (TMview): Názov Codoro bol overený v databáze TMview (existujúce záznamy sú len v potravinárskom priemysle, triedy pre vzdelávací softvér sú voľné).
  * Architektonická škálovateľnosť: Názov zámerne neobsahuje predponu "Py-", čo spolu so stĺpcom `programming_language` v databázovom modeli `Module` umožňuje kedykoľvek rozšíriť platformu o ďalšie jazyky (JavaScript, SQL, C++) bez zmeny databázovej schémy a názvu značky.
- Názov virtuálnej meny: Doros (zlaté mince získavané za aktivitu a riešenie úloh).
- Maskot a AI Tútor: Codo (postavička v modro-fialovej kapucni s laptopom `</>` a svietiacimi azúrovými očami z oficiálneho loga projektu).

- 4 hlavné piliere, ktorými sa Codoro líši od platforiem ako Duolingo, Codecademy či W3Schools:
  1. Prepojenie Študent - Trieda - Učiteľ (Classroom Ecosystem): Bežné platformy sú pre samoukov. Codoro spája žiakov do reálnych školských tried (`SchoolClass`), kde plnia spoločné triedne výzvy a učiteľ má kompletný redakčný systém (CMS) na správu obsahu, tried, úloh a živého progresu žiakov.
  2. Sokratovský AI Tútor Codo: Bežné AI (ChatGPT) napíše žiakovi hotový kód, čím sa žiak nič nenaučí. Codo má striktnú systémovú inštrukciu nikdy nenapísať hotové riešenie - iba analyzuje chybu vo výstupe testov a navedie študenta otázkou na správny riadok a logiku (v SK alebo EN).
  3. Reálna školská ekonomika s riadením zásob (Stock & Restock Marketplace): Mince Doros nie sú len virtuálne čísla. Učiteľ v obchode vypisuje reálne školské výhody (napr. odpustenie domácej úlohy, +10 % bodov k písomke, nápoveda na teste) s prísne obmedzeným skladom pre triedu (napr. 2 ks na týždeň), aby nedošlo k inflácii a hromadnému vykúpeniu.
  4. Plná dvojjazyčnosť (100 % SK / EN): Celé používateľské rozhranie, databázový obsah lekcií, cvičení, questov, odmien v obchode aj odpovede AI tútora Codo sú plne dostupné v slovenčine aj v angličtine.


3. TECHNOLOGICKÝ STACK A PRÍKAZY PROSTREDIA
--------------------------------------------------------------------------------
- Backend: Python 3 + Django (architektúra MVT - Model, View, Template).
- Databáza: SQLite (`db.sqlite3`) pre vývoj, plne kompatibilné s PostgreSQL cez Django ORM.
- Frontend: Vlastný moderný CSS Design System v `templates/base.html` (bez závislosti na externých CSS frameworkoch), responzívny CSS Grid/Flexbox, plynulé animácie (`cubic-bezier`), podpora Light/Dark režimu.
- Typografia: Google Fonts s plnou podporou slovenskej diakritiky (`subset=latin-ext`):
  * Nadpisy: `Plus Jakarta Sans` (weights 600, 700, 800)
  * Text a UI: `Inter` (weights 400, 500, 600, 700)
  * Kód a číselné metriky: `JetBrains Mono` (weights 400, 500, 600, 700)
- Integrovaný editor kódu: `CodeMirror 5.65.16` (režim `python`, téma `eclipse` pre svetlý režim a `material-darker` pre tmavý režim).
- Renderovanie Markdownu: Knižnica `marked.js` automaticky formátuje texty lekcií, zadaní a nápovied s triedou `.markdown-content.markdown-render`.
- AI integrácia: Google Gemini API (`gemini-2.5-flash` cez premennú prostredia `GEMINI_API_KEY`) + deterministický lokálny Sokratovský fallback v `courses/services.py` (zaručuje 100 % funkčnosť pri obhajobe aj bez pripojenia na internet alebo API kľúča).

- Príkazy na spustenie (Windows PowerShell):
  1. Aktivácia virtuálneho prostredia: `venv\Scripts\activate`
  2. Migrácie databázy: `python manage.py makemigrations` a `python manage.py migrate`
  3. Naplnenie kompletného kurikula a ukážkových dát: `python seed_codoro.py`
  4. Spustenie automatických testov: `python manage.py test`
  5. Spustenie vývojového servera: `python manage.py runserver`
  6. Testovacie účty vytvorené cez seed:
     - Študent: prihlasovacie meno `student` | heslo `heslo123` (trieda IV.C, kód `IVC-2027`)
     - Spolužiak v rebríčku: prihlasovacie meno `martin_k` | heslo `heslo123`
     - Učiteľ: prihlasovacie meno `ucitel` | heslo `heslo123`
     - Školský licenčný kľúč pre odomknutie EDU/PRO: `EDU-2027-IVC`


4. ŠTRUKTÚRA SÚBOROV A MODULOV V PROJEKTE
--------------------------------------------------------------------------------
codoro/
|-- config/                     # Hlavná konfigurácia projektu Django
|   |-- settings.py             # Nastavenia, INSTALLED_APPS, AUTH_USER_MODEL, TEMPLATES, STATICFILES_DIRS
|   |-- urls.py                 # Centrálny URL smerovač pre všetky 4 moduly
|   |-- wsgi.py & asgi.py
|-- accounts/                   # Modul používateľov, rolí, tried, jazyka, profilu a licencií
|   |-- models.py               # User, SchoolClass, SubscriptionLicense
|   |-- views.py                # login, register, logout, switch_language, repair_streak, activate_license, profile_view, certificate_view
|   |-- tests.py
|-- courses/                    # Modul výučby Pythonu, cvičení, kvízov, tréningovej arény a AI tútora
|   |-- models.py               # Module, Lesson, Exercise, TestCase, Submission, QuizQuestion, LessonProgress, UnlockedHint
|   |-- services.py             # evaluate_python_code (AST + subprocess sandbox runner), get_codo_ai_feedback, generate_ai_exercise
|   |-- views.py                # dashboard, lesson_detail, practice_arena, unlock_hint
|   |-- curriculum/             # Balík s modulárnymi dátami kurikula (12 modulov, 140+ hodín obsahu)
|   |   |-- __init__.py
|   |   |-- mod01_basics.py
|   |   |-- mod02_operators_strings.py
|   |   |-- mod03_conditions.py
|   |   |-- mod04_loops.py
|   |   |-- mod05_functions_recursion.py
|   |   |-- mod06_lists_tuples.py
|   |   |-- mod07_dicts_sets.py
|   |   |-- mod08_exceptions_files.py
|   |   |-- mod09_oop_basics.py
|   |   |-- mod10_oop_advanced.py
|   |   |-- mod11_algorithms.py
|   |   |-- mod12_boss_projects.py
|   |-- tests.py
|-- gamification/               # Modul hernej ekonomiky, obchodu so skladom, questov a Coin Dropov
|   |-- models.py               # RewardItem, RewardPurchase, DorosTransaction, Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution, CoinDrop, CoinDropClaim, Badge, StudentBadge
|   |-- views.py                # shop_view, buy_reward, claim_quest_reward, claim_coin_drop, leaderboard_view
|   |-- tests.py
|-- teacher_panel/              # Kompletný CMS a administrátorské rozhranie pre učiteľa (Full CRUD)
|   |-- views.py                # Kompletný CRUD pre Moduly, Lekcie, Cvičenia, Testy, Kvízy, Odmeny, Questy, Triedy, Licencie a Študentov
|   |-- tests.py
|-- templates/                  # HTML šablóny (100 % SK/EN, Light/Dark mode)
|   |-- base.html
|   |-- accounts/               # login.html, register.html, profile.html, certificate.html
|   |-- courses/                # dashboard.html, lesson_detail.html, practice_arena.html
|   |-- gamification/           # shop.html, leaderboard.html
|   |-- teacher_panel/          # dashboard.html, cms_modules.html, cms_lesson_form.html, cms_exercise_form.html, student_detail.html
|-- static/
|   |-- img/
|       |-- codoro-logo.jpg     # Oficiálne logo projektu Codoro (s automatickým SVG fallbackom)
|-- seed_codoro.py              # Hlavný skript na naplnenie databázy a celého 12-modulového kurikula
|-- requirements.txt
|-- manage.py
|-- GEMINI.md                   # Tento dokument


5. KOMPLETNÁ DATABÁZOVÁ SCHÉMA A BIZNIS LOGIKA
--------------------------------------------------------------------------------
A. Aplikácia `accounts`:
1. `SchoolClass`:
   - Polia: `name` (napr. IV.C), `join_code` (unikátny kód triedy, napr. IVC-2027), `teacher` (FK na User), `created_at`.
2. `User` (dedí z `AbstractUser`):
   - Rola a lokalizácia: `role` (STUDENT / TEACHER), `school_class` (FK na SchoolClass), `preferred_language` (sk / en), `bio`, `avatar_choice`.
   - Predplatné (Freemium SaaS model): `subscription_tier` (FREE / PRO / EDU), `daily_ai_hints_used`, `last_ai_hint_date`.
   - Gamifikácia: `xp`, `level`, `doros`.
   - Matematický vzorec pre Level: `XP = 100 * (Level - 1)^1.5`, resp. pre ďalší level `100 * Level^1.5`. Pri každom postupe na vyšší level (`add_xp_and_check_level_up`) dostane študent automaticky bonus `Nový_Level * 50 Doros`.
   - Denný Streak a záchrana: `current_streak`, `longest_streak`, `last_activity_date`, `streak_freezes`, `lost_streak_value` (hodnota vyhasnutej série, ktorú možno zachrániť za 200 Doros), `streak_lost_at`.
3. `SubscriptionLicense`:
   - Polia: `code` (napr. EDU-2027-IVC), `tier` (PRO / EDU), `max_uses`, `current_uses`, `is_active`, `created_at`.

B. Aplikácia `courses`:
4. `Module`:
   - Polia: `title_sk`, `title_en`, `description_sk`, `description_en`, `programming_language` (python / javascript / sql), `order`, `estimated_hours` (odhadovaný počet hodín štúdia, napr. 10h - 16h), `difficulty_level` (BEGINNER / INTERMEDIATE / ADVANCED), `is_pro_only` (uzamyká pokročilé moduly pre FREE účty), `icon_name`, `is_published` (umožňuje učiteľovi modul skryť/publikovať).
5. `Lesson`:
   - Polia: `module` (FK), `title_sk`, `title_en`, `summary_sk`, `summary_en`, `content_sk` (dlhý štruktúrovaný výklad v Markdowne s ukážkami kódu, tabuľkami a tipmi), `content_en` (Markdown), `estimated_minutes` (napr. 45 - 90 min), `order`, `xp_reward`, `is_published`.
6. `Exercise`:
   - Polia: `lesson` (FK), `title_sk`, `title_en`, `instructions_sk` (Markdown), `instructions_en` (Markdown), `starter_code`, `solution_code`, `explanation_sk`, `explanation_en` (vysvetlenie vzorového riešenia po úspešnom vyriešení), `hint_sk`, `hint_en`, `hint_cost_doros`, `difficulty` (EASY / MEDIUM / HARD), `xp_reward`, `doros_reward` (plná odmena na 1. pokus, polovičná na ďalšie pokusy), `order`.
7. `TestCase`:
   - Polia: `exercise` (FK), `input_data`, `expected_output`, `test_code` (Python `assert` príkaz spúšťaný v izolovanom AST + subprocess sandboxe s timeoutom 3 sekundy), `is_hidden` (skrytý test proti natvrdo napísaným odpovediam), `order`.
8. `Submission`:
   - Polia: `student` (FK), `exercise` (FK), `submitted_code`, `status` (PASSED / FAILED / ERROR), `execution_time_ms`, `output_log`, `ai_tutor_feedback` (odpoveď od AI tútora Codo), `teacher_comment` (pre Code Review od učiteľa), `created_at`.
9. `QuizQuestion`:
   - Polia: `lesson` (FK), `question_sk`, `question_en`, `option_a_sk/en`, `option_b_sk/en`, `option_c_sk/en`, `option_d_sk/en` (voliteľná 4. možnosť), `correct_option` (A/B/C/D), `explanation_sk`, `explanation_en` (vysvetlenie správnej odpovede), `order`.
10. `LessonProgress` & `UnlockedHint`:
    - Sledovanie prečítaných lekcií, vyriešených kvízov a odomknutých nápovied za Doros.

C. Aplikácia `gamification`:
11. `RewardItem` (Školský obchod s riadením skladových zásob):
    - Polia: `title_sk`, `title_en`, `description_sk`, `description_en`, `cost_doros`, `icon_name`, `max_stock`, `current_stock`, `restock_period` (DAILY / WEEKLY / MONTHLY / MANUAL), `limit_per_student_per_period`, `last_restocked_at`, `created_by`, `is_active`.
12. `RewardPurchase` (Zakúpené kupóny):
    - Polia: `student` (FK), `reward` (FK), `coupon_code` (`CDR-XXXXXX`), `cost_paid`, `status` (PENDING / REDEEMED / REFUNDED), `purchased_at`, `processed_at`, `processed_by`.
13. `DorosTransaction` (Audit Log peňaženky).
14. `Quest` & `StudentQuestProgress` (Osobné výzvy: `DAILY`, `WEEKLY`, `MONTHLY`, `TEACHER`).
15. `ClassQuest` & `ClassQuestContribution` (Kolektívne triedne výzvy s politikou `ALL_STUDENTS` alebo `CONTRIBUTORS_ONLY`).
16. `CoinDrop` & `CoinDropClaim` (Časované a náhodné bonusové dropy).
17. `Badge` & `StudentBadge` (Odznaky za míľniky).


6. PRAVIDLÁ DIZAJNOVÉHO SYSTÉMU A UI/UX (STRIKTNE DODRŽIAVAŤ PRI ÚPRAVÁCH)
--------------------------------------------------------------------------------
1. Zjednotený Light / Dark Mode:
   - Celá stránka sa riadi atribútom `html[data-theme="light"]` alebo `html[data-theme="dark"]` (prepínané tlačidlom v hornej lište a uložené v `localStorage` pod kľúčom `codoro_theme`).
   - NIKDY nemiešať svetlú kartu a tmavú kartu vedľa seba na jednej obrazovke. Všetky panely musia používať triedu `.card-surface`, ktorá sa plynule prispôsobuje zvolenému režimu.
   - Prepnutie témy zároveň dynamicky prepne tému CodeMirror editora (`eclipse` pre svetlý režim, `material-darker` pre tmavý režim).
2. Farebná paleta podľa loga Codoro:
   - Primárna akčná farba (Ro Indigo): `#4636F5` (v tmavom režime `#6366F1`).
   - Polnočná modrá (Codo Navy): `#0F172A` (texty vo svetlom režime / pozadie v tmavom režime).
   - Azúrová (Visor Cyan z očí maskota): `#5CE1E6` / `#0891B2` (akcenty pre AI tútora Codo a odznaky).
3. Formátovanie Markdownu (žiadne surové znaky `###` ani `**` v UI):
   - Každý element zobrazujúci text lekcie, zadania úlohy alebo nápovedy musí mať triedy `markdown-content markdown-render`, ktoré pri načítaní spracuje `marked.js`.
4. Bezchybná dvojjazyčnosť (SK / EN):
   - Na začiatku každej šablóny používať bezpečný tag `{% firstof user.preferred_language ui_lang 'sk' as lang %}`.
   - Každý novopridaný text, tlačidlo, nadpis alebo prázdny stav v šablóne aj vo `views.py` musí mať slovenskú aj anglickú vetvu (`{% if lang == 'en' %}...{% else %}...{% endif %}`).


7. FÁZOVÝ PLÁN PROJEKTU A DETAILNÁ ŠPECIFIKÁCIA PRE FÁZY 6, 7 A 8
--------------------------------------------------------------------------------
- FÁZA 1 až 5: Základná architektúra, databáza, základný UI/UX systém, Sokratovský AI tútor a 24 základných unit testov [DOKONČENÉ]

--------------------------------------------------------------------------------
FÁZA 6 (PRIORITA #1): KOMPLETNÝ CMS SYSTÉM NA SPRÁVU OBSAHU A POUŽÍVATEĽOV PRE UČITEĽA (`teacher_panel`)
--------------------------------------------------------------------------------
Cieľ: Učiteľ nesmie byť odkázaný na vstavaný `/admin/` ani na jednoduché pridanie jednej úlohy. V `teacher_panel` musí mať plnohodnotné vlastné CMS štúdio (Full CRUD: Create, Read, Update, Delete + zmena poradia) pre celú platformu:

6.1 Správa Vzdelávacích Modulov (CRUD pre `Module`):
    - Prehľad všetkých modulov s počtom lekcií, cvičení, odhadovanými hodinami a stavom (Publikované / Skryté, FREE / PRO-EDU).
    - Formulár na vytvorenie a úpravu modulu (`title_sk`, `title_en`, `description_sk`, `description_en`, `programming_language`, `order`, `estimated_hours`, `is_pro_only`, `is_published`).
    - Tlačidlá na okamžité posunutie poradia modulu nahor/nadol (`Move Up` / `Move Down`), prepnutie `FREE <-> PRO/EDU` a vymazanie modulu (s potvrdením).

6.2 Správa Lekcií a Markdown Editor so živým náhľadom (CRUD pre `Lesson`):
    - V rámci každého modulu učiteľ vidí zoznam lekcií a môže lekciu vytvoriť, upraviť, duplikovať alebo vymazať.
    - Pri úprave lekcie (`cms_lesson_form.html`) má učiteľ dvojstĺpcový Markdown editor: vľavo píše `content_sk` / `content_en` a vpravo okamžite vidí živý naformátovaný náhľad cez `marked.js`.
    - Správa Kvízových otázok (`QuizQuestion`) priamo v detaile lekcie: pridanie novej otázky, úprava existujúcej otázky (SK/EN text, možnosti A/B/C/D, správna odpoveď, vysvetlenie) a vymazanie otázky.

6.3 Kompletná správa Praktických Cvičení a Testovacích Prípadov (CRUD pre `Exercise` + `TestCase`):
    - Učiteľ vie v lekcii zobraziť všetky cvičenia (keďže lekcia má viacero cvičení od EASY po HARD), vytvoriť nové cvičenie, upraviť existujúce cvičenie a vymazať ho.
    - V editore cvičenia (`cms_exercise_form.html`) má CodeMirror editor pre `starter_code` a `solution_code`, polia pre `instructions_sk/en`, `hint_sk/en`, `hint_cost_doros`, `difficulty`, `xp_reward`, `doros_reward`.
    - Dynamická správa `TestCase` položiek k cvičeniu: učiteľ môže k jednému cvičeniu pridať ľubovoľný počet testovacích prípadov (`input_data`, `expected_output`, `test_code`, príznak `is_hidden` pre skryté testy), upraviť ich alebo vymazať.
    - Tlačidlo "Otestovať vzorové riešenie učiteľa": Učiteľ si priamo pri tvorbe úlohy jedným klikom overí, či jeho `solution_code` prechádza všetkými zadanými `TestCase` testami!
    - AI Asistent pre učiteľa v CMS:
      * Tlačidlo "AI Preložiť SK -> EN": Automaticky preloží slovenský názov, výklad lekcie alebo zadanie úlohy do angličtiny (cez Gemini API s inteligentným fallbackom).
      * Tlačidlo "AI Vygenerovať úlohu podľa témy": Učiteľ zadá len tému (napr. "Rekurzívny výpočet faktoriálu") a systém mu predvyplní zadanie, štartovací kód, riešenie a 3 assert testy.

6.4 Kompletná správa Obchodu, Questov, Tried a Používateľov:
    - Obchod (`RewardItem`): Okrem vytvorenia odmeny pridať možnosť upraviť cenu/sklad existujúcej odmeny, tlačidlo "Okamžite doplniť sklad na maximum (Restock Now)", prepínač Aktívna/Pozastavená a vymazanie odmeny.
    - Questy (`Quest` a `ClassQuest`): Kompletné pridávanie, úprava a mazanie osobných (Daily/Weekly/Monthly) aj kolektívnych triednych výziev, vrátane tlačidla na manuálne vyhodnotenie a rozdelenie odmien triede.
    - Triedy a Licencie (`SchoolClass`, `SubscriptionLicense`): Vytvorenie novej triedy s vlastným kódom, generovanie nových EDU/PRO licenčných kľúčov, priradenie študenta do triedy, zobrazenie detailného profilu konkrétneho žiaka (`student_detail.html`) s celou jeho históriou odovzdaných kódov a možnosťou napísať mu Code Review komentár (`teacher_comment`).

--------------------------------------------------------------------------------
FÁZA 7 (PRIORITA #2): MASÍVNE ROZŠÍRENIE VZDELÁVACIEHO KURIKULA (140+ HODÍN, 12 MODULOV, 60+ LEKCIÍ, 120+ CVIČENÍ)
--------------------------------------------------------------------------------
Cieľ: Platforma musí pôsobiť ako plnohodnotná stredoškolská a prípravná akademická platforma s desiatkami až stovkami hodín reálneho študijného materiálu.
Architektúra: Aby nebol `seed_codoro.py` jeden neprehľadný súbor, vytvoriť priečinok `courses/curriculum/` s 12 samostatnými dátovými súbormi, ktoré `seed_codoro.py` naimportuje a vloží do databázy. Každá lekcia musí obsahovať hĺbkový teoretický výklad v Markdowne (vysvetlenie pojmov, schémy v texte, viacero komentovaných ukážok kódu, časté chyby začiatočníkov a zhrnutie), viacero praktických cvičení (stupňovaných: EASY -> MEDIUM -> HARD) s minimálne 3 `TestCase` testami na cvičenie (vrátane aspoň 1 skrytého testu `is_hidden=True`) a viacero kvízových otázok (`QuizQuestion`).

Zoznam 12 modulov kurikula (spolu 146 odhadovaných hodín výučby, 100 % SK + EN):
- MODUL 1: Úvod do algoritmizácie, premenné a základné dátové typy (10 hodín, FREE)
  * Lekcia 1.1: Prvý program, funkcia `print()`, komentáre a formátovanie výstupu (`sep`, `end`).
  * Lekcia 1.2: Premenné, pravidlá pomenovania (PEP 8) a priraďovací operátor.
  * Lekcia 1.3: Základné dátové typy (`int`, `float`, `str`, `bool`) a funkcia `type()`.
  * Lekcia 1.4: Pretypovanie (Type Casting) a spracovanie vstupu od používateľa.
  * Lekcia 1.5: Zhrnutie modulu a praktické mini-projekty s výpočtami.

- MODUL 2: Operátory, matematické výrazy a pokročilá práca s reťazcami (12 hodín, FREE)
  * Lekcia 2.1: Aritmetické operátory, celočíselné delenie `//`, zvyšok po delení `%` a umocňovanie `**`.
  * Lekcia 2.2: Porovnávacie a logické operátory (`and`, `or`, `not`), priorita operátorov.
  * Lekcia 2.3: Indexovanie a rezanie reťazcov (String Slicing `[start:stop:step]`).
  * Lekcia 2.4: Vstavané metódy reťazcov (`upper`, `lower`, `strip`, `replace`, `split`, `join`, `find`).
  * Lekcia 2.5: Moderné formátovanie textu pomocou `f-strings` a zaokrúhľovanie čísel.

- MODUL 3: Vetvenie programu a rozhodovacia logika (10 hodín, FREE)
  * Lekcia 3.1: Podmienka `if` a bloková štruktúra kódu pomocou odsadenia (Indentation).
  * Lekcia 3.2: Dvojcestné a viaccestné vetvenie (`if - elif - else`).
  * Lekcia 3.3: Vnorené podmienky a kombinovanie zložených logických výrazov.
  * Lekcia 3.4: Ternárny operátor (jednoriadkový `if-else`) a pravdivostné hodnoty objektov (Truthy / Falsy).
  * Lekcia 3.5: Štrukturálne porovnávanie vzorov (`match - case` v modernom Pythone).

- MODUL 4: Cykly, iterácie a spracovanie postupností (14 hodín, FREE)
  * Lekcia 4.1: Cyklus s pevným počtom opakovaní (`for`) a generátor `range()`.
  * Lekcia 4.2: Akumulátory, počítadlá, výpočet súčtov, priemerov a hľadanie extrémov v cykle.
  * Lekcia 4.3: Podmienený cyklus `while` a prevencia nekonečných cyklov.
  * Lekcia 4.4: Riadenie behu cyklu: príkazy `break`, `continue` a vetva `else` pri cykloch.
  * Lekcia 4.5: Vnorené cykly (2D mriežky, kombinatorika, generovanie obrazcov a tabuliek).

- MODUL 5: Funkcie, modularita a rekurzívne algoritmy (14 hodín, FREE)
  * Lekcia 5.1: Definícia funkcie (`def`), parametre, argumenty a príkaz `return`.
  * Lekcia 5.2: Predvolené hodnoty parametrov, pomenované argumenty (Keyword Arguments) a `None`.
  * Lekcia 5.3: Oblasť platnosti premenných (Local vs. Global Scope) a čisté funkcie (Pure Functions).
  * Lekcia 5.4: Variabilný počet argumentov (`*args`, `**kwargs`) a anonymné `lambda` funkcie.
  * Lekcia 5.5: Rekurzia v Pythone – základný prípad, rekurzívny krok, faktoriál, Fibonacci a GCD.

- MODUL 6: Dátové štruktúry I – Zoznamy (`list`), N-tice (`tuple`) a matice (14 hodín, FREE)
  * Lekcia 6.1: Zoznamy (`list`) – vytváranie, indexovanie, zmena prvkov (mutabilita) a slicing.
  * Lekcia 6.2: Metódy zoznamov (`append`, `extend`, `insert`, `pop`, `remove`, `sort`, `reverse`).
  * Lekcia 6.3: Funkcie `enumerate()`, `zip()`, `map()`, `filter()` a agregácie (`sum`, `min`, `max`, `len`).
  * Lekcia 6.4: List Comprehensions – elegantné generovanie a filtrovanie zoznamov v jednom riadku.
  * Lekcia 6.5: N-tice (`tuple`), rozbaľovanie (Unpacking) a dvojrozmerné zoznamy (2D matice).

- MODUL 7: Dátové štruktúry II – Slovníky (`dict`), Množiny (`set`) a JSON dáta (12 hodín, FREE)
  * Lekcia 7.1: Slovníky (`dict`) – páry kľúč-hodnota, rýchle vyhľadávanie $O(1)$ a metóda `.get()`.
  * Lekcia 7.2: Iterovanie cez slovníky (`.keys()`, `.values()`, `.items()`) a Dict Comprehensions.
  * Lekcia 7.3: Vnorené slovníky a zoznamy slovníkov (reprezentácia databázových záznamov a JSON).
  * Lekcia 7.4: Množiny (`set`) – unikátnosť prvkov a množinové operácie (zjednotenie, prienik, rozdiel).
  * Lekcia 7.5: Praktická analytika dát: frekvenčná analýza textu a zoskupovanie záznamov.

- MODUL 8: Ošetrovanie výnimiek, ladenie kódu a spracovanie textových súborov (10 hodín, FREE)
  * Lekcia 8.1: Syntaktické chyby vs. behové výnimky (`ValueError`, `TypeError`, `IndexError`, `KeyError`, `ZeroDivisionError`).
  * Lekcia 8.2: Zachytávanie výnimiek pomocou blokov `try - except - else - finally`.
  * Lekcia 8.3: Vyvolanie vlastnej výnimky príkazom `raise` a defenzívne programovanie (validácia vstupov).
  * Lekcia 8.4: Práca s dátovými prúdmi a CSV/TXT formátom v pamäti (parsovanie tabuliek a logov).

- MODUL 9: Objektovo-orientované programovanie I – Triedy a zapuzdrenie (12 hodín, PRO / EDU)
  * Lekcia 9.1: Paradigma OOP – trieda (`class`) ako predpis a inštancia (objekt) v pamäti.
  * Lekcia 9.2: Konštruktor `__init__`, parameter `self` a inštančné atribúty.
  * Lekcia 9.3: Inštančné metódy a interakcia medzi viacerými objektmi.
  * Lekcia 9.4: Triedne atribúty vs. inštančné atribúty, dekorátory `@classmethod` a `@staticmethod`.
  * Lekcia 9.5: Zapuzdrenie (Encapsulation), súkromné atribúty a dekorátor `@property` (gettery a settery).

- MODUL 10: Objektovo-orientované programovanie II – Dedičnosť a polymorfizmus (12 hodín, PRO / EDU)
  * Lekcia 10.1: Dedičnosť tried (Inheritance), nadradená a odvodená trieda, funkcia `super()`.
  * Lekcia 10.2: Prekrývanie metód (Method Overriding) a polymorfizmus v praxi.
  * Lekcia 10.3: Magické (Dunder) metódy: `__str__`, `__repr__`, `__len__`, `__eq__`, `__lt__` a preťažovanie operátorov.
  * Lekcia 10.4: Kompozícia vs. dedičnosť a dátové triedy (`@dataclass`).

- MODUL 11: Klasické algoritmy, časová zložitosť a matematika (14 hodín, PRO / EDU)
  * Lekcia 11.1: Úvod do časovej a pamäťovej zložitosti algoritmov (Big-O notácia: $O(1)$, $O(\log n)$, $O(n)$, $O(n^2)$).
  * Lekcia 11.2: Vyhľadávacie algoritmy – Sekvenčné vyhľadávanie vs. Binárne vyhľadávanie (Binary Search).
  * Lekcia 11.3: Základné triediace algoritmy – Bubble Sort, Selection Sort a Insertion Sort.
  * Lekcia 11.4: Efektívne triedenie (Merge Sort / QuickSort) a vlastné kľúče triedenia (`key=lambda`).
  * Lekcia 11.5: Číselné a kryptografické algoritmy – Eratostenovo sito (prvočísla), Caesarova šifra, validácia Luhn/IBAN.

- MODUL 12: Praktické projekty a algoritmické Boss výzvy (12 hodín, PRO / EDU)
  * Lekcia 12.1: Projekt 1 – Elektronická žiacka knižka a štatistický analyzátor známok triedy.
  * Lekcia 12.2: Projekt 2 – Skladový a objednávkový e-shop engine s kupónmi a DPH.
  * Lekcia 12.3: Projekt 3 – Textový kompresor (Run-Length Encoding) a analyzátor hesiel.
  * Lekcia 12.4: Projekt 4 – Simulátor bankového účtu a transakčného auditu v OOP.
  * Lekcia 12.5: Záverečný Boss Test – Komplexná certifikačná skúška Python vývojára.

--------------------------------------------------------------------------------
FÁZA 8 (PRIORITA #3): POKROČILÁ NAVIGÁCIA V CVIČENIACH, TRÉNINGOVÁ ARÉNA A PROFIL ŠTUDENTA
--------------------------------------------------------------------------------
8.1 Prepínanie viacerých cvičení v rámci jednej lekcie (`lesson_detail.html`):
    - Keďže každá lekcia má viacero cvičení (napr. 3 úlohy: Ľahká, Stredná, Ťažká), v pravom paneli nad editorom kódu pridať prehľadný prepínač cvičení lekcie (Tabs: `Úloha 1 [✓]`, `Úloha 2`, `Úloha 3 [Boss]`), aby študent plynule prechádzal všetkými úlohami danej lekcie.
    - Po úspešnom vyriešení úlohy (`PASSED`) zobraziť študentovi aj rozbaľovací blok s vysvetlením vzorového riešenia (`explanation_sk/en`) a tlačidlo "Pokračovať na ďalšiu úlohu / ďalšiu lekciu".

8.2 Samostatná podstránka "Tréningová Aréna / Katalog úloh" (`/arena/`):
    - Študent si môže kedykoľvek otvoriť katalóg všetkých praktických cvičení z celej platformy s filtrovaním podľa:
      * Obťažnosti (`EASY`, `MEDIUM`, `HARD`),
      * Modulu (1 až 12),
      * Stavu (`Nevyriešené`, `Vyriešené`).
    - Slúži na precvičovanie pred písomkou a plnenie Daily/Weekly/Class questov.

8.3 Podstránka "Môj Profil, Odznaky a Certifikát" (`/profile/`):
    - Prehľad celkového počtu odštudovaných hodín, celkovej úspešnosti odovzdaných riešení ( v %), zoznam získaných a zamknutých odznakov (`Badge`) a generovanie oficiálneho certifikátu Codoro Python Developer (s menom študenta, dátumom, úrovňou a unikátnym ID kódom certifikátu).
================================================================================