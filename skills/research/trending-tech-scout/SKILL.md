---
name: trending-tech-scout
description: >
  Scouts trending frameworks, tools, and AI capabilities worth building with
  right now, so a tech stack choice doesn't get outdated fast.
  Use this skill when the user asks about "what's new and worth using",
  or says
  "what's trending in web dev right now", "is there a better way to build this now",
  "what AI tools should I be using in my app", "am I about to build on something outdated",
  "what's the new hotness in [category]", "should I use the new version of [framework]",
  "what should I know about before I commit to a stack".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "trends", "ai-tools", "tech-scouting"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Trending Tech Scout

This skill surveys what's currently trending and genuinely worth adopting in frameworks, hosting, AI capabilities, and dev tooling — filtered hard against hype, so a founder gets a short list of things that will actually help them ship faster or make a better product, not a list of everything new. It exists because the field moves fast and a stack decision made on 18-month-old defaults can leave real capability (especially AI capability) on the table.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Before or during `tech-stack-finder`, as a freshness check on the recommendation
- Founder heard about a new tool/framework and wants to know if it's worth switching to
- Periodically, to check whether an existing app is missing a new capability worth adding (e.g. a new AI model capability that changes what's buildable)
- Founder wants to know what capability level is now achievable that wasn't a year ago (relevant for AI-wrapper SaaS specifically, where model capability changes what the product can promise)
- Deciding whether to build a feature in-house or whether a new tool/API now does it well enough out of the box

## Input Schema
```
category_of_interest: string (required) — e.g. "frontend frameworks", "AI coding tools", "auth providers", "AI video/image generation", or "general" for a broad scan
current_stack: string[] (optional) — what the user is already using, to check for staleness specifically
purpose: enum [choosing-new-stack, checking-existing-stack-freshness, exploring-new-capability] (default: choosing-new-stack)
```

## Workflow
### Step 1: Search for genuinely current signal
Use web_search for recent (last 3-6 months, check dates explicitly since training data can be stale) developments in `category_of_interest` — new framework releases, notable GitHub trending repos, new model releases/capability jumps from major AI labs, and hosting/infra platform changes. Always check publish dates on results; do not present outdated "new" claims as current.

### Step 2: Filter hard against hype
For each trend found, apply three filters before including it: (1) is it stable enough for a solo/small-team founder to build on today, not a beta/preview with breaking changes expected, (2) does it solve a real problem the founder likely has, not novelty for its own sake, (3) is there real adoption evidence (companies shipping with it, not just launch-day hype threads). Cut anything that fails any filter — the output should be a short, trustworthy list, not a comprehensive trend report.

### Step 3: Check for AI-capability shifts specifically
For AI-adjacent products, explicitly check: has a new model or API capability recently made something newly possible or newly cheap that wasn't before (e.g. longer context windows, cheaper inference, new modality support)? This category moves fastest and most directly changes what's worth building, so it deserves its own explicit check even under `category_of_interest: "general"`.

### Step 4: Compare against `current_stack` if provided
If the founder already has a stack, explicitly flag: anything meaningfully outdated (security-relevant, end-of-life, or missing capability now standard elsewhere), and anything that's fine to keep (churn for its own sake wastes time — "still good, no need to switch" is a valid and common finding, say it plainly).

### Step 5: Give a clear adopt/watch/ignore verdict per item
For each surfaced trend: **Adopt now** (stable, solves a real problem, worth switching/adding today), **Watch** (promising but not yet stable enough to bet a solo founder's build on), or **Ignore** (hype, doesn't fit non-technical/small-team builders, or solves a problem the founder doesn't have).

### Step 6: Self-Validation
- [ ] All findings are date-checked and genuinely recent, not stale training-data claims presented as new
- [ ] Hype filter was actually applied — list is short and high-confidence, not exhaustive
- [ ] AI capability shifts were explicitly checked, not skipped
- [ ] If `current_stack` given, a direct freshness comparison was made
- [ ] Every item has a clear Adopt/Watch/Ignore verdict, not just a description

## Output Schema
```
{
  category: string,
  findings: [{ name: string, what_it_is: string, verdict: enum [adopt, watch, ignore], why: string, source_recency: string }],
  stack_freshness_check: string | null
}
```

## Output Format
```markdown
# Trending Tech Scout: <category>

## Worth Adopting Now
- **<tool/framework>**: <what it does>, <why it's worth adopting today>

## Worth Watching (not yet stable enough to bet on)
- **<tool/framework>**: <what it is>, <why to wait>

## Not Worth It (filtered out)
- <name>: <why it's hype/doesn't fit>

## Your Current Stack Freshness Check
<if current_stack given: what's fine to keep, what's genuinely worth updating and why>

## Next Step
Run `tech-stack-finder` to fold any "adopt now" findings into a concrete stack recommendation, or `architecture-decision-writer` to document a switch decision.
```

## Error Handling
- If web_search results are ambiguous on recency (can't confirm something is genuinely current), say so explicitly rather than presenting stale information as fresh.
- If nothing meaningfully new exists in `category_of_interest` right now, say that plainly — "nothing new worth switching for" is a legitimate and useful finding, don't manufacture trends to fill the output.
- If the founder's `current_stack` is already current/fine, don't invent reasons to recommend a change — confirm it's solid and move on.
- If a trend is genuinely exciting but requires `experienced-dev` skill level to adopt safely, flag that clearly so a non-technical founder doesn't get talked into something unstable.

## Examples
**Example 1**
User: "Is there a better way to add AI chat to my app than what I used 8 months ago?"
→ Skill checks recent model/API releases, finds relevant capability or pricing shifts (checking dates carefully), verdicts each as adopt/watch/ignore, and gives a specific plain-language recommendation on whether to migrate.

**Example 2**
User: "current_stack: Next.js 13, Firebase, category_of_interest: general"
→ Skill checks for meaningful framework/infra movement since, flags anything end-of-life or missing standard capability, confirms what's still fine to keep, avoids recommending churn without real justification.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `tech-stack-finder` (S1-Research) — adopt-now findings become candidate stack components
- `architecture-decision-writer` (S5-Planning) — documents a decision to switch or adopt something new
- `tech-debt-detector` (S5-Planning) — freshness findings can flag components as debt-in-waiting

### Fed By
- `tech-stack-finder` (S1-Research) — an existing stack recommendation can be checked here for freshness before finalizing

### Feedback Loop
If an "adopt now" recommendation later causes friction found by `tech-debt-detector`, that outcome should raise the bar for what counts as "stable enough" in future scouting verdicts for similar tools.

```yaml
chain_metadata:
  skill_slug: "trending-tech-scout"
  stage: "research"
  timestamp: string
  suggested_next:
    - "tech-stack-finder"
    - "architecture-decision-writer"
```
