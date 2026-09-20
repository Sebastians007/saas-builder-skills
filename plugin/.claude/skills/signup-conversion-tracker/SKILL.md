---
name: signup-conversion-tracker
description: >
  Sets up and interprets a signup and activation funnel (visit to signup to
  first key action to paid) to find the single biggest drop-off point to fix
  first, instead of guessing which step is broken.
  Use this skill when the user asks about funnel drop-off, activation rates,
  or why signups aren't converting to paid, or says
  "why aren't people signing up", "people sign up but never use the app", "where are we losing users",
  "what's my activation rate", "build me a signup funnel", "why is trial to paid so low",
  "track my conversion funnel", "which step should I fix first".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "funnel", "activation", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
---

# Signup Conversion Tracker

This skill builds the visit-to-signup-to-activation-to-paid funnel for a live SaaS app, finds the single stage losing the most people, and tells the founder exactly one thing to fix first instead of a list of ten. It replaces "conversion feels low" with a specific number at a specific step.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- The user has real signup and usage data but hasn't organized it into a funnel
- People are signing up but not using the app ("activation" problem)
- Trial-to-paid conversion feels low but the user doesn't know why
- The user wants to know where to spend the next week of effort
- After running an ab-test-generator experiment, to see whether the fix actually moved the funnel stage it targeted
- The user's Execution Squad outreach sprint is generating leads/replies but they're not converting once inside the app

## Input Schema
```
funnel_stages: array?            # defaults to: visit, signup, first_key_action, paid
first_key_action_definition: string?  # e.g. "created first project", "sent first email"
stage_counts: {                  # numbers for a given period
  visit: number?,
  signup: number?,
  first_key_action: number?,
  paid: number?
}
time_period: string?             # e.g. "last 30 days"
known_pain_point: string?        # if the user already suspects a stage
```

## Workflow
### Step 1: Define the Funnel Stages
Default funnel: Visit → Signup → First Key Action (activation) → Paid. Confirm "first key action" is defined as the ONE thing that predicts a user will get value (not just "logged in" — something that proves they used the core feature, e.g. "created a project," "sent a campaign," "connected an account"). If the user doesn't know their activation moment, help them define it: ask what the app's core value is and what action proves a user reached it.

### Step 2: Collect Stage Counts
Ask for actual numbers per stage for a fixed period (30 days is a good default — long enough to smooth noise, short enough to act on). If the user doesn't have analytics set up, tell them plainly what to instrument (pageview count, signup count, an event fired at the key action, and paid conversion count) rather than making up numbers.

### Step 3: Calculate Conversion Rate at Each Step
Compute step-to-step conversion (not just funnel-wide conversion), since a single bad step hides inside an overall number:
- Visit → Signup rate
- Signup → First Key Action rate (activation rate)
- First Key Action → Paid rate

### Step 4: Identify the Single Biggest Drop-off
Compare each step's conversion rate against typical SaaS benchmarks (rough guide, self-serve B2B SaaS):
- Visit → Signup: 2-5% is normal, under 1% is a landing page/targeting problem
- Signup → Activation: 30-50% is normal, under 20% is an onboarding problem
- Activation → Paid: 15-30% is normal for freemium/trial models, under 10% is a value or pricing problem

Rank the steps by how far below benchmark they are (in relative terms, not absolute count) and name ONE step as the priority. Resist the urge to hand back three "areas of improvement" — pick one.

### Step 5: Give One Fix Recommendation, Not a List
Based on which step is worst, name the matching downstream skill and one concrete first action (e.g. if Signup→Activation is broken, point to in-app-nav-optimizer or onboarding-flow-builder; if Visit→Signup is broken, point to marketing-site-seo-audit or unique-value-prop-audit).

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Funnel has step-to-step rates, not just an overall visit-to-paid rate
- [ ] Exactly one stage is named as the priority
- [ ] The priority pick is justified against a benchmark, not a hunch
- [ ] A concrete next action (and which skill handles it) is named
- [ ] If data is missing, the skill says what to instrument rather than inventing numbers

## Output Schema
```json
{
  "time_period": "string",
  "funnel": [
    {"stage": "string", "count": "number", "conversion_from_previous": "string|null", "benchmark": "string", "status": "healthy|below_benchmark|critical"}
  ],
  "biggest_drop_off_stage": "string",
  "why_this_stage": "string",
  "recommended_next_skill": "string",
  "recommended_first_action": "string"
}
```

## Output Format
```markdown
# Signup Funnel Report — [time period]

## Funnel
| Stage | Count | Conversion from previous | Benchmark | Status |
|---|---|---|---|---|
| Visit | [n] | — | — | — |
| Signup | [n] | [x]% | 2-5% | [status] |
| First Key Action | [n] | [x]% | 30-50% | [status] |
| Paid | [n] | [x]% | 15-30% | [status] |

## Biggest Drop-off: [stage name]
[One paragraph: how far below benchmark, what it likely means]

## Fix This First
[One concrete action]
Recommended next skill: [skill-slug]

## Do Not
- Try to fix all three stages this week
- Compare your funnel to a different business model's benchmarks
- Trust this data if fewer than ~50 people passed through the top of the funnel this period (too small to be reliable)
```

## Error Handling
- No stage counts provided → ask for them; if truly unavailable, explain the minimum instrumentation needed (a pageview counter, a signup event, one activation event, one paid event) and stop rather than fabricate numbers
- Sample size too small (under ~50 signups in the period) → warn that the funnel rates are noisy and shouldn't drive a big decision yet; suggest widening the time window
- "First key action" undefined → walk the user through picking one based on the app's core value, don't guess silently
- User wants to blame a stage that isn't actually the worst by the numbers → show the math and let the numbers, not the user's hunch, pick the priority
- Multiple stages tied for worst → break the tie by which stage has more absolute users passing through it (fixing the earlier, higher-volume stage usually has bigger impact)

## Examples
**Example 1**
User: "People sign up but never really use the app, what's going on?"
Skill: Defines the activation event with the user, asks for signup and activation counts over 30 days, finds Signup→Activation at 12% against a 30-50% benchmark, names it the priority, and points to onboarding-flow-builder as the fix.

**Example 2**
User: "Trial to paid is like 5%, is that bad?"
Skill: Confirms it against the 15-30% benchmark, flags it as critical, asks whether activation rate is healthy first (a low trial-to-paid rate is often really an upstream activation problem in disguise), and traces back to the true root cause before recommending a pricing or value-prop fix.

**Example 3**
User: "My cold outreach is getting replies but nobody who books a call ends up as a paying user."
Skill: Notes this sits downstream of the Execution Squad sprint's booked-call step, builds the in-app portion of the funnel (signup → activation → paid) for people coming from those calls specifically, and isolates whether the leak is in-app (activation) or in the sales conversation itself.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- in-app-nav-optimizer (S7-Growth)
- ab-test-generator (S7-Growth)
- onboarding-flow-builder (S3-Building)
- pricing-model-calculator (S1-Research)

### Fed By
- ab-test-generator (S7-Growth)
- monitoring-alerting-setup (S6-Operations)

### Feedback Loop
Each time a fix ships (onboarding change, nav fix, pricing test), re-run this funnel on the same stage definitions to confirm the drop-off actually moved before declaring victory and picking the next priority stage.

```yaml
chain_metadata:
  skill_slug: "signup-conversion-tracker"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "in-app-nav-optimizer"
    - "ab-test-generator"
```
