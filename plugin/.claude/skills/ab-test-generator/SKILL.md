---
name: ab-test-generator
description: >
  Designs a proper A/B test for a specific app element (pricing page, onboarding
  step, CTA button, email subject line) with a locked hypothesis, one success
  metric, and the minimum sample size needed before anyone is allowed to call
  a result significant.
  Use this skill when the user asks about testing a pricing page, onboarding
  flow, or CTA change, or says
  "should I A/B test this", "how many signups do I need before I know if this works",
  "I want to test two versions of my pricing page", "is this result actually significant",
  "help me set up an experiment on my landing page", "we changed the CTA, how do we know if it worked",
  "what sample size do I need", "design a test for this onboarding change".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "experimentation", "conversion", "statistics"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
---

# A/B Test Generator

This skill turns a vague "let's test this" idea into a real experiment with a locked hypothesis, one metric, a required sample size, and a stop date decided before the test starts. It exists to stop founders from eyeballing small-sample results and calling a coin flip a win.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- The user wants to test two versions of a pricing page, onboarding step, CTA, or email
- The user already ran a test and is asking whether the result is "real"
- The user keeps changing things based on gut feel and needs a forcing function
- The user's outreach experiment (Execution Squad sprint) needs a matching in-app test once leads convert to signups
- The user asks "how long do I need to run this" or "how many people do I need"
- The user wants to compare this test's discipline to their weekly Scale/Pivot/Kill outreach process

## Input Schema
```
element_to_test: string          # e.g. "pricing page", "onboarding step 2", "signup CTA"
current_version_description: string
proposed_change: string
current_baseline_rate: number?   # e.g. current conversion % if known
daily_or_weekly_traffic: number? # visitors/users hitting this element per period
primary_metric: string?          # what counts as a "win" - defaults inferred if missing
business_goal: string?           # e.g. "more paid signups" vs "more trial starts"
```

## Workflow
### Step 1: Lock the Hypothesis
Write it in this exact form, no exceptions:
"Changing [element] from [current] to [proposed], for [audience], will change [one metric] because [one reason]."
If the user gives a vague idea ("I want to test a new pricing page"), ask what specifically changes (price, layout, copy, number of tiers) — a test needs one variable, not a redesign. If they insist on testing a full redesign, tell them plainly: that's fine, but they'll know THAT something worked, not WHY, and won't be able to isolate it for the next test.

### Step 2: Pick One Success Metric
Reject vanity metrics stacked together ("more signups AND more engagement AND better retention"). Force one primary metric tied to the business goal (e.g. paid conversion rate, not page views). Secondary metrics can be tracked but never decide the test.

### Step 3: Calculate Required Sample Size
Use the standard two-proportion test approach, plain language:
- Ask for (or estimate) current baseline conversion rate
- Ask for the minimum lift worth caring about (a 1% lift on a 2% baseline needs a huge sample; don't chase noise)
- Use this rule of thumb table (95% confidence, 80% power) instead of running live stats software:

| Baseline rate | Minimum detectable lift | Approx. sample size needed PER variant |
|---|---|---|
| 2% | to 3% (+1pt, 50% relative) | ~3,600 |
| 5% | to 7% (+2pt, 40% relative) | ~1,700 |
| 10% | to 13% (+3pt, 30% relative) | ~900 |
| 20% | to 25% (+5pt, 25% relative) | ~600 |
| 40% | to 48% (+8pt, 20% relative) | ~400 |

If traffic is too low to hit these numbers in a reasonable window (state the math: "at your traffic you'd need 9 weeks to reach the sample size"), say so directly and offer the honest alternative: run it longer, test a bigger change (bigger lifts need smaller samples), or don't run a formal split test — use before/after with a big obvious swing instead.

### Step 4: Set the Test Window Up Front
Pick a stop date or stop-sample-size BEFORE launch, matching Step 3's number. State explicitly: no peeking early and stopping the moment it looks good — that's how false positives happen. If this is a SaaS app tied to the user's Execution Squad outreach sprint, align the test window to the same 7-day sprint cadence where possible so both loops report on the same rhythm.

### Step 5: Define the Decision Rule Before Seeing Data
Write down now what "win," "no difference," and "underpowered / inconclusive" each mean numerically, so no one negotiates with the result after the fact.

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Hypothesis names exactly one variable that changed
- [ ] Exactly one primary metric is named
- [ ] Sample size is stated as a number, not "run it a while"
- [ ] A stop date or stop-sample-size exists
- [ ] Decision rule is written before any data exists
- [ ] If traffic can't support the sample size in a reasonable time, this is flagged honestly, not glossed over

## Output Schema
```json
{
  "test_name": "string",
  "hypothesis": "string",
  "variant_a": "string (control)",
  "variant_b": "string (treatment)",
  "primary_metric": "string",
  "secondary_metrics": ["string"],
  "baseline_rate": "number|null",
  "minimum_detectable_lift": "string",
  "required_sample_size_per_variant": "number",
  "estimated_weeks_to_reach_sample": "number|null",
  "stop_condition": "string",
  "decision_rule": { "win": "string", "no_difference": "string", "inconclusive": "string" }
}
```

## Output Format
```markdown
# A/B Test Plan: [element name]

## Hypothesis
Changing [X] from [current] to [proposed], for [audience], will change [metric]
because [reason].

## Setup
- Control (A): [description]
- Treatment (B): [description]
- Primary metric: [metric] (the only one that decides the winner)
- Secondary metrics (informational only): [list]

## Sample Size & Timeline
- Baseline rate: [X]%
- Smallest lift worth detecting: [Y]%
- Sample size needed per variant: [N]
- At current traffic ([T]/week), this takes approximately [W] weeks
- [Flag if this is unrealistic and suggest alternative]

## Decision Rule (locked before launch)
- Win: [numeric condition]
- No difference: [numeric condition]
- Inconclusive / underpowered: [numeric condition]

## Do Not
- Stop early because one variant "looks like it's winning"
- Change anything else in the app while this test runs
- Declare a winner before reaching the sample size or stop date
```

## Error Handling
- No baseline rate given → ask for last 30 days of data; if unavailable, use a conservative estimate and clearly label it as an estimate
- No traffic numbers given → cannot calculate a timeline; state the sample size and ask the user to estimate weekly traffic, or default to "cannot forecast duration, tell me your weekly visitor count"
- User wants to test more than one variable at once → warn that they won't know which change caused the result; offer to sequence it as two tests instead
- User already ran the test and wants to know if it's "done" → ask for actual sample size reached and results, then check against the decision rule, don't let them round up
- Traffic is too low to ever reach significance → say so plainly and recommend either a bigger swing test or qualitative before/after review instead of fake statistics

## Examples
**Example 1**
User: "I want to test two pricing pages, $29 vs $39 for the same plan."
Skill: Locks hypothesis ("changing price from $29 to $39 for trial-to-paid converters will change paid conversion rate"), sets primary metric as paid conversion rate, calculates sample size using their baseline trial-to-paid rate, and flags if their 40 trials/week means the test would take 6+ months — recommends instead running it as a straight before/after 4-week price change if traffic is too thin for a split test.

**Example 2**
User: "We already changed the onboarding CTA copy two weeks ago, did it work?"
Skill: Asks for the sample size reached and the before/after conversion numbers, checks against a proper significance threshold (not just "does B look higher"), and reports honestly if 2 weeks of traffic was nowhere near enough to conclude anything.

**Example 3**
User: "Should I test my whole landing page redesign against the old one?"
Skill: Explains this tests everything at once — if it wins, they won't know why. Offers to break it into sequential single-variable tests (headline, then CTA, then layout) or accept the tradeoff if they just want a fast up/down call in a low-traffic startup.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- signup-conversion-tracker (S7-Growth)
- unique-value-prop-audit (S1-Research)
- pricing-model-calculator (S1-Research)

### Fed By
- signup-conversion-tracker (S7-Growth)
- competitor-teardown (S1-Research)

### Feedback Loop
Test results should update pricing-model-calculator assumptions and feed the next signup-conversion-tracker funnel read so the biggest drop-off point is retested with a real hypothesis instead of a guess.

```yaml
chain_metadata:
  skill_slug: "ab-test-generator"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "signup-conversion-tracker"
    - "pricing-model-calculator"
```
