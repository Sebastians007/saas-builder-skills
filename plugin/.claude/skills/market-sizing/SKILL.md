---
name: market-sizing
description: >
  Sizes the actual market for an app or service idea — TAM, SAM, SOM, and
  growth rate — with sourced numbers, not invented figures.
  Use this skill when the user asks about "how big is this market", "is this
  worth pursuing", or says
  "what's the market size for this", "is this market growing or shrinking",
  "how many potential customers are there", "is this a big enough opportunity",
  "what's my TAM", "give me the market numbers", "how fast is this space growing",
  "is this a real market or a niche".
license: MIT
version: "1.0.0"
tags: ["saas", "research", "market-sizing", "tam-sam-som"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Market Sizing

Produces a real, sourced market size for an app or service idea — Total Addressable Market (TAM), Serviceable Addressable Market (SAM), Serviceable Obtainable Market (SOM), and the category's growth rate. This exists because a founder can validate an idea against competitors and still not know if the market itself is big enough or growing fast enough to matter — that's a different question, and one no other skill in this pack answers.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Before committing real time to an idea, to confirm the market is actually big enough
- After `competitor-teardown`, to check whether a crowded market is crowded because it's big, or crowded because it's small and everyone's fighting over scraps
- Investor or stakeholder conversations that need real market numbers, not a guess
- As an input to `research-report-builder`'s compiled report
- The user says a market "feels small" or "feels huge" and wants an actual number instead of a feeling

## Input Schema
```
{
  category: string              # the market/category to size, as specific as possible
  geography: string?            # default: "United States" — narrows TAM appropriately
  target_segment: string?       # from underserved-market-finder or avatar-extraction, if narrower than the full category
}
```

## Workflow

### Step 1: Define the Category Precisely
A category that's too broad ("business software") produces a useless, inflated TAM. Narrow it to the actual thing being sold (e.g. "AI governance consulting for SMBs," not "cybersecurity").

### Step 2: Find TAM (Total Addressable Market)
Use `web_search` to find published market-size reports, industry association data, or analyst estimates (Gartner, IBISWorld, Statista summaries, trade publications) for the full category. Cite the actual source — never estimate from nothing. If multiple sources disagree, report the range, not a single invented average.

### Step 3: Narrow to SAM (Serviceable Addressable Market)
From the TAM, narrow by what this specific business can actually reach — geography, business size served, price point served, channel reach. Show the narrowing math explicitly (e.g. "TAM is $X globally; SAM is $X × [% that is US-based SMBs] = $Y").

### Step 4: Estimate SOM (Serviceable Obtainable Market)
From the SAM, estimate what's realistically capturable in 1-3 years given the founder's actual resources (solo/small team, no existing distribution) — this is deliberately conservative, not aspirational.

### Step 5: Find the Growth Rate
Search for the category's CAGR (compound annual growth rate) from the same sourced reports. Note whether growth is accelerating, flat, or declining, and why (a regulatory driver, a technology shift, a one-time trend) — the "why" matters more than the number alone for judging durability.

### Step 6: Self-Validation
- [ ] TAM has a cited source, not an invented figure
- [ ] SAM's narrowing logic from TAM is shown, not just stated
- [ ] SOM is conservative and tied to the founder's actual reach, not wishful
- [ ] Growth rate is sourced and the driver behind it is named
- [ ] If sources disagree, the range is reported honestly, not averaged into a fake precise number

## Output Schema
```
{
  category: string
  tam: { value: string, source: string }
  sam: { value: string, narrowing_logic: string }
  som: { value: string, timeframe: string, reasoning: string }
  growth_rate: { cagr: string, source: string, driver: string, trend: string }
  verdict: string   # "large and growing" | "large but flat/declining" | "small but growing fast" | "small and flat — niche"
}
```

## Output Format
```markdown
## Market Sizing: [Category]

**TAM:** [$ figure] — [source, with link/citation]
**SAM:** [$ figure] — narrowed from TAM by [logic: geography/segment/price point]
**SOM:** [$ figure] — realistic 1-3 year capture given [founder's actual resources]

**Growth rate:** [X]% CAGR ([source]) — [accelerating/flat/declining], driven by [named driver]

**Verdict:** [One of: large and growing / large but flat / small but growing fast / small and flat — niche]

**What this means for the idea:** [1-2 sentences translating the numbers into a go/caution signal]
```

## Error Handling
- **No published data exists for a hyper-specific category:** Size the nearest broader category with real data, then apply a reasoned narrowing percentage, and flag clearly that SOM/SAM are estimates built on a proxy category.
- **Sources wildly disagree:** Report the full range, note which source is more credible/recent, and don't average them into false precision.
- **Category is genuinely brand new (no market data exists at all):** Say so plainly — this is itself a data point (could mean genuine first-mover territory, or could mean no real demand yet) — and route to `saas-idea-validator` for a demand-signal check instead of fabricating a number.

## Examples

**Example 1:**
User: "How big is the AI governance consulting market for small businesses?"
→ Search finds a broader "AI governance software and services" market report with a global TAM
→ Narrow SAM to US SMB segment specifically (much smaller slice)
→ SOM: realistic first-year capture for a solo/small consultancy is a tiny fraction of SAM
→ Growth rate: high CAGR, driven by new state-level AI regulation — flag this as a real tailwind

**Example 2:**
User: "Is the market for [very niche idea] even real?"
→ No direct market report exists
→ Size the nearest adjacent category, apply a conservative narrowing estimate, flag it clearly as a proxy-based estimate
→ Recommend `saas-idea-validator` to check actual demand signal alongside the sizing

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- research-report-builder (S1-Research) — this skill's output is one of the four inputs the compiled report needs
- saas-idea-validator (S1-Research) — market size/growth feeds into the overall go/pivot/kill score
- pricing-model-calculator (S1-Research) — SOM realism check against planned pricing/volume assumptions

### Fed By
- underserved-market-finder (S1-Research) — can hand off a specific niche to size instead of the full category

### Feedback Loop
- If `attribution-mapper` or real signup data later shows actual market response is much stronger or weaker than the SOM estimate predicted, that's a signal to re-run this skill with corrected assumptions for the next idea.

```yaml
chain_metadata:
  skill_slug: "market-sizing"
  stage: "research"
  timestamp: string
  suggested_next:
    - "research-report-builder"
    - "saas-idea-validator"
```
