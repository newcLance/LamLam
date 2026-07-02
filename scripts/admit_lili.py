# -*- coding: utf-8 -*-
"""立项 322 粒粒的小人国 —— 阶段1 元数据建档"""
import json
from pathlib import Path

BASE = Path("d:/ecnalClaw/output/game-tracker-v2")

entry = {
    "id": 322,
    "name": "Animula Nook",
    "nameCN": "粒粒的小人国",
    "alias": "粒粒的小人国,粒粒小人国,小人国,Animula,Animula Nook",
    "icon": "🌸",
    "company": "腾讯游戏 × LilliLandia Games (北极光工作室群·银之心)",
    "category": "未发售",
    "region": "国产",
    "platforms": ["PC", "Mac", "PS5", "Switch 2", "移动"],
    "model": "免费制",
    "genre": "Simulation",
    "scale": "—",
    "mau": "—",
    "games": "—",
    "established": "2026 下半年",
    "releaseDate": "2026 下半年",
    "desc": "腾讯北极光工作室群与 LilliLandia Games 联合开发的小人国题材生活模拟治愈游戏。你意外变小到拇指大小，与「粒粒」们在书桌一角建造家园，用缩小枪把日常杂物变成建材，无任务驱动的慢生活体验。全球预约 800 万+，TapTap 9.6 分。",
    "features": ["小人国微缩视角", "生活模拟治愈", "缩小枪造家", "免费全平台", "无任务慢生活"],
    "changes": [],
    "lastUpdate": "2026-07-02",
    "slug": "animula-nook",
    "appid": 3767320,
    "website": "https://animulanook.com",
}

gp = BASE / "data" / "games.json"
games = json.load(open(gp, encoding="utf-8"))
if any(g["slug"] == entry["slug"] for g in games):
    print("[SKIP] 已存在")
else:
    games.append(entry)
    json.dump(games, open(gp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[ADD] #322 粒粒的小人国  total={len(games)}")
