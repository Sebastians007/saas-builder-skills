---
name: webinar-script-generator
description: >
  Use this skill to write a webinar script or outline. Trigger when the user
  needs a webinar script, webinar outline, live training script, online workshop
  script, masterclass outline, or automated webinar script. This skill produces
  a complete webinar structure with word-for-word scripts for the critical sections.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "webinar", "script", "live-presentation"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# Webinar Script Generator

A great webinar does two things simultaneously: genuinely teaches something
valuable AND builds the case for the offer. The best webinars feel like the
content *is* the sales pitch — because the teaching creates the desire.

---

## Webinar Structure (with timing for a 60–90 minute event)

### SECTION 1 — PRE-WEBINAR / HOLDING ROOM (0:00 – 5:00)
While people are joining:
- Loop slide: event title + promise
- Chat engagement: "Where are you joining from?" / "What's your #1 question?"
- Countdown or "we start in 2 minutes" energy
- Provide the holding room script (30 seconds of spoken welcome)

### SECTION 2 — OPEN / HOOK (5:00 – 10:00)
The most critical segment. Must accomplish:
1. Confirm they're in the right place ("This is for you if...")
2. Make a bold promise for what they'll learn today
3. Create social proof immediately (who you've helped / your results)
4. Give a "stay to the end" hook — tease the bonus or special offer
5. Set the agenda (briefly — 3 bullet points max)

Provide **word-for-word script** for this section.

### SECTION 3 — CREDIBILITY / YOUR STORY (10:00 – 18:00)
Not a bio — a relatable origin story:
- Where you were before (the struggle they recognize)
- The moment of discovery or turning point
- What changed and what you built
- Why you're doing this webinar today

Keep it brief. The audience is here to learn, not to hear a long origin story.
Provide **word-for-word script** for this section.

### SECTION 4 — CONTENT / TEACHING (18:00 – 50:00)
The heart of the webinar. Structure: 3 core lessons or pillars.

For each pillar:
- Name it clearly ("The first thing you need is...")
- Teach the concept (real, actionable, not watered-down)
- Show a quick example or mini case study
- Connect it to a result they want
- Transition to the next pillar

Provide:
- Full word-for-word script for ALL 3 pillars

Do NOT use outline-level for pillars 2 and 3. Presenters using this for
automated webinars need all content fully scripted. Each pillar runs
10-12 minutes; write enough copy to fill that time substantively.

The teaching must create the desire for the offer without mentioning the offer.
Each pillar should naturally reveal a gap that the offer fills.

### SECTION 5 — TRANSITION TO OFFER (50:00 – 55:00)
The bridge between teaching and selling. The most important few sentences in the
webinar. This transition must feel earned, not jarring.

Formula:
> "Now, everything I've taught you today works. And you could go implement this
> yourself. But if you want [RESULT] without [STRUGGLE], I've built something
> that does all of this for you..."

Provide **word-for-word script** for this section.

### SECTION 6 — OFFER PRESENTATION (55:00 – 70:00)
Present the offer with full clarity:
- What it is (name + one-sentence description)
- What's included (walk through each component)
- Who it's for / who it's not for
- Value stacking (what each piece is worth separately)
- Bonuses
- Guarantee
- Price + payment options
- What happens when they click the button

Provide **word-for-word script** for this section.

### SECTION 7 — Q&A + CLOSE (70:00 – 90:00)
- Answer pre-selected questions (anticipate the top 5 objections)
- Weave offer reminders into every answer
- Hard close at 80 minutes: "We have 10 minutes left — if you're ready, go
  click the button now"
- Final close at end: restate promise + deadline if applicable

Provide the **top 5 anticipated objections with scripted answers**.

---

## Output Format

```
# Webinar Script — [Offer Name / Webinar Title]
**Event Duration:** [60 / 75 / 90 minutes]
**Format:** [Live / Automated / Hybrid]

---

## PRE-WEBINAR [0:00–5:00]
[Slide direction + spoken script]

## OPEN / HOOK [5:00–10:00]
[Full word-for-word script]

## CREDIBILITY [10:00–18:00]
[Full word-for-word script]

## CONTENT — PILLAR 1 [18:00–30:00]
[Full word-for-word script]

## CONTENT — PILLAR 2 [30:00–42:00]
[Full word-for-word script]

## CONTENT — PILLAR 3 [42:00–50:00]
[Full word-for-word script]

## TRANSITION [50:00–55:00]
[Full word-for-word script]

## OFFER [55:00–70:00]
[Full word-for-word script]

## Q&A + CLOSE [70:00–90:00]
[Top 5 objections with scripted answers + closing script]

---

## Slide Notes
[Slide-by-slide guidance]
```

---

## Rules
- The teaching content must be genuinely useful — do not withhold value to "save it for the offer"
- The pitch must feel like a natural conclusion of the teaching, not a gear shift
- Never say "I'm not selling anything today" if you are — audiences hate this
- Match speaking style to the presenter's brand voice
- `[PRICE]` for any price not confirmed; never invent numbers


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `funnel-builder-orchestrator` (S3-Funnel-Build) — the script is the core content asset a Webinar-type funnel's registration and attendance flow is built around
- `email-sequence-generator` — the script's close/offer stack drives the post-webinar follow-up sequence

### Fed By
- `offer-extraction` (S2-Audience-Positioning) — supplies the offer and pricing the script's close must present
- `avatar-extraction` (S2-Audience-Positioning) — supplies the audience pains the script's story and content sections need to address

### Feedback Loop
If attendees stay to the end but don't buy, the fix is usually the offer stack and close, not the content teaching — check the last 10 minutes of the script before rewriting the teaching section.

```yaml
chain_metadata:
  skill_slug: "webinar-script-generator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "funnel-builder-orchestrator"
    - "email-sequence-generator"
```
