---
name: funnel-copy
description: >
  Writes the actual headline, CTA, benefit stack, objection-handling, and
  email copy for any funnel page using proven direct-response formulas
  (AIDA, PAS, benefit stacking) instead of generic marketing-speak.
  Use this skill when the user asks about writing sales page copy, headline
  ideas, or CTA button text, or says
  "write me a headline for this page", "I don't know what to put on my landing page",
  "help me write the sales copy", "what should my CTA button say", "write my email sequence",
  "how do I handle the price objection", "this copy sounds boring", "write the benefit list".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "copywriting", "sales-copy", "email"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Funnel Copy

Fills in the actual words on a funnel page — headline, sub-headline, CTA button, benefit stack, objection handlers, and email subject lines — using formulas that have worked for years, instead of leaving the founder staring at a blank page. Works with any of the 13 funnel-type skills in this pack: they define the structure, this skill writes what goes in each slot.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- A funnel page structure exists (from any funnel-builder skill) but the copy slots are still placeholders
- The user has a working app and needs a first-draft landing page headline
- Writing the email sequence that follows a signup, purchase, or webinar registration
- The user needs objection-handling language for price, time, or trust pushback
- Polishing copy that "sounds boring" or too generic to convert
- Before running `ab-test-generator` — that skill needs real copy variants to test, not placeholders

## Input Schema
```
funnel_type: string             # which funnel this copy is for (e.g., "webinar-funnel", "saas-funnel")
page_element: string            # "headline" | "cta" | "benefit_stack" | "objection_handler" | "email_subject" | "full_page"
product_name: string
target_user: string             # pulled from prd-writer if available
core_benefit: string            # the ONE outcome this offer delivers
price: number | null
tone: string?                   # "urgent" | "calm/trustworthy" | "bold" | default: match product tone
objection_type?: string         # "price" | "time" | "trust" | "not-sure-yet" — only for objection_handler
```

## Workflow
### Step 1: Pull the one-sentence core benefit
Copy is only as good as the underlying offer clarity. If `core_benefit` isn't crisp, pull it from an existing `prd-writer` output (Problem + Outcome fields) rather than asking the user to restate it from scratch.

### Step 2: Generate headline options
Produce 3-5 headline variants across different formulas so the user has real choices, not one guess:
- Benefit-driven: "How to [result] without [pain]"
- Curiosity-driven: "The [small change] that [outcome]"
- Direct/bold: "[Number]x faster [process] for [audience]"
- Problem/agitate: "Stop [pain]. Start [desired state]."

### Step 3: Write the CTA
Match CTA language to the actual commitment level being asked. "Buy Now" for a $17 tripwire is fine; the same words on a $5,000 application funnel undersell the exclusivity — use "Apply Now" instead. Never default to generic "Submit" or "Click Here."

### Step 4: Build the benefit stack (if applicable)
List every component of the offer with a dollar value next to it, sum to a "total value," then show the actual price as a discount off that total. Only use real, defensible values — don't inflate numbers the user can't back up.

### Step 5: Write objection handlers
For the requested objection type (price, time, trust, "let me think about it"), write a short paragraph that acknowledges the concern, reframes it with a specific proof point or guarantee, and moves back toward the CTA. Never argue with the objection — validate first.

### Step 6: Write email subject lines (if applicable)
Produce 3-5 subject line variants for the funnel stage requested (welcome, reminder, cart-close, etc.), keeping them short enough for mobile preview (under 50 characters where possible).

### Step 7: Self-Validation
- [ ] Every headline ties back to the single core benefit, not a feature list
- [ ] CTA copy matches the actual commitment level (free vs. paid vs. application)
- [ ] No invented statistics, fake urgency, or unverifiable claims in the copy
- [ ] Objection handlers acknowledge the concern before countering it
- [ ] At least 3 variants given for any "pick one" element so the user isn't stuck with a single untested option

## Output Schema
```
{
  "headlines": string[],
  "sub_headline": string,
  "cta_text": string,
  "benefit_stack": [ { "item": string, "value": number } ],
  "total_value": number,
  "objection_handler": string | null,
  "email_subject_lines": string[]
}
```

## Output Format
```markdown
# Funnel Copy: <Product Name> — <Page Element>

## Headline Options
1. <headline>
2. <headline>
3. <headline>

## Sub-headline
<one sentence>

## CTA Button Text
<text>

## Benefit Stack (if applicable)
- ✅ <item> — Value: $<x>
- ✅ <item> — Value: $<x>
**Total Value: $<sum> | Price: $<actual> (<x>% off)**

## Objection Handler (if requested)
<paragraph>

## Email Subject Lines (if requested)
1. <subject>
2. <subject>
3. <subject>
```

## Error Handling
- If `core_benefit` is vague or missing, stop and ask the user to state the one outcome the offer delivers before writing headlines — copy built on a vague benefit will be vague too.
- If the user asks for urgency/scarcity language but the offer has no real deadline or limited quantity, flag that fabricated urgency is a trust risk and suggest genuine urgency levers instead (bonus expiring, cohort start date, etc.).
- If `price` is missing for a benefit stack request, ask for it — the stack's math doesn't work without a real price to discount from.
- If the requested tone conflicts with the funnel type (e.g., "bold and hypey" for a `saas-funnel` enterprise buyer), flag the mismatch and recommend the tone that fits the audience.

## Examples
**Example 1:** User has a $29/mo SaaS tool for freelance bookkeepers and needs a hero headline. Output includes benefit-driven ("Send Invoices That Actually Get Paid — Without Chasing Clients"), curiosity-driven, and direct options, plus a CTA of "Start Free Trial — No Card Required" matching the SaaS funnel's zero-friction signup pattern.

**Example 2:** User is writing the cart-close email for a `webinar-funnel` and needs subject lines plus a price objection handler for their $497 course. Output gives 4 subject line variants with urgency framing and an objection paragraph anchored to a 30-day guarantee, not a fabricated discount.

**Example 3:** User has a benefit stack for a `tripwire-funnel` $17 offer with 3 bonuses. Output lists each bonus with a defensible value, totals it against the $17 price, and flags that one bonus value the user proposed ($500 for a single PDF) looks inflated and suggests a more credible number.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `ab-test-generator` (S7-Growth) — takes copy variants and sets up real tests
- Any of the 13 funnel-type skills — fills in their page placeholders
- `pricing-page-optimizer` (S7-Growth) — uses benefit stack and objection copy for pricing pages

### Fed By
- `funnel-select` — determines which funnel type this copy is being written for
- `prd-writer` (S2-Planning) — supplies target user and core benefit language

### Feedback Loop
When `ab-test-generator` or `signup-conversion-tracker` shows a specific headline or CTA underperforming, feed the losing variant and the result back into `funnel-copy` to generate the next round of test copy — don't just guess at a replacement.

```yaml
chain_metadata:
  skill_slug: "funnel-copy"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "ab-test-generator"
    - "signup-conversion-tracker"
```
