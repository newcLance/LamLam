#!/usr/bin/env python3
"""
回填全站已有游戏的 UI 界面链接 - 换成新的 gameui/iig 优先方案。
2026-07-02 用户新需求:UI 界面链接优先给 gameui.net + interfaceingame.com

用法:
  python scripts/backfill_ui_links.py --dry-run       # 只打印,不写
  python scripts/backfill_ui_links.py                 # 实际写回
  python scripts/backfill_ui_links.py --slug xxx      # 只处理某款
"""
import argparse, json, sys, time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
from assets_helper import build_ui_links

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def process(slug, dry_run=False, verbose=True):
    detail = BASE / "data" / "games" / f"{slug}.json"
    if not detail.exists():
        return "no-detail"
    games = json.load(open(BASE / "data" / "games.json", encoding="utf-8"))
    meta = next((g for g in games if g["slug"] == slug), None)
    if not meta:
        return "no-meta"
    name_cn = meta.get("nameCN", "")
    name_en = meta.get("name", "")
    if not name_en:
        return "no-en-name"

    d = json.load(open(detail, encoding="utf-8"))
    assets = d.get("assets", {})
    if not assets:
        return "no-assets"
    insp = assets.get("inspiration", [])
    ui_grp = next((g for g in insp if g.get("cat", "").startswith("UI")), None)
    if ui_grp is None:
        return "no-ui-cat"

    new_links = build_ui_links(name_cn, name_en, try_iig_direct=True)
    old_srcs = [l.get("source", "") for l in ui_grp.get("links", [])]
    new_srcs = [l.get("source", "") for l in new_links]
    changed = old_srcs != new_srcs

    if verbose:
        hit = any(l.get("source") == "InterfaceInGame" and "InterfaceInGame" and "search?q=" not in l.get("url", "")
                  for l in new_links if l.get("source") == "InterfaceInGame")
        # 更严格：iig 首条 note 是否含"直链命中"
        iig_hit = any(l.get("source") == "InterfaceInGame" and "直链命中" in l.get("note", "")
                      for l in new_links)
        tag = "iig✓" if iig_hit else "iig~"
        print(f"  [{tag}] {slug}  {name_cn}  ({name_en})")

    if changed and not dry_run:
        ui_grp["links"] = new_links
        json.dump(d, open(detail, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return "written"
    return "unchanged" if not changed else "would-write"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", help="只处理某款")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.slug:
        r = process(args.slug, dry_run=args.dry_run)
        print(f"result: {r}")
        return

    all_details = sorted((BASE / "data" / "games").glob("*.json"))
    stats = {}
    print(f"[start] {len(all_details)} detail files, dry_run={args.dry_run}")
    for i, p in enumerate(all_details, 1):
        slug = p.stem
        r = process(slug, dry_run=args.dry_run, verbose=True)
        stats[r] = stats.get(r, 0) + 1
        time.sleep(0.35)  # 别把 iig 打爆
    print(f"\n[done] {stats}")


if __name__ == "__main__":
    main()
