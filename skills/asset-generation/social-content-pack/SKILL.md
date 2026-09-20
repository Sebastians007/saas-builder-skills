---
name: social-content-pack
description: >
  Use this skill to generate a social media content pack to drive traffic into
  a marketing funnel. Trigger when a user needs social posts, Instagram captions,
  Facebook posts, LinkedIn posts, or short-form video scripts to promote their
  offer, funnel, or lead magnet across social media platforms.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "social-media", "content-repurposing", "distribution"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Social Content Pack Generator

Social content is the top-of-funnel traffic engine. These posts exist to do one
thing: move the right people from scrolling to clicking. Every post in the pack
serves a different psychological purpose — together they cover the full buyer
awareness spectrum.

---

## Content Pack Structure (5–7 posts)

Produce posts that cover all five of these roles. Never produce 5 posts that all
say the same thing from different angles.

### Post 1 — Awareness / Problem Post
Speak directly to the pain or situation without mentioning the offer.
Goal: "That's exactly me." Gets shares from people who feel seen.
Format: 3–5 short paragraphs. Hook → expand the problem → end with a question
or teaser.

### Post 2 — Story / Origin Post
The transformation story — yours or a client's. Before and after. Specific
details make it believable.
Format: Hook → the before → the turning point → the after → CTA to learn more.

### Post 3 — Value / Teaching Post
Give away a genuinely useful tip or insight related to the offer's topic.
The more useful, the more credibility. This post should make people think
"if the free content is this good, the paid content must be incredible."
Format: Hook → 3-step framework or tip → soft CTA.

### Post 4 — Social Proof Post
Results, testimonials, or numbers. Specific beats vague.
Use `[RESULT]` or `[TESTIMONIAL]` if none provided — note that real proof
should be substituted before publishing.
Format: Attention-grabbing result → context → CTA.

### Post 5 — Direct Offer / CTA Post
Ask for the click. Clear, direct, no-nonsense.
Format: Hook (who this is for) → what they get → one CTA.

### Post 6 (optional) — Objection-Busting Post
Address the #1 reason someone wouldn't click. Turn it into a reason they should.
Format: Acknowledge the objection → reframe → CTA.

### Post 7 (optional) — Urgency / Last Chance Post
For time-limited offers or launch periods.
Format: Deadline → what they'll miss → CTA.

---

## Platform Formatting

For each post, specify the platform and apply the right formatting:

**Instagram:**
- Hook in the first line (before "more")
- Line breaks every 1–3 sentences
- Hashtag block at the bottom (8–15 hashtags)
- CTA: "link in bio" or "comment [KEYWORD] for the link"

**Facebook:**
- Longer form acceptable
- Story-driven posts perform well
- CTA: "Click the link below" or "Drop a comment"
- No hashtag block needed

**LinkedIn:**
- Professional but personal tone
- Numbered lists or short paragraphs
- Hook line must earn the "see more" click
- First-person story performs best
- Light hashtag use (3–5 max)

**Short-form video script (Reels / TikTok):**
- Hook in the first 2 seconds (on-screen text + spoken line)
- 30–60 second script
- Pattern interrupt, deliver the point, CTA at end
- Include: spoken script + on-screen text suggestions

---

## Output Format

For each post:

```
### Post [N] — [Role/Type]
**Platform:** [Instagram / Facebook / LinkedIn / Short-form video]
**Format:** [Caption / Video script]

[Full post copy]

**Visual direction:** [Describe the image or video style — not stock photo
descriptions, but art direction: "talking head against clean background,"
"before/after screenshot," "text overlay on lifestyle video," etc.
Include recommended image dimensions for the platform:
  Facebook: 1200×628px | Instagram feed: 1080×1080px | Instagram story: 1080×1920px
  LinkedIn: 1200×627px | Twitter/X: 1600×900px | Reels/TikTok: 1080×1920px]

**Hashtags (if applicable):**
[hashtag block]
```

---

## Rules
- Every post needs a hook in the first line — no "Hey everyone!" openers
- Write in the brand voice — if none provided, match the tone of the offer
- Social proof posts: always note `[REAL RESULT — replace before publishing]`
  if using placeholder content
- Each post should stand alone — no "as I mentioned yesterday" references
- One CTA per post — don't ask people to follow AND click AND comment


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `user-acquisition-analyzer` (S1-Research) — measures which social channels and posts actually drive signups from the content pack
- `ad-angle-multiplier` (S10-Copywriting) — the pack's best-performing hooks and angles become paid ad variants

### Fed By
- `avatar-extraction` (S10-Copywriting) — supplies the audience language the posts need to speak in
- `headline-hook-generator` — supplies hooks the pack repurposes into post openers

### Feedback Loop
If a specific platform underperforms across the whole pack, the fix is usually format/native-style mismatch, not the underlying hook — check that video-first platforms aren't getting text-first content before rewriting hooks.

```yaml
chain_metadata:
  skill_slug: "social-content-pack"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "ad-angle-multiplier"
    - "user-acquisition-analyzer"
```
