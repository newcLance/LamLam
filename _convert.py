from PIL import Image
import json, os, shutil

base = "dist/screenshots"
src_base = "../game-platform-analysis/screenshots"

targets = {
    "baldurs-gate-3": ("Baldur's Gate 3", "https://baldursgate3.game/"),
    "god-of-war": ("God of War", "https://www.playstation.com/en-us/god-of-war/"),
    "ghost-of-tsushima": ("Ghost of Tsushima DIRECTOR'S CUT", "https://www.playstation.com/en-us/games/ghost-of-tsushima/pc/"),
    "silent-hill-2": ("SILENT HILL 2", "https://www.konami.com/games/silenthill/2r/"),
    "hollow-knight-silksong": ("Hollow Knight: Silksong", "https://hollowknightsilksong.com/"),
    "hades-2": ("Hades II", "https://www.supergiantgames.com/games/hades-ii/"),
    "persona-5-royal": ("Persona 5 Royal", "https://asia.sega.com/persona-remaster/p5r/cn/"),
    "hi-fi-rush": ("Hi-Fi RUSH", "https://hifirush.krafton.com/"),
    "kingdom-come-deliverance-2": ("Kingdom Come: Deliverance II", "https://www.deepsilver.com/games/kingdom-come-deliverance-ii"),
    "stray": ("Stray", "https://annapurnainteractive.com/games/stray"),
}

for slug, (name, url) in targets.items():
    png = os.path.join(base, slug, "home-1.png")
    webp = os.path.join(base, slug, "home-1.webp")
    if os.path.exists(png):
        sz = os.path.getsize(png)
        if sz < 3000:
            print(f"  SKIP {slug}: too small ({sz}B)")
            continue
        img = Image.open(png)
        img.save(webp, "webp", quality=82)
        os.remove(png)
        src_dir = os.path.join(src_base, slug)
        os.makedirs(src_dir, exist_ok=True)
        shutil.copy2(webp, os.path.join(src_dir, "home-1.webp"))
        print(f"  CONVERTED {slug}: {os.path.getsize(webp)//1024}KB")
    elif os.path.exists(webp):
        print(f"  EXISTS {slug}: {os.path.getsize(webp)//1024}KB")
    else:
        print(f"  MISSING {slug}")

# Update screenshots.json
with open("data/screenshots.json", "r", encoding="utf-8") as f:
    ss = json.load(f)

for slug, (name, url) in targets.items():
    webp_path = os.path.join(base, slug, "home-1.webp")
    if os.path.exists(webp_path) and os.path.getsize(webp_path) > 5000:
        ss[name] = [{
            "module": "Official",
            "screens": [{
                "title": f"{name} - Official",
                "url": url,
                "date": "2026-04-23",
                "tag": "最新",
                "imgs": [f"screenshots/{slug}/home-1.webp"]
            }]
        }]
        print(f"  JSON {slug}: updated")

with open("data/screenshots.json", "w", encoding="utf-8") as f:
    json.dump(ss, f, ensure_ascii=False, indent=2)

print("\nDone!")
