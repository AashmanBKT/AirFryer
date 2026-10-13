# -*- coding: utf-8 -*-
"""
Combines Main Course Part 1 and Part 2 into MAINS_RECIPES (24 recipes total).
"""

from data_builder.mains_1 import MAINS_PART_1
from data_builder.mains_2 import MAINS_PART_2

MAINS_RECIPES = MAINS_PART_1 + MAINS_PART_2
