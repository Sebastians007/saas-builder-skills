---
name: copy-framework-selector
description: >
  Picks the right classic copywriting framework (AIDA, PAS, BAB, PASTOR,
  StoryBrand SB7, QUEST, 4 Ps) for a piece of copy based on the audience's
  awareness stage, instead of defaulting to one framework for everything.
  Use this skill when the user asks about "what structure should this copy
  follow", "which framework fits this", or says
  "should this be AIDA or PAS", "what's the right structure for this page",
  "help me pick a copywriting framework", "this copy feels random, what
  structure should it have", "write this using StoryBrand", "what's the
  difference between these copy frameworks for my situation".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "frameworks", "strategy"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Copywriting
---

# Copy Framework Selector

Different copywriting frameworks fit different situations — a cold, unaware audience needs a different structure than someone already comparing solutions. This skill reads the audience's awareness stage (from `schwartz-awareness-mapper`) and the copy's actual job (ad, landing page, email, long-form sales page) and picks the one framework that fits, instead of the copy defaulting to whatever the founder half-remembers from a marketing blog post.

## Stage
This skill belongs to Stage S10: Copywriting

## When to Use
- After `schwartz-awareness-mapper` has identified the audience's awareness stage, before writing the actual copy
- The founder has copy that "feels random" or unstructured
- Choosing between multiple valid approaches for the same piece of copy
- Briefing `funnel-copy`, `landing-page-generator`, or any other copy-writing skill on which structure to follow

## Input Schema
```
{
  awareness_stage: string     # from schwartz-awareness-mapper: unaware | problem-aware | solution-aware | product-aware | most-aware
  copy_type: string           # "ad" | "landing-page" | "email" | "long-form-sales-page" | "social-post"
  offer_price_point: string   # (optional) low-ticket | mid-ticket | high-ticket — affects long-form vs. short-form choice
}
```

## Workflow

### Step 1: Confirm the Awareness Stage
If not already known from `schwartz-awareness-mapper`, ask or infer it. This is the single biggest factor in framework choice — get it wrong and the copy talks past the reader.

### Step 2: Match Stage + Format to a Framework

| Awareness Stage | Short copy (ad/social/email subject) | Long copy (landing/sales page) |
|---|---|---|
| Unaware | AIDA (build attention from zero) | StoryBrand SB7 (make them the hero, teach them the problem exists) |
| Problem-aware | PAS (Problem-Agitate-Solve) | PASTOR (Problem-Amplify-Story-Transformation-Offer-Response) |
| Solution-aware | BAB (Before-After-Bridge) | BAB, expanded with proof sections |
| Product-aware | QUEST (Qualify-Understand-Educate-Stimulate-Transition) | 4 Ps (Picture-Promise-Prove-Push) |
| Most-aware | Direct offer + urgency, skip the framework entirely | Short-form 4 Ps, lead with the offer |

### Step 3: Adjust for Price Point
High-ticket offers ($2,000+) generally need longer, proof-heavy structures (PASTOR, StoryBrand, 4 Ps) regardless of stage, since the purchase decision needs more trust-building. Low-ticket/tripwire offers can use shorter structures (AIDA, PAS) even at earlier awareness stages, since the ask is small.

### Step 4: Hand Off with the Structure Named
Output isn't the copy itself — it's the framework choice and why, so whichever copy-writing skill runs next (`funnel-copy`, `landing-page-generator`, `email-sequence-generator`) writes to that structure instead of improvising.

### Step 5: Self-Validation
- [ ] Framework choice is justified by awareness stage, not picked arbitrarily
- [ ] Price point was factored in when it changes the recommendation
- [ ] The explanation is specific enough that another skill can follow it without re-deriving the logic
- [ ] If most-aware, correctly recommended skipping the framework rather than forcing one

## Output Schema
```
{
  recommended_framework: string
  why: string
  structure_outline: string[]   # the actual steps of the chosen framework, e.g. ["Problem", "Agitate", "Solve"]
  copy_type: string
}
```

## Output Format
```
## Framework Recommendation

**Use: [Framework Name]**

**Why:** [1-2 sentences tying the awareness stage and copy type to this choice]

**Structure to follow:**
1. [Step 1 of the framework]
2. [Step 2]
3. [Step 3]
...

Hand this to [funnel-copy / landing-page-generator / email-sequence-generator] to write the actual copy against this structure.
```

## Error Handling
- **Awareness stage unknown:** Run `schwartz-awareness-mapper` first rather than guessing — framework choice without it is a coin flip.
- **Copy type doesn't fit the table cleanly (e.g. a tweet):** Default to the short-copy column and note the framework may need further compression.
- **User insists on a framework that doesn't fit the stage:** Explain the mismatch plainly (e.g. "AIDA on a most-aware audience wastes their patience rebuilding attention they already have") but follow their explicit choice if they still want it after hearing why.

## Examples

**Example 1:**
User: "I'm writing a cold Facebook ad for people who've never heard of my product, what structure should I use?"
→ Stage: unaware. Copy type: ad (short).
→ Recommend AIDA — build attention from zero, this is exactly its job.

**Example 2:**
User: "This is a long sales page for people already comparing SaaS tools like mine"
→ Stage: product-aware. Copy type: long-form-sales-page.
→ Recommend 4 Ps — they already believe the category works, need proof this specific product wins.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- funnel-copy (S9-Funnels) — hands off the chosen structure for actual page copy
- landing-page-generator (S11-Asset-Generation) — same, for full page generation
- email-sequence-generator (S11-Asset-Generation) — same, for email sequences

### Fed By
- schwartz-awareness-mapper (S10-Copywriting) — supplies the awareness stage this entire choice depends on
- avatar-extraction (S10-Copywriting) — informs tone/voice within whichever framework is chosen

### Feedback Loop
- If A/B tests (`ab-test-generator`) consistently show one framework underperforming for a given awareness stage in this founder's market, that should override the default table for future recommendations in the same project.

```yaml
chain_metadata:
  skill_slug: "copy-framework-selector"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "landing-page-generator"
```
