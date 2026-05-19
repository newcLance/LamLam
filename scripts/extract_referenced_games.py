"""扫描所有游戏的 detail 资料和 report，提取被提到的"真实参考游戏"，
对照游戏库，生成"待立项游戏表"。

提取来源：
1. aesthetic.summary.references[].title （type=game 优先）
2. story.dims[].value 里的书名号《...》或英文专名
3. worldview.*.value 里的明显游戏名引用
4. static/report/{slug}*.html 里的游戏名（粗略）

输出：
- 待立项清单（被多个游戏引用、但站内没有的游戏，按引用次数排序）
- 每个引用的来源（哪款游戏的哪段提到的）
"""
import json
import glob
import os
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "static" / "report"

games = json.load(open(DATA / "games.json", encoding="utf-8"))
# 已立项游戏的中文/英文/别名 set，用于快速判断"是否已在站内"
existing_names = set()
for g in games:
    for k in ("name", "nameCN", "alias"):
        v = (g.get(k) or "").strip().lower()
        if v:
            existing_names.add(v)
            # 去括号
            cleaned = re.sub(r"\s*[\(（][^)]+[\)）]\s*", "", v).strip()
            if cleaned:
                existing_names.add(cleaned)

# 候选游戏池（中文）
referenced = defaultdict(list)  # name -> [(source_slug, source_kind, snippet)]


def add_ref(name, source_slug, kind, snippet):
    name = name.strip()
    if len(name) < 2:
        return
    name_lc = name.lower()
    # 已存在站内？
    if name_lc in existing_names:
        return
    # 去 cleaned 版本检查
    cleaned = re.sub(r"\s*[\(（][^)]+[\)）]\s*", "", name_lc).strip()
    if cleaned in existing_names:
        return
    referenced[name].append((source_slug, kind, snippet[:80]))


def extract_from_text(text, source_slug, kind):
    """从文本中提取书名号 / 英文专名"""
    if not text:
        return
    text = re.sub(r"<[^>]+>", "", text)  # 去 HTML
    # 1. 书名号《...》
    for m in re.findall(r"《([^》]{2,30})》", text):
        if not re.match(r"^[\d ]+$", m):
            add_ref(m, source_slug, kind, text)
    # 2. 英文专名（连续 2 个以上首字母大写单词，不含连接词）
    for m in re.findall(r"\b([A-Z][a-zA-Z']+(?:\s+(?:of\s+)?[A-Z][a-zA-Z']+){1,4})\b", text):
        if len(m) >= 6 and m.lower() not in {"call of duty", "rainbow six", "modern warfare"}:
            # 简单过滤：不包含明显非游戏词
            blocklist = ["The Studio", "Game Awards", "Game of", "The Player",
                          "Open World", "Action RPG", "JRPG", "PS Plus", "Steam Deck"]
            if not any(b in m for b in blocklist):
                add_ref(m, source_slug, kind, text)


def main():
    for f in sorted(glob.glob(str(DATA / "games" / "*.json"))):
        slug = os.path.basename(f).replace(".json", "")
        d = json.load(open(f, encoding="utf-8"))

        # 1. references
        refs = d.get("aesthetic", {}).get("summary", {}).get("references", [])
        for r in refs:
            if r.get("type") == "game":
                title = r.get("title", "")
                # 形如 "超级马里奥银河 Super Mario Galaxy"
                # 取第一段中文 + 第一段英文
                cn_m = re.match(r"([^\s]+)\s+([A-Za-z\s']+)", title)
                if cn_m:
                    add_ref(cn_m.group(1), slug, "ref-cn", title)
                    add_ref(cn_m.group(2).strip(), slug, "ref-en", title)
                else:
                    add_ref(title, slug, "ref", title)

        # 2. story.dims
        for dim in d.get("story", {}).get("dims", []):
            extract_from_text(dim.get("value", ""), slug, "story")

        # 3. worldview
        for k, v in d.get("worldview", {}).items():
            if isinstance(v, dict):
                extract_from_text(v.get("value", ""), slug, "worldview")

        # 4. report (HTML)
        for rpt in [REPORTS / f"{slug}.html", REPORTS / f"{slug}-alt.html",
                    REPORTS / f"{slug}-alt-d.html"]:
            if rpt.exists():
                text = rpt.read_text(encoding="utf-8")
                extract_from_text(text, slug, f"report:{rpt.name}")

    # 排序：被引用次数最多的优先
    sorted_refs = sorted(referenced.items(), key=lambda x: -len(x[1]))

    print(f"=== 待立项游戏候选（被引用 ≥ 2 次）===")
    print(f"总候选数: {len(sorted_refs)}\n")

    for name, sources in sorted_refs[:50]:
        if len(sources) >= 2:
            slugs = sorted(set(s[0] for s in sources))
            print(f"  [{len(sources):>3}x] {name:50s} ← {len(slugs)} 款游戏: {', '.join(slugs[:5])}{'...' if len(slugs)>5 else ''}")

    print(f"\n=== 单次引用候选（被某款游戏的 detail 资料里专门提到的，需人工判断）===")
    for name, sources in sorted_refs:
        if len(sources) == 1 and sources[0][1] in ("ref-cn", "ref-en"):
            print(f"  [{sources[0][0]:30s}] {name}")


if __name__ == "__main__":
    main()
