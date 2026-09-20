---
name: pricing-page-optimizer
description: >
  Reviews and rewrites a SaaS pricing page's plan structure, tier framing, and
  copy for conversion, using a fixed pricing-psychology checklist instead of a
  vague "make it better" pass.
  Use this skill when the user asks about pricing page conversion, plan structure,
  or says
  "audit our pricing page", "rewrite our pricing", "are we priced right", "help me repackage our plans",
  "why do people bounce from the pricing page", "should we have 3 tiers or 4", "our pricing page isn't converting".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "pricing", "conversion", "revenue", "copywriting"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Pricing Page Optimizer

This skill audits a SaaS pricing page against a fixed pricing-psychology checklist — plan structure, naming, feature matrix, CTAs, objection handling — then produces a rewritten version with a before/after rationale for every change. It's about how the page presents the price, not what the price should be (pricing-model-calculator handles that).

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The user has a live pricing page and a conversion rate that feels low but hasn't been diagnosed
- The user is repackaging or renaming plans and wants a structural review before publishing
- People land on the pricing page and bounce without starting a trial
- After pricing-model-calculator sets the actual price points, to design how the page presents them
- The user wants competitor pricing pages compared against their own structure, not just their number

## Input Schema
```
pricing_page_url: string?             # or a description/screenshot if no live URL
current_plans: array                  # required: [{name, price, billing_period, features}]
competitor_pricing_urls: array?       # 2-5 competitors' pricing pages
customer_plan_mix: object?            # % of paying customers per plan, if known
pricing_page_conversion_rate: number? # pricing page -> trial/purchase, if known
audience_segment: string?             # who typically lands on this page
```

## Workflow
### Step 1: Audit Plan Structure
- **Plan count**: 3 is the sweet spot for self-serve SaaS; a 4th plan is only justified by a genuinely distinct enterprise tier (custom pricing, SSO, dedicated support) — not just "more of the same features"
- **Decoy effect**: is the middle plan clearly framed as the best value (badge, highlight color, "most popular")? If all three plans look equally weighted, the page isn't doing its job
- **Anchoring**: is the highest plan visible enough to make the middle plan look reasonably priced by comparison?
- **Usage-based vs. seat-based**: does the pricing axis match how the customer actually gets more value (more seats, more usage, more projects)? Mismatched axes create billing surprises and churn
- **Annual discount**: is it compelling (15%+)? Is monthly or annual the default toggle state? Default to whichever the business needs more (cash now vs. lower churn commitment)

### Step 2: Audit Plan Naming
Names should require zero explanation. Prefer:
- **Persona-based** (Solo / Team / Business) — usually best for self-serve
- **Scale-based** (Starter / Pro / Enterprise) — the safe, well-understood default
- **Use-case-based** (Build / Ship / Scale) — works when it maps to a real usage journey

Avoid cute/abstract names ("Acorn / Oak / Forest") that make the buyer stop and decode what tier they need — that hesitation is a drop-off point.

### Step 3: Audit the Feature Matrix
- Must be scannable in under 10 seconds — if a buyer has to study it, it's too dense
- Most differentiating row goes near the top, not buried
- Replace checkmark-only rows with quantified differences where possible ("5 projects" vs. "Unlimited projects" beats two identical checkmarks that make plans feel interchangeable)
- "Unlimited" claims belong on the top tier only — using it on a mid-tier undercuts the reason to upgrade

### Step 4: Audit the Hero and CTAs
- Each plan states who it's for in one line, not just a feature list
- Exactly one CTA per plan — never both "Start trial" and "Contact sales" on the same card, it splits intent
- The free-trial/self-serve CTA is visually dominant over "Contact sales" unless the business is intentionally enterprise-led
- No pricing information below the fold on the primary viewport

### Step 5: Audit Objection Handling
- FAQ directly below the pricing table covering: refund policy, annual-to-monthly switching, team/seat billing, security/compliance basics, trial terms
- Social proof near the table (logos, or one quote tied to a specific tier) where available
- A stated guarantee (money-back window, cancel-anytime language) reduces the biggest unstated objection: "what if I regret this"

### Step 6: Rewrite the Page
Produce, for each plan: a rewritten one-line hero, a cleaned feature matrix (flag which rows to cut and which quantified rows to add), and a rewritten CTA. For every change, state what was wrong with the original and why the rewrite fixes it — a rewrite without rationale can't be evaluated or learned from.

### Step 7: Propose Tests, Don't Just Ship Opinion
Recommend 1-2 concrete A/B tests from the rewrite (e.g. plan name swap, annual-default toggle, CTA copy change) and hand off to ab-test-generator rather than treating the rewrite as automatically correct.

### Step 8: Self-Validation
Before presenting output, confirm:
- [ ] Plan count, naming, feature matrix, hero/CTA, and objection handling were all audited, not just one area
- [ ] Every flagged issue in the rewrite has a stated rationale, not just a change
- [ ] The middle-plan decoy effect and anchoring were explicitly checked
- [ ] At least one testable hypothesis is handed off to ab-test-generator rather than shipped as unverified opinion
- [ ] Competitor pricing pages (if provided) were compared structurally, not just on raw price

## Output Schema
```json
{
  "plan_structure_audit": {"plan_count": "number", "decoy_effect_present": "boolean", "anchoring_present": "boolean", "pricing_axis": "string", "annual_discount_pct": "number|null"},
  "naming_audit": [{"current_name": "string", "issue": "string|null"}],
  "feature_matrix_issues": ["string"],
  "cta_issues": ["string"],
  "objection_handling_gaps": ["string"],
  "rewrite": [
    {"plan": "string", "new_hero_line": "string", "matrix_changes": ["string"], "new_cta": "string", "rationale": "string"}
  ],
  "proposed_tests": ["string"]
}
```

## Output Format
```markdown
# Pricing Page Audit

## Plan Structure
[plan count, decoy effect, anchoring, pricing axis, annual discount — pass/fail each]

## Naming
| Current | Issue |
|---|---|
| [name] | [issue or "clear, no change"] |

## Feature Matrix Issues
- [issue]

## CTA Issues
- [issue]

## Objection Handling Gaps
- [gap]

## Rewrite
### [Plan name]
**Before:** [current hero line]
**After:** [new hero line]
**Why:** [rationale]
**Matrix changes:** [list]
**CTA:** [before] → [after]

## Proposed Tests
1. [hypothesis] — hand off to ab-test-generator

## Do Not
- Ship the rewrite without an A/B test on at least the highest-risk change
- Rename plans to something clever that requires explanation
- Put "Unlimited" on more than the top tier
```

## Error Handling
- No current plan data provided → ask for it; cannot audit structure or write a rewrite without knowing existing plans/prices
- Pricing page conversion rate unknown → proceed with the structural/copy audit, note that impact can't be quantified until a baseline conversion rate is captured (point to signup-conversion-tracker or a PostHog funnel)
- User wants a 4th "just in case" plan with no distinct enterprise need → push back, explain the added-choice tax on conversion, keep it to 3 unless a genuine tier justifies it
- Competitor URLs provided but not accessible → note which ones and proceed with the rest, flag the gap rather than guessing competitor structure
- User asks this skill to set the actual price number → redirect to pricing-model-calculator; this skill only covers how the price is presented, not what it should be

## Examples
**Example 1**
User: "We have Free / Pro ($20) / Business ($80) / Enterprise (call us), 80% of paid users are on Pro. Is our pricing page structured right?"
Skill: Confirms 4 tiers is justified given the distinct enterprise tier, checks whether Pro (the dominant plan) is visually anchored as the "most popular" choice, and finds it isn't — recommends adding the decoy-effect highlight as the top fix.

**Example 2**
User: "Should we rename our plans, they're called Ignite / Momentum / Velocity and nobody gets it."
Skill: Flags the abstract naming as a decode-tax on the buyer, proposes scale-based names (Starter / Pro / Business) as a lower-risk swap, and hands it to ab-test-generator as a name-swap test rather than shipping it as a unilateral rewrite.

**Example 3**
User: "People land on pricing and just leave, no trial starts."
Skill: Audits CTA clarity first (often the highest-leverage fix), finds two competing CTAs per plan card, consolidates to one CTA per plan, and checks whether pricing data is visible above the fold on mobile.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- checkout-funnel-auditor
- ab-test-generator
- pricing-model-calculator

### Fed By
- revenue-dashboard-builder
- unique-value-prop-audit

### Feedback Loop
After a pricing page rewrite ships, watch pricing-page-conversion-rate and the plan mix in revenue-dashboard-builder for 2-4 weeks to confirm the change moved conversion or shifted the mix toward the intended plan before iterating further.

```yaml
chain_metadata:
  skill_slug: "pricing-page-optimizer"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "ab-test-generator"
```
