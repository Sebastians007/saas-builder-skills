---
name: hub-renderer
description: >
  Renders the founder-facing hub.html from project.json. It is presentation-only:
  it never invents project facts or mutates project state. Sections appear
  conditionally based on project type and available data.
license: MIT
version: "5.0.0"
tags: ["dashboard", "html", "project-hub", "visualization"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  capability: orchestration
---

# Hub Renderer

## Rule

`project.json` in, `hub.html` out.

Never write project facts back into state.

## Layout

Desktop:
- sticky left sidebar;
- content area;
- dashboard-first;
- clear current phase/status;
- open blockers visible without scrolling.

Mobile:
- compact top navigation or collapsible sidebar;
- readable cards/tables;
- no horizontal overflow.

## Conditional Sections

Potential sections:
1. Dashboard
2. Project / Company
3. Current Direction
4. Research & Evidence
5. Users, Jobs & Problems
6. Positioning & Differentiation
7. Offer / Business Model
8. Requirements & Scope
9. Roadmap
10. UX / Customer Journey
11. Marketing / Funnel
12. Build
13. Verification, Security & Accessibility
14. Launch
15. Operations & Growth
16. Decisions
17. Assumptions & Open Questions
18. Sources

Hide sections that are irrelevant and empty.

## Dashboard

Always show:
- project name/type;
- current phase/status;
- short direction;
- progress summary;
- current work;
- blockers/open questions;
- last meaningful decisions;
- next actions.

## Visual language

Internal control panel, not a sales page.

Prefer:
- restrained typography;
- strong hierarchy;
- useful density;
- status badges;
- readable tables;
- clear evidence/source treatment;
- no decorative dashboard nonsense for its own sake.

If an existing hub design system exists, reuse it. Do not force a full product-design interview on every regeneration.

## Rendering

- self-contained local HTML unless the project already has an internal web app for the hub;
- use project state, never stale embedded constants;
- escape untrusted text;
- source links remain clickable;
- regenerate completely rather than hand-patching fragments.

## Validation

Check:
- no state values are invented;
- dashboard reflects current state;
- hidden sections are genuinely irrelevant/empty;
- decisions/assumptions are distinguishable;
- sources are visible for researched claims;
- file opens locally without missing dependencies.
