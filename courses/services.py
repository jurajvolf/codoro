import subprocess
import sys
import tempfile
import os
import json
import urllib.request
from django.conf import settings

FORBIDDEN_KEYWORDS = ['import os', 'import sys', 'import subprocess', 'import shutil', '__import__', 'open(', 'eval(', 'exec(']


def evaluate_python_code(exercise, student_code):
    """
    Bezpečne spustí študentský Python kód oproti všetkým TestCase prípadom danej úlohy.
    Vráti trojicu: (passed_all: bool, status_str: str, output_log: str)
    """
    for forbidden in FORBIDDEN_KEYWORDS:
        if forbidden in student_code:
            return (
                False,
                'ERROR',
                f"Bezpečnostná ochrana Codoro: Použitie príkazu '{forbidden}' nie je v cvičeniach povolené."
            )

    test_cases = exercise.test_cases.all()
    if not test_cases.exists():
        return True, 'PASSED', "Kód bol úspešne spustený (úloha nemá definované automatické testy)."

    results_log = []
    all_passed = True

    for index, tc in enumerate(test_cases, start=1):
        label = "Skrytý test" if tc.is_hidden else f"Test #{index} ({tc.input_data})"
        full_script = f"{student_code}\n\n# --- AUTOMATICKÝ TEST ---\n{tc.test_code}\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(full_script)
            tmp_path = tmp_file.name

        try:
            proc = subprocess.run(
                [sys.executable, tmp_path],
                capture_output=True,
                text=True,
                timeout=3
            )
            if proc.returncode == 0:
                results_log.append(f"✅ {label}: ÚSPEŠNÝ")
            else:
                all_passed = False
                err_msg = proc.stderr.strip().splitlines()[-1] if proc.stderr else "Nesprávny výsledok"
                results_log.append(f"❌ {label}: ZLYHAL -> {err_msg}")
                if "SyntaxError" in proc.stderr or "IndentationError" in proc.stderr or "NameError" in proc.stderr:
                    return False, 'ERROR', "\n".join(results_log) + f"\n\nDetail chyby:\n{proc.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return (
                False,
                'ERROR',
                "⏱️ Časový limit vypršal (Timeout > 3s)! Skontroluj, či tvoj kód neobsahuje nekonečný cyklus."
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    final_status = 'PASSED' if all_passed else 'FAILED'
    return all_passed, final_status, "\n".join(results_log)


def get_codo_ai_feedback(exercise, student_code, error_log, lang='sk'):
    """
    Sokratovský AI tútor Codo. Ak je nastavený GEMINI_API_KEY, zavolá Google Gemini 2.5 Flash.
    Ak kľúč nie je nastavený, poskytne lokálnu diagnostiku kódu, aby ukážka vždy fungovala.
    """
    api_key = os.environ.get('GEMINI_API_KEY', getattr(settings, 'GEMINI_API_KEY', ''))

    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            lang_instruction = "Odpovedaj v slovenčine." if lang == 'sk' else "Respond in English."
            prompt = (
                f"Si Codo, priateľský Sokratovský AI tútor na platforme Codoro. {lang_instruction} "
                f"NIKDY nenapíš študentovi hotové riešenie ani celý opravený kód! "
                f"Vysvetli mu v 2-3 vetách, kde urobil logickú alebo syntaktickú chybu a naveď ho otázkou.\n\n"
                f"Zadanie úlohy: {exercise.instructions_sk}\n"
                f"Kód študenta:\n{student_code}\n"
                f"Výstup testov:\n{error_log}"
            )
            payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=6) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            pass

    # Inteligentná lokálna Sokratovská analýza (funguje okamžite aj bez internetu a API kľúča)
    if lang == 'en':
        if 'pass' in student_code and 'return' not in student_code:
            return "🤖 Codo: I see you still have `pass` in your function and no `return` statement. What value should your function compute and send back?"
        if 'return' not in student_code:
            return "🤖 Codo: Your code calculates something, but it doesn't return the result! Try using the `return` keyword instead of `print()`."
        return f"🤖 Codo: Look closely at the test output: {error_log.splitlines()[-1]}. Check your math operators or condition boundaries (e.g., `>` vs `>=`)."
    else:
        if 'pass' in student_code and 'return' not in student_code:
            return "🤖 Codo: Vidím, že vo funkcii máš stále príkaz `pass` a chýba ti `return`. Aký výpočet má funkcia vykonať a vrátiť?"
        if 'return' not in student_code:
            return "🤖 Codo: Tvoja funkcia nevracia žiadnu hodnotu! Nezabudni, že automatické testy kontrolujú výsledok vrátený cez príkaz `return`, nie iba výpis cez `print()`."
        return f"🤖 Codo: Pozri sa na správu z testu: „{error_log.splitlines()[-1]}“. Skontroluj si znamienka vo výpočte alebo hraničnú podmienku (napr. či má byť `>=` namiesto `>`)."