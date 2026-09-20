---
name: architecture-decision-writer
description: >
  Compares 2-3 real technical approaches for a feature or the whole app with concrete
  tradeoffs and a clear recommendation, written as a lightweight Architecture Decision
  Record (ADR), so a non-technical founder doesn't end up locked into a stack by accident.
  Use this skill when the user asks about "which stack should I use", "should I use
  Supabase or Firebase", or says
  "should I use Cloudflare or Vercel for this", "what database should this app use",
  "do I need a separate backend or can I do this serverless", "help me decide between X and Y",
  "why did the AI pick this framework", "what's the tradeoff here", "I don't want to get
  locked into something I can't undo".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "architecture", "adr", "tech-stack"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Planning
---

# Architecture Decision Writer

Produces a short, honest comparison of 2-3 real technical approaches to a feature or the whole app, with actual tradeoffs (not just a list of pros), and one clear recommendation. This exists because non-technical founders using AI coding tools often get a stack picked FOR them mid-conversation, with no record of why, and no idea what they gave up. An ADR makes that decision visible, reversible in principle, and revisitable when it stops fitting.

## Stage
This skill belongs to Stage S5: Planning

## When to Use
- A PRD exists and it's time to pick how the app will actually be built (database, hosting, auth, framework)
- A specific feature has more than one viable technical approach (e.g., real-time chat: WebSockets vs. polling vs. a managed service)
- The user is being pushed toward a stack decision by an AI coding assistant and wants to understand why before agreeing
- An existing app hit a wall (cost, scaling, complexity) and a component needs to be reconsidered
- The user asks "why did we choose this" and no record exists
- Before `feature-task-breakdown` or `data-model-diagrammer` in Stage S3, when the underlying approach isn't settled yet

## Input Schema
```
decision_scope: string            # "whole app" or a specific feature/component
prd_path?: string                 # path to the PRD this decision must satisfy
candidate_approaches?: string[]   # if the user already has 2-3 in mind; otherwise this skill proposes them
constraints: {
  budget?: string,                # e.g. "under $50/mo to start"
  team_skill?: string,            # e.g. "non-technical, relies on AI coding tools"
  scale_expectation?: string,     # e.g. "under 1000 users for first 6 months"
  must_use?: string[],            # hard requirements, if any
  must_avoid?: string[]           # things ruled out already
}
```

## Workflow
### Step 1: Pin down what's actually being decided
Confirm the scope: is this the whole app's foundation (hosting + database + auth) or one feature's approach (e.g., search, file uploads, payments)? A decision that's too broad produces mush; narrow it to one decision with a clear boundary.

### Step 2: Surface real constraints, not assumed ones
Ask directly about budget ceiling, expected scale in the next 6-12 months (not "eventually millions of users" — actual near-term number), and how much of the maintenance the user can do themselves versus relying on AI tooling. These constraints, not technical elegance, should drive the recommendation for a solo non-technical founder.

### Step 3: Generate 2-3 real candidate approaches
Each candidate must be a genuinely viable, currently-real option (not a strawman). For a stack decision, examples: "Cloudflare Workers + D1" vs. "Cloudflare Workers + Supabase" vs. "Vercel + Postgres (Neon)". For a feature decision, examples: "polling every 5s" vs. "WebSockets" vs. "managed realtime service (Supabase Realtime/Pusher)". If the user already named candidates, use those instead of substituting your own.

### Step 4: Write tradeoffs per candidate, not just pros
For each candidate cover: setup complexity for a non-expert, ongoing cost at the stated scale, what breaks or gets expensive if scale grows 10x, vendor lock-in risk, and how well it's documented/supported by AI coding assistants (this matters a lot for this audience — an obscure stack means worse AI-generated code). Avoid generic "it's scalable" language — say specifically what happens and when.

### Step 5: Make one clear recommendation
Pick one. State it in one sentence, then justify it against the constraints from Step 2, not against abstract best practice. If two options are genuinely close, say so and give the one deciding factor.

### Step 6: State what changes the decision later
Name the specific triggers that would make this the wrong choice later (e.g., "if you pass 50k monthly active users" or "if you need offline support"). This turns the ADR into something revisitable instead of a permanent commitment.

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Every candidate is a real, currently-available option, not a made-up placeholder
- [ ] Tradeoffs include cost, complexity-for-non-expert, and lock-in risk for each candidate
- [ ] Recommendation is a single clear choice, not "it depends"
- [ ] Recommendation is justified against the user's stated constraints, not generic best practice
- [ ] At least one concrete trigger for revisiting the decision is listed

## Output Schema
```
{
  "decision_scope": string,
  "constraints_considered": object,
  "candidates": [
    {
      "name": string,
      "setup_complexity": string,
      "cost_at_stated_scale": string,
      "breaks_at": string,
      "lock_in_risk": string,
      "ai_tooling_support": string
    }
  ],
  "recommendation": string,
  "recommendation_reasoning": string,
  "revisit_triggers": string[]
}
```

## Output Format
```markdown
# ADR: <Decision Title>

**Status:** Proposed
**Scope:** <whole app / specific feature>
**Date:** <date>

## Context
<what needs to be decided and why now>

## Constraints
- Budget: <...>
- Expected scale (6-12mo): <...>
- Team skill level: <...>

## Candidates

### Option A: <name>
- Setup complexity: <...>
- Cost at stated scale: <...>
- Breaks/gets expensive at: <...>
- Lock-in risk: <...>
- AI tooling support: <...>

### Option B: <name>
...

### Option C: <name>
...

## Recommendation
**Chosen: <Option X>**

<why, tied directly to the stated constraints>

## Revisit This Decision If
- <trigger 1>
- <trigger 2>
```

## Error Handling
- If the user has no idea what constraints matter, default to conservative assumptions (low budget, non-technical, low near-term scale) and state those assumptions explicitly.
- If the user demands a specific stack with no real alternative worth comparing, write a 1-option ADR that documents the choice and its risks rather than forcing a fake comparison.
- If a candidate has since been deprecated or changed materially, flag that it may be out of date and recommend verifying current pricing/limits before committing.
- If constraints are contradictory (e.g., "must scale to millions" and "must be free forever"), surface the conflict and ask which one bends.
- If this ADR would contradict an existing ADR on file, show the conflict and ask whether this supersedes it.

## Examples
**Example 1:** User asks "should I use Firebase or Supabase for my app?" The skill asks about budget and scale, learns it's a solo founder expecting under 500 users for months, and recommends Supabase for its SQL familiarity and easier migration path, noting Firebase's NoSQL model would complicate a later feature the PRD calls for (relational data between users and projects).

**Example 2:** User's AI coding tool already built half the app on a stack the user never chose. The skill treats this as a "document the existing decision" case — writes the ADR retroactively, honestly notes the risks of the stack given the constraints, and flags whether it's worth migrating now versus later.

**Example 3:** A feature decision — real-time notifications for a small internal tool. The skill compares polling, WebSockets, and a managed service, recommends polling every 10s as the simplest option given under 50 users, and notes the trigger to revisit ("if users complain about notification delay, or user count passes 200").

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `data-model-diagrammer` (S6-Building) — the chosen database approach determines the data model shape
- `feature-task-breakdown` (S6-Building) — tasks are written against the chosen stack
- `tech-debt-detector` (S5-Planning) — checks later whether the build actually followed the ADR

### Fed By
- `prd-writer` (S5-Planning) — the must-have features define what the architecture needs to support
- `tech-stack-finder` (S1-Research) — surfaces real candidate stacks before this skill compares them

### Feedback Loop
When `tech-debt-detector` or `app-performance-report` finds the app has outgrown or is straining against the chosen approach, that should trigger a fresh ADR referencing this one, not a silent stack swap mid-build.

```yaml
chain_metadata:
  skill_slug: "architecture-decision-writer"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "data-model-diagrammer"
    - "feature-task-breakdown"
    - "tech-debt-detector"
```
