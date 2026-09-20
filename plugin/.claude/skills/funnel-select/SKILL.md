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

Routes a founder to the right funnel *type* instead of them guessing or copying whatever funnel a guru sold last — a quick answer for "what kind of funnel do I even need," without triggering a full build. Asks a few pointed questions about price, business model, and goal, then recommends one primary funnel type (and a fallback), and hands off to `funnel-builder-orchestrator` to actually build it when the user is ready.

## Stage
This skill belongs to Stage S3: Funnel Build

## When to Use
- The user just wants to know what kind of funnel fits, before committing to a full build
- The user says "I need a landing page" without knowing if that's actually enough
- The user is mixing funnel types (e.g., webinar copy on a tripwire page) and needs a reset
- Re-evaluating funnel choice after `pricing-model-calculator` changes the price point
- A `saas-idea-validator` or `prd-writer` pass just finished and it's time to plan distribution

Note: `funnel-builder-orchestrator` also recommends a funnel type as part of its own intake — use this skill instead when the user wants just the type recommendation without starting a full build, or wants a second opinion before committing.

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
Goals map differently than price. "Grow my list" always points to a **lead magnet / opt-in** funnel type regardless of eventual price. "Get trial signups" points to a **free trial / SaaS** funnel type. "Make sales" or "book calls" routes by price tier.

### Step 3: Run the decision tree
Apply this logic in order, naming a funnel *type* (not a removed standalone skill — all of these are built via `funnel-builder-orchestrator`, which takes the type as input):
- Goal is list growth, no product yet → **Lead Magnet / Opt-in** (or a community-destination variant if the goal is a Skool/Discord/Whop group)
- Recurring SaaS product → **Free Trial / SaaS**
- Recurring content/community subscription → **Membership**
- Physical or digital product under $500, one-time → **Free + Shipping / Book** or standard e-commerce checkout
- Price under $50 and the goal is building a buyer list fast → **Low-Ticket / Tripwire**
- Price $200–$2,000 and audience needs education first → **Webinar** (live or evergreen)
- Price $200–$2,000, community/cohort based → **5-Day Challenge**
- Price $2,000+ and needs qualification before a call → **High-Ticket / Application**
- Complex offer that needs a persuasive long-form pitch with no live call → **VSL** (video sales letter)
- Multi-week anticipation build for a big launch (course, new product line) → **Product / Course Launch**
- Segmented lead gen where different answers lead to different offers → **Quiz**

### Step 4: Give a primary and a fallback
Never present only one option. Give the top recommendation with the reasoning tied to price/goal/audience, and a second option for if the first doesn't fit their comfort level (e.g., they don't want to do live calls, so swap High-Ticket/Application for VSL).

### Step 5: Hand Off
Tell the user the recommended type, then hand off to `funnel-builder-orchestrator` (pass the funnel type directly so it skips re-asking) to actually build the pages, emails, and every other asset the type needs.

### Step 6: Self-Validation
- [ ] Recommendation is based on stated price + goal, not just guessed
- [ ] A fallback option is included
- [ ] The user knows exactly which funnel-builder skill to run next
- [ ] If price is unknown, `pricing-model-calculator` was flagged as a prerequisite

## Output Schema
```
{
  "primary_recommendation": string,     # funnel type name, e.g. "Webinar", "High-Ticket / Application"
  "primary_reasoning": string,
  "fallback_recommendation": string,
  "fallback_reasoning": string,
  "estimated_build_effort": string      # "low" | "medium" | "high"
}
```

## Output Format
```markdown
# Funnel Recommendation

## Primary: <funnel type>
**Why:** <reasoning tied to price/goal/audience>
**Effort:** <low/medium/high>

## Fallback: <funnel type>
**Why:** <reasoning — when to pick this instead>

## Next Step
Run `funnel-builder-orchestrator` with this funnel type to generate the actual pages, emails, and every other asset it needs.
```

## Error Handling
- If price and goal point to conflicting funnel types (e.g., "$5,000 product, goal is just list growth"), ask which matters more right now — the sale or the list — rather than picking silently.
- If the user has no price set yet, stop and recommend `pricing-model-calculator` before proceeding.
- If the offer doesn't cleanly fit any category (e.g., a free tool with a paid API), default to **Free Trial / SaaS** and flag the ambiguity.
- If the user insists on a funnel type that doesn't match their price point (e.g., an application funnel for a $19 product), warn them plainly and ask for confirmation before proceeding.

## Examples
**Example 1:** A solo founder has a $19/month SaaS tool for freelancers, no email list yet. Recommendation: primary **Free Trial / SaaS** (trial-first, matches recurring low-ticket SaaS), fallback **Lead Magnet / Opt-in** if they want to build a list before opening trial signups.

**Example 2:** A consultant is launching a $4,500 done-for-you service and wants qualified leads only. Recommendation: primary **High-Ticket / Application**, fallback **VSL** if they'd rather skip the application form and go straight to a long-form sales page with a booking CTA.

**Example 3:** A course creator has a $297 course and an engaged Instagram audience (warm). Recommendation: primary **5-Day Challenge** (uses existing engagement, builds momentum), fallback **Webinar** if a single big pitch event fits their timeline better.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `funnel-builder-orchestrator` (S3-Funnel-Build) — the chosen type is passed straight in so it skips re-asking during intake

### Fed By
- `pricing-model-calculator` (S1-Research) — price point must exist before a funnel type can be chosen
- `prd-writer` (S5-Planning) — defines the offer this funnel will sell

### Feedback Loop
If `signup-conversion-tracker` or `checkout-funnel-auditor` later shows the chosen funnel isn't converting, re-run `funnel-select` before rebuilding pages from scratch — the funnel type itself, not just the copy, may be the wrong fit for the price point or audience.

```yaml
chain_metadata:
  skill_slug: "funnel-select"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "funnel-builder-orchestrator"
```
