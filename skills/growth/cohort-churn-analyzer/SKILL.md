---
name: cohort-churn-analyzer
description: >
  Analyzes churn by signup cohort and segment using PostHog and subscription
  data to find which specific segment or onboarding path is failing, instead
  of reporting one blended churn number.
  Use this skill when the user asks about churn by cohort, retention curves,
  or says
  "why are users churning", "run a cohort analysis", "build our retention curve",
  "which segment churns the most", "find the churn drivers", "who's about to cancel".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "retention", "churn", "cohort", "posthog"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Cohort Churn Analyzer

This skill builds cohort retention curves segmented by plan, acquisition source, and activation status, using PostHog event data plus subscription records, to find exactly which segment or onboarding path is churning worst — and produces a ranked at-risk list, not just a churn percentage.

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The user has a blended churn number but no idea which segment is driving it
- The user wants to know if newer cohorts are retaining better or worse than older ones
- After aha-moment-mapper defines activation, to check whether activated users actually churn less (confirming the activation event was chosen correctly)
- The user wants a list of currently active users who look like they're about to churn
- Retention feels bad but the user can't point to when in the user's lifecycle it's happening

## Input Schema
```
posthog_project_id: string?
posthog_api_key: string?              # read-only, for event/usage data
subscription_export: string?          # description or path to billing data (signup date, plan, cancel date)
churn_definition: string?             # e.g. "30 days no login" or "explicit cancel event" — ask if not given
time_range: string?                   # defaults to "last 12 monthly cohorts"
segment_dimensions: array?            # e.g. ["plan", "acquisition_source", "company_size"]
activation_event: string?             # from aha-moment-mapper, if run
```

## Workflow
### Step 1: Build the Base Cohort Curve
Group users by signup month. For each cohort, compute % retained at week 1, 2, 4, 8, 12, 24 (pull login/usage events from PostHog, or subscription-active status from billing data, depending on the churn definition). Lay out the classic cohort triangle. Flag:
- **Cliff weeks**: any single week where retention drops more than ~15 percentage points — this is usually a specific, fixable moment (a locked feature, an onboarding gap, a billing surprise)
- **Flattening point**: the week the curve stabilizes — this is the product's real "sticky rate" and the number worth reporting on a dashboard
- **Cohort-over-cohort trend**: are newer signup cohorts retaining better or worse than older ones — this tells you whether recent product/onboarding changes are helping or hurting

### Step 2: Segment the Curve
Rebuild the same curve split by plan, acquisition source, activation status (activated vs. not, using the activation event), and company size if available. Find the segment split with the widest spread between its best- and worst-retaining group — that's where fixing effort has the most leverage, not necessarily the segment with the lowest absolute number.

### Step 3: Identify Churn Drivers
For churned users, compare pre-churn behavior against retained users on the same dimensions:
- Feature-usage difference (what do retained users touch that churners don't)
- Time-to-activation (did churners activate late or never — usually the single strongest driver)
- Support ticket volume before cancellation
- Last known NPS/CSAT score, if collected

Rank the top drivers by effect size and reach (a driver that explains a lot of churn but only applies to 3% of users is a smaller lever than one that applies to 30%).

### Step 4: Estimate Uplift, Honestly
For the top driver, give a rough estimate of what W12 retention would look like if every low-usage user were moved to high-usage of the relevant feature. Flag this explicitly as a directional estimate, not a guarantee — it's meant to prioritize effort, not to be quoted as a forecast.

### Step 5: Build the At-Risk Save List
Produce a ranked list of currently active users matching the churn-driver pattern: user/account ID, plan, last-active date, a 0-100 risk score, which driver(s) they match, and a recommended intervention. This is the list an intervention (an email, an in-app nudge, a manual outreach) actually gets sent against.

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] The base cohort curve is reported with step-to-step retention, not just one blended churn number
- [ ] At least one segmentation cut (plan, source, activation, size) is applied to find the widest spread
- [ ] Churn drivers are ranked by effect size and reach, not just listed
- [ ] The at-risk save list includes a specific recommended intervention per user/segment, not just a risk score
- [ ] Any uplift estimate is explicitly labeled as directional, not a firm forecast

## Output Schema
```json
{
  "cohort_curve": [
    {"cohort_month": "string", "w1": "number", "w4": "number", "w8": "number", "w12": "number", "w24": "number"}
  ],
  "cliff_weeks": ["string"],
  "flattening_point_week": "number",
  "cohort_trend": "improving|declining|flat",
  "widest_spread_segment": {"dimension": "string", "best_group": "string", "worst_group": "string", "spread_pp": "number"},
  "churn_drivers": [
    {"driver": "string", "effect_size": "string", "reach_pct": "number"}
  ],
  "at_risk_list": [
    {"user_id": "string", "plan": "string", "last_active": "string", "risk_score": "number", "matched_drivers": ["string"], "recommended_intervention": "string"}
  ]
}
```

## Output Format
```markdown
# Cohort & Churn Analysis — [time period]

## Retention Curve
| Cohort | W1 | W4 | W8 | W12 | W24 |
|---|---|---|---|---|---|
| [month] | [%] | [%] | [%] | [%] | [%] |

Cliff week(s): [week] — [likely cause]
Sticky rate (flattening point): [week] at [%]
Trend: [improving/declining/flat] cohort over cohort

## Widest Spread: [dimension]
[best group] retains at [%] vs [worst group] at [%] — [spread]pp gap

## Top Churn Drivers
| Driver | Effect Size | Reach |
|---|---|---|
| [driver] | [size] | [%] |

## At-Risk Save List (top 10)
| User | Plan | Last Active | Risk | Matched Driver | Intervention |
|---|---|---|---|---|---|
| [id] | [plan] | [date] | [score] | [driver] | [action] |

## Do Not
- Report a single blended churn number as the final answer
- Treat the uplift estimate as a guaranteed forecast
- Send the same intervention to every at-risk user regardless of which driver they match
```

## Error Handling
- Churn definition not specified → ask explicitly (inactivity threshold vs. explicit cancel event materially changes the numbers) before computing anything
- Fewer than ~10 cohorts or very small cohort sizes → warn that the curve will be noisy, widen the time window or combine cohorts
- No segmentation dimensions available (plan, source, etc. not tracked) → proceed with the base curve only, flag the missing dimensions as an instrumentation gap for future analysis
- Activation event not defined → skip the activation-status segmentation cut, note it as unavailable, recommend running aha-moment-mapper
- At-risk list would include very low-confidence risk scores (thin behavioral data) → mark those rows as low-confidence rather than omitting them silently

## Examples
**Example 1**
User: "Run a cohort analysis, I want to see if Pro retains better than Team, and what predicts churn."
Skill: Builds the base curve, segments by plan, finds Team retains 20pp worse by week 8, drills into churn drivers for Team specifically, and finds most Team churners never invited a second seat — flags "no team invite in first 14 days" as the top driver.

**Example 2**
User: "Our overall churn looks fine but I have a feeling something's off."
Skill: Segments by acquisition source and finds one channel's users retain far worse than the blended average, masked by a better-performing channel — recommends attribution-mapper cross-reference to see if that channel is worth its spend given the retention gap.

**Example 3**
User: "Give me a list of accounts likely to cancel this month."
Skill: Builds the save list from the top churn drivers, ranks by risk score, and recommends a specific intervention per matched driver (e.g. re-onboarding nudge for never-activated users, a check-in call for high-usage-then-sudden-drop accounts).

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- trial-to-paid-converter
- growth-dashboard-builder
- onboarding-flow-builder

### Fed By
- aha-moment-mapper
- signup-conversion-tracker

### Feedback Loop
Re-run the cohort curve monthly; after an onboarding or activation fix ships, check whether the newest cohort's retention curve improved relative to the cohort immediately before it, not just whether the aggregate churn number moved.

```yaml
chain_metadata:
  skill_slug: "cohort-churn-analyzer"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "trial-to-paid-converter"
    - "growth-dashboard-builder"
```
