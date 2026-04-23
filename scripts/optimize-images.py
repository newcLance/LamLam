#!/usr/bin/env python3
"""
图片标准化脚本 — Game Design Tracker 生产管线
===============================================
功能：
  1. 扫描 screenshots/ 目录，将所有 PNG/JPG 转为 WebP
  2. 保留原目录结构，原文件删除（可加 --keep 保留）
  3. 同步更新 data/screenshots.json 中的路径引用
  4. 输出压缩报告

用法：
  python scripts/optimize-images.py                # 转换全部
  python scripts/optimize-images.py --dir sekiro   # 只处理指定子目录
  python scripts/optimize-images.py --keep         # 转换后保留原文件
  python scripts/optimize-images.py --quality 85   # 调整质量 (默认 82)
  python scripts/optimize-images.py --dry-run      # 仅预览，不执行

标准参数：WebP quality=82, method=5 (高压缩效率)
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
SCREENSHOTS = ROOT.parent / "game-platform-analysis" / "screenshots"
DATA = ROOT / "data"


def convert_image(src: Path, quality: int, keep: bool, dry_run: bool):
    """Convert a single PNG/JPG to WebP. Returns (new_path, saved_bytes, action) or None."""
    if src.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        return None

    dst = src.with_suffix(".webp")
    old_size = src.stat().st_size

    # Case 1: WebP already exists → just clean up the redundant original
    if dst.exists():
        saved = old_size  # removing the original entirely
        if not dry_run and not keep:
            src.unlink()
        return (dst, saved, "cleaned")

    # Case 2: Convert to WebP
    if dry_run:
        ratio = 0.4 if src.suffix.lower() == ".png" else 0.8
        est_size = int(old_size * ratio)
        return (dst, old_size - est_size, "convert")

    try:
        img = Image.open(src)
        img.save(dst, "WEBP", quality=quality, method=5)
        new_size = dst.stat().st_size
        if not keep:
            src.unlink()
        return (dst, old_size - new_size, "convert")
    except Exception as e:
        print(f"  WARN: Failed to convert {src.name}: {e}")
        if dst.exists():
            dst.unlink()
        return None


def update_screenshots_json(conversions: dict):
    """Update path references in screenshots.json: .png/.jpg → .webp"""
    ss_path = DATA / "screenshots.json"
    if not ss_path.exists():
        return 0

    text = ss_path.read_text("utf-8")
    count = 0
    for old_name, new_name in conversions.items():
        if old_name in text:
            text = text.replace(old_name, new_name)
            count += 1

    ss_path.write_text(text, "utf-8")
    return count


def main():
    parser = argparse.ArgumentParser(description="Screenshot optimizer for Game Tracker")
    parser.add_argument("--dir", help="Only process a specific subdirectory under screenshots/")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality (default: 82)")
    parser.add_argument("--keep", action="store_true", help="Keep original files after conversion")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no changes")
    args = parser.parse_args()

    target = SCREENSHOTS / args.dir if args.dir else SCREENSHOTS
    if not target.exists():
        print(f"ERROR: {target} does not exist")
        sys.exit(1)

    print(f"{'[DRY RUN] ' if args.dry_run else ''}Scanning: {target}")
    print(f"Quality: {args.quality}, Keep originals: {args.keep}\n")

    candidates = sorted(target.rglob("*"))
    candidates = [f for f in candidates if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg")]

    if not candidates:
        print("No PNG/JPG files found. All good!")
        return

    print(f"Found {len(candidates)} files to convert:\n")

    total_saved = 0
    converted = 0
    cleaned = 0
    conversions = {}  # old_filename -> new_filename for JSON update

    for f in candidates:
        result = convert_image(f, args.quality, args.keep, args.dry_run)
        if result:
            new_path, saved, action = result
            total_saved += saved
            rel = f.relative_to(SCREENSHOTS)
            new_rel = new_path.relative_to(SCREENSHOTS)
            old_ref = str(rel).replace("\\", "/")
            new_ref = str(new_rel).replace("\\", "/")
            conversions[old_ref] = new_ref
            saved_kb = saved / 1024
            if action == "cleaned":
                cleaned += 1
                print(f"  [clean] {rel}  (webp exists, removed original: -{saved_kb:.0f} KB)")
            else:
                converted += 1
                print(f"  {'→' if not args.dry_run else '~'} {rel} → .webp  (-{saved_kb:.0f} KB)")

    # Update JSON references
    json_updates = 0
    if conversions and not args.dry_run:
        json_updates = update_screenshots_json(conversions)

    # Report
    print(f"\n{'═' * 50}")
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Summary:")
    print(f"  Converted:  {converted} files")
    print(f"  Cleaned:    {cleaned} redundant originals")
    print(f"  Saved:      {total_saved / 1024 / 1024:.1f} MB")
    if json_updates:
        print(f"  JSON refs:  {json_updates} paths updated")
    if not args.dry_run and (converted or cleaned):
        print(f"\n  >> Done! Run `python build.py` to rebuild the site.")
    print()


if __name__ == "__main__":
    main()
