"""
截取蓝色星原官网首页全页长图 → 保存到源截图目录。
用系统 py314（含 playwright+chromium+PIL）。SPA 用 domcontentloaded + 固定等待。
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SS_DIR = Path(r"d:\ecnalClaw\output\game-platform-analysis\screenshots\azur-promilia")
SS_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://azurpromilia.manjuu.com/home/"

def dismiss(page):
    for sel in [
        'button:has-text("同意")', 'button:has-text("接受")', 'button:has-text("确定")',
        'button:has-text("我知道了")', 'button:has-text("进入")', 'button:has-text("Accept")',
        'button:has-text("Agree")', 'button[aria-label="关闭"]', 'button[aria-label="Close"]',
        '.close', '.modal-close', '.popup-close',
    ]:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                el.click(timeout=1500)
                print("dismissed", sel)
                time.sleep(0.8)
        except Exception:
            pass

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width":1920,"height":1080},
                        device_scale_factor=1,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    page = ctx.new_page()
    print("opening", URL)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        print("goto warn:", e)
    time.sleep(6)  # 等 SPA 首屏动画/资源
    dismiss(page)
    # 滚到底触发懒加载
    for i in range(6):
        page.mouse.wheel(0, 1400)
        time.sleep(0.8)
    page.mouse.wheel(0, -100000)  # 回到顶部
    time.sleep(2)
    print("title:", page.title())
    print("url:", page.url)
    out = SS_DIR / "home-full.png"
    page.screenshot(path=str(out), full_page=True)
    print("saved", out, out.stat().st_size, "bytes")
    b.close()
