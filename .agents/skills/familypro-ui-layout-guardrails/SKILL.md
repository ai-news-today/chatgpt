---
name: familypro-ui-layout-guardrails
description: Use when changing UI layout or responsive behavior in the ChatGPT Hugo site, especially home/article/list templates. Covers content-column alignment, desktop/mobile TOC separation, sticky sidebar behavior, active-heading highlighting, overflow handling, and layout regression checks.
---

# ChatGPT UI Layout Guardrails

Use this skill for template-layer UI changes in:

- `layouts/**`
- `content/**`
- shared UI components used by page layout

## Read before editing

1. `config/_default/params.toml`
2. `layouts/**` (if present)
3. Target page template(s), usually:
   - `content/_index.zh-cn.md` (home page)
   - `content/_index.en.md` (home page)
4. [layout-checklist.md](references/layout-checklist.md)

## Non-negotiable layout rules

- Keep `article-header` and `article-main` in the same content column; do not let TOC width change content width.
- Treat desktop and mobile TOC as mutually exclusive modes; never allow both to be visible at the same breakpoint.
- Use one heading source of truth (`h2` only for TOC) and keep anchor ids/data-target consistent across all TOC variants.
- Keep desktop TOC independent from main flow (sidebar module), with sticky behavior on desktop only.
- Prevent content overflow regressions (tables/code blocks/long tokens).
- Do not introduce per-article hardcoded layout exceptions.

## Recommended implementation pattern

- Use explicit mode classes such as `*-mobile-only` and `*-desktop-only`.
- In desktop media query, force exclusivity with high-priority display rules.
- Keep sticky TOC in a dedicated sidebar column in desktop grid.
- Keep active-state script bound to shared `[data-toc-link]` attributes.
- Initialize TOC interaction only after DOM is ready.

## Validation baseline

- Run `hugo`.
- If layout or style changed, run `hugo server`.
- Verify at least one article page on desktop and mobile widths.
- Validate TOC visibility, sticky behavior, active highlight, and no extra whitespace gaps.

Follow the detailed acceptance checks in [layout-checklist.md](references/layout-checklist.md).
