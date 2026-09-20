---
name: competitor-teardown
description: >
  Researches 3-5 real competitors for an app idea and reports their pricing,
  features, positioning, and weaknesses in one comparable table.
  Use this skill when the user asks about "who else does this", "competitor research",
  or says
  "who are my competitors", "what does the competition charge", "tear down my competitors",
  "is anyone already building this", "how do I compare to [competitor]",
  "find weaknesses in [competitor]", "what's already out there for [idea]".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "competitive-research", "market-research"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Competitor Teardown

This skill produces a side-by-side breakdown of 3-5 real, currently-operating competitors for a described app idea — their pricing, core features, positioning, and the specific weaknesses a new entrant could exploit. It exists so founders stop building blind and instead build against a mapped landscape.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Before building anything, to confirm what already exists
- Founder names a specific competitor and wants a full profile of them
- Founder is deciding on positioning and needs to know what's already claimed
- Founder wants to know if a market is crowded or empty
- Preparing for `unique-value-prop-audit` or `feature-differentiator`, which both need real competitor data as input

## Input Schema
```
app_idea: string (required) — what the app does
known_competitors: string[] (optional) — names, if the user already knows some
target_market: string (optional) — narrows search (e.g. "US small business" vs "enterprise")
depth: enum [quick-scan, full-teardown] (default: full-teardown)
```

## Workflow
### Step 1: Find the competitor set
If `known_competitors` given, start there. Always also use web_search to find 2-4 more — search variations like "<app category> software", "<app category> alternative to <known competitor>", and check listing sites (G2, Capterra, Product Hunt, AlternativeTo) for the category. Aim for 3-5 real, currently-live competitors — not defunct products, not tangential tools.

### Step 2: Pull pricing for each
For each competitor, use web_search / fetch their pricing page directly. Record: tier names, prices, what's gated behind each tier, and whether they offer a free tier/trial. If pricing is hidden ("contact sales"), note that explicitly — it's itself a data point (usually signals enterprise-focused, high-touch sales).

### Step 3: Map core features
List each competitor's 4-6 headline features (from their homepage/features page, not assumptions). Build a simple presence table across all competitors so patterns emerge — which features are universal (table stakes) and which only 1-2 competitors have (potential differentiators, hand this to `feature-differentiator`).

### Step 4: Read their positioning
Pull each competitor's homepage headline/subheadline verbatim. This reveals who they say they're for and what problem they claim to solve. Note repeated language across competitors (a sign of a stale, copied category narrative) versus genuinely distinct angles.

### Step 5: Find the weaknesses
For each competitor, check: recent reviews (G2, Capterra, Reddit, Twitter/X search) for repeated complaints, how outdated their UI/tech looks, what they explicitly don't do (missing from their feature list but requested in reviews), and their pricing pain points (complaints about being too expensive, confusing tiers, forced annual billing). This is the most valuable part of the output — do not skip it even in quick-scan mode.

### Step 6: Self-Validation
- [ ] 3-5 real, currently-live competitors identified (not defunct, not tangential)
- [ ] Pricing pulled from actual pricing pages, not guessed
- [ ] At least one concrete, sourced weakness found per competitor (review complaint, missing feature, or outdated tech)
- [ ] Positioning quotes are verbatim from competitor sites, not paraphrased
- [ ] Table format makes competitors genuinely comparable (same columns for each)

## Output Schema
```
{
  competitors: [{
    name: string,
    url: string,
    pricing_tiers: [{ name: string, price: string }],
    core_features: string[],
    positioning_headline: string,
    weaknesses: string[],
    weakness_sources: string[]
  }],
  market_pattern: string,
  whitespace_observations: string[]
}
```

## Output Format
```markdown
# Competitor Teardown: <category>

## The Field
| Competitor | Pricing | Key Features | Positioning | Biggest Weakness |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## What's Table Stakes
Features every competitor has: ...

## What's Rare (Potential Differentiator)
Features only 1-2 competitors have: ...

## Weaknesses Worth Exploiting
- **<Competitor>**: <specific, sourced complaint or gap>

## Market Pattern
<1-2 sentences on how this category is positioned overall, and where the whitespace might be>

## Next Step
Run `feature-differentiator` to rank features against this competitor set, or `unique-value-prop-audit` to test a positioning angle against it.
```

## Error Handling
- If fewer than 3 real competitors exist, say so directly — this is a meaningful signal (either a genuinely underserved niche, or a market too small to matter) and should route to `underserved-market-finder` or `saas-idea-validator` for a demand check.
- If a competitor's pricing is fully gated behind "contact sales," report that as-is rather than guessing a number.
- If reviews/complaints can't be found for a competitor (too small/new), note the gap rather than fabricating weaknesses.
- If the app idea is too broad to define a competitor set (e.g. "a productivity app"), ask the user to narrow to a specific use case first.
- If `known_competitors` includes a company that's actually a different category (user misidentified it), flag the mismatch before including it.

## Examples
**Example 1**
User: "I want to build a scheduling tool for personal trainers. Who's already doing this?"
→ Skill searches, finds Trainerize, PTminder, TrueCoach, Vagaro, and a couple smaller entrants. Pulls pricing, finds review complaints (e.g. "clunky client-facing app," "expensive for solo trainers"), and reports the pattern that most tools target studios, not solo trainers — a whitespace observation.

**Example 2**
User: "Tear down Notion for my note-taking app idea."
→ Skill treats Notion as the primary known competitor, adds 3-4 direct alternatives (Obsidian, Craft, Coda), builds the comparison table, and surfaces specific complaint themes from recent reviews (e.g. "too complex for simple note-taking," "slow on mobile").

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-differentiator` (S1-Research) — uses the feature presence table to rank differentiators
- `unique-value-prop-audit` (S1-Research) — tests a value prop against these exact competitors
- `pricing-model-calculator` (S1-Research) — supplies real competitor pricing to anchor against
- `saas-idea-validator` (S1-Research) — competitive density is one of its scoring inputs

### Fed By
- `underserved-market-finder` (S1-Research) — can hand off a specific niche to run a teardown against

### Feedback Loop
When `competitive-intelligence`-style downstream findings (win/loss patterns, new competitor moves) surface post-launch, this teardown should be re-run periodically rather than treated as a one-time snapshot — competitor pricing and features shift.

```yaml
chain_metadata:
  skill_slug: "competitor-teardown"
  stage: "research"
  timestamp: string
  suggested_next:
    - "feature-differentiator"
    - "unique-value-prop-audit"
```
