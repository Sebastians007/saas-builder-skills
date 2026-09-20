---
name: pricing-model-calculator
description: >
  Works out SaaS pricing tiers and unit economics — what to charge, margin
  per customer, and how many paying users are needed to break even — for a
  described product.
  Use this skill when the user asks about "what should I charge",
  or says
  "what should I charge for this", "help me price my app", "how many customers do I need to break even",
  "is $29/mo too cheap", "should I do a free tier", "what pricing tiers make sense",
  "how do I price against competitors", "what's my margin per user".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "pricing", "unit-economics", "monetization"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Pricing Model Calculator

This skill produces a concrete pricing structure — tier names, prices, feature gates, and the breakeven math behind them — for a described SaaS product. It exists because founders either guess a round number ("$29/mo, feels right") or copy a competitor's pricing page without checking whether it covers their own costs.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has a product (or idea) and no price set yet
- Founder wants to add a second tier or change an existing price
- Founder is copying a competitor's price and wants a gut check
- Founder needs to know how many customers = profitable (breakeven)
- Founder is deciding whether to offer a free tier or free trial
- Someone asks whether their price is "too cheap" or "too expensive" for the value delivered

## Input Schema
```
product_description: string (required) — what it does and for whom
running_costs: {
  hosting_per_month: number (optional, estimate if unknown),
  third_party_apis_per_user: number (optional, e.g. AI API costs, SMS costs),
  your_time_value: number (optional) — hourly rate if support/ops time should count as cost
}
target_customer: string (required) — who pays, and roughly what they earn/spend (e.g. "solo real estate agents", "10-person marketing agencies")
competitor_prices: number[] (optional) — known prices of similar tools
desired_monthly_income: number (optional) — what the founder wants this to eventually pay them
```

## Workflow
### Step 1: Establish the value metric
Decide what the customer is actually paying for — per seat, per usage unit (e.g. per email sent, per report generated), or flat per account. Match this to how the target customer thinks about value: a solo user thinks in flat monthly cost; a growing team thinks in per-seat; a usage-spiky product (AI-heavy) should charge close to usage to avoid margin risk on power users.

### Step 2: Estimate true cost per customer
Add up hosting (amortized across expected users), any per-user API costs (this matters a lot for AI-wrapper SaaS — a $5/mo plan can lose money if it calls a $0.50-per-run API twenty times), and payment processor fees (~2.9% + $0.30 typical). If `running_costs` is missing pieces, estimate conservatively and flag the estimate as such — use web_search to check current typical costs (e.g. current OpenAI/Anthropic API pricing, current Stripe fees) rather than relying on possibly-stale numbers.

### Step 3: Anchor against competitors and willingness-to-pay
If `competitor_prices` given, position deliberately — cheaper to undercut, same-price-more-value, or premium if the product is meaningfully better. If not given, use web_search to find 2-3 comparable tools' pricing pages. Cross-reference against `target_customer`'s likely budget (a solo freelancer's tolerance is different from a company with a procurement budget).

### Step 4: Build 2-3 tiers, not one
Standard structure: a low/entry tier that covers costs and proves value, a mid "most popular" tier priced 2.5-4x the entry tier where most revenue should concentrate, and optionally a high tier for power users/teams. Gate tiers on the value metric from Step 1, not arbitrary feature lists — customers should upgrade because they're getting more value, not because a feature was withheld to be annoying.

### Step 5: Calculate breakeven
Fixed monthly costs (hosting, tools, founder's baseline) ÷ (average price − cost per customer) = customers needed to break even. Show this at each tier mix scenario (e.g. all-entry-tier vs. a realistic 70/25/5 split across tiers).

### Step 6: Self-Validation
- [ ] Cost per customer was actually calculated, not skipped
- [ ] At least one tier has healthy margin (>70% gross margin is typical/healthy for SaaS; flag if below)
- [ ] Pricing is anchored to a value metric the customer understands
- [ ] Breakeven number is stated in plain customer count, not just a dollar figure
- [ ] Competitor context was checked (via input or web_search)

## Output Schema
```
{
  value_metric: string,
  tiers: [{ name: string, price_per_month: number, includes: string[], target_segment: string }],
  cost_per_customer_estimate: { hosting: number, api_costs: number, payment_fees: number, total: number },
  gross_margin_pct: number,
  breakeven_customers: number,
  competitor_positioning: string,
  risks: string[]
}
```

## Output Format
```markdown
# Pricing Plan: <product name>

## Tiers
| Tier | Price/mo | Who it's for | Includes |
|---|---|---|---|
| ... | $X | ... | ... |

## Your Cost Per Customer
Hosting: $X | API/usage costs: $X | Payment fees: $X | **Total: $X**
Gross margin at mid tier: X%

## Breakeven
You need **N paying customers** (realistic tier mix) to cover your fixed monthly costs of $X.

## How This Compares
<competitor price positioning in plain language>

## Risks
- <e.g. "your entry tier loses money if a user is a heavy API user — consider a usage cap">

## Next Step
Run `competitor-teardown` for deeper pricing/feature context, or `defensibility-calculator` to check if this pricing is sustainable long-term.
```

## Error Handling
- If `running_costs` is entirely unknown, still produce estimates using industry-typical numbers (state clearly they're estimates) rather than refusing to answer.
- If the product idea has no clear metered cost (e.g. simple CRUD app), skip the API-cost line and note margin is likely to be near-100% at scale.
- If `desired_monthly_income` implies an unrealistic customer count for the target market size, say so plainly rather than inflating the price to make the math work.
- If competitor prices vary wildly (e.g. $9 to $299 for "similar" tools), flag that the category is fragmented and ask which segment (budget/pro/enterprise) the user is actually targeting.
- If the product is free/ad-supported by design, skip tiers and instead calculate revenue-per-user needed from the alternate monetization path.

## Examples
**Example 1**
User: "I built a tool that uses AI to write cold emails. What should I charge?"
→ Skill flags that per-email AI cost must be estimated (uses web_search for current API pricing), builds a 3-tier structure gated on emails/month, and shows that a flat unmetered $9/mo plan would lose money on heavy users — recommends a usage cap or overage pricing instead.

**Example 2**
User: "Competitors charge $49-99/mo for similar project management tools, is that where I should be?"
→ Skill checks target customer segment, recommends entry tier under $49 to compete on price while mid tier matches competitor range, calculates breakeven at both.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `defensibility-calculator` (S2-Planning) — checks if this pricing/margin survives competitive pressure over time
- `prd-writer` (S2-Planning) — tier feature gates become product requirements
- `signup-conversion-tracker` (S7-Growth) — tracks whether real signups match the assumed tier mix

### Fed By
- `competitor-teardown` (S1-Research) — supplies real competitor pricing data to anchor against
- `saas-idea-validator` (S1-Research) — confirms there's a paying market before pricing it

### Feedback Loop
Once live, `signup-conversion-tracker` and `app-performance-report` data on actual tier uptake and churn-by-tier should feed back to recalibrate the assumed tier mix and price points here.

```yaml
chain_metadata:
  skill_slug: "pricing-model-calculator"
  stage: "research"
  timestamp: string
  suggested_next:
    - "defensibility-calculator"
    - "prd-writer"
```
