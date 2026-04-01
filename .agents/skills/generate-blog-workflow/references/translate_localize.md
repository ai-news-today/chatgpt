# Translation / Localization Workflow

Use this reference when producing another language version of an article or localizing an existing post.

## Default approach

- Default ordering: Chinese first, then other requested languages.
- Do not translate line by line.
- Re-express the same facts and intent in the target language’s natural editorial style.

## What must stay aligned across languages

- Core facts and claims
- Product names, model names, command names, and configuration keys
- Main SEO keyword family
- CTA and article intent
- `translationKey`
- Any translated/localized file you edit should sync `updatedDate` to today's date (`YYYY-MM-DD`).
- If the post has explicit freshness dates (`as of`, `last checked on`, `截至`, `最后核对日期`), update and align those dates across all edited language versions.
- If the post includes reference links, each language version should end with a localized final reference section:
  - non-Chinese: `## References`
  - Chinese: `## 官方参考`
- Run `npm run check:references` after translation/localization changes when references are present.

## What may change across languages

- Sentence order
- Paragraph rhythm
- Examples and transitions
- Headline wording
- Section phrasing, if the target language reads better with a different framing

## Title / Headline handling

- Keep `title` and visible `h1` (`headline` when present) highly aligned in meaning.
- Prefer the same core keywords with wording adapted to the language.
- If `headline` is used, it should improve page readability, not drift away from the search intent in `title`.

## Language-quality bar (all target languages)

- Output should feel like a native blog draft in the target language, not a translation artifact.
- Avoid stiff connectors, stacked buzzwords, and repetitive summary language.
- Prefer direct, concrete phrasing over explanatory padding.
- Apply `language-clarity.md` when polishing localized output for fluency and ambiguity reduction.
- Keep commands and configuration examples exact even when surrounding prose is localized.
