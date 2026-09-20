---
name: vsl-script-generator
description: >
  Use this skill to write a Video Sales Letter (VSL) script for a marketing
  funnel. Trigger when the user needs a video sales letter, a sales video script,
  a VSL for their landing page, a video pitch, or a talking-head sales video
  script. VSLs are typically 10–20 minutes long and follow a specific narrative
  structure to build trust and drive conversions.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "vsl", "video-sales-letter", "script"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# VSL Script Generator

A VSL is the highest-leverage video a business can create. Done right, it
replaces a full sales conversation. It hooks attention, builds trust through
story, presents an irresistible offer, and drives action — all before the viewer
talks to a single human.

---

## VSL Structure (with timing)

### SECTION 1 — HOOK (0:00 – 1:00)
The first 60 seconds determine if they watch the rest. Options:

- **Bold claim hook:** State the biggest promise immediately
- **Story hook:** Drop into a scene ("Six months ago I was about to quit...")
- **Question hook:** Ask the most important question your prospect has
- **Contrarian hook:** Challenge what they've been told

The hook must accomplish three things:
1. Identify the exact person this is for
2. Make a promise worth 10 minutes of their time
3. Create enough curiosity to keep watching

### SECTION 2 — PROBLEM (1:00 – 3:00)
Make them feel understood before you try to help them. Describe their situation
in more detail than they could describe it themselves. Cover:
- The surface problem (what they're experiencing)
- The root cause (why it keeps happening)
- The cost of inaction (what it's costing them now)

### SECTION 3 — CREDIBILITY BRIDGE (3:00 – 5:00)
Who are you and why should they listen? This is NOT a resume. It's a story:
- Where you were (relatable starting point)
- What you discovered or built
- The result that changed everything
- Your mission to help others get the same result

### SECTION 4 — SOLUTION REVEAL (5:00 – 8:00)
Introduce the mechanism — the unique approach, method, or system:
- What it is (name it if possible)
- Why it works when other things don't
- How it's different from what they've tried
- A simple framework or process visual (describe for slides)

### SECTION 5 — PROOF (8:00 – 11:00)
Stack believable evidence:
- Case studies: name, situation, result (use `[CASE STUDY]` if none provided)
- Testimonials: specific, outcome-focused (use `[TESTIMONIAL]` if none provided)
- Your own results
- Logic proof (explain *why* it works, not just *that* it works)

### SECTION 6 — OFFER PRESENTATION (11:00 – 15:00)
Present everything they get:
- Name the product/program/service
- Walk through each component + the benefit of each
- Price anchor (what it would cost to get this elsewhere)
- Investment reveal
- Payment options if applicable
- Bonuses (stack the value)
- Guarantee (reduce risk completely)

### SECTION 7 — CTA + CLOSE (15:00 – end)
- Tell them exactly what to do next (click below, fill out the form, etc.)
- Restate the core promise
- Future pace — paint the picture of their life after
- Final urgency if applicable
- Repeat the CTA

---

## Output Format

Provide the complete script with:
- Section headers and timing markers
- Stage directions in *italics* (where to cut to slides, show graphics, etc.)
- Every word written out — no bullet points in the script itself
- Estimated total runtime at the top
- Notes on slide/visual suggestions at the end

```
# VSL Script — [Offer Name]
**Estimated Runtime:** [X–Y minutes]

---

## HOOK [0:00–1:00]
[Full script text]
*[Stage direction]*

## PROBLEM [1:00–3:00]
[Full script text]
...

---

## Visual / Slide Notes
- [Slide suggestions per section]
```

---

## Rules
- Write in the speaker's natural voice — ask for tone if not established
- Short sentences for the hook and CTA; longer for the credibility and proof sections
- Never use `[PRICE]` in the middle of the script — always confirm price first; if not
  provided, use `[PRICE]` and note it in Page Notes
- Avoid jargon unless the audience uses it themselves
- Every section should naturally lead to the next — no abrupt transitions


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `vsl-funnel` (S3-Funnel-Build) — the script is the core asset the VSL funnel's landing page and video player are built around
- `landing-page-generator` — the VSL page wraps the script with a headline, video player, and CTA button

### Fed By
- `offer-extraction` (S2-Audience-Positioning) — supplies the offer the script's close must present
- `schwartz-awareness-mapper` (S2-Audience-Positioning) — determines which awareness-level opening the script should use

### Feedback Loop
If watch-time drops off early, the fix is the hook in the first 30 seconds, not the offer stack at the end — check completion-rate data at the 10%, 25%, and 50% marks before rewriting the close.

```yaml
chain_metadata:
  skill_slug: "vsl-script-generator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "vsl-funnel"
    - "landing-page-generator"
```
