"""
Curriculum Enrichment Engine pre Codoro Kurikulum.
Tento modul dynamicky dopĺňa moduly 1 až 11 o:
1. Príznak 'track' (Kariérna cesta)
2. Školské upozornenia na časté chyby na maturite (53 lekcií)
3. Prehľadové Markdown tabuľky syntaxe a metód (53 lekcií)
4. Plnú sadu 3 cvičení (EASY, MEDIUM, HARD) pre každú lekciu (spolu 237 cvičení)
"""
from .companion_data import COMPANIONS

TRACK_MAP = {
    1: 'FUNDAMENTALS',
    2: 'FUNDAMENTALS',
    3: 'FUNDAMENTALS',
    4: 'FUNDAMENTALS',
    5: 'DATA_STRUCTURES',
    6: 'DATA_STRUCTURES',
    7: 'DATA_STRUCTURES',
    8: 'DATA_STRUCTURES',
    9: 'OOP',
    10: 'OOP',
    11: 'ALGORITHMS_AND_DATA',
    12: 'ALGORITHMS_AND_DATA',
    13: 'ALGORITHMS_AND_DATA',
    14: 'ALGORITHMS_AND_DATA',
    15: 'ALGORITHMS_AND_DATA',
    16: 'MATURITA_PREP',
    17: 'MATURITA_PREP',
    18: 'MATURITA_PREP',
}

MATURITA_WARNINGS = {
    (1, 1): "> ⚠️ **Častá chyba na maturite:** Zabudnutie parametra `sep` alebo `end` pri formátovaní konzolového výstupu. Pamätaj, že `print()` štandardne pridáva medzeru medzi argumentmi a nový riadok na konci.",
    (1, 2): "> ⚠️ **Častá chyba na maturite:** Pomenovanie premenných začínajúcich číslicou (napr. `1_vysledok`) alebo použitie kľúčového slova (napr. `class = 5`), čo spôsobí okamžitú `SyntaxError`.",
    (1, 3): "> ⚠️ **Častá chyba na maturite:** Zámena reťazca s číslom (napr. `\"10\" + \"5\"` dá `'105'`, nie `15`). Vždy overuj typ pomocou `type()` a pri vstupe nezabúdaj na pretypovanie.",
    (1, 4): "> ⚠️ **Častá chyba na maturite:** Pokus o `int(\"3.14\")`, ktorý vyvolá `ValueError`. Desatinné číslo v reťazci musí ísť najprv cez `float(\"3.14\")` a až potom prípadne `int()`.",
    (1, 5): "> ⚠️ **Častá chyba na maturite:** Zanedbanie zátvoriek pri matematických výpočtoch priorít operátorov, najmä pri delení a sčítaní v zlomkoch `(a + b) / 2`.",
    (2, 1): "> ⚠️ **Častá chyba na maturite:** Zámena klasického delenia `/` (vždy vracia `float`) a celočíselného delenia `//` (vracia `int`). Na maturite často vyžadujú celočíselné delenie a zvyšok cez `%`.",
    (2, 2): "> ⚠️ **Častá chyba na maturite:** Použitie jedného rovnítka `=` namiesto dvoch `==` pri porovnávaní. Jedno `=` je priradenie a v podmienke spôsobí syntaktickú chybu.",
    (2, 3): "> ⚠️ **Častá chyba na maturite:** Pretečenie indexu (IndexError) pri prístupe k `text[len(text)]`. Nezabúdaj, že indexy začínajú od 0, takže posledný znak je `text[-1]` alebo `text[len(text)-1]`.",
    (2, 4): "> ⚠️ **Častá chyba na maturite:** Zabudnutie, že metódy ako `text.strip()`, `text.replace()` alebo `text.upper()` nemenia pôvodný reťazec (reťazce sú v Pythone immutable), ale vracajú nový!",
    (2, 5): "> ⚠️ **Častá chyba na maturite:** Zabudnutie písmena `f` pred úvodzovkou pri f-stringu `f\"{premenna}\"`. Bez `f` Python vypíše doslovný text `\"{premenna}\"`.",
    (3, 1): "> ⚠️ **Častá chyba na maturite:** Nesprávne odsadenie (IndentationError) alebo chýbajúca dvojbodka `:` za podmienkou `if`. V Pythone je odsadenie (4 medzery) syntakticky záväzné.",
    (3, 2): "> ⚠️ **Častá chyba na maturite:** Použitie viacerých `if` za sebou namiesto reťazca `if - elif - else`. Pri samostatných `if` sa vyhodnocujú všetky vetvy, čo môže prepísať správny medzivýsledok.",
    (3, 3): "> ⚠️ **Častá chyba na maturite:** Zámena logických operátorov `and` a `or`. Výraz `if a or b and c` sa vyhodnocuje podľa priority: `and` má vyššiu prioritu ako `or`!",
    (3, 4): "> ⚠️ **Častá chyba na maturite:** Písanie `if podmienka == True:`. V idiomatickom Pythone sa píše priamo `if podmienka:` alebo `if not podmienka:`.",
    (3, 5): "> ⚠️ **Častá chyba na maturite:** Vynechanie vetvy `case _:` (wildcard) v konštrukcii `match-case`. Ak žiadny vzor nepasuje, interpreter nevykoná nič, čo môže viesť k nedefinovanému stavu.",
    (4, 1): "> ⚠️ **Častá chyba na maturite:** Nesprávne stanovenie hornej hranice v `range(start, stop)`. Pamätaj, že hodnota `stop` je otvorená a do výsledku sa nezahŕňa! `range(1, 5)` dá len 1, 2, 3, 4.",
    (4, 2): "> ⚠️ **Častá chyba na maturite:** Inicializácia premennej na hľadanie maxima číslom 0 pri spracovaní záporných čísel. Vždy inicializuj prvým prvkom sekvencie alebo `float('-inf')`.",
    (4, 3): "> ⚠️ **Častá chyba na maturite:** Nekonečný cyklus (Infinite Loop) spôsobený tým, že riadiaca premenná cyklu `while` sa v tele cyklu nezvyšuje.",
    (4, 4): "> ⚠️ **Častá chyba na maturite:** Nesprávne pochopenie bloku `else` pri cykle `for/while`. Blok `else` sa vykoná iba vtedy, ak cyklus prebehol celý a NEBOL prerušený príkazom `break`.",
    (4, 5): "> ⚠️ **Častá chyba na maturite:** Zdieľanie odkazov pri vytváraní 2D mriežky cez `[[0]*cols]*rows`. Všetky riadky budú ukazovať na rovnaký zoznam v pamäti! Správne: `[[0]*cols for _ in range(rows)]`.",
    (5, 1): "> ⚠️ **Častá chyba na maturite:** Zámena `return` a `print()`. Ak funkcia nemá príkaz `return`, vracia hodnotu `None`. Pri ukladaní výsledku do premennej sa uloží `None`!",
    (5, 2): "> ⚠️ **Častá chyba na maturite:** Použitie meniteľného objektu (napr. `def f(zozn=[])`) ako predvoleného argumentu funkcie. Tento zoznam je zdieľaný medzi všetkými volaniami!",
    (5, 3): "> ⚠️ **Častá chyba na maturite:** Snaha modifikovať globálnu premennú vnútri funkcie bez deklarácie `global`. Funkcia namiesto toho vytvorí novú lokálnu premennú rovnakého mena.",
    (5, 4): "> ⚠️ **Častá chyba na maturite:** Nesprávne poradie parametrov v hlavičke funkcie: najprv pozičné, potom `*args`, potom pomenované argumenty a nakoniec `**kwargs`.",
    (5, 5): "> ⚠️ **Častá chyba na maturite:** Chýbajúca bázická (ukončovacia) podmienka v rekurzívnej funkcii, čo vedie k pádu programu s chybou `RecursionError`.",
    (6, 1): "> ⚠️ **Častá chyba na maturite:** Kopírovanie zoznamu cez `b = a`. Tým nevznikne kópia, ale len ďalší odkaz na ten istý zoznam! Na kópiu použi `b = a.copy()` alebo `b = a[:]`.",
    (6, 2): "> ⚠️ **Častá chyba na maturite:** Mazanie prvkov zo zoznamu počas iterácie cez `for item in zoznam: zoznam.remove(item)`. To naruší vnútorné indexy a preskočí susedné prvky!",
    (6, 3): "> ⚠️ **Častá chyba na maturite:** Volanie `zip()` na zoznamy rôznej dĺžky. Vstavaný `zip()` sa zastaví na dĺžke najkratšieho zoznamu a zvyšné prvky ticho zahodí.",
    (6, 4): "> ⚠️ **Častá chyba na maturite:** Zbytočne zložité cykly s `append()` namiesto čistého a rýchleho generátora zoznamov `[x for x in data if cond]`.",
    (6, 5): "> ⚠️ **Častá chyba na maturite:** Pokus o zmenu prvku v n-tici (tuple) cez `tup[0] = x`, čo vyvolá `TypeError`. N-tice sú nemenné (immutable).",
    (7, 1): "> ⚠️ **Častá chyba na maturite:** Prístup k neexistujúcemu kľúču cez `slovnik[kluc]`, čo vyvolá `KeyError`. Vždy používaj bezpečnú metódu `slovnik.get(kluc, default)`.",
    (7, 2): "> ⚠️ **Častá chyba na maturite:** Použitie meniteľného objektu (napr. zoznamu `list`) ako kľúča v slovníku. Kľúč musí byť nemenný (hašovateľný - napr. `int`, `str`, `tuple`).",
    (7, 3): "> ⚠️ **Častá chyba na maturite:** Prístup do hlboko vnoreného JSON slovníka bez ošetrenia chýbajúcich úrovní. Každú úroveň treba overovať alebo reťaziť cez `.get()`.",
    (7, 4): "> ⚠️ **Častá chyba na maturite:** Predpoklad, že prvky v množine `set` si zachovávajú poradie vloženia alebo že k nim možno pristupovať cez index `mnozina[0]`. Množiny sú neusporiadané!",
    (7, 5): "> ⚠️ **Častá chyba na maturite:** Pomalé počítanie frekvencie prvkov cez `zoznam.count(x)` v cykle, čo má kvadratickú zložitosť O(n²). Vždy použi slovník s časom O(n).",
    (8, 1): "> ⚠️ **Častá chyba na maturite:** Použitie holého `except:` bez špecifikácie typu výnimky. To zachytí aj stlačenie Ctrl+C (`KeyboardInterrupt`). Vždy špecifikuj napr. `except ValueError:`.",
    (8, 2): "> ⚠️ **Častá chyba na maturite:** Umiestnenie príliš veľkého bloku kódu do `try`. Do `try` vkladaj iba konkrétny riadok náchylný na chybu, inak riskuješ zachytenie nečakanej inej výnimky.",
    (8, 3): "> ⚠️ **Častá chyba na maturite:** Vyvolanie výnimky bez vytvorenia inštancie alebo textovej správy, napr. `raise ValueError` namiesto popisného `raise ValueError(\"Popis chyby\")`.",
    (8, 4): "> ⚠️ **Častá chyba na maturite:** Neuzavretie dátového prúdu alebo súboru. Vždy používaj kontextový manažér `with open(...) as f:`, ktorý garantuje uzavretie súboru aj pri chybe.",
    (9, 1): "> ⚠️ **Častá chyba na maturite:** Vynechanie parametra `self` v hlavičke metódy triedy, napr. `def pozdrav():` namiesto `def pozdrav(self):`. Vyvolá `TypeError` pri volaní inštancie.",
    (9, 2): "> ⚠️ **Častá chyba na maturite:** Definícia atribútu priamo v tele triedy namiesto konštruktora `__init__`. To vytvorí triedny atribút zdieľaný medzi všetkými inštanciami!",
    (9, 3): "> ⚠️ **Častá chyba na maturite:** Zámena `@classmethod` (prijíma `cls`) a `@staticmethod` (neprijíma ani `self`, ani `cls`). Používaj ich na základe toho, či potrebuješ prístup k triede.",
    (9, 4): "> ⚠️ **Častá chyba na maturite:** Priame prepisovanie atribútu v setter metóde cez `self.hodnota = val`, čo spôsobí nekonečnú rekurziu! Setter musí zapisovať do privátneho atribútu `self._hodnota = val`.",
    (9, 5): "> ⚠️ **Častá chyba na maturite:** Miešanie aplikačnej logiky do prezentačnej vrstvy. Metódy objektu by mali vracať dáta, nie priamo volať `print()`.",
    (10, 1): "> ⚠️ **Častá chyba na maturite:** Zabudnutie volania `super().__init__(...)` v konštruktore dcérskej triedy. Následkom toho sa neinicializujú atribúty rodičovskej triedy!",
    (10, 2): "> ⚠️ **Častá chyba na maturite:** Porušenie Liskovovej princípu zámeny (LSP): prekrytá metóda v potomkovi by nemala meniť počet či typ očakávaných argumentov pôvodnej metódy.",
    (10, 3): "> ⚠️ **Častá chyba na maturite:** Návrat iného typu ako `str` z metódy `__str__(self)`. Python striktne vyžaduje, aby `__str__` vracala reťazec `str`, inak vyvolá `TypeError`.",
    (10, 4): "> ⚠️ **Častá chyba na maturite:** Nastavenie meniteľného predvoleného atribútu v `@dataclass` bez použitia `field(default_factory=list)`.",
    (11, 1): "> ⚠️ **Častá chyba na maturite:** Zanedbanie vplyvu vnorených cyklov na časovú zložitosť. Cyklus v cykle znamená takmer vždy $O(n^2)$, čo je pri veľkých dátach nepoužiteľné.",
    (11, 2): "> ⚠️ **Častá chyba na maturite:** Spustenie binárneho vyhľadávania na NEZORADENÝ zoznam. Binárne vyhľadávanie striktne vyžaduje vopred zoradené pole!",
    (11, 3): "> ⚠️ **Častá chyba na maturite:** Zbytočné prechádzanie celého poľa v Bubble Sorte, aj keď už žiadne výmeny nenastali. Pridaj príznak `vymenene = False` pre skoré ukončenie v $O(n)$.",
    (11, 4): "> ⚠️ **Častá chyba na maturite:** Nepoužitie stabilného triedenia `sorted()` s parametrom `key=lambda x: ...`, čo je v Pythone optimalizovaný algoritmus Timsort v čase $O(n \log n)$.",
    (11, 5): "> ⚠️ **Častá chyba na maturite:** Testovanie prvočíselnosti až do čísla $n$ namiesto hranice $\sqrt{n}$, čo zbytočne dramaticky spomaľuje výpočet.",
}

LESSON_TABLES = {
    (1, 1): "\n#### Prehľad parametrov print()\n\n| Parameter | Význam | Predvolená hodnota |\n| :--- | :--- | :--- |\n| `sep` | Oddeľovač argumentov | `' '` (medzera) |\n| `end` | Ukončovací reťazec | `'\\n'` (nový riadok) |\n| `flush` | Okamžité vyprázdnenie buffera | `False` |\n",
    (1, 2): "\n#### Pravidlá konvencie PEP 8\n\n| Prvok | Konvencia | Príklad |\n| :--- | :--- | :--- |\n| Premenná | snake_case | `pocet_bodov = 10` |\n| Funkcia | snake_case | `def spocitaj():` |\n| Konštanta | UPPER_CASE | `MAX_USERS = 100` |\n| Trieda | PascalCase | `class ZiackaKnizka:` |\n",
    (1, 3): "\n#### Základné skalárne dátové typy v Pythone\n\n| Typ | Názov triedy | Príklad hodnoty | Mutabilita |\n| :--- | :--- | :--- | :--- |\n| `int` | Celé číslo | `42`, `-5` | Nemenný (Immutable) |\n| `float` | Desatinné číslo | `3.14`, `-0.01` | Nemenný (Immutable) |\n| `str` | Textový reťazec | `'Codoro'` | Nemenný (Immutable) |\n| `bool` | Logická hodnota | `True`, `False` | Nemenný (Immutable) |\n",
    (1, 4): "\n#### Metódy a pravidlá pretypovania (Casting)\n\n| Konverzia | Platný vstup | Neplatný vstup (Chyba) |\n| :--- | :--- | :--- |\n| `int(x)` | `'42'`, `3.99` (oreže) | `'3.14'`, `'abc'` -> `ValueError` |\n| `float(x)` | `'3.14'`, `10` | `'abc'` -> `ValueError` |\n| `str(x)` | akýkoľvek objekt | takmer nikdy nezlyhá |\n| `bool(x)` | `0`, `\"\"`, `[]` sú `False` | nenulové a neprázdne sú `True` |\n",
    (1, 5): "\n#### Matematické operácie v Pythone\n\n| Operácia | Operátor | Príklad | Výsledok |\n| :--- | :--- | :--- | :--- |\n| Sčítanie / Odčítanie | `+`, `-` | `10 + 5` | `15` |\n| Násobenie / Delenie | `*`, `/` | `7 / 2` | `3.5` (float) |\n| Celočíselné delenie | `//` | `7 // 2` | `3` (int) |\n| Zvyšok (Modulo) | `%` | `7 % 2` | `1` |\n| Umocňovanie | `**` | `2 ** 3` | `8` |\n",
    (2, 1): "\n#### Aritmetické operátory a priorita\n\n| Operátor | Názov | Priorita | Príklad |\n| :--- | :--- | :--- | :--- |\n| `**` | Umocnenie | Najvyššia | `2 ** 3 == 8` |\n| `*`, `/`, `//`, `%` | Násobenie a delenia | Stredná | `10 // 3 == 3` |\n| `+`, `-` | Sčítanie a odčítanie | Nižšia | `5 + 2 == 7` |\n",
    (2, 2): "\n#### Porovnávacie a logické operátory\n\n| Operátor | Význam | Príklad |\n| :--- | :--- | :--- |\n| `==`, `!=` | Rovnosť / Nerovnosť | `a == b` |\n| `<`, `<=`, `>`, `>=` | Nerovnosti | `vek >= 18` |\n| `and`, `or`, `not` | Logické spojky | `je_student and platny` |\n",
    (2, 3): "\n#### Syntax indexovania a rezania (Slicing)\n\n| Zápis | Význam | Príklad pre `'Python'` |\n| :--- | :--- | :--- |\n| `s[0]` | Prvý znak | `'P'` |\n| `s[-1]` | Posledný znak | `'n'` |\n| `s[1:4]` | Podreťazec od indexu 1 do 3 | `'yth'` |\n| `s[::-1]` | Obrátenie reťazca | `'nohtyP'` |\n",
    (2, 4): "\n#### Najčastejšie metódy reťazcov (str)\n\n| Metóda | Popis | Návratová hodnota |\n| :--- | :--- | :--- |\n| `.strip()` | Odstráni biele znaky po stranách | Nový `str` |\n| `.lower()` / `.upper()` | Zmena veľkosti písmen | Nový `str` |\n| `.replace(old, new)` | Nahradenie podreťazca | Nový `str` |\n| `.split(sep)` | Rozdelenie na zoznam slov | Zoznam `list[str]` |\n",
    (2, 5): "\n#### Spôsoby formátovania textu v Pythone\n\n| Spôsob | Príklad | Odporúčanie |\n| :--- | :--- | :--- |\n| f-string (Python 3.6+) | `f\"Ahoj {meno}, máš {doros} Doros\"` | **Odporúčaný štandard** |\n| `.format()` | `\"Ahoj {}, máš {}\".format(meno, doros)` | Starší kód |\n| `%` operátor | `\"Ahoj %s\" % meno` | Zastaraný C-štýl |\n",
    (3, 1): "\n#### Bloková štruktúra podmienok\n\n| Prvok | Význam | Povinné |\n| :--- | :--- | :--- |\n| `if podmienka:` | Hlavná vyhodnocovaná podmienka | Áno |\n| Odsadenie (4 medzery) | Telo príkazu vykonané pri splnení | Áno |\n| `else:` | Alternatíva pri nesplnení podmienky | Voliteľné |\n",
    (3, 2): "\n#### Porovnanie vetvenia if vs elif\n\n| Zápis | Počet vykonaných vetiev | Vhodnosť |\n| :--- | :--- | :--- |\n| `if ... elif ... else` | Maximálne 1 vetva | Vzájomne sa vylučujúce stavy |\n| Viacero `if ... if ...` | 0 až všetky vetvy | Nezávislé kontroly pravidiel |\n",
    (3, 3): "\n#### Priority logických operátorov\n\n| Operátor | Priorita | Príklad vyhodnotenia |\n| :--- | :--- | :--- |\n| `not` | Najvyššia | `not False` -> `True` |\n| `and` | Stredná | `True and False` -> `False` |\n| `or` | Najnižšia | `False or True` -> `True` |\n",
    (3, 4): "\n#### Pravdivostné hodnoty v Pythone (Truthy / Falsy)\n\n| Typ | Falsy hodnota (vyhodnotí sa ako False) | Príklad Truthy hodnoty |\n| :--- | :--- | :--- |\n| Čísla | `0`, `0.0` | `1`, `-5`, `0.1` |\n| Reťazce | `\"\"` (prázdny) | `\"text\"`, `\" \"` |\n| Zoznamy/Kolekcie | `[]`, `{}`, `set()` | `[1]`, `{\"a\": 1}` |\n| Ostatné | `None` | ľubovoľný objekt |\n",
    (3, 5): "\n#### Syntax porovnávania vzorov (match-case)\n\n| Vzor | Popis | Príklad |\n| :--- | :--- | :--- |\n| `case hodnota:` | Presná zhoda konštanty | `case 200:` |\n| `case vzor_1 \| vzor_2:` | Logické zjednotenie vzorov | `case \"ano\" \| \"yes\":` |\n| `case _:` | Záchytná vetva (Wildcard) | `case _:` |\n",
    (4, 1): "\n#### Parametre funkcie range(start, stop, step)\n\n| Volanie | Vygenerovaná postupnosť | Poznámka |\n| :--- | :--- | :--- |\n| `range(5)` | `0, 1, 2, 3, 4` | Štart od 0, krok 1 |\n| `range(2, 6)` | `2, 3, 4, 5` | Stop je otvorená hranica |\n| `range(10, 0, -2)` | `10, 8, 6, 4, 2` | Klesajúci krok |\n",
    (4, 2): "\n#### Vstavané agregačné funkcie\n\n| Funkcia | Význam | Časová zložitosť |\n| :--- | :--- | :--- |\n| `len(seq)` | Počet prvkov sekvencie | $O(1)$ |\n| `sum(seq)` | Súčet číselných prvkov | $O(n)$ |\n| `min(seq)` / `max(seq)` | Extrémy sekvencie | $O(n)$ |\n",
    (4, 3): "\n#### Porovnanie cyklov for a while\n\n| Kritérium | Cyklus for | Cyklus while |\n| :--- | :--- | :--- |\n| Známy počet opakovaní | **Ideálne** (iterácia cez sekvenciu) | Zbytočne manuálne počítadlo |\n| Podmienka do splnenia | Nevhodné | **Ideálne** (kým platí podmienka) |\n| Riziko nekonečného cyklu | Minimálne | Reálne (pri nezmenení premennej) |\n",
    (4, 4): "\n#### Riadiace príkazy cyklu\n\n| Príkaz | Účinok na cyklus | Vykonanie bloku else |\n| :--- | :--- | :--- |\n| `break` | Okamžite ukončí celý cyklus | `else` sa **nevykoná** |\n| `continue` | Preskočí na ďalšiu iteráciu | `else` sa vykoná po dobehnutí |\n| `pass` | Prázdna operácia (placeholder) | Nemá vplyv |\n",
    (4, 5): "\n#### Reprezentácia 2D matice v pamäti\n\n| Zápis | Správnosť | Dôvod |\n| :--- | :--- | :--- |\n| `[[0]*m for _ in range(n)]` | **Správne** | Každý riadok je nezávislý objekt |\n| `[[0]*m]*n` | **Chybné** | Všetky riadky odkazujú na rovnaký zoznam |\n",
    (5, 1): "\n#### Komponenty definície funkcie\n\n| Časť | Popis | Príklad |\n| :--- | :--- | :--- |\n| `def` | Kľúčové slovo definície funkcie | `def spocitaj(a, b):` |\n| Parametre | Formálne vstupné premenné | `a, b` |\n| `return` | Návrat hodnoty volajúcemu | `return a + b` |\n| `None` | Implicitná návratová hodnota bez return | `x = funkcia_bez_return()` |\n",
    (5, 2): "\n#### Typy argumentov pri volaní funkcie\n\n| Typ argumentu | Charakteristika | Príklad |\n| :--- | :--- | :--- |\n| Pozičný | Priraďuje sa podľa poradia | `vypocet(10, 20)` |\n| Pomenovaný (Keyword) | Priraďuje sa podľa názvu parametra | `vypocet(b=20, a=10)` |\n| Predvolený (Default) | Použije sa, ak volajúci nezadá hodnotu | `def f(mena=\"EUR\"):` |\n",
    (5, 3): "\n#### Pravidlo LEGB pre hľadanie premenných\n\n| Úroveň | Názov rozsahu (Scope) | Popis |\n| :--- | :--- | :--- |\n| **L** | Local | Vnútri aktuálnej funkcie |\n| **E** | Enclosing | Vo vonkajšej obalovej funkcii (uzávery) |\n| **G** | Global | Na úrovni modulu (deklarované globálne) |\n| **B** | Built-in | Vstavané objekty a funkcie Pythonu (`len`, `print`) |\n",
    (5, 4): "\n#### Variabilné argumenty *args a **kwargs\n\n| Zápis | Typ dát | Význam |\n| :--- | :--- | :--- |\n| `*args` | `tuple` | Ľubovoľný počet pozičných argumentov |\n| `**kwargs` | `dict` | Ľubovoľný počet pomenovaných argumentov |\n| `f(*zoznam)` | Rozbalenie | Odovzdá prvky zoznamu ako argumenty |\n| `f(**slovnik)` | Rozbalenie | Odovzdá kľúče a hodnoty ako argumenty |\n",
    (5, 5): "\n#### Anatómia rekurzívnej funkcie\n\n| Komponent | Účel | Dôsledok absencie |\n| :--- | :--- | :--- |\n| Bázický prípad | Zastaví vnorené volania | `RecursionError` (Stack Overflow) |\n| Rekurzívny krok | Zmenšuje problém k bázickému stavu | Nekonečná rekurzia |\n| Stack frame | Pamäťový záznam pre každé volanie | Vyčerpanie pamäte |\n",
    (6, 1): "\n#### Základné metódy zoznamov (list)\n\n| Metóda | Účinok | Časová zložitosť |\n| :--- | :--- | :--- |\n| `.append(x)` | Pridá prvok na koniec | $O(1)$ amortizovane |\n| `.extend(iter)` | Pripojí prvky z iného iterátora | $O(k)$ |\n| `.insert(i, x)` | Vloží prvok na konkrétny index | $O(n)$ |\n| `.pop([i])` | Odstráni a vráti prvok (predvolene posledný) | $O(1)$ koniec, $O(n)$ začiatok |\n| `.remove(x)` | Odstráni prvý výskyt hodnoty | $O(n)$ |\n",
    (6, 2): "\n#### Užitočné funkcie pre iteráciu zoznamov\n\n| Funkcia | Čo vracia | Príklad použitia |\n| :--- | :--- | :--- |\n| `enumerate(seq)` | Dvojice `(index, prvok)` | `for i, item in enumerate(data):` |\n| `reversed(seq)` | Reverzný iterátor | `for x in reversed(items):` |\n| `any(iterable)` | `True` ak aspoň 1 prvok je pravdivý | `if any(x < 0 for x in cisla):` |\n| `all(iterable)` | `True` ak všetky prvky sú pravdivé | `if all(x > 0 for x in cisla):` |\n",
    (6, 3): "\n#### Zoradenie zoznamov a funkcia zip\n\n| Nástroj | Mutabilita | Výsledok |\n| :--- | :--- | :--- |\n| `zoznam.sort()` | Mení pôvodný zoznam in-place | Vracia `None` |\n| `sorted(iterable)` | Pôvodný objekt nemení | Vracia nový zoradený `list` |\n| `zip(a, b)` | Nemení | Iterátor n-tíc `(a[i], b[i])` |\n| `zip(..., strict=True)` | Python 3.10+ | Vyvolá `ValueError` pri nerovnakej dĺžke |\n",
    (6, 4): "\n#### Syntax generátorov zoznamov (List Comprehensions)\n\n| Konštrukcia | Ekvivalentný for cyklus | Príklad |\n| :--- | :--- | :--- |\n| `[f(x) for x in seq]` | Mapovanie | `[x*2 for x in cisla]` |\n| `[x for x in seq if cond]` | Filtrovanie | `[x for x in cisla if x % 2 == 0]` |\n| `[f(x) if c else g(x) for x in seq]` | Podmienená transformácia | `[x if x > 0 else 0 for x in data]` |\n",
    (6, 5): "\n#### Porovnanie zoznamu (list) a n-tice (tuple)\n\n| Vlastnosť | Zoznam (`list`) | N-tica (`tuple`) |\n| :--- | :--- | :--- |\n| Syntax | `[1, 2, 3]` | `(1, 2, 3)` |\n| Meniteľnosť (Mutabilita) | Meniteľný (Mutable) | **Nemenný (Immutable)** |\n| Použitie ako kľúč slovníka | ❌ Nemožné (nehašovateľný) | ✅ Možné (hašovateľný) |\n| Pamäťová réžia | Väčšia (dynamická alokácia) | Menšia, rýchlejší prístup |\n",
    (7, 1): "\n#### Základné operácie so slovníkmi (dict)\n\n| Operácia | Syntax | Chovanie pri neexistujúcom kľúči |\n| :--- | :--- | :--- |\n| Prístup cez index | `slovnik[kluc]` | Vyvolá `KeyError` |\n| Bezpečný prístup | `slovnik.get(kluc, default)` | Vráti `default` (alebo `None`) |\n| Priradenie/Zmena | `slovnik[kluc] = hodnota` | Vytvorí kľúč alebo prepíše hodnotu |\n| Vymazanie | `del slovnik[kluc]` | Vyvolá `KeyError` |\n",
    (7, 2): "\n#### Pohľady a metódy iterácie slovníka\n\n| Metóda | Čo vracia | Časová zložitosť |\n| :--- | :--- | :--- |\n| `.keys()` | Dynamický pohľad na kľúče | $O(1)$ |\n| `.values()` | Dynamický pohľad na hodnoty | $O(1)$ |\n| `.items()` | Dvojice `(kluc, hodnota)` | $O(1)$ |\n| `.update(iny_dict)` | Spojenie slovníkov in-place | $O(k)$ |\n",
    (7, 3): "\n#### Bezpečný prístup do vnorených štruktúr\n\n| Spôsob | Kód | Bezpečnosť pri chýbajúcom kľúči |\n| :--- | :--- | :--- |\n| Priamy reťazec | `data[\"user\"][\"profile\"][\"email\"]` | ❌ Zlyhá s `KeyError` |\n| Reťazenie .get() | `data.get(\"user\", {}).get(\"profile\", {}).get(\"email\")` | ✅ Bezpečne vráti `None` |\n| Operátor zlúčenia | `novy = dict_a \| dict_b` (Python 3.9+) | Vytvorí zlúčený slovník |\n",
    (7, 4): "\n#### Množinové operácie v Pythone\n\n| Operácia | Operátor | Metóda | Význam |\n| :--- | :--- | :--- | :--- |\n| Zjednotenie | `a \| b` | `a.union(b)` | Všetky unikátne prvky z oboch |\n| Prienik | `a & b` | `a.intersection(b)` | Len spoločné prvky |\n| Rozdiel | `a - b` | `a.difference(b)` | Prvky v `a`, ktoré nie sú v `b` |\n| Symetrický rozdiel | `a ^ b` | `a.symmetric_difference(b)` | Prvky iba v jednej z množín |\n",
    (7, 5): "\n#### Porovnanie prístupov frekvenčnej analýzy\n\n| Spôsob | Kód | Časová zložitosť |\n| :--- | :--- | :--- |\n| Naivný cyklus s `.count()` | `[zoznam.count(x) for x in zoznam]` | $O(n^2)$ – pomalé! |\n| Bežný slovník | `for x in data: d[x] = d.get(x, 0) + 1` | $O(n)$ – optimálne |\n| `collections.Counter` | `Counter(data)` | $O(n)$ – štandardná knižnica |\n",
    (8, 1): "\n#### Bloky ošetrenia výnimiek\n\n| Blok | Kedy sa vykoná | Povinný |\n| :--- | :--- | :--- |\n| `try:` | Chránený kód, ktorý môže vyvolať výnimku | Áno |\n| `except TypChyby as e:` | Iba ak v `try` nastane špecifikovaná výnimka | Áno (aspoň 1) |\n| `else:` | Iba ak v `try` **nenastala** žiadna chyba | Voliteľný |\n| `finally:` | **Vždy**, aj pri chybe, aj pri `return` | Voliteľný |\n",
    (8, 2): "\n#### Bežné štandardné výnimky v Pythone\n\n| Výnimka | Typická príčina | Príklad |\n| :--- | :--- | :--- |\n| `ValueError` | Správny typ, nesprávna hodnota | `int(\"abc\")` |\n| `TypeError` | Nesprávny typ operandu | `\"text\" + 5` |\n| `IndexError` | Index sekvencie mimo rozsahu | `[1, 2][5]` |\n| `KeyError` | Kľúč v slovníku neexistuje | `{\"a\": 1}[\"b\"]` |\n| `ZeroDivisionError` | Delenie nulou | `10 / 0` |\n",
    (8, 3): "\n#### Príkaz raise a vlastné výnimky\n\n| Príkaz | Účel | Príklad |\n| :--- | :--- | :--- |\n| `raise Chyba(\"správa\")` | Vyvolanie novej výnimky | `raise ValueError(\"Záporná cena\")` |\n| `raise` (samotný) | Opätovné vyvolanie aktuálnej chyby v `except` | `except Exception: log(); raise` |\n| `class MojaChyba(Exception):` | Definícia vlastnej doménovej výnimky | `class CodoroCreditError(Exception): pass` |\n",
    (8, 4): "\n#### Režimy otvárania súborov\n\n| Režim | Význam | Správanie ak súbor neexistuje |\n| :--- | :--- | :--- |\n| `'r'` | Čítanie textu (predvolené) | Vyvolá `FileNotFoundError` |\n| `'w'` | Zápis textu (prepíše obsah) | Vytvorí nový súbor |\n| `'a'` | Pridávanie na koniec súboru (Append) | Vytvorí nový súbor |\n| `'r+'` | Čítanie aj zápis | Vyvolá `FileNotFoundError` |\n",
    (9, 1): "\n#### Základné pojmy OOP\n\n| Pojem | Popis | Analógia z reálneho sveta |\n| :--- | :--- | :--- |\n| Trieda (`class`) | Šablóna, vzor, predpis pre objekty | Architektonický výkres domu |\n| Inštancia / Objekt | Konkrétny exemplár vytvorený z triedy | Postavený dom na konkrétnej ulici |\n| Atribút | Stavová premenná viazaná na objekt | Farba fasády, počet izieb |\n| Metóda | Funkcia manipulujúca so stavom objektu | Zamknúť dvere, rozsvietiť svetlo |\n",
    (9, 2): "\n#### Konštruktor __init__ a parameter self\n\n| Prvok | Význam | Pravidlo |\n| :--- | :--- | :--- |\n| `__init__(self, ...)` | Špeciálna metóda volaná automaticky pri tvorbe objektu | Inicializuje atribúty inštancie |\n| `self` | Odkaz na konkrétnu inštanciu | Musí byť 1. parametrom každej bežnej metódy |\n| `self.meno = meno` | Uloženie hodnoty do stavu inštancie | Sprístupní atribút v iných metódach |\n",
    (9, 3): "\n#### Úrovne viditeľnosti atribútov (Zapuzdrenie)\n\n| Zápis | Úroveň | Konvencia / Správanie |\n| :--- | :--- | :--- |\n| `self.nazov` | Verejný (Public) | Prístupný odkiaľkoľvek bez obmedzenia |\n| `self._nazov` | Chránený (Protected) | Konvencia: interný atribút, neupravovať zvonku |\n| `self.__nazov` | Súkromný (Private) | Name Mangling: prepíše sa na `_Trieda__nazov` |\n",
    (9, 4): "\n#### Dekorátory vlastností @property\n\n| Dekorátor | Účel | Syntax prístupu |\n| :--- | :--- | :--- |\n| `@property` | Getter – čítanie hodnoty ako atribút | `hodnota = objekt.polomer` |\n| `@nazov.setter` | Setter – validácia pri zápise | `objekt.polomer = 10` |\n| `@nazov.deleter` | Deleter – upratanie pri vymazaní | `del objekt.polomer` |\n",
    (9, 5): "\n#### Typy metód v triedach Pythonu\n\n| Typ metódy | Dekorátor | Prvý parameter | K čomu má prístup |\n| :--- | :--- | :--- | :--- |\n| Inštancie | *žiadny* | `self` | K inštancii aj triede |\n| Triedy | `@classmethod` | `cls` | Iba k triede (továrenské metódy) |\n| Statická | `@staticmethod` | *žiadny* | Nemá prístup ani k `self`, ani k `cls` |\n",
    (10, 1): "\n#### Dedičnosť (Inheritance)\n\n| Pojem | Popis | Príklad |\n| :--- | :--- | :--- |\n| Rodičovská trieda | Všeobecná trieda obsahujúca spoločné správanie | `class Vozidlo:` |\n| Dcérska trieda | Špecializovaná trieda dediaca z rodiča | `class Elektromobil(Vozidlo):` |\n| `isinstance(obj, Trieda)` | Overí, či objekt patrí danej triede | `isinstance(tesla, Vozidlo) == True` |\n| `issubclass(A, B)` | Overí dedičnú hierarchiu medzi triedami | `issubclass(Elektromobil, Vozidlo)` |\n",
    (10, 2): "\n#### Funkcia super()\n\n| Volanie | Účinok | Využitie |\n| :--- | :--- | :--- |\n| `super().__init__(...)` | Zavolá konštruktor predka | Inicializácia spoločných atribútov rodiča |\n| `super().metoda()` | Vykoná implementáciu metódy v rodičovi | Rozšírenie správania bez prepísania |\n| MRO | Poradie prehľadávania tried pri dedičnosti | Zobrazenie cez `Trieda.__mro__` |\n",
    (10, 3): "\n#### Najdôležitejšie magické (Dunder) metódy\n\n| Metóda | Spúšťač v Pythone | Návratová hodnota |\n| :--- | :--- | :--- |\n| `__str__(self)` | `str(obj)`, `print(obj)` | Užívateľsky čitateľný `str` |\n| `__repr__(self)` | `repr(obj)`, interaktívna konzola | Technická reprezentácia pre vývojára |\n| `__len__(self)` | `len(obj)` | Nezáporné celé číslo `int` |\n| `__eq__(self, iny)` | `obj == iny` | Logická hodnota `bool` |\n| `__lt__(self, iny)` | `obj < iny` (pre `sorted()`) | Logická hodnota `bool` |\n",
    (10, 4): "\n#### Výhody dekorátora @dataclass\n\n| Tradičná trieda | Dátová trieda (@dataclass) | Automaticky generované metódy |\n| :--- | :--- | :--- |\n| Manuálny `__init__` s priradeniami | Typové anotácie atribútov | `__init__` |\n| Vlastná implementácia `__repr__` | Prehľadný výpis atribútov | `__repr__` |\n| Manuálne porovnávanie v `__eq__` | Porovnanie hodnôt atribútov | `__eq__` |\n| Voliteľné zmrazenie | `frozen=True` (nemenný objekt) | `__hash__` |\n",
    (11, 1): "\n#### Prehľad asymptotických časových zložitostí (Big-O)\n\n| Notácia | Názov | Príklad algoritmu | Správanie pri $n = 1000$ |\n| :--- | :--- | :--- | :--- |\n| $O(1)$ | Konštantná | Prístup do slovníka / k prvku poľa | Okamžité (1 krok) |\n| $O(\\log n)$ | Logaritmická | Binárne vyhľadávanie | $\\approx 10$ krokov |\n| $O(n)$ | Lineárna | Lineárne prehľadávanie poľa | $1000$ krokov |\n| $O(n \\log n)$ | Linearitmická | Merge Sort, Timsort (`sorted()`) | $\\approx 10\\,000$ krokov |\n| $O(n^2)$ | Kvadratická | Bubble Sort, dva vnorené cykly | $1\\,000\\,000$ krokov |\n| $O(2^n)$ | Exponenciálna | Naivný rekurzívny Fibonacci | $10^{300}$ krokov |\n",
    (11, 2): "\n#### Porovnanie vyhľadávacích algoritmov\n\n| Kritérium | Lineárne vyhľadávanie | Binárne vyhľadávanie |\n| :--- | :--- | :--- |\n| Predpoklad na vstupné dáta | Žiadny (ľubovoľný zoznam) | **Striktne zoradený zoznam** |\n| Časová zložitosť v najhoršom prípade | $O(n)$ | **$O(\\log n)$** |\n| Pamäťová náročnosť | $O(1)$ | $O(1)$ iteratívne |\n| Vhodnosť použitia | Malé alebo nezoradené polia | Veľké zoradené polia |\n",
    (11, 3): "\n#### Porovnanie elementárnych triedení\n\n| Algoritmus | Najlepší čas | Priemerný / Najhorší čas | Pamäť | Stabilita |\n| :--- | :--- | :--- | :--- | :--- |\n| Bubble Sort | $O(n)$ (s príznakom) | $O(n^2)$ | $O(1)$ | Stabilný |\n| Selection Sort | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Nestabilný |\n| Insertion Sort | $O(n)$ (takmer zoradené) | $O(n^2)$ | $O(1)$ | Stabilný |\n",
    (11, 4): "\n#### Pokročilé triediace algoritmy\n\n| Algoritmus | Princíp | Časová zložitosť | Poznámka |\n| :--- | :--- | :--- | :--- |\n| Merge Sort | Rozdeľ a panuj (Divide & Conquer) | $O(n \\log n)$ garantovane | Vyžaduje $O(n)$ pamäte |\n| Quick Sort | Výber pivota a rozdelenie | $O(n \\log n)$ priem., $O(n^2)$ najhorší | In-place |\n| Timsort | Hybrid Insertion + Merge Sort | $O(n)$ až $O(n \\log n)$ | **Vstavaný triediaci algoritmus Pythonu** |\n",
    (11, 5): "\n#### Dôležité algoritmické koncepty pre maturitu\n\n| Technika / Algoritmus | Oblasť použitia | Princíp fungovania |\n| :--- | :--- | :--- |\n| Dva ukazovatele (Two Pointers) | Palindrómy, zlučovanie | Zbiehanie indexov z oboch strán poľa v $O(n)$ |\n| Eratostenovo sito | Prvočísla do čísla $N$ | Vyškrtávanie násobkov prvočísel v $O(n \\log \\log n)$ |\n| Luhnov algoritmus | Kontrola platobných kariet | Overenie kontrolného súčtu modulo 10 |\n",
}

def enrich_all_modules(modules_list):
    """
    Obohatí moduly 1 až 11 o:
    - Správny 'track'
    - Prehľadovú tabuľku syntaxe v Markdowne
    - Školské upozornenie na časté chyby na maturite
    - 3 plné praktické cvičenia (EASY, MEDIUM, HARD)
    """
    diff_order = {'EASY': 1, 'MEDIUM': 2, 'HARD': 3}
    for m in modules_list:
        mod_order = m.get('order')
        if mod_order in TRACK_MAP:
            m['track'] = TRACK_MAP[mod_order]
        
        # Obohatenie lekcií modulov 1 až 11
        if mod_order <= 11:
            for les in m.get('lessons', []):
                les_order = les.get('order')
                key = (mod_order, les_order)
                
                # Pridanie tabuľky a upozornenia do content_sk
                content = les.get('content_sk', '')
                table = LESSON_TABLES.get(key, '')
                warning = MATURITA_WARNINGS.get(key, '')
                
                additions = []
                if table and table.strip() not in content:
                    additions.append(table)
                if warning and warning.strip() not in content:
                    additions.append(f"\n{warning}\n")
                
                if additions:
                    les['content_sk'] = content + "\n\n" + "\n".join(additions)
                
                # Zjednotenie cvičení: pôvodné + sprievodné
                existing_exercises = les.get('exercises', [])
                companions = COMPANIONS.get(key, [])
                
                combined = list(existing_exercises)
                existing_titles = {e.get('title_sk') for e in existing_exercises}
                for comp in companions:
                    if comp.get('title_sk') not in existing_titles:
                        combined.append(comp)
                
                # Zoradenie podľa obťažnosti: EASY -> 1, MEDIUM -> 2, HARD -> 3
                combined.sort(key=lambda x: diff_order.get(x.get('difficulty', 'EASY'), 1))
                
                for idx, ex in enumerate(combined[:3], start=1):
                    ex['order'] = idx
                    if idx == 1:
                        ex['difficulty'] = 'EASY'
                    elif idx == 2:
                        ex['difficulty'] = 'MEDIUM'
                    elif idx == 3:
                        ex['difficulty'] = 'HARD'
                
                les['exercises'] = combined[:3]
                
    return modules_list
