---
name: create-skill
description: >
  Scaffolds a brand new SKILL.md file in the pack's exact format for a task the founder
  does repeatedly but isn't covered by any of the existing 52 skills, so the pack keeps
  growing in the same shape instead of drifting into inconsistent formats.
  Use this skill when the user asks "make a skill for this", "I keep doing this thing
  manually, turn it into a skill", "add a new skill to the pack", "we need a skill for X",
  "package this workflow as a skill", "clone the format for a new task", or "write a
  SKILL.md for [task]".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "meta", "skill-authoring", "scaffolding"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Meta
---

# Create Skill

Turns a repeated manual task into a properly formatted SKILL.md file that matches the rest of the pack exactly — same front-matter schema, same section structure, same quality bar. This is how the pack grows without every new skill looking like it was written by a different person with different habits.

## Stage
This skill belongs to Stage S8: Meta

## When to Use
- The founder has done the same multi-step task 3+ times manually (a sign it's worth codifying)
- A gap surfaces from `skill-finder` returning "no good match" repeatedly for the same kind of request
- `category-designer` approves a new stage or slots a new skill into an existing one and it now needs to be written
- `self-improver` recommends turning a lesson learned into a reusable skill
- The founder explicitly asks to package a workflow, prompt, or checklist into the pack's format

## Input Schema
```
new_skill_request:
  task_description: string        # what the task is, in plain language
  proposed_slug: string           # optional, kebab-case; generated if not given
  target_stage: string            # one of S1-S8, or "needs category-designer first"
  frequency: string                # how often this comes up (e.g. "every new project")
  example_past_instance: string   # optional, a real time this task was done manually
  trigger_phrases: [string]       # optional, phrases the founder has actually typed
```

## Workflow
### Step 1: Confirm It's Not Already Covered
Check the skill name against the master list of 52 existing slugs (see References). If something close already exists, recommend using or extending that skill instead of creating a near-duplicate. Stop here if a match is found.

### Step 2: Confirm the Stage
If `target_stage` isn't given or is ambiguous, apply the same stage test `category-designer` uses: does this fit one of the 8 existing stages cleanly? If not, hand off to `category-designer` first rather than force-fitting it.

### Step 3: Define the Slug and Description
- Slug: kebab-case, verb-or-noun style matching existing conventions (e.g. `pricing-model-calculator`, not `calculate_pricing`)
- Description: one sentence of what it does, then 5-8 realistic trigger phrases a non-technical founder would actually type — pull from real chat history when available, don't invent generic phrasing

### Step 4: Draft the Workflow
Break the task into 4-7 concrete steps as the founder (or a past transcript) actually performed it, not an idealized version. Each step needs to be an instruction the assistant can execute, not a vague goal. End with a Step N: Self-Validation checklist (5-6 concrete checks).

### Step 5: Define Input/Output Schemas and Format
Write the pseudo-schema input block, the pseudo-JSON output schema, and the actual markdown Output Format template the assistant will fill in and hand back to the founder.

### Step 6: Write Error Handling and Examples
4-6 realistic edge cases (missing input, ambiguous request, conflicting data) with how to handle each. Then 2-3 short worked examples in the "user message → what happens → outcome" format.

### Step 7: Map Flywheel Connections
Identify 2-4 "Feeds Into" skills and 1-2 "Fed By" skills using the master skill list, plus a one-sentence feedback loop description. A skill with zero flywheel connections is a sign it's either mis-scoped or redundant — revisit Step 1 if so.

### Step 8: Self-Validation
Before presenting, silently check:
- [ ] Does the front-matter match the exact schema (name, description, license, version, tags, compatibility, metadata)?
- [ ] Are there 5-8 realistic trigger phrases, not generic ones?
- [ ] Does the workflow have 4-7 steps ending in a self-validation checklist?
- [ ] Are Input Schema, Output Schema, and Output Format all present as fenced code blocks?
- [ ] Does Flywheel Connections list real slugs from the master list, not invented ones?
- [ ] Is the file written to the correct path: `skills/<stage-folder>/<slug>/SKILL.md`?

## Output Schema
```
{
  "slug": string,
  "stage": string,
  "file_path": string,
  "duplicate_check_result": "clear" | "overlaps_with:<existing_slug>",
  "skill_md_content": string   // the full rendered file
}
```

## Output Format
```markdown
# New Skill Created: `<slug>`

## Stage
<S#-Name>

## File Path
`skills/<stage-folder>/<slug>/SKILL.md`

## Summary
<1-2 sentences on what it does and why it was needed>

## Trigger Phrases Used
<list>

## Flywheel Position
- Feeds into: <slugs>
- Fed by: <slugs>

---
<full SKILL.md content, ready to write to disk>
```

## Error Handling
- Task is too narrow (a one-off, not repeated): don't create a skill — tell the founder to just do it directly this time, and suggest revisiting if it recurs.
- Task overlaps heavily with an existing skill: recommend extending the existing skill's workflow instead of creating a near-duplicate; name the specific existing slug.
- No clear stage fits: hand off to `category-designer` before proceeding rather than guessing a stage.
- Founder gives a vague task description ("something for marketing"): ask one clarifying question about the specific repeated action before drafting, don't scaffold a vague skill.
- Trigger phrases not supplied: infer 5-8 plausible ones from the task description, written in the same blunt, non-technical register the founder actually uses, not generic startup-speak.

## Examples
**Example 1**
User: "I keep manually writing the same 'what changed this week' update for myself every Friday. Can this be a skill?"
The skill checks the master list, finds no exact match, confirms S7-Growth or S8-Meta fit, and drafts `weekly-status-writer` with a 5-step workflow (pull recent git commits, pull recent decisions, draft summary, self-check for hero-copy tone per Sebastian's engineer-tone preference, output).
Outcome: new SKILL.md file ready to add to the pack.

**Example 2**
User: "Turn my compliance checklist habit into a skill" — but `compliance-checker` already exists.
The skill runs the duplicate check in Step 1, finds the overlap, and tells the founder to extend `compliance-checker` instead of creating a second one.
Outcome: no new file created; founder pointed to the existing skill.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `category-designer` (S8-Meta) — when a new skill doesn't fit any stage, this routes back to category design first
- `skill-finder` (S8-Meta) — every new skill created must be added to skill-finder's reference table so it's discoverable

### Fed By
- `self-improver` (S8-Meta) — retrospectives are the most common source of "this should be a skill" ideas
- `category-designer` (S8-Meta) — approved new stages/slots hand off directly into this skill for drafting

### Feedback Loop
Each newly created skill is a data point on where the pack had gaps — tracking how often `create-skill` fires for the same theme signals to `category-designer` when a cluster deserves its own stage.

```yaml
chain_metadata:
  skill_slug: "create-skill"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "skill-finder"
    - "self-improver"
```
