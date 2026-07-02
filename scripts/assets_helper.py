# -*- coding: utf-8 -*-
"""
assets 素材链接生成器 (共享模块) —— 立项管线内容生产脚本统一 import 用。
2026-07-02: UI 界面优先给 GameUI.net + Interface In Game 两个专业站点。

用法:
    from scripts.assets_helper import build_assets_block
    d["assets"] = build_assets_block(name_cn, name_en, official_extra=[...])
"""
import re, ssl, urllib.parse, urllib.request

enc = urllib.parse.quote

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120"


def _iig_slug_variants(name_en):
    n = (name_en or "").strip().lower()
    vs = []
    v1 = re.sub(r"[:\-]", " ", n)
    v1 = re.sub(r"[^\w\s]", "", v1)
    v1 = re.sub(r"\s+", "-", v1.strip())
    if v1: vs.append(v1)
    if ":" in n:
        v2 = n.split(":")[0].strip()
        v2 = re.sub(r"[^\w\s]", "", v2)
        v2 = re.sub(r"\s+", "-", v2.strip())
        if v2 and v2 not in vs: vs.append(v2)
    v3 = re.sub(r"[^\w]", "", n)
    if v3 and v3 not in vs: vs.append(v3)
    return vs


def _try_iig(name_en, timeout=8):
    """尝试 iig 直连, 返回 (url, is_direct_hit)"""
    if not name_en:
        return None, False
    for slug in _iig_slug_variants(name_en):
        url = f"https://interfaceingame.com/games/games/{slug}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            resp = urllib.request.urlopen(req, timeout=timeout, context=_CTX)
            if resp.getcode() == 200 and slug in resp.geturl().lower():
                return url, True
        except Exception:
            continue
    return None, False


def build_ui_links(name_cn, name_en, try_iig_direct=True):
    """构造 UI 界面 / 纹理材质 分类的 links 列表。

    策略 (2026-07-02 v3, 用户反馈: 搜索引擎跳转其实更方便):
    - iig 直连命中 -> 精确 /games/games/{slug}/ 详情页(一次到位)
    - iig 未命中 -> Google site:interfaceingame.com {name_en}
    - gameui.net -> Google site:gameui.net {name_cn}
    - ArtStation / Pinterest UI 保留作为兜底

    Google site: 语法结果精度高, 一次点击到搜索结果页, 候选已列出, 比给"全站列表让手扫"更快。"""
    links = []
    # 1. Interface In Game
    if name_en:
        iig_url, hit = (_try_iig(name_en) if try_iig_direct else (None, False))
        if hit:
            links.append({
                "title": f"Interface In Game《{name_en}》UI 收录页",
                "source": "InterfaceInGame", "url": iig_url,
                "note": "国外单机 UI 数据库·直链命中"
            })
        else:
            q = urllib.parse.quote(f"site:interfaceingame.com {name_en}")
            links.append({
                "title": f"Google 搜索「site:interfaceingame.com {name_en}」",
                "source": "InterfaceInGame",
                "url": f"https://www.google.com/search?q={q}",
                "note": "国外单机 UI 数据库·未直接收录, Google site: 搜索兜底"
            })
    # 2. GameUI.net (无 API, 走 Google site: 搜索)
    gu_query = name_cn or name_en or ""
    q_gu = urllib.parse.quote(f"site:gameui.net {gu_query}")
    links.append({
        "title": f"Google 搜索「site:gameui.net {gu_query}」",
        "source": "GameUI.net",
        "url": f"https://www.google.com/search?q={q_gu}",
        "note": f"国内/手游 UI 数据库·用 Google site: 定位「{gu_query}」的 /game/{{id}} 直链"
    })
    # 3. 兜底: ArtStation UI + Pinterest UI
    if name_en:
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


def build_assets_block(name_cn, name_en, official_extra=None, try_iig_direct=True):
    """完整 assets 块 (official + inspiration)。official_extra: 该游戏的商店/官网链接 list"""
    official_extra = official_extra or []
    return {
        "official": [
            {"cat": "商店页 + 官网", "links": official_extra + [
                {"title": f"小红书搜索「{name_cn}」", "source": "小红书",
                 "url": f"https://www.xiaohongshu.com/search_result?keyword={enc(name_cn)}"}]},
            {"cat": "角色建模 / 概念设定图", "links": [
                {"title": f"ArtStation 搜索「{name_en}」", "source": "ArtStation",
                 "url": f"https://www.artstation.com/search?sort_by=relevance&query={enc(name_en)}"},
                {"title": f"Pinterest 搜索「{name_en} art」", "source": "Pinterest",
                 "url": f"https://www.pinterest.com/search/pins/?q={enc(name_en+' art')}"}]},
        ],
        "inspiration": [
            {"cat": "概念美术 / Concept Art", "links": [
                {"title": f"ArtStation 搜索「{name_en} concept art」", "source": "ArtStation",
                 "url": f"https://www.artstation.com/search?sort_by=relevance&query={enc(name_en+' concept art')}"},
                {"title": f"Pinterest 搜索「{name_en} concept art」", "source": "Pinterest",
                 "url": f"https://www.pinterest.com/search/pins/?q={enc(name_en+' concept art')}"}]},
            {"cat": "角色设计", "links": [
                {"title": f"ArtStation 搜索「{name_en} character」", "source": "ArtStation",
                 "url": f"https://www.artstation.com/search?sort_by=relevance&query={enc(name_en+' character')}"},
                {"title": f"Behance 搜索「{name_en}」", "source": "Behance",
                 "url": f"https://www.behance.net/search/projects?search={enc(name_en)}"}]},
            {"cat": "UI 界面 / 纹理材质",
             "links": build_ui_links(name_cn, name_en, try_iig_direct=try_iig_direct)},
        ],
    }
