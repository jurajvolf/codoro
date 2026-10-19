"""
Codoro Vzdelávacie Kurikulum Pythonu (12 modulov, 140+ hodín obsahu).
Tento balík obsahuje modulárne dáta pre kompletné kurikulum.
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
from .mod12_boss_projects import MODULE_DATA as MOD12

ALL_CURRICULUM_MODULES = [
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
]
