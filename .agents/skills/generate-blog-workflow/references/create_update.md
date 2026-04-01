# Create / Update Workflow

Use this reference when creating a new post, rewriting an existing one, expanding a draft, or refreshing stale content.

## Workflow

1. Determine the target file set.
   - New post: create the primary language file and any requested language variants.
   - Existing post: inspect current frontmatter, structure, claims, commands, and links before editing.
2. Lock the content identity.
   - Choose the correct `translationKey`.
   - Keep `locale` aligned with the folder.
   - Reuse the slug unless the user explicitly wants a different URL.
   - Enforce filename-title alignment: filename slug must reflect the title's core topic keywords.
   - Use kebab-case and avoid generic slugs (e.g. `post-1`, `new-article`, `update`).
   - Keep locale suffix explicit and correct (`.zh-cn.md`, `.en.md`, etc.).
3. Set or revise frontmatter early.
   - `title`: search-result-oriented title
   - `headline`: optional visible `h1` when wording should differ slightly from `title`
   - `description` and `summary`: concise, readable, and aligned with the actual article
   - Enforce snippet lengths: `title` 40-60 chars, `description` 140-160 chars
   - `featureimage` + `showHero`: set cover image metadata so Blowfish list/article views can render the cover consistently
   - `heroStyle`: prefer `basic` unless the task explicitly needs another style
   - `robots`: set only when index-control is needed; avoid accidental deindexing
   - `updatedDate`: every blog edit must sync `updatedDate` to today's date (`YYYY-MM-DD`)
   - If the post includes explicit freshness dates (`as of`, `last checked on`, `截至`, `最后核对日期`), sync those markers to the current verification date in every edited language file.
   - Keep `title`/`headline` semantically aligned with the same core keyword so the search promise and page promise match.
4. Outline before drafting.
   - Decide the article argument/order first.
   - Aim for a clear `h1 -> h2 -> h3` shape, but only add `h3` where true substructure exists.
   - If numbered headings help, number by real structure rather than cosmetic sequencing.
5. Write or rewrite freely.
   - Preserve facts and user intent.
   - Improve flow, transitions, and section boundaries when the original structure is weak.
   - Remove fluff, repeated summaries, and generic “AI-sounding” filler.
   - Apply `language-clarity.md` for sentence-level fluency and ambiguity checks in the target language.
6. If the article contains commands, links, pricing, versions, or operational steps, verify them.
   - Google-facing baseline: write for an intended audience first, not for search-engine-first filler.
   - Make the first screen explicit about what problem is solved, for whom, and what readers can do after finishing.
   - External links should default to `rel="nofollow"`.
   - If you write raw HTML anchors instead of Markdown links, keep `rel="nofollow"` explicit.
   - Prefer descriptive anchor text over generic text like "click here".
   - If adding images, ensure they use meaningful alt text and are near relevant paragraph context.
   - If the post includes reference links, add a final reference section that lists those references:
     - non-Chinese: `## References`
     - Chinese: `## 官方参考`
7. Build and inspect.
   - Run `npm run sync:updated-date` after blog edits.
   - If explicit freshness dates exist in the post, verify those date strings were updated consistently in all edited language variants.
   - Run `npm run check:references` when the post cites references.
   - Run the SEO 100 scorecard in `seo_frontmatter.md`; any failed item blocks delivery.
   - Recount final `title` and `description` lengths; out-of-range values block delivery.
   - Do not finalize output unless SEO score is `100/100`.
   - Run `npm run build` before finishing.
8. Post-publish SEO sanity check (when Search Console is available).
   - Use URL Inspection to confirm the page is crawlable, indexable, and canonicalized as expected.
   - Verify that `noindex` is not accidentally applied to indexable blog pages.
   - Check Performance report for query drift and low-CTR pages with high impressions.

## When rewriting an existing article

- Do not anchor on old sentence order.
- It is acceptable to regroup sections, merge thin sections, or split overloaded sections when that produces a better structure.
- If the article is now aimed at a different user need, update `title`, `headline`, `description`, and `summary` together instead of patching only the body.

## Output quality bar

- The article should read like a deliberate post by a human operator or developer.
- Output should read naturally to native readers of the target language: smooth phrasing, clear referents, and low ambiguity.
- Commands should be copyable.
- The intro should tell the reader what problem the post solves and who it is for.
- The conclusion should close the loop instead of restating the entire article.
- Avoid "SEO-only" padding text, synthetic FAQs, or topic stuffing that does not help the target reader complete a task.
