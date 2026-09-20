---
name: attribution-mapper
description: >
  Maps which acquisition channels and touchpoints actually drive signups and
  revenue by building multi-touch journeys from PostHog event data instead of
  trusting last-click numbers from each ad platform.
  Use this skill when the user asks about channel attribution, which marketing
  channel is working, or says
  "which channel actually drives signups", "why does each ad platform take credit for the same conversion",
  "is LinkedIn actually working or just getting last-click credit", "build an attribution model",
  "where should I put my next dollar of marketing spend", "our numbers don't add up across platforms".
license: MIT
version: "1.0.0"
tags: ["saas", "growth", "attribution", "acquisition", "posthog", "channels"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
  adapted_from: "rfstudioco/agentic_growth_team (MIT)"
---

# Attribution Mapper

This skill builds a multi-touch attribution model from PostHog event data so the founder knows which channels actually drive signups and revenue, instead of trusting whichever ad platform's dashboard claims the most credit (they all over-claim). It replaces "Google Ads says it drove this, but so does LinkedIn" with one reconciled answer plus the honest caveats.

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The user runs paid or organic channels on more than one platform and each platform's dashboard claims outsized credit
- The user wants to know where to spend the next marketing dollar and doesn't trust single-channel, last-click numbers
- After a marketing push (content, ads, outreach), to see whether it actually drove signups/revenue or just looked busy
- The user's Execution Squad outreach sprint needs to be compared against other channels for relative ROI
- The founder is about to cut a channel's budget and wants to confirm it's actually the underperformer, not just the one that reports honestly

## Input Schema
```
posthog_project_id: string?
posthog_api_key: string?              # read-only, for pulling UTM-tagged event data
touch_events: string?                 # description of what's tracked, e.g. "UTM source/medium/campaign on landing"
conversion_events: array?             # e.g. ["signup", "subscription_started"]
attribution_window_days: number?      # defaults to 30 for signup, 90 for paid
known_channels: array?                # e.g. ["Google Ads", "LinkedIn organic", "cold email", "SEO"]
vendor_reported_numbers: object?      # what each ad platform claims, for reconciliation
```

## Workflow
### Step 1: Audit the Event Data Before Modeling
An attribution model built on bad UTM data just produces confident-sounding nonsense. Check:
- What % of conversions have at least one known touch (UTM source/medium or referrer)? Below ~70%, flag that results will be noisy and instrumentation needs fixing first.
- Are UTM source/medium/campaign values consistent (`linkedin` vs `LinkedIn` vs `li`)? Normalize before modeling — this alone fixes half of most attribution confusion.
- Does signup resolve back to the anonymous visitor session (PostHog's identity merge on signup)? If not, pre-signup touches are invisible and results will undercount top-of-funnel channels.

Produce a short instrumentation-gap list before doing anything else.

### Step 2: Pull the Touch Journeys from PostHog
Query PostHog for each converting user's ordered touch history in the attribution window (`utm_source`/`utm_medium`/`utm_campaign` or referrer on each session, joined to the conversion event by person ID). Use PostHog's HogQL/Query API or its MCP integration if connected. Example journey:
```
user_abc | google/cpc (day -12) → linkedin/organic (day -6) → direct (day -1) → SIGNUP
```

### Step 3: Compute Multiple Attribution Models, Not Just One
Report credit per channel under all of these — the spread between them is the point, since it's where a single-model number hides the disagreement:
- **First-touch** — 100% to the first channel (good for "what creates awareness")
- **Last-touch** — 100% to the last channel (what most ad platforms report by default, and why they all overclaim)
- **Linear** — equal credit across every touch
- **Position-based (40/20/40)** — first and last touch weighted heavier than the middle
- **Time-decay** — more recent touches get more credit

### Step 4: Add the Assist View
For each channel, separately report: conversions where it was the *only* touch (solo), conversions where it was present but not alone (assist), and how often it shows up first/middle/last. This is what surfaces channels that never get last-click credit but are present in most journeys — often SEO, organic social, or content.

### Step 5: Reconcile Against What Each Platform Claims
Compare the model's channel-level numbers against what Google Ads, Meta, LinkedIn Ads etc. self-report for the same period. Explain the gap plainly: ad platforms use their own attribution windows and view-through credit, which is why the same conversion gets claimed by two or three platforms at once. This reconciliation table is usually the single most useful output for a founder deciding what to cut.

### Step 6: Recommend One Model as the Source of Truth
Pick one model (usually linear or position-based for SaaS with multi-touch consideration cycles, last-touch only for very short/impulse signups) based on sales cycle length and data completeness. State the reasoning in one paragraph. This is the number that should feed growth-dashboard-builder and any spend decisions — keep a second model only as a sanity check, not as a competing "truth."

### Step 7: Self-Validation
Before presenting output, confirm:
- [ ] Instrumentation gaps are reported before any attribution numbers, if data quality is under ~70% touch coverage
- [ ] At least 3 attribution models are computed and compared, not just one
- [ ] The assist view is included so under-credited channels (usually organic/content) are visible
- [ ] One model is explicitly named as the source of truth going forward, with reasoning
- [ ] The reconciliation against vendor-reported numbers is included and explains the discrepancy, not just states it

## Output Schema
```json
{
  "instrumentation_gap_pct": "number",
  "channel_credit_by_model": {
    "first_touch": {"channel": "credit_pct"},
    "last_touch": {"channel": "credit_pct"},
    "linear": {"channel": "credit_pct"},
    "position_based": {"channel": "credit_pct"},
    "time_decay": {"channel": "credit_pct"}
  },
  "assist_view": [
    {"channel": "string", "solo_pct": "number", "assist_pct": "number", "first_pct": "number", "last_pct": "number"}
  ],
  "recommended_model": "string",
  "recommended_model_rationale": "string",
  "vendor_reconciliation": [
    {"channel": "string", "vendor_reported": "number", "model_credited": "number", "gap_explanation": "string"}
  ]
}
```

## Output Format
```markdown
# Attribution Report — [time period]

## Instrumentation Check
[% of conversions with known touch] — [note if this is a data quality flag]

## Channel Credit by Model
| Channel | First-touch | Last-touch | Linear | Position | Time-decay |
|---|---|---|---|---|---|
| [channel] | [%] | [%] | [%] | [%] | [%] |

## Assist View (who gets under-credited)
| Channel | Solo | Assist | First | Last |
|---|---|---|---|---|
| [channel] | [%] | [%] | [%] | [%] |

## Recommended Source of Truth: [model name]
[One paragraph rationale]

## Reconciliation vs. Vendor-Reported Numbers
| Channel | Vendor Claims | Model Credits | Why the Gap |
|---|---|---|---|
| [channel] | [n] | [n] | [explanation] |

## Do Not
- Trust last-click-only numbers when deciding to cut a channel's budget
- Sum every ad platform's self-reported conversions (they double- and triple-count the same user)
- Build this model if fewer than 70% of conversions have a known touch — fix instrumentation first
```

## Error Handling
- Touch coverage under ~70% → stop, report the instrumentation gap and what to fix (UTM tagging discipline, identity resolution on signup) before producing model numbers
- No PostHog access / no UTM data at all → explain the minimum needed (consistent UTM parameters on every campaign link, PostHog capturing `$referrer` and UTM properties) and stop rather than fabricate channel splits
- Vendor-reported numbers not provided → skip the reconciliation table section, note it as unavailable rather than guessing platform-claimed figures
- User wants to defund a channel based on last-touch alone → show the assist view first; a channel with high assist/low last-touch may be load-bearing even though it never "closes"
- Fewer than ~30 converting users in the window → warn that model output is too noisy to act on, widen the time window

## Examples
**Example 1**
User: "Google Ads says it drove 70% of signups and LinkedIn says 60% — that's impossible."
Skill: Pulls PostHog touch journeys, computes all 5 models, shows both platforms are claiming the same multi-touch users under generous view-through windows, and recommends linear or position-based as the shared source of truth going forward.

**Example 2**
User: "I want to cut my content/SEO spend, it never shows conversions."
Skill: Runs the assist view specifically, shows SEO/organic content has a high assist rate even with near-zero last-touch credit, and flags that cutting it may quietly increase CAC on the channels that currently ride on top of it.

**Example 3**
User: "Where should my next $1,000 of ad spend go?"
Skill: Uses the recommended source-of-truth model plus channel-level CAC (fed from revenue-dashboard-builder if available) to rank channels by credited-conversions-per-dollar, not just raw conversion count.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- growth-dashboard-builder
- user-acquisition-analyzer
- ab-test-generator

### Fed By
- signup-conversion-tracker
- marketing-site-seo-audit

### Feedback Loop
Re-run this model every time a new channel is added or an existing one's spend changes materially — the credit split shifts as the channel mix shifts, and last quarter's "source of truth" model choice should be revisited if the sales cycle length changes.

```yaml
chain_metadata:
  skill_slug: "attribution-mapper"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "growth-dashboard-builder"
    - "user-acquisition-analyzer"
```
