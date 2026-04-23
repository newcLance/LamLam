"""Robust batch screenshot for Tier 1 games."""
import subprocess, os, json, time, shutil, sys
from pathlib import Path

BASE = Path("d:/ecnalClaw/output/game-tracker-v2")
DIST_SS = BASE / "dist" / "screenshots"
SRC_SS = BASE.parent / "game-platform-analysis" / "screenshots"

TARGETS = [
    ("baldurs-gate-3", "Baldur's Gate 3", "https://baldursgate3.game/"),
    ("god-of-war", "God of War", "https://www.playstation.com/en-us/god-of-war/"),
    ("ghost-of-tsushima", "Ghost of Tsushima DIRECTOR'S CUT", "https://www.playstation.com/en-us/games/ghost-of-tsushima/pc/"),
    ("silent-hill-2", "SILENT HILL 2", "https://www.konami.com/games/silenthill/2r/"),
    ("hollow-knight-silksong", "Hollow Knight: Silksong", "https://hollowknightsilksong.com/"),
    ("hades-2", "Hades II", "https://www.supergiantgames.com/games/hades-ii/"),
    ("persona-5-royal", "Persona 5 Royal", "https://www.atlus.com/p5r"),
    ("hi-fi-rush", "Hi-Fi RUSH", "https://hifirush.com"),
    ("kingdom-come-deliverance-2", "Kingdom Come: Deliverance II", "https://www.deepsilver.com/games/kingdom-come-deliverance-ii"),
    ("stray", "Stray", "https://stray.game"),
]

def run(cmd, timeout=25):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, r.stdout
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)

def main():
    # Pre-create all directories
    for slug, _, _ in TARGETS:
        (DIST_SS / slug).mkdir(parents=True, exist_ok=True)
        (SRC_SS / slug).mkdir(parents=True, exist_ok=True)

    # Check what's already done
    done = set()
    for slug, _, _ in TARGETS:
        webp = DIST_SS / slug / "home-1.webp"
        if webp.exists() and webp.stat().st_size > 5000:
            done.add(slug)
            print(f"[SKIP] {slug} - already done ({webp.stat().st_size // 1024}KB)")

    # Setup browser
    run("agent-browser close", timeout=5)
    run("agent-browser set viewport 1920 1080")

    results = {}
    for slug, name, url in TARGETS:
        if slug in done:
            results[slug] = "SKIP"
            continue

        print(f"\n[{slug}] Opening {url}...")
        ok, out = run(f'agent-browser open "{url}" --timeout 15000', timeout=20)
        if not ok:
            print(f"  FAIL: open - {out[:80]}")
            results[slug] = "FAIL_OPEN"
            continue

        time.sleep(4)

        # Dismiss popups
        run('agent-browser eval "document.querySelectorAll(\'[id*=cookie] button, [class*=accept] button, #onetrust-accept-btn-handler, .cmpboxbtn, .cc-btn\').forEach(function(b){b.click()})"', timeout=5)
        time.sleep(1)

        png_path = str(DIST_SS / slug / "home-1.png")
        print(f"  Screenshotting...")
        ok, out = run(f'agent-browser screenshot "{png_path}" --full', timeout=20)

        if not ok or not os.path.exists(png_path) or os.path.getsize(png_path) < 5000:
            print(f"  FAIL: screenshot - {out[:80] if not ok else 'file too small'}")
            results[slug] = "FAIL_SS"
            continue

        # Convert to WebP
        try:
            from PIL import Image
            img = Image.open(png_path)
            webp_path = str(DIST_SS / slug / "home-1.webp")
            img.save(webp_path, "webp", quality=82)
            os.remove(png_path)
            shutil.copy2(webp_path, str(SRC_SS / slug / "home-1.webp"))
            kb = os.path.getsize(webp_path) // 1024
            print(f"  OK: home-1.webp ({kb}KB)")
            results[slug] = "OK"
        except Exception as e:
            print(f"  FAIL: convert - {e}")
            results[slug] = "FAIL_CONVERT"

    # Update screenshots.json
    with open(str(BASE / "data" / "screenshots.json"), "r", encoding="utf-8") as f:
        ss_data = json.load(f)

    for slug, name, url in TARGETS:
        webp = DIST_SS / slug / "home-1.webp"
        if webp.exists() and webp.stat().st_size > 5000:
            ss_data[name] = [{
                "module": "官网",
                "screens": [{
                    "title": f"{name} - Official",
                    "url": url,
                    "date": "2026-04-23",
                    "tag": "最新",
                    "imgs": [f"screenshots/{slug}/home-1.webp"]
                }]
            }]

    with open(str(BASE / "data" / "screenshots.json"), "w", encoding="utf-8") as f:
        json.dump(ss_data, f, ensure_ascii=False, indent=2)

    run("agent-browser close", timeout=5)

    print(f"\n{'='*40}")
    print("RESULTS:")
    for slug, status in results.items():
        print(f"  {slug}: {status}")
    ok_count = sum(1 for v in results.values() if v in ("OK", "SKIP"))
    print(f"\n{ok_count}/{len(TARGETS)} successful")

if __name__ == "__main__":
    main()
