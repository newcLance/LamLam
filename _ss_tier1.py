"""Batch screenshot Tier 1 games."""
import subprocess, os, json, time, shutil
from pathlib import Path
from PIL import Image

DIST_SS = Path("dist/screenshots")
SRC_SS = Path("..") / "game-platform-analysis" / "screenshots"

TARGETS = [
    ("baldurs-gate-3", "Baldur's Gate 3", [
        ("https://baldursgate3.game/", "home"),
        ("https://baldursgate3.game/about/", "about"),
    ]),
    ("god-of-war", "God of War", [
        ("https://www.playstation.com/god-of-war/", "home"),
    ]),
    ("ghost-of-tsushima", "Ghost of Tsushima DIRECTOR'S CUT", [
        ("https://www.playstation.com/en-us/games/ghost-of-tsushima/pc/", "home"),
    ]),
    ("silent-hill-2", "SILENT HILL 2", [
        ("https://www.konami.com/games/silenthill/2r/", "home"),
    ]),
    ("hollow-knight-silksong", "Hollow Knight: Silksong", [
        ("https://hollowknightsilksong.com/", "home"),
    ]),
    ("hades-2", "Hades II", [
        ("http://www.supergiantgames.com/games/hades-ii/", "home"),
    ]),
    ("persona-5-royal", "Persona 5 Royal", [
        ("https://www.atlus.com/p5r", "home"),
    ]),
    ("hi-fi-rush", "Hi-Fi RUSH", [
        ("https://hifirush.com", "home"),
    ]),
    ("kingdom-come-deliverance-2", "Kingdom Come: Deliverance II", [
        ("https://www.deepsilver.com/games/kingdom-come-deliverance-ii", "home"),
    ]),
    ("stray", "Stray", [
        ("https://stray.game", "home"),
    ]),
]

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except:
        return False

def dismiss_popups():
    """Try to dismiss cookie/age/consent popups."""
    js = """(function(){
        var sels = [
            '[class*=cookie] button[class*=accept]',
            '[class*=cookie] button[class*=agree]',
            '#onetrust-accept-btn-handler',
            '.cmpboxbtn',
            '[class*=consent] button',
            'button[class*=accept]',
            '[data-testid=cookie-accept]',
            '.cc-btn.cc-allow',
            '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
        ];
        sels.forEach(function(s){
            var el = document.querySelector(s);
            if(el) el.click();
        });
        return 'ok';
    })()"""
    run('agent-browser eval "' + js.replace('"', '\\"') + '"')

def screenshot_page(slug, url, prefix):
    out_dir = DIST_SS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    src_dir = SRC_SS / slug
    src_dir.mkdir(parents=True, exist_ok=True)

    print(f"  Opening {url}")
    if not run(f'agent-browser open "{url}" --timeout 20000'):
        print(f"  FAIL: could not open")
        return None

    time.sleep(4)
    dismiss_popups()
    time.sleep(1)

    png = str(out_dir / f"{prefix}-1.png")
    print(f"  Taking screenshot...")
    run(f'agent-browser screenshot "{png}" --full')

    if not os.path.exists(png) or os.path.getsize(png) < 5000:
        print(f"  FAIL: screenshot empty/missing")
        return None

    # Convert to WebP
    webp = str(out_dir / f"{prefix}-1.webp")
    try:
        img = Image.open(png)
        img.save(webp, "webp", quality=82)
        os.remove(png)
        shutil.copy2(webp, str(src_dir / f"{prefix}-1.webp"))
        kb = os.path.getsize(webp) // 1024
        print(f"  OK: {prefix}-1.webp ({kb}KB)")
        return f"screenshots/{slug}/{prefix}-1.webp"
    except Exception as e:
        print(f"  WARN: convert failed: {e}")
        return None

def main():
    run("agent-browser set viewport 1920 1080")

    with open("data/screenshots.json", "r", encoding="utf-8") as f:
        ss_data = json.load(f)

    for slug, game_name, pages in TARGETS:
        print(f"\n{'='*60}")
        print(f"  {game_name} ({slug})")
        print(f"{'='*60}")

        all_imgs = []
        screens = []
        for url, prefix in pages:
            img_path = screenshot_page(slug, url, prefix)
            if img_path:
                all_imgs.append(img_path)
                screens.append({
                    "title": f"{game_name} - Official",
                    "url": url,
                    "date": "2026-04-23",
                    "tag": "最新" if prefix == "home" else "",
                    "imgs": [img_path]
                })

        if screens:
            ss_data[game_name] = [{"module": "官网", "screens": screens}]
            print(f"  => {len(all_imgs)} screenshots saved")
        else:
            print(f"  => FAILED - no screenshots")

    with open("data/screenshots.json", "w", encoding="utf-8") as f:
        json.dump(ss_data, f, ensure_ascii=False, indent=2)

    run("agent-browser close")
    print(f"\nAll done!")

if __name__ == "__main__":
    main()
