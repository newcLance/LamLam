#!/usr/bin/env python3
"""
Migrate old aesthetic (hook/book/look) to new structure (story + aesthetic 5-dims).

For each game JSON with old structure:
  1. Extract book + look world-building dims → story
  2. Generate placeholder aesthetic 5 dims (scene/costume/ui/symbol/promo)
     using content from old look dims as seeds
  3. Remove hook (redundant with playerExp)
  4. Keep rivals as-is

Usage: python scripts/migrate-aesthetic.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def migrate_game(slug):
    p = DATA / "games" / f"{slug}.json"
    if not p.exists():
        print(f"  [SKIP] {slug} - no data file")
        return False

    d = json.load(p.open("r", encoding="utf-8"))
    ae = d.get("aesthetic", {})

    # Check if already migrated
    if "scene" in ae or "story" in d:
        print(f"  [SKIP] {slug} - already migrated")
        return False

    # Check if old structure exists
    if "hook" not in ae and "book" not in ae:
        print(f"  [SKIP] {slug} - no old aesthetic data")
        return False

    hook = ae.get("hook", {})
    book = ae.get("book", {})
    look = ae.get("look", {})
    rivals = ae.get("rivals", [])

    # --- Build story ---
    story_dims = []

    # From book: time, place, character
    for dim in book.get("dims", []):
        story_dims.append({"label": dim["label"], "value": dim["value"]})

    # From look: tech level, factions, map, elements
    for dim in look.get("dims", []):
        story_dims.append({"label": dim["label"], "value": dim["value"]})

    story_title = book.get("title", "").replace("从故事出发", "").strip()
    if not story_title:
        story_title = "世界观与叙事"

    d["story"] = {
        "title": story_title,
        "dims": story_dims,
    }

    # --- Build new aesthetic (5 dims) ---
    # Extract seed content from old look dims for initial population
    look_dims = {dim["label"]: dim["value"] for dim in look.get("dims", [])}
    hook_dims = {dim["label"]: dim["value"] for dim in hook.get("dims", [])}

    # Generate placeholder content based on available data
    scene_seed = look_dims.get("地图", look_dims.get("元素", ""))
    costume_seed = look_dims.get("对抗关系", "")
    symbol_seed = look_dims.get("元素", "")

    new_ae = {
        "scene": {
            "title": "[待补充] 场景氛围",
            "value": f"[基于旧数据迁移，需人工优化] {scene_seed}" if scene_seed else "[待生成]",
        },
        "costume": {
            "title": "[待补充] 角色服装",
            "value": f"[基于旧数据迁移，需人工优化] {costume_seed}" if costume_seed else "[待生成]",
        },
        "ui": {
            "title": "[待补充] UI界面",
            "value": "[待生成] UI 风格尚未分析",
        },
        "symbol": {
            "title": "[待补充] 视觉符号",
            "value": f"[基于旧数据迁移，需人工优化] {symbol_seed}" if symbol_seed else "[待生成]",
        },
        "promo": {
            "title": "[待补充] 宣发风格",
            "value": "[待生成] 宣发风格尚未分析",
        },
        "rivals": rivals,
    }

    d["aesthetic"] = new_ae

    # Write back
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), "utf-8")
    print(f"  [OK] {slug} - migrated (story: {len(story_dims)} dims, aesthetic: 5 dims + {len(rivals)} rivals)")
    return True


def main():
    slugs = [
        "black-myth-wukong",
        "nioh-3",
        "sekiro-shadows-die-twice",
        "devil-may-cry-5",
        "wuchang-fallen-feathers",
    ]
    print("=== Migrating old aesthetic → new story + aesthetic ===\n")
    count = 0
    for slug in slugs:
        if migrate_game(slug):
            count += 1
    print(f"\nDone! Migrated {count} / {len(slugs)} games.")
    if count:
        print("NOTE: Aesthetic 5 dims contain placeholder content marked [待补充].")
        print("      These need to be properly generated with full content.")


if __name__ == "__main__":
    main()
