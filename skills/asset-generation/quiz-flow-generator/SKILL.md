---
name: quiz-flow-generator
description: >
  Use this skill to build a quiz funnel. Trigger when the user needs a quiz
  opt-in, interactive assessment, scorecard funnel, personality quiz, or any
  segmented lead generation experience where different results lead to different
  offers or email sequences.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "quiz", "interactive", "segmentation", "new-funnel-type"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Quiz Flow Generator

Quiz funnels out-convert standard opt-in pages because they create engagement
before asking for the email. The quiz itself is the value exchange. Your job is
to design a quiz that segments leads meaningfully AND makes every result feel
personally relevant.

---

## Quiz Structure

### Intro / Opt-in Page
Standard opt-in page structure but the CTA is "Take the Quiz" not "Download":
- Headline: promise a personalized diagnosis or result
- Subheadline: who it's for + what they'll discover
- 3 bullet points of what the quiz reveals
- "Takes 2 minutes" / number of questions
- CTA: "Start the Quiz" / "Find Out Now"

### Questions (5–7 recommended)
Rules for great quiz questions:
- Every question should feel relevant and insightful to the reader
- Avoid obviously "wrong" answers — people abandon quizzes that make them
  feel stupid
- Use situation-based questions, not knowledge-testing questions
- Progress bar increases completion rate — note it in design guidance
- Final 1–2 questions can gate the result ("Where should we send your results?")

For each question, provide:
- Question text
- 3–4 answer options
- Which result segment each answer maps to
- Scoring logic (if applicable)

### Result Segments (2–4 types)
Each result segment needs:
1. **Segment name** — memorable, not clinical ("The Overthinker" / "The Ready-to-Launch")
2. **Result headline** — speaks directly to their situation
3. **Result description** — 2–3 paragraphs that make them feel understood
4. **The gap** — what's holding them back based on this profile
5. **The bridge** — how the offer solves specifically for this segment
6. **CTA** — tailored to this segment's mindset

### Segmented Email Sequences
For each result type, provide a 3-email follow-up sequence:
- Email 1: Deliver the result + expand on their specific situation
- Email 2: Teaching that addresses their specific gap
- Email 3: Offer tailored to their result

---

## Output Format

```
# Quiz Funnel — [Offer / Topic]

## Intro Page
[Full page copy]

## Quiz Questions
### Q1: [Question]
- A) [Option] → [Segment]
- B) [Option] → [Segment]
- C) [Option] → [Segment]
- D) [Option] → [Segment]

...

## Result Segments

### Segment 1: [Name]
**Headline:** [Result headline]
[Full result page copy]
[CTA]

### Segment 2: [Name]
...

## Email Sequences

### Segment 1 Sequence
[3 emails per format in email-sequence-generator style]

### Segment 2 Sequence
...
```

---

## Rules
- Result names should feel like an identity, not a grade
- Every result should feel positive and forward-looking, even if it describes a problem
- Avoid making any segment feel like the "bad" result
- The offer pitch should feel like it was built specifically for this person's result


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

> Note: quiz funnels are a genuinely new funnel type — this pack's S9-Funnels stage did not previously include a quiz-based funnel.

## Flywheel Connections
### Feeds Into
- `landing-page-generator` — the quiz result page reuses the same page-generation patterns for presenting personalized outcomes
- `email-sequence-generator` — quiz segment/result determines which nurture sequence branch a lead enters
- `lead-magnet-creator` — quiz results are often packaged as a personalized lead magnet delivered by email

### Fed By
- `avatar-extraction` (S10-Copywriting) — supplies the audience segments the quiz questions need to distinguish between
- `offer-extraction` (S10-Copywriting) — supplies the offer(s) each quiz result path should route toward

### Feedback Loop
If quiz completion rate is high but result-page-to-offer conversion is low, the fix is the result page's offer relevance to the specific segment, not the quiz questions — check that each result path routes to a genuinely different offer, not one generic pitch.

```yaml
chain_metadata:
  skill_slug: "quiz-flow-generator"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "landing-page-generator"
    - "email-sequence-generator"
```
