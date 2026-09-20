---
name: roadmap-visualizer
description: >
  Turns a written roadmap or feature list into a real, visual, trackable board
  (phases as columns, features as cards with status) saved as a local HTML
  file in the project folder — instead of a markdown file nobody re-opens.
  Use this skill when the user asks about "show me the roadmap", "I want to see
  progress visually", or says
  "make this roadmap something I can actually look at", "I don't want another markdown file",
  "turn this into a board I can check off", "show me what's done vs. not",
  "I keep losing track of what's built", "visual version of my plan",
  "can I see this as a kanban board", "track my roadmap progress".
license: MIT
version: "2.0.0"
tags: ["saas", "planning", "roadmap", "visual", "tracking", "local-file"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "2.0"
  stage: S5-Planning
---

# Roadmap Visualizer

Takes the output of `prd-writer`, `feature-roadmap-architect`, or `mvp-feature-slicer` and turns it into a real, visual roadmap board — phases as columns, features as cards, status tracked over time — saved as a local HTML file the founder opens directly in their browser. This exists because a markdown roadmap gets written once and never looked at again; a board the founder can actually glance at gets used.

**Follows `shared/references/output-conventions.md`: local files only, never a published Artifact.**

## Stage
This skill belongs to Stage S5: Planning

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
  project_name: string         # what to title the board — ask for the brand/business name too if not already known from context
  current_status: object[]     # (optional) known status per feature: "not-started" | "in-progress" | "done" | "blocked"
  update_mode: string          # "create" | "update" — whether this is a new board or refreshing an existing one
}
```

## Workflow

### Step 1: Gather the Roadmap Content
Read the phased roadmap (from `feature-roadmap-architect` or the PRD). Each phase becomes a column. Each feature/task becomes a card. If status isn't given, ask the founder which items are done, in progress, or not started — don't guess.

### Step 2: Set Up the Project Folder
Confirm the brand/business name if not already clear from context (see `shared/references/output-conventions.md` — never default to the project name alone). Create `[brand-slug]-[project-name-slug]-roadmap/` in the user's working directory if it doesn't already exist (on an update, reuse the existing one). Inside it:
- `data/roadmap.json` — the structured source of truth: phases, cards, statuses
- `roadmap.html` — the rendered board, regenerated from `roadmap.json` every time

### Step 3: Write the Data File
Write `data/roadmap.json` with the phase/card/status structure. This file is what actually gets edited when status changes — the HTML is always a regeneration of it, never edited by hand.

### Step 4: Build the Board (static HTML, generated from the data file)
Structure:
- One column per phase (Now / Next / Later, or the phase names from the roadmap)
- One card per feature: title, one-line description, status badge
- A progress bar or percentage at the top showing overall completion, computed from `roadmap.json`
- Cards for "done" visually distinct (dimmed/checked) so progress is obvious at a glance
- Self-contained HTML: inline CSS, no external published dependencies, opens correctly straight from the filesystem (`file://`) with no server needed

### Step 5: Save and Tell the User
Write `roadmap.html` to the project folder. Tell the founder the exact path and that they can open it directly in their browser (double-click the file, or drag it into a browser tab). This is now the living source of truth for progress — not the markdown file.

### Step 6: Wire Updates
Tell the founder: when a feature ships, tell Claude "mark X as done." The skill then edits `data/roadmap.json` and regenerates `roadmap.html` in place — the founder refreshes the already-open browser tab to see the change. No client-side write-back exists; Claude is what keeps the file current.

### Step 7: Self-Validation
- [ ] Every phase from the roadmap has a column
- [ ] Every feature has a card with correct status
- [ ] `roadmap.json` is the source of truth; `roadmap.html` is always regenerated from it, never hand-edited
- [ ] Progress is visible at a glance without reading every card
- [ ] The founder was given the exact local file path, not a link

## Output Schema
```
{
  project_folder: string
  html_path: string
  data_path: string
  project_name: string
  phase_count: number
  feature_count: number
  completion_percent: number
}
```

## Output Format
```
## Roadmap Board Saved

**[Project Name] Roadmap** → [project-folder]/roadmap.html

Open it in your browser (double-click the file, or drag it into a tab).

[X]% complete — [N] of [M] features done

Phases: [Phase 1] · [Phase 2] · [Phase 3]

This is now the source of truth for progress. Tell me "mark [feature] as done"
and I'll update the file — refresh the tab to see it.
```

## Error Handling
- **No roadmap exists yet:** Point to `feature-roadmap-architect` first — this skill visualizes a roadmap, it doesn't create one from nothing.
- **Status unknown for some items:** Ask the founder rather than defaulting everything to "not-started," which would be misleading if work has already happened.
- **Updating an existing board:** Read the existing `data/roadmap.json` first, merge changes, regenerate `roadmap.html` — never create a duplicate project folder for the same project.
- **Roadmap has too many items for one screen:** Group into collapsible phases rather than cutting content.

## Examples

**Example 1:**
User: "I have a roadmap for my app but I never look at it, can you make it visual?"
→ Read the existing roadmap doc, ask which items are actually done
→ Create the project folder, write `data/roadmap.json`, generate `roadmap.html`
→ Give the founder the exact file path to open

**Example 2:**
User: "mark the auth flow as done"
→ Read the existing `data/roadmap.json`
→ Update that card's status, regenerate `roadmap.html`
→ Confirm the new completion percentage and remind them to refresh the open tab

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `shared/references/output-conventions.md`

## Flywheel Connections
### Feeds Into
- feature-task-breakdown (S6-Building) — once a phase's cards are visible, break the next one into build tasks
- app-performance-report (S10-Growth) — roadmap completion is a useful context line in a status report

### Fed By
- feature-roadmap-architect (S5-Planning) — supplies the phased structure this skill visualizes
- mvp-feature-slicer (S5-Planning) — supplies the v1 scope that becomes the first board

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
