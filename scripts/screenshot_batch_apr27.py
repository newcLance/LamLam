"""
Batch screenshot script for 8 new games (2026-04-27).
Takes full-page screenshots at 1920x1080 viewport, saves as PNG,
then converts to WebP. Screenshots go to game-platform-analysis/screenshots/{slug}/.
"""
import asyncio
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SS_DIR = Path(r"d:\ecnalClaw\output\game-platform-analysis\screenshots")

GAMES = [
    ("disco-elysium", "https://discoelysium.com", "极乐迪斯科"),
    ("eggy-party", "https://eggyparty.163.com/m/", "蛋仔派对"),
    ("fall-guys", "https://www.fallguys.com/zh-CN", "糖豆人"),
    ("genshin-impact", "https://ys.mihoyo.com/main/", "原神"),
    ("honkai-star-rail", "https://sr.mihoyo.com/main", "星穹铁道"),
    ("zenless-zone-zero", "https://zzz.mihoyo.com/main/", "绝区零"),
    ("neverness-to-everness", "https://nte.perfectworld.com/cn/index.html", "异环"),
    ("ananta", "https://ananta.163.com", "无限大"),
]


async def dismiss_overlays(page):
    """Try to dismiss cookie banners, age gates, and other overlays."""
    selectors = [
        'button:has-text("Accept")',
        'button:has-text("Accept All")',
        'button:has-text("Accept Cookies")',
        'button:has-text("I Accept")',
        'button:has-text("Got it")',
        'button:has-text("OK")',
        'button:has-text("Agree")',
        'button:has-text("Continue")',
        'button:has-text("Allow")',
        'button:has-text("Allow All")',
        'button:has-text("接受")',
        'button:has-text("同意")',
        'button:has-text("确定")',
        'button:has-text("我已年满")',
        'button:has-text("进入")',
        'button:has-text("Yes")',
        'button:has-text("Enter")',
        'a:has-text("Yes")',
        '#onetrust-accept-btn-handler',
        '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
        '[data-testid="cookie-accept"]',
        '.cookie-accept',
        '.cc-accept',
        '.js-cookie-accept',
        # Close buttons for modals
        'button[aria-label="Close"]',
        'button[aria-label="关闭"]',
        '.modal-close',
        '.popup-close',
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=500):
                await el.click()
                await page.wait_for_timeout(800)
        except Exception:
            pass


async def screenshot_game(browser, slug, url, name_cn, idx, total):
    """Take a full-page screenshot for one game."""
    out_dir = SS_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "home-full.png"

    # Skip if already has a good full webp
    webp_path = out_dir / "home-full.webp"
    if webp_path.exists() and webp_path.stat().st_size > 50000:
        print(f"[{idx}/{total}] SKIP {name_cn} ({slug}) - already has webp ({webp_path.stat().st_size:,} bytes)")
        return True

    print(f"[{idx}/{total}] Screenshotting {name_cn} ({slug}): {url}")
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        locale="zh-CN",
    )
    page = await context.new_page()
    try:
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=45000)
        status = resp.status if resp else "N/A"
        print(f"  HTTP status: {status}")

        # Wait for lazy-loaded content
        await page.wait_for_timeout(5000)

        # Dismiss overlays
        await dismiss_overlays(page)
        await page.wait_for_timeout(1000)

        # Auto-scroll to trigger lazy loading
        await page.evaluate("""() => {
            return new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 500;
                const timer = setInterval(() => {
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= document.body.scrollHeight) {
                        clearInterval(timer);
                        window.scrollTo(0, 0);
                        resolve();
                    }
                }, 200);
            });
        }""")
        await page.wait_for_timeout(3000)

        # Dismiss overlays again (some appear after scroll)
        await dismiss_overlays(page)
        await page.wait_for_timeout(500)

        # Take full-page screenshot
        await page.screenshot(path=str(out_path), full_page=True, timeout=60000)
        size = out_path.stat().st_size
        print(f"  -> Saved PNG ({size:,} bytes)")

        if size < 50000:
            print(f"  !! WARNING: Screenshot suspiciously small")
            return False

        return True
    except Exception as e:
        print(f"  !! ERROR: {e}")
        return False
    finally:
        await context.close()


async def main():
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        total = len(GAMES)
        results = {}

        for idx, (slug, url, name_cn) in enumerate(GAMES, 1):
            ok = await screenshot_game(browser, slug, url, name_cn, idx, total)
            results[slug] = ok

        await browser.close()

    # Convert PNGs to WebP
    print("\n--- Converting to WebP ---")
    try:
        from PIL import Image
        for slug, ok in results.items():
            if not ok:
                continue
            png_path = SS_DIR / slug / "home-full.png"
            webp_path = SS_DIR / slug / "home-full.webp"
            if png_path.exists():
                img = Image.open(png_path)
                img.save(str(webp_path), "WEBP", quality=82)
                webp_size = webp_path.stat().st_size
                print(f"  {slug}: {webp_size:,} bytes WebP")
                png_path.unlink()  # Remove PNG after conversion
    except ImportError:
        print("  PIL not available, skipping WebP conversion")

    # Summary
    print("\n--- Summary ---")
    success = sum(1 for v in results.values() if v)
    print(f"Success: {success}/{total}")
    for slug, ok in results.items():
        status = "OK" if ok else "FAIL"
        print(f"  {status}: {slug}")


if __name__ == "__main__":
    asyncio.run(main())
