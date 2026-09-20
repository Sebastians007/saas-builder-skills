---
name: challenge-content-generator
description: >
  Use this skill to write a 5-day challenge funnel. Trigger when the user needs
  a challenge funnel, a 5-day challenge, a 7-day bootcamp, a daily email course,
  or any time-based sequence where participants complete one action per day
  building toward an outcome and an offer.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "challenge", "live-launch", "engagement"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# Challenge Content Generator

A challenge funnel is one of the highest-engagement funnels available. Participants
opt in for free, show up for 5 days, build a real result, and are primed to buy
by Day 5 because you've already proven you can help them. The key: the daily
content must be genuinely valuable, actionable, and build toward the Day 5 offer.

---

## Challenge Structure

### Registration Page
Standard opt-in structure with these challenge-specific elements:
- Headline promises a specific result in a specific timeframe
  > "Build Your First Marketing Funnel in 5 Days — Free"
- What they'll accomplish each day (5-line teaser)
- Social proof: number of past participants or beta result
- Urgency: challenge starts [DATE] / next round starts soon
- CTA: "Join the Challenge Free"

### Confirmation / Welcome Page
- Confirm registration
- Preview what Day 1 looks like
- Where the challenge happens (email / community / platform)
- "Invite a friend" prompt — challenges spread virally

### Daily Emails (Day 1–5)

**Each daily email structure:**
- Subject: "Day [X]: [Action title]" (keep consistent format for deliverability)
- Preview text: teases today's quick win
- Body:
  1. **Context opener** (2–3 sentences connecting to yesterday if Day 2+)
  2. **Today's lesson** (the core teaching — specific, actionable, no fluff)
  3. **Today's action** (one clear, completable task — must be doable in
     under 30 minutes)
  4. **Expected result** (what completing this task will produce)
  5. **Community prompt** (share your result / reply with a question)
  6. **Preview of tomorrow** (creates anticipation)

**Day arc (for a funnel-building challenge example):**
- Day 1: Define the offer (clarity before copy)
- Day 2: Write the hook + headline
- Day 3: Build the opt-in page
- Day 4: Write the email sequence
- Day 5: [Reveal] — now connect it all + here's how to launch it faster with [OFFER]

Adapt the arc to whatever the challenge topic is.

### Day 5 Pitch Email
The transition from free challenge to paid offer:
- Celebrate what they've accomplished
- Name the gap: "You now have [X]. What most people struggle with next is [Y]"
- Introduce the offer as the natural continuation
- This email is written like a story, not a sales email
- CTA to the sales/offer page

### Post-Challenge Follow-up (3 emails)
For those who didn't buy on Day 5:
- Email 1 (Day 6): Replay / resources from the challenge + offer reminder
- Email 2 (Day 8): One success story from a participant + offer
- Email 3 (Day 10): Final call — "Challenge is closing, offer going away"

---

## Output Format

```
# [Challenge Name] — 5-Day Challenge Funnel

## Registration Page
[Full page copy]

## Confirmation Page
[Full page copy]

## Day 1 Email
[Full email — subject, preview, body, CTA]

## Day 2 Email
[Full email]

...

## Day 5 Pitch Email
[Full email]

## Post-Challenge Follow-up Sequence
[3 emails]
```

---

## Rules
- Each day's action must be completable in under 30 minutes — if it's too hard,
  people drop off before the pitch
- The content must build on itself — Day 5 should feel like the natural result
  of Days 1–4
- Never pitch until Day 5 — trust is built through delivery, not teasing
- The offer should solve the exact problem the challenge revealed, not introduce
  a new one


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `funnel-builder-orchestrator` (S3-Funnel-Build) — the daily content is the core asset a Challenge-type funnel build is built around
- `email-sequence-generator` — daily challenge reminders and the post-challenge pitch sequence extend the content into email

### Fed By
- `offer-extraction` (S2-Audience-Positioning) — supplies the offer the challenge's final-day pitch should present
- `funnel-select` (S3-Funnel-Build) — confirms a challenge format fits the offer before content generation starts

### Feedback Loop
If day-to-day retention drops, the fix is usually the daily task's time-to-value, not the teaching content — check that each day delivers a quick win before rewriting the lesson material.

```yaml
chain_metadata:
  skill_slug: "challenge-content-generator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "funnel-builder-orchestrator"
    - "email-sequence-generator"
```
