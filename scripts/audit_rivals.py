"""审计 aesthetic.rivals 字段，识别强凑/不合理的竞品搭配，并区分两类违规：
- BAD_REASON: 理由是"TGA 候选 / 销量榜邻位 / 同期发售"等纯外部并列，未谈玩法/审美/体验
- CROSS_GENRE_NO_REASON: 跨品类但理由也未补 IP / 题材 / 体验向的同源逻辑

输出：
- 每款游戏 rivals 详情
- 标注合理 / 可疑（reason 弱）/ 错误（理由完全外部并列）
"""
import json
import glob
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

games = json.load(open(DATA / "games.json", encoding="utf-8"))
by_id = {g["id"]: g for g in games}
by_slug = {g.get("slug"): g for g in games if g.get("slug")}

# 规则关键词
WEAK_REASON_PATTERNS = [
    r"TGA[^a-z]*(候选|获奖|提名|年度|竞争对手)",
    r"年度.*(候选|获奖|提名)",
    r"销量.*(榜|前\d+)",
    r"同期发售",
    r"同年发售",
    r"PS5\s*独占",  # 仅平台标签是弱依据
]
STRONG_REASON_KEYS = [
    "玩法", "战斗", "操作", "连招", "弹反", "撤离", "Roguelike", "roguelike",
    "题材", "世界观", "IP", "美学", "审美", "美术风格", "视觉",
    "体验", "情绪", "节奏", "硬核度", "难度",
    "对标", "同源", "继承", "致敬", "借鉴",
]


def reason_quality(reason):
    """返回 (level, why)
    level: STRONG / WEAK / EMPTY
    """
    if not reason:
        return "EMPTY", "理由为空"
    text = re.sub(r"<[^>]+>", "", reason)
    # 弱理由检测
    for p in WEAK_REASON_PATTERNS:
        if re.search(p, text):
            return "WEAK", f"匹配弱理由模式: {p}"
    # 强理由检测
    for kw in STRONG_REASON_KEYS:
        if kw in text:
            return "STRONG", f"含强关键词: {kw}"
    return "WEAK", "理由未提及玩法/审美/体验/题材等同源逻辑"


def main():
    issues = []
    total_games = 0
    total_rivals = 0
    weak_count = 0
    cross_weak_games = []

    for f in sorted(glob.glob(str(DATA / "games" / "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        slug = os.path.basename(f).replace(".json", "")
        rivals = d.get("aesthetic", {}).get("rivals", [])
        if not rivals:
            continue

        total_games += 1
        self_meta = by_slug.get(slug, {})
        self_genre = self_meta.get("genre", "")
        self_name = self_meta.get("nameCN") or self_meta.get("name") or slug

        flagged_rivals = []
        for r in rivals:
            total_rivals += 1
            rid = r.get("id")
            rmeta = by_id.get(rid, {}) if rid else {}
            rname = rmeta.get("nameCN") or rmeta.get("name") or r.get("name", "?")
            rgenre = rmeta.get("genre", "?")
            cross = bool(self_genre and rgenre and self_genre != rgenre)
            level, why = reason_quality(r.get("reason", ""))

            if level == "WEAK":
                weak_count += 1
                flagged_rivals.append({
                    "id": rid, "name": rname, "rgenre": rgenre,
                    "cross": cross, "level": level, "why": why,
                    "reason": r.get("reason", "")[:80],
                })

        if flagged_rivals:
            cross_weak_games.append((slug, self_name, self_genre, flagged_rivals))

    # 输出
    print(f"=== 全站 rivals 审计 ===")
    print(f"总游戏数: {total_games}, 总 rivals 数: {total_rivals}, 弱理由数: {weak_count}\n")

    print(f"=== {len(cross_weak_games)} 款游戏含弱理由 rivals ===\n")
    for slug, name, genre, flagged in cross_weak_games:
        print(f"[{slug}] {name} ({genre}):")
        for fr in flagged:
            tag = "⚠跨品类弱理由" if fr["cross"] else "⚠弱理由"
            print(f"  {tag} [id={fr['id']}] {fr['name']} ({fr['rgenre']})")
            print(f"    why: {fr['why']}")
            print(f"    reason: {fr['reason']}")
        print()


if __name__ == "__main__":
    main()
