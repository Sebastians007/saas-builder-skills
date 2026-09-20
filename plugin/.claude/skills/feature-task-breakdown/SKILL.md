---
name: feature-task-breakdown
description: >
  Break one feature or user story from a PRD into an ordered checklist of small,
  independently verifiable implementation tasks.
  Use this skill when the user asks about turning a PRD item into a build plan,
  splitting a feature into steps, or says
  "break this feature down into tasks", "how do I build this without breaking everything",
  "turn this user story into a checklist", "what order should I build this in",
  "give me small steps for this feature", "help me scope this build session",
  "I don't know where to start on this feature".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "planning", "scoping", "checklist"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# Feature Task Breakdown

Turns one PRD feature or user story into an ordered list of small, testable implementation tasks, each scoped so a single AI coding session can finish it and prove it works before the next one starts. Prevents the most common failure mode in AI-assisted building: asking the agent for "the whole feature" and getting a half-working pile of code that's hard to debug.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- The user has a PRD or user story and wants to start coding it
- The user asks "where do I even start" on a feature
- A previous build attempt on this feature produced broken or tangled code
- The user is about to hand a feature to an AI coding agent and wants a scoped prompt sequence instead of one giant prompt
- The user wants to know what order to build things in (data before UI, etc.)
- The user is resuming a half-built feature and needs to know what's left

## Input Schema
```
feature_description: string       # plain language, or pasted PRD/user story section
existing_codebase_notes: string?  # stack, framework, what already exists (optional)
constraints: string?              # deadline, must-not-touch areas, deploy target
done_definition: string?          # what "this feature works" means to the user
```

## Workflow
### Step 1: Confirm the boundary of "one feature"
Read the input. If it actually bundles two or more features (e.g. "add teams AND billing"), stop and split it — call this out to the user before proceeding. One breakdown = one feature.

### Step 2: Identify the build layers
Sort the work into the natural dependency order for a typical SaaS stack:
1. Data layer (schema/table/migration)
2. Backend logic (API endpoint, server function)
3. Frontend state/wiring (fetch, form, hook)
4. UI (component, layout)
5. Edge cases and validation
6. Polish (loading/empty/error states)

Not every feature needs all six. Skip layers that don't apply and say so.

### Step 3: Write tasks, not epics
For each layer, write 1-3 tasks. Each task must be:
- Completable in one focused AI coding session (roughly under ~200 lines of diff)
- Independently verifiable (there's a concrete way to check it worked before moving on)
- Stated as an action, not a goal ("Add `status` column to `orders` table with migration" not "handle order statuses")

### Step 4: Attach a verification step to every task
Every task gets a one-line check: what to run, click, or query to prove it worked. If there's no way to verify a task in isolation, the task is still too big — split it further.

### Step 5: Order for safety
Sequence tasks so nothing is built on top of an unverified layer. Flag any task that touches shared/critical code (auth, billing, existing tables) with a "go slow" note.

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] Every task is independently verifiable
- [ ] No task requires more than one layer's worth of new logic
- [ ] Tasks are ordered so each one only depends on previously completed tasks
- [ ] Nothing here secretly bundles a second feature
- [ ] Risky tasks (touching auth, billing, shared tables) are flagged

## Output Schema
```json
{
  "feature": "string",
  "assumptions": ["string"],
  "tasks": [
    {
      "id": "T1",
      "layer": "data | backend | frontend | ui | edge-case | polish",
      "title": "string",
      "instructions": "string",
      "verify": "string",
      "risk_flag": "string | null"
    }
  ],
  "done_definition": "string"
}
```

## Output Format
```markdown
# Task Breakdown: <Feature Name>

**Done means:** <one sentence definition of done>

## Assumptions
- <assumption 1>
- <assumption 2>

## Build Order

### T1 — <task title> (data)
- Do: <specific instruction>
- Verify: <how to check it worked>
- Risk: <none, or what to be careful of>

### T2 — <task title> (backend)
...

## Notes for the build session
- Build and verify one task at a time. Don't start T2 until T1 is verified.
- <any other guidance>
```

## Error Handling
- If the feature description is too vague to break down (e.g. "make it better"), ask one clarifying question before proceeding — don't guess at scope.
- If the input bundles multiple features, split them and only break down the first one, flagging the others as separate breakdowns needed.
- If no PRD/spec exists yet, tell the user to run `prd-writer` or `user-story-writer` first — this skill assumes a spec, it doesn't create one.
- If the codebase context is missing, proceed with reasonable framework-agnostic assumptions and label them clearly as assumptions.
- If a task can't be made independently verifiable, split it further rather than shipping an unverifiable task.

## Examples

**Example 1**
User: "Break down 'users can export their data as CSV' into build steps."
Skill does: identifies layers (backend export endpoint, frontend trigger button, download handling, empty-data edge case), writes 4 small tasks each with a verify step (e.g. "curl the endpoint with a test user, confirm CSV headers match schema").
Outcome: user hands each task to Claude Code one at a time, verifying after each.

**Example 2**
User: "Here's my PRD section on team invites, plus billing changes — help me start building."
Skill does: flags that this is two features (invites + billing), breaks down team invites only, tells user to request a separate breakdown for billing.
Outcome: avoids a tangled cross-feature build session.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- data-model-diagrammer (S6-Building)
- api-endpoint-builder (S6-Building)
- ui-component-builder (S6-Building)
- test-case-generator (S7-Testing)

### Fed By
- user-story-writer (S5-Planning)
- mvp-feature-slicer (S5-Planning)

### Feedback Loop
When a task turns out too big or fails verification during building, note it back into this skill's future breakdowns so task sizing gets tighter over time.

```yaml
chain_metadata:
  skill_slug: "feature-task-breakdown"
  stage: "building"
  timestamp: string
  suggested_next:
    - "data-model-diagrammer"
    - "api-endpoint-builder"
    - "ui-component-builder"
```
