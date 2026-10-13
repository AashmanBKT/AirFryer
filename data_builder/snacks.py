# -*- coding: utf-8 -*-
"""
Combines Snacks & Starters Part 1 and Part 2 into SNACKS_RECIPES (40 recipes total).
"""

from data_builder.snacks_1 import SNACKS_PART_1
from data_builder.snacks_2 import SNACKS_PART_2

SNACKS_RECIPES = SNACKS_PART_1 + SNACKS_PART_2
