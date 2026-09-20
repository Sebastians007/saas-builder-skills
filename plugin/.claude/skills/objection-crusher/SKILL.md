---
name: objection-crusher
description: >
  Identifies the real objections a SaaS prospect has before paying — price,
  trust, switching cost, "will this actually work for me" — and writes copy
  that answers each one directly instead of hoping it doesn't come up.
  Use this skill when the user asks about handling pricing pushback, trust
  issues, or reasons people don't convert, or says
  "why isn't anyone buying", "handle objections on my pricing page", "people say we're too expensive",
  "what's stopping signups from converting to paid", "write an FAQ that actually helps",
  "address hesitation on my landing page", "people ghost after the trial".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "objections", "pricing-page", "trust", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Objection Crusher

This skill surfaces the specific, real reasons a prospect hesitates before paying, then writes copy that answers each one head-on — on the pricing page, in the FAQ, in trial-expiring emails — instead of leaving the objection unaddressed and hoping the prospect talks themselves into buying anyway.

## Stage
This skill belongs to Stage S4: Copywriting

## When to Use
- Trial signups aren't converting to paid and the reason isn't obvious from the funnel data alone
- Building or rewriting a pricing page FAQ section
- The user has anecdotal objections from sales calls, support tickets, or churn surveys that haven't been turned into copy yet
- Writing trial-expiring or win-back email copy that needs to pre-empt hesitation
- Feeding `full-funnel-campaign-orchestrator` with the objection-handling layer for a campaign
- The user says "people seem interested but don't convert" or "we keep hearing the same pushback"

## Input Schema
```
product_or_service: string
known_objections: string[]?          # from sales calls, support tickets, churn surveys, if any
core_promise: string?                # from offer-extraction, if run
price: string?
guarantee: string?
competitor_context: string?          # from competitor-teardown, if available
```

## Workflow
### Step 1: List the Real Objections, Not Generic Ones
Start from actual evidence if available (support tickets, sales call notes, churn survey answers). If none exists, generate the standard SaaS objection set and flag which are assumptions versus confirmed:
- Price ("is this worth it compared to what we're already doing / not doing")
- Time/effort to switch or set up
- Trust ("will this actually work for my specific case, is this company going to be around")
- Complexity ("this looks like it'll take my team weeks to learn")
- Past failure ("we tried a tool like this before and it didn't stick")

### Step 2: Reframe Each Objection Three Ways
For every objection, write a response using each lens, then pick the strongest:
- **Logic** — a fact or number that resolves the concern
- **Proof** — a testimonial, case study, or usage stat that shows it's already been resolved for someone else
- **Emotion** — reframes what staying stuck actually costs them

### Step 3: Assign Each Objection to a Placement
Not every objection belongs on the pricing page. Map each to where it should live:
- Pricing page FAQ: price, contract terms, cancellation
- Landing page below the fold: trust, "will this work for my case"
- Onboarding/trial emails: complexity, time to value
- Win-back emails: past failure with a similar tool, what's different now

### Step 4: Write the Copy
Produce actual FAQ answers, page copy blocks, or email lines — not just a list of objection/response pairs. Copy should sound like a direct, honest answer a smart founder would give in person, not corporate reassurance.

### Step 5: Self-Validation
- [ ] Every objection is a real, specific concern, not a strawman
- [ ] Each response uses the strongest of logic/proof/emotion, stated honestly
- [ ] No objection is dodged, minimized, or answered with vague reassurance
- [ ] Each objection is placed where the prospect actually encounters it in the funnel
- [ ] Copy sounds like a person answering directly, not legal-safe corporate hedging

## Output Schema
```json
{
  "objections": [
    {
      "objection": "string",
      "source": "confirmed|assumed",
      "response": "string",
      "response_style": "logic|proof|emotion",
      "placement": "pricing_faq|landing_page|onboarding_email|winback_email"
    }
  ]
}
```

## Output Format
```markdown
# Objection-Handling Copy: [product name]

## [Objection 1]
**Source:** confirmed / assumed
**Response ([logic/proof/emotion]):** [actual copy, ready to paste]
**Placement:** [where this goes]

## [Objection 2]
...

## Unresolved / Needs Real Data
- [objection flagged as assumed, with a note on how to confirm it — support tickets, a quick churn survey, etc.]
```

## Error Handling
- No known objections given → generate the standard SaaS set, clearly label all as "assumed — confirm with real user feedback," and recommend pulling 5-10 support tickets or churn survey responses before finalizing copy
- Objection is about something genuinely broken in the product (e.g. a real bug or missing feature) → don't write copy to paper over it; state plainly that this objection needs a product fix, not a rewrite
- Price objection with no real guarantee to point to → recommend the cheapest real guarantee available (cancel anytime, free trial, no card required) rather than writing confident copy backed by nothing
- User wants objections hidden or avoided entirely → explain that unaddressed objections don't disappear, they just convert into silent bounces; the prospect still has the concern, they just leave instead of asking

## Examples
**Example 1**
User: "People say we're too expensive compared to spreadsheets, obviously."
Skill: Reframes using logic ("spreadsheets are free until an error costs a client relationship") and proof (a stat on hours saved per week), places the response in the pricing page FAQ under "Why not just use a spreadsheet?", and flags this as a confirmed objection worth leading with directly rather than avoiding.

**Example 2**
User: "Trial users don't convert but we don't really know why."
Skill: Generates the standard objection set (complexity, trust, past tool failure), recommends pulling churn survey data or emailing 10 lapsed trials to confirm which one is real, and drafts placeholder copy for each so the founder has something to test immediately while confirming.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- onboarding-flow-builder (S4-Building)
- pricing-page-optimizer (S10-Growth)
- full-funnel-campaign-orchestrator (S4-Copywriting)

### Fed By
- offer-extraction (S2-Audience-Positioning)
- avatar-extraction (S2-Audience-Positioning)

### Feedback Loop
Trial-to-paid conversion changes tracked by `trial-to-paid-converter` after objection-handling copy ships should confirm which objections were actually the blockers — objections that don't move the needle get deprioritized, confirmed blockers get expanded into their own dedicated page section.

```yaml
chain_metadata:
  skill_slug: "objection-crusher"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "pricing-page-optimizer"
    - "full-funnel-campaign-orchestrator"
```
