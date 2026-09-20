---
name: schwartz-awareness-mapper
description: >
  Applies Eugene Schwartz's five stages of market awareness (unaware,
  problem-aware, solution-aware, product-aware, most-aware) to determine what
  angle and message a specific SaaS audience segment actually needs, so copy
  doesn't sell to people who aren't ready for it yet.
  Use this skill when the user asks about matching messaging to audience
  readiness or choosing the right angle for cold vs warm traffic, or says
  "who am I actually writing this for", "cold traffic vs retargeting copy",
  "what awareness stage is my audience", "my ad copy isn't working for cold traffic",
  "message to market match", "why does this copy work for existing users but not new visitors".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "awareness", "positioning", "funnel-strategy"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Schwartz Awareness Mapper

This skill diagnoses how much a given audience segment already knows — about their problem, about solutions like this, about this specific product — and sets the messaging rules that follow from that. The single most common reason SaaS copy underperforms isn't bad writing, it's pitching a most-aware close ("Start your free trial") to an unaware audience who doesn't yet believe they have the problem.

## Stage
This skill belongs to Stage S10: Copywriting

## When to Use
- Writing copy for cold traffic (ads, SEO content, outbound) versus warm traffic (retargeting, existing trial users, newsletter subscribers)
- The same landing page is being used for very different traffic sources and converting inconsistently
- Choosing between an educational angle and a direct-offer angle for a given channel
- Feeding `headline-matrix` or `ad-angle-multiplier` so their outputs match where the audience actually is, not where the founder wishes they were
- The user asks why a hard-sell headline works in email but flops as a cold LinkedIn ad
- Building a multi-touch sequence where each touch needs to move the reader one stage forward, not repeat the same pitch

## Input Schema
```
audience_segment: string           # e.g. "cold LinkedIn traffic", "trial users day 3", "newsletter subscribers"
traffic_source: string?
primary_avatar: object?            # from avatar-extraction, if run
product_or_service: string
existing_copy_sample: string?      # copy currently used, if diagnosing underperformance
```

## Workflow
### Step 1: Diagnose the Stage
Assign the segment to exactly one of Schwartz's five stages by answering these in order:
1. **Unaware** — doesn't know they have the problem this solves
2. **Problem Aware** — knows the problem, doesn't know solutions exist
3. **Solution Aware** — knows solutions exist, doesn't know this product
4. **Product Aware** — knows this product, hasn't decided to buy
5. **Most Aware** — knows the product, just needs the offer/price/nudge

For SaaS specifically: cold outbound and cold ads are almost always problem-aware at best; retargeting and trial users are typically product-aware; existing free-tier users converting to paid are most-aware.

### Step 2: Set the Messaging Rules for That Stage
- **Unaware**: lead with the pain/symptom in the reader's own words, never mention the product category yet
- **Problem Aware**: name the problem directly, introduce the category of solution, build the case that a solution is needed
- **Solution Aware**: differentiate — why this approach/mechanism beats the alternatives they already know about
- **Product Aware**: proof, objection handling, specific outcomes — they know what it is, they need to trust it works for them
- **Most Aware**: state the offer plainly, remove friction, close — no re-explaining what the product does

### Step 3: State What Must NOT Be Said at This Stage
This is as important as what to say. Selling too early is the most common failure: a "Start Free Trial" CTA to an unaware audience gets ignored because they don't yet believe they need to act. Name explicitly what to avoid for the diagnosed stage.

### Step 4: Pick the Angle Direction
Choose the dominant approach for this stage: Education, Agitation, Comparison, or Offer — and hand this off as the required input for `headline-matrix` or `ad-angle-multiplier`.

### Step 5: Self-Validation
- [ ] Exactly one awareness stage is assigned, with the reasoning stated
- [ ] Messaging rules are specific to this stage, not generic advice
- [ ] "What to avoid" is explicit, not implied
- [ ] Angle direction (education/agitation/comparison/offer) is named
- [ ] If existing copy was diagnosed as underperforming, the mismatch between copy's assumed stage and audience's real stage is stated plainly

## Output Schema
```json
{
  "audience_segment": "string",
  "awareness_stage": "unaware|problem_aware|solution_aware|product_aware|most_aware",
  "stage_reasoning": "string",
  "messaging_rules": { "say": "string", "avoid": "string" },
  "angle_direction": "education|agitation|comparison|offer",
  "diagnosed_mismatch": "string|null"
}
```

## Output Format
```markdown
# Awareness Map: [audience segment]

## Stage: [name]
Reasoning: [why this segment is at this stage]

## Messaging Rules
- Say: [what this stage responds to]
- Avoid: [what kills response at this stage]

## Angle Direction
[Education / Agitation / Comparison / Offer]

## If Diagnosing Existing Copy
Current copy is written for [stage X] but this audience is at [stage Y].
Fix: [specific correction]
```

## Error Handling
- Audience mixes multiple stages (e.g. a newsletter with both new and long-time subscribers) → recommend segmenting the send rather than writing one message for a blended list, or default to the least-aware segment present since over-explaining to an aware reader costs less than under-explaining to an unaware one
- No traffic source or segment given → ask which channel this copy is for; stage assignment is meaningless without knowing where the reader is coming from
- User insists on a hard offer pitch to a cold/unaware audience → state plainly this will underperform and explain why, but provide the copy if they still want it, clearly labeled as high-risk
- Existing copy sample not provided when diagnosing underperformance → ask for it; can't diagnose a mismatch without seeing what was actually said

## Examples
**Example 1**
User: "Our cold LinkedIn ads say 'Start your free trial' and nobody clicks."
Skill: Diagnoses cold LinkedIn traffic as problem-aware at best, flags the mismatch (most-aware offer copy on a problem-aware audience), and rewrites the ad to lead with the pain in the reader's language, saving the trial CTA for retargeting instead.

**Example 2**
User: "What's different about copy for day-3 trial users versus our homepage?"
Skill: Maps homepage visitors as solution- or problem-aware (differentiation and category education) versus day-3 trial users as product-aware (proof and objection handling, since they already know what the product is and are deciding whether it works for them).

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- headline-matrix (S10-Copywriting)
- ad-angle-multiplier (S10-Copywriting)
- full-funnel-campaign-orchestrator (S10-Copywriting)

### Fed By
- avatar-extraction (S10-Copywriting)

### Feedback Loop
Reply and click-through data from live campaigns should confirm the assigned awareness stage — if a "problem-aware" angle underperforms an "unaware" one on the same segment, re-run this skill with the actual response data as new evidence.

```yaml
chain_metadata:
  skill_slug: "schwartz-awareness-mapper"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "headline-matrix"
    - "ad-angle-multiplier"
```
