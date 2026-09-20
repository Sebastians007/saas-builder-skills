---
name: prd-writer
description: >
  Turns a vague app idea into a real Product Requirements Doc that locks down the problem,
  the one target user, the core user flows, and a hard line between must-have and
  nice-to-have features before any code gets written.
  Use this skill when the user asks about "what should I build first", "help me write a PRD",
  or says
  "I have an idea for an app, can you help me plan it", "write me a PRD for this",
  "I keep telling Claude to build this and it's a mess", "what should this app actually do",
  "help me scope this feature before I build it", "I don't know what's in v1 vs later",
  "turn this idea into a spec", "my app idea is [X], where do I start".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "prd", "product-spec", "requirements"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Planning
---

# PRD Writer

Produces a short, concrete Product Requirements Document (PRD) that says exactly what the app is, who it's for, what it does, and what it deliberately does NOT do yet. This is the anchor document of the whole build — every other planning and building skill in this pack reads from it or writes back into it. Without this document, "just build the app" prompts drift into rework because nobody, including the AI, agreed on what "done" means.

## Stage
This skill belongs to Stage S5: Planning

## When to Use
- The user has an app idea but has never written it down in one place
- The user has been iterating with an AI coding tool for weeks/months without a spec and results are inconsistent or broken
- A new feature is big enough that it needs its own mini-PRD before building
- The user says "just build X" and X is vague enough that five different builds are possible
- Before kicking off `architecture-decision-writer`, `mvp-feature-slicer`, or `feature-task-breakdown`
- Revisiting an existing product to document what it actually is now (reverse-engineered PRD)

## Input Schema
```
idea: string                      # free-text description of the app, however rough
existing_prd_path?: string        # path to an existing PRD to revise instead of starting fresh
target_user_hint?: string         # optional steer if the user already knows their audience
constraints?: string[]            # known hard constraints (budget, timeline, must use X stack)
```

## Workflow
### Step 1: Extract the raw idea
Ask the user to describe the idea in their own words if not already given. Do not let vague input pass silently — if the description is one sentence like "an app for freelancers to track invoices," treat that as a starting point, not a finished input.

### Step 2: Force one target user
Ask (or infer and confirm): "If this app could only make ONE type of person happy, who is it?" Reject answers like "small businesses" or "freelancers" as too broad — push for a specific role, situation, or workflow (e.g., "a solo graphic designer billing 3-8 clients a month who currently uses spreadsheets"). Write this as a single sentence. A PRD with two target users is a PRD for two products — flag this if it happens and ask which one comes first.

### Step 3: Nail the one problem and the one outcome
State the problem in the user's own pain language, not feature language ("I lose track of which invoices are overdue and it costs me money" not "needs invoice tracking"). State the outcome as a before/after: what changes in the target user's life if this works. If the user gives multiple problems, ask which one is the reason they'd pay or come back — that's the one that goes in the PRD; the rest go in Out of Scope or a "later" list.

### Step 4: Map the core user flows
List the 3-5 flows a user takes to get the outcome (e.g., "create invoice → send invoice → get paid → see overdue status"). For each flow, write it as a numbered sequence of concrete steps, not a feature name. This becomes the backbone that `user-story-writer` later expands.

### Step 5: Sort features into Must-Have vs Nice-to-Have vs Out of Scope
For every feature mentioned anywhere in the conversation (including ones the user throws in offhand), ask: "does the core user flow work without this?" If yes, it's Nice-to-Have or Out of Scope. If the app is unusable or pointless without it, it's Must-Have. Be ruthless — most first-time PRDs have 3x too many must-haves. Cap Must-Have at what's needed for ONE core flow to work end to end.

### Step 6: Write Out of Scope explicitly
List things the app will NOT do, especially ones that are tempting or that competitors do. This prevents scope creep later and gives future-you (or the AI) a citable reason to say no. Include things like "no team/multi-user accounts in v1," "no mobile app," "no payment processing," if true.

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Target user is one specific person/role, not a segment
- [ ] Problem statement uses pain language, not solution language
- [ ] Every Must-Have feature is required for at least one core user flow to complete
- [ ] Must-Have list has 8 or fewer items (if more, push items to Nice-to-Have)
- [ ] Out of Scope section has at least 3 concrete exclusions
- [ ] No feature appears in both Must-Have and Out of Scope

## Output Schema
```
{
  "product_name": string,
  "one_liner": string,
  "target_user": string,
  "problem": string,
  "outcome": string,
  "core_user_flows": [ { "name": string, "steps": string[] } ],
  "must_have_features": string[],
  "nice_to_have_features": string[],
  "out_of_scope": string[],
  "open_questions": string[]
}
```

## Output Format
```markdown
# PRD: <Product Name>

**One-liner:** <what it is in one sentence>

## Target User
<one specific person/role — not a segment>

## Problem
<pain language, in the user's own words where possible>

## Outcome
<before → after: what changes if this works>

## Core User Flows
### 1. <Flow name>
1. <step>
2. <step>

### 2. <Flow name>
...

## Must-Have Features (v1)
- [ ] <feature> — required for: <which flow>
- [ ] ...

## Nice-to-Have (later)
- <feature>

## Out of Scope (v1)
- <explicitly excluded thing> — why: <reason>

## Open Questions
- <anything still unresolved that needs a decision before building>
```

## Error Handling
- If the user gives two unrelated ideas at once, stop and ask which one to PRD first — do not merge them.
- If the target user can't be narrowed after one round of pushback, propose a specific persona based on best guess and flag it as an assumption to confirm, rather than blocking indefinitely.
- If the user insists on a huge Must-Have list, write it, but flag clearly which items look non-essential and recommend running `mvp-feature-slicer` next.
- If revising an existing PRD, read `existing_prd_path` first and produce a diff-style summary of what changed, not just a fresh document.
- If constraints conflict with the stated outcome (e.g., "must be free to run" plus a feature that requires paid infra), surface the conflict rather than silently picking one side.

## Examples
**Example 1:** User says "I want to build something like Notion but for contractors." The skill pushes past "contractors" (too broad) to "a solo general contractor managing 2-4 active job sites who currently texts photos and notes to themselves," extracts the core flow (log a job site update → attach photos → client sees status), and produces a PRD with 5 must-have features and an explicit Out of Scope excluding invoicing, scheduling, and multi-user teams for v1.

**Example 2:** User pastes a huge list of 40 features for a CRM idea with no target user defined. The skill asks who the ONE buyer is, gets "solo real estate agents," then sorts the 40 features — most land in Nice-to-Have or Out of Scope, leaving 6 Must-Haves that support one flow: add a lead → log a touch → see who's due for follow-up.

**Example 3:** User has an existing 6-month-old app with no PRD and says "things keep breaking, help me get organized." The skill asks the user to describe what the app currently does, reverse-engineers a PRD from that description, and flags the parts that are unclear or contradictory as Open Questions.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `mvp-feature-slicer` (S5-Planning) — trims the Must-Have list down further if it's still too big
- `user-story-writer` (S5-Planning) — expands each core user flow into buildable stories
- `architecture-decision-writer` (S5-Planning) — technical approach must satisfy the PRD's must-haves
- `feature-roadmap-architect` (S5-Planning) — sequences must-have + nice-to-have into phases

### Fed By
- `saas-idea-validator` (S1-Research) — confirms the idea is worth writing a PRD for
- `underserved-market-finder` (S1-Research) — surfaces the target user and problem before the PRD locks them in

### Feedback Loop
When later stages (user testing, `signup-conversion-tracker`, `app-performance-report`) reveal the target user or problem statement was wrong, the PRD should be revised first — not the code — so every downstream skill re-derives from a corrected source of truth.

```yaml
chain_metadata:
  skill_slug: "prd-writer"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "mvp-feature-slicer"
    - "architecture-decision-writer"
    - "user-story-writer"
```
