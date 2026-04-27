"""
Manual slice for the new batch of 8 games (2026-04-27).
Handles home-full.webp files directly.
"""
import json
import os
from pathlib import Path
from PIL import Image

SS_DIR = Path(r"d:\ecnalClaw\output\game-platform-analysis\screenshots")
DATA_DIR = Path(r"d:\ecnalClaw\output\game-tracker-v2\data")
SLICE_HEIGHT = 1080
MIN_TAIL = 270
WEBP_QUALITY = 82
TARGET_WIDTH = 1920

SLUGS = [
    "disco-elysium", "eggy-party", "fall-guys", "genshin-impact",
    "honkai-star-rail", "zenless-zone-zero", "neverness-to-everness", "ananta"
]

# Map slug -> game name for screenshots.json
NAMES = {
    "disco-elysium": "Disco Elysium - The Final Cut",
    "eggy-party": "Eggy Party",
    "fall-guys": "Fall Guys: Ultimate Knockout",
    "genshin-impact": "Genshin Impact",
    "honkai-star-rail": "Honkai: Star Rail",
    "zenless-zone-zero": "Zenless Zone Zero",
    "neverness-to-everness": "Neverness to Everness",
    "ananta": "Ananta",
}

URLS = {
    "disco-elysium": "https://discoelysium.com",
    "eggy-party": "https://www.eggyparty.com/",
    "fall-guys": "https://www.fallguys.com/zh-CN",
    "genshin-impact": "https://ys.mihoyo.com/main/",
    "honkai-star-rail": "https://sr.mihoyo.com/main",
    "zenless-zone-zero": "https://zzz.mihoyo.com/main/",
    "neverness-to-everness": "https://nte.perfectworld.com/cn/index.html",
    "ananta": "https://ananta.163.com",
}

def process_game(slug):
    game_dir = SS_DIR / slug
    full_path = game_dir / "home-full.webp"
    
    if not full_path.exists():
        print(f"  SKIP {slug}: no home-full.webp")
        return None
    
    img = Image.open(full_path)
    w, h = img.size
    print(f"  {slug}: {w}x{h}")
    
    # If width != 1920, resize proportionally
    if w != TARGET_WIDTH:
        ratio = TARGET_WIDTH / w
        new_h = int(h * ratio)
        img = img.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
        w, h = img.size
        # Re-save the full image
        img.save(str(full_path), "WEBP", quality=WEBP_QUALITY)
        print(f"    Resized to {w}x{h}")
    
    # If height <= 1.5 * SLICE_HEIGHT, it's a single screen — no slicing needed
    if h <= SLICE_HEIGHT * 1.5:
        print(f"    Single screen ({h}px), no slicing needed")
        # Just ensure we have a home-1.webp copy
        home1 = game_dir / "home-1.webp"
        img.save(str(home1), "WEBP", quality=WEBP_QUALITY)
        imgs = [
            f"screenshots/{slug}/home-full.webp",
            f"screenshots/{slug}/home-1.webp",
        ]
        return imgs
    
    # Calculate slices
    n_full = h // SLICE_HEIGHT
    tail = h % SLICE_HEIGHT
    
    if tail > 0 and tail < MIN_TAIL and n_full > 0:
        n_slices = n_full
        merge_tail = True
    elif tail > 0:
        n_slices = n_full + 1
        merge_tail = False
    else:
        n_slices = n_full
        merge_tail = False
    
    imgs = [f"screenshots/{slug}/home-full.webp"]
    
    for i in range(n_slices):
        top = i * SLICE_HEIGHT
        if i == n_slices - 1:
            if merge_tail:
                bottom = h
            else:
                bottom = min((i + 1) * SLICE_HEIGHT, h)
        else:
            bottom = (i + 1) * SLICE_HEIGHT
        
        slice_img = img.crop((0, top, w, bottom))
        slice_name = f"home-{i+1}.webp"
        slice_path = game_dir / slice_name
        slice_img.save(str(slice_path), "WEBP", quality=WEBP_QUALITY)
        imgs.append(f"screenshots/{slug}/{slice_name}")
        print(f"    Slice {i+1}: {top}-{bottom} ({bottom-top}px)")
    
    print(f"    Total: {len(imgs)} images (1 full + {n_slices} slices)")
    return imgs


def main():
    # Load screenshots.json
    ss_json_path = DATA_DIR / "screenshots.json"
    with open(ss_json_path, "r", encoding="utf-8") as f:
        ss_data = json.load(f)
    
    for slug in SLUGS:
        print(f"\n=== {slug} ===")
        imgs = process_game(slug)
        
        if imgs is None:
            continue
        
        name = NAMES[slug]
        url = URLS[slug]
        
        # Build screenshots.json entry
        entry = [{
            "module": "Official",
            "screens": [{
                "title": f"{name} - Official",
                "url": url,
                "date": "2026-04-27",
                "tag": "长图" if len(imgs) > 2 else "最新",
                "imgs": imgs
            }]
        }]
        
        ss_data[name] = entry
        print(f"  Updated screenshots.json entry: {name}")
    
    # Write back
    with open(ss_json_path, "w", encoding="utf-8") as f:
        json.dump(ss_data, f, ensure_ascii=False, indent=2)
    
    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
