"""Convert Tier 2+3 PNGs to WebP and update screenshots.json."""
import os
import json
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS_DIR = os.path.join(BASE, "dist", "screenshots")
SCREENSHOTS_JSON = os.path.join(BASE, "data", "screenshots.json")

# Game name -> slug -> url mapping
GAMES_INFO = {
    "Stellar Blade": {"slug": "stellar-blade", "url": "https://www.playstation.com/games/stellar-blade/", "nameCN": "星刃"},
    "Resident Evil Village": {"slug": "resident-evil-village", "url": "https://www.residentevil.com/village/", "nameCN": "生化危机：村庄"},
    "Hogwarts Legacy": {"slug": "hogwarts-legacy", "url": "https://www.hogwartslegacy.com/", "nameCN": "霍格沃茨之遗"},
    "Cyberpunk 2077": {"slug": "cyberpunk-2077", "url": "https://www.cyberpunk.net", "nameCN": "赛博朋克2077"},
    "Marvel's Spider-Man Remastered": {"slug": "marvels-spider-man-remastered", "url": "https://insomniac.games/game/marvels-spider-man-remastered/", "nameCN": "漫威蜘蛛侠"},
    "Inscryption": {"slug": "inscryption", "url": "https://www.inscryption-game.com", "nameCN": "邪恶冥刻"},
    "DAVE THE DIVER": {"slug": "dave-the-diver", "url": "https://www.mintrock.et/en/", "nameCN": "潜水员戴夫"},
    "SIGNALIS": {"slug": "signalis", "url": "http://rose-engine.org/signalis/", "nameCN": "信号"},
    "Split Fiction": {"slug": "split-fiction", "url": "https://www.ea.com/games/split-fiction", "nameCN": "分裂虚构"},
    "Days Gone": {"slug": "days-gone", "url": "https://www.playstation.com/games/days-gone/", "nameCN": "往日不再"},
    "Balatro": {"slug": "balatro", "url": "https://www.playbalatro.com/", "nameCN": "小丑牌"},
    "Cult of the Lamb": {"slug": "cult-of-the-lamb", "url": "https://massivemonster.com/games/cult-of-the-lamb", "nameCN": "咩咩启示录"},
    "DREDGE": {"slug": "dredge", "url": "https://www.dredge.game/", "nameCN": "疏浚"},
    "Satisfactory": {"slug": "satisfactory", "url": "https://www.satisfactorygame.com/", "nameCN": "幸福工厂"},
    "Teardown": {"slug": "teardown", "url": "http://teardowngame.com", "nameCN": "拆迁"},
}

def convert_pngs():
    """Convert all PNGs to WebP for Tier 2+3 games."""
    converted = []
    for name, info in GAMES_INFO.items():
        slug = info["slug"]
        game_dir = os.path.join(SS_DIR, slug)
        png_path = os.path.join(game_dir, "home-1.png")
        webp_path = os.path.join(game_dir, "home-1.webp")

        if os.path.exists(png_path):
            try:
                img = Image.open(png_path)
                img.save(webp_path, "WEBP", quality=82)
                png_size = os.path.getsize(png_path)
                webp_size = os.path.getsize(webp_path)
                ratio = webp_size / png_size * 100
                print(f"  {slug}: {png_size/1024:.0f}KB -> {webp_size/1024:.0f}KB ({ratio:.0f}%)")
                # Remove PNG after successful conversion
                os.remove(png_path)
                converted.append(slug)
            except Exception as e:
                print(f"  {slug}: ERROR - {e}")
        elif os.path.exists(webp_path):
            print(f"  {slug}: already WebP")
            converted.append(slug)
        else:
            print(f"  {slug}: NO FILE FOUND")

    return converted


def update_screenshots_json():
    """Add Tier 2+3 entries to screenshots.json."""
    with open(SCREENSHOTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = "2026-04-23"
    added = 0

    for name, info in GAMES_INFO.items():
        slug = info["slug"]
        webp_path = os.path.join(SS_DIR, slug, "home-1.webp")
        if not os.path.exists(webp_path):
            print(f"  SKIP {name} - no webp")
            continue

        if name in data:
            print(f"  EXISTS {name}")
            continue

        data[name] = [
            {
                "module": "Official",
                "screens": [
                    {
                        "title": f"{info['nameCN']} - Official",
                        "url": info["url"],
                        "date": today,
                        "tag": "最新",
                        "imgs": [f"screenshots/{slug}/home-1.webp"]
                    }
                ]
            }
        ]
        print(f"  ADDED {name}")
        added += 1

    with open(SCREENSHOTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nTotal added to screenshots.json: {added}")


if __name__ == "__main__":
    print("=== Converting PNGs to WebP ===")
    converted = convert_pngs()
    print(f"\nConverted: {len(converted)} games")

    print("\n=== Updating screenshots.json ===")
    update_screenshots_json()
