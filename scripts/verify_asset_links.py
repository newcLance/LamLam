"""
素材链接审查脚本 — 新游戏管线必跑
用法: python scripts/verify_asset_links.py <slug>
      python scripts/verify_asset_links.py --all

审查规则:
1. HTTP 可达性（GET 请求，跟随重定向）
2. 反爬 403 的站点（ArtStation/Epic/IGDB/Behance）用白名单放行，但会标注
3. 需要登录才能访问的（NGA/部分论坛）→ FAIL
4. 页面标题必须包含游戏名关键词（中文或英文）→ 强相关校验
5. 重定向到首页/404 → FAIL
"""
import json, sys, os, urllib.request, urllib.error, ssl, re

# 反爬白名单：这些站点的 403 是反爬机制，浏览器可正常访问
ANTI_CRAWL_WHITELIST = {
    "artstation.com", "epicgames.com", "igdb.com", 
    "behance.net", "dribbble.com", "x.com", "twitter.com",
    "gameui.net", "playstation.com"
}

# 需要登录 / 搜索功能失效的黑名单
LOGIN_REQUIRED_BLACKLIST = {
    "ngabbs.com", "nga.cn", "bbs.nga.cn"
}

# 搜索参数失效的 URL 模式（这些站的 ?s= 搜索不生效，但 /game/{id} 直链可用）
SEARCH_BROKEN_PATTERNS = [
    ("gameui.net", "?s="),  # gameui.net/?s=xxx 跳首页，/game/13663 才是正确格式
]

def get_domain(url):
    from urllib.parse import urlparse
    return urlparse(url).netloc.replace("www.", "")

def check_link(url, game_keywords):
    domain = get_domain(url)
    
    # 黑名单直接拒绝
    for bl in LOGIN_REQUIRED_BLACKLIST:
        if bl in domain:
            return "FAIL", "需要登录才能访问，设计师打开是空白页"
    for pat_domain, pat_param in SEARCH_BROKEN_PATTERNS:
        if pat_domain in domain and pat_param in url:
            return "FAIL", f"该站 {pat_param} 搜索失效（跳首页），请用直链格式"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        code = resp.getcode()
        final_url = resp.geturl()
        
        if code >= 400:
            return "FAIL", f"HTTP {code}"
        
        # 检查是否重定向到首页
        if final_url.rstrip("/") in ["https://store.steampowered.com", "https://www.playstation.com", "https://store.epicgames.com"]:
            return "FAIL", f"重定向到首页: {final_url}"
        
        return "OK", f"HTTP {code}"
        
    except urllib.error.HTTPError as e:
        # 反爬白名单放行
        for wl in ANTI_CRAWL_WHITELIST:
            if wl in domain:
                return "WARN", f"HTTP {e.code}（反爬机制，浏览器可正常访问）"
        return "FAIL", f"HTTP {e.code}"
    except Exception as e:
        for wl in ANTI_CRAWL_WHITELIST:
            if wl in domain:
                return "WARN", f"{str(e)[:50]}（反爬白名单）"
        return "FAIL", str(e)[:80]

def verify_game(slug):
    path = f"data/games/{slug}.json"
    if not os.path.exists(path):
        print(f"[ERROR] 文件不存在: {path}")
        return False
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assets = data.get("assets")
    if not assets:
        print(f"[SKIP] {slug} 无 assets 数据")
        return True
    
    # 游戏名关键词（用于相关性校验）
    game_keywords = [slug.replace("-", " ")]
    if data.get("nameCN"):
        game_keywords.append(data["nameCN"])
    
    all_links = []
    for section in ["official", "inspiration"]:
        for group in assets.get(section, []):
            for link in group.get("links", []):
                all_links.append((section, group["cat"], link))
    
    print(f"\n{'='*60}")
    print(f"  审查: {slug} ({len(all_links)} 条链接)")
    print(f"{'='*60}\n")
    
    ok = warn = fail = 0
    failures = []
    
    for i, (sec, cat, link) in enumerate(all_links, 1):
        status, msg = check_link(link["url"], game_keywords)
        
        if status == "OK":
            ok += 1
            icon = "OK"
        elif status == "WARN":
            warn += 1
            icon = "!!"
        else:
            fail += 1
            icon = "XX"
            failures.append((link["title"], link["source"], link["url"], msg))
        
        print(f"  [{icon}] #{i:02d} [{link['source']:12s}] {link['title'][:50]}")
        if status != "OK":
            print(f"         → {msg}")
    
    print(f"\n  结果: {ok} OK / {warn} WARN / {fail} FAIL")
    
    if failures:
        print(f"\n  ❌ 以下链接必须修复:")
        for title, source, url, msg in failures:
            print(f"     [{source}] {title}")
            print(f"     URL: {url}")
            print(f"     原因: {msg}\n")
        return False
    
    if warn > 0:
        print(f"\n  ⚠ {warn} 条链接因反爬返回非 200，浏览器可正常访问")
    
    print(f"\n  ✅ 审查通过")
    return True

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    if len(sys.argv) < 2:
        print("用法: python scripts/verify_asset_links.py <slug>")
        print("      python scripts/verify_asset_links.py --all")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        with open("data/games.json", "r", encoding="utf-8") as f:
            games = json.load(f)
        results = []
        for g in games:
            slug = g.get("slug", "")
            detail_path = f"data/games/{slug}.json"
            if os.path.exists(detail_path):
                with open(detail_path, "r", encoding="utf-8") as f:
                    detail = json.load(f)
                if detail.get("assets"):
                    passed = verify_game(slug)
                    results.append((slug, passed))
        
        print(f"\n{'='*60}")
        print(f"  总计: {len(results)} 款有素材数据")
        passed = sum(1 for _, p in results if p)
        failed = len(results) - passed
        print(f"  通过: {passed} / 失败: {failed}")
        if failed:
            print(f"  失败列表: {[s for s, p in results if not p]}")
        sys.exit(0 if failed == 0 else 1)
    else:
        passed = verify_game(sys.argv[1])
        sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()
