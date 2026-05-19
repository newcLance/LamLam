"""全站游戏模块完整性审计：检查每款游戏的 worldview / story / aesthetic / playerExp / assets 字段，
找出"少模块"或"有数据但没显示"的情况。

输出维度：
- 每款游戏的字段命中：worldview/story/aesthetic.summary/aesthetic.rivals/playerExp.biliVideos/assets
- 区分 stub（不需要这些数据）和 visible（需要）
- 标出缺失字段
"""
import json
import glob
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

games_idx = json.load(open(DATA / "games.json", encoding="utf-8"))
by_slug = {g.get("slug"): g for g in games_idx if g.get("slug")}


def audit(slug, d):
    """检查每个模块，返回 (visible_status, issues)"""
    meta = by_slug.get(slug, {})
    is_stub = meta.get("stub", False)
    if is_stub:
        return "STUB", []

    issues = []

    # worldview: 应有 background/mainStory/combat/coreLoop 4 项
    wv = d.get("worldview") or {}
    wv_keys = ["background", "mainStory", "combat", "coreLoop"]
    missing_wv = [k for k in wv_keys if not wv.get(k)]
    if missing_wv:
        issues.append(f"worldview 缺: {missing_wv}")

    # story: 应有 overview + dims
    story = d.get("story") or {}
    if not story.get("overview"):
        issues.append("story.overview 缺")
    if not story.get("dims") or len(story.get("dims") or []) < 5:
        issues.append(f"story.dims 不足 (有 {len(story.get('dims') or [])} 条)")

    # aesthetic: summary + rivals + 五维卡片(scene/costume/ui/symbol/promo)
    ae = d.get("aesthetic") or {}
    if not ae.get("summary"):
        issues.append("aesthetic.summary 缺")
    if not ae.get("rivals"):
        issues.append("aesthetic.rivals 缺/空")
    five_cards = ["scene", "costume", "ui", "symbol", "promo"]
    missing_cards = [k for k in five_cards if not ae.get(k)]
    if missing_cards:
        issues.append(f"aesthetic 五维卡片缺: {missing_cards}")

    # playerExp: 应有 media + community 各 4 子字段（memory/excitement/pain/churn） + biliVideos
    pe = d.get("playerExp") or {}
    if not pe:
        issues.append("playerExp 整个缺")
    else:
        for top in ("media", "community"):
            sub = pe.get(top) or {}
            if not sub:
                issues.append(f"playerExp.{top} 整个缺")
                continue
            for field in ("memory", "excitement", "pain", "churn"):
                if not sub.get(field) or len(sub.get(field) or []) == 0:
                    issues.append(f"playerExp.{top}.{field} 缺/空")
        if not pe.get("biliVideos"):
            issues.append("playerExp.biliVideos 缺")

    # assets: 应有 official/inspiration
    assets = d.get("assets") or {}
    if not assets:
        issues.append("assets 整个缺")

    return ("OK" if not issues else "PARTIAL"), issues


def main():
    json_files = sorted(glob.glob(str(DATA / "games" / "*.json")))
    stats = {"STUB": 0, "OK": 0, "PARTIAL": 0}
    partials = []

    for f in json_files:
        slug = os.path.basename(f).replace(".json", "")
        d = json.load(open(f, encoding="utf-8"))
        status, issues = audit(slug, d)
        stats[status] = stats.get(status, 0) + 1

        if status == "PARTIAL":
            partials.append((slug, issues))

    print(f"=== 全站模块完整性审计 ===")
    print(f"总游戏文件: {len(json_files)}")
    print(f"  STUB (无需数据): {stats.get('STUB', 0)}")
    print(f"  OK (全字段齐全): {stats.get('OK', 0)}")
    print(f"  PARTIAL (有缺): {stats.get('PARTIAL', 0)}\n")

    if partials:
        print("=== PARTIAL 游戏列表 ===\n")
        for slug, issues in partials:
            print(f"[{slug}]")
            for issue in issues:
                print(f"  - {issue}")
            print()


if __name__ == "__main__":
    main()
