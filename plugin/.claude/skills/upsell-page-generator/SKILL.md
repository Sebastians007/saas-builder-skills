---
name: upsell-page-generator
description: >
  Use this skill to write an upsell page, one-time offer (OTO) page, order bump
  copy, downsell page, or any post-purchase offer page in a marketing funnel.
  Trigger when a user needs copy for an upgrade offer, a "one-time offer" shown
  after checkout, a cross-sell, or an add-on to an existing purchase.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "upsell", "one-click-offer", "order-flow"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Asset-Generation
  source: "internal (user-owned, not third-party)"
---

# Upsell Page + Order Bump Generator

Upsells and order bumps are the highest-margin assets in any funnel. The customer
has already decided to buy — your job is to make the upgrade obvious and the
decision easy.

---

## Two Formats

### Order Bump (checkout page add-on)
A single-sentence to 3-sentence description shown as a checkbox on the order
form. The reader has their credit card in hand. Keep it extremely short and
frictionless.

**Structure:**
```
☑ YES! Add [PRODUCT NAME] to my order for just [PRICE] — [one-line benefit]
[2–3 sentences maximum describing what it is and why they want it right now]
```

**Rules:**
- Must be a natural complement to what they just bought
- Price should be significantly lower than the main offer
- Framed as an obvious "while you're here" add-on
- Never use `[PRICE]` — if price not given, ask for it; order bumps live or die on price clarity

---

### Upsell Page (full post-purchase page)

**Structure:**

1. **Headline** — acknowledge the purchase, then pivot immediately
   > "Wait — Your Order Is Complete. But Before You Go..."
   > "Congratulations — Here's How to Get Results 3x Faster"

2. **Bridge** — connect the upsell to the purchase they just made
   > "You just got [main product]. The one thing that holds most people back
   > from [result] is [gap]. That's exactly what [upsell] solves."

3. **Offer reveal** — what the upsell is and what's included

4. **Value stack** — walk through each component + benefit

5. **Why right now** — this price, this bonus, this offer is only available
   on this page, one time

6. **Guarantee** — extend or restate the guarantee

7. **CTA** — "Yes, Add This To My Order" / "No thanks, I don't need [specific
   result]"

**Note on the "No" button:** Write the no button copy as a consequence, not an
insult. "No thanks, I'll figure it out on my own" works. "No thanks, I hate
money" doesn't — it creates resentment.

---

### Downsell Page
Shown if they decline the upsell. Offer a lower-priced version, payment plan,
or stripped-down alternative. Structure is identical to the upsell page but
opens with acknowledgment that they passed on the previous offer:
> "No problem — I get it. That's why I've put together something smaller..."

---

## Output Format

For each upsell/order bump:
- Complete copy from headline to CTA
- "Yes" and "No" button text
- Page Notes: placement guidance, timing (immediate vs. delayed), platform
  deployment notes based on the user's stated tech stack

---

## Rules
- Never invent prices — use `[PRICE]` if not provided
- Never use high-pressure tactics — urgency should be real (one-time page),
  not manufactured panic
- The upsell must be a logical extension of the main purchase
- Keep the upsell page shorter than the main sales page — they've already bought


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `checkout-funnel-auditor` (S7-Growth) — audits the completed checkout-to-upsell flow for drop-off points
- `tripwire-funnel` (S9-Funnels) — the upsell page is a standard step directly after a tripwire's low-ticket purchase

### Fed By
- `thank-you-page-generator` — the purchase confirmation flow leads directly into the one-click upsell offer
- `offer-extraction` (S10-Copywriting) — supplies the upsell offer's pricing and value stack

### Feedback Loop
If upsell take-rate is low, check offer relevance to the original purchase before touching page copy — a mismatched upsell (wrong product for what they just bought) won't convert no matter how the page is written.

```yaml
chain_metadata:
  skill_slug: "upsell-page-generator"
  stage: "asset-generation"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "thank-you-page-generator"
```
