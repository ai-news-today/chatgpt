#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Skill Threshold Checker (2026)
----------------------------------
校验 seo-audit 的 SKILL.md 是否包含规定章节、报告字段与评估型数字信号。

结构校验：
  - 优先使用 markdown-it-py（CommonMark token 流）提取标题节点；
  - 未安装依赖时使用内置 ATX 解析（跳过 fenced code block），作为无依赖回退。

分词统计（辅助指标）：
  - 中文：优先 jieba；未安装则对 CJK 做字符级回退。
  - 英文：正则词元提取。

完整指标与使用说明见同目录：SEO_SKILL_THRESHOLD_CHECK.md

注意：本脚本用于校验 seo-audit 的 SKILL.md（章节与报告模板）。对博客正文「AI 比例」类诉求应使用
article_seo_eval.py（文章结构/可读性代理指标 + 基线回归），勿将本脚本误用于文章 AI 概率估计。
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Pattern, Sequence, Tuple, Union

# ---------------------------------------------------------------------------
# 常量：语言与英文词元
# ---------------------------------------------------------------------------

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CJK_ONLY_RE = re.compile(
    r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+"
)
EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z']+|[A-Za-z]")


def read_text(path: Path) -> str:
    """读取 UTF-8 文本。"""
    return path.read_text(encoding="utf-8")


def strip_yaml_front_matter(text: str) -> str:
    """去掉 YAML front matter，避免干扰 Markdown 解析。"""
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
    """移除 fenced code block 行，避免标题误报。"""
    lines = text.splitlines()
    out: List[str] = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def normalize_heading_inline(text: str) -> str:
    """弱化标题内 Markdown 装饰，便于正则匹配。"""
    s = text
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    return s.strip()


# ---------------------------------------------------------------------------
# Markdown 结构：AST（markdown-it-py）与内置 ATX 回退
# ---------------------------------------------------------------------------


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
            level = int(tok.tag[1])  # h1 -> 1
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
    """无第三方库时：解析 ATX 标题行（已建议先 strip code fence）。"""
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
    """返回标题列表与解析器来源。"""
    body = strip_fenced_code_blocks(text)
    ast = extract_headings_markdown_it(body)
    if ast is not None:
        return {
            "parser": "markdown-it-py",
            "heading_count": len(ast),
            "headings": ast,
        }
    built = extract_headings_builtin_atx(body)
    return {
        "parser": "builtin-atx",
        "heading_count": len(built),
        "headings": built,
    }


# ---------------------------------------------------------------------------
# 规则定义：标题正则 / 正文正则
# ---------------------------------------------------------------------------


def _heading_line_regex(core: str) -> Pattern[str]:
    """兼容旧逻辑：整行源码级匹配（回退用）。"""
    return re.compile(
        rf"^#{{1,6}}\s+.*{core}",
        re.IGNORECASE | re.MULTILINE,
    )


@dataclass(frozen=True)
class CheckRule:
    """单条检测规则：可选 heading_regex（匹配标题纯文本）与 body_regex（全文）。"""

    name: str
    weight: float
    heading_regex: Optional[str] = None
    body_regex: Optional[str] = None
    # 无 AST 时用于全文回退的合并模式（标题规则）
    fallback_line_pattern: Optional[Pattern[str]] = None


REQUIRED_RULES: List[CheckRule] = [
    CheckRule(
        name="2026 强制章节",
        weight=3.0,
        heading_regex=r"2026\s+Ranking\s+Focus\s*\(Mandatory\)",
        fallback_line_pattern=_heading_line_regex(
            r"2026\s+Ranking\s+Focus\s*\(Mandatory\)"
        ),
    ),
    CheckRule(
        name="信息增益小节",
        weight=10.0,
        heading_regex=r"Information\s+Gain\s*\(Net-New\s+Value\)",
        fallback_line_pattern=_heading_line_regex(
            r"Information\s+Gain\s*\(Net-New\s+Value\)"
        ),
    ),
    CheckRule(
        name="低密度警报小节",
        weight=8.0,
        heading_regex=(
            r"Low-Density\s+Content\s+Alert\s*"
            r"\(Unhelpful\s+Content\s+Risk\)"
        ),
        fallback_line_pattern=_heading_line_regex(
            r"Low-Density\s+Content\s+Alert\s*"
            r"\(Unhelpful\s+Content\s+Risk\)"
        ),
    ),
    CheckRule(
        name="UX 密度小节",
        weight=5.0,
        heading_regex=r"UX\s+Density\s*&\s*Answer-First\s+Structure",
        fallback_line_pattern=_heading_line_regex(
            r"UX\s+Density\s*&\s*Answer-First\s+Structure"
        ),
    ),
    CheckRule(
        name="信息增益 0-3 评分",
        weight=10.0,
        body_regex=(
            r"0\s*=\s*No gain[\s\S]*?1\s*=\s*Minor gain[\s\S]*?"
            r"2\s*=\s*Clear gain[\s\S]*?3\s*=\s*Strong gain"
        ),
    ),
    CheckRule(
        name="报告包含 IG 分数字段",
        weight=10.0,
        body_regex=r"Information\s+Gain\s+Score\s*\(0-3\)",
    ),
    CheckRule(
        name="报告包含密度风险分级",
        weight=5.0,
        body_regex=(
            r"Density\s+Risk\**\s*:\s*Low\s*/\s*Medium\s*/\s*High"
        ),
    ),
    CheckRule(
        name="报告包含首屏答案通过失败字段",
        weight=5.0,
        body_regex=(
            r"Above-the-Fold\s+Answer\s+Check\**\s*:\s*Pass\s*/\s*Fail"
        ),
    ),
    CheckRule(
        name="报告包含改写动作字段",
        weight=5.0,
        body_regex=(
            r"Rewrite\s+Direction\**\s*:\s*Keep\s*/\s*Rewrite\s*/\s*Merge\s*/\s*Prune"
        ),
    ),
    CheckRule(
        name="AI 拟真降分启发式小节",
        weight=5.0,
        heading_regex=(
            r"AI-Likeness\s+Reduction\s+Heuristics\s*\(Editorial\s+Pattern\)"
        ),
        fallback_line_pattern=_heading_line_regex(
            r"AI-Likeness\s+Reduction\s+Heuristics\s*\(Editorial\s+Pattern\)"
        ),
    ),
    CheckRule(
        name="文章迭代工具 article_seo_eval 引用",
        weight=3.0,
        body_regex=r"article_seo_eval\.py",
    ),
]


def _max_rule_weight_total(rules: Sequence[CheckRule]) -> float:
    return float(sum(r.weight for r in rules))


def rule_matches(
    rule: CheckRule,
    full_text: str,
    heading_titles: Sequence[str],
    use_heading_fallback: bool,
) -> bool:
    """单条规则是否命中。"""
    if rule.heading_regex is not None:
        hpat = re.compile(rule.heading_regex, re.IGNORECASE)
        if any(hpat.search(h) for h in heading_titles):
            return True
        if use_heading_fallback and rule.fallback_line_pattern is not None:
            if rule.fallback_line_pattern.search(full_text):
                return True
    if rule.body_regex is not None:
        bpat = re.compile(rule.body_regex, re.IGNORECASE | re.DOTALL)
        if bpat.search(full_text):
            return True
    return False


def evaluate_rules(
    full_text: str,
    rules: Sequence[CheckRule],
    structure: Dict[str, Any],
) -> Tuple[List[str], List[str], float, float]:
    """根据 AST/内置标题列表与正文匹配规则。"""
    headings_raw = structure.get("headings") or []
    heading_titles: List[str] = []
    for h in headings_raw:
        if isinstance(h, (list, tuple)) and len(h) >= 2:
            heading_titles.append(str(h[1]))
    parser = structure.get("parser", "")
    use_fb = parser == "builtin-atx" or not heading_titles

    passed: List[str] = []
    failed: List[str] = []
    earned = 0.0
    max_w = _max_rule_weight_total(rules)

    for rule in rules:
        if rule_matches(rule, full_text, heading_titles, use_heading_fallback=use_fb):
            passed.append(rule.name)
            earned += rule.weight
        else:
            failed.append(rule.name)

    return passed, failed, earned, max_w


# ---------------------------------------------------------------------------
# 评估型数字信号
# ---------------------------------------------------------------------------

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


def count_weighted_eval_signals(text: str) -> Tuple[float, Dict[str, float]]:
    """返回加权评估信号总分及各模式贡献。"""
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


def count_legacy_numeric_signals(text: str) -> int:
    """兼容：任意数字/分级词粗计数（仅供参考）。"""
    legacy = re.compile(
        r"\b\d+(?:\.\d+)?\b|"
        r"\b(?:High|Medium|Low|Pass|Fail)\b|"
        r"\b(?:0-3)\b",
        re.IGNORECASE,
    )
    return len(legacy.findall(text))


# ---------------------------------------------------------------------------
# 语言检测与分词（中 / 英）
# ---------------------------------------------------------------------------


def detect_document_language(text: str) -> str:
    """启发式：CJK 字符数 vs 拉丁字母数。"""
    cjk = len(CJK_RE.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk >= latin else "en"


def tokenize_chinese(text: str) -> Tuple[List[str], str]:
    """中文分词：优先 jieba；失败则返回 CJK 连续片段。"""
    try:
        import jieba  # type: ignore[import-untyped]

        tokens = [t.strip() for t in jieba.cut(text) if t.strip()]
        return tokens, "jieba"
    except ImportError:
        return CJK_ONLY_RE.findall(text), "cjk-chars-fallback"


def tokenize_english(text: str) -> List[str]:
    """英文词元：正则提取小写词形。"""
    return EN_WORD_RE.findall(text.lower())


def analyze_tokens(text: str, lang: str) -> Dict[str, Union[str, int, float]]:
    """篇幅与词元多样性辅助指标。"""
    if lang == "zh":
        tokens, tokenizer_name = tokenize_chinese(text)
    else:
        tokens = tokenize_english(text)
        tokenizer_name = "regex-en"

    n = len(tokens)
    unique = len(set(tokens)) if tokens else 0
    ratio = (unique / n) if n else 0.0
    avg_len = (sum(len(t) for t in tokens) / n) if n else 0.0

    return {
        "language": lang,
        "token_count": n,
        "unique_token_count": unique,
        "unique_token_ratio": round(ratio, 6),
        "avg_token_length": round(avg_len, 4),
        "tokenizer": tokenizer_name,
    }


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------


def build_report(
    file_path: Path,
    passed: List[str],
    failed: List[str],
    earned_weight: float,
    max_weight: float,
    eval_weighted_total: float,
    eval_breakdown: Dict[str, float],
    legacy_numeric_count: int,
    min_eval_weighted: float,
    min_weighted_ratio: float,
    strict: bool,
    structure: Dict[str, Any],
    token_analysis: Dict[str, Union[str, int, float]],
) -> Dict[str, object]:
    """构建结构化报告。"""
    weighted_ratio = earned_weight / max_weight if max_weight > 0 else 0.0
    ratio_ok = weighted_ratio + 1e-9 >= min_weighted_ratio
    eval_ok = eval_weighted_total + 1e-9 >= min_eval_weighted

    if strict:
        status = "PASS" if not failed and eval_ok else "FAIL"
    else:
        status = "PASS" if ratio_ok and eval_ok else "FAIL"

    headings = structure.get("headings") or []
    preview: List[Dict[str, Any]] = []
    for level, title in headings[:12]:
        preview.append({"level": level, "title": title[:120]})

    return {
        "file": str(file_path),
        "status": status,
        "mode": "strict" if strict else "weighted",
        "summary": {
            "passed_rules": len(passed),
            "failed_rules": len(failed),
            "rule_weight_earned": round(earned_weight, 4),
            "rule_weight_max": round(max_weight, 4),
            "weighted_ratio": round(weighted_ratio, 6),
            "min_weighted_ratio": min_weighted_ratio,
            "weighted_ratio_ok": ratio_ok,
            "eval_signal_weighted_total": round(eval_weighted_total, 4),
            "min_eval_weighted": min_eval_weighted,
            "eval_signal_ok": eval_ok,
            "legacy_numeric_signals": legacy_numeric_count,
        },
        "structure": {
            "parser": structure.get("parser"),
            "heading_count": structure.get("heading_count"),
            "headings_preview": preview,
        },
        "token_analysis": token_analysis,
        "passed": passed,
        "failed": failed,
        "eval_signal_breakdown": {k: round(v, 4) for k, v in eval_breakdown.items()},
    }


def print_human_report(report: Dict[str, object]) -> None:
    """打印人类可读报告。"""
    summary = report["summary"]
    assert isinstance(summary, dict)
    print(f"File: {report['file']}")
    print(f"Status: {report['status']} ({report['mode']})")
    print(
        "Rules: "
        f"{summary['passed_rules']} passed, "
        f"{summary['failed_rules']} failed"
    )
    print(
        "Rule weights: "
        f"{summary['rule_weight_earned']}/{summary['rule_weight_max']} "
        f"(ratio {summary['weighted_ratio']:.4f}, "
        f"need >= {summary['min_weighted_ratio']}) "
        f"-> {summary['weighted_ratio_ok']}"
    )
    print(
        "Eval signals (weighted): "
        f"{summary['eval_signal_weighted_total']} "
        f"(need >= {summary['min_eval_weighted']}) "
        f"-> {summary['eval_signal_ok']}"
    )
    print(
        "Legacy numeric count (reference only): "
        f"{summary['legacy_numeric_signals']}"
    )

    struct = report.get("structure")
    if isinstance(struct, dict):
        print(
            f"Structure: parser={struct.get('parser')}, "
            f"headings={struct.get('heading_count')}"
        )

    tok = report.get("token_analysis")
    if isinstance(tok, dict):
        print(
            f"Tokens: lang={tok.get('language')}, "
            f"count={tok.get('token_count')}, "
            f"unique_ratio={tok.get('unique_token_ratio')}"
        )

    passed = report["passed"]
    failed = report["failed"]
    assert isinstance(passed, list)
    assert isinstance(failed, list)

    if passed:
        print("\nPassed:")
        for item in passed:
            print(f"- {item}")

    if failed:
        print("\nFailed:")
        for item in failed:
            print(f"- {item}")


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="Check seo-audit SKILL.md against 2026 measurable threshold rules."
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(".agents/skills/seo-audit/SKILL.md"),
        help="Target Markdown file path",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="All rules must pass (ignore weighted ratio; still checks eval signals)",
    )
    parser.add_argument(
        "--min-weighted-ratio",
        type=float,
        default=0.85,
        help="In weighted mode: minimum earned_weight/max_weight (default: 0.85)",
    )
    parser.add_argument(
        "--min-eval-weighted",
        type=float,
        default=6.0,
        help="Minimum weighted eval-signal score (percentages, 0-3 scales, etc.)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON report",
    )
    parser.add_argument(
        "--no-token-analysis",
        action="store_true",
        help="Skip Chinese/English token statistics",
    )
    return parser.parse_args()


def main() -> None:
    """程序入口。"""
    args = parse_args()
    file_path: Path = args.file

    if not file_path.exists():
        raise SystemExit(f"Target file does not exist: {file_path}")

    raw = read_text(file_path)
    text_for_rules = strip_yaml_front_matter(raw)
    structure = extract_structure(text_for_rules)

    passed, failed, earned_w, max_w = evaluate_rules(
        full_text=text_for_rules,
        rules=REQUIRED_RULES,
        structure=structure,
    )
    eval_total, eval_breakdown = count_weighted_eval_signals(text_for_rules)
    legacy_count = count_legacy_numeric_signals(text_for_rules)

    strict_mode = bool(args.strict)
    min_ratio = 1.0 if strict_mode else float(args.min_weighted_ratio)

    if args.no_token_analysis:
        token_analysis = {
            "language": "skipped",
            "token_count": 0,
            "unique_token_count": 0,
            "unique_token_ratio": 0.0,
            "avg_token_length": 0.0,
            "tokenizer": "disabled",
        }
    else:
        lang = detect_document_language(text_for_rules)
        token_analysis = analyze_tokens(text_for_rules, lang)

    report = build_report(
        file_path=file_path,
        passed=passed,
        failed=failed,
        earned_weight=earned_w,
        max_weight=max_w,
        eval_weighted_total=eval_total,
        eval_breakdown=eval_breakdown,
        legacy_numeric_count=legacy_count,
        min_eval_weighted=float(args.min_eval_weighted),
        min_weighted_ratio=min_ratio,
        strict=strict_mode,
        structure=structure,
        token_analysis=token_analysis,
    )

    if args.json:
        # JSON 需可序列化：structure 内 headings 可能很长，保留完整列表供调试
        out = dict(report)
        out["structure"] = {
            "parser": structure.get("parser"),
            "heading_count": structure.get("heading_count"),
            "headings": [
                {"level": lev, "title": tit}
                for lev, tit in (structure.get("headings") or [])
            ],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print_human_report(report)

    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
