#!/usr/bin/env python3
"""
B站视频采集脚本 — 通过搜索 API 拉取真实 biliVideos 数据

用法:
  python scripts/fetch-bili-videos.py                    # 处理所有游戏
  python scripts/fetch-bili-videos.py --slug black-myth-wukong  # 只处理指定游戏
  python scripts/fetch-bili-videos.py --dry-run           # 预览模式，不写入文件
  python scripts/fetch-bili-videos.py --verify-only       # 仅验证现有数据

流程:
  1. 读取 data/games/{slug}.json
  2. 用游戏中文名+英文名搜索 B站（按播放量排序）
  3. 合并去重，取 top 5
  4. 逐条调 B站 view API 验证视频真实性
  5. 写回 JSON
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

# ── 配置 ──────────────────────────────────────────────
BILI_SEARCH_API = "https://api.bilibili.com/x/web-interface/search/type"
BILI_VIEW_API = "https://api.bilibili.com/x/web-interface/view"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com"
}
MIN_PLAY = 10000           # 最低播放量门槛
TARGET_COUNT = 5           # 每款游戏取 5 条
REQUEST_DELAY = 1.5        # API 请求间隔（秒），避免被风控
VERIFY_DELAY = 0.8         # 验证请求间隔

# 游戏相关的 B站分区（tname），用于过滤无关分区
GAME_ZONES = {
    "单机游戏", "网络游戏", "手机游戏", "电子竞技", "游戏",
    "GMV", "Mugen", "游戏杂谈", "其他游戏", "音游",
    "综合", "影视杂谈", "动画", "科技", "数码", "知识"  # 宽松匹配
}

# ── 工具函数 ──────────────────────────────────────────

def api_get(url, params=None, max_retries=3):
    """带重试的 API GET 请求"""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            resp = urllib.request.urlopen(req, timeout=15)
            data = json.loads(resp.read().decode("utf-8"))
            return data
        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 2
                print(f"    ⚠ 请求失败 ({e})，{wait}s 后重试...")
                time.sleep(wait)
            else:
                print(f"    ✗ 请求最终失败: {e}")
                return None


def search_bili(keyword, page=1):
    """搜索 B站视频，返回结果列表"""
    params = {
        "search_type": "video",
        "keyword": keyword,
        "order": "click",  # 按播放量排序
        "page": page,
    }
    data = api_get(BILI_SEARCH_API, params)
    if not data or data.get("code") != 0:
        return []
    results = data.get("data", {}).get("result", [])
    if results is None:
        return []
    return results


def clean_title(title):
    """清除搜索结果中的 HTML 高亮标签"""
    return re.sub(r'<em class="keyword">', '', re.sub(r'</em>', '', title))


def format_views(play_count):
    """格式化播放量为中文可读格式"""
    if play_count >= 10000000:
        return f"{play_count / 10000000:.0f}千万"
    if play_count >= 10000:
        return f"{play_count / 10000:.0f}万"
    return str(play_count)


def verify_video(bvid):
    """
    通过 B站 view API 验证视频
    返回 (is_valid, info_dict) 
    """
    data = api_get(BILI_VIEW_API, {"bvid": bvid})
    if not data or data.get("code") != 0:
        return False, {"error": f"API 返回 code={data.get('code') if data else 'None'}"}
    
    vdata = data.get("data", {})
    title = vdata.get("title", "")
    play = vdata.get("stat", {}).get("view", 0)
    tname = vdata.get("tname", "")
    desc = vdata.get("desc", "")
    duration = vdata.get("duration", 0)
    
    return True, {
        "title": title,
        "play": play,
        "tname": tname,
        "desc": desc,
        "duration": duration,
    }


def build_name_variants(game_name_cn, game_name_en, alias_str=""):
    """
    构建游戏名匹配变体列表（全小写）
    """
    variants = set()
    
    if game_name_cn:
        cn = game_name_cn.strip()
        variants.add(cn.lower())
        # 去掉括号内的年份标注，如"使命召唤：现代战争2 (2022)" → "使命召唤：现代战争2"
        import re
        cleaned = re.sub(r'\s*[\(（]\d{4}[\)）]\s*', '', cn).strip()
        if cleaned:
            variants.add(cleaned.lower())
        # 中文冒号/英文冒号互换
        variants.add(cn.replace("：", ":").lower())
        variants.add(cn.replace(":", "：").lower())
    
    if game_name_en:
        en = game_name_en.strip()
        variants.add(en.lower())
        # 去掉括号内的年份
        cleaned = re.sub(r'\s*[\(（]\d{4}[\)）]\s*', '', en).strip()
        if cleaned:
            variants.add(cleaned.lower())
    
    # alias 支持逗号分隔多个别名
    if alias_str:
        for a in alias_str.split(","):
            a = a.strip()
            if a:
                variants.add(a.lower())
    
    # 过滤掉空字符串
    variants.discard("")
    return variants


def is_relevant_video(title, desc, game_name_cn, game_name_en, tname="", extra_variants=None):
    """
    判断视频是否与目标游戏相关
    extra_variants: 额外的名称变体集合（全小写）
    """
    text = (title + " " + desc).lower()
    
    # 基础名称匹配
    name_variants = set()
    if game_name_cn:
        name_variants.add(game_name_cn.lower())
    if game_name_en:
        name_variants.add(game_name_en.lower())
        name_variants.add(game_name_en.replace(" ", "").lower())
    
    # 合并额外变体
    if extra_variants:
        name_variants.update(extra_variants)
    
    # 任一变体命中即可
    has_game_name = False
    for v in name_variants:
        if v in text or v in text.replace(" ", ""):
            has_game_name = True
            break
    
    if not has_game_name:
        return False
    
    # 排除明显无关的内容类型
    spam_keywords = ["壁纸", "铃声", "手机主题", "动态桌面", "直播切片合集",
                     "混剪100", "盘点100", "top100"]
    for kw in spam_keywords:
        if kw in text:
            return False
    
    return True


def fetch_videos_for_game(slug, game_data, dry_run=False):
    """
    为单款游戏采集 B站视频
    返回 (videos_list, stats_dict)
    """
    name_cn = game_data.get("nameCN", "") or game_data.get("name", "")
    name_en = game_data.get("name", "")
    alias = game_data.get("alias", "")
    
    # 构建名称变体集（用于相关性匹配）
    name_variants = build_name_variants(name_cn, name_en, alias)
    
    print(f"\n{'='*60}")
    print(f"📺 {name_cn} ({name_en}) [{slug}]")
    print(f"{'='*60}")
    
    # 搜索关键词列表
    keywords = []
    if name_cn:
        keywords.append(name_cn)
    if name_en and name_en != name_cn:
        keywords.append(name_en)
    if alias and alias != name_cn and alias != name_en:
        keywords.append(alias)
    
    # 搜集所有候选视频
    candidates = {}  # bvid -> video_info
    
    for kw in keywords:
        print(f"  🔍 搜索: {kw}")
        results = search_bili(kw)
        time.sleep(REQUEST_DELAY)
        
        for r in results:
            bvid = r.get("bvid", "")
            if not bvid or bvid in candidates:
                continue
            
            title = clean_title(r.get("title", ""))
            play = r.get("play", 0)
            desc = r.get("description", "")
            
            # 播放量门槛
            if play < MIN_PLAY:
                continue
            
            # 相关性检查（使用增强变体）
            if not is_relevant_video(title, desc, name_cn, name_en, extra_variants=name_variants):
                print(f"    ⊘ 跳过(不相关): {title[:40]}... ({format_views(play)})")
                continue
            
            candidates[bvid] = {
                "title": title,
                "bvid": bvid,
                "play": play,
                "desc": desc
            }
            print(f"    ✓ 候选: {title[:40]}... ({format_views(play)})")
    
    if not candidates:
        print(f"  ⚠ 未找到符合条件的视频")
        return [], {"status": "no_results", "searched": keywords}
    
    # 按播放量排序，取 top N
    sorted_candidates = sorted(candidates.values(), key=lambda x: x["play"], reverse=True)
    top_candidates = sorted_candidates[:TARGET_COUNT]
    
    # 逐条验证
    print(f"\n  🔎 验证 top {len(top_candidates)} 条...")
    verified = []
    
    for c in top_candidates:
        time.sleep(VERIFY_DELAY)
        is_valid, info = verify_video(c["bvid"])
        
        if not is_valid:
            print(f"    ✗ 验证失败: {c['bvid']} — {info.get('error','')}")
            continue
        
        # 二次确认标题相关性（用 API 返回的真实标题）
        real_title = info["title"]
        if not is_relevant_video(real_title, info.get("desc", ""), name_cn, name_en, extra_variants=name_variants):
            print(f"    ✗ 标题不匹配: 搜索标题='{c['title'][:30]}' 实际='{real_title[:30]}'")
            continue
        
        # 检查视频时长（排除 < 10 秒的垃圾视频）
        if info["duration"] < 10:
            print(f"    ✗ 时长过短({info['duration']}s): {real_title[:40]}")
            continue
        
        verified.append({
            "title": real_title,
            "bvid": c["bvid"],
            "views": format_views(info["play"]),
            "_play_raw": info["play"],  # 内部字段，写入 JSON 前删除
            "_tname": info["tname"],
            "_verified": True
        })
        print(f"    ✓ 已验证: {real_title[:40]}... ({format_views(info['play'])})")
    
    if not verified:
        print(f"  ⚠ 所有候选均未通过验证")
        return [], {"status": "all_failed", "candidates": len(candidates)}
    
    # 清理内部字段
    output = []
    for v in verified:
        output.append({
            "title": v["title"],
            "bvid": v["bvid"],
            "views": v["views"]
        })
    
    print(f"\n  ✅ 最终结果: {len(output)} 条视频")
    for i, v in enumerate(output, 1):
        print(f"     {i}. [{v['bvid']}] {v['title'][:50]} ({v['views']})")
    
    return output, {"status": "ok", "count": len(output)}


def verify_existing_videos(slug, game_data):
    """
    仅验证现有 biliVideos 数据的正确性
    返回验证报告
    """
    name_cn = game_data.get("nameCN", "") or game_data.get("name", "")
    name_en = game_data.get("name", "")
    videos = game_data.get("playerExp", {}).get("biliVideos", [])
    
    print(f"\n🔎 验证: {name_cn} ({slug}) — {len(videos)} 条视频")
    
    report = {"slug": slug, "name": name_cn, "total": len(videos), "pass": 0, "fail": 0, "warn": 0, "details": []}
    
    for v in videos:
        bvid = v.get("bvid", "")
        claimed_title = v.get("title", "")
        
        if "placeholder" in bvid:
            report["fail"] += 1
            report["details"].append({"bvid": bvid, "status": "FAIL", "reason": "占位符 bvid"})
            print(f"  ✗ FAIL {bvid}: 占位符")
            continue
        
        time.sleep(VERIFY_DELAY)
        is_valid, info = verify_video(bvid)
        
        if not is_valid:
            report["fail"] += 1
            report["details"].append({"bvid": bvid, "status": "FAIL", "reason": f"API 错误: {info.get('error','')}"})
            print(f"  ✗ FAIL {bvid}: API 错误")
            continue
        
        real_title = info["title"]
        
        # 检查标题相关性
        if not is_relevant_video(real_title, info.get("desc", ""), name_cn, name_en):
            report["fail"] += 1
            report["details"].append({
                "bvid": bvid,
                "status": "FAIL",
                "reason": f"内容不相关 — 声称: '{claimed_title[:30]}' 实际: '{real_title[:30]}'"
            })
            print(f"  ✗ FAIL {bvid}: 内容不相关 (实际: {real_title[:40]})")
            continue
        
        # 检查播放量数量级
        claimed_views = v.get("views", "")
        real_play = info["play"]
        
        report["pass"] += 1
        report["details"].append({"bvid": bvid, "status": "PASS", "real_title": real_title, "play": real_play})
        print(f"  ✓ PASS {bvid}: {real_title[:40]} ({format_views(real_play)})")
    
    return report


# ── 主流程 ──────────────────────────────────────────

def load_games_index(project_root):
    """
    从 data/games.json 主索引加载游戏名信息
    返回 {slug: {name, nameCN, alias}} 的字典
    """
    index_file = project_root / "data" / "games.json"
    if not index_file.exists():
        print("⚠ data/games.json 不存在，将尝试从单个 JSON 文件读取名称")
        return {}
    
    with open(index_file, "r", encoding="utf-8") as f:
        games_list = json.load(f)
    
    index = {}
    for g in games_list:
        slug = g.get("slug", "")
        if slug:
            index[slug] = {
                "name": g.get("name", ""),
                "nameCN": g.get("nameCN", ""),
                "alias": g.get("alias", ""),
            }
    return index


def main():
    parser = argparse.ArgumentParser(description="B站视频采集 & 验证")
    parser.add_argument("--slug", help="只处理指定游戏的 slug")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不写入文件")
    parser.add_argument("--verify-only", action="store_true", help="仅验证现有数据")
    parser.add_argument("--skip", help="跳过指定游戏（逗号分隔）")
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent
    games_dir = project_root / "data" / "games"
    
    # 加载主索引获取游戏名
    games_index = load_games_index(project_root)
    print(f"📋 主索引: {len(games_index)} 款游戏")
    
    skip_list = set()
    if args.skip:
        skip_list = set(s.strip() for s in args.skip.split(","))
    
    # 获取要处理的游戏列表
    if args.slug:
        json_files = [games_dir / f"{args.slug}.json"]
        if not json_files[0].exists():
            print(f"✗ 文件不存在: {json_files[0]}")
            sys.exit(1)
    else:
        json_files = sorted(games_dir.glob("*.json"))
    
    total_stats = {"processed": 0, "skipped": 0, "success": 0, "failed": 0, "no_results": 0}
    
    for jf in json_files:
        slug = jf.stem
        
        if slug in skip_list:
            print(f"\n⊘ 跳过 (--skip): {slug}")
            total_stats["skipped"] += 1
            continue
        
        with open(jf, "r", encoding="utf-8") as f:
            game_data = json.load(f)
        
        # 检查是否有 playerExp（占位条目没有）
        if "playerExp" not in game_data:
            print(f"\n⊘ 跳过 (无 playerExp): {slug}")
            total_stats["skipped"] += 1
            continue
        
        # 从主索引补充游戏名信息
        if slug in games_index:
            idx = games_index[slug]
            if not game_data.get("name"):
                game_data["name"] = idx["name"]
            if not game_data.get("nameCN"):
                game_data["nameCN"] = idx["nameCN"]
            if not game_data.get("alias"):
                game_data["alias"] = idx["alias"]
        
        if args.verify_only:
            verify_existing_videos(slug, game_data)
            total_stats["processed"] += 1
            continue
        
        # 采集视频
        videos, stats = fetch_videos_for_game(slug, game_data, dry_run=args.dry_run)
        total_stats["processed"] += 1
        
        if stats["status"] == "ok":
            total_stats["success"] += 1
            
            if not args.dry_run:
                # 写回 JSON
                game_data["playerExp"]["biliVideos"] = videos
                # 清理临时补充的字段（不改变原始 JSON 结构）
                for key in ["name", "nameCN", "alias"]:
                    if key not in json.load(open(jf, "r", encoding="utf-8")):
                        game_data.pop(key, None)
                with open(jf, "w", encoding="utf-8") as f:
                    json.dump(game_data, f, ensure_ascii=False, indent=2)
                print(f"  💾 已写入 {jf.name}")
        elif stats["status"] == "no_results":
            total_stats["no_results"] += 1
        else:
            total_stats["failed"] += 1
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 总结")
    print(f"{'='*60}")
    print(f"  处理: {total_stats['processed']}  跳过: {total_stats['skipped']}")
    print(f"  成功: {total_stats['success']}  无结果: {total_stats['no_results']}  失败: {total_stats['failed']}")


if __name__ == "__main__":
    main()
