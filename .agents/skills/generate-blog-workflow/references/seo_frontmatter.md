# SEO / Frontmatter Notes

Use this reference when adjusting `title`, `headline`, `description`, `summary`, or article structure.

## Frontmatter roles

- `title`: search-result-facing title used in HTML `<title>`, OG, and Twitter tags
- `headline`: optional visible page `h1`
- `description`: search/social summary
- `summary`: on-page short intro block under the article header
- `robots`: per-page crawler directives for index-control scenarios
- `featureimage`: article cover image URL/path used by Blowfish hero/list rendering
- `showHero` / `heroStyle`: control article hero image visibility and style
- Any edit to `title` / `headline` / `description` / `summary` must sync `updatedDate` to today (`YYYY-MM-DD`)
- If the article includes explicit freshness labels (`as of`, `last checked on`, `截至`, `最后核对日期`), sync those date markers to the current verification date when you edit SEO-facing copy.

## Title and headline rules

- `title` and `headline` should share the same core keywords and meaning.
- Prefer “same core terms, slightly different wording” over total separation.
- `headline` should improve page readability, not represent a different promise.
- Keep `title` unique per indexable URL; avoid micro-boilerplate titles that differ only by tiny suffixes.

## Length guidance

- `title`: 40-60 characters (hard rule)
- `description` (meta description): 140-160 characters (hard rule)

These ranges are mandatory for this skill. Treat out-of-range values as bugs that must be rewritten before delivery.

## Description and snippet rules

- Write `description` for users first: specific, concrete, and matching the page's actual scope.
- Assume Google may rewrite snippets; keep the opening paragraph aligned with `title` and user intent.
- Do not promise outcomes the article body does not actually deliver.

## Structure guidance

- The page has one template-level `h1`.
- Markdown body should begin at `h2`.
- Aim for a clear `h1 -> h2 -> h3` structure, but only when the article logic supports it.
- Numbered `h2` / `h3` headings are fine when the article is tutorial-like and the numbering reflects the true structure.
- External links in the article body should default to `rel="nofollow"`.
- If the article uses raw HTML `<a>` tags, keep `rel="nofollow"` explicit instead of assuming the renderer will add it later.

## Blowfish cover and list-display guidance

- To ensure cover image appears in article and list pages, prefer setting:
  - `featureimage`
  - `showHero: true`
  - `heroStyle: basic` (or another style allowed by Blowfish)
- Keep image semantics aligned:
  - Cover should match `title` intent and first-screen summary.
  - Use descriptive alt text in Markdown body when the same image is inserted in content.
- For list CTR quality:
  - Keep `summary` concrete and consistent with `description`.
  - Avoid generic cover files; use topic-specific image naming where possible.

Recommended front matter baseline for SEO + cover display:

```yaml
title: "..."
headline: "..."
description: "..."
summary: "..."
date: 2026-04-01
lastmod: 2026-04-01
updatedDate: 2026-04-01
robots: "index,follow,max-image-preview:large"
featureimage: "images/articles/your-topic-cover.jpg"
showHero: true
heroStyle: "basic"
showSummary: true
showTableOfContents: true
```

## Canonical / hreflang / indexing notes

- Each indexable page should have one self-referencing canonical absolute URL.
- In multilingual variants, keep canonical within the same language page and use `hreflang` to connect alternates.
- `hreflang` sets should include reciprocal return links and `x-default`.
- Do not treat `robots.txt` as a `noindex` mechanism; use robots meta or `X-Robots-Tag` when deindexing is needed.

## Validation triggers

Always measure final string length when you touch `title` or `description`.

Inspect built output when changing any of the following:

- `title`
- `headline`
- `description`
- canonical-sensitive page logic
- hreflang-sensitive content availability
- structured-data-relevant article metadata

Also verify in-file explicit freshness dates when any SEO-facing copy is edited:

- Intro/body/reference date markers (`as of`, `last checked on`, `截至`, `最后核对日期`) should be updated consistently in each edited language file.

If available, validate these post-build with Search Console:

- URL Inspection (selected canonical, crawl/index status)
- Page Indexing report (`noindex` and crawl-blocking anomalies)

## SEO 100 scorecard (mandatory for create/rewrite/refresh)

Treat this as a release gate, not a suggestion. Final score must be `100/100`.

Scoring rubric:

- 20 points: Search intent alignment
  - `title`, `description`, intro, and main sections solve the same user problem.
  - The promise in search snippet matches what the article actually delivers.
- 15 points: Keyword and entity strategy
  - One primary keyword cluster is clear and naturally repeated.
  - Supporting entities and variants are present without stuffing.
- 15 points: SERP snippet quality
  - `title` is within 40-60 characters.
  - `description` is within 140-160 characters.
  - Snippet copy is specific, concrete, and avoids clickbait.
- 10 points: Information architecture
  - One page `h1` from template; Markdown body starts at `h2`.
  - `h2 -> h3` hierarchy is logical and not decorative.
- 10 points: Internal and external linking
  - Internal links are relevant and use descriptive anchor text.
  - External links are authoritative and use `rel="nofollow"` when applicable.
- 10 points: Trust and freshness
  - Facts, versions, pricing, commands, and dates are verified.
  - Explicit freshness markers are synced to current verification date.
- 10 points: Rich results readiness
  - Frontmatter and body stay consistent with structured-data fields.
  - No conflicts between title/headline/description and visible page semantics.
- 10 points: Media and accessibility
  - Images (if present) include meaningful alt text and contextual placement.
  - Readability is high and phrasing is clear for the target locale.

Fail conditions (must fix before delivery):

- Any `title` length outside 40-60 characters
- Any `description` length outside 140-160 characters
- Misaligned search promise vs body scope
- Broken heading hierarchy
- Missing references section when citations are present
- Stale explicit freshness date markers
- Canonical/hreflang inconsistency in multilingual variants

Required output note for AI-generated content:

- Include a short "SEO checklist" with each rubric line marked pass/fail.
- If all pass, report `SEO score: 100/100`.
- If any line fails, keep revising until score reaches `100/100`.
