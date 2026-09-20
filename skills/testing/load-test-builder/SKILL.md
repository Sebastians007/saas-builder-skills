---
name: load-test-builder
description: >
  Defines lightweight load and stress checks sized for a small SaaS app with
  real but modest traffic — not enterprise-scale over-engineering that
  wastes a solo founder's time.
  Use this skill when the user asks about "will my app hold up under
  load", "how many users can this handle", "should I load test this",
  "what happens if this gets busy", "am I going to fall over at launch",
  "check if this scales", or "stress test my app before I post this on
  Reddit".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "performance", "load-testing"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Testing
---

# Load Test Builder

Defines a right-sized load check for a small SaaS app — enough to catch "this falls over the moment 20 people show up at once," without pretending you need to simulate a million concurrent users. Most early-stage apps never get killed by scale; they get killed by one slow query or one unbounded loop that only shows up under a small burst of real traffic. This skill finds that.

## Stage
This skill belongs to Stage S7: Testing

## When to Use
- Before a launch day, Product Hunt post, cold email blast, or anything that could send a burst of traffic at once
- When a feature does something expensive per request (image processing, PDF generation, AI API calls, big DB queries)
- When the app has never been checked under more than one user at a time
- When Cloudflare Workers/Pages usage limits or a database connection limit could realistically be hit
- Not needed for a feature with near-zero expected concurrent use (internal admin tool, single-user app) — say so and skip it

## Input Schema
```
app_url: string
expected_peak_users: number (optional)   # e.g. "maybe 50 people click the launch link in an hour"
expensive_operations: [string] (optional) # e.g. "AI summary generation", "PDF export"
backend: string (optional)               # Cloudflare Workers, Node server, serverless DB, etc.
current_scale: string (optional)         # "0 users so far" is a valid, common answer
```

## Workflow
### Step 1: Size the actual expected load
Get a realistic number, not a hypothetical one. For a solo founder's SaaS, "peak load" usually means: a launch post drives 50-500 visitors over a few hours, with maybe 5-20 concurrent at any one moment. Anchor the test to that reality, not to "what if we go viral" — that's a different, later problem, and over-building for it now wastes time.

### Step 2: Identify the actual bottleneck candidates
Not everything needs load testing. Focus on: anything that calls a paid third-party API per-request (AI, email, payment), anything that writes to the database without an index, anything that processes a file (upload/resize/PDF), and any serverless function with a cold-start or timeout limit.

### Step 3: Define the lightweight test
For a small SaaS this means: simulate 10-50 concurrent requests to the 2-3 riskiest endpoints (not the whole app), using a simple tool appropriate to the stack (e.g. a basic script hitting the URL N times concurrently, or a free tier of a tool like k6/Artillery if already available — don't introduce new paid infrastructure for this).

### Step 4: Define pass/fail thresholds sized for a small app
Reasonable defaults: 95% of requests complete in under 3 seconds, error rate under 1% at expected peak, no hard crash or unbounded memory growth. These are "don't embarrass yourself at launch" thresholds, not enterprise SLAs.

### Step 5: Check platform-specific limits
If on Cloudflare Workers/Pages: check for CPU time limits per request, subrequest limits, and D1/KV rate limits at the expected volume. If using a database with a connection pool limit (common failure mode: serverless functions exhausting a small Postgres connection pool), flag it explicitly — this is the single most common "worked in testing, died at 20 users" bug for solo-built SaaS apps.

### Step 6: Self-Validation
- [ ] Load target is based on a realistic number for this specific launch, not an arbitrary big number
- [ ] Only the 2-3 actually-risky endpoints are targeted, not the whole app
- [ ] Connection pool / rate limit / cold-start limits for the actual backend were checked, not assumed fine
- [ ] Thresholds are stated in plain numbers (X seconds, Y% errors), not vague ("should be fast")
- [ ] If load testing genuinely isn't needed yet (near-zero traffic expected), the skill says so instead of manufacturing a test

## Output Schema
```
{
  expected_peak: string,
  risky_endpoints: [
    {
      endpoint: string,
      why_risky: string,
      test_plan: string,
      threshold: string
    }
  ],
  platform_limits_checked: [string],
  verdict: "ready_for_expected_load" | "risk_found" | "not_yet_tested"
}
```

## Output Format
```markdown
# Load Check: [App Name]

Expected peak: [number/description]

## Risky Endpoints
### [endpoint]
Why risky: ...
Test: [what to run, exact command/tool if applicable]
Threshold: [numbers]

## Platform Limits to Watch
- ...

## Verdict
[plain statement: ready, or here's what will break first and at roughly what volume]
```

## Error Handling
- No expected traffic estimate given → use a conservative default (20-50 concurrent) appropriate for a first launch and state that assumption
- App has zero users so far and no launch planned yet → say load testing isn't the priority right now, point back to shipping/validating first (per build-first philosophy), and offer to revisit before any real launch
- No load testing tool available in the environment → provide a simple manual alternative (e.g. open N browser tabs, or a basic curl-in-a-loop script) sized for "good enough" rather than requiring new infrastructure
- Database connection limits unknown → flag this as the most common silent killer and instruct how to check it (provider dashboard, pool size setting) rather than guessing
- User wants enterprise-scale testing for a pre-revenue app → gently redirect: right-size the test to actual current/near-term traffic, note that this can be revisited at real scale

## Examples
1. User: "I'm posting this on Reddit tomorrow, will it hold up" → Skill sizes test to ~100-300 visitors/few hours, identifies the AI-generation endpoint as the risk (rate-limited external API), recommends a queue or rate-limit-friendly fallback message instead of a hard failure. Outcome: founder adds a "high demand, try again in a moment" state instead of a raw error page.
2. User: "check if my app scales" (2 users total so far) → Skill points out load testing isn't the current bottleneck, redirects to getting more users first, offers to build this once there's an actual launch date.
3. User: "why did my app die during the product hunt launch" → Skill (used retroactively) identifies the serverless function exhausted the database's 20-connection limit at ~30 concurrent users. Outcome: founder switches to a pooled connection setup before the next launch attempt.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- monitoring-alerting-setup (S9-Operations)
- app-performance-report (S10-Growth)
- incident-runbook-writer (S9-Operations)

### Fed By
- cloudflare-deployer (S8-Deployment)
- architecture-decision-writer (S5-Planning)

### Feedback Loop
When a real launch reveals a bottleneck this check missed, feed the actual failure point back so future load checks for similar apps test that endpoint by default.

```yaml
chain_metadata:
  skill_slug: "load-test-builder"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "monitoring-alerting-setup"
    - "incident-runbook-writer"
```
