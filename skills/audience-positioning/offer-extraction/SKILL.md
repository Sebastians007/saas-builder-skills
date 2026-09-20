---
name: offer-extraction
description: >
  Clarifies and sharpens the actual offer — what's promised, to whom, for
  what price, with what guarantee — before any headline, page, or email gets
  written around it, so copy doesn't get built on a fuzzy premise.
  Use this skill when the user asks about clarifying their offer, value
  proposition, or pricing page pitch, or says
  "what's my actual offer", "why would someone buy this", "sharpen my value prop",
  "what am I actually promising", "help me define my offer", "my pricing page feels weak",
  "what's the pitch here", "turn this feature list into an offer".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "positioning", "offer-strategy", "pricing"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S2-Audience-Positioning
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Offer Extraction

This skill turns a feature list or a vague pitch into a specific offer: one promised outcome, for one buyer, at one price, backed by one guarantee. It runs before any copy is written, because no headline formula fixes an offer that isn't clear about what's actually being sold.

## Stage
This skill belongs to Stage S2: Audience & Positioning

## When to Use
- Before writing a pricing page, landing page hero, or trial signup flow
- The founder can list features but struggles to say why someone would pay for them
- Conversion is weak and the suspicion is the offer itself, not the copy polish
- A new pricing tier or plan is being launched and needs its own clear pitch
- The user says "I don't know what makes this worth paying for" or similar

## Input Schema
```
product_or_service: string
features_list: string[]?
current_pricing: string?              # e.g. "$29/mo", "free trial + $49/mo"
primary_avatar: object?                # output of avatar-extraction, if run
competitor_offers: string?             # from competitor-teardown, if available
current_guarantee_or_refund_policy: string?
```

## Workflow
### Step 1: Define the Outcome, Not the Feature
For each major feature, ask: what changes for the buyer once they have this? Strip mechanism language ("automated reporting dashboard") down to outcome language ("know which clients are about to churn before they cancel"). Outcomes sell; features get compared and commoditized.

### Step 2: Extract the Four Kinds of Value
Score the offer against each, even if the SaaS is B2B and some feel awkward to name:
- Financial upside (revenue gained, cost avoided)
- Time saved (hours per week, specific if possible)
- Effort removed (what manual work disappears)
- Risk reduced (what bad outcome becomes less likely)

The strongest offers hit at least two of these specifically, not vaguely.

### Step 3: Build the Tension — Why Now
Define what happens if the buyer does nothing. Not manufactured urgency — the real cost of staying on their current workaround (spreadsheet errors compound, churn keeps happening silently, competitors keep pulling ahead). This becomes the "why now" that closes the gap between interested and paying.

### Step 4: Pressure-Test the Guarantee and Price
- Does the guarantee (refund policy, free trial, cancel-anytime) remove the buyer's actual risk, or just look like a guarantee?
- Is the price stated plainly, or buried behind "contact sales" when it doesn't need to be?
- Would this offer survive being read back to the avatar from `avatar-extraction` word for word?

### Step 5: Write 3 Offer Angles, Then Pick the Dominant One
Generate three different ways to frame the same underlying offer (e.g. led with time saved vs. led with risk reduced vs. led with financial upside). Pick the one most likely to land with the primary avatar and state why.

### Step 6: Self-Validation
- [ ] Offer is stated as an outcome, not a feature list
- [ ] At least two of the four value types are named specifically (with numbers where possible)
- [ ] "Why now" tension is the real cost of inaction, not fake scarcity
- [ ] Price and guarantee are stated plainly, not hedged
- [ ] One dominant offer angle is chosen, not three left unresolved

## Output Schema
```json
{
  "core_promise": "string",
  "value_breakdown": { "financial": "string|null", "time_saved": "string|null", "effort_removed": "string|null", "risk_reduced": "string|null" },
  "why_now": "string",
  "price": "string",
  "guarantee": "string",
  "offer_angles": ["string", "string", "string"],
  "dominant_offer": "string",
  "dominant_offer_rationale": "string"
}
```

## Output Format
```markdown
# Offer: [product name]

## Core Promise
[one sentence — outcome, for whom, in what timeframe if relevant]

## Value Breakdown
- Financial: [specific if possible]
- Time saved: [specific if possible]
- Effort removed: [specific]
- Risk reduced: [specific]

## Why Now
[real cost of staying on the current workaround]

## Price & Guarantee
- Price: [plainly stated]
- Guarantee: [what risk this actually removes for the buyer]

## Offer Angles
1. [angle — led with which value type]
2. [angle]
3. [angle]

## Dominant Offer (use this one)
[the winning angle]
Why: [one sentence tied to the primary avatar]
```

## Error Handling
- User can only list features, no outcomes → walk each feature through "so what changes for the buyer" until an outcome surfaces; don't accept a feature as a final answer
- No pricing decided yet → note that price should be tested with `pricing-model-calculator`, use a placeholder, and flag the offer as pending price confirmation
- Guarantee is weak or nonexistent → state plainly that this raises perceived risk, and suggest the lowest-cost real guarantee available (e.g. cancel anytime, no card required for trial) rather than inventing a bogus one
- Multiple offers exist for different tiers → run this skill once per tier rather than blending them into one offer that fits none of them well

## Examples
**Example 1**
User: "We have unlimited projects, real-time collaboration, and custom branding on the Pro plan."
Skill: Converts to outcome language — "your whole team sees the same live project status instead of chasing updates in Slack, and clients see a branded portal instead of a generic tool" — then builds the why-now (they're currently losing time to status-update meetings every week) and picks the dominant angle: time saved, led with the status-meeting pain.

**Example 2**
User: "Our pricing page just lists three tiers with checkmarks and conversion is bad."
Skill: Flags that a checkmark grid is a feature comparison, not an offer — recommends leading each tier with its core promise sentence above the checkmark table, and pressure-tests whether the guarantee (or lack of one) is adding friction.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- objection-crusher (S4-Copywriting)
- pricing-page-optimizer (S10-Growth)
- ad-angle-multiplier (S4-Copywriting)

### Fed By
- avatar-extraction (S2-Audience-Positioning)
- pricing-model-calculator (S1-Research)

### Feedback Loop
Trial-to-paid conversion data from `trial-to-paid-converter` should confirm whether the dominant offer angle actually closes buyers — if trials convert but paid conversion lags, re-run this skill on the guarantee and price framing specifically.

```yaml
chain_metadata:
  skill_slug: "offer-extraction"
  stage: "audience-positioning"
  timestamp: string
  suggested_next:
    - "objection-crusher"
```
