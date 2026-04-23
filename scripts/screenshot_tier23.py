"""
Tier 2+3 batch screenshot script.
Takes a full-page screenshot of each game's official website,
saves as PNG in dist/screenshots/{slug}/home-1.png.
Then converts all PNGs to WebP (quality=82).
"""
import asyncio
import os
import sys

# --- Config ---
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS_DIR = os.path.join(BASE, "dist", "screenshots")

GAMES = [
    # (slug, url, name_cn)
    ("stellar-blade", "https://www.playstation.com/games/stellar-blade/", "星刃"),
    ("resident-evil-village", "https://www.residentevil.com/village/", "生化危机：村庄"),
    ("hogwarts-legacy", "https://www.hogwartslegacy.com/", "霍格沃茨之遗"),
    ("cyberpunk-2077", "https://www.cyberpunk.net", "赛博朋克2077"),
    ("marvels-spider-man-remastered", "https://insomniac.games/game/marvels-spider-man-remastered/", "漫威蜘蛛侠"),
    ("inscryption", "https://www.inscryption-game.com", "邪恶冥刻"),
    ("dave-the-diver", "https://mintrocket.co.kr/davethediver", "潜水员戴夫"),
    ("signalis", "http://rose-engine.org/signalis/", "信号"),
    ("split-fiction", "https://www.ea.com/games/split-fiction", "分裂虚构"),
    ("days-gone", "https://www.playstation.com/games/days-gone/", "往日不再"),
    ("balatro", "https://www.playbalatro.com/", "小丑牌"),
    ("cult-of-the-lamb", "http://cultofthelamb.com", "咩咩启示录"),
    ("dredge", "https://www.dredge.game/", "疏浚"),
    ("satisfactory", "https://www.satisfactorygame.com/", "幸福工厂"),
    ("teardown", "http://teardowngame.com", "拆迁"),
]


async def dismiss_cookies(page):
    """Try to dismiss common cookie/consent banners."""
    selectors = [
        # Common cookie accept buttons
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
        # Chinese variants
        'button:has-text("接受")',
        'button:has-text("同意")',
        # ID-based
        '#onetrust-accept-btn-handler',
        '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
        '[data-testid="cookie-accept"]',
        '.cookie-accept',
        '.cc-accept',
        '.js-cookie-accept',
        # Age gate
        'button:has-text("Yes")',
        'button:has-text("Enter")',
        'a:has-text("Yes")',
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
    out_dir = os.path.join(SS_DIR, slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "home-1.png")

    # Skip if already has a good webp or png
    webp_path = os.path.join(out_dir, "home-1.webp")
    if os.path.exists(webp_path) and os.path.getsize(webp_path) > 30000:
        print(f"[{idx}/{total}] SKIP {name_cn} ({slug}) - already has webp ({os.path.getsize(webp_path)} bytes)")
        return True

    print(f"[{idx}/{total}] Screenshotting {name_cn} ({slug}): {url}")
    page = await browser.new_page(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)  # Let JS/images load
        await dismiss_cookies(page)
        await page.wait_for_timeout(1000)

        await page.screenshot(path=out_path, full_page=True, timeout=30000)
        size = os.path.getsize(out_path)
        print(f"  -> Saved {out_path} ({size} bytes)")

        # Check if screenshot is suspiciously small (age gate, blocked, etc.)
        if size < 30000:
            print(f"  !! WARNING: Screenshot only {size} bytes, may be age-gated or blocked")

        return True
    except Exception as e:
        print(f"  !! ERROR: {e}")
        return False
    finally:
        await page.close()


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

    # Summary
    print("\n--- Summary ---")
    success = sum(1 for v in results.values() if v)
    print(f"Success: {success}/{total}")
    for slug, ok in results.items():
        status = "OK" if ok else "FAIL"
        print(f"  {status}: {slug}")


if __name__ == "__main__":
    asyncio.run(main())
