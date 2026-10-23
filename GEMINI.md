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


5. PRAVIDLÁ DIZAJNOVÉHO SYSTÉMU A ŠTRUKTÚRY UI/UX (MINERAL & EMERALD EDTECH DIZAJN)
--------------------------------------------------------------------------------
1. Celkový štýl a vizuálna identita (Mineral & Emerald EdTech):
   - Čistý, harmonický denný dizajn s mäkkými prírodnými tieňmi, bielymi kartami, zaoblením `16px - 20px` a vektorovými ilustráciami v smaragdovo-zelenej palete.
   - Presná farebná paleta pre svetlý režim (`:root` / `html[data-theme="light"]`):
     * Pozadie plátna (`--bg-canvas`): `#F3F7F5` s jemným prechodom do `#EBF2EE`
     * Povrch kariet (`--bg-surface`): `#FFFFFF` s jemným okrajom `#E2ECE7` a tieňom `0 8px 24px -4px rgba(14, 30, 24, 0.05)`
     * Sekundárny mätový povrch (`--bg-mint-soft`): `#E3F5EE` (pre aktívne položky v navigácii, aktívne tab karty a vybrané podklady)
     * Hlavný text (`--text-primary`): `#111C18` (hlboká lesná uhľová)
     * Sekundárny text (`--text-secondary`): `#4B5E57`
     * Primárna smaragdová (`--brand-emerald`): `#008767` (tlačidlá, aktívne rámčeky, kapucňa maskota Codo; hover `#006E53`)
     * Jasná zelená pre progres a úspešné testy (`--pass-green`): `#16A34A` / `#22C55E` (pozadie `#DCFCE7`)
     * Oranžová pre Streak a Class Quest (`--streak-orange`): `#F97316` (pozadie `#FFEDD5`)
     * Zlatá pre Doros mince (`--doros-gold`): `#EAB308` / `#D97706` (pozadie `#FEF9C3`)
   - Tmavý režim (`html[data-theme="dark"]`):
     * Lesný bridlicový režim (`#0D1512` pozadie, `#15201C` karty, `#23332D` okraje, `#10B981` smaragdový akcent, `#4ADE80` svetlozelená pre testy).
2. Maskot Codo a Zelené Logo:
   - Oficiálne logo platformy: `static/img/codorolo_logo_with_letters_green.png` a `static/img/codoro_logo_without_letters_transparent_green.png`.
   - Znovupoužiteľný inline SVG komponent maskota Codo: smaragdovo-zelená kapucňa (`#008767`) s bielym lemom, tmavá tvár (`#111C18`) s dvoma vysmiatymi oblúkovými azúrovými očami (`#5CE1E6`) a strieborno-sivý laptop so značkou `</>`.
3. ZÁKAZ NEKONEČNÉHO SCROLLOVANIA ("ENDLESS WALL OF CONTENT"):
   - Je prísne zakázané vykresľovať všetky moduly, lekcie, formuláre alebo tabuľky otvorené pod sebou na jednej dlhej stránke.
   - Každá obrazovka využíva progresívne odhaľovanie obsahu:
     * Prepínacie záložky (Tabs / Segmented Pills),
     * Zbaliteľné akordeóny (Collapsible Accordions - predvolene je rozbalený len 1 aktívny modul s 2px smaragdovým okrajom `#008767`, ostatné sú zbalené),
     * Interaktívna kľukatá cesta (Winding Stepping-Stone Path) s 3D pedestálmi a vlajočkami (zelená `✓`, aktívna `▶`, zamknutá `🔒`).
4. Apple Design & Impeccable Motion:
   - Plynulé fyzikálne animácie (spring transitions), okamžitá odozva na stlačenie (`:active transform: scale(0.97)`), prerušiteľné prepínania záložiek (Interruptibility) a 1:1 prepínanie obsahu bez skákania stránky.
5. Formátovanie Markdownu a 100 % Dvojjazyčnosť (SK / EN):
   - Všetky texty lekcií, zadaní a nápovied majú triedy `markdown-content markdown-render` spracované cez `marked.js`.
   - Na začiatku každej šablóny sa používa bezpečný tag `{% firstof user.preferred_language ui_lang 'sk' as lang %}`.


6. DOTERAJŠÍ STAV A ŠPECIFIKÁCIA NOVÝCH FÁZ PROJEKTU
--------------------------------------------------------------------------------
- FÁZA 1 až 8: Základná architektúra, databáza, autentifikácia, Sokratovský AI tútor, CMS základy, aréna, profil a unit testy [DOKONČENÉ]
- FÁZA 9: Rearchitektúra UI/UX proti nekonečnému scrollovaniu (Dashboard Hub, Split-Screen IDE) [DOKONČENÉ]
- FÁZA 10: Masívne rozšírenie kurikula na 18 modulov (220+ hodín, 5 kariérnych ciest) [DOKONČENÉ]
- FÁZA 11: Interaktívne Python ťaháky a slovník pojmov (/cheatsheets/) [DOKONČENÉ]
- FÁZA 12: SuperAdmin rozhranie a Live Support Helpdesk (/admin-panel/) [DOKONČENÉ]
- FÁZA 13: Registrácia pedagógov, zaobstaranie licencií a správa tried (/get-license/, /teacher/) [DOKONČENÉ]
- FÁZA 14: Verejná prezentácia a Landing Page (/ a /welcome/) [DOKONČENÉ]
- FÁZA 15: Vizuálny audit a refaktoring podľa zásad Impeccable Design & Craft Floor [DOKONČENÉ]
- FÁZA 16: Kompletný architektonický a dizajnový overhaul celej platformy [DOKONČENÉ]
- FÁZA 17: Modernizácia Landing Page, interaktívne demo štúdio, dynamický progress tracker a systém vlastných avatarov [DOKONČENÉ]
- FÁZA 18: Oprava renderovania lekcií (Markdown & CodeMirror) a rearchitektúra prírodnej scenérie na Mape učiva [DOKONČENÉ]

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

--------------------------------------------------------------------------------
FÁZA 12: SUPERADMIN ROZHRANIE A LIVE SUPPORT HELPDESK (`/admin-panel/`)
--------------------------------------------------------------------------------
Cieľ: Poskytnúť hlavnému administrátorovi platformy (`role=ADMIN` / `is_admin`) nezávislé webové rozhranie na kompletnú správu platformy Codoro bez nutnosti otvárať vývojové prostredie (IDE), terminál či Django `/admin/`.
- 12.1 Analytický SuperAdmin Dashboard (`/admin-panel/`):
  * Celkové štatistiky používateľov (počet študentov, učiteľov, administrátorov).
  * Metriky kurikula (počet modulov, lekcií, cvičení a úspešných odovzdaní).
  * Diagnostika databázy, pamäte a integrity sandboxu.
- 12.2 Live User & Student Helpdesk (`/admin-panel/users/`):
  * Okamžité vyhľadávanie a filtrovanie študentov podľa mena, triedy, roly a stavu licencie.
  * Zásahová pomoc priamo z webu (Helpdesk):
    - Reset hesla používateľa na počkanie bez e-mailového potvrdzovania,
    - Manuálna oprava poškodeného Streaku pri výpadku pripojenia,
    - Úprava hernej peňaženky (pridanie/odčítanie mincí Doros a bodov XP),
    - Zmena roly (povýšenie na učiteľa/admina) a preradenie medzi triedami.
- 12.3 Správa a schvaľovanie školských licencií (`/admin-panel/licenses/`):
  * Schvaľovanie a zamietanie verejných žiadostí škôl (`SchoolLicenseRequest`).
  * Generovanie oficiálnych EDU kľúčov s určením expiračného dátumu a počtu žiackych slotov.
  * Správa aktívnych a expirovaných licencií.

--------------------------------------------------------------------------------
FÁZA 13: REGISTRÁCIA PEDAGÓGOV, ZAOBSTARANIE LICENCIÍ A SPRÁVA TRIED
--------------------------------------------------------------------------------
Cieľ: Vybudovať ucelený a jednoduchý onboardingový systém pre školy a pedagógov bez byrokracie a manuálneho zásahu.
- 13.1 Dvojitá registrácia (`/register/`):
  * Prepínač rolí: `Študent` vs. `Učiteľ / Škola`.
  * Ak učiteľ disponuje školským EDU kľúčom, okamžite ho overí. Ak kľúč nemá, systém mu automaticky vytvorí 30-dňovú plnohodnotnú pilotnú EDU licenciu (`EDU-PILOT-XXXX`) pre okamžitý začiatok výučby.
- 13.2 Verejný portál na získanie licencie (`/get-license/`):
  * Transparentný formulár pre riaditeľov a učiteľov stredných škôl.
  * Automatické generovanie pilotného kľúča a uloženie žiadosti do `SchoolLicenseRequest` pre schválenie v SuperAdmin paneli.
- 13.3 Správa tried a hromadné generovanie účtov v Učiteľskom štúdiu (`/teacher/`):
  * Karta `Triedy & Kódy (School Classes)` s prehľadom všetkých tried učiteľa.
  * Založenie triedy s automatickým generovaním 8-miestneho kľúča triedy (napr. `IVC-2027`).
  * Zmazanie triedy a bezpečné odobratie žiaka z triedy.
  * Hromadný import žiakov (Batch Provisioning):
    - Učiteľ vloží zoznam mien (napr. z triednej knihy EduPage).
    - Systém automaticky odstráni diakritiku (mäkčene a dĺžne), transformuje mená na normalizované prihlasovacie mená (napr. `juraj_volf`) a vygeneruje bezpečné heslo pre každého žiaka.
    - Okamžitý náhľad, generovanie tlačiteľných kartičiek s prihlasovacími údajmi pre žiakov do lavice a CSV export.

--------------------------------------------------------------------------------
FÁZA 14: VEREJNÁ PREZENTÁCIA A LANDING PAGE (`/` A `/welcome/`) [DOKONČENÉ]
--------------------------------------------------------------------------------
Cieľ: Vytvoriť špičkovú, technologicky a vizuálne prepracovanú vstupnú stránku (Landing Page) platformy Codoro s plnou podporou Light/Dark režimu, 100% dvojjazyčnosťou (SK/EN) a nulovou závislosťou na externých CSS knižniciach.
- 14.1 Inteligentné smerovanie (`courses/views.py`):
  * Neprihlásený návštevník smerujúci na koreňovú adresu `/` vidí reprezentatívnu Landing Page (`templates/landing.html`).
  * Prihlásený študent smerujúci na `/` je priamo a plynule presmerovaný na svoj študentský Dashboard (`/dashboard/`).
  * Trvalá priama adresa `/welcome/` umožňuje zobraziť verejnú prezentáciu kedykoľvek bez nutnosti odhlásenia.
- 14.2 Profesionálny vizuálny a animačný engine (Advanced Visual Engine):
  * Kompletné nahradenie neformálnych emoji čistými vektorovými SVG ikonami s precíznym zarovnaním, CSS premennými a responzívnou farebnosťou (`currentColor`).
  * Živé reaktívne hviezdicové pozadie (`#heroBackgroundCanvas`):
    - Matematická simulácia konštelácie 42 svietiacich uzlov v HTML5 Canvas s dynamickým výpočtom vzdialeností a prepojovacích lúčov (vzdialenostný cutoff < 125 px),
    - Plynulý ambientný drift s periódou a reaktivita na pohyb kurzora myši cez odpudivé tlmiace sily (Spring-Damper Physics),
    - Optimalizácia pre Retina a HiDPI displeje cez `window.devicePixelRatio` a stabilných 60 FPS s nulovým zaťažením DOM stromu.
  * Reaktívna navigácia pri scrollovaní:
    - Horný indikátor priebehu čítania (`#scrollProgressBar`) s lineárnym gradientom [0 % až 100 %],
    - Dynamická zmena stavu navigácie (`.public-navbar.scrolled`) s aplikáciou hĺbkového skleneného rozostrenia (`backdrop-filter: blur(16px)`),
    - Scroll-Spy engine: Automatické zvýrazňovanie aktívneho odkazu v hornom menu podľa skutočnej polohy používateľa na obrazovke.
  * Svetelný efekt kurzora na kartách (Mouse-Follow Spotlight Glow):
    - Trieda `.spotlight-card` dynamicky prepočítava lokálne súradnice `--mouse-x` a `--mouse-y` a vykresľuje jemný radiálny kužeľ svetla na okrajoch kariet.
  * Animované číselné počítadlá (Smooth Counter Animation):
    - `IntersectionObserver` aktivuje plynulý nábeh číselných hodnôt pri vstupe do zorného poľa (18 Modulov, 220+ Hodín, 250+ Úloh, 100% AI).
- 14.3 Živé multi-snippet Python IDE & Sokratovský Codo showcase:
  * Prepínač 3 reálnych programátorských úloh priamo v Hero sekcii:
    1. `01_priemer.py`: Výpočet váženého priemeru známok maturanta,
    2. `02_caesar_sifra.py`: Šifrovanie textu Caesarovým algoritmom,
    3. `03_fibonacci.py`: Generovanie Fibonacciho postupnosti s kontrolou limitov.
  * Interaktívna simulácia AST syntaktickej analýzy, kompilácie a okamžitého testovania:
    - Kroková animácia terminálu s odozvou v milisekundách (napr. 14 ms),
    - Streamovaný výpis úspešných unit testov so zelenými indikátormi,
    - Interaktívna bublina Sokratovského AI tútora Codo, ktorá demonštruje princíp navádzania študenta k riešeniu bez vyzradenia kódu.
  * Vznášajúce sa paralaxové widgety okolo IDE (AST izolovaný proces, Top 5% umiestnenie v triede IV.C, 14-dňový Streak).
- 14.4 Špičková štruktúra informačnej architektúry:
  * Lišta metrík (Metrics Ribbon) s animovanými číselníkmi a SVG symbolmi,
  * 4 Strategické piliere Codoro v prehľadných kartách s porovnaním voči konkurencii,
  * Interaktívny prehliadač 5 kariérnych ciest a 18 modulov kurikula so záložkami bez znovunačítania stránky,
  * Sprievodca pre stredné školy a učiteľov: 3 jednoduché kroky nasadenia a živý náhľad Učiteľského štúdia,
  * Transparentná porovnávacia tabuľka: Codoro vs. Duolingo vs. W3Schools vs. Tradičná výučba,
  * Responzívny FAQ akordeón s plynulým rozbaľovaním a SVG rotáciou šípok,
  * Konverzný CTA banner a oficiálna maturitná pätička (Spojená škola Nižná, Téma č. 22, Juraj Volf, Mgr. Markéta Brišová, TMview ochranná známka a odkaz na GitHub).

--------------------------------------------------------------------------------
FÁZA 15: KOMPLETNÝ UI/UX OVERHAUL A INTEGRÁCIA SKILLOV (IMPECCABLE, TRANSITIONS.DEV, GSAP, MAKE-INTERFACES-FEEL-BETTER) [DOKONČENÉ]
--------------------------------------------------------------------------------
Cieľ: Posunúť vizuálne a hmatové spracovanie platformy Codoro na úroveň špičkových svetových digitálnych produktov (Linear, Stripe, Vercel) prostredníctvom prísnych princípov štyroch odborných dizajnových a animačných skillov.
- 15.1 Dizajnová filozofia Impeccable (Craft & Hierarchy):
  * Dôsledné uplatnenie módu povrchu: Mód *Persuade* pre verejnú prezentáciu (Landing Page) s vysokou vizuálnou ambíciou a mód *Operate* pre študentský Dashboard, Učiteľské štúdio a Python IDE s dôrazom na čitateľnosť, ergonómiu a rýchlu orientáciu.
  * Harmonická farebná paleta odvodená od loga Codoro bez generických plochých odtieňov, s dokonalou koexistenciou v Light aj Dark režime.
- 15.2 Princípy Make-Interfaces-Feel-Better (Hmatová odozva a optická precíznosť):
  * **Globálne vyhladzovanie písma (Font Smoothing):** Aplikácia `-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;` pre maximálnu ostrosť typografie na displejoch všetkých platforiem (macOS, Windows, iOS, Android).
  * **Tabulárne čísla bez posunu layoutu (Tabular Numbers):** Nasadenie `font-variant-numeric: tabular-nums;` na všetky počítadlá, stopky, časy unit testov, indikátory XP, mincí Doros a štatistické widgety (`.counter-val`, `.metric-val`, `.ide-time-tag`, `.sidebar-stat-pill`), čím sa eliminuje nepríjemné trasenie prvkov pri zmene čísel.
  * **Optické vyváženie textu (Text Wrapping):** Aplikácia `text-wrap: balance;` na všetky hlavné nadpisy (`h1, h2, h3, h4`, `.hero-headline`, `.section-title`) a `text-wrap: pretty;` na odseky a vysvetlenia, čo odstraňuje nevzhľadné osirotené slová na koncoch riadkov.
  * **Hmatový fyzikálny klik (Tactile Scale-On-Press):** Presne kalibrovaná hodnota `transform: scale(0.96) !important;` pri stlačení tlačidiel a interaktívnych prvkov (`.btn:active:not(:disabled)`). Striktný zákaz hodnôt pod 0.95, ktoré pôsobia prehnane a neprirodzene.
  * **Striktná eliminácia `transition: all`:** Každé prechodové pravidlo explicitne vymenúva cieľové vlastnosti (`transition-property: transform, background, border-color, box-shadow, color, opacity;`), čo zabraňuje náhodným a trhavým prechodom pri zmene nezaradených štýlov.
  * **Koncentrické zaoblenie rohov (Concentric Border Radius):** Matematické pravidlo `outerRadius = innerRadius + padding` (vonkajšie karty `--radius-outer: 18px`, vnútorné tlačidlá a elementy `--radius-inner: 12px`, vnorené čipy 8px), vďaka čomu vnútorné prvky v kartách nepôsobia opticky "priškripnuto".
  * **Vrstvené tiene a jemný obrys (Layered Elevation & Outlines):** Dvojvrstvové tiene kombinujúce jemný 1-2px kontaktný tieň, hĺbkový mäkký rozptyl a 1px jemný kontrastný obrys (`rgba(15, 23, 42, 0.06)` v svetlom a `rgba(255, 255, 255, 0.08)` v tmavom režime) pre špičkovú separáciu povrchov.
  * **Ergonomická veľkosť dotykových plôch:** Minimálna výška ovládacích prvkov 42px pre pohodlné ovládanie na dotykových aj desktopových zariadeniach.
- 15.3 Pohybový slovník Transitions.dev (Micro-Interactions):
  * **Univerzálne Bezierové krivky:** Import vyladených pohybových kriviek (`--ease-out-expo`, `--ease-out-back`, `--ease-out-quart`, `--ease-in-out-cubic`, `--ease-spring`) zjednotených s modernými animačnými štandardmi.
  * **Svetelný tok textu (Shimmer Text - `15-shimmer-text`):** Čistá CSS animácia plynulého prechodu svetelného odlesku cez text odznakov maturitného projektu a konverzných bannerov (`.t-shimmer`).
  * **Animované kreslenie úspešných fajok (Success Checkmark - `10-success-check`):** Dynamické kreslenie ťahu SVG fajky (`stroke-dasharray: 25`, `stroke-dashoffset: 25`) s postupným oneskorením po dokončení unit testov v sandboxe.
  * **Trojrozmerný náklon kariet (3D Card Tilt - `19-card-tilt`):** Fyzikálny výpočet relatívneho posunu kurzora voči stredu karty `(dx, dy)` s plynulou rotáciou `rotationX` a `rotationY` v perspektíve 1000px a pružným návratom do pokojového stavu pri opustení myšou.
  * **Rešpektovanie prístupnosti:** Plná podpora používateľského nastavenia `@media (prefers-reduced-motion: reduce)`, kedy sa všetky animácie a prechody okamžite skrátia na 0 ms pre používateľov s vestibulárnymi poruchami.
- 15.4 Orchestrácia GSAP 3.12 a ScrollTrigger (gsap-skills):
  * **Hero Stagger Timeline:** Využitie `gsap.timeline()` s predvoleným `power3.out` pre precízne načasovaný nábeh Hero sekcie:
    - Odznak maturitného projektu: `scale: 0.88`, `opacity: 0`, `ease: "back.out(1.8)"`,
    - Hlavný nadpis a podnadpis: plynulý posun `y: 35`,
    - CTA tlačidlá: sekvenčný nábeh so staggerom 0.1s a odrazom `back.out(1.5)`,
    - Okno Python IDE: hĺbkový 3D nábeh s rotáciou `rotationX: 4` a `y: 45`,
    - Vznášajúce sa widgety: sekvenčný pop-in so staggerom 0.12s.
  * **Kontinuálne sínusové vznášanie (Ambient Floating Loop):** Trojica paralaxových widgetov okolo IDE vykonáva plynulý zvislý pohyb v protifáze s rôznou periódou (2.8s až 3.6s, `ease: "sine.inOut"`, `yoyo: true`).
  * **ScrollTrigger Batch Reveals:** Automatická aktivácia sekcií a prvkov pri dosiahnutí 85% výšky viewportu (`ScrollTrigger.batch()`) s plynulým kaskádovým nábehom.
  * **Numerické počítadlá cez GSAP Tweening:** Plynulá matematická interpolácia číselných hodnôt na lište metrík s automatickým zaokrúhľovaním bez zaťaženia pamäte.
  * **Deterministický Vanilla Fallback:** V prípade nedostupnosti externých CDN skriptov je celý systém postavený na automatickom záložnom režime (vstavaný `IntersectionObserver` a natívne CSS prechody), takže platforma funguje 100% autonómne aj pri offline prezentácii.

- 15.5 Kompletný zoznam prepracovaných šablón a komponentov v rámci celoplatformového UI overhaulu:
  * `templates/base.html`:
    - Odstránené globálne `transition: all`, zavedené striktne explicitné prechodové vlastnosti (`transition: color, background-color, border-color, box-shadow, transform`),
    - Globálne CSS tokeny pre motion (`--ease-out-expo`, `--ease-out-back`, `--ease-spring`), koncentrické rádiusy (`--radius-outer`, `--radius-inner`, `--radius-sm`, `--radius-pill`),
    - Globálne vyhladzovanie písma (`-webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;`),
    - Hmatová kalibrácia stlačenia tlačidiel (`.btn:active:not(:disabled) { transform: scale(0.96) !important; }`),
    - Globálna integrácia knižníc GSAP 3.12.5 + ScrollTrigger s deterministickým vanilla fallbackom.
  * `templates/landing.html`:
    - Živé reaktívne hviezdicové pozadie (`#heroBackgroundCanvas`) so spring-damper časticovou fyzikou a interakciou na kurzor,
    - Interaktívne multi-snippet Python IDE (3 reálne maturitné úlohy, AST syntaktická analýza, kroková simulácia behu v ms),
    - 100% eliminácia surových emoji a ich nahradenie vektorovými SVG ikonami (`currentColor`, konzistentná hrúbka ťahu `2.2`),
    - GSAP staggered Hero timeline, ScrollTrigger batch kaskády, 3D tilt kariet, animované SVG fajky úspechu,
    - Striktná eliminácia `transition: all`, tabulárne čísla na všetkých metrikách a časomeroch.
  * `templates/courses/dashboard.html`:
    - Kompaktný Hero Card "Pokračovať v štúdiu" s lineárnym progress barom a záchranou streaku,
    - Horizontálne prepínanie 5 kariérnych ciest s real-time vyhľadávaním bez obnovy stránky,
    - Zbaliteľné akordeóny modulov (moduly 01 až 18) s progresom a badge-mi,
    - Pravý bočný panel s 3 prepínacími kartami (Osobné výzvy, Triedny Quest, Rebríček),
    - 100% vektorové SVG ikony (odznaky, mince Doros, oheň streaku, fajky úspechu), tabulárne čísla, hmatová odozva.
  * `templates/courses/lesson_detail.html`:
    - Profesionálne Split-Screen IDE pracovisko bez nežiaduceho scrollovania celej stránky,
    - Ľavý panel: 3 vnútorné záložky (Teoretický výklad v Markdown, Overovací kvíz, Vzorové riešenie),
    - Pravý panel: Prepínač úloh lekcie, CodeMirror editor (Python), konzolové záložky (Unit testy, Codo AI rada, Moje odovzdania),
    - 100% SVG ikony, tabulárne čísla na časovačoch a XP, explicitné prechody a hmatová odozva.
  * `templates/gamification/shop.html`:
    - Horné prepínacie záložky (Ponuka odmien, Moje kupóny, Licencia PRO/EDU, História peňaženky),
    - Nahradenie všetkých emoji čistými vektorovými SVG ikonami,
    - Tabulárne čísla pre zostatok mincí Doros, počítadlá zásob a ceny odmien, hmatový klik.
  * `templates/courses/cheat_sheets.html` & `courses/curriculum/cheatsheets_data.py`:
    - Interaktívny slovník pojmov a Python ťahákov so živým vyhľadávaním a filtrovaním v JS,
    - 6 tematických záložiek, každá s vlastnou SVG ikonou namiesto emoji,
    - Kopírovanie kódu do schránky jedným klikom s okamžitou vizuálnou odozvou, tabulárne čísla, explicitné prechody.
  * `templates/courses/practice_arena.html`:
    - Generovanie neobmedzených AI cvičení a okamžité precvičovanie v sandboxe,
    - SVG ikony, tabulárne čísla, hmatový scale a vyladené tiene kariet.
  * `templates/accounts/profile.html` & `certificate.html`:
    - Profil študenta: vizuálny celoročný Streak kalendár, záchrana streaku, história odznakov a certifikátov,
    - Oficiálny overiteľný certifikát absolventa s QR kódom, SVG hviezdami a pečaťou Codoro,
    - Odstránené všetky `transition: all`, tabulárne čísla na bodoch XP a koncentrické rádiusy.
  * `templates/accounts/register.html`, `login.html` & `get_license.html`:
    - Profesionálna Persuade / Auth typografia a architektúra kariet,
    - SVG ikony pre roly (Študent vs. Učiteľ/Škola), licenčné kľúče a benefity,
    - Explicitné prechody, tabulárne počítadlá žiackych slotov.
  * `templates/teacher_panel/` (`dashboard.html`, `cms_modules.html`, `cms_lesson_form.html`, `cms_exercise_form.html`, `student_detail.html`):
    - Kompletný stromový akordeón kurikula (Modul -> Lekcia -> Úlohy & Kvízy),
    - Všetky akčné tlačidlá (editácia, tvorba, publikovanie, AI preklad do EN, unit testy) vybavené čistými SVG ikonami,
    - Tabulárne čísla na metrikách triedy a odovzdaných kódoch, hmatová odozva tlačidiel.
  * `templates/admin_panel/dashboard.html`:
    - SuperAdmin centrum a Live Support Desk s 5 prepínacími záložkami,
    - Všetky akcie (reset hesla, oprava streaku, úprava Doros peňaženky, generovanie kľúčov, inšpekcia kódov) kompletne prevedené na vektorové SVG ikony,
    - Odstránené `transition: all`, tabulárne čísla na všetkých 50 odovzdaniach, dobách behu a systémových metrikách.

- FÁZA 16: KOMPLETNÝ ARCHITEKTONICKÝ A DIZAJNOVÝ OVERHAUL CELEJ PLATFORMY [DOKONČENÉ]
  * Oprava všetkých 41 IDE syntaktických chýb (`@[current_problems]`):
    - Konverzia inline Django interpolácií v `onclick="..."` (`{{ module.id }}`, `{{ c.id }}`) na štandardné HTML5 `data-*` atribúty a `this.dataset.*`,
    - Plne validná JS syntax v šablónach bez konfliktov s HTML/JS jazykovými servermi.
  * Nový Desktop App Header (`.app-desktop-header`) pre prihlásených používateľov (Linear / Vercel style):
    - Sticky navigačný pás s hĺbkovým blur efektom (`backdrop-filter: blur(16px)`),
    - Kontextové omrvinky (Breadcrumbs) pre aktuálnu polohu študenta a učiteľa,
    - Živé HUD odznaky pre sériu (Streak flame), Doros peňaženku (Gold coin), triedu (School class), prepínač jazyka (SK/EN), plynulý prepínač témy (Sun/Moon SVG) a profilový avatar.
  * Zavedenie globálnych pravidiel zručnosti Impeccable & Craft Floor:
    - 0 surových emoji v celom projekte (100% SVG vektorové ikony s jednotnou hrúbkou a štýlom),
    - 0 výskytov `transition: all` (všetky animácie cielia explicitné CSS vlastnosti),
    - Zákaz kickers/eyebrows nad hlavnými nadpismi (odstránené nadbytočné texty, nadpisy hovoria samy za seba),
    - Zákaz hrubých `border-left` na kartách a calloutoch (nahradené jemnými 1px hairline kontúrami a badge štítkami),
    - Vlastný dizajn systémových prvkov prehliadača: `::selection` vo farbe Ro-Indigo, vlastné zaoblené 6px posuvníky (Scrollbars), zjednotené `focus-visible` a vlastný kurzor (`caret-color`).
  * Klávesové skratky pre profesionálny vývoj:
    - `Ctrl + Enter` (alebo `Cmd + Enter`) v CodeMirror editore pre okamžité spustenie a otestovanie kódu v Python sandboxe s AST kontrolou.

- FÁZA 17: MODERNIZÁCIA LANDING PAGE, DEMO ŠTÚDIO, PROGRESS TRACKER A SYSTÉM AVATAROV [DOKONČENÉ]
  * Modernizácia sekcie modulov na Landing Page (`templates/landing.html`):
    - Úplné odstránenie horizontálneho scrollbaru v prospech intuitívneho, ergonomického rozhrania.
    - Zavedený horizontálny prepínač 5 kariérnych ciest (Segmented Track Pills) s plynulým prepínaním cez data atribúty a real-time vyhľadávacím poľom.
    - Responzívny grid kariet modulov s odznakmi náročnosti, časovou dotáciou a odkazmi do výučby.
  * Očistenie maskota Codo a oprava modálneho okna prihlásenia:
    - Odstránené rušivé žlté lúče a žiarenie okolo maskota Codo vo všetkých inštanciách, zachovaný čistý, priateľský 2D vektorový vzhľad s kapucňou a laptopom.
    - Oprava modálneho dialógu prihlásenia (`#loginModal`) na Welcome page: funkčné otváranie cez tlačidlá v navigácii a CTA tlačidlá, zatváranie krížikom, kliknutím na backdrop alebo klávesom ESC, funkčné demo predvyplnenie jedným klikom.
  * Presný dynamický progress tracker:
    - Odstránená statická hodnota "62% hotovo".
    - Nahradené dynamickým kruhovým SVG indikátorom počítaným z reálneho stavu dokončených lekcií používateľa v databáze (0% pre nového študenta).
  * Plná lokalizácia interaktívneho demo štúdia na Landing Page (100% SK / EN):
    - Kompletný preklad popiskov, súborových záložiek a tlačidiel podľa preferovaného jazyka.
    - Obojsmerné prepínanie súborov v demo editore medzi `main.py` a `priemer_znamok.py` s plnou interaktivitou.
    - Plná funkčnosť ovládacích tlačidiel: Reset kódu do pôvodného stavu, Formátovanie kódu s vizuálnym potvrdením, Klávesové skratky v samostatnom modálnom okne.
  * Systém vlastných profilových avatarov (`profile.html` & `accounts/`):
    - Generovanie 4 nových unikátnych AI portrétov v anime/edtech štýle:
      * `student_alex`: Chlapec s hnedými vlasmi, mikinou a slúchadlami
      * `student_mia`: Dievča s tmavými vlasmi v cope a zelenom svetri
      * `student_sam`: Chlapec s kučeravými vlasmi v rifľovej bunde
      * `cyber_ninja`: Postava v tmavej mikine s neónovými azúrovými prvkami
      * `codo`: Oficiálny zelený maskot platformy Codoro
    - Nové pole `avatar_choice` v modeli `User` s migráciou a možnosťou okamžitej zmeny profilovej fotky.
    - Integrácia zvoleného avatara do celého rozhrania (top app bar, profil, rebríček triedy).

- FÁZA 18: OPRAVA LEKCIÍ (MARKDOWN & CODEMIRROR) A REARCHITEKTÚRA PRÍRODNEJ SCENÉRIE [DOKONČENÉ]
  * Oprava pracoviska lekcie a Split-Screen IDE (`templates/courses/lesson_detail.html`):
    - Presun knižníc `CodeMirror 5.65.16` (jadro, python režim, matchbrackets, closebrackets) a `marked.js` priamo do `<head>` v `templates/base.html`, čím sa eliminovala chyba `ReferenceError: CodeMirror is not defined`.
    - Plné automatické renderovanie teórie cez `marked.js`: formátované smaragdové nadpisy H1-H4, bloky kódu v tmavom bloku (`#0D1512`), inline mätové `code` štítky, formátované Markdown tabuľky a odrážky.
    - CodeMirror editor inicializovaný s číslami riadkov, syntaxou Pythonu, klávesovou skratkou `Ctrl + Enter` pre spustenie a nastavenou výškou.
    - Pevná jednoradová horná navigačná lišta s elipsou pre dlhé názvy lekcií – tlačidlo `Ďalšia lekcia →` drží pevnú pozíciu vpravo bez zalamovania na druhý riadok.
    - Názov okna *Codoro Studio Workbench* upravený s elipsou, zamedzené nežiaducemu zalamovaniu do dvoch riadkov.
    - Výstupy unit testov a chybové tracebacky vybavené pravidlom `word-break: break-word` a `white-space: pre-wrap`.
  * Rearchitektúra prírodnej scenérie na Mape učiva (`templates/courses/dashboard.html` & `static/css/codoro.css`):
    - Kamene a kríky boli **kompletne odstránené z vlajok a pedestálov** (`.path-pedestal-anchor`). Vlajky sú čisté a zreteľné.
    - Úprava responzívneho breakpointu z `1280px` na `1040px` v `.emerald-dashboard-grid`: 3 bočné widgety (*Triedny Quest*, *Moja Doros peňaženka*, *Môj postup*) stoja v pravom stĺpci priamo vedľa mapy na všetkých bežných displejoch a notebookoch (1184px+), čím sa úplne vyplnil prázdny biely priestor vpravo.
    - Prírodné prvky presunuté do prázdnych okrajov a pozadia mapy:
      * Panoramatický horský hrebeň v pozadí (`mountain_peaks_landscape`),
      * Zhluky borovíc (`pine_tree_cluster`), riečnych balvanov a lúčnych kríkov vo voľných okrajoch plátna.
    - Ľavý bočný panel (`emerald-sidebar`) nastavený ako `position: sticky` na výšku obrazovky, čím sa zamedzilo vzniku prázdneho bieleho vákua pod navigáciou.
  * Validácia celistvosti systému:
    - Všetkých 76 automatizovaných testov Django ORM a biznis logiky úspešne prebehlo: `Ran 76 tests in 309.113s - OK`.

- FÁZA 19: REARCHITEKTÚRA PRÍRODNEJ SCENÉRIE MAPY, ZLÚČENIE OKRAJOV JAZYKOV A ČISTENIE PROFILU [DOKONČENÉ]
  * Úplné odstránenie horizontálneho scrollbaru na Welcome page:
    - Globálne `overflow-x: hidden; max-width: 100%;` pridané pre selektor `html, body`.
    - Kontajner `.public-hero-canvas-root` zabezpečený vlastnosťou `overflow-x: clip;`.
    - Odstránená nesprávna šírka `width: 100vw;` z prvkov `.scenic-ambient-glow` a `.scenic-hero-hills-backdrop` (spôsobovala 17px presah kvôli vertikálnemu scrollbaru) a nahradená bezpečným `width: 100%; max-width: 100%;`.
  * Rearchitektúra prírodných scenérií na Mape učiva (`templates/courses/dashboard.html` & `illustrations_svg.html`):
    - Odstránené náhodne vložené zhluky borovíc a kameňov (`landscape-ambient-cluster`), ktoré neprimerane prekrývali ľavý horný roh Modulu 1.
    - Zelená prírodná oáza vľavo (okolie maskota Codo v bočnom paneli): Maskot Codo bol zakotvený do prírodnej lúčnej scenérie s vlnitými kopcami v pozadí, borovicovým hájom, rozkvitnutým kríkom a riečnymi balvanmi s trsom trávy pod nohami (`codo_on_rock` / `codo_hero_scene`).
    - Horská cesta poznania vpravo (vyplnenie bieleho prázdna v pravom stĺpci pozdĺž 18 modulov): Do pravého panelu widgetov pridaná `.scenic-nature-column` s kartou `.scenic-nature-card`, ktorá obsahuje horský hrebeň, borovicový lesík, skalnú lúčku, výškové míľniky postupu (Zelené údolie -> Algoritmický hrebeň -> Vrchol kurikula) a kamenný Python monolit.
  * Odstránenie nefunkčných retro emoji avatarov a výberu farby motívu (`templates/accounts/profile.html`):
    - Odstránený blok `<details>` so zastaranými emoji a výber farebného motívu `avatar_colors`.
    - Ponechaný výhradne prémiový systém 5 vlastných autorských edtech avatarov (`student_alex`, `student_mia`, `student_sam`, `cyber_ninja`, `codo`).
  * Oprava ikony pri zmene hesla v profile:
    - Nahradená neforemná deformovaná čiara v tlačidle čistou autorskou vektorovou ikonou kľúča (`key`) so zaoblenými hranami.
    - Hlavička sekcie osadená čistou smaragdovou ikonou bezpečnostného zámku (`lock`).
  * Precízne koncentrické zlúčenie okrajov prepínača jazykov (`SK | EN`):
    - Prebudované CSS pre `.lang-segmented` a `.lang-pill`: kontajner s rovnomerným paddingom 3px a vnútorná kapsula s pevnou výškou 24px a `border-radius: 9999px`.
    - Vonkajší a vnútorný oblúk do seba matematicky presne zapadajú s identickým 3px odstupom vo všetkých uhloch, bez akýchkoľvek zubov alebo nepekných medzier.
  * Oprava tmavého režimu na stránke zaobstarania licencie (`/get-license/` a `.card-surface`):
    - Odstránené staré hardcoded modré pozadie kariet `rgba(14, 20, 32, 0.94)` a `rgba(14, 20, 32, 0.98)` v `codoro.css` pre `.card-surface` a `.app-sidebar`, ktoré pochádzalo z pôvodného indigo/navy dizajnu.
    - Zjednotené na prémiový Forest Slate token `--bg-surface` (`#15201C`), vďaka čomu majú všetky karty aj formuláre jednotný harmonický tmavozelený bridlicový vzhľad.
    - V šablóne `templates/accounts/get_license.html` bol fialovo-modrý gradient v hero boxe nahradený čistým radiálnym prechodom z mätového povrchu do povrchu karty s jemným smaragdovým okrajom.
================================================================================