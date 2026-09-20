---
name: skill-finder
description: >
  Finds specialist skills for a scoped task by reading registry.json dynamically.
  It no longer embeds a hard-coded copy of the skill catalog or acts as the
  project-level orchestrator.
license: MIT
version: "5.0.0"
tags: ["meta", "discovery", "routing"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  capability: meta
---

# Skill Finder

## Role

Use this for **specialist discovery**, not for running an entire project.

For project-level work, use `project-orchestrator`.

## Workflow

1. Read `registry.json` fresh. Never rely on a copied skill table in this file.
2. Restate the scoped task in one line.
3. Match task intent against current skill descriptions/capabilities.
4. Return 1-3 best specialists.
5. If the task spans a lifecycle or requires sequencing, route to `project-orchestrator` instead of constructing an ad-hoc workflow here.
6. If no real match exists, say so.

## Output

```json
{
  "task": "",
  "recommended": [
    {"slug": "", "why": ""}
  ],
  "route_to_project_orchestrator": false
}
```

## Rules

- Never recommend a skill only because its name shares a keyword.
- Never expose stale stage numbers as if the user must follow them.
- Never maintain an embedded "full skill table."
- Prefer action skills over informational skills when the user asked to do something.
