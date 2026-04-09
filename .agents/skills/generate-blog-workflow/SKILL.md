---
name: generate-blog-workflow
description: File naming, frontmatter, translationKey, build validation, and reference section rules for this Hugo + Blowfish multilingual blog repo. Use for new posts, rewrites, translations, localization, fact-checking, and review. Writing voice and structure see blog-seo-content-create; SEO keywords see blog-seo-keyword-select; post-draft checks see blog-seo-content-check.
---

# generate-blog-workflow

This skill is the **framework baseline** for blog work in this repo: file naming, frontmatter, multilingual setup, translationKey, build validation, and reference sections.

**Out of scope for this skill:** writing voice, tone, style, AI-likeness reduction, keyword density. Those belong to dedicated skills.

---

## Skill responsibilities at a glance

| Stage | Skill |
|-------|-------|
| Topic and keyword research | [blog-seo-keyword-select](../blog-seo-keyword-select/SKILL.md) |
| Draft writing (voice / structure / perspective) | [blog-seo-content-create](../blog-seo-content-create/SKILL.md) |
| Post-draft checks (TD / density / script) | [blog-seo-content-check](../blog-seo-content-check/SKILL.md) |
| Chinese AIGC score reduction (after writing) | [humanize-chinese](../humanize-chinese/SKILL.md) |
| Academic paper AIGC reduction | [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) |
| Site-wide technical SEO | [seo-audit](../seo-audit/SKILL.md) |
| AI answer citations and extractable blocks | [ai-seo](../ai-seo/SKILL.md) |

---

## Typical tasks

- Create a new blog post
- Rewrite or expand an existing post
- Translate or localize a post into another language
- Refresh stale facts, commands, links, or positioning
- Review frontmatter, structure, or SEO fields

---

## Read before starting work

```
config/_default/hugo.toml
config/_default/languages.*.toml
content/**  (the relevant article files)
```

Read theme/template overrides only when the task involves custom rendering or SEO output not covered by frontmatter.

---

## Load by task

| Task | Read |
|------|------|
| Create / rewrite / expand / refresh | [create_update.md](references/create_update.md) |
| Translation / localization | [translate_localize.md](references/translate_localize.md) |
| Review only | [review.md](references/review.md) |
| frontmatter / title / description | [seo_frontmatter.md](references/seo_frontmatter.md) |
| Sentence fluency and disambiguation | [language-clarity.md](references/language-clarity.md) |

Load only the files relevant to the current task.

---

## Core operating rules

### File naming
- kebab-case slug based on the article's core topic keywords
- Language suffix explicit and correct: `.zh-cn.md`, `.en.md`
- No generic names: `post-1`, `update`, `new-article`

### Required frontmatter fields
- `title`: 40–60 characters (hard rule)
- `description`: 140–160 characters (hard rule)
- `translationKey`: consistent across all language variants of the same article
- `updatedDate`: sync to today (`YYYY-MM-DD`) after any edit
- If the post contains explicit freshness markers (`as of`, `last checked on`, `截至`, `最后核对日期`), update those date strings in every edited language file

### Multilingual
- Treat Chinese and English as separate writing tasks, not word-for-word translation
- `translationKey` and `locale` must be consistent across language files
- Facts, product claims, and data must be consistent across language variants

### Reference section
- Required when the post cites external sources
  - Non-Chinese posts: `## References`
  - Chinese posts: `## 官方参考`

### External links
- Default to `rel="nofollow"`
- Use descriptive anchor text; avoid "click here"

---

## Build validation

```bash
# After any content/** edit
hugo server

# Sync updatedDate
npm run sync:updated-date

# When post has reference links
npm run check:references

# Before delivery
npm run build
```

The SEO 100-point scorecard in [seo_frontmatter.md](references/seo_frontmatter.md) is a hard delivery gate.

---

## Review task rules

- Surface findings first; do not silently rewrite unless the user asks
- Cite specific file paths and line numbers
- title / description out of range must be fixed before marking done

---

## Post-publish check (when Search Console is available)

- URL Inspection: confirm crawlable, indexable, canonical correct
- Confirm no accidental noindex on indexable pages
- Performance report: check for query drift and high-impression / low-CTR pages
