---
name: checkout-funnel-auditor
description: >
  Audits a SaaS signup, checkout, or plan-upgrade flow step by step for drop-off
  points, friction, and missing trust signals, producing a ranked fix list
  instead of a vague "checkout feels off".
  Use this skill when the user asks about checkout drop-off, upgrade flow friction,
  or says
  "why are people dropping at payment", "audit our checkout flow", "reduce friction in signup",
  "people abandon before entering their card", "review our upgrade modal", "why isn't the free trial converting to a card add".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "checkout", "conversion", "revenue", "posthog"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Checkout Funnel Auditor

This skill walks a SaaS checkout, signup, or plan-upgrade flow step by step, flags friction and trust gaps against a fixed checklist, and produces a ranked fix list scored by effort vs. expected lift. It replaces "checkout conversion feels low" with specific, fixable steps.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- The user has step-level drop-off numbers (from PostHog funnels) showing a specific checkout/upgrade step is losing people
- The user is adding a new payment path (new plan, new provider, Apple/Google Pay) and wants a pre-launch review
- Trial users open the upgrade modal but rarely complete payment
- After pricing-page-optimizer ships changes, to confirm the downstream checkout flow matches the new plan structure
- The user wants a concrete "ship this week" list instead of a general design critique

## Input Schema
```
flow_description: string         # required: the steps a user takes, e.g. "dashboard -> upgrade modal -> plan select -> Stripe checkout -> success"
flow_screenshots: array?         # image paths/URLs if available
funnel_step_counts: object?      # from PostHog funnel, e.g. {"modal_opened": 500, "plan_selected": 300, "payment_started": 180, "payment_completed": 90}
payment_methods: array?          # e.g. ["card", "Apple Pay", "invoice"]
plan_structure: object?          # from pricing-page-optimizer if available
region_mix: string?              # e.g. "80% US, 15% EU, 5% other" — affects tax/trust needs
```

## Workflow
### Step 1: Map the Current Flow Step by Step
List every screen the user passes through from "intent to pay" to "confirmed." For each step record: what's required (fields, account creation), what trust signals are visible, what exit options exist (close/back/skip), and how it behaves on mobile. Pull step-level counts from PostHog's funnel feature if available — this tells you where to focus before doing any checklist work.

### Step 2: Run the Friction Checklist
Flag any of the following present in the flow:
- Account creation required *before* payment can even be started (usually the single biggest killer — measure how much of the drop-off happens right at this step)
- Asking for company name/VAT/business fields when the buyer is clearly a self-serve consumer
- A card form with no inline validation (errors only shown after full submit)
- No saved-card path for an existing logged-in user upgrading plans
- Taxes or fees that only appear at the final step (feels like bait-and-switch)
- Mandatory email confirmation before the user gets any access (delays the reward past the moment of intent)
- Confusing field order (CVV/billing address placement)
- No visible coupon/promo field when the user expects one
- Mobile keyboard mismatched to input type (text keyboard for a card number field)

### Step 3: Run the Trust Checklist
- Guarantee visible on the payment step itself (money-back, cancel anytime) — not just buried in the FAQ
- Recognizable security signals (lock icon, "secured by Stripe," payment logos)
- One relevant testimonial or logo near the payment step, if available
- Full price breakdown (subtotal, tax, discount, total) visible before the final click
- Renewal date and billing cadence stated plainly, not hidden in terms

### Step 4: Run the Clarity Checklist
- CTA button says the actual outcome ("Pay $29/mo") rather than a vague verb ("Subscribe", "Continue")
- The total is shown right above the final button, not just earlier on the page
- The post-payment screen tells the user what happens next, not a dead-end "Success!" with no path forward

### Step 5: Run the Mobile Checklist
- Single-column layout, no horizontal scroll
- Apple Pay / Google Pay offered above the manual card form when available (materially reduces friction)
- No fields hidden below an unscrolled fold on a 375px-wide screen
- Correct keyboard type per field (numeric for card number/CVV)

### Step 6: Score and Rank the Fix List
For every issue found, score effort (roughly: hours vs. days vs. weeks) against expected lift (based on where in the funnel it sits — earlier steps with more volume generally have higher lift). Group into three buckets:
- **Ship today**: copy changes, button text, adding a visible guarantee/trust badge
- **This sprint**: reordering the flow, adding Apple/Google Pay, removing an unnecessary field
- **Strategic**: removing account-creation-before-payment, switching payment providers

### Step 7: Hand Off the Top Fix for Testing
Name the single highest-ROI fix and phrase it as a testable hypothesis for ab-test-generator (e.g. "Moving account creation to after payment will increase payment-start-to-complete rate").

### Step 8: Self-Validation
Before presenting output, confirm:
- [ ] The flow is mapped step by step with actual step-level counts where available, not just a general impression
- [ ] All four checklists (friction, trust, clarity, mobile) were run, not just one
- [ ] Every flagged issue is scored on effort vs. lift and bucketed into ship-today/this-sprint/strategic
- [ ] Exactly one fix is named as the top priority to test first
- [ ] If account-creation-before-payment is present, it's explicitly called out (it's the single most common high-impact fix in SaaS checkout flows)

## Output Schema
```json
{
  "flow_map": [
    {"step": "string", "count": "number|null", "conversion_from_previous": "string|null"}
  ],
  "friction_issues": [{"issue": "string", "severity": "high|medium|low"}],
  "trust_issues": [{"issue": "string", "severity": "high|medium|low"}],
  "clarity_issues": [{"issue": "string", "severity": "high|medium|low"}],
  "mobile_issues": [{"issue": "string", "severity": "high|medium|low"}],
  "fix_list": [
    {"fix": "string", "effort": "hours|days|weeks", "expected_lift": "high|medium|low", "bucket": "ship_today|this_sprint|strategic"}
  ],
  "top_test_hypothesis": "string"
}
```

## Output Format
```markdown
# Checkout Funnel Audit — [flow name]

## Flow Map
| Step | Users | Conversion from previous |
|---|---|---|
| [step] | [n] | [%] |

## Issues Found
### Friction
- [severity] [issue]
### Trust
- [severity] [issue]
### Clarity
- [severity] [issue]
### Mobile
- [severity] [issue]

## Fix List (ranked)
### Ship Today
- [fix]
### This Sprint
- [fix]
### Strategic
- [fix]

## Top Test to Run First
Hypothesis: [testable statement]
Hand off to: ab-test-generator

## Do Not
- Ship all fixes at once without a way to know which one moved the number
- Add trust badges as a substitute for fixing a structural issue like account-before-payment
- Assume desktop findings apply to mobile without checking separately
```

## Error Handling
- No step-level funnel counts provided → proceed with the checklist audit alone (still valuable) but flag that prioritization is a best guess until PostHog funnel data is pulled
- Flow description too vague to map (e.g. "checkout is broken") → ask for the actual step sequence before running checklists
- User wants every issue fixed simultaneously → push back, insist on shipping the top 1-2 fixes first and measuring before moving to the next batch
- Region mix not provided but user is clearly multi-region → flag tax-display and currency-display as an open risk rather than skipping it silently
- Screenshots unavailable and flow description is thin → note the audit is lower-confidence and recommend a screen recording for next time

## Examples
**Example 1**
User: "We're losing 60% of people between the upgrade modal and completing Stripe checkout."
Skill: Maps the flow, finds account-creation-before-payment isn't present but the modal requires re-entering billing address for existing logged-in users, flags it high-severity, and proposes autofilling from the account profile as the top fix to test.

**Example 2**
User: "Adding Apple Pay, what's best practice?"
Skill: Runs the mobile checklist specifically, confirms Apple Pay should sit above the manual card form (not below), and checks the rest of the flow doesn't force account creation before the Apple Pay button is reachable.

**Example 3**
User: "Review our new checkout before launch."
Skill: Runs all four checklists against the described flow, finds tax only shown at the final step, flags it high-severity as a trust issue, and puts it in "ship today" since it's a copy/layout fix, not an engineering rebuild.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- trial-to-paid-converter
- ab-test-generator
- revenue-dashboard-builder

### Fed By
- signup-conversion-tracker
- pricing-page-optimizer

### Feedback Loop
After the top fix ships, re-pull the PostHog funnel counts for the same steps and confirm the targeted step's conversion actually moved before picking the next fix off the list.

```yaml
chain_metadata:
  skill_slug: "checkout-funnel-auditor"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "ab-test-generator"
    - "revenue-dashboard-builder"
```
