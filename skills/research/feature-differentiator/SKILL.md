---
name: feature-differentiator
description: >
  Ranks a list of possible product features by whether they actually
  differentiate the product versus whether they're table-stakes that
  competitors already have.
  Use this skill when the user asks about "which features matter", "what should I build first",
  or says
  "which of these features actually matter", "am I wasting time on this feature",
  "what makes my app different", "rank my feature list", "what's table stakes vs. a differentiator",
  "should I build [feature] or is everyone doing that already", "help me cut my feature list down".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "product-strategy", "feature-prioritization"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Feature Differentiator

This skill takes a raw list of possible features for a product and sorts each one into table-stakes (must-have, doesn't differentiate), differentiator (rare, defensible, worth building), or noise (neither expected nor valuable — cut it). It exists to stop founders from burning build time on features that don't move the needle either way.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has a long feature wishlist and needs to know what actually matters
- Deciding what goes in the MVP vs. later
- Founder is tempted to build a feature "because a competitor has it" without checking if it's actually a differentiator
- After a `competitor-teardown`, to formally classify the feature list that emerged
- Founder asks "what makes us different" and the honest answer isn't clear yet

## Input Schema
```
app_idea: string (required)
feature_list: string[] (required) — the candidate features to classify
competitor_feature_data: object (optional) — output from competitor-teardown, if available
target_customer: string (optional) — who the differentiation needs to matter to
```

## Workflow
### Step 1: Get competitor feature baseline
If `competitor_feature_data` is not supplied, run a lightweight version of `competitor-teardown` logic: use web_search to check 3-4 competitors' feature/pricing pages for what they already offer. This baseline is required — differentiation can only be judged relative to what already exists, not in a vacuum.

### Step 2: Classify each feature
For each item in `feature_list`, check it against the competitor baseline and sort into:
- **Table-stakes**: most/all competitors have it. Users expect it; its absence would be noticed, but its presence won't win anyone over. Still may need to be built, just not marketed.
- **Differentiator**: rare or absent among competitors AND solves a real pain point for `target_customer` (not rare because nobody wants it). This is the category worth featuring in marketing and building early.
- **Noise**: neither common among competitors nor clearly wanted by the target customer. Usually a "nice idea" with no evidence behind it — candidate to cut or defer indefinitely.

### Step 3: Stress-test each "differentiator" claim
A feature isn't a real differentiator just because competitors lack it — it might be missing because nobody wants it. Check: does it map to a complaint found in competitor reviews (from `competitor-teardown` weaknesses), or a pain point the founder has direct evidence for (user interviews, their own experience)? If there's no evidence of demand, downgrade it from "differentiator" to "unproven — validate before building."

### Step 4: Rank within the differentiator bucket
Order true differentiators by build effort vs. impact — cheap-to-build + high-impact first. Flag any differentiator that would take disproportionate engineering effort for a non-technical or solo founder; that's a candidate to defer past MVP even if it's genuinely valuable.

### Step 5: Self-Validation
- [ ] Every feature was checked against real competitor data, not assumed
- [ ] "Differentiator" claims are backed by evidence of demand, not just competitor absence
- [ ] Table-stakes features are acknowledged as necessary even though they won't be marketed as special
- [ ] Noise features have a clear reason given for why they're noise
- [ ] Output gives a build-order recommendation, not just a static categorization

## Output Schema
```
{
  table_stakes: string[],
  differentiators: [{ feature: string, evidence: string, build_effort: enum[low,med,high] }],
  unproven: [{ feature: string, why_unproven: string }],
  noise: [{ feature: string, why_cut: string }],
  build_order_recommendation: string[]
}
```

## Output Format
```markdown
# Feature Differentiation: <app name>

## Table Stakes (build, don't market)
- ...

## Real Differentiators (build early, lead with these)
| Feature | Why It's Different | Evidence | Build Effort |
|---|---|---|---|
| ... | ... | ... | Low/Med/High |

## Unproven — Validate Before Building
- <feature>: no evidence of demand yet, why

## Cut These
- <feature>: neither expected nor clearly wanted

## Recommended Build Order
1. ...
2. ...

## Next Step
Run `mvp-feature-slicer` to turn this into an actual MVP scope, or `unique-value-prop-audit` to test messaging built on the differentiators.
```

## Error Handling
- If `feature_list` is empty or the user just wants feature ideas generated, redirect them to describe the product more first — this skill classifies, it doesn't brainstorm from nothing.
- If no competitor data exists and web_search turns up no comparable products, treat the whole space as unproven — say so, and recommend `underserved-market-finder` or direct user interviews before feature-ranking makes sense.
- If every feature turns out to be table-stakes with zero differentiators, say that plainly — it means the current idea has no wedge yet, and that's important to surface, not soften.
- If the user pushes back on a "noise" classification with real evidence Claude didn't have, re-classify based on that evidence — this skill should update, not defend its first answer.

## Examples
**Example 1**
User: "I want to build a client portal for consultants. Features: file sharing, e-signatures, AI meeting summaries, invoicing, branded client login, chat."
→ Skill checks 4 competitors, finds file sharing/e-signatures/invoicing are table-stakes everywhere, branded client login is semi-rare, AI meeting summaries is genuinely rare and maps to a common consultant complaint about post-call admin work → classified as top differentiator, low-med build effort.

**Example 2**
User: "Is a dark mode toggle a differentiator for my app?"
→ Skill classifies as table-stakes (near-universal expectation now) bordering on noise if the target customer never mentioned it — recommends building it eventually but not marketing around it.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `mvp-feature-slicer` (S2-Planning) — turns the ranked list into an actual build scope
- `unique-value-prop-audit` (S1-Research) — differentiators become candidate value-prop claims
- `feature-roadmap-architect` (S2-Planning) — table-stakes and deferred features become later roadmap items

### Fed By
- `competitor-teardown` (S1-Research) — supplies the competitor feature baseline this skill classifies against

### Feedback Loop
Post-launch, `signup-conversion-tracker` and `ab-test-generator` data on which features actually drive signups/retention should feed back to correct any "differentiator" that turned out not to matter to real users.

```yaml
chain_metadata:
  skill_slug: "feature-differentiator"
  stage: "research"
  timestamp: string
  suggested_next:
    - "mvp-feature-slicer"
    - "unique-value-prop-audit"
```
