# Output Conventions v5

## One project, one root

The project root uses the user-facing brand/product/company name when known.

Examples:

```text
Acme/
Acme CRM/
Internal Finance Tool/
```

Do not append service names to the root unless the user explicitly wants separate roots.

## Core files

Prefer a small set of durable files:

```text
ProjectName/
  project.json     # source of truth
  hub.html         # human-facing rendered control panel
  brief.md         # portable narrative summary
  ...actual project/site/app files
```

Do not create a new planning document for every specialist skill.

## State ownership

Specialist skills return structured patches.

`project-state-manager` is responsible for applying those patches to `project.json`.

`hub-renderer` reads `project.json` and regenerates `hub.html`.

No specialist should hand-edit `hub.html`.

## Hub behavior

The hub is conditional. Hide irrelevant empty sections.

Recommended sidebar:

- Dashboard
- Project / Company
- Current Direction
- Research & Evidence
- Users, Jobs & Problems
- Positioning & Differentiation
- Offer / Business Model
- Requirements & Scope
- Roadmap
- UX / Customer Journey
- Marketing / Funnel
- Build
- Verification, Security & Accessibility
- Launch
- Operations & Growth
- Decisions
- Assumptions & Open Questions
- Sources

## Design

The hub should be clean, functional, and founder-readable.

For customer-facing HTML, use the strongest available design skill.

For internal hub updates, do not require a heavyweight product-design interview on every render. Reuse an established hub design system. Only re-run a full design process when the user asks for a redesign or the hub has no design system yet.

## Local-first

Keep project outputs as real files.

Do not publish hosted artifacts unless the user explicitly asks for a hosted/shared artifact.

## Progressive updates

Long-running research/build work should update `project.json` and the hub as useful milestones complete. The user should be able to see progress without receiving five disconnected chat reports.

## Questions

Do not block on information that can be responsibly inferred.

When blocked:
- ask one compact question;
- explain the decision it affects;
- keep unrelated work moving where possible.

## Evidence

External claims must preserve source/provenance in project state. The hub may show concise citations/source links in its Sources section.
