---
name: blog-seo-content-check
description: Post-draft quantitative checks for blog articles — SEO compliance, TD (Title/Description) lengths, structure metrics, and text density. Can run article_seo_eval.py for quantitative scores. Does not judge whether writing sounds human — that is the starting point for blog-seo-content-create, not a patch at the end. Site-wide SEO diagnosis see seo-audit; Chinese AIGC reduction see humanize-chinese.
metadata:
  version: 2.0.0
---

# blog-seo-content-check

This skill handles **post-draft quantitative checks**: whether a single Markdown/Hugo article meets the repo's SEO and structure standards.

**Out of scope:** judging whether the article sounds like a real person wrote it. If AI-likeness is the problem, the root cause is at the writing stage — see [blog-seo-content-create](../blog-seo-content-create/SKILL.md). That cannot be fixed here.

---

## Scope boundary

| Concern | This skill |
|---------|------------|
| TD length compliance and semantic alignment on a single post | Yes |
| Quantitative structure metrics (paragraph length, list ratio, intro length, etc.) | Yes (script) |
| Site-wide crawl, indexation, speed, sitemap | No → [seo-audit](../seo-audit/SKILL.md) |
| AI search engine citation and extractability | No → [ai-seo](../ai-seo/SKILL.md) |
| Chinese AIGC detection and score reduction | No → [humanize-chinese](../humanize-chinese/SKILL.md) |

---

## TD check (required)

- `title`: **40–60** characters (hard rule — must rewrite if out of range)
- `description`: **140–160** characters (hard rule — must rewrite if out of range)
- `title` and `headline` share the same core keyword meaning
- `description` does not exaggerate or contradict the body
- Sync `updatedDate` / `lastmod` whenever SEO fields are edited

Full rules: [seo_frontmatter.md](../generate-blog-workflow/references/seo_frontmatter.md)

---

## Structure check (required)

- Body starts at `##`; heading hierarchy is logical (h2 → h3, no skipped levels)
- Opening screen makes clear: what problem this solves, who it is for
- Reference section present when external sources are cited:
  - Non-Chinese: `## References`
  - Chinese: `## 官方参考`

---

## Quantitative script

`article_seo_eval.py` outputs structure and density proxy metrics plus optional baseline regression comparison. See:

- [ARTICLE_SEO_EVAL.md](../scripts/ARTICLE_SEO_EVAL.md)

```bash
python3 .agents/skills/scripts/article_seo_eval.py \
  --file content/articles/your-article.en.md
```

Dependencies: `requirements-seo-check.txt` (optional install).

**Note:** `seo_skill_threshold_check.py` validates SKILL.md document structure, not article content. Do not use it as an article AI-score checker.

---

## SEO 100-point scorecard

Must pass the scorecard in [seo_frontmatter.md](../generate-blog-workflow/references/seo_frontmatter.md) before delivery. Any failing item must be fixed first.

---

## Related skills

| Stage | Skill |
|-------|-------|
| Keyword selection | [blog-seo-keyword-select](../blog-seo-keyword-select/SKILL.md) |
| Draft writing | [blog-seo-content-create](../blog-seo-content-create/SKILL.md) |
| Site-wide SEO | [seo-audit](../seo-audit/SKILL.md) |
| AI visibility and citability | [ai-seo](../ai-seo/SKILL.md) |
