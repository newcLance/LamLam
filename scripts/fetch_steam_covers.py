"""
批量下载 Steam header 图作为游戏卡片封面
用法: python scripts/fetch_steam_covers.py

流程:
1. 遍历 data/games.json，用游戏英文名搜索 Steam appid
2. 通过 Steam API 获取 header_image URL
3. 下载并转为 WebP，保存到 screenshots/{slug}/cover.webp
4. 注册到 screenshots.json 确保构建能读到
"""
import json, os, sys, urllib.request, urllib.error, ssl, time

try:
    from PIL import Image
    from io import BytesIO
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("[WARN] Pillow not installed, will save as jpg instead of webp")

SS_SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "..", "game-platform-analysis", "screenshots")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    return json.loads(resp.read().decode("utf-8"))

def search_steam_appid(game_name):
    """Search Steam for a game and return appid"""
    try:
        encoded = urllib.request.quote(game_name)
        url = f"https://store.steampowered.com/api/storesearch/?term={encoded}&l=english&cc=US"
        data = fetch_json(url)
        items = data.get("items", [])
        if items:
            return str(items[0]["id"])
    except:
        pass
    return None

def get_steam_header(appid):
    """Get header image URL from Steam API"""
    try:
        url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
        data = fetch_json(url)
        app_data = data.get(str(appid), {}).get("data", {})
        return app_data.get("header_image", "")
    except:
        return ""

def download_image(url, save_path):
    """Download image and convert to WebP"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    img_data = resp.read()
    
    if HAS_PIL:
        img = Image.open(BytesIO(img_data))
        # Resize to 460x215 if larger (Steam header standard size)
        if img.width > 460:
            img = img.resize((460, 215), Image.LANCZOS)
        img.save(save_path, "WEBP", quality=85)
    else:
        # Fallback: save as-is
        with open(save_path.replace(".webp", ".jpg"), "wb") as f:
            f.write(img_data)

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    with open("data/games.json", "r", encoding="utf-8") as f:
        games = json.load(f)
    
    # Also check what covers already exist
    existing = set()
    for g in games:
        slug = g["slug"]
        cover_path = os.path.join(SS_SRC, slug, "cover.webp")
        if os.path.exists(cover_path):
            existing.add(slug)
    
    print(f"Total games: {len(games)}, already have covers: {len(existing)}")
    
    success = 0
    failed = []
    skipped = 0
    
    for i, g in enumerate(games, 1):
        slug = g["slug"]
        name = g.get("name", "")
        nameCN = g.get("nameCN", "")
        
        if slug in existing:
            skipped += 1
            continue
        
        print(f"\n[{i}/{len(games)}] {nameCN or name} ({slug})")
        
        # Try to find appid from assets first
        appid = None
        try:
            with open(f"data/games/{slug}.json", "r", encoding="utf-8") as f2:
                detail = json.load(f2)
            for group in detail.get("assets", {}).get("official", []):
                for link in group.get("links", []):
                    if "store.steampowered.com/app/" in link.get("url", ""):
                        appid = link["url"].split("/app/")[1].split("/")[0].split("?")[0]
                        break
                if appid: break
        except:
            pass
        
        # If no appid in assets, search Steam
        if not appid:
            print(f"  Searching Steam for: {name}")
            appid = search_steam_appid(name)
            if not appid and nameCN:
                appid = search_steam_appid(nameCN)
            time.sleep(0.3)  # Rate limit
        
        if not appid:
            print(f"  [SKIP] No Steam appid found")
            failed.append((slug, nameCN or name, "no appid"))
            continue
        
        print(f"  Steam appid: {appid}")
        
        # Get header image URL
        header_url = get_steam_header(appid)
        if not header_url:
            print(f"  [SKIP] No header image")
            failed.append((slug, nameCN or name, "no header"))
            continue
        
        # Download
        slug_dir = os.path.join(SS_SRC, slug)
        os.makedirs(slug_dir, exist_ok=True)
        cover_path = os.path.join(slug_dir, "cover.webp")
        
        try:
            download_image(header_url, cover_path)
            size_kb = os.path.getsize(cover_path) // 1024
            print(f"  [OK] cover.webp ({size_kb}KB)")
            success += 1
        except Exception as e:
            print(f"  [FAIL] {str(e)[:60]}")
            failed.append((slug, nameCN or name, str(e)[:60]))
        
        time.sleep(0.3)  # Rate limit
    
    print(f"\n{'='*50}")
    print(f"Results: {success} downloaded, {skipped} skipped (existing), {len(failed)} failed")
    if failed:
        print(f"\nFailed:")
        for slug, name, reason in failed:
            print(f"  {name} ({slug}): {reason}")

if __name__ == "__main__":
    main()
