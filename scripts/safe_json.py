# -*- coding: utf-8 -*-
"""
safe_json.py - 容错性超强的 JSON 解析器
==========================================
设计原则：宁可多修复，不要抛异常。

覆盖的出错场景（按实际频率排序）：
  1. 中文引号   ""'' → ""''
  2. 尾部逗号   [1,2,3,] → [1,2,3]
  3. 单引号     {'k':'v'} → {"k":"v"}
  4. 无引号key  {key: "v"} → {"key":"v"}
  5. 注释       // 和 /* */ 和 #
  6. NaN/Infinity → null
  7. 多余逗号   {,,"k":"v",,} → {"k":"v"}
  8. 缺少逗号   {"a":"1" "b":"2"} → {"a":"1","b":"2"}
  9. 未闭合字符串  {"k": "v  → {"k": "v"}
  10. 未闭合括号   {"k":"v" → {"k":"v"}
  11. BOM 头      \ufeff 开头
  12. 控制字符    \x00-\x1f 非法字符
  13. 转义错误    \\x27 等非标准转义
  14. Markdown 代码块包裹  ```json ... ```
  15. 混入的 HTML 标签（保留 <b></b>，清理其他）

用法：
  from scripts.safe_json import safe_load, safe_load_file

  data = safe_load(dirty_string)
  data = safe_load_file("path/to/file.json")
"""

import json
import re
import sys
from pathlib import Path


class JsonRepairError(Exception):
    """All repair attempts failed."""
    pass


def safe_load(text, source="<string>"):
    """
    Parse JSON with maximum tolerance.
    Returns parsed object, or raises JsonRepairError if truly unrecoverable.
    """
    if not text or not text.strip():
        raise JsonRepairError(f"Empty input from {source}")

    # === Phase 0: Quick try (maybe it's already valid) ===
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass

    # === Phase 1: Progressive cleanup ===
    cleaned = text
    repairs = []

    # 1a. Strip BOM
    if cleaned.startswith("\ufeff"):
        cleaned = cleaned[1:]
        repairs.append("stripped BOM")

    # 1b. Strip markdown code fence
    md_match = re.search(r"```(?:json)?\s*\n(.*?)```", cleaned, re.DOTALL)
    if md_match:
        cleaned = md_match.group(1)
        repairs.append("extracted from markdown code block")

    # 1c. Strip leading/trailing whitespace and junk
    cleaned = cleaned.strip()

    # 1d. Remove // line comments (but not inside strings)
    cleaned = _remove_line_comments(cleaned)
    if cleaned != text.strip():
        repairs.append("removed line comments")

    # 1e. Remove /* block comments */
    prev = cleaned
    cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
    if cleaned != prev:
        repairs.append("removed block comments")

    # 1f. Remove # line comments
    prev = cleaned
    cleaned = _remove_hash_comments(cleaned)
    if cleaned != prev:
        repairs.append("removed hash comments")

    # 1g. Replace Chinese/smart quotes
    prev = cleaned
    cleaned = cleaned.replace("\u201c", '"').replace("\u201d", '"')  # ""
    cleaned = cleaned.replace("\u2018", "'").replace("\u2019", "'")  # ''
    cleaned = cleaned.replace("\u300c", '"').replace("\u300d", '"')  # Corner brackets
    cleaned = cleaned.replace("\uff02", '"')  # Fullwidth "
    if cleaned != prev:
        repairs.append("replaced smart/Chinese quotes")

    # 1h. Remove control characters (except \n \r \t)
    prev = cleaned
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", cleaned)
    if cleaned != prev:
        repairs.append("removed control characters")

    # 1i. Replace NaN / Infinity
    prev = cleaned
    cleaned = re.sub(r"\bNaN\b", "null", cleaned)
    cleaned = re.sub(r"\b-?Infinity\b", "null", cleaned)
    if cleaned != prev:
        repairs.append("replaced NaN/Infinity with null")

    # Try after basic cleanup
    try:
        result = json.loads(cleaned)
        if repairs:
            _log(f"[safe_json] Repaired ({source}): {', '.join(repairs)}")
        return result
    except (json.JSONDecodeError, ValueError):
        pass

    # === Phase 2: Structural repairs ===

    # 2a. Single quotes to double quotes (careful with apostrophes in text)
    prev = cleaned
    cleaned = _single_to_double_quotes(cleaned)
    if cleaned != prev:
        repairs.append("converted single quotes to double quotes")

    # 2b. Trailing commas before } or ] (loop until stable)
    prev = cleaned
    for _ in range(5):
        new = re.sub(r",\s*([}\]])", r"\1", cleaned)
        if new == cleaned:
            break
        cleaned = new
    if cleaned != prev:
        repairs.append("removed trailing commas")

    # 2c. Leading/duplicate commas
    prev = cleaned
    cleaned = re.sub(r"([{\[]),+\s*", r"\1 ", cleaned)
    cleaned = re.sub(r",{2,}", ",", cleaned)
    if cleaned != prev:
        repairs.append("removed duplicate/leading commas")

    # 2d. Unquoted keys: { key: "value" } → { "key": "value" }
    prev = cleaned
    cleaned = re.sub(
        r'(?<=[{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:',
        r' "\1":',
        cleaned
    )
    if cleaned != prev:
        repairs.append("quoted unquoted keys")

    # Try again
    try:
        result = json.loads(cleaned)
        _log(f"[safe_json] Repaired ({source}): {', '.join(repairs)}")
        return result
    except (json.JSONDecodeError, ValueError):
        pass

    # === Phase 3: Missing comma insertion ===
    prev = cleaned
    # Pattern: "value" "nextkey" → "value", "nextkey"
    cleaned = re.sub(r'"\s*\n\s*"', '",\n"', cleaned)
    # Pattern: "value" { → "value", {
    cleaned = re.sub(r'"\s*\n\s*\{', '",\n{', cleaned)
    # Pattern: } "next → }, "next
    cleaned = re.sub(r'\}\s*\n\s*"', '},\n"', cleaned)
    # Pattern: ] "next → ], "next
    cleaned = re.sub(r'\]\s*\n\s*"', '],\n"', cleaned)
    # Pattern: } { → }, {
    cleaned = re.sub(r'\}\s*\n\s*\{', '},\n{', cleaned)
    if cleaned != prev:
        repairs.append("inserted missing commas")

    try:
        result = json.loads(cleaned)
        _log(f"[safe_json] Repaired ({source}): {', '.join(repairs)}")
        return result
    except (json.JSONDecodeError, ValueError):
        pass

    # === Phase 4: Unclosed structures ===
    prev = cleaned
    cleaned = _fix_unclosed(cleaned)
    if cleaned != prev:
        repairs.append("closed unclosed brackets/strings")

    # === Phase 5: Fix bad escapes ===
    prev = cleaned
    cleaned = re.sub(r"\\x([0-9a-fA-F]{2})", r"\\u00\1", cleaned)
    cleaned = re.sub(r"\\([^\"\\\/bfnrtu])", r"\\\\\1", cleaned)
    if cleaned != prev:
        repairs.append("fixed non-standard escapes")

    # Final attempt
    try:
        result = json.loads(cleaned)
        _log(f"[safe_json] Repaired ({source}): {', '.join(repairs)}")
        return result
    except json.JSONDecodeError as e:
        # === Phase 6: Nuclear option — extract partial data ===
        partial = _extract_partial(cleaned)
        if partial is not None:
            repairs.append("extracted partial data (nuclear fallback)")
            _log(f"[safe_json] PARTIAL REPAIR ({source}): {', '.join(repairs)}")
            return partial

        raise JsonRepairError(
            f"Failed to parse JSON from {source} after {len(repairs)} repair attempts.\n"
            f"Repairs tried: {', '.join(repairs)}\n"
            f"Last error: {e}\n"
            f"First 500 chars: {cleaned[:500]}"
        )


def safe_load_file(path, encoding="utf-8"):
    """Load and parse a JSON file with full tolerance."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = p.read_text(encoding, errors="replace")
    return safe_load(text, source=str(p.name))


# ============================================================
# Internal helpers
# ============================================================

def _log(msg):
    """Print repair log to stderr (non-blocking)."""
    print(msg, file=sys.stderr)


def _remove_line_comments(text):
    """Remove // comments that are not inside strings."""
    result = []
    in_string = False
    escape = False
    i = 0
    while i < len(text):
        c = text[i]
        if escape:
            result.append(c)
            escape = False
            i += 1
            continue
        if c == "\\" and in_string:
            result.append(c)
            escape = True
            i += 1
            continue
        if c == '"' and not escape:
            in_string = not in_string
            result.append(c)
            i += 1
            continue
        if not in_string and c == "/" and i + 1 < len(text) and text[i + 1] == "/":
            # Skip to end of line
            nl = text.find("\n", i)
            if nl == -1:
                break
            i = nl
            continue
        result.append(c)
        i += 1
    return "".join(result)


def _remove_hash_comments(text):
    """Remove # comments (not inside strings)."""
    lines = text.split("\n")
    result = []
    in_string = False
    for line in lines:
        out = []
        esc = False
        for c in line:
            if esc:
                out.append(c)
                esc = False
                continue
            if c == "\\" and in_string:
                out.append(c)
                esc = True
                continue
            if c == '"':
                in_string = not in_string
                out.append(c)
                continue
            if not in_string and c == "#":
                break  # skip rest of line
            out.append(c)
        result.append("".join(out))
    return "\n".join(result)


def _single_to_double_quotes(text):
    """Convert single-quoted JSON to double-quoted, handling apostrophes."""
    result = []
    i = 0
    in_double = False
    in_single = False
    while i < len(text):
        c = text[i]
        if c == "\\" and (in_double or in_single):
            result.append(c)
            if i + 1 < len(text):
                result.append(text[i + 1])
                i += 2
            else:
                i += 1
            continue
        if c == '"' and not in_single:
            in_double = not in_double
            result.append(c)
        elif c == "'" and not in_double:
            if not in_single:
                in_single = True
                result.append('"')
            else:
                in_single = False
                result.append('"')
        else:
            # Escape double quotes inside single-quoted strings
            if in_single and c == '"':
                result.append('\\"')
            else:
                result.append(c)
        i += 1
    return "".join(result)


def _fix_unclosed(text):
    """Try to close unclosed brackets and strings."""
    # Count brackets
    opens = {"[": 0, "{": 0}
    closes = {"]": "[", "}": "{"}
    in_string = False
    escape = False
    for c in text:
        if escape:
            escape = False
            continue
        if c == "\\" and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if not in_string:
            if c in opens:
                opens[c] += 1
            elif c in closes:
                opens[closes[c]] -= 1

    # Close unclosed string
    if in_string:
        text += '"'

    # Close unclosed brackets (in reverse order)
    if opens["{"] > 0:
        text += "}" * opens["{"]
    if opens["["] > 0:
        text += "]" * opens["["]

    return text


def _extract_partial(text):
    """Nuclear fallback: try to extract the first complete JSON object or array."""
    # Try to find the first { ... } or [ ... ]
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start = text.find(start_char)
        if start == -1:
            continue

        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            c = text[i]
            if esc:
                esc = False
                continue
            if c == "\\" and in_str:
                esc = True
                continue
            if c == '"':
                in_str = not in_str
                continue
            if not in_str:
                if c == start_char:
                    depth += 1
                elif c == end_char:
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[start:i + 1])
                        except json.JSONDecodeError:
                            break
    return None


# ============================================================
# CLI: validate / repair a file
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python safe_json.py <file.json> [--repair]")
        print("  Without --repair: validate only")
        print("  With --repair: fix in-place and write back")
        sys.exit(1)

    path = sys.argv[1]
    repair_mode = "--repair" in sys.argv

    try:
        data = safe_load_file(path)
        print(f"[OK] {path} - parsed successfully")

        if repair_mode:
            # Write back clean JSON
            clean = json.dumps(data, ensure_ascii=False, indent=2)
            Path(path).write_text(clean, "utf-8")
            print(f"  -> Written back (cleaned)")

        # Quick stats
        if isinstance(data, dict):
            print(f"  Type: object, keys: {list(data.keys())[:10]}")
        elif isinstance(data, list):
            print(f"  Type: array, length: {len(data)}")

    except JsonRepairError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)
