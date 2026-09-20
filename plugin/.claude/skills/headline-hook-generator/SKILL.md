---
name: headline-hook-generator
description: >
  Use this skill to generate headline and hook variations for any marketing
  asset — landing pages, ads, emails, social posts, VSLs, or webinars. Trigger
  when a user needs multiple headline options, wants to A/B test copy, needs
  hook ideas, or asks for attention-grabbing openers for any offer.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "headlines", "hooks", "copywriting"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Headline + Hook Generator

The headline is the most leveraged sentence in any funnel. A 10% improvement in
headline performance lifts the entire funnel. Generate 15–20 variations across
every psychological category so the user has real options to test.

---

## Headline Categories to Cover

For every offer, produce at least 2–3 variants in each category:

### 1. Direct Benefit / Outcome
State exactly what the reader gets. No cleverness. Just clarity.
> "Get a Complete Marketing Funnel Written in One Session"

### 2. Curiosity / Open Loop
Create a question they need answered.
> "The 11-Minute Funnel Strategy Most Marketers Have Never Tried"

### 3. Social Proof / Numbers
Anchor with specificity.
> "3,400 Agency Owners Built Their Funnels With This"

### 4. Problem / Fear of Loss
Speak to the pain or what they're risking by not acting.
> "Why Most Funnels Die Before They Make a Dollar (And How to Fix Yours)"

### 5. How-To / Formula
Promise a process.
> "How to Write a 7-Page Funnel From Scratch in Under 90 Minutes"

### 6. Bold Claim / Contrarian
Challenge conventional wisdom.
> "You Don't Need a Copywriter. You Need a System."

### 7. "If / Then" Conditional
Qualify the reader while making the promise.
> "If You Can Answer 6 Questions About Your Offer, I Can Build Your Entire Funnel"

### 8. Story Hook (for emails, VSLs, webinars)
Drop the reader into the middle of a story.
> "At 11:47 PM the night before launch, everything I'd built was gone."

---

## Hooks (for VSL, webinar, video, social)

Hooks are the first 5–15 seconds of a video or the first line of a post.
Produce 10 hook variants for the offer.

Hook formats:
- **Question hook:** "What would you do if you could write an entire funnel in one afternoon?"
- **Confession hook:** "I spent $11,000 on a copywriter before I figured this out."
- **Bold statement hook:** "Most funnels fail before the first page is written."
- **Contrast hook:** "Same offer. Same traffic. Two completely different results. Here's why."
- **Result hook:** "My client went from zero leads to 400 opt-ins in 8 days."

---

## Output Format

```
# Headlines — [Offer Name]

## Direct Benefit
1. [headline]
2. [headline]
3. [headline]

## Curiosity
1. [headline]
...

## [Category]
...

---

# Hooks — [Offer Name]

1. [hook type] — [hook copy]
2. [hook type] — [hook copy]
...
```

---

## Rules
- Never use passive voice in headlines
- Avoid corporate buzzwords: "solutions," "leverage," "synergy," "empower"
- Specificity always beats vagueness: "12 pounds" beats "weight loss"
- Write for skimmers — the meaning should land in under 3 seconds
- Subheadlines should support, not repeat, the main headline


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `landing-page-generator` — supplies the primary headline the page opens with
- `social-content-pack` — supplies hooks used as post openers and video hooks
- `vsl-script-generator` — supplies the opening hook the script's first 30 seconds is built around

### Fed By
- `headline-matrix` (S10-Copywriting) — supplies proven headline formulas and structures this skill's outputs are variants of
- `avatar-extraction` (S10-Copywriting) — supplies the pains and desires the hooks need to target

### Feedback Loop
Track which generated headlines actually get used and which get discarded — feed winning patterns back into future generations for the same avatar rather than starting from a blank formula list each time.

```yaml
chain_metadata:
  skill_slug: "headline-hook-generator"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "landing-page-generator"
    - "vsl-script-generator"
    - "social-content-pack"
```
