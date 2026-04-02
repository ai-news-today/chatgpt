---
name: generate-blog-workflow
description: Use when creating, rewriting, expanding, translating, localizing, fact-checking, SEO-polishing, or reviewing multilingual Hugo blog posts. For Chinese body copy (去 AI 味 / natural phrasing), coordinate with humanize-chinese. For English body copy, coordinate with paper-humanizer-skill (AI-pattern removal, phrase blacklist). For traditional on-page and technical SEO beyond Hugo frontmatter, coordinate with seo-audit. For AI search citations, extractability, and LLM visibility (AEO/GEO), coordinate with ai-seo.
---

# generate-blog-workflow

Use this skill for blog-content work in the `chatgpt` repo, including:

- Create a new blog post
- Rewrite or expand an existing post
- Translate or localize a post into another language
- Refresh stale facts, commands, links, or positioning
- Review a blog post for factual, structural, SEO, or localization issues
- Adjust frontmatter such as `title`, `headline`, `description`, `summary`, or language variants

## Always read first

Before doing substantive work, align with:

- `config/_default/hugo.toml`
- `config/_default/languages.*.toml`
- The relevant file(s) under `content/**`

Read theme/template overrides only when the task involves custom rendering or SEO output not covered by frontmatter.

## Related skills (load when the task matches)

These skills complement this workflow. Read the relevant `SKILL.md` **before** finalizing copy when the user’s goal overlaps:

| When | Read |
|------|------|
| **Chinese posts** (`zh-cn`, `zh-hans`, `zh-hant`, or user asks 去 AI 味 / 人性化 / 降 AIGC) | [humanize-chinese](../humanize-chinese/SKILL.md) — detection patterns, rewrite strategies, optional CLI (`scripts/*.py` in that skill) for scoring or batch humanization. Use for body text; keep [language-clarity.md](references/language-clarity.md) as the generic baseline for all languages. |
| **English posts** (`en`, `.en.md`, `locale: "en"`, or target language English) | [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) — strip English AI-isms (see `references/phrase_blacklist.md` in that skill), keep facts intact; optional `scripts/paper_humanizer.py` for prompts or batch. Pair with [language-clarity.md](references/language-clarity.md). For **formal or academic** English, follow that skill’s factuality and citation-preservation rules; the four-section deliverable there is optional unless the user wants that format. |
| **Traditional / technical / on-page SEO** (crawlability, indexation, Core Web Vitals, site-wide meta diagnosis, snippet issues beyond a single post) | [seo-audit](../seo-audit/SKILL.md) — audit framework and fixes. Pair with [seo_frontmatter.md](references/seo_frontmatter.md) for per-post Hugo fields. |
| **AI search & citations** (AI Overviews, Perplexity/ChatGPT citations, extractable answer blocks, authority and structure for LLM surfacing) | [ai-seo](../ai-seo/SKILL.md) — citable content patterns, extractability checks, platform notes. Apply on top of frontmatter rules in [seo_frontmatter.md](references/seo_frontmatter.md). |

**Split of concerns:** `seo-audit` + `seo_frontmatter.md` cover **search engines and pages-as-documents**. `ai-seo` covers **being quoted and extracted by AI systems**. `humanize-chinese` covers **Chinese** prose quality and AI-text reduction. `paper-humanizer-skill` covers **English** (and academic) de-AI patterns and blacklist-driven polish—not a substitute for `language-clarity.md`, which still applies to all locales.

## Choose the mode, then load only the matching reference

- For creating, rewriting, expanding, or refreshing a post: read [create_update.md](references/create_update.md); **if the post is English**, also apply [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) on the body before delivery (blacklist + de-AI pass).
- For multilingual translation or localization: read [translate_localize.md](references/translate_localize.md); **if the target or reviewed language is Chinese**, also follow [humanize-chinese](../humanize-chinese/SKILL.md) for the Chinese body; **if the target or reviewed language is English**, also follow [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) for English body polish (blacklist + anti–AI-pattern pass).
- For review-only work: read [review.md](references/review.md)
- For frontmatter, title, headline, or SEO-specific adjustments: read [seo_frontmatter.md](references/seo_frontmatter.md); **for deeper SEO or AI-search goals**, also read [seo-audit](../seo-audit/SKILL.md) and/or [ai-seo](../ai-seo/SKILL.md) as in the table above.
- For language fluency/clarity polishing (smooth phrasing, ambiguity reduction): read [language-clarity.md](references/language-clarity.md); **for Chinese**, prefer [humanize-chinese](../humanize-chinese/SKILL.md) for patterns and verification; **for English**, prefer [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) for AI-ism removal alongside language-clarity.

You may need more than one reference file, but only load the ones relevant to the current task.

## Core operating rules

- Prefer content-only changes unless the task clearly requires a template or SEO logic change.
- Treat Chinese and other languages as separate writing tasks, not literal sentence mapping.
- For writing/rewriting/localization tasks in any language, apply the default checklist in `references/language-clarity.md` unless the user requests a specific voice that conflicts with it.
- **Chinese body copy:** apply [humanize-chinese](../humanize-chinese/SKILL.md) patterns (reduce template connectives, hollow buzzwords, and uniform paragraph rhythm; inject concrete examples where appropriate). Run that skill’s `detect_cn.py` / `humanize_cn.py` when the repo includes those scripts and the user wants measurable de-AI scoring.
- **English body copy:** apply [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) — avoid overused connectors and filler (“It is worth noting that”, “In summary”, mechanical Firstly/Secondly/Finally chains, etc.); use `references/phrase_blacklist.md` in that skill as the checklist. Do not invent facts or soften verified claims. Optional: `paper_humanizer.py` when batching or composing prompts. Academic or thesis-style English must keep that skill’s **strict factuality** and citation-marker rules.
- **SEO scope:** satisfy [seo_frontmatter.md](references/seo_frontmatter.md) and the scorecard gate below. When the user asks for ranking, technical SEO, or site health, use [seo-audit](../seo-audit/SKILL.md). When they ask for AI answers, citations, or LLM visibility, use [ai-seo](../ai-seo/SKILL.md) for structure (clear definitions, self-contained blocks, stats with sources, FAQ where fitting).
- Preserve shared facts, product claims, and `translationKey` consistency across languages.
- Any blog file edit (frontmatter or body) should sync `lastmod` to the current date (`YYYY-MM-DD`) when used.
- If an edited post contains explicit freshness markers in frontmatter/body (for example `as of`, `last checked on`, `截至`, `最后核对日期`), sync those dates to the current verification date and keep wording consistent across language variants.
- If facts, commands, links, or product behavior may have changed, verify them before writing.
- If a post includes reference links, it must end with a reference section:
  - `## References` for non-Chinese posts
  - `## 官方参考` for Chinese posts
- Treat SEO snippet length rules as mandatory:
  - `title` must be 40-60 characters
  - `description` must be 140-160 characters
  - Any out-of-range value must be rewritten before delivery.
- File naming must be strongly related to the article title intent:
  - Use a concise kebab-case slug based on the title's core keywords.
  - Avoid generic names like `post-1`, `update`, `new-article`.
  - Keep language suffix explicit (for example `.zh-cn.md`, `.en.md`) and aligned with content locale.
- For create/rewrite/refresh tasks, SEO acceptance score is a hard gate: only deliver when `seo_frontmatter.md` scorecard is `100/100`.
- If the user asks for review, findings come first; do not silently rewrite content unless asked.

## Validation

- After changing any file under `content/**`, run `hugo` or `hugo server` to validate output.
- For posts with reference links, verify the final reference section exists and includes cited references.
- If `title` or `description` was reviewed or edited, measure length explicitly against the hard ranges (`title` 40-60, `description` 140-160) before finishing.
- If the edited post includes explicit freshness dates, verify all in-article date markers were updated consistently in each edited language file.
- If `title`, `headline`, `description`, canonical, hreflang, or structured data changed, inspect generated output or built HTML.
- If review is requested, validate by citing concrete file paths and line numbers.
- **Chinese posts:** when tools are available, optionally re-run `detect_cn.py` from humanize-chinese after edits; aim for scores aligned with that skill’s targets if the user cares about AIGC-style detection.
- **English posts:** re-read against [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) English blacklist patterns; ensure no new fabricated stats or altered citations were introduced during polish.
- **AI-search-oriented posts:** cross-check headings and first paragraphs against [ai-seo](../ai-seo/SKILL.md) extractability (definition up front, self-contained sections, cited stats).
