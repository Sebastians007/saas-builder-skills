---
name: funnel-select
description: >
  Picks the right funnel type for a SaaS or app offer based on price point,
  business model, and goal (leads, trial signups, or a direct sale), then
  hands off to the matching funnel-building skill instead of guessing.
  Use this skill when the user asks about which funnel to build, how to sell
  their product online, or says
  "what kind of funnel do I need", "how do I sell this app", "should I do a webinar or just a landing page",
  "what's the best way to get signups for this", "help me pick a funnel", "I don't know where to start with marketing this",
  "what pages do I actually need", "is my product too cheap for a sales call funnel".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "strategy", "planning", "router"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Funnel Select

Routes a founder to the right funnel type instead of them guessing or copying whatever funnel a guru sold last. Asks a few pointed questions about price, business model, and goal, then recommends one primary funnel (and a fallback) plus the exact page list to build next.

## Stage
This skill belongs to Stage S3: Funnel Build

## When to Use
- The user has a working app or offer but no plan for how to sell it
- The user says "I need a landing page" without knowing if that's actually enough
- Before running any of the 13 specific funnel-builder skills in this pack — this decides which one
- The user is mixing funnel types (e.g., webinar copy on a tripwire page) and needs a reset
- Re-evaluating funnel choice after `pricing-model-calculator` changes the price point
- A `saas-idea-validator` or `prd-writer` pass just finished and it's time to plan distribution

## Input Schema
```
offer_type: string              # "lead magnet" | "product" | "service" | "saas subscription" | "community"
price_point: number | null      # 0 if free, otherwise dollar amount
is_physical_product: boolean
needs_education_before_sale: boolean   # does the buyer need convincing/teaching first?
recurring_revenue: boolean
primary_goal: string            # "grow email list" | "get trial signups" | "make sales" | "book calls" | "grow a community"
audience_temperature: string    # "cold" | "warm" | "existing list"
```

## Workflow
### Step 1: Get the fundamentals
Ask for price point, whether it's a one-time sale or recurring, and whether it's a SaaS product, physical product, service, or community. If the user doesn't know their price yet, point them to `pricing-model-calculator` first — funnel choice depends on price.

### Step 2: Identify the primary goal
Goals map differently than price. "Grow my list" always points to `optin-funnel` or `group-funnel` regardless of eventual price. "Get trial signups" points to `saas-funnel`. "Make sales" or "book calls" routes by price tier.

### Step 3: Run the decision tree
Apply this logic in order:
- Goal is list growth, no product yet → `optin-funnel` (or `group-funnel` if the destination is a community platform like Skool/Discord/Whop)
- Recurring SaaS product → `saas-funnel`
- Recurring content/community subscription → `membership-funnel`
- Physical or digital product under $500, one-time → `ecommerce-funnel`
- Price under $50 and the goal is building a buyer list fast → `tripwire-funnel`
- Price $200–$2,000 and audience needs education first → `webinar-funnel` (live) or `evergreen-webinar-funnel` (automated/scalable)
- Price $200–$2,000, community/cohort based → `challenge-funnel`
- Price $2,000+ and needs qualification before a call → `application-funnel` or `high-ticket-funnel`
- Complex offer that needs a persuasive long-form pitch with no live call → `vsl-funnel`
- Multi-week anticipation build for a big launch (course, new product line) → `product-launch-funnel`

### Step 4: Give a primary and a fallback
Never present only one option. Give the top recommendation with the reasoning tied to price/goal/audience, and a second option for if the first doesn't fit their comfort level (e.g., they don't want to do live calls, so swap `application-funnel` for `vsl-funnel`).

### Step 5: List the exact pages to build
Pull the page list straight from the recommended skill's Output Schema so the user knows what's coming before they commit.

### Step 6: Self-Validation
- [ ] Recommendation is based on stated price + goal, not just guessed
- [ ] A fallback option is included
- [ ] The user knows exactly which funnel-builder skill to run next
- [ ] If price is unknown, `pricing-model-calculator` was flagged as a prerequisite

## Output Schema
```
{
  "primary_recommendation": string,     # funnel skill slug
  "primary_reasoning": string,
  "fallback_recommendation": string,
  "fallback_reasoning": string,
  "page_list": string[],
  "estimated_build_effort": string      # "low" | "medium" | "high"
}
```

## Output Format
```markdown
# Funnel Recommendation

## Primary: <funnel-slug>
**Why:** <reasoning tied to price/goal/audience>
**Pages to build:** <list>
**Effort:** <low/medium/high>

## Fallback: <funnel-slug>
**Why:** <reasoning — when to pick this instead>

## Next Step
Run `<funnel-slug>` to generate the actual page copy and structure.
```

## Error Handling
- If price and goal point to conflicting funnels (e.g., "$5,000 product, goal is just list growth"), ask which matters more right now — the sale or the list — rather than picking silently.
- If the user has no price set yet, stop and recommend `pricing-model-calculator` before proceeding.
- If the offer doesn't cleanly fit any category (e.g., a free tool with a paid API), default to `saas-funnel` and flag the ambiguity.
- If the user insists on a funnel type that doesn't match their price point (e.g., application funnel for a $19 product), warn them plainly and ask for confirmation before proceeding.

## Examples
**Example 1:** A solo founder has a $19/month SaaS tool for freelancers, no email list yet. Recommendation: primary `saas-funnel` (trial-first, matches recurring low-ticket SaaS), fallback `optin-funnel` if they want to build a list before opening trial signups.

**Example 2:** A consultant is launching a $4,500 done-for-you service and wants qualified leads only. Recommendation: primary `application-funnel`, fallback `high-ticket-funnel` if they'd rather skip the application form and go straight to a long-form sales page with a booking CTA.

**Example 3:** A course creator has a $297 course and an engaged Instagram audience (warm). Recommendation: primary `challenge-funnel` (uses existing engagement, builds momentum), fallback `webinar-funnel` if a single big pitch event fits their timeline better.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `optin-funnel`, `saas-funnel`, `webinar-funnel`, `application-funnel`, `tripwire-funnel` (and the other 8 funnel-type skills, depending on recommendation)
- `funnel-copy` — once a funnel type is chosen, this writes the actual page copy

### Fed By
- `pricing-model-calculator` (S5-Planning) — price point must exist before a funnel can be chosen
- `prd-writer` (S5-Planning) — defines the offer this funnel will sell

### Feedback Loop
If `signup-conversion-tracker` or `checkout-funnel-auditor` later shows the chosen funnel isn't converting, re-run `funnel-select` before rebuilding pages from scratch — the funnel type itself, not just the copy, may be the wrong fit for the price point or audience.

```yaml
chain_metadata:
  skill_slug: "funnel-select"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "saas-funnel"
    - "webinar-funnel"
```
