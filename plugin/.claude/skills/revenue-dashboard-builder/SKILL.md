---
name: revenue-dashboard-builder
description: >
  Builds a revenue-specific dashboard covering MRR, churned revenue, LTV, and
  CAC payback in one place, complementing the broader growth-dashboard-builder
  with the numbers investors and the founder actually track week to week.
  Use this skill when the user asks about an MRR dashboard, revenue tracking,
  or says
  "build me a revenue dashboard", "track my MRR", "what's my churn in dollars",
  "how long until CAC pays back", "I need an LTV dashboard", "show me revenue over time",
  "what should I show investors about revenue".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "revenue", "mrr", "dashboard", "posthog"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Revenue Dashboard Builder

This skill builds a single page that tracks MRR, churn in dollars, LTV, and CAC payback — the four numbers that answer "is this a healthy business" better than signup counts do. It complements growth-dashboard-builder (which covers the whole funnel at a glance) by going deep on money specifically. Build growth-dashboard-builder first if it doesn't exist yet; this skill's output gets linked into it as one tile.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- The user has paying customers and needs to track revenue health, not just signups
- The user is preparing investor updates or a board summary and needs real MRR/churn numbers
- growth-dashboard-builder already exists and its Revenue tile needs a deeper linked page
- The user asks "are we actually making more money than last month" and can't answer with a number
- After trial-to-paid-converter or checkout-funnel-auditor ships a change, to see whether it moved MRR or churn
- The user is billing through Stripe (or similar) and has never pulled the numbers into one view

## Input Schema
```
billing_provider: string?        # e.g. "Stripe", defaults to "Stripe"
analytics_tool: string?          # defaults to "PostHog" for usage-linked revenue events
hosting_target: string?          # defaults to "Cloudflare Pages"
plan_structure: array?           # plan names + prices, if known
current_customer_count: number?
known_cac: number?               # blended customer acquisition cost, if known
time_range: string?              # defaults to "last 12 months"
```

## Workflow
### Step 1: Lock the Four Numbers
Don't build a revenue dashboard with everything Stripe can export. Four numbers, defined precisely:
- **MRR** — sum of active subscription value normalized to monthly, broken into New + Expansion + Contraction + Churned (a single MRR line hides which direction is driving the change)
- **Churned revenue ($)** — dollars lost to cancellation/downgrade this period, separate from logo churn (a business can have low logo churn and still bleed dollars if big accounts are shrinking)
- **LTV** — average revenue per customer over their lifetime, computed as ARPU ÷ monthly churn rate (simple version) — flag this as a rough estimate, not gospel, until 12+ months of cohort data exists
- **CAC payback** — months of gross margin needed to recover the cost of acquiring a customer; needs a CAC number from the user (spend ÷ customers acquired in the period) — if the user doesn't track CAC yet, note it as a gap rather than guessing

### Step 2: Get the Data
- Stripe (or the billing provider) is the source of truth for MRR and churned revenue — pull via Stripe's own reporting or a CSV export, not manual tracking
- PostHog is the source for usage-linked context (which plan/cohort is churning, tied to product events) — use PostHog's API to join subscription events with usage data when the user wants to know *why* revenue churned, not just that it did
- If neither is instrumented, stop and specify the minimum: `subscription_started`, `subscription_upgraded`, `subscription_downgraded`, `subscription_canceled` events with plan and amount properties

### Step 3: Choose the Build Approach
Same two options as growth-dashboard-builder, applied to revenue data specifically:
- **Fastest**: Stripe's own built-in reporting/dashboard already computes MRR, growth rate, and churn — start here if it's enough
- **Custom**: a small Cloudflare Pages page + Pages Function that pulls Stripe's API (billing data) and, where needed, PostHog's API (usage context), cached and refreshed on a schedule. Never expose Stripe secret keys client-side — proxy through a Function holding the key as a Cloudflare secret, restricted to read-only reporting scopes where Stripe permits it.
- Avoid recommending paid subscription-analytics tools (ChartMogul, Baremetrics, ProfitWell) unless the user is already paying for one and just wants it summarized — for a pre-scale SaaS, Stripe's native reporting plus a simple custom page covers it for free.

### Step 4: Lay Out the Page
1. One-line status: "MRR: $[X], up/down $[Y] from last month ([Z]% churn)"
2. MRR over time, stacked by New / Expansion / Contraction / Churned
3. Churned revenue this period, with the top 3 accounts that churned (if small customer count, name them; if large, show the segment)
4. LTV and CAC payback side by side, with LTV:CAC ratio (aim for 3:1+ as a rough health check, flag if under)
5. Link back to growth-dashboard-builder for the acquisition/activation/retention view this page doesn't cover

### Step 5: Set the Update Cadence
- Monthly is usually the right cadence for revenue (unlike daily-refresh growth metrics) — MRR doesn't meaningfully change day to day for most early SaaS businesses
- Recommend the user close the books on the 1st of each month, update the dashboard, and write one sentence on what drove the change

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Exactly the four numbers (MRR breakdown, churned $, LTV, CAC payback) are shown, not a Stripe data dump
- [ ] MRR is broken into New/Expansion/Contraction/Churned, not a single line
- [ ] LTV and CAC payback are both flagged as estimates if underlying data is thin
- [ ] No paid BI/subscription-analytics tool is recommended unless the user already has one
- [ ] The page links to growth-dashboard-builder rather than duplicating its acquisition/activation tiles

## Output Schema
```json
{
  "mrr_breakdown": {"new": "number", "expansion": "number", "contraction": "number", "churned": "number", "net_mrr": "number"},
  "churned_revenue": "number",
  "ltv": "number",
  "ltv_confidence": "estimate|validated",
  "cac": "number|null",
  "cac_payback_months": "number|null",
  "ltv_cac_ratio": "number|null",
  "data_source": "string",
  "build_approach": "stripe_native|cloudflare_pages_custom",
  "instrumentation_gaps": ["string"]
}
```

## Output Format
```markdown
# Revenue Dashboard Spec

## This Month
MRR: $[X] ([+/-][Y]% vs last month) | Churned: $[Z] | LTV: $[A] | CAC payback: [B] months

## MRR Breakdown
| Component | Amount |
|---|---|
| New | $[x] |
| Expansion | $[x] |
| Contraction | -$[x] |
| Churned | -$[x] |
| **Net MRR** | **$[x]** |

## LTV : CAC
LTV $[x] / CAC $[y] = [ratio]:1 — [healthy (3:1+) | watch | unhealthy]

## Build Approach
[Stripe native | Cloudflare Pages custom]

## Instrumentation Gaps
[what's missing before this is trustworthy]

## Do Not
- Report a single blended MRR number without the New/Expansion/Contraction/Churned split
- Treat LTV as precise with under 12 months of cohort data
- Recommend a paid subscription-analytics tool before Stripe's own reporting has been tried
```

## Error Handling
- No CAC data → report LTV alone, mark CAC payback as "unavailable" rather than guessing a CAC number
- Fewer than ~20 paying customers → flag that LTV and churn % will be noisy, widen the time window before trusting trends
- Billing provider isn't Stripe → ask which provider, adapt the same four-number structure to whatever export/API it offers
- User wants vanity metrics (total revenue ever, total signups) mixed in → keep those off this dashboard, they don't answer "is the business healthy right now"
- Stripe secret key requested for client-side use → refuse, require a server-side proxy (Cloudflare Pages Function) instead

## Examples
**Example 1**
User: "I want to know our MRR trend for an investor update."
Skill: Pulls Stripe's native MRR report first (fastest, no build needed), breaks it into New/Expansion/Contraction/Churned, and formats it for a one-slide investor summary.

**Example 2**
User: "We just ran a trial-to-paid experiment, did it move revenue?"
Skill: Compares MRR new-additions and CAC payback before/after the experiment window, ties the result back to trial-to-paid-converter's hypothesis.

**Example 3**
User: "Should I pay for ChartMogul?"
Skill: Explains Stripe's native reporting plus this dashboard covers the same four numbers for free at this customer count; recommends revisiting a paid tool only once the business needs multi-currency/multi-entity consolidation Stripe's reporting doesn't handle well.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- growth-dashboard-builder
- pricing-model-calculator

### Fed By
- trial-to-paid-converter
- checkout-funnel-auditor
- cohort-churn-analyzer

### Feedback Loop
Every pricing, checkout, or trial-conversion change from upstream skills should show up as a visible shift in the MRR breakdown or LTV:CAC ratio here within one billing cycle — if it doesn't, the upstream fix likely didn't work as intended.

```yaml
chain_metadata:
  skill_slug: "revenue-dashboard-builder"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "growth-dashboard-builder"
    - "pricing-model-calculator"
```
