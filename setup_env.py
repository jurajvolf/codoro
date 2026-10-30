"""
Codoro — Bezpečný inicializátor produkčnej konfigurácie a kryptografických kľúčov (.env)

Použitie:
    python setup_env.py
"""
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'
EXAMPLE_PATH = BASE_DIR / '.env.example'


def generate_env():
    print("=" * 72)
    print("CODORO — INICIALIZÁCIA A ROTÁCIA BEZPEČNOSTNÝCH KĽÚČOV (.env)")
    print("=" * 72)

    existing = {}
    if ENV_PATH.exists():
        print(f"[*] Nájdený existujúci súbor .env: {ENV_PATH}")
        for raw_line in ENV_PATH.read_text(encoding='utf-8').splitlines():
            line = raw_line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                existing[k.strip()] = v.strip().strip('"').strip("'")
    else:
        print("[+] Vytváram nový zabezpečený súbor .env...")

    # 1. DJANGO_SECRET_KEY: generovanie nového silného kľúča
    secret_key = existing.get('DJANGO_SECRET_KEY')
    is_compromised = (
        not secret_key
        or 'replace-with' in secret_key
        or 'codoro-production' in secret_key
        or 'django-insecure' in secret_key
    )
    if is_compromised:
        secret_key = secrets.token_urlsafe(50)
        existing['DJANGO_SECRET_KEY'] = secret_key
        print("[+] Vygenerovaný nový kryptografický DJANGO_SECRET_KEY (50 bajtov).")
    else:
        print("[i] DJANGO_SECRET_KEY je už bezpečne nakonfigurovaný.")

    # 2. GITHUB_WEBHOOK_SECRET: generovanie unikátneho webhook hesla
    webhook_secret = existing.get('GITHUB_WEBHOOK_SECRET')
    is_webhook_compromised = (
        not webhook_secret
        or 'codoro-maturita' in webhook_secret
        or len(webhook_secret) < 16
    )
    if is_webhook_compromised:
        webhook_secret = secrets.token_hex(24)
        existing['GITHUB_WEBHOOK_SECRET'] = webhook_secret
        print("[+] Vygenerovaný nový bezpečný GITHUB_WEBHOOK_SECRET (48 znakov hex).")
    else:
        print("[i] GITHUB_WEBHOOK_SECRET je už bezpečne nakonfigurovaný.")

    # 3. Predvolené produkčné nastavenia
    existing.setdefault('DJANGO_DEBUG', 'False')
    existing.setdefault(
        'DJANGO_ALLOWED_HOSTS',
        'codoro.sk,www.codoro.sk,codoro.eu.pythonanywhere.com,.pythonanywhere.com,localhost,127.0.0.1',
    )
    existing.setdefault(
        'DJANGO_CSRF_TRUSTED_ORIGINS',
        'https://codoro.sk,https://www.codoro.sk,https://codoro.eu.pythonanywhere.com,https://*.pythonanywhere.com',
    )

    env_content = f"""# ==============================================================================
# CODORO — BEZPEČNÁ PRODUKČNÁ KONFIGURÁCIA (.env)
# UPOZORNENIE: Tento súbor NIKDY necommitujte do Gitu (.gitignore ho chráni)!
# ==============================================================================

# 1. Základná Django bezpečnosť (šifrovanie cookies, relácií a CSRF)
DJANGO_SECRET_KEY={existing['DJANGO_SECRET_KEY']}
DJANGO_DEBUG={existing['DJANGO_DEBUG']}
DJANGO_ALLOWED_HOSTS={existing['DJANGO_ALLOWED_HOSTS']}
DJANGO_CSRF_TRUSTED_ORIGINS={existing['DJANGO_CSRF_TRUSTED_ORIGINS']}

# 2. GitHub Auto-Deploy Webhook overovací podpis (HMAC-SHA256)
GITHUB_WEBHOOK_SECRET={existing['GITHUB_WEBHOOK_SECRET']}

# 3. Sokratovský AI Tútor Codo (Google Gemini API)
GEMINI_API_KEY={existing.get('GEMINI_API_KEY', '')}
GEMINI_MODEL={existing.get('GEMINI_MODEL', 'gemini-2.5-flash')}
"""
    ENV_PATH.write_text(env_content, encoding='utf-8')
    print(f"\n[OK] Súbor .env bol úspešne zapísaný!")
    print("=" * 72)
    print("AKO DOKONČIŤ NASTAVENIE NA GITHUB A PYTHONANYWHERE:")
    print("=" * 72)
    print("1. GITHUB WEBHOOK (nastavenie v prehliadači):")
    print("   - Otvor: https://github.com/jurajvolf/codoro/settings/hooks")
    print("   - Klikni na Edit pri svojom webhooks")
    print(f"   - Do poľa 'Secret' vlož túto novú hodnotu:\n     {existing['GITHUB_WEBHOOK_SECRET']}")
    print("   - Ulož tlačidlom 'Update webhook'.")
    print("=" * 72)


if __name__ == '__main__':
    generate_env()
