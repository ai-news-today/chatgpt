---
name: generate-blog-workflow
description: Use when creating, rewriting, expanding, translating, localizing, fact-checking, SEO-polishing, or reviewing multilingual Hugo blog posts.
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

## Choose the mode, then load only the matching reference

- For creating, rewriting, expanding, or refreshing a post: read [create_update.md](references/create_update.md)
- For multilingual translation or localization: read [translate_localize.md](references/translate_localize.md)
- For review-only work: read [review.md](references/review.md)
- For frontmatter, title, headline, or SEO-specific adjustments: read [seo_frontmatter.md](references/seo_frontmatter.md)
- For language fluency/clarity polishing (smooth phrasing, ambiguity reduction): read [language-clarity.md](references/language-clarity.md)

You may need more than one reference file, but only load the ones relevant to the current task.

## Core operating rules

- Prefer content-only changes unless the task clearly requires a template or SEO logic change.
- Treat Chinese and other languages as separate writing tasks, not literal sentence mapping.
- For writing/rewriting/localization tasks in any language, apply the default checklist in `references/language-clarity.md` unless the user requests a specific voice that conflicts with it.
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
