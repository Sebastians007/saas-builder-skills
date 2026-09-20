---
name: category-designer
description: >
  Designs a new skill category (stage) for the pack when an existing task doesn't fit
  anywhere in the current 8 stages, defining its purpose, boundaries, and how it wires
  into the existing flywheel without causing overlap or sprawl.
  Use this skill when the user asks about "where does this skill belong", "we keep adding
  skills that don't fit S1-S8", "do we need a new stage", "add a category for X", "our pack
  is getting messy", "should this be its own stage or fit in S6", "reorganize the skill
  pack", or "we have 5 new skill ideas and no home for them".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "meta", "taxonomy", "skill-pack-architecture"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Meta
---

# Category Designer

Decides whether a cluster of new skill ideas needs a brand new stage or actually belongs inside an existing one, and if a new stage is warranted, defines its scope, naming, and its connections to the rest of the flywheel. This exists to stop the pack from turning into 80 loosely related files with no shared logic — every stage should represent one coherent phase of building or running a SaaS product.

## Stage
This skill belongs to Stage S8: Meta

## When to Use
- A founder has 3+ new skill ideas that don't cleanly fit any of the 8 existing stages (Research, Planning, Building, Testing, Deployment, Operations, Growth, Meta)
- The pack is growing skill-by-skill with no plan and starting to feel redundant or scattered
- Someone proposes a skill that could arguably live in two different stages and the ambiguity needs resolving
- A recurring class of work (e.g. "customer support", "fundraising", "hiring") keeps coming up and has no home
- Before adding a 9th stage, to confirm it's really needed and not just a mis-slotted skill or two
- After `self-improver` flags a repeated gap that existing skills don't cover

## Input Schema
```
new_stage_request:
  trigger: string              # what prompted this (e.g. "keep needing fundraising help")
  candidate_skills: [string]   # rough skill ideas that might need a new home, 1-10
  existing_stages_considered: [string]  # optional, stages already ruled out and why
  pack_size_context: int       # optional, current total skill count (default 52)
```

## Workflow
### Step 1: Restate the Gap
Summarize in plain language what kind of work isn't covered. Name the pattern, not just the individual skill ideas — e.g. "post-launch customer support triage" not "we need a skill for angry emails."

### Step 2: Test Against Existing Stages First
Before inventing anything, check every candidate skill against the current 8 stages (S1-Research through S8-Meta). A skill is often just mis-slotted, not a sign of a missing stage. Reject a new stage if 1-2 skills can absorb into an existing stage without stretching its definition.

### Step 3: Apply the Coherence Test
A new stage is justified only if ALL of the following are true:
- At least 4-6 distinct, non-overlapping skills would live there
- Those skills share a genuine phase of the SaaS lifecycle (not just a vague theme)
- No existing stage's definition can be reasonably widened to include them
- The new stage has a clear "enters from" and "exits to" in the flywheel (nothing is an island)

If any of these fail, recommend folding the skills into an existing stage instead and stop here.

### Step 4: Define the New Stage
If justified, write:
- Stage code and name (e.g. "S9-Support")
- One-sentence purpose
- 4-8 skill slugs that would live there, each with a one-line job
- Explicit boundary: what this stage does NOT do (to prevent future overlap)

### Step 5: Map Flywheel Connections
For the new stage as a whole, and for its 2-3 most central skills, specify which existing stages feed it and which it feeds. A stage with no upstream or downstream connection is a red flag — go back to Step 3.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Did I try to avoid creating a new stage first?
- [ ] Does every proposed skill in the new stage have a clear, distinct job (no near-duplicates)?
- [ ] Is the stage named with the same "S#-Name" convention as the existing 8?
- [ ] Does the recommendation include explicit upstream/downstream flywheel links?
- [ ] Would a non-technical founder understand why this is or isn't its own stage?

## Output Schema
```
{
  "verdict": "new_stage" | "fold_into_existing",
  "target_stage": string,            // existing stage name if folding in
  "new_stage": {
    "code": string,
    "name": string,
    "purpose": string,
    "skills": [{"slug": string, "job": string}],
    "boundary": string
  } | null,
  "flywheel_links": {"feeds_into": [string], "fed_by": [string]},
  "rationale": string
}
```

## Output Format
```markdown
# Category Design Review

## The Gap
<plain-language description of the uncovered work>

## Verdict: [New Stage / Fold Into Existing Stage X]

### If folding in:
- Target stage: <name>
- Why it fits: <1-2 sentences>
- Skills to add there: <list>

### If new stage:
- Stage: S#-<Name>
- Purpose: <one sentence>
- Boundary (what it is NOT): <one sentence>
- Skills in this stage:
  1. `<slug>` — <job>
  2. `<slug>` — <job>
  ...

## Flywheel Connections
- Feeds into: <stages/skills>
- Fed by: <stages/skills>

## Next Step
<what to do now — e.g. run create-skill for each new skill listed>
```

## Error Handling
- Fewer than 4 candidate skills offered: don't invent a stage — recommend folding into the closest existing stage and explain why.
- Candidate skills span two unrelated themes: split the request, evaluate each theme separately, don't force one stage to cover both.
- User insists on a new stage despite failing the coherence test: state the test result plainly, then comply if they still want it, but flag the sprawl risk explicitly in the output.
- No existing stage list provided: default to the 8 known stages (S1-Research through S8-Meta) listed in this pack.
- Overlapping skill ideas within the candidate list itself: flag the duplication before deciding on stage placement — don't let redundant skills get created just because they got a stage.

## Examples
**Example 1**
User: "I keep needing help with customer support tickets, refund handling, and churn save calls. Is that its own category?"
The skill tests these against S6-Operations and S7-Growth, finds they share a genuine "post-signup customer response" phase not covered elsewhere, and 6 distinct skill ideas exist. Verdict: new stage `S9-Support`, with skills like `ticket-triage`, `refund-decision-helper`, `churn-save-scripter`.
Outcome: founder gets a scoped new stage definition plus a note to run `create-skill` for each one.

**Example 2**
User: "We need a skill for writing investor updates. New category?"
Only one skill idea, no cluster. The skill folds it into S7-Growth (adjacent to reporting-style skills) or S8-Meta if it's about internal reporting, and explains why a whole new stage isn't warranted for a single skill.
Outcome: no new stage created; `investor-update-writer` recommended as an addition to S7-Growth instead.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `create-skill` (S8-Meta) — once a stage or skill gap is confirmed, this hands off the actual scaffolding
- `self-improver` (S8-Meta) — stage additions get logged as pack-evolution history

### Fed By
- `self-improver` (S8-Meta) — retrospectives often surface the repeated gaps that trigger a category redesign
- `skill-finder` (S8-Meta) — repeated "no good match" results from skill-finder are a signal a category is missing

### Feedback Loop
Every stage decision (new or folded-in) gets logged so future category requests can be checked against precedent instead of re-litigating the same boundary questions.

```yaml
chain_metadata:
  skill_slug: "category-designer"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "create-skill"
    - "self-improver"
```
