"""Retry screenshot for Eggy Party using international site."""
import asyncio
import os
from pathlib import Path

SS_DIR = Path(r"d:\ecnalClaw\output\game-platform-analysis\screenshots")


async def dismiss_overlays(page):
    selectors = [
        'button:has-text("Accept")', 'button:has-text("OK")',
        'button:has-text("Got it")', 'button:has-text("Close")',
        'button:has-text("接受")', 'button:has-text("同意")',
        'button:has-text("确定")', 'button[aria-label="Close"]',
    ]
    for sel in selectors:
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=500):
                await el.click()
                await page.wait_for_timeout(800)
        except Exception:
            pass


async def main():
    from playwright.async_api import async_playwright

    urls = [
        ("eggy-party", "https://www.eggyparty.com/", "蛋仔派对 (国际版)"),
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for slug, url, name in urls:
            out_dir = SS_DIR / slug
            out_dir.mkdir(parents=True, exist_ok=True)
            png_path = out_dir / "home-full.png"

            print(f"Screenshotting {name}: {url}")
            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                locale="zh-CN",
            )
            page = await context.new_page()
            try:
                resp = await page.goto(url, wait_until="networkidle", timeout=45000)
                print(f"  HTTP: {resp.status if resp else 'N/A'}")
                await page.wait_for_timeout(5000)
                await dismiss_overlays(page)

                # Auto-scroll
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
                await dismiss_overlays(page)

                await page.screenshot(path=str(png_path), full_page=True, timeout=60000)
                size = png_path.stat().st_size
                print(f"  PNG: {size:,} bytes")

                if size > 50000:
                    from PIL import Image
                    img = Image.open(png_path)
                    webp_path = out_dir / "home-full.webp"
                    img.save(str(webp_path), "WEBP", quality=82)
                    print(f"  WebP: {webp_path.stat().st_size:,} bytes")
                    png_path.unlink()
                else:
                    print("  !! Still too small, trying mobile site fallback")
                    await context.close()
                    # Try mobile
                    context = await browser.new_context(
                        viewport={"width": 1920, "height": 1080},
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        locale="zh-CN",
                    )
                    page = await context.new_page()
                    resp = await page.goto("https://eggyparty.163.com/", wait_until="networkidle", timeout=45000)
                    print(f"  Fallback HTTP: {resp.status if resp else 'N/A'}")
                    await page.wait_for_timeout(5000)
                    await page.screenshot(path=str(png_path), full_page=True, timeout=60000)
                    size = png_path.stat().st_size
                    print(f"  Fallback PNG: {size:,} bytes")
                    if size > 50000:
                        from PIL import Image
                        img = Image.open(png_path)
                        webp_path = out_dir / "home-full.webp"
                        img.save(str(webp_path), "WEBP", quality=82)
                        print(f"  WebP: {webp_path.stat().st_size:,} bytes")
                        png_path.unlink()

            except Exception as e:
                print(f"  ERROR: {e}")
            finally:
                await context.close()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
