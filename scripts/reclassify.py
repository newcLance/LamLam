#!/usr/bin/env python3
"""Reclassify all games and platforms for balanced distribution."""
import json, sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================
# GAME genre remap: slug -> new genre
# Target: 7 categories, each ~8-10 games (total 61)
# ============================================================
GAME_REMAP = {
    # === Shooter 射击 (11) ===
    "doom-the-dark-ages": "Shooter",
    "s-t-a-l-k-e-r-2-heart-of-chornobyl": "Shooter",
    "atomfall": "Shooter",
    "call-of-duty-modern-warfare-ii-2022": "Shooter",
    "counter-strike-2": "Shooter",
    "call-of-duty-modern-warfare-iii-2023": "Shooter",
    "call-of-duty-black-ops-6": "Shooter",
    "delta-force": "Shooter",
    "killing-floor-3": "Shooter",
    "helldivers-2": "Shooter",
    "avatar-frontiers-of-pandora": "Shooter",

    # === Action 动作 (10) ===
    "sekiro-shadows-die-twice": "Action",
    "devil-may-cry-5": "Action",
    "god-of-war": "Action",
    "stellar-blade": "Action",
    "hollow-knight-silksong": "Action",
    "hi-fi-rush": "Action",
    "marvels-spider-man-remastered": "Action",
    "vampire-survivors": "Action",
    "astro-bot": "Action",
    "pizza-tower": "Action",

    # === Action RPG 动作角色扮演 (10) ===
    "black-myth-wukong": "Action RPG",
    "elden-ring-shadow-of-the-erdtree": "Action RPG",
    "nioh-3": "Action RPG",
    "phantom-blade-zero": "Action RPG",
    "wuchang-fallen-feathers": "Action RPG",
    "where-winds-meet": "Action RPG",
    "hades-2": "Action RPG",
    "cult-of-the-lamb": "Action RPG",
    "hogwarts-legacy": "Action RPG",
    "atomic-heart": "Action RPG",

    # === RPG 角色扮演 (9) ===
    "final-fantasy-vii-rebirth": "RPG",
    "metaphor-refantazio": "RPG",
    "clair-obscur-expedition-33": "RPG",
    "baldurs-gate-3": "RPG",
    "persona-5-royal": "RPG",
    "kingdom-come-deliverance-2": "RPG",
    "cyberpunk-2077": "RPG",
    "the-outer-worlds-2": "RPG",
    "resident-evil-village": "RPG",

    # === Adventure 冒险叙事 (10) ===
    "death-stranding-2-on-the-beach": "Adventure",
    "ghost-of-yotei": "Adventure",
    "ghost-of-tsushima": "Adventure",
    "indiana-jones-and-the-great-circle": "Adventure",
    "silent-hill-2": "Adventure",
    "signalis": "Adventure",
    "split-fiction": "Adventure",
    "stray": "Adventure",
    "days-gone": "Adventure",
    "dredge": "Adventure",

    # === Survival 生存探索 (5) ===
    "dying-light-the-beast": "Survival",
    "metroid-prime-4-beyond": "Survival",
    "high-on-life-2": "Survival",
    "lethal-company": "Survival",
    "dave-the-diver": "Survival",

    # === Simulation 模拟策略 (6) ===
    "satisfactory": "Simulation",
    "teardown": "Simulation",
    "dyson-sphere-program": "Simulation",
    "the-planet-crafter": "Simulation",
    "balatro": "Simulation",
    "inscryption": "Simulation",
}

# ============================================================
# PLATFORM category remap: name -> new category
# Only 3 categories: PC平台 / 移动平台 / 游戏厂商官网
# ============================================================
PLATFORM_REMAP = {
    # PC 平台
    "Steam": "PC平台",
    "Epic Games Store": "PC平台",
    "GOG": "PC平台",
    "WeGame": "PC平台",
    "Xbox / Microsoft Store": "PC平台",
    "Nintendo eShop": "PC平台",
    "PlayStation Store": "PC平台",
    "Steam Deck / 掌机生态": "PC平台",
    "NVIDIA GeForce NOW": "PC平台",
    "Xbox Cloud Gaming": "PC平台",
    # 移动平台
    "TapTap": "移动平台",
    "好游快爆": "移动平台",
    "Google Play Games": "移动平台",
    "Apple Arcade": "移动平台",
    # 游戏厂商官网
    "Discord": "游戏厂商官网",
    "米哈游 HoYoverse": "游戏厂商官网",
}


def main():
    # Load games
    games_path = DATA / "games.json"
    games = json.loads(games_path.read_text("utf-8"))

    # Reclassify games
    unmapped = []
    changes = 0
    for g in games:
        slug = g.get("slug", "")
        if slug in GAME_REMAP:
            old = g["genre"]
            new = GAME_REMAP[slug]
            if old != new:
                g["genre"] = new
                changes += 1
        else:
            unmapped.append(f'{slug} ({g.get("nameCN", "?")})')

    # Save games
    games_path.write_text(json.dumps(games, ensure_ascii=False, indent=2), "utf-8")

    # Print new game distribution
    c = Counter(g["genre"] for g in games)
    print("=== NEW GAME GENRE DISTRIBUTION ===")
    for k, v in c.most_common():
        names = [g["nameCN"] for g in games if g["genre"] == k]
        print(f"  {k:15s} ({v:2d}): {', '.join(names)}")
    print(f"\n  Total: {len(games)} games, {changes} changed")
    if unmapped:
        print(f"  WARNING unmapped: {unmapped}")

    # Load products
    prod_path = DATA / "products.json"
    products = json.loads(prod_path.read_text("utf-8"))

    # Reclassify platforms
    pchanges = 0
    for p in products:
        name = p.get("name", "")
        if name in PLATFORM_REMAP:
            old = p.get("category", "")
            new = PLATFORM_REMAP[name]
            if old != new:
                p["category"] = new
                pchanges += 1

    # Save products
    prod_path.write_text(json.dumps(products, ensure_ascii=False, indent=2), "utf-8")

    # Print new platform distribution
    c2 = Counter(p["category"] for p in products)
    print("\n=== NEW PLATFORM CATEGORY DISTRIBUTION ===")
    for k, v in c2.most_common():
        names = [p["nameCN"] for p in products if p["category"] == k]
        print(f"  {k:12s} ({v:2d}): {', '.join(names)}")
    print(f"\n  Total: {len(products)} platforms, {pchanges} changed")


if __name__ == "__main__":
    main()
