---
name: technical-spike-brief
description: >
  Run a quick, time-boxed research spike on an uncertain technical piece (a new API,
  a tricky integration, an unfamiliar service) and write up findings and risks before
  any real code gets committed.
  Use this skill when the user asks about de-risking an unfamiliar integration,
  evaluating whether something is technically feasible, or says
  "I'm not sure this API will do what I need", "spike this before we build it",
  "will Stripe/Twilio/whatever actually support this", "research this integration first",
  "what are the gotchas with this service", "is this even possible with our stack",
  "don't want to commit code until I know this works".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "research", "risk", "integration"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# Technical Spike Brief

Produces a short, focused writeup that answers "can we actually build this, and what will bite us" before real implementation code is written. A spike is throwaway exploration — a test script, a docs read, a sandbox call — not production code, and this skill keeps it that way so the founder doesn't accidentally build half a feature on an unverified assumption.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- Before integrating a new third-party API or service the team hasn't used before
- When a feature depends on something unverified (rate limits, a library's actual behavior, a platform's constraints)
- When a previous integration attempt failed partway through and burned time
- When the user is unsure if their stack (e.g. Cloudflare Workers) can even do what's being asked
- Before committing to an architecture decision that's expensive to reverse
- When "let's just try it in production code" would be risky or slow

## Input Schema
```
uncertainty: string         # the specific thing that's unknown/risky
context: string?            # what feature this supports, current stack
time_box: string?           # default "60 minutes" if not specified
must_answer: string[]?      # specific questions that must be resolved
```

## Workflow
### Step 1: Pin down the real question
Restate the uncertainty as one or two precise yes/no or specific-answer questions. "Will Stripe support usage-based billing on our plan" not "figure out Stripe."

### Step 2: Set the time box
Default to 60 minutes of research/testing. State it up front. A spike that runs long has stopped being a spike.

### Step 3: Research and/or throwaway test
Use docs (Context7 if the library is code-related), the vendor's official documentation, and if needed a minimal disposable test script or sandbox call — never wire it into the real app. Note exact findings: rate limits, pricing tiers, auth requirements, known limitations, version-specific gotchas.

### Step 4: Identify risks and workarounds
For anything that doesn't fully answer "yes this works cleanly," name the risk plainly and give the workaround or fallback option if one exists.

### Step 5: Make the call
End with an explicit recommendation: proceed as planned, proceed with a specific workaround, or don't build this the way it was planned (and what to do instead).

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] The original uncertainty has a direct answer, not a vague summary
- [ ] Any claim is backed by a source (docs link, tested output) not assumption
- [ ] Risks are stated in plain terms with real-world impact, not just "may have issues"
- [ ] No production code was written during the spike
- [ ] There's a clear go/no-go/go-with-workaround recommendation

## Output Schema
```json
{
  "question": "string",
  "time_boxed_to": "string",
  "findings": [
    {"claim": "string", "source": "string", "confidence": "high | medium | low"}
  ],
  "risks": [
    {"risk": "string", "impact": "string", "workaround": "string | null"}
  ],
  "recommendation": "proceed | proceed_with_workaround | do_not_proceed",
  "recommendation_detail": "string"
}
```

## Output Format
```markdown
# Spike: <one-line question>

**Time boxed to:** <duration>

## What I found
- <finding 1, with source>
- <finding 2, with source>

## Risks
| Risk | Impact | Workaround |
|---|---|---|
| ... | ... | ... |

## Recommendation
**<Proceed / Proceed with workaround / Do not proceed as planned>**

<1-3 sentences explaining why, in plain language>

## Next step
<what to build now that this is answered, or what to research instead>
```

## Error Handling
- If the uncertainty is too broad ("will this whole app work"), narrow it to the single riskiest unknown first and note the rest need their own spikes.
- If research is inconclusive after the time box, say so explicitly rather than guessing — recommend a small real-world test (e.g. sandbox account signup) as the next step.
- If the vendor's docs contradict themselves or are out of date, flag the discrepancy and prefer the most recent official source; note the uncertainty in confidence level.
- If the answer is "this won't work as planned," don't soften it — give the alternative approach immediately so the founder isn't stuck.
- If no library/API is actually involved (pure logic question), redirect to feature-task-breakdown instead — a spike is for external unknowns, not internal design choices.

## Examples

**Example 1**
User: "Not sure if Cloudflare Workers can handle scheduled email sends for our onboarding sequence."
Skill does: time-boxes to 45 min, checks Cloudflare Cron Triggers + Email Workers docs, tests a minimal cron worker, finds a 24-hour minimum granularity limitation, flags workaround (use a queue + external cron), recommends proceed with workaround.
Outcome: founder avoids building the naive version and hitting the limitation mid-build.

**Example 2**
User: "Will Twilio's API let us do two-way SMS conversations, not just one-off sends?"
Skill does: reads Twilio Conversations API docs, confirms yes with pricing tier note, recommendation: proceed as planned.
Outcome: clears the path to build the real feature with confidence.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- architecture-decision-writer (S5-Planning)
- api-endpoint-builder (S6-Building)
- feature-task-breakdown (S6-Building)

### Fed By
- tech-stack-finder (S1-Research)
- feature-task-breakdown (S6-Building)

### Feedback Loop
When a spike's recommendation turns out wrong during actual building, feed that back into future spikes on similar integrations to raise or lower default confidence.

```yaml
chain_metadata:
  skill_slug: "technical-spike-brief"
  stage: "building"
  timestamp: string
  suggested_next:
    - "architecture-decision-writer"
    - "api-endpoint-builder"
    - "feature-task-breakdown"
```
