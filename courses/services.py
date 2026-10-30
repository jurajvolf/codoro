"""
Servisná vrstva výučbového modulu Codoro:
1. Bezpečný sandbox na spúšťanie študentského Python kódu (AST kontrola + izolovaný podproces s timeoutom).
2. Sokratovský AI tútor Codo (Google Gemini API + deterministický lokálny fallback).
3. AI nástroje pre učiteľa: generátor nového cvičenia a prekladač SK -> EN.
"""
import ast
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

from django.conf import settings


class EvaluationResult(tuple):
    """Trojica (passed, status, log) s dodatočným atribútom execution_time_ms."""
    def __new__(cls, passed, status, log, execution_time_ms=0):
        obj = super().__new__(cls, (passed, status, log))
        obj.passed = passed
        obj.status = status
        obj.log = log
        obj.execution_time_ms = execution_time_ms
        return obj


# ----------------------------------------------------------------------
# 1. SANDBOX
# ----------------------------------------------------------------------
FORBIDDEN_MODULES = {
    'os', 'sys', 'subprocess', 'shutil', 'socket', 'ctypes', 'importlib', 'pathlib',
    'builtins', 'multiprocessing', 'threading', 'signal', 'pickle', 'marshal', 'urllib',
    'http', 'requests', 'glob', 'tempfile', 'io', 'inspect', 'gc', 'code', 'pty', 'asyncio',
    'webbrowser', 'ftplib', 'smtplib', 'resource', 'platform',
}
FORBIDDEN_CALLS = {
    'open', 'eval', 'exec', 'compile', '__import__', 'globals', 'locals', 'vars',
    'getattr', 'setattr', 'delattr', 'breakpoint', 'exit', 'quit', 'help', 'memoryview',
}
FORBIDDEN_DUNDERS = {
    '__builtins__', '__subclasses__', '__globals__', '__bases__', '__base__', '__mro__',
    '__code__', '__loader__', '__spec__', '__import__', '__getattribute__', '__closure__',
}
FORBIDDEN_ATTRIBUTES = {
    'gi_frame', 'gi_code', 'cr_frame', 'cr_code', 'ag_frame', 'ag_code',
    'f_builtins', 'f_globals', 'f_locals', 'f_code', 'f_back', 'f_trace',
    'co_code', 'co_consts', 'co_names', 'co_varnames', 'tb_frame', 'tb_next',
    'mro',
}

# Spätná kompatibilita (pôvodný zoznam použitý v dokumentácii)
FORBIDDEN_KEYWORDS = ['import os', 'import sys', 'import subprocess', 'import shutil', '__import__', 'open(', 'eval(', 'exec(']


def _msg(lang, sk, en):
    return en if lang == 'en' else sk


def check_code_safety(code, lang='sk'):
    """
    Statická analýza kódu pomocou abstraktného syntaktického stromu (AST).
    Na rozdiel od jednoduchého hľadania reťazcov odhalí aj obchádzky typu
    `from os import system` alebo `import os as o`.
    Vráti (True, None) ak je kód bezpečný, inak (False, chybová_správa).
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        line = exc.lineno or '?'
        return False, _msg(
            lang,
            f"[SyntaxError] Chyba na riadku {line}: {exc.msg}\n\nTip: Skontroluj dvojbodky, zátvorky, úvodzovky a odsadenie.",
            f"[SyntaxError] Error on line {line}: {exc.msg}\n\nTip: Check colons, brackets, quotes and indentation."
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in FORBIDDEN_MODULES:
                    return False, _blocked(lang, f"import {alias.name}", node.lineno)
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] in FORBIDDEN_MODULES:
                return False, _blocked(lang, f"from {node.module} import ...", node.lineno)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                return False, _blocked(lang, f"{node.func.id}()", node.lineno)
            elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_CALLS:
                return False, _blocked(lang, f".{node.func.attr}()", node.lineno)
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_DUNDERS:
            return False, _blocked(lang, node.id, node.lineno)
        elif isinstance(node, ast.Attribute) and (node.attr in FORBIDDEN_DUNDERS or node.attr in FORBIDDEN_ATTRIBUTES):
            return False, _blocked(lang, f".{node.attr}", node.lineno)
    return True, None


def _blocked(lang, what, line):
    return _msg(
        lang,
        f"[Bezpečnostná ochrana Codoro] Príkaz '{what}' (riadok {line}) nie je v cvičeniach povolený.",
        f"[Codoro Security Guard] Command '{what}' (line {line}) is not permitted in exercises."
    )


def _sandbox_env():
    env = {'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1'}
    # Na Windows Python potrebuje SYSTEMROOT na inicializáciu generátora náhodných čísel
    for key in ('SYSTEMROOT', 'SystemRoot'):
        if os.environ.get(key):
            env[key] = os.environ[key]
    return env


def _run_isolated(script, workdir, timeout):
    path = os.path.join(workdir, 'solution.py')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(script)
    return subprocess.run(
        [sys.executable, '-I', path],   # -I = izolovaný režim (ignoruje PYTHONPATH a používateľské balíky)
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=timeout,
        stdin=subprocess.DEVNULL,       # input() nesmie zablokovať server
        cwd=workdir,
        env=_sandbox_env(),
    )


def _last_error_line(stderr):
    lines = [ln for ln in (stderr or '').strip().splitlines() if ln.strip()]
    return lines[-1] if lines else ''


def _clean_traceback(stderr, workdir):
    text = (stderr or '').replace(os.path.join(workdir, 'solution.py'), 'solution.py')
    return text.strip()


def evaluate_python_code(exercise, student_code, lang='sk', custom_test_cases=None):
    """
    Bezpečne spustí študentský Python kód oproti všetkým TestCase prípadom danej úlohy
    alebo zoznamu custom_test_cases.
    Vráti EvaluationResult: (passed_all: bool, status_str: str, output_log: str) s .execution_time_ms
    """
    t_start = time.perf_counter()

    def _ret(passed, status, log):
        ms = int((time.perf_counter() - t_start) * 1000)
        return EvaluationResult(passed, status, log, ms)

    is_safe, error = check_code_safety(student_code, lang)
    if not is_safe:
        return _ret(False, 'ERROR', error)

    timeout = getattr(settings, 'SANDBOX_TIMEOUT_SECONDS', 3)
    max_chars = getattr(settings, 'SANDBOX_MAX_OUTPUT_CHARS', 2000)

    if custom_test_cases is not None:
        test_cases = list(custom_test_cases)
        for tc_item in test_cases:
            tc_code = tc_item.get('test_code', '') if isinstance(tc_item, dict) else getattr(tc_item, 'test_code', '')
            if tc_code:
                tc_safe, tc_err = check_code_safety(tc_code, lang)
                if not tc_safe:
                    return _ret(False, 'ERROR', _msg(lang, f"Nebezpečný testovací kód: {tc_err}", f"Unsafe test code: {tc_err}"))
    elif exercise:
        test_cases = list(exercise.test_cases.all())
    else:
        test_cases = []

    results_log = []
    all_passed = True
    stdout_preview = ''

    with tempfile.TemporaryDirectory(prefix='codoro_') as workdir:
        if not test_cases:
            try:
                proc = _run_isolated(student_code, workdir, timeout)
            except subprocess.TimeoutExpired:
                return _ret(False, 'ERROR', _timeout_msg(lang, timeout))
            if proc.returncode != 0:
                return _ret(False, 'ERROR', _clean_traceback(proc.stderr, workdir)[-max_chars:])
            out = (proc.stdout or '')[:max_chars]
            return _ret(True, 'PASSED', _msg(lang, "[PASS] Kód bol úspešne spustený.", "[PASS] Code ran successfully.") + (
                f"\n\n--- stdout ---\n{out}" if out else ''))

        for index, tc in enumerate(test_cases, start=1):
            is_hidden = getattr(tc, 'is_hidden', False) if not isinstance(tc, dict) else tc.get('is_hidden', False)
            input_data = getattr(tc, 'input_data', '') if not isinstance(tc, dict) else tc.get('input_data', '')
            test_code = getattr(tc, 'test_code', '') if not isinstance(tc, dict) else tc.get('test_code', '')

            if is_hidden:
                label = _msg(lang, f"Skrytý test #{index}", f"Hidden test #{index}")
            else:
                label = f"Test #{index} ({input_data})" if input_data else f"Test #{index}"
            full_script = f"{student_code}\n\n# --- AUTOMATICKÝ TEST CODORO ---\n{test_code}\n"

            try:
                proc = _run_isolated(full_script, workdir, timeout)
            except subprocess.TimeoutExpired:
                return _ret(False, 'ERROR', "\n".join(results_log + [_timeout_msg(lang, timeout)]))

            if index == 1 and proc.stdout:
                stdout_preview = proc.stdout[:max_chars]

            if proc.returncode == 0:
                results_log.append(f"[PASS] {label}: " + _msg(lang, "ÚSPEŠNÝ", "PASSED"))
                continue

            all_passed = False
            stderr = proc.stderr or ''
            err_line = _last_error_line(stderr)
            if 'EOFError' in stderr:
                err_line = _msg(
                    lang,
                    "EOFError – cvičenia sa testujú cez funkcie, nepoužívaj input().",
                    "EOFError – exercises are tested through functions, don't use input()."
                )
            elif err_line.strip() == 'AssertionError':
                err_line = _msg(lang, "Nesprávny výsledok", "Wrong result")
            if is_hidden and err_line.startswith('AssertionError'):
                err_line = _msg(lang, "Nesprávny výsledok pre skrytý vstup", "Wrong result for a hidden input")
            results_log.append(f"[FAIL] {label}: " + _msg(lang, "ZLYHAL", "FAILED") + f" -> {err_line}")

            if any(e in stderr for e in ('SyntaxError', 'IndentationError', 'NameError', 'TypeError')) \
                    and 'AssertionError' not in stderr:
                detail = _clean_traceback(stderr, workdir)[-max_chars:]
                return _ret(False, 'ERROR', "\n".join(results_log) + "\n\n" + _msg(lang, "Detail chyby:", "Error details:") + f"\n{detail}")

    passed_n = sum(1 for r in results_log if r.startswith('[PASS]'))
    summary = _msg(lang, f"\n\nVýsledok: {passed_n}/{len(test_cases)} testov prešlo.",
                   f"\n\nResult: {passed_n}/{len(test_cases)} tests passed.")
    log = "\n".join(results_log) + summary
    if stdout_preview:
        log += f"\n\n--- {_msg(lang, 'Výpis tvojho programu (stdout)', 'Your program output (stdout)')} ---\n{stdout_preview}"
    return _ret(all_passed, ('PASSED' if all_passed else 'FAILED'), log)


def _timeout_msg(lang, timeout):
    return _msg(
        lang,
        f"[Timeout] Časový limit vypršal (> {timeout}s)! Skontroluj, či tvoj kód neobsahuje nekonečný cyklus.",
        f"[Timeout] Time limit exceeded (> {timeout}s)! Check your code for an infinite loop."
    )


# ----------------------------------------------------------------------
# 2. GEMINI API
# ----------------------------------------------------------------------
def _gemini_key():
    return os.environ.get('GEMINI_API_KEY') or getattr(settings, 'GEMINI_API_KEY', '')


def ai_is_configured():
    return bool(_gemini_key())


def call_gemini(prompt, timeout=8, json_mode=False):
    """Zavolá Google Gemini REST API. Pri akejkoľvek chybe vráti None (volajúci použije fallback)."""
    api_key = _gemini_key()
    if not api_key:
        return None
    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    if json_mode:
        body["generationConfig"] = {"responseMimeType": "application/json"}
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return None


# ----------------------------------------------------------------------
# 3. SOKRATOVSKÝ AI TÚTOR CODO
# ----------------------------------------------------------------------
def get_codo_ai_feedback(exercise, student_code, error_log, lang='sk'):
    """
    Sokratovský AI tútor Codo. Ak je nastavený GEMINI_API_KEY, zavolá Google Gemini.
    Ak kľúč nie je nastavený alebo API zlyhá, poskytne lokálnu diagnostiku kódu, aby ukážka vždy fungovala.
    """
    instructions = exercise.instructions_en if lang == 'en' else exercise.instructions_sk
    if lang == 'en':
        prompt = (
            "You are Codo, a friendly Socratic AI tutor on the Codoro platform for high-school students learning Python. "
            "Respond in English. NEVER write the finished solution or a corrected version of the code! "
            "In 2-3 short sentences explain where the logical or syntax mistake is (mention the line if possible) "
            "and end with one guiding question. You may use inline `code` for single identifiers only.\n\n"
        )
    else:
        prompt = (
            "Si Codo, priateľský Sokratovský AI tútor na platforme Codoro pre stredoškolákov, ktorí sa učia Python. "
            "Odpovedaj po slovensky. NIKDY nenapíš študentovi hotové riešenie ani opravený kód! "
            "V 2-3 krátkych vetách vysvetli, kde urobil logickú alebo syntaktickú chybu (ak vieš, spomeň riadok), "
            "a zakonči jednou návodnou otázkou. Inline `kód` používaj iba pre jednotlivé názvy.\n\n"
        )
    prompt += (
        f"Exercise / Zadanie:\n{instructions}\n\n"
        f"Student code / Kód študenta:\n{student_code}\n\n"
        f"Test output / Výstup testov:\n{error_log}"
    )
    answer = call_gemini(prompt, timeout=8)
    if answer:
        return answer.strip()
    return local_socratic_feedback(student_code, error_log, lang)


def local_socratic_feedback(student_code, error_log, lang='sk'):
    """Deterministická lokálna Sokratovská analýza (funguje okamžite aj bez internetu a API kľúča)."""
    log = error_log or ''
    last_line = next((ln for ln in reversed(log.splitlines()) if ln.strip().startswith(('FAIL', 'CHYBA', '[FAIL]', 'Error', 'Exception'))), '')
    last_line = last_line or (log.strip().splitlines()[-1] if log.strip() else '')

    rules = [
        ('Timeout' in log or 'limit vypršal' in log,
         "Codo: Tvoj program beží príliš dlho. Mení sa v tvojom cykle `while` premenná z podmienky? Kedy by mal cyklus skončiť?",
         "Codo: Your program runs too long. Does the variable in your `while` condition ever change? When should the loop stop?"),
        ('Bezpečnostná ochrana' in log or 'Security' in log,
         "Codo: Tento príkaz je v cvičeniach zablokovaný z bezpečnostných dôvodov. Dá sa úloha vyriešiť len pomocou premenných, podmienok a cyklov?",
         "Codo: That statement is blocked for security reasons. Can you solve the task using only variables, conditions and loops?"),
        ('IndentationError' in log,
         "Codo: Python je citlivý na odsadenie. Sú všetky riadky vo vnútri funkcie, `if` alebo `for` odsadené o rovnaký počet medzier (4)?",
         "Codo: Python is sensitive to indentation. Are all lines inside your function, `if` or `for` indented by the same 4 spaces?"),
        ('SyntaxError' in log or 'Syntaktická' in log or 'Syntax error' in log,
         "Codo: Python nerozumie zápisu kódu. Nechýba ti na konci riadku s `def`, `if` alebo `for` dvojbodka `:`, alebo nejaká zátvorka?",
         "Codo: Python can't parse your code. Are you missing a colon `:` after `def`, `if` or `for`, or a closing bracket?"),
        ('NameError' in log,
         "Codo: Používaš názov, ktorý Python nepozná. Je funkcia pomenovaná presne tak ako v zadaní a je premenná definovaná skôr, než ju použiješ?",
         "Codo: You're using a name Python doesn't know. Is the function named exactly like in the task, and is every variable defined before use?"),
        ('TypeError' in log,
         "Codo: Nastala chyba typov. Nesčítavaš náhodou text (`str`) s číslom (`int`), alebo voláš funkciu s iným počtom parametrov?",
         "Codo: There's a type error. Are you adding text (`str`) to a number (`int`), or calling a function with the wrong number of arguments?"),
        ('pass' in student_code and 'return' not in student_code,
         "Codo: Vidím, že vo funkcii máš stále príkaz `pass` a chýba ti `return`. Aký výpočet má funkcia vykonať a vrátiť?",
         "Codo: I see you still have `pass` in your function and no `return` statement. What value should your function compute and send back?"),
        ('def ' in student_code and 'return' not in student_code,
         "Codo: Tvoja funkcia nevracia žiadnu hodnotu! Testy kontrolujú výsledok vrátený cez `return`, nie iba výpis cez `print()`.",
         "Codo: Your function doesn't return anything! Tests check the value sent back with `return`, not just `print()`."),
    ]
    for condition, sk, en in rules:
        if condition:
            return en if lang == 'en' else sk
    if lang == 'en':
        return (f"Codo: Look closely at the test output: „{last_line}“. "
                "Which input breaks your code? Check math operators and boundaries (e.g. `>` vs `>=`).")
    return (f"Codo: Pozri sa na správu z testu: „{last_line}“. "
            "Pre aký vstup tvoj kód zlyhá? Skontroluj znamienka vo výpočte a hraničné podmienky (napr. `>` vs `>=`).")


# ----------------------------------------------------------------------
# 4. AI GENERÁTOR CVIČENÍ PRE UČITEĽA
# ----------------------------------------------------------------------
FALLBACK_EXERCISE_BANK = [
    {
        'keywords': ['premenn', 'variab', 'typ', 'základ', 'basic'],
        'title_sk': 'Obvod obdĺžnika', 'title_en': 'Rectangle Perimeter',
        'instructions_sk': "Napíš funkciu `obvod(a, b)`, ktorá vráti obvod obdĺžnika so stranami `a` a `b`.\n\nVzorec: **o = 2 · (a + b)**",
        'instructions_en': "Write a function `obvod(a, b)` that returns the perimeter of a rectangle with sides `a` and `b`.\n\nFormula: **p = 2 · (a + b)**",
        'starter_code': "def obvod(a, b):\n    pass\n",
        'solution_code': "def obvod(a, b):\n    return 2 * (a + b)\n",
        'tests': ["assert obvod(2, 3) == 10", "assert obvod(0, 5) == 10", "assert obvod(7, 7) == 28"],
        'hint_sk': "Sčítaj strany v zátvorke a výsledok vynásob dvomi.", 'hint_en': "Add the sides in brackets and multiply by two.",
    },
    {
        'keywords': ['podmienk', 'if', 'vetv', 'condition', 'branch'],
        'title_sk': 'Párne alebo nepárne', 'title_en': 'Even or Odd',
        'instructions_sk': "Napíš funkciu `parita(n)`, ktorá vráti text `'parne'`, ak je číslo `n` párne, inak vráti `'neparne'`.",
        'instructions_en': "Write a function `parita(n)` that returns `'parne'` if `n` is even, otherwise `'neparne'`.",
        'starter_code': "def parita(n):\n    pass\n",
        'solution_code': "def parita(n):\n    return 'parne' if n % 2 == 0 else 'neparne'\n",
        'tests': ["assert parita(4) == 'parne'", "assert parita(7) == 'neparne'", "assert parita(0) == 'parne'"],
        'hint_sk': "Zvyšok po delení zistíš operátorom `%`.", 'hint_en': "Use the modulo operator `%` to get the remainder.",
    },
    {
        'keywords': ['cykl', 'for', 'while', 'loop', 'opak'],
        'title_sk': 'Súčet čísel od 1 po n', 'title_en': 'Sum from 1 to n',
        'instructions_sk': "Napíš funkciu `sucet_do(n)`, ktorá pomocou cyklu vráti súčet všetkých celých čísel od 1 po `n` (vrátane).",
        'instructions_en': "Write a function `sucet_do(n)` that uses a loop to return the sum of all integers from 1 to `n` (inclusive).",
        'starter_code': "def sucet_do(n):\n    vysledok = 0\n    # doplň cyklus\n    return vysledok\n",
        'solution_code': "def sucet_do(n):\n    return sum(range(1, n + 1))\n",
        'tests': ["assert sucet_do(5) == 15", "assert sucet_do(1) == 1", "assert sucet_do(100) == 5050"],
        'hint_sk': "Použi `for i in range(1, n + 1):` a pripočítavaj `i`.", 'hint_en': "Use `for i in range(1, n + 1):` and keep adding `i`.",
    },
    {
        'keywords': ['funkc', 'rekurz', 'function', 'recurs'],
        'title_sk': 'Faktoriál rekurziou', 'title_en': 'Recursive Factorial',
        'instructions_sk': "Napíš **rekurzívnu** funkciu `faktorial(n)`, ktorá vráti `n!` (pričom `0! = 1`).",
        'instructions_en': "Write a **recursive** function `faktorial(n)` that returns `n!` (where `0! = 1`).",
        'starter_code': "def faktorial(n):\n    pass\n",
        'solution_code': "def faktorial(n):\n    return 1 if n <= 1 else n * faktorial(n - 1)\n",
        'tests': ["assert faktorial(0) == 1", "assert faktorial(5) == 120", "assert faktorial(7) == 5040"],
        'hint_sk': "Základný prípad: pre `n <= 1` vráť 1. Inak vráť `n * faktorial(n - 1)`.", 'hint_en': "Base case: return 1 for `n <= 1`. Otherwise return `n * faktorial(n - 1)`.",
    },
    {
        'keywords': ['zoznam', 'list', 'pole', 'array'],
        'title_sk': 'Najväčší prvok zoznamu', 'title_en': 'Largest List Item',
        'instructions_sk': "Napíš funkciu `najvacsi(cisla)`, ktorá **bez použitia** `max()` vráti najväčšie číslo zo zoznamu.",
        'instructions_en': "Write a function `najvacsi(cisla)` that returns the largest number in the list **without using** `max()`.",
        'starter_code': "def najvacsi(cisla):\n    pass\n",
        'solution_code': "def najvacsi(cisla):\n    m = cisla[0]\n    for c in cisla:\n        if c > m:\n            m = c\n    return m\n",
        'tests': ["assert najvacsi([3, 9, 2]) == 9", "assert najvacsi([-5, -1, -9]) == -1", "assert najvacsi([4]) == 4"],
        'hint_sk': "Ulož si prvý prvok ako doterajšie maximum a porovnávaj s ním ostatné.", 'hint_en': "Store the first item as the current maximum and compare the rest with it.",
    },
    {
        'keywords': ['slovník', 'slovnik', 'dict', 'kľúč'],
        'title_sk': 'Počítadlo písmen', 'title_en': 'Letter Counter',
        'instructions_sk': "Napíš funkciu `pocet_pismen(text)`, ktorá vráti slovník, kde kľúčom je znak a hodnotou počet jeho výskytov v texte.",
        'instructions_en': "Write a function `pocet_pismen(text)` that returns a dictionary mapping each character to the number of its occurrences.",
        'starter_code': "def pocet_pismen(text):\n    vysledok = {}\n    return vysledok\n",
        'solution_code': "def pocet_pismen(text):\n    d = {}\n    for z in text:\n        d[z] = d.get(z, 0) + 1\n    return d\n",
        'tests': ["assert pocet_pismen('aab') == {'a': 2, 'b': 1}", "assert pocet_pismen('') == {}"],
        'hint_sk': "Použi `d[z] = d.get(z, 0) + 1`.", 'hint_en': "Use `d[z] = d.get(z, 0) + 1`.",
    },
    {
        'keywords': ['oop', 'trieda', 'objekt', 'class', 'object'],
        'title_sk': 'Trieda Pes', 'title_en': 'Dog Class',
        'instructions_sk': "Vytvor triedu `Pes` s atribútom `meno` (nastaveným v `__init__`) a metódou `zaštekaj()`, ktorá vráti text `'<meno>: Haf!'`.",
        'instructions_en': "Create a class `Pes` with a `meno` attribute (set in `__init__`) and a method `zaštekaj()` returning `'<meno>: Haf!'`.",
        'starter_code': "class Pes:\n    def __init__(self, meno):\n        pass\n",
        'solution_code': "class Pes:\n    def __init__(self, meno):\n        self.meno = meno\n\n    def zaštekaj(self):\n        return f'{self.meno}: Haf!'\n",
        'tests': ["assert Pes('Rex').zaštekaj() == 'Rex: Haf!'", "assert Pes('Bobik').meno == 'Bobik'"],
        'hint_sk': "V `__init__` ulož `self.meno = meno`.", 'hint_en': "Store `self.meno = meno` in `__init__`.",
    },
]


def generate_exercise_with_ai(topic, difficulty='EASY'):
    """
    Vygeneruje návrh nového cvičenia (SK + EN, štartovací kód, riešenie, assert testy).
    Pri dostupnom API kľúči použije Gemini, inak vyberie najvhodnejšiu úlohu z lokálnej banky.
    Vráti slovník s kľúčom `source` = 'gemini' | 'fallback'.
    """
    prompt = (
        "Vytvor jedno krátke programátorské cvičenie v jazyku Python pre stredoškolákov.\n"
        f"Téma: {topic}\nObtiažnosť: {difficulty}\n"
        "Úloha musí byť riešiteľná napísaním funkcie (alebo triedy) a overiteľná príkazmi assert.\n"
        "Vráť IBA JSON objekt s kľúčmi: title_sk, title_en, instructions_sk, instructions_en (Markdown), "
        "starter_code, solution_code, tests (pole 3 reťazcov typu 'assert f(x) == y'), hint_sk, hint_en."
    )
    raw = call_gemini(prompt, timeout=15, json_mode=True)
    if raw:
        try:
            data = json.loads(raw)
            required = {'title_sk', 'title_en', 'instructions_sk', 'instructions_en', 'starter_code', 'solution_code', 'tests'}
            if required.issubset(data.keys()) and isinstance(data['tests'], list):
                data['source'] = 'gemini'
                return data
        except (ValueError, TypeError):
            pass

    topic_l = (topic or '').lower()
    matches = [ex for ex in FALLBACK_EXERCISE_BANK if any(k in topic_l for k in ex['keywords'])]
    chosen = dict(random.choice(matches or FALLBACK_EXERCISE_BANK))
    chosen.pop('keywords', None)
    chosen['source'] = 'fallback'
    return chosen


# ----------------------------------------------------------------------
# 5. AI PREKLADAČ SK -> EN
# ----------------------------------------------------------------------
SK_EN_GLOSSARY = [
    (r'\bNapíš funkciu\b', 'Write a function'), (r'\bnapíš funkciu\b', 'write a function'),
    (r'\bVytvor triedu\b', 'Create a class'), (r'\bktorá vráti\b', 'that returns'),
    (r'\bktorá prijme\b', 'that takes'), (r'\bvráti\b', 'returns'), (r'\bvráť\b', 'return'),
    (r'\bzoznam\b', 'list'), (r'\bzoznamu\b', 'list'), (r'\bslovník\b', 'dictionary'),
    (r'\bčíslo\b', 'number'), (r'\bčísla\b', 'numbers'), (r'\bčísel\b', 'numbers'),
    (r'\btext\b', 'text'), (r'\bpočet\b', 'count'), (r'\bsúčet\b', 'sum'),
    (r'\bak\b', 'if'), (r'\binak\b', 'otherwise'), (r'\ba\b', 'and'), (r'\balebo\b', 'or'),
    (r'\bpomocou cyklu\b', 'using a loop'), (r'\bcyklus\b', 'loop'), (r'\bpodmienka\b', 'condition'),
    (r'\bpremenná\b', 'variable'), (r'\bparameter\b', 'parameter'), (r'\bvýsledok\b', 'result'),
    (r'\bNápoveda\b', 'Hint'), (r'\bPoužij\b', 'Use'), (r'\bpoužij\b', 'use'),
    (r'\bpárne\b', 'even'), (r'\bnepárne\b', 'odd'), (r'\bnajväčší\b', 'largest'), (r'\bnajmenší\b', 'smallest'),
]


def translate_to_english(fields):
    """
    Preloží slovník textových polí (napr. title, instructions, hint) zo slovenčiny do angličtiny.
    Kód v `backtickoch` a Markdown formátovanie zostávajú zachované.
    """
    clean = {k: v for k, v in fields.items() if v}
    if not clean:
        return {'source': 'none'}
    prompt = (
        "Translate the values of this JSON object from Slovak to natural English for a programming course. "
        "Keep Markdown formatting, Python identifiers and everything inside `backticks` unchanged. "
        "Return ONLY a JSON object with the same keys.\n\n" + json.dumps(clean, ensure_ascii=False)
    )
    raw = call_gemini(prompt, timeout=12, json_mode=True)
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                data['source'] = 'gemini'
                return data
        except (ValueError, TypeError):
            pass

    result = {}
    for key, text in clean.items():
        parts = re.split(r'(`[^`]*`)', text)  # nechaj kód v backtickoch bez zmeny
        out = []
        for part in parts:
            if part.startswith('`'):
                out.append(part)
                continue
            for pattern, repl in SK_EN_GLOSSARY:
                part = re.sub(pattern, repl, part)
            out.append(part)
        result[key] = ''.join(out)
    result['source'] = 'fallback'
    return result