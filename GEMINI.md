================================================================================
CODORO - MASTER PROJECT CONTEXT & SPECIFICATION (PRE ANTIGRAVITY IDE AGENT)
================================================================================

1. OFICIÁLNE ZADANIE MATURITNEJ PRÁCE A IDENTIFIKÁCIA PROJEKTU
--------------------------------------------------------------------------------
- Číslo a názov témy: Téma č. 22 (trieda IV.C) - Webová platforma na výučbu Pythonu s registráciou používateľov[cite: 1]
- Podtitul práce: Návrh a implementácia gamifikovaného vzdelávacieho systému Codoro
- Študijný odbor: 2697 K mechanik elektrotechnik / čka - oblasť vzdelávania Informačno-mediálne technológie[cite: 1]
- Forma práce: B - obhajoba vlastného projektu (PČOZ MS v zmysle vyhlášky MŠVVaŠ SR 224/2022 Z. z. podľa § 15 odst. 11 písm. b)[cite: 1, 2]
- Škola: Spojená škola, Hattalova 471, 027 43 Nižná (Organizačná zložka SOŠ Technická), rok obhajoby 2027[cite: 2]
- Konzultant maturitnej práce: Mgr. Markéta Brišová[cite: 1]
- Autor projektu: Juraj Volf
- Lokálna cesta projektu: C:\Users\jurvox\codoro[cite: 3]
- GitHub repozitár: https://github.com/jurajvolf/codoro.git[cite: 3]
- Oficiálny text zadania: Webová aplikácia slúžiaca ako vzdelávacia platforma na výučbu programovania v jazyku Python[cite: 1]. Registrovaní používatelia majú prístup k lekciám a praktickým cvičeniam, systém umožňuje kontrolu ich riešení[cite: 1]. Učiteľ má samostatné administrátorské rozhranie na správu obsahu a používateľov[cite: 1]. Nástroje a technológie: webový framework (Python/Django), databáza (SQLite/PostgreSQL), HTML/CSS/JavaScript, systém autentifikácie používateľov[cite: 1].


2. IDENTITA ZNAČKY "CODORO" A KONKURENČNÉ VÝHODY (USP PRE OBHAJOBU)
--------------------------------------------------------------------------------
- Názov platformy: Codoro[cite: 4]
  * Pôvod slova: Spojenie slov "Code" (kód), "Oro" (zlato po španielsky - odkaz na hernú ekonomiku) a techniky efektívneho učenia "Pomodoro" / tréningového centra "Dojo".
  * Rešerš ochranných známok (TMview): Názov Codoro bol overený v databáze TMview (existujúce záznamy sú len v potravinárskom priemysle, triedy pre vzdelávací softvér sú voľné).
  * Architektonická škálovateľnosť: Názov zámerne neobsahuje predponu "Py-", čo spolu so stĺpcom `programming_language` v databázovom modeli `Module` umožňuje kedykoľvek rozšíriť platformu o ďalšie jazyky (JavaScript, SQL, C++) bez zmeny databázovej schémy a názvu značky.
- Názov virtuálnej meny: Doros (zlaté mince získavané za aktivitu a riešenie úloh).
- Maskot a AI Tútor: Codo (postavička v modro-fialovej kapucni s laptopom `</>` a svietiacimi azúrovými očami z oficiálneho loga projektu)[cite: 4].

- 4 hlavné piliere, ktorými sa Codoro líši od platforiem ako Duolingo, Codecademy či W3Schools:
  1. Prepojenie Študent - Trieda - Učiteľ (Classroom Ecosystem): Bežné platformy sú pre samoukov. Codoro spája žiakov do reálnych školských tried (`SchoolClass`), kde plnia spoločné triedne výzvy a učiteľ vidí ich živý progres a odovzdané kódy[cite: 1].
  2. Sokratovský AI Tútor Codo: Bežné AI (ChatGPT) napíše žiakovi hotový kód, čím sa žiak nič nenaučí. Codo má striktnú systémovú inštrukciu nikdy nenapísať hotové riešenie - iba analyzuje chybu vo výstupe testov a navedie študenta otázkou na správny riadok a logiku (v SK alebo EN).
  3. Reálna školská ekonomika s riadením zásob (Stock & Restock Marketplace): Mince Doros nie sú len virtuálne čísla. Učiteľ v obchode vypisuje reálne školské výhody (napr. odpustenie domácej úlohy, +10 % bodov k písomke, nápoveda na teste) s prísne obmedzeným skladom pre triedu (napr. 2 ks na týždeň), aby nedošlo k inflácii a hromadnému vykúpeniu.
  4. Plná dvojjazyčnosť (100 % SK / EN): Celé používateľské rozhranie, databázový obsah lekcií, cvičení, questov, odmien v obchode aj odpovede AI tútora Codo sú plne dostupné v slovenčine aj v angličtine (pre zahraničných študentov).


3. TECHNOLOGICKÝ STACK A PRÍKAZY PROSTREDIA
--------------------------------------------------------------------------------
- Backend: Python 3 + Django (architektúra MVT - Model, View, Template)[cite: 1].
- Databáza: SQLite (`db.sqlite3`) pre vývoj, plne kompatibilné s PostgreSQL cez Django ORM[cite: 1].
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
  3. Naplnenie ukážkových dát: `python seed_codoro.py`
  4. Spustenie vývojového servera: `python manage.py runserver`
  5. Testovacie účty vytvorené cez seed:
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
|-- accounts/                   # Modul používateľov, rolí, tried, jazyka a licencií
|   |-- models.py               # User, SchoolClass, SubscriptionLicense
|   |-- views.py                # login, register, logout, switch_language, repair_streak, activate_license
|   |-- admin.py
|-- courses/                    # Modul výučby Pythonu, cvičení, kvízov a AI tútora
|   |-- models.py               # Module, Lesson, Exercise, TestCase, Submission, QuizQuestion, LessonProgress
|   |-- services.py             # evaluate_python_code (sandbox runner), get_codo_ai_feedback (Gemini API + fallback)
|   |-- views.py                # dashboard, lesson_detail (spúšťanie kódu, kvízy, pripisovanie XP/Doros/Questov)
|   |-- admin.py
|-- gamification/               # Modul hernej ekonomiky, obchodu so skladom, questov a Coin Dropov
|   |-- models.py               # RewardItem, RewardPurchase, DorosTransaction, Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution, CoinDrop, CoinDropClaim, Badge, StudentBadge
|   |-- views.py                # shop_view, buy_reward, claim_quest_reward, claim_coin_drop
|   |-- admin.py
|-- teacher_panel/              # Vlastné administrátorské rozhranie pre učiteľa (mimo Django admina)
|   |-- views.py                # teacher_dashboard, manage_student_economy, process_coupon, create_reward_item, create_coin_drop, create_exercise
|-- templates/                  # HTML šablóny
|   |-- base.html               # Hlavný layout, CSS premenné (Light/Dark), navigácia, skripty pre tému a Markdown
|   |-- accounts/
|   |   |-- login.html          # Prihlásenie + rýchle demo tlačidlá (Študent / Učiteľ)
|   |   |-- register.html       # Registrácia so štartovacím bonusom +100 Doros a kódom triedy
|   |-- courses/
|   |   |-- dashboard.html      # Študentský prehľad, Streak repair, Live Coin Drop, Kolektívny quest, Moduly, Osobné questy, Rebríček
|   |   |-- lesson_detail.html  # Split-screen pracovisko: Teória + Kvíz vľavo, CodeMirror Python editor + Testy + Codo AI vpravo
|   |-- gamification/
|   |   |-- shop.html           # Školský obchod so skladovými zásobami, aktivácia EDU licencie, zakúpené kupóny, história peňaženky
|   |-- teacher_panel/
|       |-- dashboard.html      # Učiteľské štúdio rozdelené do 3 záložiek (Študenti a kupóny | Obchod a Coin Dropy | Cvičenia a riešenia)
|-- static/
|   |-- img/
|       |-- codoro-logo.jpg     # Oficiálne logo projektu Codoro (s automatickým SVG fallbackom v šablónach)
|-- seed_codoro.py              # Skript na automatické naplnenie databázy ukážkovými dátami
|-- requirements.txt            # Závislosti projektu
|-- manage.py
|-- GEMINI.md                   # Tento dokument


5. KOMPLETNÁ DATABÁZOVÁ SCHÉMA A BIZNIS LOGIKA (15 MODELOV)
--------------------------------------------------------------------------------
A. Aplikácia `accounts`:
1. `SchoolClass`:
   - Polia: `name` (napr. IV.C), `join_code` (unikátny kód triedy, napr. IVC-2027), `teacher` (FK na User), `created_at`.
2. `User` (dedí z `AbstractUser`):
   - Rola a lokalizácia: `role` (STUDENT / TEACHER), `school_class` (FK na SchoolClass), `preferred_language` (sk / en).
   - Predplatné (Freemium SaaS model): `subscription_tier` (FREE / PRO / EDU), `daily_ai_hints_used`, `last_ai_hint_date`.
   - Gamifikácia: `xp`, `level`, `doros`.
   - Matematický vzorec pre Level (použitý aj v Zozname rovníc v dokumentácii):
     XP potrebné na úroveň: `XP = 100 * (Level - 1)^1.5`, resp. pre ďalší level `100 * Level^1.5`.
     Pri každom postupe na vyšší level (`add_xp_and_check_level_up`) dostane študent automaticky bonus `Nový_Level * 50 Doros`.
   - Denný Streak a záchrana: `current_streak`, `longest_streak`, `last_activity_date`, `streak_freezes`, `lost_streak_value` (hodnota vyhasnutej série, ktorú možno zachrániť za 200 Doros), `streak_lost_at`.
3. `SubscriptionLicense`:
   - Polia: `code` (napr. EDU-2027-IVC), `tier` (PRO / EDU), `max_uses`, `current_uses`, `is_active`, `created_at`.

B. Aplikácia `courses`:
4. `Module`:
   - Polia: `title_sk`, `title_en`, `description_sk`, `description_en`, `programming_language` (python / javascript / sql), `order`, `is_pro_only` (uzamyká pokročilé moduly pre FREE účty), `icon_name`.
5. `Lesson`:
   - Polia: `module` (FK), `title_sk`, `title_en`, `content_sk` (Markdown), `content_en` (Markdown), `order`, `xp_reward`.
6. `Exercise`:
   - Polia: `lesson` (FK), `title_sk`, `title_en`, `instructions_sk` (Markdown), `instructions_en` (Markdown), `starter_code`, `solution_code`, `hint_sk`, `hint_en`, `hint_cost_doros`, `difficulty` (EASY / MEDIUM / HARD), `xp_reward`, `doros_reward` (plná odmena na 1. pokus, polovičná na ďalšie pokusy), `order`.
7. `TestCase`:
   - Polia: `exercise` (FK), `input_data`, `expected_output`, `test_code` (Python `assert` príkaz spúšťaný v izolovanom podprocese s timeoutom 3 sekundy a kontrolou zakázaných importov `os`, `sys`, `subprocess`, `shutil`, `open`, `eval`, `exec`), `is_hidden` (skrytý test proti natvrdo napísaným odpovediam).
8. `Submission`:
   - Polia: `student` (FK), `exercise` (FK), `submitted_code`, `status` (PASSED / FAILED / ERROR), `output_log`, `ai_tutor_feedback` (odpoveď od AI tútora Codo), `teacher_comment` (pre Code Review od učiteľa), `created_at`.
9. `QuizQuestion`:
   - Polia: `lesson` (FK), `question_sk`, `question_en`, `option_a_sk/en`, `option_b_sk/en`, `option_c_sk/en`, `correct_option` (A/B/C).
10. `LessonProgress`:
    - Polia: `student` (FK), `lesson` (FK), `is_completed`, `completed_at`.

C. Aplikácia `gamification`:
11. `RewardItem` (Školský obchod s riadením skladových zásob):
    - Polia: `title_sk`, `title_en`, `description_sk`, `description_en`, `cost_doros`, `icon_name`, `max_stock` (maximálny sklad pre triedu), `current_stock` (aktuálny zostatok), `restock_period` (DAILY - každých 24h / WEEKLY - každých 7 dní / MONTHLY - každých 30 dní / MANUAL), `limit_per_student_per_period`, `last_restocked_at`, `created_by`, `is_active`.
    - Metóda `check_and_restock()` automaticky porovná `timezone.now()` s `last_restocked_at` a pri uplynutí intervalu doplní `current_stock = max_stock`. Pri nákupe sa používa databázový zámok `select_for_update()`, aby dvaja žiaci nemohli kúpiť posledný kus v tej istej milisekunde.
12. `RewardPurchase` (Zakúpené kupóny):
    - Polia: `student` (FK), `reward` (FK), `coupon_code` (unikátny kód `CDR-XXXXXX`), `cost_paid`, `status` (PENDING - čaká na uplatnenie u učiteľa / REDEEMED - uplatnené na hodine / REFUNDED - zamietnuté učiteľom s automatickým vrátením Doros aj skladu), `purchased_at`, `processed_at`, `processed_by`.
13. `DorosTransaction` (Audit Log peňaženky):
    - Polia: `student` (FK), `amount` (+ príjem / - výdavok), `reason_sk`, `reason_en`, `performed_by_teacher` (ak išlo o manuálny zásah učiteľa), `created_at`.
14. `Quest` & `StudentQuestProgress` (Osobné výzvy):
    - Rozdelenie: `DAILY`, `WEEKLY`, `MONTHLY`, `TEACHER`.
    - Metriky: `SOLVE_EXERCISES`, `EARN_XP`, `FIRST_TRY_SOLVES`, `COMPLETE_LESSONS`.
15. `ClassQuest` & `ClassQuestContribution` (Kolektívne triedne výzvy):
    - Celá trieda spolupracuje na spoločnom cieli (`target_exercises_count`).
    - Politika odmeňovania (`reward_policy`): buď `ALL_STUDENTS` (celá trieda), alebo `CONTRIBUTORS_ONLY` (iba žiaci, ktorí prispeli aspoň `min_contribution_required` vyriešenými úlohami).
16. `CoinDrop` & `CoinDropClaim` (Časované a náhodné bonusové dropy):
    - Učiteľ nastaví časové okno (`available_from` - `available_until`), maximálny počet žiakov (`max_claims`) a interval náhodnej výhry (`min_doros` až `max_doros`).
17. `Badge` & `StudentBadge` (Odznaky za míľniky).


6. PRAVIDLÁ DIZAJNOVÉHO SYSTÉMU A UI/UX (STRIKTNE DODRŽIAVAŤ PRI ÚPRAVÁCH)
--------------------------------------------------------------------------------
1. Zjednotený Light / Dark Mode:
   - Celá stránka sa riadi atribútom `html[data-theme="light"]` alebo `html[data-theme="dark"]` (prepínané tlačidlom v hornej lište a uložené v `localStorage` pod kľúčom `codoro_theme`).
   - NIKDY nemiešať svetlú kartu a tmavú kartu vedľa seba na jednej obrazovke[cite: 5]. Všetky panely (vrátane teoretického výkladu a pravého panela s Python editorom v `lesson_detail.html`) musia používať triedu `.card-surface`, ktorá sa plynule prispôsobuje zvolenému režimu[cite: 5].
   - Prepnutie témy zároveň dynamicky prepne tému CodeMirror editora (`eclipse` pre svetlý režim, `material-darker` pre tmavý režim).
2. Farebná paleta podľa loga Codoro[cite: 4]:
   - Primárna akčná farba (Ro Indigo): `#4636F5` (v tmavom režime `#6366F1`).
   - Polnočná modrá (Codo Navy): `#0F172A` (texty vo svetlom režime / pozadie v tmavom režime).
   - Azúrová (Visor Cyan z očí maskota): `#5CE1E6` / `#0891B2` (akcenty pre AI tútora Codo a odznaky).
3. Formátovanie Markdownu (žiadne surové znaky `###` ani `**` v UI)[cite: 5]:
   - Každý element zobrazujúci text lekcie, zadania úlohy alebo nápovedy musí mať triedy `markdown-content markdown-render`, ktoré pri načítaní spracuje `marked.js`.
4. Bezchybná dvojjazyčnosť (SK / EN):
   - Na začiatku každej šablóny používať bezpečný tag `{% firstof user.preferred_language ui_lang 'sk' as lang %}` (nikdy nepoužívať priamy filter `|default:request.session.ui_lang`, ktorý pri prázdnej session vyhadzuje `VariableDoesNotExist`).
   - Každý novopridaný text, tlačidlo, nadpis alebo prázdny stav v šablóne aj vo `views.py` musí mať slovenskú aj anglickú vetvu (`{% if lang == 'en' %}...{% else %}...{% endif %}`).


7. FÁZOVÝ PLÁN PROJEKTU A ROADMAPA ĎALŠÍCH FUNKCIÍ NA IMPLEMENTÁCIU
--------------------------------------------------------------------------------
- FÁZA 1: Príprava, GitHub repozitár a kostra Django projektu [DOKONČENÉ]
- FÁZA 2: Databázová schéma (15+ modelov) a autentifikácia [DOKONČENÉ]
- FÁZA 3: Základný Učiteľský panel, Študentský dashboard, Editor kódu a Obchod [DOKONČENÉ]
- FÁZA 4 (Aktuálna práca v Antigravity IDE): Rozšírenie funkcií a obsahu aplikácie:
  * 4.1 Rozšírenie obsahu v `seed_codoro.py`: Pridať kompletnú sadu lekcií a cvičení pre všetky hlavné stredoškolské témy (1. Premenné a dátové typy, 2. Podmienky a vetvenie, 3. Cykly for a while, 4. Funkcie a rekurzia, 5. Zoznamy a slovníky, 6. Objektovo-orientované programovanie - PRO/EDU).
  * 4.2 Podstránka "Môj Profil & Odznaky" (`/profile/`): Zobrazenie získaných odznakov (`Badge`), štatistík vyriešených úloh, grafu aktivity, zmeny hesla/avatara a tlačidla na vygenerovanie PDF/HTML Certifikátu o absolvovaní kurzu.
  * 4.3 Platenie za nápovedu v cvičeniach: Ak si študent v cvičení odomkne nápovedu (`hint`), odpočíta sa mu `hint_cost_doros` (iba raz pre danú úlohu) a zapíše sa transakcia.
  * 4.4 Rozšírenie Učiteľského panela (`teacher_panel`):
        - Možnosť pre učiteľa pridať slovný komentár (`teacher_comment` - Code Review) ku konkrétnemu odovzdanému riešeniu žiaka (`Submission`).
        - Formulár pre učiteľa na vytvorenie nového Kolektívneho triedneho questu (`ClassQuest`) a Osobného questu (`Quest`).
- FÁZA 5: Komplexné testovanie a produkčná pripravenosť [DOKONČENÉ]
  * 24 automatizovaných unit a integračných testov prebiehajúcich cez Django Test Runner (100 % pass rate):
    - `courses/tests.py`: Bezpečnosť AST sandboxu (blokovanie zakázaných importov `os`, `sys`, `subprocess`, funkcií `open`, `eval`, `exec`, dunder metód), timeout ochrana pred nekonečnými cyklami, unit test runner cvičení (PASSED / FAILED / ERROR), Sokratovský Codo fallback bez zverejnenia hotového kódu.
    - `accounts/tests.py`: Matematický vzorec progresie úrovní (Rovnica 1), odmeny Doros za level-up, denný Streak, zmrazenia, detekcia prerušenia a záchrana za 200 Doros, aktivácia EDU/PRO licencií a denné kvóty AI rád pre FREE používateľov.
    - `gamification/tests.py`: Skladové hospodárstvo obchodu (odpočítanie skladu, kontrola zostatku Doros, generovanie kupónu CDR-XXXXXX, automatické naskladnenie po expirácii periódy), ClassQuest metriky a sledovanie príspevkov žiakov.
    - `teacher_panel/tests.py`: Ochrana prístupu pre rolu TEACHER, Code Review slovné hodnotenie učiteľa k odovzdanému riešeniu, schvaľovanie a zamietnutie kupónu s refundáciou mincí študentovi.
- FÁZA 6: Vypracovanie 25+ stranovej písomnej dokumentácie a prezentácie na obhajobu (pozastavené na žiadosť používateľa, prioritou je dokonalý UI/UX dizajn a unikátnosť aplikácie).


8. ZÁVÄZNÉ POŽIADAVKY NA PÍSOMNÚ MATURITNÚ PRÁCU (ŠABLÓNA SPOJENÁ ŠKOLA NIŽNÁ)
--------------------------------------------------------------------------------
- Záväzný minimálny rozsah: Minimálne 25 strán vlastného odborného textu, pričom samotné Jadro práce musí mať minimálne 15 strán (v praxi: Úvod 1,5 strany + Jadro cca 22,5 strany + Záver 1,5 strany = 25,5 strany čistého textu)[cite: 2].
- Čo sa DO ROZSAHU 25 STRÁN ZAPOČÍTAVA:
  * Výlučne Úvod (nečíslovaný), Jadro práce (číslované kapitoly 1, 2, 3, 4) a Záver (nečíslovaný)[cite: 2].
- Čo sa DO ROZSAHU 25 STRÁN NEZAPOČÍTAVA:
  * Obálka, Zadanie práce, Abstrakt (100 - 200 slov v jednom odseku + 3 až 5 kľúčových slov), Obsah (musí byť naformátovaný tak, aby sa zmestil celý na stranu 4)[cite: 2], Zoznam ilustrácií/tabuliek/rovníc, Zoznam použitej literatúry (min. 5 knižných a 5 internetových zdrojov citovaných podľa normy)[cite: 2] a Prílohy (rozsiahle výpisy kódu patria do príloh, v jadre uvádzame len kľúčové ukážky algoritmov, schémy a odborný výklad)[cite: 2].

- Schválená štruktúra kapitol maturitnej práce:
  * Úvod (cca 1,5 strany)[cite: 2]
  * 1. Teoretické východiská a analýza problematiky (cca 7 strán)
       1.1 Moderné e-learningové platformy a gamifikácia vo vzdelávaní (analýza konkurencie a vymedzenie prínosu systému Codoro)
       1.2 Programovací jazyk Python vo výučbe algoritmizácie[cite: 1]
       1.3 Architektúra moderných webových aplikácií (Klient-server, HTTP, MVC vs. MVT v Djangu)
       1.4 Prehľad použitých technológií (Python, Django ORM, SQLite/PostgreSQL, HTML5/CSS3/JS, CodeMirror)[cite: 1]
       1.5 Bezpečnosť webových aplikácií a riziká spúšťania používateľského kódu ( autentifikácia, PBKDF2 hashovanie, CSRF, XSS, SQL Injection, sandboxing)[cite: 1]
  * 2. Analýza požiadaviek a návrh systému Codoro (cca 6 strán)
       2.1 Špecifikácia funkčných a nefunkčných požiadaviek (Modul Študent, Modul Učiteľ, Modul AI Tútor Codo)[cite: 1]
       2.2 Prípady použitia (Use-Case diagram a scenáre používania)
       2.3 Návrh dátového modelu a relačnej databázy (ER diagram a detailný opis 15 tabuliek)
       2.4 Matematický návrh hernej ekonomiky, progresie úrovní (Rovnica 1: výpočet XP) a riadenia zásob v obchode[cite: 2]
       2.5 Návrh používateľského rozhrania, typografie a farebnej identity (Light/Dark systém, dvojjazyčnosť SK/EN)
  * 3. Implementácia webovej platformy (cca 7 strán)
       3.1 Štruktúra projektu, konfigurácia Django a verzionovanie cez Git/GitHub
       3.2 Implementácia používateľského modelu, rolí, tried a licenčného systému (`accounts`)[cite: 1]
       3.3 Realizácia vzdelávacieho modulu, interaktívneho editora a automatizovaného testovacieho enginu (`courses`)[cite: 1]
       3.4 Integrácia Sokratovského AI tútora Codo pomocou Google Gemini API
       3.5 Implementácia gamifikácie: Osobné a kolektívne questy, časované Coin Dropy a skladový obchod s atomickými transakciami (`gamification`)
       3.6 Implementácia vlastného učiteľského administrátorského rozhrania (`teacher_panel`)[cite: 1]
  * 4. Testovanie, nasadenie a zhodnotenie (cca 3 strany)
       4.1 Metodika testovania a testovacie scenáre (funkčné testy, testy bezpečnosti sandboxu a timeoutov)
       4.2 Nasadenie aplikácie do produkčného prostredia a metodická príručka pre učiteľa a študenta
  * Záver (cca 1,5 strany)[cite: 2]
================================================================================