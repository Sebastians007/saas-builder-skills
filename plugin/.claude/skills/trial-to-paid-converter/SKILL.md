---
name: trial-to-paid-converter
description: >
  Designs the trial-to-paid conversion sequence for a SaaS product — in-app
  prompts, emails, and timing — personalized to what each trial user has
  actually done, instead of one generic "your trial is ending" blast.
  Use this skill when the user asks about trial conversion, what to email
  trial users, or says
  "increase trial to paid conversion", "what should I send trialists", "redesign our trial flow",
  "trial conversion is low", "people sign up for the trial but never upgrade", "we're launching a free trial, help design it".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "trial", "conversion", "revenue", "lifecycle"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Trial-to-Paid Converter

This skill designs the full in-trial experience — in-app nudges and emails, segmented by what the user has actually done, timed against the trial countdown. It replaces one generic "your trial ends in 3 days" email with a playbook that treats an activated power user completely differently from someone who never logged in twice.

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The user is launching a new free trial and needs the in-trial experience designed from scratch
- Trial-to-paid conversion is known and feels low, but there's no segmented plan for different user behavior
- The user wants to know what to actually email trial users beyond a countdown reminder
- After aha-moment-mapper defines the activation event, to build the conversion sequence around it
- The user is sending the same message to everyone in the trial regardless of usage level

## Input Schema
```
trial_length_days: number             # required, e.g. 7, 14, 30
trial_type: string?                   # "card_required" | "reverse_trial" | "freemium_time_locked", ask if unknown
activation_event: string?             # from aha-moment-mapper, e.g. "created first project"
current_trial_to_paid_rate: number?
feature_access: object?               # what's locked in trial vs paid
posthog_available: boolean?           # whether usage data can drive segmentation
```

## Workflow
### Step 1: Confirm the Trial Archetype
Three options, each with a tradeoff — pick one deliberately, don't default without asking:
- **Opt-in, card required**: highest eventual conversion rate, lowest signup volume (friction filters out non-serious signups upfront)
- **Reverse trial**: full product access for the trial period, then downgrades to a free tier — good when the value is only obvious with full feature access
- **Freemium with time-locked features**: lowest signup friction, hardest to convert (nothing forces a decision)

Recommend one based on the ICP and price point (higher-priced B2B tools lean toward card-required; low-price/high-volume tools lean toward freemium).

### Step 2: Segment Trial Users by Actual Usage
At each check-in point (day 1, day 3, day 7, trial-end), classify every trial user into one of four segments based on real behavior, not time-in-trial alone:

| Segment | Signal | Message angle |
|---|---|---|
| Activated | Hit the activation event | Show what advanced users do next |
| Trying | Some activity, hasn't hit activation | One specific nudge toward the activation event |
| Ghost | Signed up, no meaningful activity | A reactivation hook, or accept the loss and stop emailing |
| Power | Usage well above typical | Early upgrade nudge; a personal outreach if the account is high-value |

If PostHog is available, pull these segments from real event data rather than guessing.

### Step 3: Design the Day-by-Day Sequence
For each segment, specify per touchpoint: the in-app element (banner, checklist, modal, tooltip) and the email (subject + one-line body direction + CTA). Anchor the critical beats to the trial calendar, not arbitrary days:
- **Day 0**: welcome message + a checklist pointing straight at the activation event
- **The day activation happens**: a "here's what's possible next" message — this is the single highest-leverage moment in the whole sequence
- **1-2 days before trial ends**: recap of value delivered (usage stats if available) + a clear upgrade CTA with the actual price shown
- **Trial-end day**: direct upgrade prompt + an easy path to a short extension if requested (better to extend than lose someone who's still engaged)
- **The day after trial ends**: one final value-recap email with an offer; then stop — repeated urgency past this point reads as spam, not persuasion

### Step 4: Handle Price Anchoring Without Overdoing It
Show the plan they'd be on, the annual savings if relevant, and specifically which features they used that they'd lose without upgrading. State loss-aversion framing once, clearly — not across every touchpoint, which trains the user to tune it out.

### Step 5: Set the Success Metric and Guardrails
Primary metric: trial-to-paid rate, tracked by segment (an aggregate rate hides whether the activated segment is converting well while ghosts drag the average down). Guardrails: unsubscribe rate around trial-end messaging, and post-trial NPS or support ticket volume (a sequence that converts through pressure rather than value shows up here first).

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] A trial archetype is explicitly chosen with a stated tradeoff, not defaulted silently
- [ ] All four usage segments have distinct messaging, not one sequence for everyone
- [ ] The activation-event-hit moment has its own dedicated message, separate from the generic day-0 welcome
- [ ] Trial-end messaging escalates urgency at most once, with a hard stop after trial-end+1
- [ ] Guardrail metrics (unsubscribe, NPS) are specified alongside the primary conversion metric

## Output Schema
```json
{
  "trial_archetype": "opt_in_card_required|reverse_trial|freemium_time_locked",
  "archetype_rationale": "string",
  "segments": [
    {"segment": "activated|trying|ghost|power", "signal": "string", "message_angle": "string"}
  ],
  "sequence": [
    {"day": "string", "segment": "string", "in_app": "string", "email_subject": "string", "email_direction": "string", "cta": "string"}
  ],
  "success_metric": "string",
  "guardrails": ["string"]
}
```

## Output Format
```markdown
# Trial-to-Paid Conversion Playbook

## Archetype: [name]
Rationale: [why this fits the ICP/price point]

## Segments
| Segment | Signal | Message Angle |
|---|---|---|
| Activated | [signal] | [angle] |
| Trying | [signal] | [angle] |
| Ghost | [signal] | [angle] |
| Power | [signal] | [angle] |

## Day-by-Day Sequence
### Day [X] — [segment]
**In-app:** [element]
**Email:** [subject] — [direction] — CTA: [cta]

## Success Metric
Primary: [trial-to-paid rate by segment]
Guardrails: [unsubscribe rate, NPS]

## Do Not
- Send the same message to activated and ghost users
- Escalate urgency more than once in the final 48 hours
- Keep emailing past trial-end+1 day with no response
```

## Error Handling
- Activation event not defined → hand off to aha-moment-mapper first; the sequence can't be properly segmented without it
- No usage/event data available to segment by → fall back to time-based segmentation (day 1/3/7 check-ins) but flag it as weaker than behavior-based segmentation and recommend instrumenting PostHog events
- Trial archetype forced by existing product decisions the user can't change → work within it, note the tradeoff honestly rather than recommending a switch that isn't feasible
- User wants to skip straight to aggressive discounting at trial-end → push back; recommend testing value-recap messaging first since deep discounts train users to wait for them on every renewal
- Very short trial (under 5 days) → compress the sequence, drop the mid-trial checkpoint, focus almost entirely on getting to the activation event fast

## Examples
**Example 1**
User: "14-day trial, card required, 18% conversion. ICP is RevOps at 50-500 person companies. Activation is 'connect a data source AND build a first report.'"
Skill: Builds the full day-0 through day-15 sequence per segment, with a dedicated "you just built your first report" in-app moment right after activation, and a power-user segment triggering a manual outreach touch for accounts above an ARR threshold.

**Example 2**
User: "We're launching our first trial ever, 7 days, freemium with locked features."
Skill: Recommends confirming freemium is the right call given it converts hardest, designs a compressed 7-day sequence focused entirely on reaching activation by day 2-3, and flags that this archetype will need a longer nurture beyond trial-end since freemium users rarely decide on day 7.

**Example 3**
User: "Ghosts never open our emails, should we keep sending them?"
Skill: Recommends capping ghost-segment emails at 2 touches (day 1 nudge, trial-end recap) and redirecting the effort toward improving the day-0 activation nudge instead, since a ghost segment that never engages is an activation problem in disguise, not an email-copy problem.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- onboarding-flow-builder
- ab-test-generator
- revenue-dashboard-builder

### Fed By
- aha-moment-mapper
- cohort-churn-analyzer

### Feedback Loop
Track trial-to-paid rate by segment in revenue-dashboard-builder after the sequence ships; if the activated segment still converts below benchmark, the problem has moved from trial messaging to pricing or checkout friction — hand off to pricing-page-optimizer or checkout-funnel-auditor next.

```yaml
chain_metadata:
  skill_slug: "trial-to-paid-converter"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "revenue-dashboard-builder"
```
