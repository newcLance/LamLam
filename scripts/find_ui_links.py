#!/usr/bin/env python3
"""
UI 界面素材链接查找器 (2026-07-02)

策略更新（2026-07-02 v2）：
用户反馈现有 ArtStation/Dribbble 搜索命中不准。改为优先使用两个专业站点：
- gameui.net (国内/手游 UI 数据库)
  - 只能用 /game/{id} 直链, ?s= 搜索会跳首页, sitemap 无法拿到
  - 自动定位 game id 不可靠 → 默认给"检索指引"链接 + 说明用法
- interfaceingame.com (国外单机 UI 数据库)
  - URL 结构 /games/games/{slug-lowercase-hyphen}/, 收录约 400 款
  - 按英文名规则化 slug 直连验证：命中→给直链；未命中→给 games 列表页 + Bing site: 兜底

用法:
  python scripts/find_ui_links.py --slug wuchang-fallen-feathers
  python scripts/find_ui_links.py --slug xxx --write
"""
import argparse, json, re, ssl, sys, urllib.parse, urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    resp = urllib.request.urlopen(req, timeout=timeout, context=CTX)
    return resp.getcode(), resp.geturl(), resp.read().decode("utf-8", errors="replace")


# ── interfaceingame.com ───────────────────────────────────────
def iig_slug_variants(name_en):
    """按 iig 规则生成候选 slug（lowercase, 空格/冒号转-, 保留字母数字）"""
    n = name_en.strip().lower()
    variants = []
    # v1: 冒号连字符全转空格, 去标点, 空格转 -
    v1 = re.sub(r"[:\-]", " ", n)
    v1 = re.sub(r"[^\w\s]", "", v1)
    v1 = re.sub(r"\s+", "-", v1.strip())
    variants.append(v1)
    # v2: 冒号后内容去掉
    if ":" in n:
        v2 = n.split(":")[0].strip()
        v2 = re.sub(r"[^\w\s]", "", v2)
        v2 = re.sub(r"\s+", "-", v2.strip())
        variants.append(v2)
    # v3: 全去符号连一起
    v3 = re.sub(r"[^\w]", "", n)
    if v3 and v3 not in variants:
        variants.append(v3)
    return [v for v in variants if v]


def find_interfaceingame(name_en):
    """返回 (最佳链接, 状态描述, is_direct_hit)
    v3 (2026-07-02): 直连命中优先精确直链; 未命中走 Google site: 搜索(用户偏好)。
    """
    if not name_en:
        return None, "无英文名", False
    for slug in iig_slug_variants(name_en):
        url = f"https://interfaceingame.com/games/games/{slug}/"
        try:
            code, final, _ = http_get(url, timeout=12)
            if code == 200 and slug in final.lower():
                return url, f"直连命中 ({slug})", True
        except Exception:
            continue
    q = urllib.parse.quote(f"site:interfaceingame.com {name_en}")
    return f"https://www.google.com/search?q={q}", "iig 未直连命中, 走 Google site: 搜索", False


# ── gameui.net ────────────────────────────────────────────────
def find_gameui(name_cn, name_en):
    """gameui 无稳定搜索/sitemap → 直接走 Google site:gameui.net。
    返回 (URL, 状态描述, is_direct_hit)"""
    query = name_cn or name_en or ""
    q = urllib.parse.quote(f"site:gameui.net {query}")
    return f"https://www.google.com/search?q={q}", "gameui 走 Google site: 搜索", False


# ── 主流程 ────────────────────────────────────────────────────
def build_ui_links(name_cn, name_en, verbose=True):
    """返回一组 UI 界面链接（顺序：直链命中优先 → 搜索兜底 → 通用兜底）"""
    links = []

    iig_url, iig_info, iig_hit = find_interfaceingame(name_en)
    if verbose:
        print(f"interfaceingame: {'✓ 直连' if iig_hit else '~ 搜索兜底'}  {iig_url}\n    {iig_info}")
    if iig_url:
        if iig_hit:
            links.append({
                "title": f"Interface In Game《{name_en}》UI 收录页",
                "source": "InterfaceInGame", "url": iig_url,
                "note": "国外单机 UI 数据库·直链命中"
            })
        else:
            links.append({
                "title": f"Google 搜索「site:interfaceingame.com {name_en}」",
                "source": "InterfaceInGame", "url": iig_url,
                "note": "国外单机 UI 数据库·未直接收录, Google site: 搜索兜底"
            })

    gu_url, gu_info, gu_hit = find_gameui(name_cn, name_en)
    query = name_cn or name_en or ""
    if verbose:
        print(f"gameui.net     : Google site: 搜索  {gu_url}\n    {gu_info}")
    if gu_url:
        links.append({
            "title": f"Google 搜索「site:gameui.net {query}」",
            "source": "GameUI.net", "url": gu_url,
            "note": f"国内/手游 UI 数据库·用 Google site: 定位「{query}」的 /game/{{id}} 直链"
        })

    # 传统兜底（保留原 ArtStation/Pinterest, 排在专业站点后面）
    if name_en:
        enc = urllib.parse.quote
        links.append({
            "title": f"ArtStation 搜索「{name_en} UI」",
            "source": "ArtStation",
            "url": f"https://www.artstation.com/search?sort_by=relevance&query={enc(name_en+' UI')}"
        })
        links.append({
            "title": f"Pinterest 搜索「{name_en} UI」",
            "source": "Pinterest",
            "url": f"https://www.pinterest.com/search/pins/?q={enc(name_en+' UI')}"
        })

    return links


def find_and_maybe_write(slug=None, name_en=None, name_cn=None, write=False):
    if slug and (not name_en or not name_cn):
        games = json.load(open(BASE / "data" / "games.json", encoding="utf-8"))
        found = next((g for g in games if g["slug"] == slug), None)
        if found:
            name_en = name_en or found.get("name", "")
            name_cn = name_cn or found.get("nameCN", "")

    print(f"\n=== {name_cn} / {name_en} (slug={slug}) ===")
    links = build_ui_links(name_cn, name_en)

    if write and slug:
        detail_path = BASE / "data" / "games" / f"{slug}.json"
        if not detail_path.exists():
            print(f"[SKIP write] {detail_path.name} 不存在")
            return
        d = json.load(open(detail_path, encoding="utf-8"))
        assets = d.get("assets", {})
        insp = assets.setdefault("inspiration", [])
        ui_grp = None
        for grp in insp:
            if grp.get("cat", "").startswith("UI"):
                ui_grp = grp
                break
        if ui_grp is None:
            ui_grp = {"cat": "UI 界面 / 纹理材质", "links": []}
            insp.append(ui_grp)
        ui_grp["links"] = links
        json.dump(d, open(detail_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[WRITE] {detail_path.name} UI 组已重写 ({len(links)} 条)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--slug", help="从 games.json 读英文名/中文名")
    p.add_argument("--name", dest="name_en", help="英文名")
    p.add_argument("--nameCN", dest="name_cn", help="中文名")
    p.add_argument("--write", action="store_true", help="写回 detail JSON")
    args = p.parse_args()
    if not (args.slug or args.name_en):
        p.print_help(); sys.exit(1)
    find_and_maybe_write(slug=args.slug, name_en=args.name_en, name_cn=args.name_cn, write=args.write)
