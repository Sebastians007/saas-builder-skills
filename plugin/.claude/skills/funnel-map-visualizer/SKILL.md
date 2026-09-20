---
name: funnel-map-visualizer
description: >
  Turns a planned or live funnel into one visual map showing every step, the
  page/copy at each step, and (once tracking exists) real conversion numbers
  per step — published as an Artifact instead of scattered SKILL.md workflow output.
  Use this skill when the user asks about "show me the whole funnel", "I want to see
  this visually", or says
  "map out my funnel visually", "show me the funnel as a diagram", "I can't picture
  how these pages connect", "where are people dropping off in this funnel",
  "give me a visual overview of the funnel", "show conversion rate at each step",
  "I want to see the whole customer journey in one place".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "visual", "tracking", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
---

# Funnel Map Visualizer

Takes the output of `funnel-select` and the individual funnel-type skill (webinar-funnel, tripwire-funnel, saas-funnel, etc.) and renders the whole funnel as one visual map — every step in order, what page/email/ad lives at each step, and once real traffic exists, the actual conversion rate between each step. This exists because a funnel described across several SKILL.md workflows is hard to hold in your head; a founder needs to see the whole path in one place to know where it's actually leaking.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- After `funnel-select` has picked a funnel type and the founder wants to see the whole thing laid out, not just read the steps
- Before building, to sanity-check the funnel makes sense end to end
- After launch, once `signup-conversion-tracker` or PostHog funnel data exists, to see real drop-off per step overlaid on the map
- The founder can't picture how the landing page, emails, and checkout connect

## Input Schema
```
{
  funnel_type: string          # from funnel-select, e.g. "tripwire-funnel", "webinar-funnel"
  steps: object[]              # ordered list: { name, type (page/email/ad/checkout), copy_summary }
  live_data: object            # (optional) per-step visitor/conversion counts, from PostHog or signup-conversion-tracker
  update_mode: string          # "create" | "update"
}
```

## Workflow

### Step 1: Gather the Funnel Structure
Pull the step sequence from the chosen funnel-type skill's output (e.g. tripwire-funnel: landing page → order bump → one-time-offer → thank-you/upsell). Confirm the order and what lives at each step (page, email, ad) before building anything.

### Step 2: Load the Artifact Design and Diagramming Skills
Load `artifact-design` for page fundamentals, and `artifact-diagramming` since this is fundamentally a flow diagram — read it before drawing the funnel so the connections between steps are legible, not just a stack of boxes.

### Step 3: Decide on Live Data
If the founder has PostHog connected and real traffic, this map should show real numbers (visitors in, converted, drop-off %) at each step — pull that via the PostHog MCP tools referenced in `growth-dashboard-builder` and `checkout-funnel-auditor`. If no live data yet, show the planned structure only and label it clearly as "not yet live" rather than inventing numbers.

### Step 4: Build the Map
Structure: a left-to-right (or top-to-bottom on mobile) flow of steps, each step as a card showing:
- Step name and type (page/email/ad)
- One-line copy summary (what this step says/sells)
- If live: visitor count in, % who moved to the next step, biggest visual weight given to the step with the worst drop-off (so the eye goes straight to the problem)

### Step 5: Publish
Publish via the Artifact tool. This is a living page — use the `db` capability if the founder wants it to auto-update as new PostHog data comes in, otherwise a static snapshot republished on request is fine for early-stage funnels with little traffic.

### Step 6: Highlight the Biggest Leak
If live data exists, explicitly call out which single step has the worst drop-off — that's the one `checkout-funnel-auditor` or `ab-test-generator` should be pointed at next, not a vague "optimize everything" note.

### Step 7: Self-Validation
- [ ] Every step from the chosen funnel type appears in order
- [ ] Each step shows what actually lives there (page/email/ad), not just a generic label
- [ ] Live data is only shown if real, never fabricated to look complete
- [ ] The worst-performing step (if data exists) is visually obvious, not buried
- [ ] The founder was given the actual link

## Output Schema
```
{
  artifact_url: string
  funnel_type: string
  step_count: number
  has_live_data: boolean
  worst_dropoff_step: string
}
```

## Output Format
```
## Funnel Map Published

**[Funnel Type] Funnel Map** → [artifact link]

Steps: [Step 1] → [Step 2] → [Step 3] → [Step 4]

[If live data:]
Biggest leak: [Step Name] — only [X]% continue past this step. Fix this one first.

[If no live data:]
No traffic yet — this is the planned structure. Come back once PostHog is
tracking real visitors and I'll overlay actual conversion numbers.
```

## Error Handling
- **No funnel type chosen yet:** Point to `funnel-select` first — this skill visualizes a chosen funnel, it doesn't pick one.
- **Live data requested but PostHog isn't connected:** Say so plainly and show the planned structure only; never fabricate conversion numbers to fill the gap.
- **Funnel has steps not covered by the source funnel-type skill (custom steps added):** Include them as given, but flag if the sequence seems to skip a normally-required step (e.g. a checkout with no thank-you page).
- **Updating an existing map with new live data:** Read the current artifact, refresh only the data layer, keep the structure — don't regenerate the whole page from scratch each time.

## Examples

**Example 1:**
User: "I picked the tripwire funnel, can you show me what it actually looks like end to end?"
→ Pull the 4-step structure from tripwire-funnel's output
→ Build the visual map with no live data yet, labeled as planned
→ Publish and hand over the link

**Example 2:**
User: "where is my funnel actually leaking?"
→ Confirm PostHog is connected, pull step-by-step conversion data via checkout-funnel-auditor's data source
→ Overlay real numbers on the existing map, highlight the worst step
→ Recommend ab-test-generator or checkout-funnel-auditor as the next skill to run on that specific step

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- checkout-funnel-auditor (S7-Growth) — the worst-performing step this map surfaces is exactly what that skill should audit next
- ab-test-generator (S7-Growth) — once a leak is identified, test a fix at that specific step

### Fed By
- funnel-select (S9-Funnels) — supplies the chosen funnel type and step structure
- signup-conversion-tracker (S7-Growth) / growth-dashboard-builder (S7-Growth) — supply the live per-step numbers once traffic exists

### Feedback Loop
- Each time this map is refreshed with new live data, the trend in where the worst leak sits over time tells `self-improver` whether past fixes actually worked.

```yaml
chain_metadata:
  skill_slug: "funnel-map-visualizer"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "ab-test-generator"
```
