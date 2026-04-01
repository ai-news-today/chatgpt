# SEO / Frontmatter Notes

Use this reference when adjusting `title`, `headline`, `description`, `summary`, or article structure.

## Frontmatter roles

- `title`: search-result-facing title used in HTML `<title>`, OG, and Twitter tags
- `headline`: optional visible page `h1`
- `description`: search/social summary
- `summary`: on-page short intro block under the article header
- Any edit to `title` / `headline` / `description` / `summary` must sync `updatedDate` to today (`YYYY-MM-DD`)
- If the article includes explicit freshness labels (`as of`, `last checked on`, `截至`, `最后核对日期`), sync those date markers to the current verification date when you edit SEO-facing copy.

## Title and headline rules

- `title` and `headline` should share the same core keywords and meaning.
- Prefer “same core terms, slightly different wording” over total separation.
- `headline` should improve page readability, not represent a different promise.
- Keep `title` unique per indexable URL; avoid micro-boilerplate titles that differ only by tiny suffixes.

## Length guidance

- Chinese `title`: 20-32 Han characters, hard cap 40
- English/Japanese `title`: 45-65 characters, hard cap 70
- Chinese `description`: 60-90 Han characters, hard cap 110
- English/Japanese `description`: 120-160 characters, hard cap 160

Hard caps are mandatory. Treat anything over the cap as a bug that must be rewritten, not as an acceptable tradeoff.

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
