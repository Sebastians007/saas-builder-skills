---
name: app-performance-report
description: >
  Pulls raw uptime, load time, error rate, and active user metrics into a
  short plain-language report a non-technical founder can actually read and
  act on, instead of a wall of dashboard numbers.
  Use this skill when the user asks for a performance summary, health check,
  or status report on their live app, or says
  "how is my app doing", "give me a performance report", "is my app healthy",
  "summarize my uptime and errors this month", "translate these metrics into plain english",
  "what should I worry about with my app's performance", "weekly app health check".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "performance", "reporting", "operations"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Growth
---

# App Performance Report

This skill converts raw monitoring/analytics numbers into a one-page plain-language report: what's healthy, what's not, and the one thing to fix this week. It exists because founders have dashboards full of numbers they never open because none of it says what to actually do.

## Stage
This skill belongs to Stage S7: Growth

## When to Use
- Monthly or weekly health check on a live app
- Founder wants to know if slow performance is costing them users
- After a monitoring-alerting-setup is in place and data has accumulated
- Before a growth push, to confirm the app can handle more users first
- Investor, cofounder, or team update needs a status summary
- Error rates or downtime alerts have been firing and the founder wants context, not just alert noise

## Input Schema
```
uptime_percent: number?
load_time_data: { avg_ms: number?, p95_ms: number? }?
error_rate: { total_errors: number?, total_requests: number?, error_percent: number? }?
active_users: { daily: number?, weekly: number?, monthly: number?, trend: string? }?
time_period: string?             # e.g. "last 30 days"
known_incidents: string?         # any outages or issues the founder already knows about
```

## Workflow
### Step 1: Gather the Four Core Numbers
Uptime %, load time (average and p95 — p95 matters more since it's what your slowest real users feel), error rate (% of requests that failed), and active users (with trend direction). If the user only has some of these, work with what's available and clearly list what's missing and how to start tracking it (point to monitoring-alerting-setup).

### Step 2: Translate Each Number Into Plain Language
Never present a raw number without a "what this means" line:
- Uptime under 99.5% → translate to actual downtime minutes/hours per month, and what that likely cost in lost usage
- p95 load time over 3 seconds → translate to "your slowest 5% of page loads take longer than [X] seconds, which is past where users start bouncing"
- Error rate over 1% → translate to "roughly 1 in every 100 actions fails for a user"
- Active user trend → translate to whether the app is growing, flat, or shrinking, not just the raw count

### Step 3: Rank by Business Impact, Not Alarm Volume
A monitoring tool might fire 50 alerts about minor latency blips and stay silent about a slow user-facing page. Re-rank issues by what actually affects users and revenue, not by alert count.

### Step 4: Name the One Thing to Fix This Week
Same discipline as the rest of the pack: don't hand back five action items. Pick the single highest-impact fix and say so plainly. List the rest as "worth watching" but not urgent.

### Step 5: Flag What's Actually Fine
Explicitly call out what's healthy so the founder doesn't waste time worrying about things that don't need it. A report that's all red flags trains people to ignore it.

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Every raw number has a plain-language translation next to it
- [ ] Exactly one "fix this week" item is named
- [ ] Healthy metrics are explicitly called out, not omitted
- [ ] No jargon (p50/p99/SLA/MTTR) appears without being explained in plain words
- [ ] Report is short enough to read in under 2 minutes

## Output Schema
```json
{
  "time_period": "string",
  "summary_verdict": "healthy|needs_attention|urgent",
  "metrics": [
    {"name": "string", "raw_value": "string", "plain_meaning": "string", "status": "healthy|watch|urgent"}
  ],
  "fix_this_week": "string",
  "worth_watching": ["string"],
  "whats_fine": ["string"]
}
```

## Output Format
```markdown
# App Health Report — [time period]

## Bottom Line
[One sentence: healthy / needs attention / urgent, and why]

## The Numbers, Plain English
| Metric | Number | What It Means |
|---|---|---|
| Uptime | [x]% | [plain translation] |
| Load time (typical user) | [x]s | [plain translation] |
| Load time (slowest 5%) | [x]s | [plain translation] |
| Error rate | [x]% | [plain translation] |
| Active users | [n], trending [up/down/flat] | [plain translation] |

## Fix This Week
[One specific thing, why it matters, rough effort]

## Worth Watching (not urgent)
- [item]

## What's Fine
- [item] — no action needed

## Missing Data
[If any core metric wasn't available, note it and what to set up]
```

## Error Handling
- No monitoring data exists at all → don't fabricate numbers; recommend monitoring-alerting-setup first and offer a lightweight starting point (uptime pinger + basic error logging)
- Only some metrics available → report on what exists, clearly list what's missing, still give a bottom-line verdict based on available data with that caveat stated
- Numbers look fine but user still feels something's wrong → ask for specifics (which page, which action) since raw aggregate metrics can hide a problem isolated to one feature or one user segment
- Conflicting data (uptime good but users report the app "feels slow") → trust user reports over the monitoring tool and flag a likely monitoring gap (e.g. checking only the homepage, not the actual app pages)
- User wants every number, not a summary → provide the plain-language version first, then offer the raw numbers appendix on request

## Examples
**Example 1**
User: "Can you give me a performance report for this month, here's my uptime and error data."
Skill: Translates 99.2% uptime into "about 6 hours of downtime this month," flags error rate at 2.3% as "roughly 1 in 43 actions failing" and urgent, names fixing the error source as this week's priority, confirms load times are fine and don't need attention.

**Example 2**
User: "Is my app ready to handle more traffic before I push a big marketing campaign?"
Skill: Checks p95 load time and error rate under current load, and if p95 is already climbing near a concerning threshold, flags that scaling traffic without addressing it first risks a bad first impression for new users — ties this back to load-test-builder for a proper stress test before the campaign.

**Example 3**
User: "My monitoring tool fired 30 alerts this week, am I in trouble?"
Skill: Asks for the alert list, separates noise (minor latency blips on non-critical background jobs) from real user-facing issues, and reports that only 2 of the 30 actually matter, naming the top one to fix.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- incident-runbook-writer (S6-Operations)
- load-test-builder (S4-Testing)
- signup-conversion-tracker (S7-Growth)

### Fed By
- monitoring-alerting-setup (S6-Operations)
- backup-recovery-builder (S6-Operations)

### Feedback Loop
Recurring performance issues that keep landing in "fix this week" should get written into incident-runbook-writer so the same problem isn't re-diagnosed from scratch every report cycle.

```yaml
chain_metadata:
  skill_slug: "app-performance-report"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "incident-runbook-writer"
    - "load-test-builder"
```
