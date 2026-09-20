---
name: tech-debt-detector
description: >
  Reviews an existing codebase or a written plan for shortcuts, vague areas, and
  unresolved decisions that will cause problems later, and flags them before they get
  built on top of, not after.
  Use this skill when the user asks about "is my codebase a mess", "what's going to
  break later", or says
  "review my codebase for problems", "the AI keeps making stuff up in this file",
  "I think there's tech debt here but I don't know where", "check this plan before I build it",
  "something feels off about how this was built", "audit what Claude built last week",
  "is this going to be a nightmare to extend later".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "tech-debt", "code-review", "risk-audit"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S2-Planning
---

# Tech Debt Detector

Reads either an existing codebase or a written plan/PRD/ADR and flags shortcuts, vague or hand-waved areas, and decisions nobody actually made — before they get built on top of and become expensive to fix. This is planning-stage risk control: catching "TODO: figure out auth later" or "we'll just hardcode this for now" while it's still cheap to fix, not six months in when three other features depend on the shortcut.

## Stage
This skill belongs to Stage S2: Planning

## When to Use
- Before starting a new build phase on top of an existing codebase
- The user has been "vibe coding" with AI tools for a while and suspects things are fragile
- A PRD, ADR, or roadmap has vague language like "handle this properly later" or "TBD"
- Before `feature-roadmap-architect` sequences new work — debt should be visible in the sequencing, not hidden
- Periodically (e.g., before each major release) as a standing check, not just once
- The user asks "why does everything feel harder to change than it used to"

## Input Schema
```
target: "codebase" | "plan"
codebase_path?: string            # if reviewing code
plan_path?: string                # if reviewing a PRD/ADR/roadmap document
focus_area?: string               # optional: narrow to auth, data model, payments, etc.
severity_threshold?: "all" | "high-only"
```

## Workflow
### Step 1: Establish what "done right" looks like
Pull the relevant PRD and ADR if they exist, so shortcuts can be judged against actual stated requirements, not generic best practice. If no PRD/ADR exists, note that as debt itself — you cannot tell if something is a shortcut without knowing what it was supposed to do.

### Step 2: Scan for the four debt categories
1. **Hardcoded / stubbed logic** — values, user IDs, permissions, or config that should be dynamic but are hardcoded "for now."
2. **Silent scope gaps** — features referenced in the UI or plan but not actually implemented, or implemented for only one path (e.g., signup exists but password reset doesn't).
3. **Vague/undecided areas** — comments like "TODO," "figure out later," "temporary," or plan language like "we'll handle edge cases eventually."
4. **Structural risk** — things that work now but will actively break as usage grows or a new feature is added (e.g., no way to have more than one user, data model that can't represent a relationship the PRD implies is coming).

### Step 3: Rate each finding by blast radius, not just presence
For each item found, estimate: how many future features would need to touch or work around this? A shortcut that's isolated (affects one screen) is low severity. A shortcut in the data model, auth, or a shared utility that many features will build on is high severity — flag these regardless of how small they look today.

### Step 4: Distinguish "acceptable for now" from "must fix before building more"
Not all debt needs fixing immediately. For each finding, state a recommendation: fix now, fix before the next feature that touches it, or accept and document (with a note of what would force revisiting it). Do not recommend fixing everything — that defeats the purpose of planning-stage triage.

### Step 5: Write the findings as a punch list, not prose
Non-technical founders need a scannable list they can act on or hand to an AI coding tool, not a narrative essay. Group by severity.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Every finding names a specific file/area or plan section, not a vague generalization
- [ ] Every finding has a severity and a recommendation (fix now / fix before next touch / accept)
- [ ] High-severity findings are ones with real blast radius, not just stylistic nitpicks
- [ ] If no PRD/ADR existed to check against, that absence is itself listed as a finding
- [ ] The list is short enough to actually be actionable (prioritized, not exhaustive noise)

## Output Schema
```
{
  "target": "codebase" | "plan",
  "reviewed_against": string,     # PRD/ADR reference, or "none found"
  "findings": [
    {
      "category": "hardcoded" | "scope_gap" | "vague_undecided" | "structural_risk",
      "location": string,
      "description": string,
      "blast_radius": "low" | "medium" | "high",
      "recommendation": "fix_now" | "fix_before_next_touch" | "accept_and_document"
    }
  ],
  "summary": string
}
```

## Output Format
```markdown
# Tech Debt Review: <target>

Reviewed against: <PRD/ADR name, or "no plan on file — flagged below">

## Fix Now (high blast radius)
- **<location>** — <what's wrong> → <why it matters>

## Fix Before Next Touch
- **<location>** — <what's wrong> → <what triggers needing to fix it>

## Accept & Document (low risk, known tradeoff)
- **<location>** — <what's wrong> → <why it's fine for now, and what would change that>

## Summary
<2-3 sentence plain-language read on overall health: solid foundation with isolated debt, or foundational debt that will slow every future feature>
```

## Error Handling
- If given a huge codebase, ask to scope to a focus area (auth, data model, a specific feature) rather than attempting a shallow full-codebase pass.
- If no PRD or ADR exists to check against, still scan for the four debt categories using general correctness/consistency signals, but clearly flag "no spec on file" as the top finding.
- If everything looks clean, say so plainly — do not manufacture findings to seem thorough.
- If a finding depends on a technical judgment call (e.g., is this actually a scaling risk at this user count), state the assumption behind the call rather than presenting it as certain.
- If reviewing a plan rather than code, do not evaluate code quality — only evaluate whether the plan's stated approach has gaps or hand-waves.

## Examples
**Example 1:** User asks to review a codebase before adding a team/multi-user feature. The skill finds the data model hardcodes a single user ID in several places (high blast radius, fix now — it blocks the exact feature being planned), a missing password reset flow (medium, fix before next touch), and a hardcoded email sender address (low, accept and document).

**Example 2:** User pastes a roadmap plan with a line "auth: use whatever's easiest, figure out permissions later." The skill flags this as vague/undecided with high blast radius since nearly every future feature will need to know what a user can and can't do, and recommends resolving it via `architecture-decision-writer` before any building starts.

**Example 3:** User asks for a periodic health check on an app that's been stable for months. The skill scans and finds mostly low-severity, accept-and-document items, and reports the app is in solid shape with no urgent fixes needed.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-roadmap-architect` (S2-Planning) — high-severity debt gets slotted into the roadmap before new features that depend on it
- `architecture-decision-writer` (S2-Planning) — vague/undecided structural findings often need a real ADR to resolve
- `security-review-lite` (S4-Testing) — structural risk findings around auth/data access feed the security pass

### Fed By
- `architecture-decision-writer` (S2-Planning) — provides the "what was actually decided" baseline to check the build against
- `feature-task-breakdown` (S3-Building) — completed tasks are what gets reviewed for shortcuts taken during implementation

### Feedback Loop
Recurring high-severity findings in the same area (e.g., auth, data model) across multiple review passes should trigger a dedicated ADR and a roadmap phase to fix it properly, rather than being re-flagged and deferred indefinitely.

```yaml
chain_metadata:
  skill_slug: "tech-debt-detector"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-roadmap-architect"
    - "architecture-decision-writer"
    - "security-review-lite"
```
