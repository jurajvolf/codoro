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
  4. Plná dvojjazyčnosť (100 % SK / EN): Celé používateľské rozhranie, databázový obsah lekcií, cvičení, questov, ťahákov, odmien v obchode aj odpovede AI tútora Codo sú plne dostupné v slovenčine aj v angličtine.


3. TECHNOLOGICKÝ STACK A PRÍKAZY PROSTREDIA
--------------------------------------------------------------------------------
- Backend: Python 3 + Django (architektúra MVT - Model, View, Template).
- Databáza: SQLite (`db.sqlite3`) pre vývoj, plne kompatibilné s PostgreSQL cez Django ORM.
- Frontend: Vlastný moderný CSS Design System v `templates/base.html` (bez závislosti na externých CSS frameworkoch), responzívny CSS Grid/Flexbox, akordeónové komponenty, záložkové prepínače (Tabs), modálne okná, plynulé animácie (`cubic-bezier`), podpora Light/Dark režimu.
- Typografia: Google Fonts s plnou podporou slovenskej diakritiky (`subset=latin-ext`):
  * Nadpisy: `Plus Jakarta Sans` (weights 600, 700, 800)
  * Text a UI: `Inter` (weights 400, 500, 600, 700)
  * Kód a číselné metriky: `JetBrains Mono` (weights 400, 500, 600, 700)
- Integrovaný editor kódu: `CodeMirror 5.65.16` (režim `python`, téma `eclipse` pre svetlý režim a `material-darker` pre tmavý režim).
- Renderovanie Markdownu: Knižnica `marked.js` automaticky formátuje texty lekcií, zadaní a nápovied s triedou `.markdown-content.markdown-render`.
- AI integrácia: Google Gemini API (`gemini-2.5-flash` cez premennú prostredia `GEMINI_API_KEY`) + deterministický lokálny Sokratovský fallback v `courses/services.py`.

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
|   |-- settings.py
|   |-- urls.py
|-- accounts/                   # Používatelia, roly, triedy, jazyk, profil a certifikáty
|   |-- models.py               # User, SchoolClass, SubscriptionLicense
|   |-- views.py                # login, register, logout, switch_language, repair_streak, activate_license, profile_view, certificate_view
|   |-- tests.py
|-- courses/                    # Výučba Pythonu, cvičenia, kvízy, aréna, ťaháky a AI tútor
|   |-- models.py               # Module, Lesson, Exercise, TestCase, Submission, QuizQuestion, LessonProgress, UnlockedHint
|   |-- services.py             # evaluate_python_code, get_codo_ai_feedback, generate_ai_exercise, translate_content_ai
|   |-- views.py                # dashboard, lesson_detail, practice_arena, cheat_sheets_view, unlock_hint
|   |-- curriculum/             # Balík s modulárnymi dátami kurikula (18 modulov, 220+ hodín obsahu)
|   |   |-- __init__.py
|   |   |-- mod01_basics.py ... až ... mod18_graduation_projects.py
|   |   |-- cheatsheets_data.py # Štruktúrované ťaháky a slovník pojmov Pythonu (SK/EN)
|   |-- tests.py
|-- gamification/               # Herná ekonomika, obchod so skladom, questy a Coin Dropy
|   |-- models.py               # RewardItem, RewardPurchase, DorosTransaction, Quest, StudentQuestProgress, ClassQuest, ClassQuestContribution, CoinDrop, CoinDropClaim, Badge, StudentBadge
|   |-- views.py                # shop_view, buy_reward, claim_quest_reward, claim_coin_drop
|   |-- tests.py
|-- teacher_panel/              # Kompletný CMS a administrátorské rozhranie pre učiteľa (Full CRUD)
|   |-- views.py
|   |-- tests.py
|-- admin_panel/                # SuperAdmin rozhranie, Live Support Helpdesk, správa licencií a údržba DB
|   |-- views.py
|   |-- urls.py
|   |-- tests.py
|-- templates/                  # HTML šablóny (100 % SK/EN, Light/Dark mode, App Shell architektúra)
|   |-- base.html
|   |-- accounts/               # login.html, register.html, profile.html, certificate.html
|   |-- courses/                # dashboard.html, lesson_detail.html, practice_arena.html, cheat_sheets.html
|   |-- gamification/           # shop.html
|   |-- teacher_panel/          # dashboard.html, cms_modules.html, cms_lesson_form.html, cms_exercise_form.html, student_detail.html
|   |-- admin_panel/            # dashboard.html
|-- static/img/codoro-logo.jpg
|-- seed_codoro.py
|-- manage.py
|-- GEMINI.md


5. PRAVIDLÁ DIZAJNOVÉHO SYSTÉMU A ŠTRUKTÚRY UI/UX (STRIKTNE DODRŽIAVAŤ)
--------------------------------------------------------------------------------
1. ZÁKAZ NEKONEČNÉHO SCROLLOVANIA ("ENDLESS WALL OF CONTENT"):
   - Je prísne zakázané vykresľovať všetky moduly, lekcie, formuláre alebo tabuľky otvorené pod sebou na jednej dlhej stránke.
   - Každá obrazovka musí využívať progresívne odhaľovanie obsahu (Progressive Disclosure):
     * Prepínacie záložky (Tabs / Segmented Pills),
     * Zbaliteľné akordeóny (Collapsible Accordions - predvolene je rozbalený len 1 aktívny prvok, ostatné sú zbalené),
     * Vyhľadávacie pole a filtre v reálnom čase (Search & Filter),
     * Modálne okná (Modals / Drawers) pre formuláre na tvorbu/úpravu položiek.
2. Zjednotený Light / Dark Mode:
   - Celá stránka sa riadi atribútom `html[data-theme="light"]` alebo `html[data-theme="dark"]` (uložené v `localStorage` pod kľúčom `codoro_theme`).
   - Nikdy nemiešať svetlú kartu a tmavú kartu vedľa seba na jednej obrazovke.
   - Prepnutie témy zároveň dynamicky prepne tému CodeMirror editora (`eclipse` pre svetlý režim, `material-darker` pre tmavý režim).
3. Farebná paleta podľa loga Codoro:
   - Primárna akčná farba (Ro Indigo): `#4636F5` (v tmavom režime `#6366F1`).
   - Polnočná modrá (Codo Navy): `#0F172A`.
   - Azúrová (Visor Cyan): `#5CE1E6` / `#0891B2`.
4. Formátovanie Markdownu a 100 % Dvojjazyčnosť (SK / EN):
   - Všetky texty lekcií, zadaní a nápovied musia mať triedy `markdown-content markdown-render` spracované cez `marked.js`.
   - Na začiatku každej šablóny používať bezpečný tag `{% firstof user.preferred_language ui_lang 'sk' as lang %}`.


6. DOTERAJŠÍ STAV A ŠPECIFIKÁCIA NOVÝCH FÁZ (FÁZA 9, 10 A 11)
--------------------------------------------------------------------------------
- FÁZA 1 až 8: Základná architektúra, databáza, autentifikácia, Sokratovský AI tútor, CMS základy, aréna, profil a unit testy [DOKONČENÉ]

--------------------------------------------------------------------------------
FÁZA 9 (PRIORITA #1): REARCHITEKTÚRA UI/UX PROTI NEKONEČNÉMU SCROLLOVANIU
--------------------------------------------------------------------------------
Cieľ: Prebudovať rozloženie obrazoviek tak, aby bola aplikácia maximálne prehľadná, štruktúrovaná, intuitívna a vizuálne rozdelená do logických celkov bez nutnosti dlhého scrollovania nadol.

9.1 Študentský Dashboard (`templates/courses/dashboard.html`) - Štruktúrovaný Hub:
    - A) Horná sekcia "Pokračovať v štúdiu (Continue Learning Hero Card)":
         Kompaktný, výrazný panel na vrchu, ktorý zobrazuje poslednú neukončenú (alebo nasledujúcu odporúčanú) lekciu študenta, celkový progres kurzu v % (Progress Bar) a veľké tlačidlo "Pokračovať v lekcii X.Y". Ak prebieha Live Coin Drop alebo záchrana Streaku, zobrazí sa ako kompaktná horná lišta.
    - B) Filtrovanie podľa Kariérnych ciest (5 Learning Tracks Tabs) + Vyhľadávanie:
         Nad modulmi vytvoriť horizontálny prepínač kategórií (Segmented Tabs) a vyhľadávacie pole (`Hľadať lekciu alebo tému...`):
         * `Všetky cesty (All Tracks)`
         * `1. Základy a Logika (Moduly 1 - 4)`
         * `2. Funkcie a Dátové štruktúry (Moduly 5 - 8)`
         * `3. OOP a Softvérové inžinierstvo (Moduly 9 - 10)`
         * `4. Algoritmy, Dáta a Bezpečnosť (Moduly 11 - 15)`
         * `5. Maturitný špeciál a Projekty (Moduly 16 - 18)`
    - C) Zbaliteľné akordeóny modulov (Collapsible Module Accordions):
         ZÁKAZ zobrazovať všetky lekcie všetkých modulov naraz otvorené!
         Každý modul je čistá, klikateľná hlavička akordeónu, ktorá zobrazuje:
         - Číslo a názov modulu, odznak obťažnosti, odhadovaný čas (napr. `14h`) a príznak `FREE` / `PRO-EDU`.
         - Ukazovateľ progresu v module (napr. `3 / 5 dokončených lekcií` + mini progress bar).
         - Tlačidlo/šípku na rozbalenie (`▼`).
         Predvolene je rozbalený IBA prvý nedokončený modul študenta. Kliknutím na hlavičku ktoréhokoľvek iného modulu sa plynule rozbalí jeho zoznam lekcií (a ostatné sa môžu zbaliť).
    - D) Pravý bočný panel (Sticky Sidebar s prepínacími kartami):
         Namiesto dlhého stĺpca pod sebou bude mať pravý panel na Dashboarde 3 čisté prepínacie záložky (Tabs) v jednej karte:
         * Záložka `🎯 Osobné výzvy` (s pod-filtrami Daily / Weekly / Monthly),
         * Záložka `🤝 Triedny Quest` (spoločný cieľ triedy IV.C a top prispievatelia),
         * Záložka `🏆 Rebríček` (Top študenti triedy).

9.2 Pracovisko lekcie (`templates/courses/lesson_detail.html`) - Profesionálne Split-Screen IDE:
    - Celá obrazovka lekcie musí fungovať ako moderné dvojpanelové IDE (v štýle LeetCode / Codecademy) bez zbytočného scrollovania celej stránky:
    - Horná pod-navigácia lekcie (Breadcrumb Bar):
      * Tlačidlo `← Späť na prehľad`, vysúvacie menu `📑 Obsah modulu (Rýchly preskok na inú lekciu v module)`, názov aktuálnej lekcie a tlačidlá `Predchádzajúca lekcia` / `Ďalšia lekcia →`.
    - Ľavý panel (Samostatne scrollovateľný panel s 3 vnútornými záložkami - Tabs):
      * Záložka 1: `📖 Teoretický výklad` (štruktúrovaný Markdown text, tabuľky, ukážky kódu a na konci tlačidlo "Prejsť na overovací kvíz →").
      * Záložka 2: `🧠 Overovací kvíz (+20 XP)` (interaktívne otázky A/B/C/D s vysvetlením odpovedí bez toho, aby tlačili teóriu hore alebo dole).
      * Záložka 3: `💡 Vzorové riešenie a vysvetlenie` (odomkne sa po úspešnom vyriešení cvičenia alebo obsahuje nápovedu k úlohe).
    - Pravý panel (Interaktívne Python IDE pracovisko):
      * Hore: Prepínač úloh lekcie (Exercise Pills: `Úloha 1: Ľahká ✓`, `Úloha 2: Stredná`, `Úloha 3: Boss`) s odmenou XP a Doros.
      * Stred: Stručné zadanie aktuálnej úlohy + CodeMirror editor s nástrojovou lištou (tlačidlá `▶ Spustiť a otestovať kód`, `↺ Resetovať štartovací kód`, `💡 Odomknúť nápovedu`).
      * Dole: Prepínací výstupný terminál (Console Tabs):
        - Záložka `🖥️ Výsledky Unit Testov` (prehľadný zoznam Test #1, Test #2, Skrytý test s časom vykonania v ms),
        - Záložka `🤖 Sokratovský AI Tútor Codo` (rada od AI tútora s indikátorom),
        - Záložka `📜 Moje odovzdania & Code Review` (história pokusov študenta v tejto úlohe a prípadný komentár od učiteľa).

9.3 Štrukturalizácia Obchodu (`shop.html`) a Učiteľského Panela (`teacher_panel`):
    - V `shop.html` pridať horné záložky: `🛍️ Ponuka odmien`, `🎟️ Moje kupóny ({{ my_coupons.count }})`, `🔑 Licencia PRO/EDU` a `💳 História peňaženky`, aby používateľ videl každú sekciu čisto a na celú šírku.
    - V `teacher_panel/cms_modules.html` použiť zbaliteľné stromové zobrazenie (Tree Accordion): Moduly sú zbalené; po kliknutí na modul sa zobrazia jeho lekcie; po kliknutí na lekciu sa zobrazia jej cvičenia a kvízy.

--------------------------------------------------------------------------------
FÁZA 10 (PRIORITA #2): MASÍVNE ROZŠÍRENIE UČIVA NA 18 MODULOV (220+ HODÍN) A HĹBKOVÝ OBSAH
--------------------------------------------------------------------------------
Cieľ: Každá lekcia v `courses/curriculum/` musí obsahovať skutočne bohatý, detailný učebný text (aspoň 40 - 80 riadkov kvalitného Markdownu na lekciu: úvod do problematiky, teoretické vysvetlenie, prehľadová Markdown tabuľka syntaxe/metód, 2 až 3 plne komentované bloky kódu v Pythone, blok `> ⚠️ **Častá chyba na maturite:** ...` a zhrnutie).
Zároveň rozšíriť kurikulum z 12 na 18 modulov rozdelených do 5 kariérnych ciest (`track` pole v modeli `Module`):

- TRACK 1: ZÁKLADY A LOGIKA (`FUNDAMENTALS`)
  * Modul 01: Úvod do algoritmizácie, premenné a základné dátové typy (10h, 5 lekcií, 15 cvičení)
  * Modul 02: Operátory, matematické výrazy a spracovanie reťazcov (12h, 5 lekcií, 15 cvičení)
  * Modul 03: Vetvenie programu a rozhodovacia logika `if / elif / else / match` (10h, 5 lekcií, 15 cvičení)
  * Modul 04: Cykly `for` a `while`, iterácie a 2D vnorené cykly (14h, 5 lekcií, 15 cvičení)

- TRACK 2: FUNKCIE A DÁTOVÉ ŠTRUKTÚRY (`DATA_STRUCTURES`)
  * Modul 05: Funkcie, oblasť platnosti (Scope), `lambda` a rekurzívne algoritmy (14h, 5 lekcií, 15 cvičení)
  * Modul 06: Zoznamy (`list`), N-tice (`tuple`), List Comprehensions a 2D matice (14h, 5 lekcií, 15 cvičení)
  * Modul 07: Slovníky (`dict`), Množiny (`set`), hašovacie tabuľky a frekvenčná analýza (12h, 5 lekcií, 15 cvičení)
  * Modul 08: Ošetrovanie výnimiek (`try/except`), defenzívne programovanie a parsovanie CSV/TXT dát (10h, 4 lekcie, 12 cvičení)

- TRACK 3: OBJEKTOVO-ORIENTOVANÉ PROGRAMOVANIE (`OOP`)
  * Modul 09: OOP I – Triedy, objekty, konštruktor `__init__`, `@property` a zapuzdrenie (12h, 5 lekcií, 15 cvičení, PRO/EDU)
  * Modul 10: OOP II – Dedičnosť, `super()`, polymorfizmus, magické dunder metódy a `@dataclass` (12h, 4 lekcie, 12 cvičení, PRO/EDU)

- TRACK 4: ALGORITMY, DÁTA A BEZPEČNOSŤ (`ALGORITHMS_AND_DATA`)
  * Modul 11: Časová zložitosť Big-O, vyhľadávacie (Binary Search) a triediace algoritmy (14h, 5 lekcií, 15 cvičení, PRO/EDU)
  * Modul 12: Regulárne výrazy (`re`), validácia vstupov (e-mail, telefón, IBAN) a parsovanie logov (10h, 4 lekcie, 12 cvičení, FREE)
  * Modul 13: Práca s relačnými databázami a jazykom SQL v Pythone (`sqlite3` v pamäti `:memory:`) (14h, 4 lekcie, 12 cvičení, PRO/EDU)
    *(Poznámka: V Python sandboxe možno bezpečne používať vstavaný modul `sqlite3` s databázou `:memory:`, takže študenti môžu priamo v cvičeniach písať funkcie vykonávajúce `CREATE TABLE`, `INSERT`, `SELECT ... JOIN` a agregácie!)*
  * Modul 14: Spracovanie JSON dát, REST API štruktúry a dátová analytika (12h, 4 lekcie, 12 cvičení, PRO/EDU)
  * Modul 15: Automatizované testovanie softvéru (`assert`, `unittest`, TDD) a čistý kód (10h, 4 lekcie, 12 cvičení, PRO/EDU)

- TRACK 5: MATURITNÝ ŠPECIÁL A PRAKTICKÉ PROJEKTY (`MATURITA_PREP`)
  * Modul 16: Kryptografia a kyberbezpečnosť v Pythone (Caesarova a Vigenèrova šifra, hašovanie, kontrola sily hesiel, bitové operácie) (12h, 4 lekcie, 12 cvičení, FREE)
  * Modul 17: Maturitné algoritmické zadania z praxe (Spracovanie meraní v elektrotechnike a IMT, štatistika triedy, plánovač rozvrhov, komprimácia dát) (14h, 5 lekcií, 15 cvičení, FREE)
  * Modul 18: Komplexné záverečné Boss Projekty a certifikačná skúška (16h, 5 lekcií, 15 cvičení, PRO/EDU)

--------------------------------------------------------------------------------
FÁZA 11 (PRIORITA #3): INTERAKTÍVNE PYTHON ŤAHÁKY (CHEAT SHEETS) A SLOVNÍK POJMOV (`/cheatsheets/`)
--------------------------------------------------------------------------------
Cieľ: Pridať do hlavnej navigácie novú podstránku `📚 Ťaháky a Slovník` (`/cheatsheets/`), ktorá slúži ako okamžitá interaktívna príručka pre študentov (a skvelá ukážka na obhajobe):
- Obsahuje vyhľadávacie pole (okamžité filtrovanie cez JS) a 6 kategórií záložiek:
  1. Základná syntax a dátové typy,
  2. Metódy reťazcov (`str`) a formátovanie,
  3. Metódy zoznamov (`list`) a slovníkov (`dict`),
  4. Funkcie, List Comprehensions a `lambda`,
  5. Objektovo-orientované programovanie (OOP),
  6. Časová zložitosť (Big-O) a vstavané funkcie Pythonu.
- Každá karta v ťaháku obsahuje názov konštrukcie (SK/EN), stručné vysvetlenie, ukážku kódu s tlačidlom `📋 Kopírovať kód` a informáciu o návratovej hodnote.
================================================================================