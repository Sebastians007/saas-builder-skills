---
name: aha-moment-mapper
description: >
  Identifies the single action that correlates with a user actually getting
  value — the product's "aha moment" — by combining event data with user
  interviews, so onboarding can be designed around reaching it fast.
  Use this skill when the user asks about defining activation, finding the
  aha moment, or says
  "what's our aha moment", "define activation for us", "which action predicts retention",
  "set up our North Star metric", "why don't new users stick around", "what should onboarding get people to do".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "activation", "onboarding", "retention", "posthog"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Aha Moment Mapper

This skill finds the one specific action that most strongly predicts a user will stick around, by testing candidate events from PostHog data against actual retention and cross-checking the result against real user interviews. It replaces "activation" as a vague concept with one precise, instrumentable definition that onboarding, trial sequencing, and dashboards can all be built around.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- The product has no defined activation event, or the current one was picked by guesswork
- The user wants to redesign onboarding but doesn't know what it should be driving toward
- trial-to-paid-converter or cohort-churn-analyzer need an activation event and none exists yet
- The user has at least ~60 days of usage event data and wants a rigorous answer, not a hunch
- The user references "the Facebook 7 friends in 10 days" idea and wants their own version

## Input Schema
```
posthog_project_id: string?
posthog_api_key: string?          # read-only, needs at least 60 days of event history
retention_definition: string?     # e.g. "used product in week 4 post-signup" — ask if not given
candidate_events: array?          # product team's guesses, optional — the skill also generates its own
interview_notes: array?           # 3-5 retained-user interview transcripts/notes, optional but strongly recommended
```

## Workflow
### Step 1: Find Predictive Events from Usage Data
For every distinct event type in PostHog: split signed-up users into two groups by whether they performed that event within the first N days (test N = 1, 3, 7), then compute week-4 (or whatever the retention definition is) retention for each group. Record the retention lift between the groups and its statistical significance (a simple chi-squared/Fisher's test is enough at this scale), plus the event's reachability — what % of all signups ever perform it. An event only 2% of users ever do isn't a usable activation target no matter how strongly it predicts retention; it has to be both high-lift and reasonably reachable.

### Step 2: Test Frequency and Time-Window Combinations
The strongest activation definitions are rarely a single one-time action — they're usually "did X, at least N times, within T days" (the shape behind "7 friends in 10 days"). Test a few (N, T) combinations around the best candidate event from Step 1 and look for the combination that produces the cleanest retention cliff — the sharpest jump between users below and above the threshold.

### Step 3: Cross-Check Against User Interviews
If interview transcripts are available, pull quotes matching patterns like "the moment I got it was when...", "I started using it regularly after...", or "I almost quit, but then...". Check whether these moments line up with the quantitative candidate from Step 1-2. If they don't line up, treat that as a signal something's wrong — either the event instrumentation is missing the real moment, or the real "aha" happens upstream of anything currently tracked (in which case the gap itself is the finding).

### Step 4: Write the Activation Definition
State it in one precise sentence: the action (verb + object), the frequency and time window, why this event specifically (the retention lift and reachability numbers), and 2-3 supporting interview quotes if available. This sentence is what every downstream skill (onboarding-flow-builder, trial-to-paid-converter, cohort-churn-analyzer, growth-dashboard-builder) should reference identically — inconsistent activation definitions across those skills is a common and avoidable failure mode.

### Step 5: Specify the Instrumentation
List the exact event name, properties, and triggering condition needed in PostHog so the activation event can be tracked cleanly going forward (not inferred after the fact from a combination of other events).

### Step 6: Set a Target
State the current % of signups reaching activation, a 90-day target, and who owns moving it. Without an owner and a target, the definition tends to get written once and never revisited.

### Step 7: Self-Validation
Before presenting output, confirm:
- [ ] The candidate event is both high-lift (meaningful retention difference) and high-reachability (a realistic % of signups can do it)
- [ ] A frequency/time-window version was tested, not just a single-occurrence event
- [ ] Interview evidence (if available) was explicitly checked against the quantitative pick, and any mismatch is called out rather than ignored
- [ ] The final definition is one precise sentence usable verbatim by other skills, not a vague description
- [ ] A current baseline, a 90-day target, and an owner are all specified

## Output Schema
```json
{
  "candidate_events": [
    {"event": "string", "retention_lift_pp": "number", "significant": "boolean", "reachability_pct": "number"}
  ],
  "chosen_activation_event": "string",
  "frequency_threshold": "string",
  "time_window_days": "number",
  "rationale": "string",
  "interview_evidence": ["string"],
  "instrumentation_spec": {"event_name": "string", "properties": ["string"], "trigger_condition": "string"},
  "current_activation_rate_pct": "number|null",
  "target_90_day_pct": "number|null",
  "owner": "string|null"
}
```

## Output Format
```markdown
# Aha Moment Definition

## Activation Event
**[action verb + object], done at least [N] times within [T] days of signup**

Why this event: [X]pp retention lift vs. non-activators, reached by [Y]% of signups.

## Candidate Events Considered
| Event | Retention Lift | Reachability | Chosen? |
|---|---|---|---|
| [event] | [pp] | [%] | [yes/no] |

## Interview Evidence
- "[quote]"
- "[quote]"

## Instrumentation Spec
Event name: `[name]`
Properties: [list]
Trigger: [condition]

## Targets
Current: [%] activated | 90-day target: [%] | Owner: [name/role]

## Do Not
- Pick an event that's high-lift but reached by under ~10% of signups
- Skip the interview cross-check when transcripts are available
- Leave the definition without an owner or target
```

## Error Handling
- Fewer than 60 days of event history → proceed but flag the result as preliminary, recommend re-running once more data accumulates
- No interview data available → proceed with the quantitative definition alone, explicitly note the qualitative cross-check is missing rather than skipping the step silently
- No single event clears both the lift and reachability bar → look for a combination event (did any of A/B/C) rather than forcing a single weak candidate
- Retention definition not specified → ask explicitly; "retained" needs a precise meaning (e.g. week-4 login) before any lift calculation is valid
- Quantitative and qualitative signals conflict → report both, name the conflict directly, and recommend deeper instrumentation or more interviews rather than picking one arbitrarily

## Examples
**Example 1**
User: "Help me find our aha moment. I've got 90 days of events and 5 interview transcripts with retained users."
Skill: Tests candidate events, finds "created 2+ projects within 5 days" produces the cleanest retention cliff, cross-checks against interviews where 4 of 5 mention "once I had a couple projects going," and writes the final one-sentence definition with instrumentation spec.

**Example 2**
User: "We think login is our activation event."
Skill: Tests login against real retention lift, finds it's reached by 95% of signups but has almost no retention lift (too weak a signal — nearly everyone logs in once), and finds a stronger candidate further into the product.

**Example 3**
User: "Our quant data says one thing but our interviews say something totally different."
Skill: Reports the conflict explicitly rather than picking a winner, hypothesizes the real moment is upstream of what's tracked (e.g. a manual setup call, not a trackable in-app action), and recommends instrumenting the missing step before finalizing.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- onboarding-flow-builder
- trial-to-paid-converter
- cohort-churn-analyzer

### Fed By
- signup-conversion-tracker
- attribution-mapper

### Feedback Loop
Once onboarding is redesigned around this activation event, watch the activation rate and cohort-churn-analyzer's activation-status segmentation together — if activation rate rises but retention doesn't follow, the event was reachable but not actually predictive, and this analysis should be re-run.

```yaml
chain_metadata:
  skill_slug: "aha-moment-mapper"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "onboarding-flow-builder"
    - "trial-to-paid-converter"
```
