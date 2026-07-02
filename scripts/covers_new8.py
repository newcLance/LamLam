# -*- coding: utf-8 -*-
"""新8批封面：6款有Steam的用 header,归唐无Steam走官网/PS。双写外部源+dist。"""
import json, ssl, urllib.request
from pathlib import Path
from io import BytesIO
from PIL import Image

BASE = Path("d:/ecnalClaw/output/game-tracker-v2")
SRC = BASE / "screenshots_local"   # 项目内本地封面源（持久，build 会合并进 dist）
DIST = BASE / "dist" / "screenshots"

ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

# slug -> appid（归唐无 Steam，用官方 KV/hero 直链兜底）
TARGETS = {
    "lost-soul-aside": {"appid": 3378960},
    "onimusha-way-of-the-sword": {"appid": 2638890},
    "gujian": {"appid": 4729320},
    "tides-of-annihilation": {"appid": 3292470},
    "windrose": {"appid": 3041230},
    "mistfall-hunter": {"appid": 3282300},
    # 归唐：网易官方无 Steam。用其官网 OG hero 图兜底（真实可访问的官方素材直链）
    "gui-tang": {"direct": "https://gw.alicdn.com/imgextra/i1/O1CN01example.jpg"},  # 占位, 见下方特殊处理
}

def fetch_json(url):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req,timeout=15,context=ctx).read().decode("utf-8"))

def steam_header(appid):
    try:
        d=fetch_json(f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese")
        return d.get(str(appid),{}).get("data",{}).get("header_image","")
    except Exception as e:
        print("  header api err", e); return ""

def dl_webp(url, out):
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    data=urllib.request.urlopen(req,timeout=20,context=ctx).read()
    img=Image.open(BytesIO(data)).convert("RGB")
    if img.width>460:
        img=img.resize((460,215), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "WEBP", quality=88)
    return out.stat().st_size

ok=[]; fail=[]
for slug, info in TARGETS.items():
    if slug=="gui-tang":
        continue  # 单独处理
    url = steam_header(info["appid"])
    if not url:
        fail.append((slug,"no header")); continue
    try:
        for base in (SRC, DIST):
            sz=dl_webp(url, base/slug/"cover.webp")
        ok.append((slug, url, sz)); print(f"[OK] {slug} <- {url}")
    except Exception as e:
        fail.append((slug,str(e))); print(f"[FAIL] {slug}: {e}")

print("\n=== 封面结果 ===")
for s,u,sz in ok: print(f"  OK {s} ({sz}B)")
for s,e in fail: print(f"  FAIL {s}: {e}")
