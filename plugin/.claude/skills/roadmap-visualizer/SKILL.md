---
name: roadmap-visualizer
description: >
  Turns a written roadmap or feature list into a live, visual, trackable board
  (phases as columns, features as cards with status) published as an Artifact —
  instead of a markdown file nobody re-opens.
  Use this skill when the user asks about "show me the roadmap", "I want to see
  progress visually", or says
  "make this roadmap something I can actually look at", "I don't want another markdown file",
  "turn this into a board I can check off", "show me what's done vs. not",
  "I keep losing track of what's built", "visual version of my plan",
  "can I see this as a kanban board", "track my roadmap progress".
license: MIT
version: "1.0.0"
tags: ["saas", "planning", "roadmap", "visual", "tracking"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S2-Planning
---

# Roadmap Visualizer

Takes the output of `prd-writer`, `feature-roadmap-architect`, or `mvp-feature-slicer` and publishes it as a live, visual roadmap board — phases as columns, features as cards, status tracked and updated over time. This exists because a markdown roadmap gets written once and never looked at again; a board the founder can actually glance at gets used.

## Stage
This skill belongs to Stage S2: Planning

## When to Use
- After `feature-roadmap-architect` produces a phased plan and the founder wants to see it, not read it
- The founder says they keep losing track of what's built vs. not
- A roadmap markdown file exists but hasn't been opened in weeks
- Starting a new build and want a trackable board from day one instead of a doc
- Reviewing progress mid-project and the current roadmap doc is stale

## Input Schema
```
{
  roadmap_source: string       # phased feature list, usually from feature-roadmap-architect output
  project_name: string         # what to title the board
  current_status: object[]     # (optional) known status per feature: "not-started" | "in-progress" | "done" | "blocked"
  update_mode: string          # "create" | "update" — whether this is a new board or refreshing an existing one
}
```

## Workflow

### Step 1: Gather the Roadmap Content
Read the phased roadmap (from `feature-roadmap-architect` or the PRD). Each phase becomes a column. Each feature/task becomes a card. If status isn't given, ask the founder which items are done, in progress, or not started — don't guess.

### Step 2: Load the Artifact Design Skill
Before writing any HTML, load the `artifact-design` skill for page-design guidance (title, layout, theming, mobile width). Load `artifact-capabilities` too, since this board needs state that persists across viewers and sessions — this is not a one-off static page.

### Step 3: Decide on the Capability
This board needs the `db` capability (ArtifactData) so that checking a card off as done is a real write that survives republishing and is visible next time the founder opens it — not `localStorage`, which only lives in one browser. Use `ArtifactData` for status changes (`update` action), not a full republish, once the board exists.

### Step 4: Build the Board
Structure:
- One column per phase (Now / Next / Later, or the phase names from the roadmap)
- One card per feature: title, one-line description, status badge, and a click-to-cycle status control (not-started → in-progress → done → blocked)
- A progress bar or percentage at the top showing overall completion
- Cards for "done" visually distinct (dimmed/checked) so progress is obvious at a glance

### Step 5: Publish
Publish via the Artifact tool. Title it clearly with the project name. Give the founder the link and tell them this is now the living source of truth for progress — not the markdown file.

### Step 6: Wire Updates
Tell the founder: going forward, when a feature ships, either they click the status on the board themselves, or they can tell Claude "mark X as done" and the skill writes that update via `ArtifactData` rather than rebuilding the whole page.

### Step 7: Self-Validation
- [ ] Every phase from the roadmap has a column
- [ ] Every feature has a card with correct status
- [ ] The board uses `db` capability, not browser storage, for status
- [ ] Progress is visible at a glance without reading every card
- [ ] The founder was given the actual link, not just told "it's published"

## Output Schema
```
{
  artifact_url: string
  project_name: string
  phase_count: number
  feature_count: number
  completion_percent: number
}
```

## Output Format
```
## Roadmap Board Published

**[Project Name] Roadmap** → [artifact link]

[X]% complete — [N] of [M] features done

Phases: [Phase 1] · [Phase 2] · [Phase 3]

This board is now the source of truth for progress. Update it by telling me
"mark [feature] as done" or clicking status directly on the board.
```

## Error Handling
- **No roadmap exists yet:** Point to `feature-roadmap-architect` first — this skill visualizes a roadmap, it doesn't create one from nothing.
- **Status unknown for some items:** Ask the founder rather than defaulting everything to "not-started," which would be misleading if work has already happened.
- **Updating an existing board:** Read the current artifact first via the Artifact tool's read action, merge changes, and republish to the same URL — never create a duplicate board.
- **Roadmap has too many items for one screen:** Group into collapsible phases rather than cutting content.

## Examples

**Example 1:**
User: "I have a roadmap for my app but I never look at it, can you make it visual?"
→ Read the existing roadmap doc, ask which items are actually done
→ Build a Kanban-style board with db-backed status, publish, hand over the link

**Example 2:**
User: "mark the auth flow as done"
→ Read the existing roadmap board artifact
→ Update that card's status via ArtifactData, not a full rebuild
→ Confirm the new completion percentage

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- feature-task-breakdown (S3-Building) — once a phase's cards are visible, break the next one into build tasks
- app-performance-report (S7-Growth) — roadmap completion is a useful context line in a status report

### Fed By
- feature-roadmap-architect (S2-Planning) — supplies the phased structure this skill visualizes
- mvp-feature-slicer (S2-Planning) — supplies the v1 scope that becomes the first board

### Feedback Loop
- As features get marked done on the board over multiple sessions, the completion trend itself becomes useful data for `self-improver` to judge whether the roadmap's original phase sizing was realistic.

```yaml
chain_metadata:
  skill_slug: "roadmap-visualizer"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-task-breakdown"
    - "app-performance-report"
```
