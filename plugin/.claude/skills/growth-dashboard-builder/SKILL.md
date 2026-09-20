---
name: growth-dashboard-builder
description: >
  Builds one central dashboard that shows acquisition, activation, retention,
  revenue, and referral numbers in a single page, pulled from PostHog so the
  founder stops checking five tools to answer "is the business growing".
  Use this skill when the user asks about a growth dashboard, a single view of
  all their metrics, or says
  "build me a growth dashboard", "I need one place to see all my metrics",
  "how is the business doing this week", "track my whole funnel in one place",
  "set up a dashboard with PostHog", "I'm tired of checking five different tools",
  "what should I be measuring every week".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "dashboard", "posthog", "metrics", "aarrr"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Growth Dashboard Builder

This skill builds a single-page dashboard that shows the full AARRR funnel — Acquisition, Activation, Retention, Revenue, Referral — in one place, pulled live from PostHog and hosted for free on Cloudflare Pages. It replaces "let me check four tools and guess" with one page the founder opens every Monday. This is the direct answer to "I have data everywhere but no central view of it."

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The user has PostHog (or another analytics tool) collecting events but no single view of the numbers
- The user is checking multiple tabs/tools to answer basic growth questions
- The user wants a weekly or Monday-morning growth review ritual
- After several other S7 skills (signup-conversion-tracker, attribution-mapper, cohort-churn-analyzer, aha-moment-mapper) have defined what to measure — this skill is where those definitions get displayed continuously
- The user asks "is the business actually growing" and can't answer with a number
- The user wants something non-technical to check daily without opening a spreadsheet

## Input Schema
```
analytics_tool: string?          # defaults to "PostHog"
posthog_project_id: string?
posthog_api_key: string?         # personal API key, read-only project scope
hosting_target: string?          # defaults to "Cloudflare Pages"
metrics_already_defined: {
  activation_event: string?,     # from aha-moment-mapper, if run
  key_funnel_stages: array?      # from signup-conversion-tracker, if run
}
update_frequency: string?        # defaults to "daily auto-refresh"
audience: string?                # defaults to "solo founder / small team"
```

## Workflow
### Step 1: Confirm the Metric Set (Don't Guess)
A dashboard with the wrong metrics is worse than no dashboard — it trains the founder to look at the wrong numbers. Lock exactly one metric per funnel stage before building anything:
- **Acquisition**: new visitors + new signups (7-day and 30-day)
- **Activation**: % of new signups that hit the activation event (pull the exact event name from aha-moment-mapper if it's been run; if not, ask what proves a user got value)
- **Retention**: W1 / W4 retention rate (returning users as % of a signup cohort)
- **Revenue**: MRR, new MRR, churned MRR (link to revenue-dashboard-builder for the deep version — this dashboard only needs the top-line number)
- **Referral**: % of new signups tagged with a referral source

Resist requests to add more than 6-8 tiles total. A dashboard nobody can read in 30 seconds doesn't get checked.

### Step 2: Pick the Data Source
Default to PostHog since it's free, self-hostable, and has an API. Confirm:
- Is PostHog already installed and firing events (signup, login, activation event, payment)?
- If not, this skill stops here and hands off — instrumentation has to exist before a dashboard can show anything. Point to the minimum event set: `signup`, `login`, the activation event, `subscription_started`, `subscription_canceled`.
- Get a read-only Personal API Key scoped to one project (Settings → Personal API Keys in PostHog). Never use a key with write/delete scope for a dashboard.

### Step 3: Choose the Build Approach
Two options, pick based on the user's comfort level — always the simpler one unless they ask for more:

**Option A — PostHog's own dashboard (fastest, zero build)**
PostHog already has dashboard and insight-building UI. If the user just needs the numbers visible and doesn't need a branded page, build the dashboard directly inside PostHog using its Trends/Funnels/Retention insights, pin the 6-8 tiles above, and share the dashboard link. Recommend this first — it's free, requires no hosting, and updates in real time automatically.

**Option B — Custom Cloudflare Pages page pulling PostHog's API (for a branded, single-URL view)**
When the user wants one clean URL to check (or to share with a co-founder/investor) that isn't PostHog's own UI:
1. Build a static HTML page (or small Cloudflare Worker + Pages Function) with the 6-8 metric tiles laid out per the `dataviz` skill's stat-tile guidance.
2. The page calls PostHog's [Query API](https://posthog.com/docs/api/queries) or [HogQL API] server-side via a Cloudflare Pages Function (never expose the API key client-side — proxy it through a Function that holds the key as a Cloudflare secret).
3. Cache the API response for 15-60 minutes using Cloudflare's cache or KV, so the page loads instantly and doesn't hammer PostHog's API on every visit.
4. Deploy with `cloudflare-deployer`. No paid BI tool (Looker, Tableau, etc.) is needed or appropriate for this scale — avoid recommending them.

### Step 4: Lay Out the Page
Order top to bottom by funnel stage, not by what's easiest to pull:
1. One-line status: "Last 7 days: [X] signups, [Y]% activated, $[Z] MRR" — the answer to "how's it going" before anyone scrolls
2. Acquisition tile row
3. Activation tile row (with trend vs. prior period)
4. Retention curve (simple line, W1/W4)
5. Revenue snapshot (link out to revenue-dashboard-builder for detail)
6. Referral %

### Step 5: Set the Update Cadence
- Auto-refresh: the PostHog API pull should run on page load (cached) rather than requiring a manual export
- Weekly ritual: recommend the user open the dashboard every Monday, screenshot it, and note one sentence about what changed — this is what actually makes a dashboard useful long-term, not the dashboard itself
- Revisit metric definitions every 90 days (activation event, referral definition) since they drift as the product changes

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Exactly one metric is chosen per funnel stage, not a metric dump
- [ ] The data source (PostHog) and how the API key is secured are both specified
- [ ] A free/simple hosting path is used (PostHog native dashboard or Cloudflare Pages) — no paid enterprise BI tool recommended
- [ ] The page answers "how's it going" in one line before any chart
- [ ] Update frequency and a weekly-review habit are both specified, not just the build

## Output Schema
```json
{
  "metric_set": {
    "acquisition": "string",
    "activation": "string",
    "retention": "string",
    "revenue": "string",
    "referral": "string"
  },
  "data_source": "string",
  "build_approach": "posthog_native|cloudflare_pages_custom",
  "hosting_url": "string|null",
  "update_frequency": "string",
  "instrumentation_gaps": ["string"]
}
```

## Output Format
```markdown
# Growth Dashboard Spec

## Metrics (one per stage)
| Stage | Metric | Source event(s) |
|---|---|---|
| Acquisition | [metric] | [PostHog event] |
| Activation | [metric] | [PostHog event] |
| Retention | [metric] | [PostHog event] |
| Revenue | [metric] | [PostHog event/Stripe] |
| Referral | [metric] | [PostHog event] |

## Build Approach: [PostHog native | Cloudflare Pages custom]
[Setup steps]

## Instrumentation Gaps
[Any events missing before this can be built — stop and fix these first]

## Weekly Review Habit
Every Monday: open the dashboard, screenshot it, write one sentence on what changed.

## Do Not
- Add more than 6-8 tiles
- Recommend a paid BI tool (Looker, Tableau, Mode) at this stage
- Expose the PostHog API key client-side
- Build before instrumentation exists
```

## Error Handling
- PostHog not installed or not firing events → stop, point to the minimum event set to instrument first, do not fabricate a dashboard with no data
- No activation event defined → hand off to aha-moment-mapper before finishing this dashboard's Activation tile
- User wants 15+ metrics on one page → push back, cap at 6-8, offer a secondary page for detail
- User asks for Looker/Tableau/Mode-style BI tooling → explain that at this stage (pre-scale SaaS) a free PostHog dashboard or a simple Cloudflare page is sufficient and cheaper; revisit only past clear PMF and a data team
- API key with write access requested → refuse, generate a read-only scoped key instead

## Examples
**Example 1**
User: "I check Stripe, PostHog, and a spreadsheet every morning and it takes 20 minutes. Build me one dashboard."
Skill: Locks the 5 metrics, confirms PostHog is already firing signup/activation/payment events, recommends starting with PostHog's own native dashboard (zero build cost), and gives the exact insight configuration for each tile.

**Example 2**
User: "I want a branded page I can share with my co-founder, not the PostHog UI."
Skill: Recommends Option B — a small Cloudflare Pages page with a Pages Function proxying PostHog's Query API, caches responses, and deploys via cloudflare-deployer.

**Example 3**
User: "Can you add 20 metrics, I want to see everything?"
Skill: Pushes back — a dashboard with 20 metrics doesn't get read. Picks the 6-8 that matter, offers a secondary "deep dive" page for the rest, and points to the specific downstream skill (attribution-mapper, cohort-churn-analyzer) for anything that needs its own detailed view.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- revenue-dashboard-builder
- app-performance-report
- ab-test-generator

### Fed By
- signup-conversion-tracker
- attribution-mapper
- cohort-churn-analyzer
- aha-moment-mapper

### Feedback Loop
Every metric definition change from an upstream skill (a new activation event, a redefined funnel stage) should update the corresponding dashboard tile, and every weekly review should flag which upstream skill to re-run if a number moved unexpectedly.

```yaml
chain_metadata:
  skill_slug: "growth-dashboard-builder"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "revenue-dashboard-builder"
    - "app-performance-report"
```
