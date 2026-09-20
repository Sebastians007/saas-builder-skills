---
name: funnel-planner
description: >
  Plans the end-to-end signup, activation, and retention funnel for a SaaS app and maps
  which specific pack skills should be used at each funnel stage, so growth work isn't
  scattered across ad-hoc tactics with no throughline.
  Use this skill when the user asks "what's our signup funnel look like", "plan our
  onboarding to retention path", "how do we get people from signup to paying", "map out
  our activation flow", "why are people signing up and not sticking around", "what skills
  do we need for growth", or "build the whole funnel, not just one piece".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "funnel", "activation", "retention", "growth"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Meta
---

# Funnel Planner

Maps the full signup-to-retained-customer funnel for a SaaS app and assigns the right pack skill to each stage, so growth and onboarding work happens in the right order instead of jumping straight to ads or a redesign without knowing where users are actually dropping off. This is the skill that turns "we need more users" into a stage-by-stage plan with owners.

## Stage
This skill belongs to Stage S8: Meta

## When to Use
- Before launch, to design the funnel intentionally instead of bolting pieces together after the fact
- Signups are happening but activation or retention is weak and the founder doesn't know which stage is broken
- The founder has used individual growth skills (onboarding-flow-builder, signup-conversion-tracker) in isolation and wants them connected into one plan
- Planning a specific growth sprint and needing to know which skill to invoke first
- After a `self-improver` retrospective flags that funnel work was done out of order last time

## Input Schema
```
funnel_planning_request:
  app_name: string
  current_funnel_stage: string      # "pre-launch" | "has signups, low activation" | "has activation, low retention" | "established, optimizing"
  known_metrics: {
    signups_per_week: int | null,
    activation_rate: float | null,   # % who reach "aha moment"
    week1_retention: float | null,
    paid_conversion: float | null
  }
  primary_bottleneck_guess: string  # founder's hunch, may be wrong
  existing_skills_used: [string]    # optional, which pack skills already applied
```

## Workflow
### Step 1: Define the Funnel Stages for This App
Lay out the specific funnel for this app in plain terms: Visitor → Signup → First Value ("aha moment") → Habit/Repeat Use → Paid Conversion → Retained Customer. Name what the "aha moment" actually is for this specific app — don't use a generic template.

### Step 2: Locate the Actual Bottleneck
Using `known_metrics`, identify which stage is leaking the most, not just where the founder's hunch points. If metrics aren't available, recommend instrumenting first (`signup-conversion-tracker`, S7-Growth) before optimizing blind.

### Step 3: Assign a Skill to Each Stage
Map the funnel to specific pack skills:
- **Visitor → Signup**: `unique-value-prop-audit` (S1), `marketing-site-seo-audit` (S7), `ab-test-generator` (S7) on the landing page
- **Signup → First Value**: `onboarding-flow-builder` (S3), `auth-flow-builder` (S3) if friction is in signup itself
- **First Value → Habit**: `in-app-nav-optimizer` (S7), `seed-data-generator` (S6) if empty-state is killing early use
- **Habit → Paid**: `pricing-model-calculator` (S1), `signup-conversion-tracker` (S7)
- **Paid → Retained**: `app-performance-report` (S7), `monitoring-alerting-setup` (S6) to catch churn-causing bugs early

### Step 4: Sequence the Work
Order the recommended skills by where the bottleneck actually is, not funnel order — fixing the top of the funnel when activation is the leak wastes effort. State explicitly: "fix stage X before touching stage Y."

### Step 5: Set Success Thresholds Per Stage
For each funnel stage being worked on, define what "good" looks like numerically (e.g. activation rate target, week-1 retention target) so it's clear when to move attention to the next stage.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Is the "aha moment" specific to this app, not generic?
- [ ] Does the bottleneck identification use real metrics where available, not just the founder's hunch?
- [ ] Is every funnel stage mapped to an actual existing skill slug, not a vague suggestion?
- [ ] Is there a clear sequence (what to fix first), not a flat list?
- [ ] Are success thresholds numeric and stage-specific?

## Output Schema
```
{
  "app_name": string,
  "funnel_stages": [
    {"stage": string, "aha_moment_or_goal": string, "current_metric": float | null, "target_metric": float | null}
  ],
  "bottleneck_stage": string,
  "skill_sequence": [{"order": int, "skill_slug": string, "stage": string, "why_now": string}],
  "instrumentation_gap": bool
}
```

## Output Format
```markdown
# Funnel Plan — <App Name>

## The Funnel
Visitor → Signup → First Value → Habit → Paid → Retained

| Stage | What "good" looks like here | Current | Target |
|---|---|---|---|
| ... | ... | ... | ... |

## Bottleneck
**<stage>** — <why this is the leak, based on data or reasoning>

## Skill Sequence (do these in order)
1. `<skill-slug>` (Stage) — <why this one first>
2. `<skill-slug>` (Stage) — <why next>
...

## If You Don't Have Metrics Yet
<instrumentation recommendation before optimizing blind>

## Review Cadence
<when to re-run this planner, e.g. "after 2 weeks of the fix, re-check activation rate">
```

## Error Handling
- No metrics available at all: don't guess the bottleneck — recommend `signup-conversion-tracker` first to get baseline numbers, and mark the plan as provisional.
- Founder's bottleneck hunch conflicts with the data: state the conflict directly, trust the data, explain why (e.g. "you think it's pricing but signups never activate, so pricing doesn't matter yet").
- Pre-launch app with zero funnel data: skip metric-based diagnosis, build the funnel plan around the design of the onboarding/activation flow instead, using `onboarding-flow-builder` and `mvp-feature-slicer` (S2) as the starting points.
- Multiple stages look equally broken: recommend fixing the earliest broken stage first — a leak downstream can't be diagnosed accurately while the upstream leak is still masking real volume.
- Founder asks for funnel plan but has no defined "aha moment": don't skip past this — force a concrete answer before proceeding, since every downstream recommendation depends on it.

## Examples
**Example 1**
User: "We get 50 signups a week but almost nobody comes back after day 1. What do we fix?"
The skill identifies this as a First Value → Habit leak, not a signup problem, and sequences `onboarding-flow-builder` and `seed-data-generator` (to kill empty-state confusion) ahead of any acquisition work.
Outcome: founder gets a 2-step plan instead of spending on more ads.

**Example 2**
User: "Pre-launch, haven't built onboarding yet. Plan the whole funnel for us."
The skill lays out the full 6-stage funnel with app-specific "aha moment" definition, and sequences `mvp-feature-slicer` → `onboarding-flow-builder` → `unique-value-prop-audit` → `signup-conversion-tracker` as the build order.
Outcome: founder has a stage-by-stage roadmap tied to specific skills before writing any growth copy.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `onboarding-flow-builder` (S3-Building) — primary skill for the activation-stage fix
- `signup-conversion-tracker` (S7-Growth) — instrumentation needed to validate the plan
- `ab-test-generator` (S7-Growth) — used to test funnel-stage fixes once identified
- `in-app-nav-optimizer` (S7-Growth) — habit-stage fixes route here

### Fed By
- `mvp-feature-slicer` (S2-Planning) — defines what "first value" even is, pre-launch
- `unique-value-prop-audit` (S1-Research) — informs what should be promised at the top of the funnel

### Feedback Loop
Each funnel plan's actual results (did the sequenced fix move the metric) get logged, so `self-improver` can flag when a stage was misdiagnosed and sharpen the bottleneck-detection logic for next time.

```yaml
chain_metadata:
  skill_slug: "funnel-planner"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "onboarding-flow-builder"
    - "signup-conversion-tracker"
```
