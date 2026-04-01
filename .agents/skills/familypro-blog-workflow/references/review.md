# Blog Review Workflow

Use this reference when the user asks to review, audit, inspect, or sanity-check a blog post.

## Review posture

- Findings first.
- Prioritize bugs, factual risk, behavioral regressions, stale guidance, broken commands, broken links, and SEO or localization issues.
- Do not lead with a summary.
- Do not rewrite content unless the user asks for edits after the review.

## Review order

1. Fact stability
   - Has anything time-sensitive potentially changed?
   - Are versions, commands, links, or product capabilities stated too absolutely?
2. Operational correctness
   - Are commands plausible and in the right order?
   - Are config paths, files, and auth flows described correctly?
3. Structure and readability
   - Does the `h1 -> h2 -> h3` structure reflect the actual argument?
   - Are any sections thin, duplicated, or mechanically split?
   - For posts in any language, check sentence-level ambiguity (unclear referents, overloaded long sentences, missing subject/object) using `language-clarity.md`.
4. Frontmatter and multilingual integrity
   - `locale`, `translationKey`, `title`, `headline`, `description`, `summary`, dates
   - If a blog file was edited, `updatedDate` should be synced to the actual edit date (`YYYY-MM-DD`)
   - locale-specific `title` / `description` length limits, including hard caps
   - Cross-language consistency without literal translation artifacts
5. SEO basics
   - `title` / `headline` relation and single-intent consistency
   - clarity and uniqueness of `description`
   - hard-cap violations on `title` or `description` are findings, not style nits
   - first-screen content matches the search promise (no bait-and-switch)
   - links are crawlable (`<a href>`) and anchor text is descriptive
   - image alt text is meaningful where images carry information
   - external links defaulting to `rel="nofollow"`
   - likely canonical/hreflang/structured-data implications if relevant to the change
6. Reference links section integrity
   - If a post includes reference links, it must end with one final localized reference section:
     - non-Chinese: `## References`
     - Chinese: `## 官方参考`
   - The final reference section should include links that were cited in the article body.
   - For multi-post review, run `npm run check:references` and report failures as findings.

## Findings format

- Order by severity.
- Use file paths and line numbers.
- Explain the consequence, not just the symptom.
- If no findings are discovered, say so explicitly and mention any residual risk or verification gap.

## Typical issue patterns

- Reader is sent to the wrong config or auth file
- A command path is outdated or no longer canonical
- The article treats a conditional fact as universal
- The post adds keyword-heavy filler that does not help the intended reader
- Multilingual variants drift in meaning or over-translate
- `title` and `h1` no longer describe the same page
- English or Japanese `title` exceeds 70 characters, or `description` exceeds 160 characters
- The article cites external references but does not end with localized final references (`## References` / `## 官方参考`)
- Canonical/hreflang is internally inconsistent or missing `x-default` where expected
