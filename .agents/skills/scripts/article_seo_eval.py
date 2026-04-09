#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章 SEO / 可读性评估（生成后质检 + 回归对比）

用于 Markdown 正文（含 Hugo front matter），与 seo_skill_threshold_check.py（技能文档）分离。

默认阈值：article_eval_defaults.json
说明文档：ARTICLE_SEO_EVAL.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ---------------------------------------------------------------------------
# 与技能脚本一致：可选依赖见 requirements-seo-check.txt
# - markdown-it-py：CommonMark token 流提取标题（与 seo_skill_threshold_check 一致）
# - jieba：中文分词（未安装则 CJK 字片回退）
# 未安装上述包时仍可运行，仅结构解析与中文词数精度略降。
# ---------------------------------------------------------------------------

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CJK_ONLY_RE = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+"
)
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']+|[A-Za-z]")

# 人类可读输出用
STATUS_ZH = {"PASS": "通过", "WARN": "警告", "FAIL": "未通过"}
SEVERITY_ZH = {"warn": "警告", "fail": "严重"}

PARSER_ZH = {
    "markdown-it-py": "CommonMark 解析（markdown-it-py，标题 AST）",
    "builtin-atx": "内置 ATX 行解析（未装 markdown-it-py）",
}

LANG_ZH = {"zh": "中文", "en": "英文"}

# 回归项指标名（中文）
METRIC_NAME_ZH: Dict[str, str] = {
    "structure_parser": "标题解析方式",
    "heading_count": "章节标题数（≥##）",
    "intro_word_count": "开篇词数",
    "list_line_ratio": "列表行占比",
    "max_paragraph_words": "最长段落词数",
    "long_paragraph_count": "超长段落数",
    "eval_signal_weighted_total": "评估型数字加权分",
    "unique_token_ratio": "词面唯一比例",
    "token_count": "词元总数",
    "link_count": "Markdown 链接数",
    "avg_paragraph_words": "段落平均词数",
}

EVAL_PATTERN_WEIGHTS: List[Tuple[str, float]] = [
    (r"\d+(?:\.\d+)?%", 2.0),
    (
        r"(?:\(0\s*[-–]\s*3\)|(?<![0-9])0\s*[-–]\s*3(?![0-9]))(?!\s*年)",
        3.0,
    ),
    (
        r"(?<![0-9])(?:[1-9]\d?|100)\s*/\s*(?:[1-9]\d?|100)(?![0-9])",
        1.5,
    ),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_yaml_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1 :])
    return text


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.splitlines()
    out: List[str] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def normalize_heading_inline(text: str) -> str:
    """弱化标题内 Markdown 装饰。"""
    s = text
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s.strip()


def extract_headings_markdown_it(text: str) -> Optional[List[Tuple[int, str]]]:
    """使用 markdown-it-py 从 token 流提取 (level, title_text)。"""
    try:
        from markdown_it import MarkdownIt  # type: ignore[import-untyped]
    except ImportError:
        return None

    md = MarkdownIt()
    tokens = md.parse(text)
    headings: List[Tuple[int, str]] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.type == "heading_open":
            level = int(tok.tag[1])
            i += 1
            parts: List[str] = []
            while i < len(tokens) and tokens[i].type != "heading_close":
                if tokens[i].type == "inline":
                    parts.append(tokens[i].content or "")
                i += 1
            raw = "".join(parts)
            headings.append((level, normalize_heading_inline(raw)))
        i += 1
    return headings


def extract_headings_builtin_atx(text: str) -> List[Tuple[int, str]]:
    """无 markdown-it-py 时：按行解析 ATX 标题。"""
    headings: List[Tuple[int, str]] = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = normalize_heading_inline(m.group(2).rstrip("#").strip())
        headings.append((level, title))
    return headings


def extract_structure(text: str) -> Dict[str, Any]:
    """与 seo_skill_threshold_check 相同：优先 AST，否则 builtin-atx。"""
    body = strip_fenced_code_blocks(text)
    ast = extract_headings_markdown_it(body)
    if ast is not None:
        return {"parser": "markdown-it-py", "headings": ast}
    built = extract_headings_builtin_atx(body)
    return {"parser": "builtin-atx", "headings": built}


def detect_language(text: str) -> str:
    cjk = len(CJK_RE.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk >= latin else "en"


def tokenize_words(text: str, lang: str) -> List[str]:
    if lang == "zh":
        try:
            import jieba  # type: ignore[import-untyped]

            return [t.strip() for t in jieba.cut(text) if t.strip()]
        except ImportError:
            return CJK_ONLY_RE.findall(text)
    return EN_WORD_RE.findall(text.lower())


def count_weighted_eval_signals(text: str) -> Tuple[float, Dict[str, float]]:
    breakdown: Dict[str, float] = {}
    total = 0.0
    for pattern, w in EVAL_PATTERN_WEIGHTS:
        matches = list(re.finditer(pattern, text, flags=re.IGNORECASE))
        if not matches:
            continue
        contrib = float(len(matches)) * w
        breakdown[pattern] = breakdown.get(pattern, 0.0) + contrib
        total += contrib
    return total, breakdown


def split_paragraphs(body: str) -> List[str]:
    parts = re.split(r"\n\s*\n+", body.strip())
    return [p.strip() for p in parts if p.strip()]


def word_count_paragraph(para: str, lang: str) -> int:
    return len(tokenize_words(para, lang))


def intro_before_first_h2(body: str) -> str:
    """第一个 ## 标题之前的正文（首屏/开篇代理）。"""
    lines = body.splitlines()
    buf: List[str] = []
    for line in lines:
        if re.match(r"^##\s+", line.strip()):
            break
        buf.append(line)
    return "\n".join(buf).strip()


def count_markdown_links(text: str) -> int:
    """粗略统计 [text](url) 形式链接数量。"""
    return len(re.findall(r"\[[^\]]*\]\([^)]+\)", text))


def list_line_ratio(body: str) -> Tuple[int, int, float]:
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if not lines:
        return 0, 0, 0.0
    list_lines = sum(
        1
        for ln in lines
        if re.match(r"^\s*([-*+]|\d+\.)\s+", ln)
    )
    return list_lines, len(lines), list_lines / len(lines)


def compute_metrics(raw: str) -> Dict[str, Any]:
    body_fm = strip_yaml_front_matter(raw)
    body = strip_fenced_code_blocks(body_fm)
    lang = detect_language(body)

    struct = extract_structure(body_fm)
    headings = struct["headings"]
    structure_parser = struct["parser"]
    heading_count = len([h for h in headings if h[0] >= 2])
    h1_count = len([h for h in headings if h[0] == 1])

    intro = intro_before_first_h2(body)
    intro_words = tokenize_words(intro, lang)
    intro_word_count = len(intro_words)

    paragraphs = split_paragraphs(body)
    if lang == "en":
        pwc = [word_count_paragraph(p, lang) for p in paragraphs]
    else:
        pwc = [word_count_paragraph(p, lang) for p in paragraphs]

    max_pw = max(pwc) if pwc else 0
    avg_pw = (sum(pwc) / len(pwc)) if pwc else 0.0
    long_thr = 120
    long_cnt = sum(1 for n in pwc if n > long_thr)

    ll, nl, lratio = list_line_ratio(body)
    eval_total, eval_bd = count_weighted_eval_signals(body)

    tokens = tokenize_words(body, lang)
    tc = len(tokens)
    ut = len(set(tokens)) if tokens else 0
    ut_ratio = (ut / tc) if tc else 0.0

    links = count_markdown_links(body)

    return {
        "language": lang,
        "structure_parser": structure_parser,
        "h1_count": h1_count,
        "heading_count": heading_count,
        "intro_word_count": intro_word_count,
        "intro_char_count": len(intro),
        "paragraph_count": len(paragraphs),
        "avg_paragraph_words": round(avg_pw, 4),
        "max_paragraph_words": max_pw,
        "long_paragraph_count": long_cnt,
        "long_paragraph_word_threshold": long_thr,
        "list_line_ratio": round(lratio, 6),
        "list_lines": ll,
        "non_empty_lines": nl,
        "eval_signal_weighted_total": round(eval_total, 4),
        "eval_signal_breakdown": {k: round(v, 4) for k, v in eval_bd.items()},
        "token_count": tc,
        "unique_token_count": ut,
        "unique_token_ratio": round(ut_ratio, 6),
        "link_count": links,
    }


def load_defaults(path: Optional[Path]) -> Dict[str, Any]:
    if path is None:
        here = Path(__file__).resolve().parent / "article_eval_defaults.json"
        path = here
    data = json.loads(read_text(path))
    return data


def check_thresholds(
    metrics: Dict[str, Any], defaults: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """根据 defaults.thresholds 生成检查结果（message 为中文说明）。"""
    """根据 defaults.thresholds 生成检查结果。"""
    out: List[Dict[str, Any]] = []
    th = defaults.get("thresholds") or {}

    def get_num(key: str) -> Optional[float]:
        v = metrics.get(key)
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return float(v)
        return None

    # heading_count_min
    spec = th.get("heading_count_min") or {}
    if spec.get("min") is not None:
        v = get_num("heading_count")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "heading_count_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"章节标题数（≥##）为 {v}，低于下限 {spec['min']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # intro_word_count_min
    spec = th.get("intro_word_count_min") or {}
    if spec.get("min") is not None:
        v = get_num("intro_word_count")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "intro_word_count_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"开篇词数（首个 ## 之前）为 {v}，低于下限 {spec['min']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # list_line_ratio_min
    spec = th.get("list_line_ratio_min") or {}
    if spec.get("min") is not None:
        v = get_num("list_line_ratio")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "list_line_ratio_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"列表行占比 {v:.4f}，低于下限 {spec['min']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # max_paragraph_words_soft
    spec = th.get("max_paragraph_words_soft") or {}
    if spec.get("max") is not None:
        v = get_num("max_paragraph_words")
        if v is not None and v > float(spec["max"]):
            out.append(
                {
                    "id": "max_paragraph_words_soft",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"最长段落词数 {v}，超过建议上限 {spec['max']}（可考虑拆段）。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # long_paragraph_count_max（long_paragraph_word_threshold 在 main 中已写入 metrics）
    spec = th.get("long_paragraph_count_max") or {}
    if spec.get("max") is not None:
        v = get_num("long_paragraph_count")
        if v is not None and v > float(spec["max"]):
            lwt = int(metrics.get("long_paragraph_word_threshold", 120))
            out.append(
                {
                    "id": "long_paragraph_count_max",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"超长段落数（单段词数>{lwt}）为 {v}，超过上限 {spec['max']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # eval_signal_weighted_min
    spec = th.get("eval_signal_weighted_min") or {}
    if spec.get("min") is not None:
        v = get_num("eval_signal_weighted_total")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "eval_signal_weighted_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"评估型数字加权分 {v}，低于下限 {spec['min']}（可补充 %、分制、比率等）。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # unique_token_ratio_min
    spec = th.get("unique_token_ratio_min") or {}
    if spec.get("min") is not None:
        v = get_num("unique_token_ratio")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "unique_token_ratio_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"词面唯一比例 {v:.4f}，低于下限 {spec['min']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    # link_count_min
    spec = th.get("link_count_min") or {}
    if spec.get("min") is not None:
        v = get_num("link_count")
        if v is not None and v < float(spec["min"]):
            out.append(
                {
                    "id": "link_count_min",
                    "severity": spec.get("severity", "warn"),
                    "message": (
                        f"Markdown 链接数为 {v}，低于下限 {spec['min']}。"
                    ),
                    "hint": spec.get("hint", ""),
                }
            )

    return out


def compare_regression(
    current: Dict[str, Any],
    baseline: Dict[str, Any],
    defaults: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """与基线 metrics 对比；对「越大越好」指标检测相对下降。"""
    reg = defaults.get("regression") or {}
    rw = float(reg.get("relative_warn", 0.12))
    rf = float(reg.get("relative_fail", 0.28))
    keys = defaults.get("metrics_in_baseline") or []
    base_m = baseline.get("metrics") or baseline
    issues: List[Dict[str, Any]] = []

    # 越小越好：长段数量上升为劣化
    lower_is_better = {"long_paragraph_count", "max_paragraph_words"}

    for key in keys:
        if key not in current or key not in base_m:
            continue
        cur = current[key]
        b0 = base_m[key]
        if not isinstance(cur, (int, float)) or not isinstance(
            b0, (int, float)
        ):
            continue
        if b0 == 0 and cur == 0:
            continue

        if key in lower_is_better:
            if b0 <= 0:
                continue
            # 当前比基线大 → 变差
            delta = (float(cur) - float(b0)) / float(b0)
            if delta > rf:
                sev = "fail"
            elif delta > rw:
                sev = "warn"
            else:
                continue
            label = METRIC_NAME_ZH.get(key, key)
            issues.append(
                {
                    "metric": key,
                    "severity": sev,
                    "baseline": b0,
                    "current": cur,
                    "relative_change": round(delta, 4),
                    "message": (
                        f"「{label}」相对基线上升 {delta:.1%}（该指标越小越好）。"
                    ),
                }
            )
        else:
            if b0 <= 0:
                # 无基线尺度时用绝对差
                continue
            delta = (float(cur) - float(b0)) / float(abs(b0))
            if delta < -rf:
                sev = "fail"
            elif delta < -rw:
                sev = "warn"
            else:
                continue
            label = METRIC_NAME_ZH.get(key, key)
            issues.append(
                {
                    "metric": key,
                    "severity": sev,
                    "baseline": b0,
                    "current": cur,
                    "relative_change": round(delta, 4),
                    "message": (
                        f"「{label}」相对基线下降 {(-delta):.1%}（该指标越大越好）。"
                    ),
                }
            )

    return issues


def overall_status(
    checks: List[Dict[str, Any]],
    regressions: List[Dict[str, Any]],
    fail_on_warn: bool,
) -> str:
    fails = [x for x in checks if x.get("severity") == "fail"]
    warns = [x for x in checks if x.get("severity") == "warn"]
    rf = [x for x in regressions if x.get("severity") == "fail"]
    rw = [x for x in regressions if x.get("severity") == "warn"]

    if fails or rf:
        return "FAIL"
    if fail_on_warn and (warns or rw):
        return "FAIL"
    if warns or rw:
        return "WARN"
    return "PASS"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="对生成后的 Markdown 文章做指标统计、阈值检查与回归对比。"
    )
    p.add_argument("--file", type=Path, required=True, help="文章 .md 路径")
    p.add_argument(
        "--defaults",
        type=Path,
        default=None,
        help="阈值 JSON（默认：脚本同目录 article_eval_defaults.json）",
    )
    p.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="历史基线 JSON（由 --save-baseline 生成），用于回归对比",
    )
    p.add_argument(
        "--save-baseline",
        type=Path,
        default=None,
        help="将当前指标快照写入文件，供后续回归对比",
    )
    p.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="出现「警告」级阈值/回归时也以非零退出码结束",
    )
    p.add_argument("--json", action="store_true", help="输出 JSON 报告")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    path = args.file
    if not path.exists():
        print(f"找不到文件：{path}", file=sys.stderr)
        sys.exit(2)

    defaults = load_defaults(args.defaults)
    raw = read_text(path)
    metrics = compute_metrics(raw)

    # 应用 defaults 中长段阈值（若存在）
    th = defaults.get("thresholds") or {}
    lthr = th.get("long_paragraph_word_threshold", {}).get("value", 120)
    if isinstance(lthr, (int, float)):
        body_fm = strip_yaml_front_matter(raw)
        body = strip_fenced_code_blocks(body_fm)
        lang = metrics["language"]
        paragraphs = split_paragraphs(body)
        pwc = [word_count_paragraph(p, lang) for p in paragraphs]
        long_cnt = sum(1 for n in pwc if n > int(lthr))
        metrics["long_paragraph_count"] = long_cnt
        metrics["long_paragraph_word_threshold"] = int(lthr)

    checks = check_thresholds(metrics, defaults)
    regressions: List[Dict[str, Any]] = []
    if args.baseline:
        bp = args.baseline
        if not bp.exists():
            print(f"找不到基线文件：{bp}", file=sys.stderr)
            sys.exit(2)
        baseline_obj = json.loads(read_text(bp))
        regressions = compare_regression(metrics, baseline_obj, defaults)

    status = overall_status(checks, regressions, args.fail_on_warn)

    for c in checks:
        c["severity_zh"] = SEVERITY_ZH.get(str(c.get("severity", "")), "")
    for r in regressions:
        r["severity_zh"] = SEVERITY_ZH.get(str(r.get("severity", "")), "")

    report: Dict[str, Any] = {
        "file": str(path.resolve()),
        "status": status,
        "status_zh": STATUS_ZH.get(status, status),
        "metrics": metrics,
        "threshold_checks": checks,
        "regression_checks": regressions,
        "defaults_version": defaults.get("version"),
    }

    if args.save_baseline:
        snap = {
            "version": 1,
            "source_file": str(path.resolve()),
            "metrics": {k: metrics[k] for k in defaults.get("metrics_in_baseline", []) if k in metrics},
        }
        args.save_baseline.write_text(
            json.dumps(snap, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        report["baseline_saved"] = str(args.save_baseline.resolve())

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        st_zh = STATUS_ZH.get(status, status)
        lang_zh = LANG_ZH.get(str(metrics["language"]), metrics["language"])
        parser_zh = PARSER_ZH.get(
            str(metrics.get("structure_parser", "")), "未知"
        )
        print(f"文件：{report['file']}")
        print(f"状态：{st_zh}（{status}）")
        print(f"语言：{lang_zh}")
        print(f"标题解析：{parser_zh}")
        print(
            "摘要："
            f"章节标题数（≥##）={metrics['heading_count']}，"
            f"开篇词数={metrics['intro_word_count']}，"
            f"列表行占比={metrics['list_line_ratio']:.4f}，"
            f"评估型数字加权分={metrics['eval_signal_weighted_total']}，"
            f"词面唯一比例={metrics['unique_token_ratio']:.4f}，"
            f"链接数={metrics['link_count']}"
        )
        if checks:
            print("\n阈值检查：")
            for c in checks:
                sev = str(c.get("severity", ""))
                sev_zh = SEVERITY_ZH.get(sev, sev)
                print(f"  [{sev_zh}] {c.get('message')}")
                hint = c.get("hint")
                if hint:
                    print(f"      说明：{hint}")
        if regressions:
            print("\n回归对比（相对基线）：")
            for r in regressions:
                sev = str(r.get("severity", ""))
                sev_zh = SEVERITY_ZH.get(sev, sev)
                print(f"  [{sev_zh}] {r.get('message')}")

    if status == "FAIL":
        sys.exit(1)
    if status == "WARN" and args.fail_on_warn:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
