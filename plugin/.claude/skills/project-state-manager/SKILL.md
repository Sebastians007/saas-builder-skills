---
name: project-state-manager
description: >
  Owns the durable project.json state for the v5 workflow. Initializes project
  state, applies structured patches from specialist skills, preserves decisions
  and assumptions, tracks provenance, and prevents planning documents from
  contradicting one another.
license: MIT
version: "5.0.0"
tags: ["state", "context", "memory", "project-management"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  capability: orchestration
---

# Project State Manager

## Authority

`project.json` is the project source of truth.

Do not treat chat history, hub HTML, old briefs, or stale plans as more authoritative than current state plus current code/product reality.

## Initialize

Use `shared/references/project-schema.md`.

Create only one project root unless the user requests otherwise.

At minimum initialize:
- name;
- type;
- status;
- current phase;
- summary/direction;
- known facts;
- assumptions;
- decisions;
- next actions.

## Apply Patch

Specialists should return bounded changes. Merge them into the correct section.

Rules:
- facts and assumptions are separate;
- user corrections replace/reject assumptions;
- decisions are append-only records; supersede rather than erase;
- external findings keep source/provenance;
- current product/code evidence may invalidate stale plan state;
- do not destroy unknown fields during schema upgrades.

## Conflict Resolution

Priority:
1. explicit current user instruction;
2. current observed product/code reality;
3. verified current external evidence;
4. current project decisions;
5. older plans;
6. assumptions.

Record meaningful conflicts in `open_questions` or `decisions`.

## State Hygiene

Avoid storing:
- giant raw transcripts;
- duplicated specialist prose;
- secrets;
- credentials;
- temporary chain-of-thought.

Store conclusions, evidence, rationale, and actionable state.

## Output

After an update, return:
- keys changed;
- decisions appended;
- assumptions added/rejected;
- next-actions changed;
- whether hub regeneration is warranted.
