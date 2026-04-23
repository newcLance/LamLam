#!/usr/bin/env python3
"""
全页长图切割脚本 — Game Design Tracker 生产管线
================================================
功能：
  1. 读入全页长截图（PNG 或 WebP）
  2. 保留原长图作为第一张（打 "长图" 标签）
  3. 按 16:9 一屏（1920×1080）高度切割成 N 张子图
  4. 所有输出统一为 WebP (quality=82)
  5. 自动更新 data/screenshots.json

用法：
  python scripts/slice-fullpage.py --slug sekiro --page home
  python scripts/slice-fullpage.py --slug sekiro --page home --source story
  python scripts/slice-fullpage.py --slug sekiro              # 处理该游戏目录下所有长图
  python scripts/slice-fullpage.py --all                      # 处理所有游戏
  python scripts/slice-fullpage.py --slug sekiro --dry-run    # 预览，不执行

切割规则：
  - viewport 宽度 = 1920px → 16:9 一屏高度 = 1080px
  - 末尾残余高度 ≥ 270px（一屏的 25%）才保留为独立切片
  - 末尾残余高度 < 270px 时并入上一张切片（允许该切片略超一屏）

命名规范：
  screenshots/{slug}/home-full.webp      ← 长图原图（打 tag: 长图）
  screenshots/{slug}/home-1.webp         ← 第 1 屏切片
  screenshots/{slug}/home-2.webp         ← 第 2 屏切片
  ...
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOTS_SRC = ROOT.parent / "game-platform-analysis" / "screenshots"
DATA = ROOT / "data"
WEBP_QUALITY = 82
VIEWPORT_WIDTH = 1920
SLICE_HEIGHT = 1080  # 16:9 at 1920px width
MIN_TAIL = SLICE_HEIGHT // 4  # 270px — minimum tail height to keep as separate slice


def find_fullpage_images(game_dir: Path):
    """Find candidate full-page screenshots in a game directory.

    A full-page image is any image whose height > 1.5× SLICE_HEIGHT (i.e., taller than
    one and a half screens). This catches both existing long images and newly captured ones.

    Returns list of (page_prefix, source_path) tuples.
    e.g. [("home", Path(".../home-1.webp")), ("story", Path(".../story-1.webp"))]
    """
    candidates = []
    if not game_dir.exists():
        return candidates

    for f in sorted(game_dir.iterdir()):
        if not f.is_file():
            continue
        if f.suffix.lower() not in (".webp", ".png", ".jpg", ".jpeg"):
            continue
        # Skip already-sliced files (e.g., home-full.webp)
        if "-full" in f.stem:
            continue

        try:
            with Image.open(f) as img:
                w, h = img.size
                if h > SLICE_HEIGHT * 1.5:
                    # Extract page prefix: "home-1.webp" → "home"
                    stem = f.stem
                    # Remove trailing "-N" number
                    parts = stem.rsplit("-", 1)
                    if len(parts) == 2 and parts[1].isdigit():
                        prefix = parts[0]
                    else:
                        prefix = stem
                    candidates.append((prefix, f))
        except Exception:
            continue

    return candidates


def slice_image(src_path: Path, game_dir: Path, prefix: str, dry_run: bool = False):
    """Slice a full-page image into 16:9 screens.

    Returns:
        list of output file paths (relative to SCREENSHOTS_SRC parent),
        or None on failure.
        First item is always the full-page image.
    """
    img = Image.open(src_path)
    w, h = img.size

    # Calculate number of slices
    n_full = h // SLICE_HEIGHT
    tail = h % SLICE_HEIGHT

    # Handle tail
    if tail > 0 and tail < MIN_TAIL and n_full > 0:
        # Merge tail into last slice
        n_slices = n_full  # last slice will be taller
        merge_tail = True
    elif tail > 0:
        n_slices = n_full + 1
        merge_tail = False
    else:
        n_slices = n_full
        merge_tail = False

    if n_slices <= 1:
        # Not worth slicing — only one screen
        print(f"    SKIP {src_path.name}: only {n_slices} screen ({w}×{h}), not slicing")
        return None

    print(f"    {src_path.name}: {w}×{h} → {n_slices} slices" +
          (f" (tail {tail}px merged)" if merge_tail else f" (tail {tail}px)" if tail else ""))

    if dry_run:
        return ["(dry-run)"] * (n_slices + 1)

    outputs = []

    # 1. Save full-page image as {prefix}-full.webp
    full_path = game_dir / f"{prefix}-full.webp"
    if src_path.suffix.lower() == ".webp" and src_path != full_path:
        # Just copy/rename
        import shutil
        shutil.copy2(src_path, full_path)
    else:
        img.save(full_path, "WEBP", quality=WEBP_QUALITY, method=5)
    outputs.append(full_path)

    # 2. Slice into individual screens
    for i in range(n_slices):
        top = i * SLICE_HEIGHT
        if i == n_slices - 1 and merge_tail:
            bottom = h  # Last slice includes merged tail
        elif i == n_slices - 1 and tail > 0:
            bottom = h  # Last slice is the tail
        else:
            bottom = top + SLICE_HEIGHT

        slice_img = img.crop((0, top, w, bottom))
        slice_path = game_dir / f"{prefix}-{i + 1}.webp"
        slice_img.save(slice_path, "WEBP", quality=WEBP_QUALITY, method=5)
        outputs.append(slice_path)
        slice_img.close()

    # 3. Remove the original source if it's different from the full output
    if src_path != full_path and src_path.exists():
        src_path.unlink()
        print(f"    Removed original: {src_path.name}")

    img.close()
    return outputs


def update_screenshots_json(slug: str, prefix: str, outputs: list, url: str = "", date: str = ""):
    """Update data/screenshots.json with sliced images.

    The first image (full-page) gets tag "长图".
    """
    import datetime
    if not date:
        date = datetime.date.today().isoformat()

    ss_path = DATA / "screenshots.json"
    data = {}
    if ss_path.exists():
        data = json.loads(ss_path.read_text("utf-8"))

    # Build relative img paths: "screenshots/{slug}/{filename}"
    imgs = []
    for p in outputs:
        rel = f"screenshots/{slug}/{p.name}"
        imgs.append(rel)

    # Find the game name key in screenshots.json that uses this slug
    game_name = None
    for name, modules in data.items():
        for m in modules:
            for s in m.get("screens", []):
                for img_path in s.get("imgs", []):
                    if f"screenshots/{slug}/" in img_path:
                        game_name = name
                        break
                if game_name:
                    break
            if game_name:
                break
        if game_name:
            break

    if not game_name:
        print(f"    WARN: No existing entry found for slug '{slug}' in screenshots.json")
        print(f"    You'll need to add it manually or re-run after adding the game.")
        return False

    # Find the matching screen entry and update it
    updated = False
    for m in data[game_name]:
        for s in m.get("screens", []):
            # Match by prefix in img paths
            if s.get("imgs") and any(f"/{prefix}-" in img or f"/{prefix}." in img for img in s["imgs"]):
                s["imgs"] = imgs
                s["tag"] = "长图"
                s["date"] = date
                updated = True
                break
        if updated:
            break

    if not updated:
        # If no existing screen matched, update the first screen
        if data[game_name] and data[game_name][0].get("screens"):
            s = data[game_name][0]["screens"][0]
            s["imgs"] = imgs
            s["tag"] = "长图"
            s["date"] = date
            updated = True

    if updated:
        ss_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
        print(f"    Updated screenshots.json: {game_name} → {len(imgs)} images (tag: 长图)")

    return updated


def process_game(slug: str, page_filter: str = None, dry_run: bool = False):
    """Process all full-page images for a single game."""
    game_dir = SCREENSHOTS_SRC / slug
    if not game_dir.exists():
        print(f"  SKIP {slug}: directory not found at {game_dir}")
        return 0

    candidates = find_fullpage_images(game_dir)
    if page_filter:
        candidates = [(p, f) for p, f in candidates if p == page_filter]

    if not candidates:
        print(f"  SKIP {slug}: no full-page images found" +
              (f" matching '{page_filter}'" if page_filter else ""))
        return 0

    count = 0
    for prefix, src_path in candidates:
        outputs = slice_image(src_path, game_dir, prefix, dry_run)
        if outputs and not dry_run:
            update_screenshots_json(slug, prefix, [Path(o) for o in outputs if isinstance(o, Path)])
            count += 1
        elif outputs:
            count += 1

    return count


def get_all_slugs():
    """Get all game slugs from the screenshots source directory."""
    if not SCREENSHOTS_SRC.exists():
        return []
    return sorted(d.name for d in SCREENSHOTS_SRC.iterdir() if d.is_dir())


def main():
    parser = argparse.ArgumentParser(description="Slice full-page screenshots into 16:9 screens")
    parser.add_argument("--slug", help="Game slug to process (e.g., 'sekiro')")
    parser.add_argument("--page", help="Page prefix to process (e.g., 'home', 'story'). Default: all pages")
    parser.add_argument("--all", action="store_true", help="Process all games")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    args = parser.parse_args()

    if not args.slug and not args.all:
        parser.error("Must specify --slug or --all")

    print(f"{'[DRY RUN] ' if args.dry_run else ''}=== Slice Full-Page Screenshots ===")
    print(f"Source: {SCREENSHOTS_SRC}")
    print(f"Slice height: {SLICE_HEIGHT}px (16:9 at {VIEWPORT_WIDTH}px)")
    print(f"Min tail: {MIN_TAIL}px\n")

    total = 0
    if args.all:
        slugs = get_all_slugs()
        print(f"Processing {len(slugs)} game directories...\n")
        for slug in slugs:
            n = process_game(slug, args.page, args.dry_run)
            total += n
    else:
        total = process_game(args.slug, args.page, args.dry_run)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}=== Done! {total} images sliced ===")
    if total and not args.dry_run:
        print("Run `python build.py` to rebuild the site.")


if __name__ == "__main__":
    main()
