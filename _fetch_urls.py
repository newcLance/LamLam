"""Fetch official website URLs from Steam store API for Tier 1 games."""
import json, urllib.request, time, ssl

# Steam App IDs for Tier 1 games
GAMES = {
    "baldurs-gate-3":              1086940,
    "god-of-war":                  1593500,
    "ghost-of-tsushima":           2215430,
    "silent-hill-2":               2124490,
    "hollow-knight-silksong":      1030300,
    "hades-2":                     1145350,
    "persona-5-royal":             1687950,
    "hi-fi-rush":                  1817230,
    "kingdom-come-deliverance-2":  2611710,
    "stray":                       1332010,
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = {}
for slug, appid in GAMES.items():
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&l=schinese"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = json.loads(resp.read())
        app_data = data.get(str(appid), {}).get("data", {})
        website = app_data.get("website", "")
        name = app_data.get("name", slug)
        developers = app_data.get("developers", [])
        publishers = app_data.get("publishers", [])
        print(f"{slug}: {website or '(none)'} | Dev: {', '.join(developers)} | Pub: {', '.join(publishers)}")
        results[slug] = {
            "name": name,
            "website": website,
            "developers": developers,
            "publishers": publishers
        }
    except Exception as e:
        print(f"{slug}: ERROR - {e}")
        results[slug] = {"website": "", "error": str(e)}
    time.sleep(0.5)

print("\n=== Summary ===")
for slug, info in results.items():
    w = info.get("website", "")
    status = "OK" if w else "MISSING"
    print(f"  [{status}] {slug}: {w}")
