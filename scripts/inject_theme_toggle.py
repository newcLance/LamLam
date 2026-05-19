"""把 _theme-toggle.html 的内容注入到所有报告页 </body> 之前。
可重复运行（幂等）：注入前会先剥离旧的注入块。
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "static" / "report"
SNIPPET_FILE = REPORT_DIR / "_theme-toggle.html"

MARKER_START = "<!-- THEME_TOGGLE_INJECT_START -->"
MARKER_END = "<!-- THEME_TOGGLE_INJECT_END -->"


def main():
    snippet_raw = SNIPPET_FILE.read_text(encoding="utf-8")
    snippet = f"{MARKER_START}\n{snippet_raw}\n{MARKER_END}"

    targets = sorted(p for p in REPORT_DIR.glob("*.html") if not p.name.startswith("_"))
    print(f"Injecting into {len(targets)} report files...")

    for f in targets:
        text = f.read_text(encoding="utf-8")
        # 移除旧注入
        if MARKER_START in text and MARKER_END in text:
            i = text.index(MARKER_START)
            j = text.index(MARKER_END) + len(MARKER_END)
            text = text[:i] + text[j:]
            # 清理可能多余的换行
            text = text.replace("\n\n\n", "\n\n")

        # 在 </body> 前插入
        if "</body>" not in text:
            print(f"  [SKIP] {f.name} - no </body>")
            continue
        text = text.replace("</body>", snippet + "\n</body>", 1)
        f.write_text(text, encoding="utf-8")
        print(f"  [OK] {f.name}")


if __name__ == "__main__":
    main()
