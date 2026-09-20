---
name: underserved-market-finder
description: >
  Finds niches within a broad market space that are underserved by existing
  SaaS tools, surfacing where demand outpaces the current options.
  Use this skill when the user asks about "what niche should I go after", "underserved markets",
  or says
  "what's a good niche in [space]", "is there a gap in the market for [category]",
  "who's underserved right now", "find me a niche nobody's building for",
  "what broad space should I narrow into", "where's the whitespace in [industry]".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "market-research", "niche-finding"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Underserved Market Finder

This skill takes a broad market space (e.g. "scheduling software," "compliance tools") and surfaces specific sub-niches within it where demand signals exist but current tools are generic, expensive, or absent. It exists because "the market is too crowded" is usually true only at the broad category level — niches inside it are often wide open.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has a broad space in mind but no specific angle yet
- Founder was told a market is "too saturated" and wants to check if that's true at every level or just the top
- Founder has domain expertise in an industry and wants to find where that expertise is a wedge
- Before running `saas-idea-validator`, to generate a specific idea worth validating
- Founder's current idea got a weak competitor-teardown result (too crowded, no whitespace) and needs a pivot direction

## Input Schema
```
broad_space: string (required) — e.g. "project management", "HR software", "invoicing"
founder_domain_expertise: string (optional) — industries/roles the founder has real experience in (huge advantage if present)
constraints: string[] (optional) — e.g. "must be B2B", "must not require enterprise sales"
```

## Workflow
### Step 1: Map the broad category's existing players
Use web_search to identify the dominant, well-funded tools in `broad_space` (the ones that come up first, that everyone's heard of). These define what's "generic" — built to serve the widest possible audience, which is exactly why niches get underserved: broad tools can't specialize without alienating their core base.

### Step 2: Segment by vertical, role, or workflow quirk
Break the broad space into 8-12 candidate sub-niches along three axes: **vertical industry** (e.g. scheduling for gyms vs. scheduling for tattoo studios vs. scheduling for tutors), **role/company size** (e.g. solo freelancer vs. 50-person agency), and **workflow quirk** (a specific compliance requirement, a specific data format, a specific integration need that generic tools ignore). Domain expertise from `founder_domain_expertise` should heavily weight which segments get explored deepest — a founder's own industry knowledge is a real, defensible signal.

### Step 3: Check demand signals per candidate niche
For each promising segment, use web_search to look for demand evidence: Reddit/forum threads complaining about the generic tool not fitting their vertical, "alternative to X for Y" search patterns, review complaints on G2/Capterra mentioning a specific unmet need, or job posts/spreadsheet templates showing people manually solving the problem (a strong signal — manual workarounds mean demand exists but no tool serves it well).

### Step 4: Check that the niche is servable, not just underserved
A niche can be underserved because it's genuinely too small, too poor, or too resistant to paying for software — that's not opportunity, that's a trap. Sanity-check each candidate: is there a plausible number of businesses/people in this niche (use web_search for rough industry size), and do they currently pay for other software (a proxy for willingness to pay)?

### Step 5: Rank and present top 3-5 niches
Score each surviving candidate on: demand evidence strength, competitive gap size (how bad are the current options), servability (can it be reached and will it pay), and fit with founder's expertise/constraints. Present the top 3-5, not just one — let the founder pick, since fit with their own interest/expertise matters more than any single score.

### Step 6: Self-Validation
- [ ] At least 8 candidate niches were actually considered before narrowing, not just the first idea
- [ ] Each surfaced niche has a real demand signal cited (forum complaint, workaround, search pattern), not just "seems underserved"
- [ ] Servability was checked, not assumed — small/no-budget niches were filtered out or flagged
- [ ] Founder's domain expertise was weighted if provided
- [ ] Top niches are presented with enough specificity to hand directly to `saas-idea-validator`

## Output Schema
```
{
  broad_space: string,
  candidates_considered: number,
  top_niches: [{
    niche: string,
    demand_signal: string,
    demand_source: string,
    current_options: string,
    gap: string,
    servability_note: string,
    fit_with_founder: string
  }]
}
```

## Output Format
```markdown
# Underserved Niches in: <broad space>

Considered N sub-niches across vertical, role, and workflow axes. Top candidates:

## 1. <Niche name>
- **Gap**: <what's missing or badly served>
- **Demand signal**: <specific evidence, with source>
- **Current options**: <what they use now, and why it's a bad fit>
- **Servable?**: <size/budget reality check>
- **Fit**: <why this matches founder's expertise/constraints, if applicable>

(repeat for each of top 3-5)

## Recommendation
<which niche looks strongest and why, in plain language>

## Next Step
Run `saas-idea-validator` on the top niche to score it before building, or `competitor-teardown` to confirm the gap in detail.
```

## Error Handling
- If `broad_space` is already extremely narrow (e.g. "scheduling software for dog groomers in Ohio"), skip re-segmenting and instead validate that exact niche directly via `saas-idea-validator` — this skill is for narrowing, not for further-narrowing an already-narrow idea.
- If web_search turns up no demand evidence for any candidate, say so honestly rather than inventing plausible-sounding gaps — recommend direct outreach/interviews as the next step instead.
- If every niche in the space turns out too small to be servable, report that and suggest either a wider founder search or a completely different broad space.
- If `founder_domain_expertise` conflicts with the strongest-scoring niche (founder has no experience there), present both: the objectively strongest niche and the best-fit-to-expertise niche, and let the user choose.

## Examples
**Example 1**
User: "Everyone says CRM software is too crowded. Is there really no room?"
→ Skill segments CRM by vertical (real estate, wedding photographers, independent insurance agents, private tutors) and role (solo vs. team), finds specific verticals still running CRM out of spreadsheets with active forum complaints, presents 4 candidate niches with demand evidence.

**Example 2**
User: "I used to manage compliance at a dental practice. Is there a SaaS gap in dental?"
→ Skill weights dental-adjacent niches heavily given founder expertise, checks demand signals specific to dental compliance/scheduling/billing pain points, surfaces top 3 with evidence.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `saas-idea-validator` (S1-Research) — hands off the top niche for a full go/no-go score
- `competitor-teardown` (S1-Research) — confirms the specific gap with a detailed competitor breakdown
- `tech-stack-finder` (S1-Research) — once a niche is chosen, stack selection can begin

### Fed By
- None — this is typically a starting point

### Feedback Loop
If `saas-idea-validator` later scores the recommended niche poorly on feasibility or demand, that result should be used to recheck the "servability" judgment made here and adjust future niche scoring criteria.

```yaml
chain_metadata:
  skill_slug: "underserved-market-finder"
  stage: "research"
  timestamp: string
  suggested_next:
    - "saas-idea-validator"
    - "competitor-teardown"
```
