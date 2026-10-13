# -*- coding: utf-8 -*-
"""
Update all recipe image references to their dedicated images/recipes/recipe_{id}.jpg,
regenerate recipes-data.js, COOKBOOK.md, and rebuild the master PDF.
"""

import os
import subprocess
from data_builder.intro_faq import INTRO_SECTIONS
from data_builder.breakfast import BREAKFAST_RECIPES
from data_builder.snacks import SNACKS_RECIPES
from data_builder.mains import MAINS_RECIPES
from data_builder.sweets import SWEETS_RECIPES

def main():
    all_recipes = BREAKFAST_RECIPES + SNACKS_RECIPES + MAINS_RECIPES + SWEETS_RECIPES
    print(f"Assigning dedicated image path to all {len(all_recipes)} recipes...")
    
    for r in all_recipes:
        r_id = r["id"]
        r["image"] = f"images/recipes/recipe_{r_id}.jpg"

    # Re-save build_all
    import build_all
    build_all.main()
    print("Regenerated recipes-data.js and COOKBOOK.md with dedicated recipe images.")

    # Now rebuild PDF using dedicated recipe images
    import build_pdf
    build_pdf.render_pdf()
    print("Rebuilt The_Ultimate_Air_Fryer_Cookbook.pdf successfully!")

if __name__ == "__main__":
    main()
