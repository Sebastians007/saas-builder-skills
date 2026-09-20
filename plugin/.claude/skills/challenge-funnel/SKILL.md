---
name: challenge-funnel
description: >
  Builds a 3-7 day challenge funnel that engages participants with daily
  micro-wins and community momentum, then presents a paid offer when
  engagement peaks, for mid-ticket offers ($197-$997).
  Use this skill when the user asks about running a challenge to sell a
  product, or says
  "I want to run a 5-day challenge", "build me a challenge funnel", "how do I structure daily challenge content",
  "sell my course through a challenge", "help me build momentum before pitching my offer",
  "what should each day of my challenge cover".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "challenge", "community", "mid-ticket"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Challenge Funnel

Builds momentum through daily small wins over 3-7 days, then presents the paid offer at the moment engagement and trust are highest. Works especially well when there's an existing engaged audience (social following, small list) since the challenge format thrives on community and shared progress.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is $197-$997 and community/cohort dynamics fit the audience
- There's an existing engaged audience willing to commit a few days of attention
- `funnel-select` recommended `challenge-funnel` for a mid-ticket, community-based offer
- The founder wants an alternative to a single-event webinar pitch that builds deeper trust over several days

## Input Schema
```
challenge_name: string
challenge_length_days: number      # 3, 5, or 7
daily_themes: [ { "day": number, "title": string } ]
community_platform: string?        # Facebook group, Discord, Skool, etc. for accountability
offer_name: string
offer_price: number
offer_reveal_day: number           # typically final day or day after
```

## Workflow
### Step 1: Pick the length based on topic depth
3 days for quick wins/simple topics (highest completion rate), 5 days for skill-building (best balance), 7 days for complex transformations (deepest engagement but lower completion). Match `challenge_length_days` to the actual complexity of what's being taught, not just what feels ambitious.

### Step 2: Write the registration page
Captures email and adds to the challenge community group if `community_platform` is set. Sets clear expectations: what each day covers, time commitment per day, and what the paid offer will be about (seed it here — don't hide it).

### Step 3: Structure each daily page
Day badge ("Day 3 of 5"), daily theme/title, training content (10-20 min), one specific completable action step, a completion CTA (mark complete / share in community), and a preview of tomorrow to build anticipation.

### Step 4: Write the offer page and reveal timing
Present the offer on `offer_reveal_day` (typically the final day or immediately after), building on momentum from the challenge itself — the pitch should feel like a natural continuation, not an ambush.

### Step 5: Write the full email sequence
Welcome → daily unlock + evening reminder for each day → midpoint check-in → final day build-up → offer email → 24hr social-proof reminder → cart close.

### Step 6: Self-Validation
- [ ] Challenge length matches topic complexity, not just ambition
- [ ] The offer is seeded from Day 1, not sprung as a surprise on the final day
- [ ] Each daily action step is completable in 15-30 minutes
- [ ] Community/accountability mechanism is specified if used
- [ ] Cart close has a real deadline, not an indefinitely "limited time"

## Output Schema
```
{
  "registration_page": object,
  "daily_pages": [ { "day": number, "title": string, "action_step": string } ],
  "offer_page": object,
  "email_sequence": [ { "timing": string, "purpose": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# Challenge Funnel: <Challenge Name> (<length>-Day)

## Flow
Registration → Daily Challenge Pages (Day 1-<N>) → Offer Page → Thank You

## Registration Page
<copy>

## Daily Pages
| Day | Theme | Action Step |
|---|---|---|

## Offer Page (Day <offer_reveal_day>)
<copy>

## Email Sequence
| Email | Timing | Purpose |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Registration rate | > 40% |
| Day 1 completion | > 70% |
| Overall reg → purchase | > 3% |
```

## Error Handling
- If `daily_themes` don't build toward `offer_name` logically, flag the disconnect — each day should seed the eventual offer, not feel unrelated to it.
- If `challenge_length_days` is outside 3-7, ask why — shorter feels incomplete, longer typically tanks completion rates without a very engaged audience.
- If no community/accountability mechanism exists, warn that completion rates drop significantly without one and suggest at minimum a shared hashtag or comment thread.
- If the offer reveal happens before day 2 or 3, flag that this undercuts the "build momentum first" premise of the format.

## Examples
**Example 1:** A SaaS founder runs a free "5-Day Automate Your Onboarding Challenge" to sell a $497 implementation package. Each day covers one automation concept with a completable action step in the app itself, seeding the paid "done-for-you" package from Day 1.

**Example 2:** A fitness coach runs a 3-day "Quick Win" challenge (simple topic, highest completion target) to sell a $197 program, using a Facebook group for daily accountability posts.

**Example 3:** A GRC consultant runs a 7-day "SOC 2 Readiness Sprint" challenge to sell a $997 compliance audit-prep package, given the topic's genuine complexity justifies the longer format, accepting a lower completion rate in exchange for deeper trust-building with serious prospects.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/challenge-day-page.html`

## Flywheel Connections
### Feeds Into
- `funnel-copy` — writes daily page copy and the offer reveal pitch
- `signup-conversion-tracker` (S7-Growth) — measures registration and completion rates
- `group-funnel` — if the challenge's community component becomes an ongoing group

### Fed By
- `funnel-select` — confirms challenge format fits the price point and audience
- `optin-funnel` — existing list is often the challenge registration source

### Feedback Loop
If day-3+ completion drops sharply, the daily action steps are likely too large or vague — tighten each to something completable in under 30 minutes before assuming the topic itself is the problem.

```yaml
chain_metadata:
  skill_slug: "challenge-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "signup-conversion-tracker"
```
