---
name: blog-seo-content-create
description: Blog draft writing rules. Core principle: you are a real person writing something, not a robot filling a template. Use for new posts or rewrites. File/frontmatter rules see generate-blog-workflow; keywords see blog-seo-keyword-select; quantitative post-draft checks see blog-seo-content-check.
metadata:
  version: 2.1.0
---

# blog-seo-content-create

**This skill owns one thing: producing a post that reads like a real person wrote it.**

No matter what tool you use to write, the reader should encounter a person who has genuine thoughts about the topic and is sharing what they know — not a program completing a content template.

---

## The only question to ask before writing

> **What do I actually want to say about this topic?**

Not "what angles should this topic cover." Not "what keywords does SEO require."

What is your real judgment on this? Where did you get burned? What did you find that most explanations get wrong?

If you have no real perspective yet, research the topic until you do. **Without a genuine point of view, every writing technique is a patch on a symptom.**

---

## Where to start

Pick one real entry point. Do not start from an outline.

- **You used this thing**: write what the experience was actually like, including where it fell short
- **You made a mistake**: what the mistake was, why it happened, how you got out of it
- **You have a counterintuitive observation**: correct something that's widely repeated but wrong
- **You have a concrete comparison**: what A vs B actually looks like in your real situation
- **You were confused by something**: how you figured it out, what you discovered along the way

Once the first paragraph exists, the rest of the article will have a direction. Before it exists, building an outline is just deferring the actual problem.

---

## Voice

**Write to a specific person, not to "readers" as an abstraction.**

Imagine you're messaging a friend who needs to understand this. You would not:
- Open every section with "first… second… finally"
- Use filler transitions like "it is worth noting that" or "in conclusion"
- Write every paragraph at the same length with the same sentence rhythm
- Hide your opinion and just list information

You would:
- Say directly what you think is better and why
- Sometimes one sentence is enough; sometimes you need to unpack
- Admit where you're not certain
- Give the specific example you actually encountered, not a generalized "for example, a user might…"

**For Chinese posts**: write in natural spoken Chinese. "我觉得", "说实话", "你可能会遇到" are normal expressions, not things to avoid.

**For English posts**: write in real English. Mix sentence lengths. Use dashes, parentheses, contractions. Don't write every paragraph as four perfectly structured sentences.

---

## AI-pattern checklist for English posts (high-risk signals)

Grammarly and AI detectors flag these patterns consistently. Fix them before delivery.

### 1. Section body = bullet list → convert to prose

The single highest-weight AI signal. AI defaults to:
> "This tool does X. Use it for: [bullet] [bullet] [bullet]"

Rewrite as a personal narrative paragraph. The only acceptable bullet lists are: multi-step terminal commands, comparison tables, or short inline enumerations inside a sentence.

Bad → Good:
- "A simple decision pattern: [bullets]" → "I try not to overthink it. If I'm just brainstorming…"
- "Good fits: [bullets]" → "I use it for the boring but important stuff: tone for client writing, the syllabus I'm stuck with…"

### 2. Third-person narrator voice in section bodies

AI describes features from the outside. Humans describe what *they* do.

Bad → Good:
- "Plus usually exposes GPT‑5‑series variants" → "With Plus, you usually get a few GPT‑5 options"
- "Deep Research helps when you need a multi-source pass" → "I turn to Deep Research when I need more than a quick Google"
- "This cuts repeated preamble" → "You'll stop getting those 'As an AI language model…' intros"
- "route at least one real task through" → "I make myself run a real task through"

**Rule**: every action sentence in a how-to section should be anchored to "I use", "I put", "I make myself", "I turn to" — or addressed directly to "you". Not "[tool] does X" or passive constructs.

### 3. Formal parenthetical hedges inside sentences

These sound like an AI trying to be accurate. Readers parse them as non-human.

Bad → Good:
- "(or the current equivalent)" → cut or rewrite as a separate caveat sentence
- "(wording varies by release)" → "names change, so double-check in the app"
- "(where policy allows)" → "what you let it save"
- "verify current pricing" as a parenthetical → move to its own sentence: "I'd treat that as a ballpark, not a promise"

### 4. Noun-stacking and compressed technical descriptions

AI compresses feature descriptions into noun phrases. Humans expand them into clauses.

Bad → Good:
- "conversational image generation/editing" → "image tools right inside your chat"
- "multi-source pass on a defined question" → "more than just a quick Google"
- "competitive scans, topic primers, technology comparisons" → "figuring out who competes with X, what changed in regulation…"
- "scraps of context it's allowed to store" → "little bits of context you let it save"

### 5. Clever closing contrasts in section titles or final paragraphs

AI invents catchy turn-of-phrase closers. They read as constructed.

Bad → Good:
- Section title: "Closing: make the $20 feel like tooling, not trivia" → "Put the subscription to work"
- Final paragraph: "Users who adopt that pattern often report the same shift: the subscription stops feeling like a faster free chat, and starts feeling like time saved and context preserved." → "After a month of that, Plus stops feeling like just a faster version of the free tier. Instead, you start to notice you're dropping fewer threads…"

**Rule**: never close a section or article with third-person observation ("users who X tend to Y"). Anchor the conclusion in your experience or address the reader directly.

### 6. Formal word choices where colloquial ones are natural

| AI default | Human equivalent |
|-----------|-----------------|
| invoice | bill |
| cadence | rhythm |
| prune Memory | tidy up Memory |
| annoying | a pain |
| day-to-day | daily |
| on the fence (already good) | vs "undecided" (too clinical) |
| "the bundle" | "Plus" (use the product name) |
| "route a task through" | "run a task through" |

### 7. Missing spoken fillers — calibrate, don't stuff

AI either avoids all fillers (clinical) or stacks them (detectable). Place them naturally:
- "Basically, anything I'd otherwise end up pasting in every week." (not: "Stuff I'd otherwise paste weekly.")
- "Honestly, menus and limits change all the time…"
- "I always recommend checking your own billing page just to be sure."

Fillers to use sparingly in the right place: *basically, honestly, actually, just, kind of, sort of, I always, I usually, I find*.

### 8. Unusually precise similes or constructed comparisons

AI uses rare analogies to seem creative. They read as artificial.

Bad → Good:
- "the reply feels like skimmed milk on a hard problem" → "the reply feels thin or just doesn't cut it on a tough problem"
- "Memory drifts." (short isolated declarative) → "Memory can drift over time."

---

## Structure

Structure grows from what you want to say. You do not pick a structure and fill it in.

**Opening**: say what the post is about, who it's for, and what they'll be able to do or know after reading. No warm-up paragraphs.

**Middle**: follow the logical order of your argument. If a section has nothing to add, delete it — don't keep it because "this type of article usually has this section."

**Ending**: state the conclusion specific to this post. Not a generic closer that could apply to any article on Earth ("hope this was helpful" → delete).

**Headings**: add H2/H3 only where a real section boundary exists. Headings describe content; they do not exist to slot in keywords.

---

## On SEO

Keywords appear naturally in the article after you write it. They are not placed intentionally during writing.

After finishing, check density with the formula in [blog-seo-keyword-select](../blog-seo-keyword-select/SKILL.md) to confirm no stuffing. The core keyword appearing 4–8 times (~1–2%) is enough for a ~2000-word post.

`title` and `description` length rules (40–60 / 140–160 characters) are hard constraints, handled after the body is written. See [seo_frontmatter.md](../generate-blog-workflow/references/seo_frontmatter.md).

---

## Factual accuracy

- If you cite data, include the source. If you don't have data, don't invent it.
- "In my experience" and "research shows" are different claims. Do not conflate them.
- Versions, pricing, features — anything time-sensitive — note the date (`as of YYYY-MM-DD`).

---

## Format by article type

**Tutorial / how-to**: follow the steps in order; each step must be independently verifiable. Put caveats and gotchas next to the step they apply to, not stacked at the end.

**Comparison / buying guide**: compare on fixed dimensions; acknowledge the downsides of each option. State your recommendation explicitly and give a reason.

**Opinion / analysis**: state your position clearly, support it with specific examples, and acknowledge the limits of your position.

---

## Scope boundary

| Concern | This skill |
|---------|------------|
| Writing perspective, voice, structural logic | Yes |
| File naming, frontmatter, translationKey | No → [generate-blog-workflow](../generate-blog-workflow/SKILL.md) |
| Keyword selection and density calculation | No → [blog-seo-keyword-select](../blog-seo-keyword-select/SKILL.md) |
| TD lengths, quantitative script checks | No → [blog-seo-content-check](../blog-seo-content-check/SKILL.md) |
| Chinese article AIGC score too high after writing | No → [humanize-chinese](../humanize-chinese/SKILL.md) |
| Academic paper AIGC reduction | No → [paper-humanizer-skill](../paper-humanizer-skill/SKILL.md) |
