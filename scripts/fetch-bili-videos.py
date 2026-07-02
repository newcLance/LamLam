#!/usr/bin/env python3
"""
B站视频采集脚本 v2 — 严格相关度版

用法:
  python scripts/fetch-bili-videos.py                    # 处理所有游戏
  python scripts/fetch-bili-videos.py --slug signalis    # 单款
  python scripts/fetch-bili-videos.py --dry-run          # 预览不写入
  python scripts/fetch-bili-videos.py --verify-only      # 验证现有数据
  python scripts/fetch-bili-videos.py --audit            # 审计所有游戏，列出可疑视频

策略升级（2026-05-19）:
  1. 双关键词搜索：「{中文名}」+「{英文名}」+「{中文名} 游戏」+「{英文名} game」
  2. 综合排序（B 站 totalrank），非纯播放量
  3. 严格相关度评分:
     - 标题/UP 名含完整游戏名 +50
     - UP 是官方号（名含游戏名+官方/Official/Studio）+30
     - 头部游戏 UP（老番茄/籽岷/敖厂长/芒果冰OL...）+20
     - 标题含「游戏/实况/攻略/全流程/通关/解说/试玩/评测/首发」+10
     - 黑名单（同名歌曲/壁纸/铃声/动态桌面/翻唱/MV/搞笑混剪/营销号）-100
     - 分数 >= 40 才入库
  4. 写入前再次用 view API 双重验证 + 标题黑白名单复核
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
import re
import argparse
from pathlib import Path

# Windows GBK 控制台无法打印 emoji（如视频标题里的🤡）会 UnicodeEncodeError 崩溃。
# 强制 stdout/stderr 用 UTF-8，遇到无法编码的字符替换而非崩溃。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ── 配置 ──────────────────────────────────────────────
BILI_SEARCH_API = "https://api.bilibili.com/x/web-interface/search/type"
BILI_VIEW_API = "https://api.bilibili.com/x/web-interface/view"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
MIN_PLAY = 5000            # 最低播放量门槛（降低以容纳冷门游戏）
TARGET_COUNT = 5
REQUEST_DELAY = 1.5
VERIFY_DELAY = 0.8
RELEVANCE_THRESHOLD = 40   # 分数门槛

# 头部游戏 UP 主白名单（命中加分）
TOP_GAME_UPS = {
    # 通用游戏
    "老番茄", "敖厂长", "芒果冰OL", "籽岷", "五十嵐", "五十岚", "靠脸吃饭的徐大王",
    "AmazingLP", "逍遥散人", "黑桐谷歌", "蓝月夜雪", "Skyline游戏", "OMG电竞",
    "屌德斯解说", "大祥哥来了", "怕上火暴王老菊", "大蛇丸的解说", "纯黑-V",
    "PaPa丶猪", "羊老板", "大锤说他不想说话", "若风", "卡尔Vinson",
    # 主机/单机向
    "鹿鸣Backy", "Steam硬核游戏指南", "GameDB", "WaytoooDeep", "VGtime", 
    "游民星空", "3DMGAME", "电玩历史馆", "马男的精神世界", "暗影行者",
    # 网易心动游戏频道、IGN中国、A9VG 等媒体
    "IGN中国", "A9VG电玩部落", "Eurogamer", "GameLook", "游研社",
    # PvP/FPS 向
    "蓝忘机games", "刺激马伯庸", "西瓜JUN", "魔法Acker",
}

# 标题正向关键词（命中加分）
POSITIVE_KEYWORDS = [
    "实况", "攻略", "全流程", "通关", "速通", "解说", "试玩", "评测", "首发",
    "全收集", "全成就", "白金", "全结局", "剧情向", "深度评测", "上手", "体验",
    "游戏", "Gameplay", "gameplay", "Walkthrough", "walkthrough", "Review", "review",
    "首测", "测评", "实机", "演示", "全章节", "boss战", "BOSS",
    "结局", "剧情", "全任务", "支线"
]

# 标题黑名单（命中扣分/拒绝）
NEGATIVE_KEYWORDS = [
    "壁纸", "铃声", "手机主题", "动态桌面", "翻唱", "cover", "Cover",
    "歌曲", "MV", "钢琴版", "古筝版", "二胡", "翻奏", "音乐",
    "搞笑混剪", "鬼畜", "鬼蓄", "沙雕", "毒奶粉", "口胡",
    "盘点100", "TOP100", "top100", "100个", "100款", "盘点全部",
    "壁纸4K", "壁纸 4K", "2分钟看完", "5分钟看完",
    "网易云", "QQ音乐", "听歌", "BGM", "插曲推荐",
    "lol", "英雄联盟", "王者荣耀",  # 同名 / 蹭流量
    "Stray Kids", "stray kids", "STRAY KIDS",  # 韩国男团
    "喜羊羊", "灰太狼",  # 国产动画同人
    "拆迁队", "拆迁款", "拆迁房", "拆迁补偿",  # Teardown 误中
    "披萨塔尖叫",  # Pizza Tower 同名梗
    "迷失东京", "迷失太空", "迷失青岛", "迷失自我",  # Stray 误中
    "信号灯", "信号塔", "信号空隙", "信号机",  # Signalis 误中
    "蛋仔派对",  # 与 Eggy Party 同名但也是关键词
    "原子弹", "原子核", "原子结构",  # Atomic Heart 误中
    "异常的信号",  # 剑星 误中
]

# B 站游戏类分区 tid（数字判定，因为 tname 字段已返回空）
# B 站游戏类分区 tid（数字判定，因为 tname 字段已返回空）
GAME_TIDS = {17, 65, 19, 20, 121, 17170, 171, 172, 173, 174, 175, 176, 177, 178}
# 17=游戏, 65=电子竞技, 19=网络游戏, 20=单机游戏, 121=游戏赛事

# 通用词中文名清单（这些游戏中文名太常用，必须英文名/Alias 命中才能算相关）
GENERIC_CN_NAMES = {
    "信号", "信号机", "出走", "蜡笔小新", "传说", "无主之地",
    "战神",          # God of War
    "迷失",          # Stray
    "星刃",          # Stellar Blade
    "小丑牌",        # Balatro
    "疏浚",          # Dredge
    "拆迁",          # Teardown
    "异环",          # Neverness to Everness
    "无限大",        # Ananta
    "披萨塔",        # Pizza Tower
    "归唐",          # Blood Message（唐/归唐是常见词，需英文名 Blood Message 命中）
    "古剑",          # GuJian（会撞老古剑奇谭1/2/3，需实机/烛龙/古剑奇谭四 命中）
    "湮灭之潮",      # Tides of Annihilation（湮灭是常见词）
}

# ── 工具函数 ──────────────────────────────────────────

def api_get(url, params=None, max_retries=3):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            resp = urllib.request.urlopen(req, timeout=15)
            return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 2)
            else:
                print(f"    [warn] API 请求失败: {e}")
                return None


def search_bili(keyword, order="totalrank", page=1):
    """
    搜索 B站视频 — 优先用 search HTML 端点（更稳，不易被反爬）
    fallback 到 search/type API
    """
    # 方案 1: HTML 搜索结果页（提取 BV 列表 + 标题 + UP）
    html_url = "https://search.bilibili.com/all"
    html_params = {
        "keyword": keyword,
        "order": order,
        "page": page,
    }
    try:
        url = html_url + "?" + urllib.parse.urlencode(html_params)
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        # 从 __NEXT_DATA__ 或正则抓视频信息
        results = parse_search_html(html)
        if results:
            return results
    except Exception as e:
        pass

    # 方案 2: API 备选
    params = {
        "search_type": "video",
        "keyword": keyword,
        "order": order,
        "page": page,
    }
    data = api_get(BILI_SEARCH_API, params)
    if not data or data.get("code") != 0:
        return []
    return data.get("data", {}).get("result", []) or []


def parse_search_html(html):
    """从 search.bilibili.com 的 HTML 提取视频列表"""
    results = []
    # 用 __pinia 或 window.__INITIAL_STATE__ 都不稳定，直接 regex 提取 BV 卡片
    # 简化版：扫描所有 BV 号，配合 view API 获取详情
    bvids = list(dict.fromkeys(re.findall(r'(BV[A-Za-z0-9]{10})', html)))
    # 取前 25 个（一页约 30）
    for bv in bvids[:25]:
        results.append({
            "bvid": bv,
            "title": "",
            "play": 0,
            "author": "",
            "description": "",
            "typename": "",
            "typeid": 0,
            "_needs_view": True,  # 标记需要 view API 补充
        })
    return results


def clean_html(text):
    """清除 B 站搜索返回的 HTML 高亮标签"""
    return re.sub(r'<[^>]+>', '', text or "")


def format_views(play_count):
    if play_count >= 10000000:
        return f"{play_count / 10000000:.1f}千万"
    if play_count >= 10000:
        return f"{play_count / 10000:.0f}万"
    return str(play_count)


def build_name_variants(name_cn, name_en, alias):
    """构建名称变体（全小写）"""
    variants = set()
    for raw in [name_cn, name_en, alias]:
        if not raw:
            continue
        for piece in str(raw).replace("，", ",").split(","):
            p = piece.strip()
            if not p:
                continue
            variants.add(p.lower())
            # 去括号内年份
            cleaned = re.sub(r'\s*[\(（][^)]+[\)）]\s*', '', p).strip()
            if cleaned:
                variants.add(cleaned.lower())
            # 中文冒号互换
            variants.add(p.replace("：", ":").lower())
            variants.add(p.replace(":", "：").lower())
            # 去空格版本
            variants.add(p.replace(" ", "").lower())
    variants.discard("")
    return variants


def has_full_name_match(text, name_variants, name_cn, name_en):
    """
    严格检查：必须完整命中某个 name_variant（不是子串截断）
    text 已经是小写
    """
    if not text:
        return False
    text_lc = text.lower()
    text_nospace = text_lc.replace(" ", "")

    for v in name_variants:
        if not v or len(v) < 2:
            continue
        # 中文：直接子串匹配（中文里一般完整匹配就算）
        if re.search(r'[\u4e00-\u9fa5]', v):
            if v in text_lc:
                return True
        else:
            # 英文：必须是单词边界（避免 ARC 命中 "march"）
            pattern = r'(?<![a-z0-9])' + re.escape(v) + r'(?![a-z0-9])'
            if re.search(pattern, text_lc):
                return True
            # 去空格版本（PhantomBladeZero 也算）
            if v.replace(" ", "") in text_nospace and len(v.replace(" ", "")) >= 6:
                return True
    return False


def score_video(video_info, name_variants, name_cn, name_en):
    """
    计算视频相关度评分
    输入：search 结果或 view API 返回的 dict（含 title, author/owner_name, desc, tname, tid, play）
    """
    title = clean_html(video_info.get("title", ""))
    author = video_info.get("author", "") or video_info.get("owner_name", "")
    desc = clean_html(video_info.get("desc", "") or video_info.get("description", ""))
    tname = video_info.get("tname", "")
    tid = video_info.get("tid", 0)
    play = video_info.get("play", 0) or video_info.get("view", 0)

    title_lc = title.lower()
    text = (title + " " + desc).lower()

    score = 0
    reasons = []

    # 必要条件：标题或 UP 名必须命中完整游戏名
    name_match_in_title = has_full_name_match(title_lc, name_variants, name_cn, name_en)
    name_match_in_author = has_full_name_match((author or "").lower(), name_variants, name_cn, name_en)
    if not (name_match_in_title or name_match_in_author):
        return -1, ["NO_NAME_MATCH"]

    # 通用中文名严格判定：必须英文名/Alias 命中（书名号包裹中文名仅作为加分，不能替代英文名）
    if name_cn and name_cn in GENERIC_CN_NAMES:
        en_variants = set()
        if name_en:
            en_variants.add(name_en.lower())
            en_variants.add(name_en.replace(" ", "").lower())
        en_match = False
        for v in en_variants:
            if not v or len(v) < 3:
                continue
            pattern = r'(?<![a-z0-9])' + re.escape(v) + r'(?![a-z0-9])'
            if re.search(pattern, title_lc) or re.search(pattern, (author or "").lower()):
                en_match = True
                break
        if not en_match:
            return -1, [f"GENERIC_CN_NEEDS_EN[{name_cn}]"]
        # 书名号包裹中文名时额外加分
        bracketed_patterns = [
            f"《{name_cn}》", f"【{name_cn}】", f"〖{name_cn}〗",
            f"「{name_cn}」", f"『{name_cn}』",
        ]
        if any(p in title for p in bracketed_patterns):
            score += 10
            reasons.append("bracketed+10")

    # 1. 完整名命中
    if name_match_in_title:
        score += 50
        reasons.append("title_match+50")
    if name_match_in_author:
        score += 20
        reasons.append("author_match+20")

    # 2. 黑名单
    for kw in NEGATIVE_KEYWORDS:
        if kw.lower() in title_lc:
            score -= 100
            reasons.append(f"NEG[{kw}]-100")
            break  # 一个就够了

    # 3. 头部 UP 加分
    if author and author.strip() in TOP_GAME_UPS:
        score += 20
        reasons.append(f"top_up[{author}]+20")

    # 4. 官方号（UP 名含游戏名 + 官方/Official/Studio）
    if author:
        au_lc = author.lower()
        if name_match_in_author and any(t in au_lc for t in ["官方", "official", "studio", "工作室"]):
            score += 30
            reasons.append("official+30")

    # 5. 正向关键词
    for kw in POSITIVE_KEYWORDS:
        if kw in title:  # 大小写敏感保留中文
            score += 10
            reasons.append(f"pos[{kw}]+10")
            break

    # 6. 分区加分（游戏分区）
    if tid and int(tid) in GAME_TIDS:
        score += 15
        reasons.append(f"game_tid[{tid}]+15")

    # 7. 播放量微调（>=100万再加分，避免冷门高分）
    if play >= 1000000:
        score += 5
        reasons.append("play_1m+5")
    if play >= 5000000:
        score += 5
        reasons.append("play_5m+5")

    return score, reasons


def verify_video(bvid):
    data = api_get(BILI_VIEW_API, {"bvid": bvid})
    if not data or data.get("code") != 0:
        return False, {"error": f"code={data.get('code') if data else 'None'}"}
    vd = data.get("data", {})
    return True, {
        "title": vd.get("title", ""),
        "play": vd.get("stat", {}).get("view", 0),
        "tname": vd.get("tname", ""),
        "tid": vd.get("tid", 0),
        "desc": vd.get("desc", ""),
        "duration": vd.get("duration", 0),
        "owner_name": vd.get("owner", {}).get("name", ""),
    }


# ── 主采集流程 ──────────────────────────────────────────

def fetch_videos_for_game(slug, game_data, dry_run=False, verbose=False):
    name_cn = game_data.get("nameCN", "") or game_data.get("name", "")
    name_en = game_data.get("name", "")
    alias = game_data.get("alias", "")
    name_variants = build_name_variants(name_cn, name_en, alias)

    print(f"\n{'='*60}")
    print(f"[GAME] {name_cn} ({name_en}) [{slug}]")
    print(f"{'='*60}")
    print(f"  variants: {sorted(name_variants)[:10]}")

    # 关键词列表（双重检测 + 「游戏」后缀）
    keywords = []
    if name_cn:
        keywords.append(name_cn)
        keywords.append(f"{name_cn} 游戏")
    if name_en and name_en.lower() != name_cn.lower():
        keywords.append(name_en)
        keywords.append(f"{name_en} game")
    if alias and alias.lower() != name_cn.lower() and alias.lower() != name_en.lower():
        keywords.append(alias)

    candidates = {}  # bvid -> (info, score, reasons)

    for kw in keywords:
        print(f"  [search] {kw}")
        results = search_bili(kw, order="totalrank")
        time.sleep(REQUEST_DELAY)

        for r in results:
            bvid = r.get("bvid", "")
            if not bvid:
                continue

            # 如果是 HTML 抓的（无标题/播放量），先用 view API 取信息
            if r.get("_needs_view"):
                if bvid in candidates:
                    continue  # 之前已经有候选不用重复 view
                time.sleep(VERIFY_DELAY)
                ok, vinfo = verify_video(bvid)
                if not ok:
                    continue
                if vinfo["duration"] < 60:
                    continue
                if vinfo["play"] < MIN_PLAY:
                    continue
                info = {
                    "bvid": bvid,
                    "title": vinfo["title"],
                    "author": vinfo["owner_name"],
                    "desc": vinfo["desc"],
                    "tname": vinfo["tname"],
                    "tid": vinfo["tid"],
                    "play": vinfo["play"],
                }
            else:
                play = r.get("play", 0)
                if play < MIN_PLAY:
                    continue
                info = {
                    "bvid": bvid,
                    "title": clean_html(r.get("title", "")),
                    "author": r.get("author", ""),
                    "desc": r.get("description", ""),
                    "tname": r.get("typename", ""),
                    "tid": r.get("typeid", 0),
                    "play": play,
                }
            score, reasons = score_video(info, name_variants, name_cn, name_en)

            if score < RELEVANCE_THRESHOLD:
                if verbose:
                    print(f"    [skip {score:>3}] {info['title'][:50]} ({format_views(info['play'])}) [{','.join(reasons[:3])}]")
                continue

            # 同 bvid 取更高分
            if bvid in candidates and candidates[bvid][1] >= score:
                continue
            candidates[bvid] = (info, score, reasons)
            print(f"    [keep {score:>3}] {info['title'][:50]} ({format_views(info['play'])}) UP={info['author']}")

    if not candidates:
        print(f"  [warn] 无候选视频")
        return [], {"status": "no_results"}

    # 按 score 降序排，取 top
    sorted_cands = sorted(candidates.values(), key=lambda x: (x[1], x[0]["play"]), reverse=True)
    top_cands = sorted_cands[:TARGET_COUNT * 2]  # 取 2 倍备选给验证用

    print(f"\n  [verify] top {len(top_cands)}...")
    verified = []
    for info, score, reasons in top_cands:
        if len(verified) >= TARGET_COUNT:
            break
        time.sleep(VERIFY_DELAY)
        is_valid, vinfo = verify_video(info["bvid"])
        if not is_valid:
            print(f"    [fail] {info['bvid']}: {vinfo.get('error')}")
            continue
        if vinfo["duration"] < 30:
            print(f"    [fail] {info['bvid']}: 时长 {vinfo['duration']}s 过短")
            continue

        # 用 view API 真实数据再评一次分
        vinfo["author"] = vinfo["owner_name"]
        real_score, real_reasons = score_video(vinfo, name_variants, name_cn, name_en)
        if real_score < RELEVANCE_THRESHOLD:
            print(f"    [fail] {info['bvid']}: 二次评分 {real_score} 不达标 [{','.join(real_reasons[:3])}]")
            continue

        verified.append({
            "title": vinfo["title"],
            "bvid": info["bvid"],
            "views": format_views(vinfo["play"]),
            "_score": real_score,
            "_author": vinfo["owner_name"],
        })
        print(f"    [pass {real_score:>3}] {vinfo['title'][:50]} UP={vinfo['owner_name']}")

    if not verified:
        print(f"  [warn] 候选均未通过验证")
        return [], {"status": "all_failed"}

    output = [{"title": v["title"], "bvid": v["bvid"], "views": v["views"]} for v in verified]
    print(f"\n  [done] {len(output)} 条")
    for i, v in enumerate(verified, 1):
        print(f"    {i}. {v['title'][:55]} ({v['views']}) score={v['_score']} UP={v['_author']}")

    return output, {"status": "ok", "count": len(output)}


def audit_existing(slug, game_data):
    """审计现有视频，返回每条的评分/标题/状态"""
    name_cn = game_data.get("nameCN", "") or game_data.get("name", "")
    name_en = game_data.get("name", "")
    alias = game_data.get("alias", "")
    name_variants = build_name_variants(name_cn, name_en, alias)
    videos = game_data.get("playerExp", {}).get("biliVideos", [])

    if not videos:
        return {"slug": slug, "name": name_cn, "videos": []}

    report = {"slug": slug, "name": name_cn, "videos": []}
    for v in videos:
        bvid = v.get("bvid", "")
        if "placeholder" in bvid.lower() or len(bvid) < 10:
            report["videos"].append({"bvid": bvid, "score": -999, "status": "PLACEHOLDER", "title": v.get("title", "")})
            continue

        time.sleep(VERIFY_DELAY)
        ok, info = verify_video(bvid)
        if not ok:
            report["videos"].append({"bvid": bvid, "score": -999, "status": "DEAD", "title": v.get("title", ""), "error": info.get("error")})
            continue

        info["author"] = info["owner_name"]
        score, reasons = score_video(info, name_variants, name_cn, name_en)
        status = "PASS" if score >= RELEVANCE_THRESHOLD else "FAIL"
        report["videos"].append({
            "bvid": bvid,
            "score": score,
            "status": status,
            "title": info["title"],
            "real_play": info["play"],
            "author": info["owner_name"],
            "reasons": reasons[:5],
        })
    return report


def load_games_index(project_root):
    idx_file = project_root / "data" / "games.json"
    if not idx_file.exists():
        return {}
    with open(idx_file, "r", encoding="utf-8") as f:
        games_list = json.load(f)
    return {g.get("slug", ""): {
        "name": g.get("name", ""),
        "nameCN": g.get("nameCN", ""),
        "alias": g.get("alias", ""),
    } for g in games_list if g.get("slug")}


def main():
    parser = argparse.ArgumentParser(description="B站视频采集 v2 — 严格相关度版")
    parser.add_argument("--slug", help="只处理指定游戏")
    parser.add_argument("--dry-run", action="store_true", help="不写入文件")
    parser.add_argument("--verify-only", action="store_true", help="仅验证现有数据 (legacy)")
    parser.add_argument("--audit", action="store_true", help="审计所有游戏，输出 audit_report.json")
    parser.add_argument("--skip", help="跳过指定 slug（逗号分隔）")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    parser.add_argument("--audit-output", default="audit_report.json", help="审计输出文件")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    games_dir = project_root / "data" / "games"
    games_index = load_games_index(project_root)
    print(f"[init] {len(games_index)} 款游戏已索引")

    skip_list = set(s.strip() for s in (args.skip or "").split(",") if s.strip())

    if args.slug:
        json_files = [games_dir / f"{args.slug}.json"]
        if not json_files[0].exists():
            print(f"[error] 文件不存在: {json_files[0]}")
            sys.exit(1)
    else:
        json_files = sorted(games_dir.glob("*.json"))

    audit_results = []
    stats = {"processed": 0, "ok": 0, "no_results": 0, "skipped": 0}

    for jf in json_files:
        slug = jf.stem
        if slug in skip_list:
            stats["skipped"] += 1
            continue

        with open(jf, "r", encoding="utf-8") as f:
            game_data = json.load(f)

        if "playerExp" not in game_data:
            stats["skipped"] += 1
            continue

        # 从主索引补名
        if slug in games_index:
            idx = games_index[slug]
            game_data["name"] = game_data.get("name") or idx["name"]
            game_data["nameCN"] = game_data.get("nameCN") or idx["nameCN"]
            game_data["alias"] = game_data.get("alias") or idx["alias"]

        if args.audit:
            r = audit_existing(slug, game_data)
            audit_results.append(r)
            print(f"\n[{slug}] {r['name']}")
            for v in r["videos"]:
                print(f"  [{v['status']:>11}] {v['score']:>4} {v['bvid']}: {v['title'][:55]}")
            stats["processed"] += 1
            continue

        videos, vs = fetch_videos_for_game(slug, game_data, dry_run=args.dry_run, verbose=args.verbose)
        stats["processed"] += 1
        if vs["status"] == "ok":
            stats["ok"] += 1
            if not args.dry_run:
                # 重新读取原始 JSON，仅更新 biliVideos 字段，避免污染
                with open(jf, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                raw.setdefault("playerExp", {})["biliVideos"] = videos
                with open(jf, "w", encoding="utf-8") as f:
                    json.dump(raw, f, ensure_ascii=False, indent=2)
                print(f"  [save] {jf.name}")
        elif vs["status"] == "no_results":
            stats["no_results"] += 1

    if args.audit:
        out = project_root / args.audit_output
        with open(out, "w", encoding="utf-8") as f:
            json.dump(audit_results, f, ensure_ascii=False, indent=2)
        print(f"\n[audit] 报告已写入 {out}")

        # 汇总：失败/可疑视频
        print(f"\n{'='*60}\n审计汇总\n{'='*60}")
        for r in audit_results:
            bad = [v for v in r["videos"] if v["status"] != "PASS"]
            if bad:
                print(f"\n[{r['slug']}] {r['name']}: {len(bad)}/{len(r['videos'])} 条不合格")
                for v in bad:
                    print(f"  - [{v['status']}] {v['bvid']}: {v.get('title','')[:55]} (score={v['score']})")

    print(f"\n[stat] processed={stats['processed']} ok={stats['ok']} no_results={stats['no_results']} skipped={stats['skipped']}")


if __name__ == "__main__":
    main()
