---
name: funnel-map-visualizer
description: >
  Turns a planned or live funnel into one visual map showing every step, the
  page/copy at each step, and (once tracking exists) real conversion numbers
  per step — saved as a local HTML file in the project folder instead of
  scattered SKILL.md workflow output.
  Use this skill when the user asks about "show me the whole funnel", "I want to see
  this visually", or says
  "map out my funnel visually", "show me the funnel as a diagram", "I can't picture
  how these pages connect", "where are people dropping off in this funnel",
  "give me a visual overview of the funnel", "show conversion rate at each step",
  "I want to see the whole customer journey in one place".
license: MIT
version: "2.0.0"
tags: ["saas", "funnel", "visual", "tracking", "conversion", "local-file"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "2.0"
  stage: S3-Funnel-Build
---

# Funnel Map Visualizer

Takes the output of `funnel-select` and `funnel-builder-orchestrator` (whichever funnel type was built — Webinar, Tripwire, Free Trial/SaaS, etc.) and renders the whole funnel as one visual map — every step in order, what page/email/ad lives at each step, and once real traffic exists, the actual conversion rate between each step. This exists because a funnel described across several SKILL.md workflows is hard to hold in your head; a founder needs to see the whole path in one place to know where it's actually leaking.

**Follows `shared/references/output-conventions.md`: writes into the brand's single consolidated `hub.html` (Funnel Map section) — never its own separate page — and passes through `impeccable` before being called done.**

## Stage
This skill belongs to Stage S3: Funnel Build

## When to Use
- After `funnel-select` has picked a funnel type and the founder wants to see the whole thing laid out, not just read the steps
- Before building, to sanity-check the funnel makes sense end to end
- After launch, once `signup-conversion-tracker` or PostHog funnel data exists, to see real drop-off per step overlaid on the map
- The founder can't picture how the landing page, emails, and checkout connect

## Input Schema
```
{
  funnel_type: string          # from funnel-select, e.g. "Low-Ticket / Tripwire", "Webinar"
  steps: object[]              # ordered list: { name, type (page/email/ad/checkout), copy_summary }
  live_data: object            # (optional) per-step visitor/conversion counts, from PostHog or signup-conversion-tracker
  update_mode: string          # "create" | "update"
}
```

## Workflow

### Step 1: Gather the Funnel Structure
Pull the step sequence from `funnel-builder-orchestrator`'s output for the chosen type (e.g. Low-Ticket/Tripwire: landing page → order bump → one-time-offer → thank-you/upsell). Confirm the order and what lives at each step (page, email, ad) before building anything.

### Step 2: Set Up the Brand Folder and Find the Shared Hub
Confirm the brand/business name first if not already known — the root is the brand name alone, never the offer name. **Check whether `[BrandName]/hub.html` and `hub-data.json` already exist** (likely, since `funnel-builder-orchestrator` or `research-report-builder` probably ran first) — read them and update the Funnel Map section rather than creating a competing page. If no hub exists yet, create it with all 7 sections, marking everything but Funnel Map as "not started yet."

### Step 3: Decide on Live Data
If the founder has PostHog connected and real traffic, this map should show real numbers (visitors in, converted, drop-off %) at each step — pull that via the PostHog MCP tools referenced in `growth-dashboard-builder` and `checkout-funnel-auditor`. If no live data yet, show the planned structure only and label it clearly as "not yet live" rather than inventing numbers.

### Step 4: Write the Funnel Map Data and Regenerate the Hub
Update the Funnel Map section of `hub-data.json`: steps, types, copy summaries, live numbers if any. Structure within the section:
- A left-to-right (or top-to-bottom on mobile) flow of steps, each step as a card showing step name, type (page/email/ad), one-line copy summary
- If live: visitor count in, % who moved to the next step, biggest visual weight given to the step with the worst drop-off (so the eye goes straight to the problem)

Regenerate the *entire* `hub.html` from `hub-data.json`, not just this section in isolation.

### Step 5: Run `impeccable`, Save, and Tell the User
Before saving, load and apply the `impeccable` skill (fall back to `taste-skill`) to `hub.html`. Then write it to the brand folder and give the founder the exact path — `[BrandName]/hub.html` — to open in their browser.

### Step 6: Highlight the Biggest Leak
If live data exists, explicitly call out which single step has the worst drop-off — that's the one `checkout-funnel-auditor` or `ab-test-generator` should be pointed at next, not a vague "optimize everything" note. If this is a genuinely new finding, append it to the hub's Decisions Log.

### Step 7: Self-Validation
- [ ] Every step from the chosen funnel type appears in order
- [ ] Each step shows what actually lives there (page/email/ad), not just a generic label
- [ ] Live data is only shown if real, never fabricated to look complete
- [ ] The worst-performing step (if data exists) is visually obvious, not buried
- [ ] `impeccable` (or `taste-skill`) was applied before saving
- [ ] The founder was given the exact local hub path, not a link

## Output Schema
```
{
  brand_folder: string
  hub_html_path: string
  funnel_type: string
  step_count: number
  has_live_data: boolean
  worst_dropoff_step: string
}
```

## Output Format
```
## Funnel Map Updated

**[Brand Name] — [Funnel Type] Funnel Map** — [BrandName]/hub.html (Funnel Map section)

Open the hub in your browser (double-click the file, or drag it into a tab)
and jump to the Funnel Map section.

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
- **Updating an existing map with new live data:** Read the existing `hub-data.json`, refresh only the Funnel Map section, regenerate the full `hub.html` — don't recreate the brand folder from scratch.

## Examples

**Example 1:**
User: "I picked the tripwire funnel, can you show me what it actually looks like end to end?"
→ Pull the 4-step structure from the Tripwire-type build's output
→ Find or create the brand folder and hub, write the Funnel Map section into `hub-data.json`, regenerate `hub.html` through `impeccable`, labeled as planned (no live data yet)
→ Give the founder the exact hub path

**Example 2:**
User: "where is my funnel actually leaking?"
→ Confirm PostHog is connected, pull step-by-step conversion data via checkout-funnel-auditor's data source
→ Overlay real numbers on the existing map, highlight the worst step
→ Recommend ab-test-generator or checkout-funnel-auditor as the next skill to run on that specific step

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `shared/references/output-conventions.md`

## Flywheel Connections
### Feeds Into
- checkout-funnel-auditor (S10-Growth) — the worst-performing step this map surfaces is exactly what that skill should audit next
- ab-test-generator (S10-Growth) — once a leak is identified, test a fix at that specific step

### Fed By
- funnel-select (S3-Funnel-Build) — supplies the chosen funnel type and step structure
- signup-conversion-tracker (S10-Growth) / growth-dashboard-builder (S10-Growth) — supply the live per-step numbers once traffic exists

### Feedback Loop
- Each time this map is refreshed with new live data, the trend in where the worst leak sits over time tells `self-improver` whether past fixes actually worked.

```yaml
chain_metadata:
  skill_slug: "funnel-map-visualizer"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "ab-test-generator"
```
