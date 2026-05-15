#!/usr/bin/env python3
"""
Game Design Tracker - Static Site Generator
Tech: Jinja2 + Tailwind CSS (CDN) + Alpine.js (CDN)
Usage: python build.py
"""
import json, shutil, os, sys, re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Add scripts/ to path for safe_json
sys.path.insert(0, str(Path(__file__).parent / "scripts"))
from safe_json import safe_load

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
DATA = ROOT / "data"
DIST = ROOT / "dist"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
SCREENSHOTS_SRC = ROOT.parent / "game-platform-analysis" / "screenshots"


def load(path):
    text = path.read_text("utf-8")
    return safe_load(text, source=path.name)


def load_game_detail(slug):
    p = DATA / "games" / f"{slug}.json"
    return load(p) if p.exists() else {}


def slugify(text):
    """Convert name to URL-safe slug."""
    s = text.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)      # remove non-word chars except -
    s = re.sub(r'[\s_]+', '-', s)        # spaces/underscores → hyphens
    s = re.sub(r'-+', '-', s).strip('-') # collapse multiple hyphens
    return s or 'unnamed'


def main():
    print("=== Building Game Design Tracker (v2) ===")

    # Clean
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # Load data
    products = load(DATA / "products.json")
    games = load(DATA / "games.json")
    screenshots = load(DATA / "screenshots.json")

    # Add slug to products (platforms)
    for p in products:
        if not p.get("slug"):
            p["slug"] = slugify(p["name"])

    # Enrich games with detail data
    games_by_id = {}
    for g in games:
        detail = load_game_detail(g.get("slug", ""))
        if detail:
            g["playerExp"] = detail.get("playerExp")
            g["aesthetic"] = detail.get("aesthetic")
            g["story"] = detail.get("story")
            g["worldview"] = detail.get("worldview")
            g["assets"] = detail.get("assets")
        games_by_id[g["id"]] = g

    # Jinja2 setup
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=False)

    # Global template context
    total_ss = sum(
        sum(len(s.get("imgs", [])) for s in m.get("screens", []))
        for entry in screenshots.values() for m in entry
    )
    ctx = dict(
        products=products,
        games=games,
        games_by_id=games_by_id,
        screenshots=screenshots,
        total_screenshots=total_ss,
        total_products=len(products) + len(games),
        survey_url="https://wj.qq.com/s2/26428392/849b/",
    )

    # 1. Index
    html = env.get_template("pages/index.html").render(**ctx)
    (DIST / "index.html").write_text(html, "utf-8")
    print(f"  [OK] index.html")

    # 2. Game detail pages
    detail_tpl = env.get_template("pages/detail.html")
    gdir = DIST / "game"
    gdir.mkdir()
    for g in games:
        slug = g.get("slug", "")
        if not slug:
            continue
        ss = screenshots.get(g["name"], [])
        # Find first screenshot image for hero banner background
        hero_bg = ""
        for _m in ss:
            for _s in _m.get("screens", []):
                if _s.get("imgs"):
                    hero_bg = _s["imgs"][0]
                    break
            if hero_bg:
                break
        # Find first screenshot URL for "Visit Website" button
        first_url = ""
        for _m in ss:
            for _s in _m.get("screens", []):
                if _s.get("url"):
                    first_url = _s["url"]
                    break
            if first_url:
                break
        html = detail_tpl.render(game=g, ss=ss, hero_bg=hero_bg, site_url=first_url, **ctx)
        (gdir / f"{slug}.html").write_text(html, "utf-8")
    print(f"  [OK] {len(games)} detail pages")

    # 2b. Platform detail pages (reuse detail template)
    pcount = 0
    for p in products:
        slug = p.get("slug", "")
        if not slug:
            continue
        ss = screenshots.get(p["name"], [])
        hero_bg = ""
        for _m in ss:
            for _s in _m.get("screens", []):
                if _s.get("imgs"):
                    hero_bg = _s["imgs"][0]
                    break
            if hero_bg:
                break
        first_url = ""
        for _m in ss:
            for _s in _m.get("screens", []):
                if _s.get("url"):
                    first_url = _s["url"]
                    break
            if first_url:
                break
        html = detail_tpl.render(game=p, ss=ss, hero_bg=hero_bg, site_url=first_url, **ctx)
        (gdir / f"{slug}.html").write_text(html, "utf-8")
        pcount += 1
    print(f"  [OK] {pcount} platform detail pages")

    # 3. Compare page (client-side rendering)
    html = env.get_template("pages/compare.html").render(**ctx)
    (DIST / "compare.html").write_text(html, "utf-8")
    print(f"  [OK] compare.html")

    # 4. Static assets
    if STATIC.exists():
        shutil.copytree(STATIC, DIST / "static", dirs_exist_ok=True)
    print(f"  [OK] static/")

    # 5. Screenshots
    if SCREENSHOTS_SRC.exists():
        shutil.copytree(str(SCREENSHOTS_SRC), str(DIST / "screenshots"), dirs_exist_ok=True)
        n = sum(1 for _ in (DIST / "screenshots").rglob("*") if _.is_file())
        print(f"  [OK] screenshots/ ({n} images)")

    # 6. Client data JSON (for compare page)
    ddir = DIST / "data"
    ddir.mkdir()
    # Full game data with aesthetic for comparison
    (ddir / "games-full.json").write_text(
        json.dumps(games, ensure_ascii=False), "utf-8"
    )
    (ddir / "screenshots.json").write_text(
        json.dumps(screenshots, ensure_ascii=False), "utf-8"
    )
    print(f"  [OK] data/")

    size = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    print(f"\n=== Done! dist/ = {size/1024/1024:.1f} MB ===")


if __name__ == "__main__":
    main()
