# -*- coding: utf-8 -*-
"""
Build script to compile all recipes into recipes-data.js and COOKBOOK.md.
"""

import json
import os
from data_builder.intro_faq import INTRO_SECTIONS
from data_builder.breakfast import BREAKFAST_RECIPES
from data_builder.snacks import SNACKS_RECIPES
from data_builder.mains import MAINS_RECIPES
from data_builder.sweets import SWEETS_RECIPES

def main():
    all_recipes = BREAKFAST_RECIPES + SNACKS_RECIPES + MAINS_RECIPES + SWEETS_RECIPES
    print(f"Total recipes loaded: {len(all_recipes)}")
    # Assign dedicated image path for each of the 100 recipes
    for r in all_recipes:
        r["image"] = f"images/recipes/recipe_{r['id']}.jpg"

    # 1. Output recipes-data.js
    js_content = f"""// Auto-generated Air Fryer Cookbook Data
window.COOKBOOK_INTRO = {json.dumps(INTRO_SECTIONS, indent=2)};

window.COOKBOOK_RECIPES = {json.dumps(all_recipes, indent=2)};
"""
    with open("recipes-data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Successfully wrote recipes-data.js")

    # 2. Output COOKBOOK.md
    md_lines = []
    md_lines.append("# 🌟 The Ultimate Air Fryer Indian Cookbook")
    md_lines.append("### *100 Authentic, Wholesome & Crispy Air Fryer Recipes*")
    md_lines.append("\n---\n")
    md_lines.append("![Cookbook Cover](images/cover.jpg)\n")
    
    # Welcome
    md_lines.append("## 📖 Welcome\n")
    md_lines.append(INTRO_SECTIONS["welcome"]["content"] + "\n")
    
    # Why Air Fryer Is Healthier
    md_lines.append("## 🌿 Why Air Fryer Cooking Is Healthier\n")
    for pt in INTRO_SECTIONS["why_healthy"]["points"]:
        md_lines.append(f"### {pt['headline']}\n{pt['text']}\n")
    
    # Tips
    md_lines.append("## 💡 Air Fryer Tips for Best Results\n")
    for r in INTRO_SECTIONS["tips_best_results"]["rules"]:
        md_lines.append(f"### {r['title']}\n{r['desc']}\n")
    
    # Table of Contents
    md_lines.append("## 📑 Table of Contents\n")
    md_lines.append("### 🌅 Breakfast (Recipes 1–20)")
    for r in BREAKFAST_RECIPES:
        md_lines.append(f"- [{r['toc_number']}. {r['title']}](#recipe-{r['id']})")
    
    md_lines.append("\n### 🥟 Snacks & Starters (Recipes 21–60)")
    for r in SNACKS_RECIPES:
        md_lines.append(f"- [{r['toc_number']}. {r['title']}](#recipe-{r['id']})")
        
    md_lines.append("\n### 🍛 Main Course (Recipes 61–84)")
    for r in MAINS_RECIPES:
        md_lines.append(f"- [{r['toc_number']}. {r['title']}](#recipe-{r['id']})")
        
    md_lines.append("\n### 🍯 Sweet Treats (Recipes 85–100)")
    for r in SWEETS_RECIPES:
        md_lines.append(f"- [{r['toc_number']}. {r['title']}](#recipe-{r['id']})")

    md_lines.append("\n---\n")

    current_cat = ""
    for r in all_recipes:
        if r['category_name'] != current_cat:
            current_cat = r['category_name']
            hero_map = {
                "Breakfast": "images/breakfast.jpg",
                "Snacks & Starters": "images/snacks.jpg",
                "Main Course": "images/mains.jpg",
                "Sweet Treats": "images/sweets.jpg"
            }
            md_lines.append(f"\n# 🍽️ SECTION: {current_cat.upper()}\n")
            if current_cat in hero_map:
                md_lines.append(f"![{current_cat} Hero]({hero_map[current_cat]})\n")
        
        md_lines.append(f"<a id='recipe-{r['id']}'></a>")
        md_lines.append(f"## {r['toc_number']}. {r['title']}\n")
        md_lines.append(f"*{r['description']}*\n")
        
        if r.get('image'):
            md_lines.append(f"![{r['title']}]({r['image']})\n")
            
        md_lines.append(f"**⏱️ Prep Time:** {r['prep_time']} | **🔥 Cook Time:** {r['cook_time']} | **⌛ Total:** {r['total_time']}")
        md_lines.append(f"**🌡️ Air Fryer Temp:** {r['temp_c']}°C / {r['temp_f']}°F | **👥 Servings:** {r['servings']} | **📊 Calories:** {r['calories']}")
        md_lines.append(f"**Macros:** Protein: {r['protein']} | Carbs: {r['carbs']} | Fat: {r['fat']}")
        md_lines.append(f"**🏷️ Tags:** {', '.join(r['tags'])}\n")
        
        md_lines.append("### 🛒 Ingredients")
        for ing in r['ingredients']:
            md_lines.append(f"- {ing}")
            
        md_lines.append("\n### 👩‍🍳 Step-by-Step Air Fryer Instructions")
        for step_idx, step in enumerate(r['instructions'], 1):
            md_lines.append(f"{step_idx}. {step}")
            
        md_lines.append(f"\n> [!TIP]\n> **Chef's Air Fryer Secret:** {r['chef_tip']}\n")
        md_lines.append(f"**🥢 Serving & Pairing:** {r['dip_pairing']}\n")
        md_lines.append("\n---\n")

    # FAQ
    md_lines.append("## ❓ Frequently Asked Questions\n")
    for item in INTRO_SECTIONS["faq"]:
        md_lines.append(f"### Q: {item['q']}\n**A:** {item['a']}\n")
        
    md_lines.append("## 🙏 Thank You & Happy Air Frying!\n")
    md_lines.append("May your air fryer bring crispy joy, rich memories, and wholesome nourishment to your table every single day!")

    with open("COOKBOOK.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print("Successfully wrote COOKBOOK.md")

if __name__ == "__main__":
    main()
