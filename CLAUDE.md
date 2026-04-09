# Repository Collaboration Guide (Claude Code / Workspace Agent)

This file is the **skill index and task routing guide**. Detailed rules live in each skill's `SKILL.md`.

## Language Rule for All SKILL.md Files

**All SKILL.md files in this repository must be written in English only.**

- Instructions, rules, section headings, descriptions, comments — all English
- Exception: `humanize-chinese` Chinese detection word lists (高危模式, 机械连接词, etc.) stay in Chinese because they are data, not instructions
- When editing or creating any SKILL.md, if you write a non-English sentence in the instruction/rule sections, rewrite it in English before saving
- Mixed-language SKILL.md files must be converted to English on next edit

---

## Blog Pipeline (Hugo + Blowfish, `content/**`)

**Standard writing workflow (in order):**

1. `.agents/skills/blog-seo-keyword-select/SKILL.md` — Core keyword, long-tail expansion, Reddit/X operators, Google Trends
2. `.agents/skills/blog-seo-content-create/SKILL.md` — **Writing starting point**: real perspective, voice, structural logic
3. `.agents/skills/blog-seo-content-check/SKILL.md` — Post-draft quantitative check: TD lengths, structure metrics, `article_seo_eval.py`

**Framework and file rules (always load):**

- `.agents/skills/generate-blog-workflow/SKILL.md` — File naming, multilingual, `translationKey`, frontmatter, build validation

**Load on demand (only when explicitly needed):**

| Scenario | Skill | Trigger condition |
|----------|-------|-------------------|
| Chinese article scores >50 on external AI detector | `.agents/skills/humanize-chinese/SKILL.md` | Post-hoc AIGC reduction only |
| Academic paper / thesis | `.agents/skills/paper-humanizer-skill/SKILL.md` | Academic writing only — not for blog posts |
| Site-wide / technical SEO, indexation, CWV | `.agents/skills/seo-audit/SKILL.md` | Technical issues, unrelated to writing |
| AI answer citations, extractable blocks | `.agents/skills/ai-seo/SKILL.md` | AI search visibility goal |
| Article quantitative eval script | `.agents/skills/scripts/ARTICLE_SEO_EVAL.md` | When running the script |

**Key principle:** `humanize-chinese` and `paper-humanizer-skill` are **not part of the default blog workflow**. Do not auto-invoke them for every article. If an article comes out AI-sounding, the root cause is step 2 (writing starting point), not something step 3 can fix.

---

## Cursor Rules

`.cursor/rules/` rules coexist with this file. On conflict, the **user's current task** and **in-repo SKILL.md** take precedence.

## Without Workspace Tools (e.g. Grok)

When repo files are not accessible: paste the relevant `SKILL.md` excerpt from the table above into the conversation or system prompt. Do not rely on auto-loading.
