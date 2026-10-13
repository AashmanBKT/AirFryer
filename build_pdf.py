# -*- coding: utf-8 -*-
"""
Generate publication-quality HTML specifically designed for PDF rendering,
then call headless Chrome to produce The_Ultimate_Air_Fryer_Cookbook.pdf.
"""

import os
import base64
import subprocess
from data_builder.intro_faq import INTRO_SECTIONS
from data_builder.breakfast import BREAKFAST_RECIPES
from data_builder.snacks import SNACKS_RECIPES
from data_builder.mains import MAINS_RECIPES
from data_builder.sweets import SWEETS_RECIPES

def img_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
    return ""

def generate_pdf_html():
    print("Loading images for embedded PDF...")
    cover_b64 = img_to_base64("images/cover.jpg")
    breakfast_b64 = img_to_base64("images/breakfast.jpg")
    snacks_b64 = img_to_base64("images/snacks.jpg")
    mains_b64 = img_to_base64("images/mains.jpg")
    sweets_b64 = img_to_base64("images/sweets.jpg")

    print("Embedding all 100 dedicated recipe images into memory...")
    recipe_b64_map = {}
    for r_id in range(1, 101):
        r_path = f"images/recipes/recipe_{r_id}.jpg"
        if os.path.exists(r_path):
            recipe_b64_map[r_id] = img_to_base64(r_path)
    print(f"Loaded {len(recipe_b64_map)}/100 dedicated recipe images as base64.")

    sections = [
        {
            "name": "Breakfast",
            "icon": "🌅",
            "desc": "Crispy morning cutlets, savory cheelas, spiced idli bites, and blistered parathas prepared with minimal oil.",
            "hero_img": breakfast_b64,
            "recipes": BREAKFAST_RECIPES
        },
        {
            "name": "Snacks & Starters",
            "icon": "🥟",
            "desc": "Street-side favorites reimagined: shatteringly crisp samosas, charred paneer tikka, bhindi chips, and golden fritters.",
            "hero_img": snacks_b64,
            "recipes": SNACKS_RECIPES
        },
        {
            "name": "Main Course",
            "icon": "🍛",
            "desc": "Wholesome, satisfying centerpieces: stuffed bell peppers, whole tandoori gobi, fragrant dum biryani, and rich koftas.",
            "hero_img": mains_b64,
            "recipes": MAINS_RECIPES
        },
        {
            "name": "Sweet Treats",
            "icon": "🍯",
            "desc": "Festive sweets and tea-time delicacies: whole wheat gujiyas, banana chips, cardamom modaks, and jaggery cookies.",
            "hero_img": sweets_b64,
            "recipes": SWEETS_RECIPES
        }
    ]

    html = []
    html.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Ultimate Air Fryer Indian Cookbook</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap');

  @page {
    size: A4 portrait;
    margin: 12mm 14mm 14mm 14mm;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.45;
    font-size: 9.5pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* FRONT COVER */
  .cover-page {
    page-break-after: always;
    height: 100vh;
    min-height: 275mm;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24mm 16mm 20mm;
    background: linear-gradient(135deg, #18120c 0%, #2b1f14 100%);
    color: #ffffff;
    box-sizing: border-box;
    text-align: center;
  }
  .cover-bg {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    opacity: 0.35;
    background-size: cover;
    background-position: center;
    z-index: 1;
  }
  .cover-content {
    position: relative;
    z-index: 2;
  }
  .cover-badge {
    display: inline-block;
    padding: 6px 18px;
    border: 1.5px solid #fdba74;
    border-radius: 999px;
    color: #fed7aa;
    font-size: 9pt;
    font-weight: 800;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 25px;
    background: rgba(0,0,0,0.4);
  }
  .cover-title {
    font-family: 'Playfair Display', serif;
    font-size: 34pt;
    font-weight: 800;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 15px;
    text-shadow: 0 4px 12px rgba(0,0,0,0.8);
  }
  .cover-title span {
    color: #f97316;
  }
  .cover-subtitle {
    font-size: 13pt;
    color: #ffedd5;
    max-width: 500px;
    margin: 0 auto 30px;
    line-height: 1.4;
  }
  .cover-highlights {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 15px;
  }
  .cover-stat {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 8px 16px;
    border-radius: 10px;
  }
  .cover-stat-val { font-size: 14pt; font-weight: 800; color: #fdba74; }
  .cover-stat-lbl { font-size: 7pt; text-transform: uppercase; color: #cbd5e1; letter-spacing: 0.05em; }
  .cover-footer {
    position: relative;
    z-index: 2;
    font-size: 8.5pt;
    color: #94a3b8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* INTRO & SCIENCE PAGES */
  .doc-page {
    page-break-after: always;
    min-height: 265mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .page-header-ribbon {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #ea580c;
    padding-bottom: 6px;
    margin-bottom: 14px;
    font-size: 8pt;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
  }
  .doc-title {
    font-family: 'Playfair Display', serif;
    font-size: 22pt;
    color: #0f172a;
    margin-bottom: 12px;
  }
  .doc-title span { color: #ea580c; }
  .doc-lead {
    font-size: 10.5pt;
    line-height: 1.55;
    color: #334155;
    margin-bottom: 16px;
  }
  .feature-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }
  .feature-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
  }
  .feature-card-title {
    font-size: 10pt;
    font-weight: 700;
    color: #c2410c;
    margin-bottom: 4px;
  }
  .feature-card-desc {
    font-size: 8.5pt;
    color: #475569;
    line-height: 1.4;
  }
  .rule-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 16px;
  }
  .rule-item {
    display: flex;
    gap: 10px;
    background: #fff7ed;
    border-left: 3.5px solid #ea580c;
    padding: 8px 12px;
    border-radius: 0 8px 8px 0;
  }
  .rule-item-title { font-weight: 700; color: #9a3412; font-size: 9pt; }
  .rule-item-desc { color: #7c2d12; font-size: 8.5pt; }

  /* TABLE OF CONTENTS */
  .toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 20px;
  }
  .toc-section-title {
    font-family: 'Playfair Display', serif;
    font-size: 11.5pt;
    color: #c2410c;
    border-bottom: 1.5px solid #fdba74;
    padding-bottom: 3px;
    margin: 10px 0 6px;
    font-weight: 700;
  }
  .toc-item {
    display: flex;
    justify-content: space-between;
    font-size: 8pt;
    padding: 2.5px 0;
    border-bottom: 1px dotted #cbd5e1;
  }
  .toc-item-name { font-weight: 600; color: #1e293b; }
  .toc-item-meta { color: #64748b; font-weight: 500; font-size: 7.5pt; }

  /* SECTION DIVIDER PAGE */
  .section-divider-page {
    page-break-after: always;
    min-height: 265mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
  }
  .section-hero-box {
    position: relative;
    height: 120mm;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 16px;
    background: #0f172a;
  }
  .section-hero-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  .section-hero-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(15,23,42,0.9) 0%, transparent 100%);
    padding: 20px 24px;
    color: #ffffff;
  }
  .section-divider-title {
    font-family: 'Playfair Display', serif;
    font-size: 24pt;
    color: #ffffff;
    font-weight: 800;
  }
  .section-divider-desc {
    color: #e2e8f0;
    font-size: 10pt;
    max-width: 600px;
    line-height: 1.4;
    margin-top: 6px;
  }
  .section-tips-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
  }
  .section-tips-title {
    font-weight: 700;
    color: #c2410c;
    margin-bottom: 8px;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* INDIVIDUAL RECIPE PAGE */
  .recipe-page {
    page-break-after: always;
    min-height: 265mm;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .recipe-header {
    margin-bottom: 8px;
  }
  .recipe-top-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .recipe-num-badge {
    background: #c2410c;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .recipe-category-label {
    font-size: 8pt;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
  }
  .recipe-title {
    font-family: 'Playfair Display', serif;
    font-size: 17pt;
    color: #0f172a;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 3px;
  }
  .recipe-blurb {
    font-size: 8.5pt;
    color: #475569;
    font-style: italic;
    line-height: 1.35;
    margin-bottom: 8px;
  }

  /* STATS RIBBON */
  .stats-ribbon {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 10px;
    text-align: center;
  }
  .stat-item {
    border-right: 1px solid #e2e8f0;
  }
  .stat-item:last-child { border-right: none; }
  .stat-item-val {
    font-weight: 800;
    font-size: 8.5pt;
    color: #0f172a;
  }
  .stat-item-lbl {
    font-size: 6.5pt;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
  }
  .stat-highlight {
    color: #c2410c;
  }

  /* RECIPE PHOTO */
  .recipe-photo-box {
    height: 52mm;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 10px;
    background: #1e293b;
  }
  .recipe-photo-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* TWO-COLUMN CONTENT */
  .recipe-body-grid {
    display: grid;
    grid-template-columns: 41% 57%;
    gap: 14px;
    flex-grow: 1;
  }
  .col-heading {
    font-family: 'Playfair Display', serif;
    font-size: 10pt;
    color: #0f172a;
    border-bottom: 1.5px solid #ea580c;
    padding-bottom: 2px;
    margin-bottom: 6px;
    font-weight: 700;
  }
  .ingredients-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 8px;
  }
  .ingredients-list li {
    font-size: 7.8pt;
    line-height: 1.35;
    color: #334155;
    position: relative;
    padding-left: 10px;
  }
  .ingredients-list li::before {
    content: "•";
    color: #ea580c;
    font-weight: bold;
    position: absolute;
    left: 0;
  }
  .pairing-box-mini {
    background: #f0fdf4;
    border-left: 3px solid #16a34a;
    padding: 5px 8px;
    border-radius: 0 6px 6px 0;
    font-size: 7.5pt;
    color: #14532d;
    line-height: 1.3;
    margin-top: 6px;
  }
  .pairing-box-mini strong { color: #166534; }

  .instructions-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 8px;
  }
  .instruction-step {
    display: flex;
    gap: 8px;
    font-size: 7.8pt;
    line-height: 1.35;
    color: #334155;
  }
  .step-index {
    width: 16px;
    height: 16px;
    background: #ffedd5;
    color: #9a3412;
    border-radius: 50%;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 7pt;
    margin-top: 1px;
  }
  .chef-secret-box {
    background: #eff6ff;
    border-left: 3px solid #2563eb;
    padding: 6px 10px;
    border-radius: 0 6px 6px 0;
    font-size: 7.5pt;
    color: #1e3a8a;
    line-height: 1.35;
    margin-top: 4px;
  }
  .chef-secret-box strong { color: #1d4ed8; }

  /* PAGE FOOTER */
  .page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 4px;
    font-size: 7pt;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 6px;
  }
</style>
</head>
<body>
""")

    # 1. FRONT COVER
    html.append(f"""
<div class="cover-page">
  <div class="cover-bg" style="background-image: url('{cover_b64}');"></div>
  <div class="cover-content">
    <div class="cover-badge">⚡ 100% Rapid Air Convection Mastery</div>
    <h1 class="cover-title">The Ultimate<br><span>Air Fryer</span><br>Indian Cookbook</h1>
    <p class="cover-subtitle">100 Authentic, Wholesome & Shatteringly Crisp Recipes Engineered Specifically for Your Air Fryer</p>
    
    <div class="cover-highlights">
      <div class="cover-stat">
        <div class="cover-stat-val">100</div>
        <div class="cover-stat-lbl">Master Recipes</div>
      </div>
      <div class="cover-stat">
        <div class="cover-stat-val">85%</div>
        <div class="cover-stat-lbl">Less Fat & Oil</div>
      </div>
      <div class="cover-stat">
        <div class="cover-stat-val">4</div>
        <div class="cover-stat-lbl">Complete Courses</div>
      </div>
      <div class="cover-stat">
        <div class="cover-stat-val">360°</div>
        <div class="cover-stat-lbl">Air Convection</div>
      </div>
    </div>
  </div>

  <div class="cover-footer">
    A Complete Culinary Reference Guide • Temperature & Timing Optimized
  </div>
</div>
""")

    # 2. WELCOME & SCIENCE OF CRISP
    html.append("""
<div class="doc-page">
  <div>
    <div class="page-header-ribbon">
      <span>The Ultimate Air Fryer Indian Cookbook</span>
      <span>Culinary Science & Introduction</span>
    </div>

    <h2 class="doc-title">Welcome to the <span>Air Fryer Kitchen</span></h2>
    <p class="doc-lead">
      Welcome to the definitive collection of 100 recipes engineered from the ground up for air fryer mastery. 
      Whether you crave nostalgic street-side samosas, sizzling tandoori skewers, fluffy breakfast cutlets, 
      or guilt-free festive sweets—this book provides exact temperatures, minute-by-minute milestones, 
      and tested oil-brush techniques for authentic, restaurant-grade results.
    </p>

    <h2 class="doc-title" style="font-size: 16pt; margin-top: 15px;">Why Air Fryer Cooking Is <span>Healthier</span></h2>
    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-card-title">Up to 80-85% Less Dietary Fat</div>
        <div class="feature-card-desc">Submerging food into boiling oil causes porous batters to absorb excess lipids. A micro-mist of oil (under 1 teaspoon across an entire batch) triggers the identical Maillard reaction with 85% fewer calories.</div>
      </div>
      <div class="feature-card">
        <div class="feature-card-title">Acrylamide Mitigation</div>
        <div class="feature-card-desc">Erratic stovetop frying temperatures can cause excessive acrylamide formation on starchy root vegetables. The air fryer maintains precise thermodynamic thresholds to prevent scorching.</div>
      </div>
      <div class="feature-card">
        <div class="feature-card-title">Nutrient & Vitamin Retention</div>
        <div class="feature-card-desc">Water-soluble vitamins (Vitamin C and B-complex in peppers, okra, and spinach) degrade during prolonged shallow frying or boiling. Rapid dry convection seals phytonutrients in half the cook time.</div>
      </div>
      <div class="feature-card">
        <div class="feature-card-title">Light & Effortless Digestion</div>
        <div class="feature-card-desc">Heavy deep-fried snacks leave a feeling of lethargy. Air-fried snacks preserve the pure, vibrant aromas of spices (cumin, ajwain, chaat masala, kasuri methi) while leaving you feeling energized.</div>
      </div>
    </div>

    <h2 class="doc-title" style="font-size: 16pt; margin-top: 10px;">The <span>7 Golden Rules</span> for Maximum Crisp</h2>
    <div class="rule-list">
      <div class="rule-item">
        <div>
          <div class="rule-item-title">1. Always Preheat (3 to 4 Minutes)</div>
          <div class="rule-item-desc">A hot basket immediately sets the exterior crust, sealing moisture inside before it can soften the exterior.</div>
        </div>
      </div>
      <div class="rule-item">
        <div>
          <div class="rule-item-title">2. Never Crowd the Basket (Respect Cyclonic Airflow)</div>
          <div class="rule-item-desc">Keep 0.5 inches (1.5 cm) clearance between cutlets and samosas. Cook in two fast batches rather than one soggy batch.</div>
        </div>
      </div>
      <div class="rule-item">
        <div>
          <div class="rule-item-title">3. The 5-Minute Oil Brush Rule</div>
          <div class="rule-item-desc">Don't drench food upfront. Brush or mist with oil at the midpoint flip to blister the crust with under 1 teaspoon total oil.</div>
        </div>
      </div>
      <div class="rule-item">
        <div>
          <div class="rule-item-title">4. Bone-Dry Surfaces Crisp Best</div>
          <div class="rule-item-desc">Pat paneer, tofu, and parboiled potatoes completely dry with paper towels. Excess water creates steam instead of crispiness.</div>
        </div>
      </div>
      <div class="rule-item">
        <div>
          <div class="rule-item-title">5. The Rice Flour / Cornstarch Shield</div>
          <div class="rule-item-desc">Dredge pakoras, cutlets, and bhindi in 1 tablespoon of rice flour or fine cornstarch for a shatteringly crisp micro-crust.</div>
        </div>
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>The Ultimate Air Fryer Indian Cookbook</span>
    <span>Introduction & Principles</span>
  </div>
</div>
""")

    # 3. TABLE OF CONTENTS
    html.append("""
<div class="doc-page">
  <div>
    <div class="page-header-ribbon">
      <span>The Ultimate Air Fryer Indian Cookbook</span>
      <span>Master Table of Contents (100 Recipes)</span>
    </div>

    <h2 class="doc-title">Table of <span>Contents</span></h2>
    <div class="toc-grid">
      <div>
        <div class="toc-section-title">🌅 Section 1: Breakfast (Recipes 1–20)</div>
""")
    for r in BREAKFAST_RECIPES:
        html.append(f"""
        <div class="toc-item">
          <span class="toc-item-name">{r['toc_number']}. {r['title']}</span>
          <span class="toc-item-meta">{r['temp_c']}°C • {r['cook_time']}</span>
        </div>
""")
    html.append("""
        <div class="toc-section-title" style="margin-top: 14px;">🍯 Section 4: Sweet Treats (Recipes 85–100)</div>
""")
    for r in SWEETS_RECIPES:
        html.append(f"""
        <div class="toc-item">
          <span class="toc-item-name">{r['toc_number']}. {r['title']}</span>
          <span class="toc-item-meta">{r['temp_c']}°C • {r['cook_time']}</span>
        </div>
""")
    html.append("""
      </div>
      <div>
        <div class="toc-section-title">🥟 Section 2: Snacks & Starters (Part 1, #1–20)</div>
""")
    for r in SNACKS_RECIPES[:20]:
        html.append(f"""
        <div class="toc-item">
          <span class="toc-item-name">{r['toc_number']}. {r['title']}</span>
          <span class="toc-item-meta">{r['temp_c']}°C • {r['cook_time']}</span>
        </div>
""")
    html.append("""
        <div class="toc-section-title" style="margin-top: 14px;">🥟 Snacks & Starters (Part 2, #21–40)</div>
""")
    for r in SNACKS_RECIPES[20:]:
        html.append(f"""
        <div class="toc-item">
          <span class="toc-item-name">{r['toc_number']}. {r['title']}</span>
          <span class="toc-item-meta">{r['temp_c']}°C • {r['cook_time']}</span>
        </div>
""")
    html.append("""
        <div class="toc-section-title" style="margin-top: 14px;">🍛 Section 3: Main Course (Recipes 61–84)</div>
""")
    for r in MAINS_RECIPES:
        html.append(f"""
        <div class="toc-item">
          <span class="toc-item-name">{r['toc_number']}. {r['title']}</span>
          <span class="toc-item-meta">{r['temp_c']}°C • {r['cook_time']}</span>
        </div>
""")
    html.append("""
      </div>
    </div>
  </div>

  <div class="page-footer">
    <span>The Ultimate Air Fryer Indian Cookbook</span>
    <span>Table of Contents</span>
  </div>
</div>
""")

    # 4. RECIPE SECTIONS & PAGES
    recipe_page_counter = 1
    for sec in sections:
        # Section Divider Page
        html.append(f"""
<div class="section-divider-page">
  <div>
    <div class="page-header-ribbon">
      <span>The Ultimate Air Fryer Indian Cookbook</span>
      <span>Course Opener</span>
    </div>

    <div class="section-hero-box">
      <img src="{sec['hero_img']}" class="section-hero-img" alt="{sec['name']}">
      <div class="section-hero-overlay">
        <div style="font-size: 11pt; text-transform: uppercase; color: #fdba74; font-weight: 800; letter-spacing: 0.1em; margin-bottom: 4px;">
          {sec['icon']} Section Collection
        </div>
        <h2 class="section-divider-title">{sec['name']}</h2>
        <p class="section-divider-desc">{sec['desc']}</p>
      </div>
    </div>

    <div class="section-tips-box">
      <div class="section-tips-title">💡 Chef's Guidelines for {sec['name']}</div>
      <p style="font-size: 8.5pt; color: #475569; line-height: 1.45;">
        Every recipe in this {sec['name']} collection includes precision temperature calibrations for both Celsius and Fahrenheit, 
        recommended basket arrangements, flipping milestones, and pairing suggestions. 
        Ensure you preheat the basket for at least 3 minutes before inserting chilled patties or pastries.
      </p>
    </div>
  </div>

  <div class="page-footer">
    <span>The Ultimate Air Fryer Indian Cookbook</span>
    <span>{sec['name']} Divider</span>
  </div>
</div>
""")

        # Individual Recipe Pages
        for r in sec['recipes']:
            img_src = recipe_b64_map.get(r['id'])
            if not img_src:
                hero_map = {
                    "breakfast": breakfast_b64,
                    "snacks": snacks_b64,
                    "mains": mains_b64,
                    "sweets": sweets_b64
                }
                img_src = hero_map.get(r['category'], cover_b64)

            html.append(f"""
<div class="recipe-page">
  <div>
    <!-- Header -->
    <div class="recipe-header">
      <div class="recipe-top-meta">
        <span class="recipe-num-badge">Recipe #{r['toc_number']}</span>
        <span class="recipe-category-label">{r['category_name']} • {', '.join(r['tags'][:2])}</span>
      </div>
      <h2 class="recipe-title">{r['title']}</h2>
      <p class="recipe-blurb">{r['description']}</p>
    </div>

    <!-- Quick Stats Ribbon -->
    <div class="stats-ribbon">
      <div class="stat-item">
        <div class="stat-item-val stat-highlight">{r['temp_c']}°C / {r['temp_f']}°F</div>
        <div class="stat-item-lbl">Air Fryer Temp</div>
      </div>
      <div class="stat-item">
        <div class="stat-item-val">{r['cook_time']}</div>
        <div class="stat-item-lbl">Cook Time</div>
      </div>
      <div class="stat-item">
        <div class="stat-item-val">{r['prep_time']}</div>
        <div class="stat-item-lbl">Prep Time</div>
      </div>
      <div class="stat-item">
        <div class="stat-item-val">{r['servings']}</div>
        <div class="stat-item-lbl">Servings</div>
      </div>
      <div class="stat-item">
        <div class="stat-item-val">{r['calories']}</div>
        <div class="stat-item-lbl">Calories</div>
      </div>
      <div class="stat-item">
        <div class="stat-item-val">P: {r['protein']} | C: {r['carbs']}</div>
        <div class="stat-item-lbl">Key Macros</div>
      </div>
    </div>

    <!-- Photo -->
    <div class="recipe-photo-box">
      <img src="{img_src}" class="recipe-photo-img" alt="{r['title']}">
    </div>

    <!-- Two-Column Recipe Details -->
    <div class="recipe-body-grid">
      <!-- Left Column: Ingredients & Pairing -->
      <div>
        <div class="col-heading">🛒 Ingredients</div>
        <ul class="ingredients-list">
""")
            for ing in r['ingredients']:
                html.append(f"          <li>{ing}</li>\n")

            html.append(f"""
        </ul>

        <div class="pairing-box-mini">
          <strong>🥢 Dip & Pairing:</strong> {r['dip_pairing']}
        </div>
      </div>

      <!-- Right Column: Instructions & Chef's Tip -->
      <div>
        <div class="col-heading">👩‍🍳 Step-by-Step Air Frying Method</div>
        <ul class="instructions-list">
""")
            for s_idx, s in enumerate(r['instructions'], 1):
                html.append(f"""
          <li class="instruction-step">
            <span class="step-index">{s_idx}</span>
            <div>{s}</div>
          </li>
""")

            html.append(f"""
        </ul>

        <div class="chef-secret-box">
          <strong>💡 Air Fryer Secret:</strong> {r['chef_tip']}
        </div>
      </div>
    </div>
  </div>

  <!-- Page Footer -->
  <div class="page-footer">
    <span>The Ultimate Air Fryer Indian Cookbook</span>
    <span>{r['category_name']} • Page {recipe_page_counter}</span>
  </div>
</div>
""")
            recipe_page_counter += 1

    # 5. FAQ & CONCLUDING PAGE
    html.append("""
<div class="doc-page">
  <div>
    <div class="page-header-ribbon">
      <span>The Ultimate Air Fryer Indian Cookbook</span>
      <span>Troubleshooting & Reference</span>
    </div>

    <h2 class="doc-title">Frequently Asked <span>Questions</span></h2>
    <div class="rule-list" style="margin-top: 10px;">
""")
    for item in INTRO_SECTIONS["faq"]:
        html.append(f"""
      <div class="rule-item" style="background: #f8fafc; border-left-color: #3b82f6;">
        <div>
          <div class="rule-item-title" style="color: #1e3a8a;">Q: {item['q']}</div>
          <div class="rule-item-desc" style="color: #334155; margin-top: 2px;">A: {item['a']}</div>
        </div>
      </div>
""")
    html.append("""
    </div>

    <h2 class="doc-title" style="font-size: 16pt; margin-top: 20px;">Master Quick <span>Conversion Table</span></h2>
    <div class="feature-grid" style="margin-top: 8px;">
      <div class="feature-card">
        <div class="feature-card-title">Conventional Oven to Air Fryer</div>
        <div class="feature-card-desc">Reduce temperature by 15°C to 20°C (25°F to 30°F) and reduce cook time by 20% to 25% due to compact cyclonic airflow.</div>
      </div>
      <div class="feature-card">
        <div class="feature-card-title">Deep Fry to Air Fryer</div>
        <div class="feature-card-desc">Lightly brush or spray with oil at minute 5 or at the midpoint flip. Avoid runny wet batter; use thick cling batter or perforated parchment.</div>
      </div>
    </div>

    <div style="text-align: center; margin-top: 30px; padding: 20px; background: #fff7ed; border-radius: 12px; border: 1px solid #fdba74;">
      <h3 style="font-family: 'Playfair Display', serif; font-size: 14pt; color: #9a3412; margin-bottom: 4px;">Happy Air Frying!</h3>
      <p style="font-size: 8.5pt; color: #7c2d12;">May every basket emerge golden, crisp, and filled with authentic flavor.</p>
    </div>
  </div>

  <div class="page-footer">
    <span>The Ultimate Air Fryer Indian Cookbook</span>
    <span>Reference & Appendix</span>
  </div>
</div>
</body>
</html>
""")

    output_html = "cookbook_pdf.html"
    with open(output_html, "w", encoding="utf-8") as f:
        f.write("".join(html))
    print(f"Successfully generated {output_html}")
    return output_html

def render_pdf():
    html_file = generate_pdf_html()
    abs_html = os.path.abspath(html_file)
    output_pdf = os.path.abspath("The_Ultimate_Air_Fryer_Cookbook.pdf")
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if not os.path.exists(chrome_path):
        chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        
    print(f"Rendering PDF using {chrome_path}...")
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf}",
        f"file:///{abs_html.replace(os.sep, '/')}"
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(output_pdf):
        size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
        print(f"SUCCESS! Rendered PDF at: {output_pdf} (Size: {size_mb:.2f} MB)")
    else:
        print(f"Failed to generate PDF. Subprocess returned {res.returncode}")
        print(f"Stderr: {res.stderr}")

if __name__ == "__main__":
    render_pdf()
