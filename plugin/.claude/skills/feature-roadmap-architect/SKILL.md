---
name: feature-roadmap-architect
description: >
  Sequences a feature list into phases and milestones based on real dependency order and
  user value, instead of "build everything at once," so a founder always knows what to
  build next and why.
  Use this skill when the user asks about "what should I build first vs later", "help me
  sequence this roadmap", or says
  "I have all these features, what order do I build them in", "what's phase 1 vs phase 2",
  "help me plan my next 3 months of building", "what depends on what here", "I'm building
  everything at once and it's chaos", "turn this feature list into a roadmap".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "roadmap", "sequencing", "milestones"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S2-Planning
---

# Feature Roadmap Architect

Takes a feature list (must-haves, nice-to-haves, and known tech debt) and sequences it into ordered phases based on actual dependency order and user value delivered — not a random or "everything in parallel" order that's how most non-technical founders end up mid-build with three half-finished features and nothing shippable. Each phase in the output should be independently shippable and independently valuable.

## Stage
This skill belongs to Stage S2: Planning

## When to Use
- A PRD or feature list exists and it's time to decide build order
- The user has been building multiple features simultaneously with an AI tool and nothing is finished
- `mvp-feature-slicer` has defined the MVP and the remaining features need a post-launch sequence
- `tech-debt-detector` found high-severity debt that needs to be slotted into the plan, not just noted
- The user asks "what's next" after shipping a phase
- Planning a multi-month build and needing checkpoints, not just a task list

## Input Schema
```
prd_path?: string
feature_list?: string[]           # if not pulling from a PRD directly
known_dependencies?: string[]     # explicit "X needs Y first" if the user already knows some
tech_debt_items?: string[]        # from tech-debt-detector, if run
timeframe?: string                # e.g. "next 8 weeks", optional
```

## Workflow
### Step 1: Collect every feature into one list
Pull from the PRD's must-have and nice-to-have lists, plus any tech debt items flagged as needing a fix. Nothing gets sequenced if it isn't in this list first — this avoids features getting built ad hoc outside the plan.

### Step 2: Map real dependencies
For each feature, ask: what does this actually require to exist first (not "it would be nice to have X," but "this cannot function without X")? Common dependency types: data model dependencies (can't build "invite teammates" before "user accounts" exist), workflow dependencies (can't build "mark invoice overdue" before "invoice due dates" exist), and infra dependencies (can't build "email notifications" before an email-sending capability exists). Draw this as a simple list of "X requires Y" pairs, not a complex graph — keep it legible.

### Step 3: Score value independent of dependency order
For each feature, rate how much it moves the user toward the PRD's core outcome: High (directly delivers the core promised outcome), Medium (meaningfully improves it), Low (polish or edge-case coverage). A feature can be a hard dependency but still low standalone value (e.g., auth) — that's fine, it just means it's early but not a "phase win" on its own.

### Step 4: Build phases that are each independently shippable
Group features into phases where: (a) all of a phase's dependencies are satisfied by earlier phases, and (b) the phase as a whole delivers a real, demoable chunk of value — not just "the backend for something invisible." Phase 1 should always be the smallest set that gets one full core user flow working end to end (this should mirror what `mvp-feature-slicer` produces if that skill ran first). Later phases add breadth or depth.

### Step 5: Slot in tech debt at the right point, not first or last by default
Tech debt tagged "fix before next touch" from `tech-debt-detector` goes into the phase right before the feature that would touch it. Debt tagged "fix now" goes into Phase 1 regardless of feature value. Don't create a separate giant "cleanup phase" that never gets prioritized against real features.

### Step 6: Name each phase by the value it delivers, not by feature count
Phase names should describe what becomes true for the user after that phase ships (e.g., "Phase 1: a solo user can create and send one invoice end to end" not "Phase 1: core features").

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Every feature from the input list appears in exactly one phase
- [ ] No phase includes a feature whose dependency lands in a later phase
- [ ] Phase 1 delivers one complete, demoable core user flow
- [ ] Each phase name describes user-facing value, not internal feature labels
- [ ] High-severity tech debt is placed no later than the phase where it would first cause a problem

## Output Schema
```
{
  "phases": [
    {
      "phase_number": integer,
      "name": string,
      "delivers": string,
      "features": string[],
      "dependencies_satisfied": string[],
      "tech_debt_addressed": string[]
    }
  ],
  "dependency_map": [ { "feature": string, "requires": string[] } ]
}
```

## Output Format
```markdown
# Feature Roadmap: <product name>

## Dependency Map
- <feature> requires: <feature(s)>
- <feature> requires: nothing (can start immediately)

## Phase 1: <what becomes true for the user>
**Features:** <list>
**Tech debt addressed:** <list, if any>
**Why this order:** <one line tying to dependencies/value>

## Phase 2: <what becomes true for the user>
...

## Phase 3: <what becomes true for the user>
...
```

## Error Handling
- If the feature list has a circular dependency (A needs B, B needs A), surface it directly — this usually means one of the two is mis-scoped and needs splitting.
- If no PRD exists, ask for at least a rough feature list and target user before sequencing — value scoring is meaningless without knowing what outcome matters.
- If the user demands everything in Phase 1, push back with the specific dependency and value reasoning for why that's not shippable as one phase, and propose the honest minimum instead.
- If `mvp-feature-slicer` hasn't been run and Phase 1 still looks too large, recommend running it before finalizing the roadmap.
- If tech debt items are given without severity, ask or infer conservatively (treat unspecified debt as medium, not automatically high or low).

## Examples
**Example 1:** User has a PRD for an invoicing app with 6 must-haves and 5 nice-to-haves. The skill maps "send invoice" as requiring "create invoice," and "mark overdue" as requiring "due dates on invoices," builds Phase 1 as create+send+view (one full flow), Phase 2 as overdue tracking + reminders, Phase 3 as nice-to-haves like recurring invoices.

**Example 2:** User ran `tech-debt-detector` and got a "fix now" finding about hardcoded single-user data model, plus wants to add a team feature next. The skill puts the data model fix at the start of Phase 1 (blocking the team feature), before any new team-facing work.

**Example 3:** User says "I want to build the AI feature, the payments feature, and the dashboard all at once this month." The skill maps dependencies, shows payments and dashboard both depend on core data existing first, and proposes a realistic single-phase-at-a-time order instead, explaining why parallel building on a small team causes nothing to finish.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-task-breakdown` (S3-Building) — each phase's features become concrete tasks in order
- `ci-cd-pipeline-builder` (S5-Deployment) — phase boundaries often map to release/deploy checkpoints

### Fed By
- `prd-writer` (S2-Planning) — supplies the feature list and target outcome
- `mvp-feature-slicer` (S2-Planning) — defines what Phase 1 must contain
- `tech-debt-detector` (S2-Planning) — supplies debt items that must be slotted into the sequence

### Feedback Loop
When a phase ships and `app-performance-report` or `signup-conversion-tracker` shows the assumed value didn't materialize, re-score the remaining phases' value ratings before continuing — don't keep building the original sequence on outdated assumptions.

```yaml
chain_metadata:
  skill_slug: "feature-roadmap-architect"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-task-breakdown"
    - "ci-cd-pipeline-builder"
```
