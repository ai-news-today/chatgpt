#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TD（Title / Description）长度检测：Hugo Markdown 的 frontmatter 中 title 与 description。

规则默认对齐 generate-blog-workflow / seo_frontmatter.md：title 40–60、description 140–160
（字符数 = Python 3 str 的 Unicode 码点个数，中英混排均适用）。

用法：
  python3 td_frontmatter_check.py --file content/articles/foo.zh-cn.md
  python3 td_frontmatter_check.py --file content/articles/foo.en.md --json
  python3 td_frontmatter_check.py --file a.md --defaults path/to/td_check_defaults.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unquote_scalar(raw: str) -> str:
    """解析 frontmatter 行尾的值：支持双引号、单引号包裹，或裸值。"""
    s = raw.strip()
    if len(s) >= 2 and s[0] in "\"'" and s[-1] == s[0]:
        inner = s[1:-1]
        q = s[0]
        return inner.replace("\\" + q, q).replace("\\\\", "\\")
    return s


def parse_frontmatter_block(text: str) -> Tuple[Dict[str, str], int]:
    """
    解析首个 YAML frontmatter 块（仅支持常见单行键值，与仓库文章格式一致）。

    Returns:
        (meta 字典, 正文起始行号 0-based；无 frontmatter 时 meta 为空)
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 0

    meta: Dict[str, str] = {}
    end_idx: Optional[int] = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, 0

    for line in lines[1:end_idx]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, rest = stripped.split(":", 1)
        key = key.strip()
        val = unquote_scalar(rest)
        meta[key] = val

    body_start_line = end_idx + 1
    return meta, body_start_line


def load_defaults(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        path = Path(__file__).resolve().parent / "td_check_defaults.json"
    data = json.loads(read_text(path))
    return data


def resolve_ranges(
    defaults: Dict[str, Any], locale: Optional[str]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """返回 (title_min, title_max), (description_min, description_max)。"""
    t = defaults.get("title") or {}
    d = defaults.get("description") or {}
    title_range = (int(t["min"]), int(t["max"]))
    desc_range = (int(d["min"]), int(d["max"]))

    overrides = defaults.get("locale_overrides") or {}
    if locale and locale in overrides:
        lo = overrides[locale]
        if "title" in lo:
            title_range = (int(lo["title"]["min"]), int(lo["title"]["max"]))
        if "description" in lo:
            desc_range = (
                int(lo["description"]["min"]),
                int(lo["description"]["max"]),
            )
    return title_range, desc_range


def check_field(
    name: str,
    value: str,
    min_len: int,
    max_len: int,
) -> Dict[str, Any]:
    n = len(value)
    ok = min_len <= n <= max_len
    status = "PASS" if ok else "FAIL"
    detail = f"{name}: 长度 {n}（要求 {min_len}–{max_len}）"
    if not ok:
        if n < min_len:
            detail += f"，还差 {min_len - n} 个字符"
        else:
            detail += f"，超出 {n - max_len} 个字符"
    return {
        "field": name,
        "length": n,
        "min": min_len,
        "max": max_len,
        "status": status,
        "detail": detail,
    }


def run_check(
    file_path: Path, defaults_path: Optional[Path]
) -> Tuple[str, List[Dict[str, Any]], Dict[str, Any]]:
    raw = read_text(file_path)
    meta, _ = parse_frontmatter_block(raw)
    defaults = load_defaults(defaults_path)

    locale = meta.get("locale") or meta.get("lang")
    title_rng, desc_rng = resolve_ranges(defaults, locale)

    results: List[Dict[str, Any]] = []
    missing: List[str] = []

    title = meta.get("title")
    description = meta.get("description")

    if title is None or title == "":
        missing.append("title")
        results.append(
            {
                "field": "title",
                "length": 0,
                "min": title_rng[0],
                "max": title_rng[1],
                "status": "FAIL",
                "detail": "title: 缺失或为空",
            }
        )
    else:
        results.append(check_field("title", title, title_rng[0], title_rng[1]))

    if description is None or description == "":
        missing.append("description")
        results.append(
            {
                "field": "description",
                "length": 0,
                "min": desc_rng[0],
                "max": desc_rng[1],
                "status": "FAIL",
                "detail": "description: 缺失或为空",
            }
        )
    else:
        results.append(
            check_field("description", description, desc_rng[0], desc_rng[1])
        )

    overall = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"

    summary: Dict[str, Any] = {
        "file": str(file_path.resolve()),
        "locale": locale,
        "title_range": list(title_rng),
        "description_range": list(desc_rng),
        "overall": overall,
        "checks": results,
    }
    if missing:
        summary["missing_fields"] = missing

    return overall, results, summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检测 Markdown frontmatter 中 title / description（TD）长度是否合规。"
    )
    parser.add_argument(
        "--file",
        required=True,
        type=Path,
        help="文章 .md 路径",
    )
    parser.add_argument(
        "--defaults",
        type=Path,
        default=None,
        help="JSON 阈值文件（默认：与本脚本同目录的 td_check_defaults.json）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON（stdout），适合 CI",
    )
    args = parser.parse_args()

    path = args.file
    if not path.is_file():
        err = {"error": "file_not_found", "path": str(path)}
        print(json.dumps(err, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2

    overall, results, summary = run_check(path, args.defaults)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        loc = summary.get("locale") or "(未设置 locale)"
        print(f"文件：{summary['file']}")
        print(f"locale：{loc}")
        print(f"title 允许：{summary['title_range'][0]}–{summary['title_range'][1]} 字符")
        print(
            f"description 允许："
            f"{summary['description_range'][0]}–{summary['description_range'][1]} 字符"
        )
        print(f"结果：{summary['overall']}")
        for r in results:
            print(f"  - {r['detail']}")

    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
