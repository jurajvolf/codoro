"""
Codoro — Databázový router a manažér simulovanej demo databázy.
Umožňuje 100% bezpečnú izoláciu prednastavených demo účtov (student, ucitel, martin_k)
od produkčnej databázy s reálnymi žiakmi a učiteľmi.
"""
import contextvars
import os
import shutil
from pathlib import Path
from django.conf import settings
from django.db import connections

# Thread-safe a async-safe kontextová premenná pre aktívnu databázu
_active_db = contextvars.ContextVar('active_db', default='default')

DEMO_USERNAMES = {'student', 'ucitel', 'martin_k'}


def set_active_db(db_name: str):
    """Nastaví aktívnu databázu pre aktuálny kontext požiadavky."""
    return _active_db.set(db_name)


def reset_active_db(token):
    """Obnoví predchádzajúci stav databázy podľa kontextového tokenu."""
    try:
        if token is not None:
            _active_db.reset(token)
    except Exception:
        pass


def get_active_db() -> str:
    """Vráti názov aktuálne aktívnej databázy ('default' alebo 'demo')."""
    return _active_db.get()


class DemoDatabaseRouter:
    """
    Dynamický databázový router Django:
    - Štandardné požiadavky bežných registrovaných používateľov smerujú do 'default'.
    - Požiadavky demo relácií (student, ucitel) smerujú do izolovanej databázy 'demo'.
    - Sessions a ContentTypes ostávajú v 'default' pre stabilnú správu HTTP cookies.
    """

    GLOBAL_APPS = {'sessions', 'contenttypes'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.GLOBAL_APPS:
            return 'default'
        return get_active_db()

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.GLOBAL_APPS:
            return 'default'
        return get_active_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True


def get_demo_db_path() -> Path:
    return Path(settings.DATABASES['demo']['NAME'])


def get_demo_template_path() -> Path:
    return Path(settings.BASE_DIR) / 'db_demo_template.sqlite3'


def ensure_demo_database():
    """Zabezpečí, že simulovaná databáza 'demo' existuje a je pripravená na použitie."""
    demo_path = get_demo_db_path()
    template_path = get_demo_template_path()

    if demo_path.exists() and demo_path.stat().st_size > 0:
        return

    # Ak existuje šablóna, skopírujeme ju
    if template_path.exists() and template_path.stat().st_size > 0:
        try:
            shutil.copyfile(template_path, demo_path)
            return
        except Exception:
            pass

    # Ak ešte neexistuje ani šablóna ani databáza, inicializujeme ju
    initialize_demo_database()


def initialize_demo_database():
    """Vytvorí novú simulovanú databázu 'demo', vykoná migrácie a naplní čisté demo kurikulum."""
    from django.core.management import call_command
    import seed_codoro

    demo_path = get_demo_db_path()
    template_path = get_demo_template_path()

    # Uzavrieme existujúce spojenie, ak existuje
    if 'demo' in connections:
        connections['demo'].close()

    # 1. Spustenie migrácií pre databázu 'demo'
    call_command('migrate', database='demo', interactive=False)

    # 2. Naplnenie dát do databázy 'demo'
    prev_token = set_active_db('demo')
    try:
        seed_codoro.run_seed()
    finally:
        reset_active_db(prev_token)

    # Uzavrieme spojenie pred kopírovaním súboru
    if 'demo' in connections:
        connections['demo'].close()

    # 3. Vytvorenie zálohy / šablóny pre bleskový reset
    try:
        if demo_path.exists():
            shutil.copyfile(demo_path, template_path)
    except Exception:
        pass


def reset_demo_database():
    """Resetuje simulovanú databázu 'demo' do čistého počiatočného stavu."""
    demo_path = get_demo_db_path()
    template_path = get_demo_template_path()

    if 'demo' in connections:
        connections['demo'].close()

    if template_path.exists() and template_path.stat().st_size > 0:
        try:
            shutil.copyfile(template_path, demo_path)
            return True
        except Exception:
            pass

    # Fallback re-inicializácia
    initialize_demo_database()
    return True
