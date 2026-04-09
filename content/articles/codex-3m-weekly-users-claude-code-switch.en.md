---
title: "Codex Hits 3M Weekly Users: Why Devs Are Switching"
headline: "Codex at 3M WAU: Why Claude Code Users Are Moving"
description: "Codex reached 3M weekly users, and Sam Altman tied limit resets to every +1M users up to 10M. This article explains why many Claude Code users are switching."
summary: "Codex moved from fast growth to mainstream in months. The biggest reason is not hype, but independent usage limits and a smoother path for long autonomous coding runs."
date: 2026-04-09
lastmod: 2026-04-09
updatedDate: 2026-04-09
featureimage: "images/codex-blow-claude-code.webp"
translationKey: "codex-3m-weekly-users-claude-code-switch"
locale: "en"
robots: "index,follow,max-image-preview:large"
showSummary: true
showTableOfContents: true
categories: ["AI Coding", "Industry Analysis"]
tags: ["Codex", "Claude Code", "OpenAI", "Anthropic", "Developer Tools"]
---

So, on April 7, 2026, I saw Sam Altman (OpenAI’s CEO) post on X about Codex hitting 3 million weekly active users. To celebrate, OpenAI reset everyone’s usage limits—and promised to do so again for every additional million users, up to 10 million. Honestly, that’s a pretty bold move.

That post did more than trend. It confirmed that Codex has become one of the fastest-rising coding AI products in 2026. From breaking one million downloads in its first Mac app week to scaling weekly active users from around 1.6M to 3M, Codex moved from momentum to mainstream in just a few months.

## How shocking is Codex's growth speed?

Codex isn’t just a code-completion tool anymore. Now, it’s more like a full-on coding agent—think GPT-5.3 level smarts, plus its own desktop workflow (starting with Mac, but I’m guessing other platforms are coming soon).

Officially reported highlights repeatedly referenced by the community include:

- Weekly active users have roughly tripled in 2026.
- The Mac app passed 1 million downloads in its first week, while total token usage rose about 5x.
- Internally, OpenAI has stated very high engineering adoption, with a notable increase in PR output per engineer.

What really stands out to me isn’t just how good the model is, but the policy behind it. Sam Altman’s promise to reset limits every time another million users join is a direct answer to the frustration developers feel about hitting usage caps. If you’re a heavy user, this means you can actually get through a full day of building without that constant worry about running out of quota.

## Claude Code vs Codex: real 2026 daily workflow comparison

In 2026, the most-discussed matchup is still Anthropic’s Claude Code (terminal-native, highly collaborative) vs OpenAI’s Codex (cloud sandbox, highly autonomous).

Both are top-tier coding AIs, but quota mechanics, user experience, and best-fit scenarios differ significantly.

| Dimension                             | Claude Code (Pro/Max)                                                                                    | Codex (ChatGPT Plus/Pro)                                                                              | Who wins?                        |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------- |
| **Are quotas independent?**           | **Shared pool** across Claude web/desktop/mobile and Claude Code usage                                   | **Independent pool** separated from regular ChatGPT chat/media usage                                  | **Codex (clear win)**            |
| **How limits are calculated**         | 5-hour rolling window + weekly active compute cap; long threads, tool calls, and big repos drain quickly | 5-hour windows + task-dependent consumption; from April some plans move toward token-based accounting | Codex is often easier to predict |
| **Heavy coding burn rate**            | Fast; many heavy users can hit limits within days                                                        | Moderate; independent quota + temporary higher rate limits in this phase                              | **Codex**                        |
| **What happens after you hit limits** | Extra Usage, pay-as-you-go, or upgrade to higher Max tiers                                               | Mostly wait for reset windows plus growth-triggered reset policy                                      | Codex feels smoother             |
| **Coding style and efficiency**       | Strong reasoning and high design fidelity for exploratory work                                           | Production-ready execution, stronger autonomous delivery, concise throughput                          | Depends on task                  |
| **Best-fit scenario**                 | Ambiguous requirements, iterative debugging, high human-in-loop control                                  | Clear specs, long autonomous tasks, batch delivery, cloud parallelism                                 | Codex for "true production runs" |

From what I’ve heard (and experienced myself), a lot of developers are switching from Claude Code to Codex for one big reason: you can actually code for longer stretches without getting interrupted by limits.

The main gripe I keep hearing about Claude Code is the shared quota thing. If you use up your daily chat allowance, your coding time gets cut short—and the other way around, too. Codex doesn’t have that problem. Its quota is separate, so you don’t get hit with that annoying ‘chat tax’ if you’re building something big.

## What does a 5-hour rolling window actually mean?

A 5-hour rolling window is a personal burst limit. It is not tied to fixed clock resets.

How it works:

- The timer starts when you send your first prompt.
- Example: if your first message is at 10:00, your window runs until 15:00.
- You consume your quota within that period.
- At the end of the window, quota resets and a new cycle begins.

In practice, how fast you burn through your quota really depends on what you’re doing. If you’re working on something complex or using a lot of tokens, you’ll hit the limit faster. Simpler tasks? You’ll probably last longer.

### Why some users burn through limits quickly

- **Long context chains:** each turn can reprocess large histories.
- **Task type:** large repos, multi-file edits, autonomous agent loops, and heavy tool usage cost far more than simple Q&A.
- **Model choice:** higher-intensity models tend to consume faster.
- **Peak periods:** high-load windows can affect practical limits.
- **Shared pools:** all Claude surfaces can draw from one overall budget for many plans/users.

### Weekly cap on top of rolling windows

But here’s the catch: there’s also a 7-day rolling weekly cap. So even if your 5-hour window keeps resetting, if you’re really pushing it, you might still run into a weekly limit after a few days.

### Practical user tactics

- **Window warming:** start a light prompt before your intended deep-work block to shift reset timing.
- **Monitoring:** use `/status` in Claude Code and other tracking methods to watch remaining usage.
- **When capped:** wait for reset, enable extra usage, move to pay-as-you-go, or upgrade to higher Max tiers.

## Price and value: same $20 tier, very different experience

At similar entry pricing, the winner in user perception is often the one that provides more uninterrupted coding time.

- **Claude Pro (~$20/month):**
  - Can feel tight for heavy coding users.
  - After limits, users may rely on Extra Usage/pay-as-you-go or move to higher Max tiers.
  - Still strong on deep single-response reasoning in exploratory tasks.

- **ChatGPT Plus + Codex ($20/month):**
  - Codex is included for eligible usage paths and treated as independent in workflow planning.
  - In the current phase, limit policies have felt more generous to many heavy users.
  - Core advantage: smoother long-run coding continuity.

Bottom line at the same price point: many developers currently read Codex as the higher "work completed per dollar" option.

## Why Codex is rising fast right now

Three forces reinforce each other:

1. **Direct painkiller:** independent quota behavior plus growth-triggered resets reduce interruption.
2. **Workflow ecosystem:** desktop app + CLI + cloud sandbox create a more complete delivery loop.
3. **Growth flywheel:** more users -> looser practical limits -> better UX -> more users.

To me, Sam Altman’s post wasn’t just a celebration—it was a clear sign that OpenAI wants Codex to become the go-to platform for developers.

Honestly, in 2026, coding AI isn’t just a sidekick anymore—it’s a core part of how we actually get things done. Claude Code is still a strong choice, but Codex is winning people over fast because it’s just easier to use for long, uninterrupted sessions.

Happy coding—and if you try out Codex, let me know how it goes for you!
If you’re coding every day, now’s the perfect time to give Codex a real test drive on your own projects.

<div class="cta-center familypro-cta">
  <a
    class="cta-pill cta-pill--familypro"
    href="https://familypro.io/en/products/chatgpt?invite=HJa89c5c&promo=qyyx"
    target="_blank"
    rel="noopener"
    aria-label="Enjoy Codex at a Low Price">
    🚀 Enjoy Codex at a Low Price  →
  </a>
</div>

## References

- <a href="https://x.com/sama/status/2041658719839383945" rel="nofollow">Sam Altman on Codex reaching 3M WAU</a>
- <a href="https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan" rel="nofollow">Using Claude Code with Pro or Max</a>
- <a href="https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work" rel="nofollow">Claude usage and length limits</a>
- <a href="https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan" rel="nofollow">Using Codex with your ChatGPT plan</a>
