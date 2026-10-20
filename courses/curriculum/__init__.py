"""
Codoro Vzdelávacie Kurikulum Pythonu (18 modulov, 220+ hodín obsahu).
Tento balík obsahuje modulárne dáta pre kompletné kurikulum rozdelené do 5 kariérnych ciest.
"""

from .mod01_basics import MODULE_DATA as MOD01
from .mod02_operators_strings import MODULE_DATA as MOD02
from .mod03_conditions import MODULE_DATA as MOD03
from .mod04_loops import MODULE_DATA as MOD04
from .mod05_functions_recursion import MODULE_DATA as MOD05
from .mod06_lists_tuples import MODULE_DATA as MOD06
from .mod07_dicts_sets import MODULE_DATA as MOD07
from .mod08_exceptions_files import MODULE_DATA as MOD08
from .mod09_oop_basics import MODULE_DATA as MOD09
from .mod10_oop_advanced import MODULE_DATA as MOD10
from .mod11_algorithms import MODULE_DATA as MOD11
from .mod12_regex_validation import MODULE_DATA as MOD12
from .mod13_sql_databases import MODULE_DATA as MOD13
from .mod14_json_apis import MODULE_DATA as MOD14
from .mod15_testing_clean_code import MODULE_DATA as MOD15
from .mod16_cryptography import MODULE_DATA as MOD16
from .mod17_maturita_practical import MODULE_DATA as MOD17
from .mod18_graduation_projects import MODULE_DATA as MOD18

from .curriculum_enrichment import enrich_all_modules

ALL_CURRICULUM_MODULES = enrich_all_modules([
    MOD01,
    MOD02,
    MOD03,
    MOD04,
    MOD05,
    MOD06,
    MOD07,
    MOD08,
    MOD09,
    MOD10,
    MOD11,
    MOD12,
    MOD13,
    MOD14,
    MOD15,
    MOD16,
    MOD17,
    MOD18,
])
