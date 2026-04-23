#!/usr/bin/env python3
"""
批量生成游戏详细数据 — Game Design Tracker v2
==============================================
为所有缺少数据的游戏生成 playerExp + story + aesthetic(5维度)

用法：
  python generate-all-data.py              # 生成所有缺失的
  python generate-all-data.py --status     # 只看状态，不生成
  python generate-all-data.py --slug xxx   # 只生成指定游戏

数据结构（v2）：
  - playerExp: media/community × memory/excitement/pain/churn + biliVideos
  - story: title + dims (时间/发生地/角色/科技水平/对抗关系/地图/元素)
  - aesthetic: scene/costume/ui/symbol/promo (各含 title+value) + rivals
"""

import json, sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"


def check_status():
    """Check which games need data generation."""
    games = json.loads((DATA / "games.json").read_text("utf-8"))

    complete = []     # has playerExp + story + aesthetic(5dims)
    need_aes = []     # has playerExp + story but aesthetic is placeholder
    need_story = []   # has playerExp but missing story
    need_all = []     # no data file at all

    for g in games:
        slug = g.get("slug", "")
        p = DATA / "games" / f"{slug}.json"
        if not p.exists():
            need_all.append(g)
            continue

        d = json.loads(p.read_text("utf-8"))
        has_pe = bool(d.get("playerExp"))
        has_st = bool(d.get("story"))
        ae = d.get("aesthetic", {})

        # Check if aesthetic has real content (not placeholders)
        has_real_ae = False
        if "scene" in ae:
            v = ae["scene"].get("value", "")
            has_real_ae = v and "[待" not in v and "[基于" not in v

        if has_pe and has_st and has_real_ae:
            complete.append(g)
        elif has_pe and has_st:
            need_aes.append(g)
        elif has_pe:
            need_story.append(g)
        else:
            need_all.append(g)

    return complete, need_aes, need_story, need_all


def print_status():
    complete, need_aes, need_story, need_all = check_status()
    total = len(complete) + len(need_aes) + len(need_story) + len(need_all)

    print(f"\n{'='*60}")
    print(f"Game Data Status Report ({total} games)")
    print(f"{'='*60}\n")

    print(f"COMPLETE ({len(complete)}):")
    for g in complete:
        print(f"  [OK] {g['slug']}")

    print(f"\nNEED AESTHETIC UPGRADE ({len(need_aes)}):")
    print(f"  (has playerExp + story, but aesthetic is placeholder)")
    for g in need_aes:
        print(f"  [AE] {g['slug']}")

    print(f"\nNEED STORY + AESTHETIC ({len(need_story)}):")
    for g in need_story:
        print(f"  [ST] {g['slug']}")

    print(f"\nNEED EVERYTHING ({len(need_all)}):")
    for g in need_all:
        print(f"  [--] {g['slug']}  ({g.get('nameCN', g['name'])})")

    print(f"\n{'='*60}")
    print(f"Summary: {len(complete)} complete, "
          f"{len(need_aes)} need aesthetic, "
          f"{len(need_story)} need story+aesthetic, "
          f"{len(need_all)} need everything")
    print(f"Total work remaining: {len(need_aes) + len(need_story) + len(need_all)} games")
    print(f"{'='*60}\n")

    return complete, need_aes, need_story, need_all


def main():
    if "--status" in sys.argv:
        print_status()
        return

    if "--slug" in sys.argv:
        idx = sys.argv.index("--slug")
        if idx + 1 < len(sys.argv):
            slug = sys.argv[idx + 1]
            print(f"Single game mode: {slug}")
            print(f"NOTE: This script only reports status.")
            print(f"      Actual data generation requires AI + web search.")
            print(f"      Use WorkBuddy to generate data for specific games.")
            return

    # Default: show status
    complete, need_aes, need_story, need_all = print_status()

    todo = len(need_aes) + len(need_story) + len(need_all)
    if todo == 0:
        print("All games have complete data!")
        return

    print(f"To generate data for these {todo} games:")
    print(f"  1. Ask the AI assistant to process them batch by batch")
    print(f"  2. Each game needs ~15 min of AI + web search work")
    print(f"  3. Estimated total: ~{todo * 15 // 60} hours")
    print(f"\nSuggested prompt:")
    print(f'  "Please generate full data (playerExp + story + aesthetic) ')
    print(f'   for the next 5 games that need it, following the pipeline ')
    print(f'   in docs/pipeline-new-game.md"')


if __name__ == "__main__":
    main()
