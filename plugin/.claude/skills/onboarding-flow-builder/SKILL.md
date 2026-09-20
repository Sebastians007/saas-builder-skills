---
name: onboarding-flow-builder
description: >
  Design a first-run onboarding flow — empty states, setup wizard, and the first
  successful action — so new users reach real value fast.
  Use this skill when the user asks about improving first-time user experience,
  reducing signup drop-off, or says
  "what should happen right after someone signs up", "design my onboarding flow",
  "users sign up but don't do anything after", "what should the empty state say",
  "help new users get to their first win faster", "design a setup wizard",
  "people churn right after signup", "what's the first thing a new user should see".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "onboarding", "activation", "ux"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# Onboarding Flow Builder

Designs the sequence of screens and actions a brand-new user goes through from signup to their first real win inside the product — what empty states say, what the setup wizard asks for, and exactly what "success" looks like on day one. Most SaaS churn happens in the first session; this skill builds the path to value on purpose instead of leaving new users to figure it out.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- Right after auth-flow-builder, before the app has any post-signup experience defined
- Users are signing up but not activating (never do the core action)
- The app currently dumps new users onto a blank dashboard with no guidance
- Adding a new major feature that needs its own mini first-run experience
- Reviewing/improving an existing onboarding flow that's losing users
- Before a launch, to make sure the first 5 minutes of the product actually works

## Input Schema
```
app_description: string         # what the product does
core_value_action: string       # the one action that proves the product's value to a new user
existing_flow: string?          # what currently happens after signup, if anything
target_user: string?            # who's signing up (technical/non-technical, solo/team)
```

## Workflow
### Step 1: Name the "aha moment"
State the single action that proves value to a brand-new user (e.g. "sent their first campaign," "saw their first report," "invited their first teammate"). If core_value_action isn't given, infer it from app_description and confirm it's specific, not vague ("understand the product" is not an aha moment).

### Step 2: Map the shortest path to it
List the minimum steps between "just signed up" and the aha moment. Cut anything not strictly necessary to reach it — no settings tours, no "customize your profile" detours before first value.

### Step 3: Design empty states
For every screen a new user sees before they have data, write the exact empty-state copy: what's missing, why it matters, and the one button/action to fix it. Never leave a blank screen with no next step.

### Step 4: Design the setup wizard (if needed)
Only include a wizard step if it's truly required before the core action can happen (e.g. connecting a data source). Each wizard step needs: what it asks for, why (one sentence, user-facing), and what happens if skipped (if skip is allowed).

### Step 5: Define the success moment
Describe what the user sees/feels the instant they complete the core value action — confirmation, a visible result, an obvious next step. This is the payoff; make it visible, not buried in a toast notification.

### Step 6: Define drop-off recovery
For each step, note what happens if the user abandons (does nothing for X time) — email nudge content angle, or nothing if not warranted yet.

### Step 7: Self-Validation
Before presenting, silently confirm:
- [ ] The aha moment is one specific, provable action
- [ ] No unnecessary step sits between signup and the aha moment
- [ ] Every empty state has copy and a next action, none left blank
- [ ] Wizard steps (if any) are justified as strictly required
- [ ] The success moment is visible and specific, not generic ("Welcome!")

## Output Schema
```json
{
  "aha_moment": "string",
  "path_steps": [
    {"step": "string", "screen": "string", "required": "boolean"}
  ],
  "empty_states": [
    {"screen": "string", "copy": "string", "cta": "string"}
  ],
  "wizard_steps": [
    {"asks_for": "string", "why": "string", "skippable": "boolean"}
  ],
  "success_moment": "string",
  "dropoff_recovery": [
    {"step": "string", "trigger": "string", "action": "string"}
  ]
}
```

## Output Format
```markdown
# Onboarding Flow: <App Name>

**Aha moment:** <the one action that proves value>

## Path from signup to aha moment
1. <step> — <screen/action>
2. <step> — <screen/action>
3. Aha moment reached

## Empty states
### <screen name>
- Copy: "<exact copy>"
- CTA: "<button text>" -> <what it does>

## Setup wizard
### Step 1: <ask>
- Why: <one sentence, user-facing>
- Skippable: <yes/no>

## Success moment
<what the user sees/feels right when they hit the aha moment>

## Drop-off recovery
| Step | If abandoned | Action |
|---|---|---|
| ... | ... | ... |
```

## Error Handling
- If core_value_action isn't clear from the input, infer the most likely candidate from app_description and state it as an assumption for the user to confirm, rather than blocking.
- If the existing flow already reaches the aha moment but too slowly, focus the redesign on cutting steps rather than rebuilding from zero — respect blank-slate-only-when-asked; if the user just wants incremental fixes, don't propose a full rebuild.
- If the app requires data/integration before any value is visible (e.g. needs a data source connected first), be honest that the wizard step is unavoidable and focus effort on making that step painless (progress indicator, clear reason).
- If this is being designed before auth-flow-builder has run, note that signup/login must exist first, but proceed with the onboarding design assuming standard auth completes normally.
- If the target_user is a team/multi-seat product, clarify whether onboarding is for the first admin only or also invited members — these need separate flows, don't conflate them.

## Examples

**Example 1**
User: "Users sign up for my invoicing app but most never send an invoice. What should happen after signup?"
Skill does: names aha moment as "sent first invoice," cuts profile-setup detour, designs empty dashboard state with "Create your first invoice" CTA, 2-step wizard (add one client, add one line item) marked required since invoice needs both, success moment shows the sent invoice with a "nice, that's invoice #1" confirmation.
Outcome: clear, short path replaces a vague "explore the dashboard" experience.

**Example 2**
User: "Adding a new 'reports' feature — what should new users see the first time they open it?"
Skill does: treats this as a mini onboarding for one feature, aha moment = "viewed their first generated report," empty state explains what reports need (at least one week of data) with CTA to check back or import historical data, no separate wizard needed since setup already happened elsewhere in the app.
Outcome: feature-specific onboarding instead of reusing app-wide onboarding awkwardly.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- ui-component-builder (S6-Building)
- signup-conversion-tracker (S10-Growth)
- user-acceptance-test-planner (S7-Testing)

### Fed By
- auth-flow-builder (S6-Building)
- mvp-feature-slicer (S5-Planning)

### Feedback Loop
When signup-conversion-tracker shows where users actually drop off, feed that data back into this skill to re-cut the path and rewrite empty states at the real friction point.

```yaml
chain_metadata:
  skill_slug: "onboarding-flow-builder"
  stage: "building"
  timestamp: string
  suggested_next:
    - "ui-component-builder"
    - "signup-conversion-tracker"
    - "user-acceptance-test-planner"
```
