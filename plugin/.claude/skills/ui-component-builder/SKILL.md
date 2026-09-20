---
name: ui-component-builder
description: >
  Turn a plain-language UI description into a scoped component build task —
  props, states, and responsive behavior defined — without letting it creep into
  a full redesign.
  Use this skill when the user asks about building a specific UI piece, adding a
  component, or says
  "build me a settings panel", "I need a pricing table component", "add a modal for this",
  "what props should this component take", "build this form", "make a card component for this",
  "add a dropdown for X", "I just need this one piece of UI, not a redesign".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "ui", "frontend", "component"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# UI Component Builder

Turns a plain-language description of one piece of UI into a tightly scoped build task: what props it takes, what states it can be in, how it behaves on mobile vs desktop, and what it explicitly does NOT touch. Exists to stop the common failure where "add a settings panel" turns into the AI agent restyling the whole app.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- Building one new UI piece (form, modal, table, card, nav item) for an existing app
- The user has a working app and needs to add a component without disturbing the rest of the design
- A feature task from feature-task-breakdown reaches the UI layer
- The user's previous AI build attempt on a component sprawled into unrelated files
- Wiring a component to an already-designed API endpoint (from api-endpoint-builder)
- The user says "just this one thing" and needs guardrails to keep it that way

## Input Schema
```
component_description: string    # plain language description of the UI piece
existing_design_system: string?  # component library, tokens, or "match existing style"
data_source: string?             # API endpoint or data shape it displays/submits
framework: string?               # React, Vue, Svelte, plain HTML, etc.
explicitly_out_of_scope: string? # anything the user wants untouched
```

## Workflow
### Step 1: Name the component and its one job
State the component name and the single job it does. If the description implies multiple components (e.g. "a settings page" = nav + form + save button as separate concerns), break it into the smallest real component first and note the others as separate tasks.

### Step 2: Define props/inputs
List every prop the component needs: name, type, required/optional, default value. No prop should be vague ("data: object") — specify shape.

### Step 3: Define states
List every visual/behavioral state: default, loading, empty, error, success, disabled, hover/focus if relevant. A component missing loading/empty/error states is not done.

### Step 4: Define responsive behavior
State explicitly what changes at mobile width vs desktop (stacks, hides, truncates, scrolls). If existing_design_system gives breakpoints, use them; otherwise use sensible defaults and flag as assumption.

### Step 5: Draw the scope boundary
List explicitly what this task does NOT include: no changes to layout outside this component, no changes to global styles/tokens unless stated, no touching unrelated pages. This is the section that prevents scope creep.

### Step 6: Scaffold the component
Write the component code in the specified framework, wired to the given data_source if provided, with all defined states implemented (not just the happy path).

### Step 7: Self-Validation
Before presenting, silently confirm:
- [ ] Component has exactly one clear job
- [ ] Every prop has a defined type and default
- [ ] Loading, empty, and error states are all covered, not just the happy path
- [ ] Responsive behavior is explicit, not left to chance
- [ ] Out-of-scope boundary is stated so the build doesn't creep
- [ ] Code matches existing design system/tokens if provided

## Output Schema
```json
{
  "component_name": "string",
  "job": "string",
  "props": [
    {"name": "string", "type": "string", "required": "boolean", "default": "string | null"}
  ],
  "states": ["default", "loading", "empty", "error", "success", "disabled"],
  "responsive_behavior": {"mobile": "string", "desktop": "string"},
  "out_of_scope": ["string"],
  "code_scaffold": "string"
}
```

## Output Format
```markdown
# Component: <ComponentName>

**Job:** <one sentence>

## Props
| Prop | Type | Required | Default |
|---|---|---|---|
| ... | ... | ... | ... |

## States to handle
- Default: <description>
- Loading: <description>
- Empty: <description>
- Error: <description>
- Success: <description>

## Responsive behavior
- Mobile: <behavior>
- Desktop: <behavior>

## Out of scope (do not touch)
- <boundary 1>
- <boundary 2>

## Code
```<language/jsx>
<component code>
```

## Verify
- <how to visually/functionally confirm each state works, e.g. "toggle loading prop, confirm spinner shows">
```

## Error Handling
- If the description is really a full page or multiple components, split it and build the smallest piece first, listing the rest as follow-up tasks — never silently expand scope to "finish the page."
- If no design system info is given, default to plain, clean styling matching common SaaS conventions and flag it as an assumption, don't invent a new visual language.
- If the data_source/API isn't built yet, scaffold against the expected shape and mark it clearly as a stub pending api-endpoint-builder.
- If the user's ask implies a visual redesign rather than one component, redirect to the `impeccable` or `taste-skill` design skills instead — this skill is for scoped component builds, not design direction.
- If explicitly_out_of_scope conflicts with something the component technically requires (e.g. "don't touch global styles" but the component needs a new color token), flag the conflict rather than silently overriding the boundary.

## Examples

**Example 1**
User: "Add a pricing table component to my landing page, don't touch anything else."
Skill does: scopes to one PricingTable component, props (plans: Plan[], currentPlanId?, onSelect), states (default, loading if plans are fetched, empty if no plans), responsive (grid on desktop, stacked cards on mobile), explicit out-of-scope note that hero/nav/footer aren't touched.
Outcome: clean isolated component, no unrelated page changes.

**Example 2**
User: "I need a form for users to update their billing address, wired to my existing PATCH /api/billing-address endpoint."
Skill does: defines props matching the endpoint's request shape, states include submitting/success/validation-error, responsive stacks fields on mobile, scaffolds with client-side validation matching server rules from api-endpoint-builder output.
Outcome: form component ready to drop in, consistent with the already-defined API contract.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- test-case-generator (S7-Testing)
- browser-verifier (S7-Testing)
- accessibility-auditor (S7-Testing)

### Fed By
- api-endpoint-builder (S6-Building)
- feature-task-breakdown (S6-Building)

### Feedback Loop
When accessibility-auditor or browser-verifier flags issues (missing states, broken responsive behavior), feed those back so future component scaffolds include that state/behavior by default.

```yaml
chain_metadata:
  skill_slug: "ui-component-builder"
  stage: "building"
  timestamp: string
  suggested_next:
    - "test-case-generator"
    - "browser-verifier"
    - "accessibility-auditor"
```
