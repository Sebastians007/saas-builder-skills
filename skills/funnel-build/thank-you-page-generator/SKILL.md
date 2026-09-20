---
name: thank-you-page-generator
description: >
  Use this skill to write a thank you page, confirmation page, order confirmation
  page, delivery page, "what happens next" page, or any post-conversion page in
  a marketing funnel. Trigger when a user needs copy for the page shown immediately
  after an opt-in, purchase, webinar registration, application submission, or
  free trial signup.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "thank-you-page", "post-conversion", "upsell-path"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# Thank You Page Generator

Thank you pages are the most underused real estate in any funnel. Most people
waste them with "Thanks! Check your inbox." A great thank you page does four
things: confirms the action, delivers immediate value, sets expectations, and
advances the relationship (or the sale).

---

## Thank You Page Types & Structure

### Post Opt-in / Lead Magnet Confirmation
1. **Confirmation headline** — affirm they made the right move ("You're in!")
2. **What happens next** — tell them exactly what to expect and when
3. **Immediate value** — quick win, first tip, or preview of what's coming
4. **Soft ascend** — introduce the next step (book a call, join the community,
   check out this resource) — do NOT hard pitch
5. **Social share prompt** — optional: "Know someone who'd love this?"

### Post-Purchase / Order Confirmation
1. **Confirmation headline** — celebrate the decision
2. **Order summary** — what they bought, what they get, delivery timeline
3. **What happens next** — login link, email to check, next step
4. **Onboarding CTA** — get them started immediately (reduces buyer's remorse)
5. **Upsell or upgrade opportunity** — if this is a tripwire funnel, this is
   where the upsell lives

### Post-Webinar Registration
1. **Confirmation headline** — they're registered; make them feel excited
2. **Event details** — date, time, platform, add-to-calendar link
3. **What to expect** — tease 2–3 things they'll learn
4. **Pre-webinar warmup** — a short video, PDF, or question to prime them
5. **Share prompt** — "Bring a friend" / referral hook

### Post-Application / High-Ticket
1. **Confirmation headline** — validate their courage in applying
2. **What happens next** — when they'll hear back, what the review process looks
   like
3. **Pre-call prep** — what to think about / prepare before the call
4. **Credibility reinforcement** — testimonial, case study, or result that
   reassures them they made the right choice

---

## Output Format

For each thank you page, provide:
- Complete headline
- Subheadline
- Body copy in order (following the structure above)
- CTA button text + destination
- Page Notes: design suggestions (video vs. text, layout, urgency elements)

---

## Rules
- Never waste this page on a generic "check your email" message
- Match tone exactly to the brand context and funnel type
- Keep it focused — one next step only
- Use `[PRICE]` for any price not provided; never invent numbers


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `upsell-page-generator` — the thank-you page is the natural bridge into a one-click upsell or tripwire offer
- `email-sequence-generator` — sets the tone and next-step expectation the first nurture email needs to match

### Fed By
- `landing-page-generator` — supplies the original offer context the confirmation message needs to reference
- `optin-funnel` (S3-Funnel-Build) — defines what was just converted (opt-in vs purchase) which determines the thank-you page's next-step CTA

### Feedback Loop
If the next-step CTA (upsell, calendar link, download) has a low click rate, check that the page correctly matches what was just promised on the previous page — a mismatch in expectation kills thank-you-page conversion faster than weak copy does.

```yaml
chain_metadata:
  skill_slug: "thank-you-page-generator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "upsell-page-generator"
    - "email-sequence-generator"
```
