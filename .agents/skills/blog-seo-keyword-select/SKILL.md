---
name: blog-seo-keyword-select
description: SEO keyword research for blog content — core keyword selection, long-tail expansion, and density calculation. Use for "what to write to cover search intent," "how to expand a seed term into a topic cluster," "validate real demand with search and trends." Not for site-wide technical audits (see seo-audit). Hugo workflow see generate-blog-workflow.
metadata:
  version: 2.0.0
---

# blog-seo-keyword-select

This skill defines **single-article keyword research** and density calculation. It pairs with [generate-blog-workflow](../generate-blog-workflow/SKILL.md) for file and frontmatter rules.

---

## Scope boundary

| Scenario | This skill |
|----------|------------|
| Select core keywords, expand long-tails, align search intent | Yes |
| Validate real discussion with community and trend signals | Yes |
| Keyword density formula and post-draft density check | Yes |
| Site-wide crawl, indexation, CWV, sitemap | No → [seo-audit](../seo-audit/SKILL.md) |
| AI snippet citations and extractable answer blocks | No → [ai-seo](../ai-seo/SKILL.md) |
| TD length compliance and structure script thresholds | No → [blog-seo-content-check](../blog-seo-content-check/SKILL.md) |

---

## Workflow (recommended order)

### 1. Clarify intent and audience

Pick one: informational / comparison / tutorial / opinion.
Note primary language and region — affects Trends `geo` parameter and natural phrasing choices.

### 2. Seed term and core keyword (1–3 terms)

- Core keyword: tightly bound to the page's single topic; should appear in `title` / `headline` and the opening paragraph (exact placement rules: [seo_frontmatter.md](../generate-blog-workflow/references/seo_frontmatter.md)).
- Avoid picking an overly broad term and forcing a long article around it unless the structure genuinely covers the sub-intents.

### 3. Long-tail and topic cluster

- Expand the core term into **question phrases, comparison phrases, and scenario phrases** (e.g. `vs`, `how to`, `best for`, `worth it`).
- Prefer long-tails during writing — they are more specific, carry clearer intent, and naturally pull in the core keyword and LSI variants.
- Each long-tail maps to **one independently answerable H2 or section** — do not stack terms without content behind them.

### 4. Sample real discussion with search operators

Replace the quoted topic and date as needed.

**Reddit (community pain points and natural phrasing)**
```
site:reddit.com "your seed term or core phrase" after:2026-01-01
```

**X / Twitter (short discussions and trending phrasing)**
```
site:x.com "your seed term or core phrase" after:2026-01-01
```

- Roll `after:YYYY-MM-DD` forward with your research cycle.
- Goal: extract **natural question phrasing**, objections, and real scenarios to inform headings and H2s — not to copy posts.

### 5. Google Trends (relative demand and related queries)

Open in browser (replace `q=` and `geo=` as needed):

`https://trends.google.com/explore?geo=US&date=today%203-m&q=YOUR_TERM`

- Compare 2–5 candidate core terms or phrasing variants.
- Check **Related queries** to expand long-tail list. Note: Trends shows **relative interest**, not absolute search volume.

### 6. Align with the article draft

- Every core term and long-tail in the deliverable should map to a **planned section or paragraph** in the article — no floating keywords.
- After writing, hand frontmatter and structure compliance to [blog-seo-content-check](../blog-seo-content-check/SKILL.md).

---

## Keyword density: formula and post-draft check

Write the full article first in a natural voice. Density is a **post-draft verification tool**, not a target to hit while writing.

**Formula**
```
keyword density (%) = (keyword count ÷ total word count) × 100
```

**Reference ranges (primary keyword)**

| Density | Assessment |
|---------|------------|
| ~0.5–2% | Typically natural |
| ~2–3% | Borderline — read aloud to check |
| >3% | Usually feels forced; review the most concentrated paragraphs |

These are directional, not hard thresholds. Reading the article aloud is the real test.

**Post-draft check steps**

1. Write completely, then count.
2. If clearly above ~3%, fix the most concentrated paragraphs first: swap synonyms, add a concrete example.
3. Read aloud: does it sound like you're sharing something useful? If yes, density is fine.

**For a ~2000-word article**: the primary keyword appearing 20–35 times (~1–1.75%) alongside generous use of related terms and LSI variants is a reasonable baseline.

---

## Deliverable (for writer / next skill)

- **Core keyword(s)** (1–3) + **one-line positioning** (what problem this article solves)
- **Long-tail list** (each mapped to a planned H2 or FAQ entry)
- **Research evidence summary**: patterns and natural phrasing extracted from Reddit/X — not raw copy-pastes
- (Optional) **Planned placement notes**: which long-tails go into H2s, where the primary keyword appears most (title / opening / scenario sections)

---

## Related skills

| Skill | Purpose |
|-------|---------|
| [generate-blog-workflow](../generate-blog-workflow/SKILL.md) | File naming, multilingual, translationKey, reference section rules |
| [blog-seo-content-create](../blog-seo-content-create/SKILL.md) | Writing voice, structure, and perspective |
| [blog-seo-content-check](../blog-seo-content-check/SKILL.md) | Post-draft TD, density, and script checks |
