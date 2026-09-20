---
name: monitoring-alerting-setup
description: >
  Sets up lightweight uptime, error, and performance monitoring with alerts
  so the founder hears about outages before customers do.
  Use this skill when the user asks about "how do I know if my app is down",
  "set up monitoring for my app", "I want alerts when something breaks",
  "how do I catch errors in production", "add uptime monitoring", "what
  should I monitor for my SaaS", or "customers found a bug before I did".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "monitoring", "alerting", "ops", "cloudflare"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Operations
---

# Monitoring & Alerting Setup

Designs a small, free-or-cheap monitoring stack that tells a solo founder the moment their app goes down, starts erroring, or slows to a crawl — before a customer emails them about it. Produces a concrete setup checklist, not a monitoring philosophy essay.

## Stage
This skill belongs to Stage S6: Operations

## When to Use
- The app just went live and there is currently zero visibility into uptime or errors
- A customer reported a bug or outage the founder didn't know about
- The founder wants to add alerting (Slack, email, SMS) for downtime or error spikes
- Traffic or revenue has grown enough that "I'll just check it manually" no longer works
- Setting up a new environment (staging, production) that needs its own watch
- Post-incident review calls for "how do we catch this earlier next time"

## Input Schema
```
app_url: string                    # public URL of the app
hosting: enum                      # cloudflare-pages | cloudflare-workers | vercel | other
has_backend_api: boolean
has_database: boolean              # e.g. D1, Postgres, Supabase
critical_user_flows: string[]      # e.g. ["signup", "login", "checkout"]
current_monitoring: string | none  # what's already in place, if anything
alert_channels: string[]           # e.g. ["email", "slack", "sms"]
budget: enum                       # free-only | under-$20/mo | flexible
```

## Workflow
### Step 1: Inventory what needs watching
List the app's critical surfaces: the public URL, the API base, the login/signup flow, any payment flow, and the database. Rank by "if this breaks, do customers notice within 5 minutes" — those get real-time alerts; everything else can be daily-digest.

### Step 2: Pick the monitoring layers (proportional to app size)
- **Uptime**: UptimeRobot free tier (50 monitors, 5-min checks) or Cloudflare's own Health Checks if on Cloudflare. Ping the homepage and one authenticated API route every 5 minutes.
- **Error tracking**: Sentry free tier (5k events/mo) wired into the frontend and backend. This catches JS exceptions and unhandled server errors — the things that break silently.
- **Platform analytics**: Cloudflare Web Analytics (free, privacy-friendly) or Cloudflare Workers/Pages built-in request analytics for traffic and 5xx rate at a glance.
- **Log-based alerts**: if using Cloudflare Workers, a simple `console.error` + Logpush or Tail Worker that posts to a Slack webhook on repeated failures is enough — no need for a full log pipeline at this scale.

Do NOT recommend Datadog, New Relic, or a self-hosted Prometheus/Grafana stack unless the user explicitly has enterprise scale or asks for it — that is over-engineering for a small SaaS.

### Step 3: Define alert thresholds
Write explicit, boring thresholds, not vibes:
- Uptime check fails 2 consecutive times (10 min) → alert
- 5xx error rate > 5% of requests over 5 min → alert
- Error tracker sees a new (never-before-seen) error type → alert
- No signups/logins succeeded in the last 24h on an app that normally has them → daily digest flag

### Step 4: Wire up alert delivery
Match channel to urgency: uptime/5xx alerts go to a channel the founder actually checks fast (SMS or a phone-push app like Slack mobile with notifications on) — email alone is too slow for "site is down." New-error-type and digest-level items can go to email or a Slack channel that's checked once a day.

### Step 5: Write the setup as copy-pasteable steps
Produce literal account-creation and config steps (tool name, plan tier, what URL to add, what threshold to set) so the founder can execute in under 30 minutes without further research.

### Step 6: Self-Validation
- [ ] Every critical user flow from the input has at least one monitor covering it
- [ ] At least one check has a "you'll know within 10 minutes" alert, not just a dashboard
- [ ] Every tool recommended has a free or near-free tier matching stated budget
- [ ] No tool recommended requires infra the founder doesn't already run
- [ ] Alert thresholds are numeric and specific, not "monitor for issues"
- [ ] Output includes what to do the first time an alert fires (link to incident-runbook-writer if none exists)

## Output Schema
```
{
  monitors: [
    { name: string, tool: string, target: string, check_interval: string, alert_condition: string }
  ],
  alert_channels: [ { channel: string, used_for: string[] } ],
  setup_steps: string[],
  monthly_cost_estimate: string,
  gaps_not_covered: string[]
}
```

## Output Format
```markdown
# Monitoring & Alerting Plan — <app name>

## What gets watched
| Surface | Tool | Check | Alert Trigger |
|---|---|---|---|
| Homepage uptime | UptimeRobot | every 5 min | 2 consecutive fails |
| API errors | Sentry | real-time | new error type or spike |
| ... | ... | ... | ... |

## Alert routing
- Urgent (site down, 5xx spike) → <channel>
- Daily digest (new errors, low signal) → <channel>

## Setup steps (do these in order)
1. ...
2. ...

## Estimated monthly cost
<$X or free>

## Not covered yet (call out honestly)
- ...
```

## Error Handling
- If the user hasn't specified hosting, ask once, then default to assuming Cloudflare since this pack targets Cloudflare-hosted apps
- If budget is unstated, default to free-tier-only and note where paid tiers would add value
- If the app has no backend (static site only), skip error tracking recommendations and focus on uptime + Cloudflare Analytics
- If the user already has partial monitoring, don't rebuild it — audit gaps against Step 1's inventory and only fill what's missing
- If critical_user_flows is empty, ask for at least the signup/login flow before proceeding — "monitor everything generically" isn't useful

## Examples
**Example 1**: User says "my app went down for 2 hours last night and I didn't find out until a customer emailed me." Skill inventories the app (Cloudflare Pages + Workers API + D1), recommends UptimeRobot on the homepage and API health endpoint with SMS alerts, Sentry for backend errors, and a Slack digest for anything non-urgent. Output: a setup checklist executable in ~20 minutes.

**Example 2**: User says "what should I be monitoring for my SaaS" before launch. Skill asks for critical_user_flows, gets "signup, login, dashboard load," and produces a pre-launch monitoring plan sized to a pre-revenue app (free tiers only, no SMS cost yet).

**Example 3**: User already has UptimeRobot but no error tracking. Skill audits the gap, recommends adding Sentry only, and skips re-recommending uptime monitoring.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- incident-runbook-writer (S6-Operations)
- app-performance-report (S7-Growth)
- security-review-lite (S4-Testing)

### Fed By
- cloudflare-deployer (S5-Deployment)
- ci-cd-pipeline-builder (S5-Deployment)

### Feedback Loop
Alert frequency and false-positive rate over time should tighten or loosen thresholds — noisy alerts get widened, missed incidents get new monitors.

```yaml
chain_metadata:
  skill_slug: "monitoring-alerting-setup"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "incident-runbook-writer"
    - "backup-recovery-builder"
```
