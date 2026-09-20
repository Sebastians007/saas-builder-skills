---
name: affiliate-promo-kit
description: >
  Use this skill to create an affiliate or JV (joint venture) promo kit for a
  product launch. Trigger when the user needs affiliate email swipes, partner
  promotional materials, JV page copy, affiliate onboarding materials, or any
  promotional assets designed for third-party partners to use when promoting
  an offer.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "affiliate", "partner-marketing", "promo-assets"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Affiliate / JV Promo Kit Generator

Affiliates and JV partners will only promote what's easy to promote. Your kit
needs to make it frictionless: clear on the offer, high-converting swipes ready
to copy-paste, and compelling enough that a partner feels confident sending it
to their list.

---

## Promo Kit Components

### 1. JV / Affiliate Partner Page
A page explaining the opportunity to potential affiliates (not customers):
- Headline: "Promote [OFFER] to Your Audience and Earn [COMMISSION]"
- What the offer is (1 paragraph — sell the offer to affiliates)
- Commission structure and payout details
- Conversion stats if available (EPC, conversion rate)
- Who the audience is (so affiliates can assess fit)
- Launch dates and key deadlines
- Resources included in the kit
- How to sign up as an affiliate

### 2. Email Swipes (3–5 variations)
Each swipe is a complete, ready-to-send email for affiliates to use with their
lists. Provide:
- 1 announcement email (launch day)
- 1 story/value email (mid-launch)
- 1 last chance email (cart close)
- Optional: 1 early bird email (before launch)
- Optional: 1 re-mail (for affiliates to send to non-openers)

Each email includes:
- Subject line (+ 1 B variant)
- Preview text
- Full body copy with `[AFFILIATE LINK]` placeholders
- Note: affiliates add their own link — copy should flow naturally around it

### 3. Social Media Swipes (3–5 posts)
Platform-ready posts affiliates can publish:
- 1 announcement post
- 1 story/testimonial post
- 1 direct CTA post
- 1 short-form video script (optional)

Include `[AFFILIATE LINK]` placeholders throughout.

### 4. Graphics / Promotional Assets Brief
Not the assets themselves, but the brief for what to create:
- Recommended banner sizes
- Key messages to feature
- Call-to-action copy for graphics
- Color/brand notes

### 5. Affiliate Onboarding Email
Sent automatically when someone joins the affiliate program:
- Welcome + approval confirmation
- Link to the promo kit
- Key dates (launch day, cart close, payout date)
- Who to contact for support
- One thing to do right now (share the first swipe or create their tracking link)

---

## Output Format

```
# [Offer Name] — Affiliate / JV Promo Kit

## JV Partner Page
[Full page copy]

---

## Email Swipes

### Swipe 1 — Launch Day Announcement
Subject: [Subject line]
Subject B: [Alternate]
Preview: [Preview text]

[Full email body]

---

### Swipe 2 — Story / Value
...

---

## Social Swipes

### Post 1 — Announcement
[Full post copy + visual direction]

...

---

## Graphics Brief
[Specifications and key messages]

---

## Affiliate Onboarding Email
[Full email]
```

---

## Rules
- Affiliate swipes must be written to the affiliate's audience, not to the product owner's audience
- Always include `[AFFILIATE LINK]` and `[YOUR NAME]` merge tags
- Never use `[PRICE]` — affiliates need the real price; if not provided, ask for it
- Commission rate and payout terms must be included if provided; use `[COMMISSION]` if not
- Swipes should be adaptable — give affiliates flexibility to personalize the opening


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `launch-directory-submitter` (S1-Research) — affiliate promo assets often get paired with launch directory listings for the same launch window
- `social-content-pack` — affiliate swipe copy gets repurposed into the brand's own social content and vice versa

### Fed By
- `offer-extraction` (S10-Copywriting) — supplies the offer details and commission structure affiliates need to promote it
- `headline-hook-generator` — supplies hooks affiliates can drop into swipe emails and ad copy

### Feedback Loop
If affiliates aren't using the provided swipe copy, check whether it's generic vs. tailored to each affiliate's specific audience — a one-size-fits-all kit gets ignored; segment-specific angles get used.

```yaml
chain_metadata:
  skill_slug: "affiliate-promo-kit"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "social-content-pack"
    - "launch-directory-submitter"
```
