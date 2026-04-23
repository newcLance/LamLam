#!/usr/bin/env python3
"""
心愿单自动处理脚本 — Game Design Tracker
==========================================
功能：
  1. 读取腾讯问卷导出的心愿单数据（CSV 或 XLSX）
  2. 与 data/games.json 比对，筛出尚未收录的游戏
  3. 对新游戏执行 Phase 1 立项审核（自动）
  4. 输出待接入清单，供后续管线继续执行

用法：
  python scripts/process-wishlist.py wishlist.csv
  python scripts/process-wishlist.py wishlist.xlsx
  python scripts/process-wishlist.py --demo   # 用示例数据演示流程

数据源：
  腾讯问卷导出文件，预期列：
    - 列1: 提交时间
    - 列2: 游戏名称（中文或英文）
    - 列3: 花名/昵称（可选）
    - 列4: 推荐理由（可选）

输出：
  打印待接入游戏清单 + 写入 data/wishlist-pending.json
"""

import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GAMES_JSON = DATA / "games.json"


def load_games():
    """Load existing games and build a set of known names/aliases."""
    games = json.loads(GAMES_JSON.read_text("utf-8"))
    known = set()
    for g in games:
        known.add(g["name"].lower())
        if g.get("nameCN"):
            known.add(g["nameCN"].lower())
        if g.get("alias"):
            for a in g["alias"].split("/"):
                known.add(a.strip().lower())
    return games, known


def read_csv(path):
    """Read wishlist from CSV export."""
    entries = []
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 2 and row[1].strip():
                entries.append({
                    "submit_time": row[0].strip() if row[0] else "",
                    "game_name": row[1].strip(),
                    "nickname": row[2].strip() if len(row) > 2 else "",
                    "reason": row[3].strip() if len(row) > 3 else "",
                })
    return entries


def read_xlsx(path):
    """Read wishlist from XLSX export (requires openpyxl)."""
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl not installed. Run: pip install openpyxl")
        print("  Or export as CSV from the survey dashboard.")
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb.active
    entries = []
    first = True
    for row in ws.iter_rows(values_only=True):
        if first:
            first = False
            continue  # skip header
        if len(row) >= 2 and row[1]:
            entries.append({
                "submit_time": str(row[0] or ""),
                "game_name": str(row[1]).strip(),
                "nickname": str(row[2] or "").strip() if len(row) > 2 else "",
                "reason": str(row[3] or "").strip() if len(row) > 3 else "",
            })
    return entries


def demo_entries():
    """Demo data for testing."""
    return [
        {"submit_time": "2026-05-05", "game_name": "Hollow Knight: Silksong", "nickname": "test", "reason": "indie masterpiece"},
        {"submit_time": "2026-05-05", "game_name": "Black Myth: Wukong", "nickname": "test", "reason": "already exists"},
        {"submit_time": "2026-05-05", "game_name": "Onimusha: Way of the Sword", "nickname": "test", "reason": "new samurai game"},
    ]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    # Load existing games
    games, known = load_games()
    print(f"Database: {len(games)} games, {len(known)} known names/aliases\n")

    # Read wishlist
    arg = sys.argv[1]
    if arg == "--demo":
        entries = demo_entries()
        print("[DEMO MODE]\n")
    elif arg.endswith(".xlsx"):
        entries = read_xlsx(arg)
    else:
        entries = read_csv(arg)

    print(f"Wishlist entries: {len(entries)}\n")

    # Filter new games
    new_games = []
    seen = set()
    for e in entries:
        name_lower = e["game_name"].lower()
        if name_lower in known or name_lower in seen:
            print(f"  [SKIP] {e['game_name']} (already in database)")
            continue
        seen.add(name_lower)
        new_games.append(e)
        print(f"  [NEW]  {e['game_name']} -- {e.get('reason', '')}")

    print(f"\n{'=' * 50}")
    print(f"New games to process: {len(new_games)}")

    if not new_games:
        print("Nothing to do!")
        return

    # Write pending list
    pending_path = DATA / "wishlist-pending.json"
    pending_data = {
        "generated": str(Path(arg).name) if arg != "--demo" else "demo",
        "count": len(new_games),
        "games": new_games,
    }
    pending_path.write_text(json.dumps(pending_data, ensure_ascii=False, indent=2), "utf-8")
    print(f"\nPending list saved to: {pending_path}")
    print(f"\nNext steps:")
    print(f"  1. Review the pending list")
    print(f"  2. For each game, run the full pipeline (Phase 1-6)")
    print(f"  3. Or use: python generate-all-data.py --from-wishlist")


if __name__ == "__main__":
    main()
