---
name: saas-funnel
description: >
  Builds the 4-page funnel that converts visitors into free trial or freemium
  signups and nurtures them to paid — landing page, signup page, in-app
  onboarding, and upgrade/pricing page.
  Use this skill when the user asks about a trial signup funnel, freemium
  conversion, or landing-to-paid flow for a SaaS product, or says
  "build me a signup funnel for my app", "how do I convert trial users to paid",
  "I need a SaaS landing page", "design my free trial flow", "what should my pricing page look like",
  "help me get more trial signups", "my trial users aren't upgrading".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "trial", "freemium", "onboarding", "pricing"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# SaaS Funnel

The core funnel for any subscription software product: get a visitor to try it, get the trial user to their "aha moment" fast, and convert them to a paying plan. This is the primary funnel type for most apps built with this skill pack.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The product is a recurring-revenue SaaS app with a free trial or freemium tier
- `funnel-select` recommended `saas-funnel` for a subscription product
- The landing page exists but signup or trial-to-paid conversion is weak
- Onboarding exists in-app but isn't clearly mapped to a specific "aha moment"
- Before or alongside `auth-flow-builder` and `onboarding-flow-builder` — this defines the marketing/conversion shell those technical skills implement

## Input Schema
```
product_name: string
core_value_prop: string           # one sentence: what problem it solves
trial_length_days: number         # 0 if freemium with no trial clock
requires_credit_card: boolean
target_user: string
key_features: string[]            # 3-6
pricing_tiers: [ { "name": string, "price": number, "is_recommended": boolean } ]
aha_moment: string?               # the specific action that predicts activation, if known
```

## Workflow
### Step 1: Write the landing page
Required sections in order: hero (headline + sub-headline + CTA + product screenshot), social proof bar, features grid (3-6 features with plain-language descriptions, not jargon), "how it works" 3-step process, 2-3 use cases with outcomes, testimonials, pricing preview with "Start Free" CTA, FAQ, final CTA. Use headline patterns like "[Verb] your [process] in [fraction of time]" or "Stop [pain]. Start [desired state]."

### Step 2: Design the signup page for zero friction
Email + password (or SSO) only — no long forms, no navigation, no credit card requirement unless there's a specific reason for it (note: requiring a card typically cuts signup volume but can raise trial-to-paid quality; flag this tradeoff to the user rather than deciding for them).

### Step 3: Map onboarding to the aha moment
If `aha_moment` isn't defined yet, flag that `aha-moment-mapper` should run first — onboarding built without knowing the aha moment is just a feature tour, not a conversion engine. Otherwise, structure onboarding as: welcome → the ONE key setup action → second most impactful action → visible first result → celebrate + next steps. Hand off structural detail to `onboarding-flow-builder`.

### Step 4: Build the pricing/upgrade page
Feature comparison table, one visually highlighted recommended plan, annual/monthly toggle (annual shown by default), per-seat or usage pricing calculator if applicable, guarantee/risk reversal, pricing FAQ, "Contact Sales" for enterprise if relevant.

### Step 5: Write the trial nurture email sequence
A day-by-day sequence (typically matched to `trial_length_days`) covering: welcome+quickstart, feature tips, a case study, a midpoint check-in, a premium feature preview, and an ending warning with upgrade CTA before trial expiry.

### Step 6: Self-Validation
- [ ] Signup page has no navigation and asks for the minimum viable info
- [ ] Onboarding explicitly targets a named aha moment, not a generic feature tour
- [ ] Pricing page highlights exactly one recommended plan, not all plans equally
- [ ] Trial nurture sequence has a clear expiry warning with enough lead time to act
- [ ] If `requires_credit_card` is true, the tradeoff was flagged, not silently assumed

## Output Schema
```
{
  "pages": [
    { "name": "landing_page", "sections": string[], "copy": object },
    { "name": "signup_page", "fields": string[] },
    { "name": "onboarding", "steps": string[] },
    { "name": "pricing_page", "tiers": array }
  ],
  "trial_nurture_sequence": [ { "day": number, "focus": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# SaaS Funnel: <Product Name>

## Flow
Landing Page → Signup Page → Onboarding → Upgrade/Pricing Page

## Page 1: Landing Page
<section-by-section copy>

## Page 2: Signup Page
<fields, friction-reduction notes>

## Page 3: Onboarding
<steps mapped to aha moment>

## Page 4: Pricing / Upgrade Page
<tier table, recommended plan, guarantee>

## Trial Nurture Email Sequence
| Day | Focus |
|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Visitor → Signup | 3-8% |
| Signup → Activation | 40-70% |
| Activation → Paid | 15-30% |
```

## Error Handling
- If `aha_moment` is unknown, don't guess — recommend running `aha-moment-mapper` first and build a provisional onboarding flow flagged as "needs validation."
- If `pricing_tiers` has more than 4 plans, warn that choice overload typically hurts conversion and suggest consolidating.
- If the landing page copy leads with features instead of the outcome in `core_value_prop`, rewrite the hero before finalizing.
- If `requires_credit_card` is true for a first-time small SaaS with no brand trust yet, flag that this usually kills top-of-funnel volume and suggest testing without it first.

## Examples
**Example 1:** A founder has a $29/mo invoicing tool for freelancers with a 14-day trial, no card required. The skill builds a landing page headlined "Get Paid Faster — Without Chasing Clients," a 2-field signup, onboarding that gets the user to send their first invoice within 5 minutes (the aha moment), and a 2-tier pricing page.

**Example 2:** A B2B analytics SaaS wants to require a credit card for trial signup to filter for serious buyers. The skill flags the tradeoff (lower volume, higher trial quality), builds both a card-required and card-optional version of the signup copy, and recommends testing with `ab-test-generator`.

**Example 3:** An existing SaaS app has trial signups but only 8% activation. The skill notes the aha moment was never defined, recommends `aha-moment-mapper` first, then rebuilds onboarding around the specific action that data shows predicts retention.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/landing-page.html`

## Flywheel Connections
### Feeds Into
- `onboarding-flow-builder` (S3-Building) — implements the onboarding structure this funnel maps out
- `auth-flow-builder` (S3-Building) — implements the signup page technically
- `trial-to-paid-converter` (S7-Growth) — owns ongoing trial-to-paid optimization after launch
- `signup-conversion-tracker` (S7-Growth) — measures every stage of this funnel live

### Fed By
- `aha-moment-mapper` (S7-Growth) — defines the activation action onboarding should target
- `pricing-model-calculator` (S2-Planning) — supplies the pricing tiers this funnel presents
- `funnel-select` — confirms this is the right funnel for a recurring SaaS product

### Feedback Loop
If `trial-to-paid-converter` or `cohort-churn-analyzer` shows weak activation-to-paid conversion after launch, revisit the onboarding step mapping here rather than only tweaking the pricing page — the root cause is often that the aha moment was never truly reached.

```yaml
chain_metadata:
  skill_slug: "saas-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "onboarding-flow-builder"
    - "signup-conversion-tracker"
    - "trial-to-paid-converter"
```
