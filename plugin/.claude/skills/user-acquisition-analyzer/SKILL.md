---
name: user-acquisition-analyzer
description: >
  Analyzes which user acquisition channels — SEO, cold outreach, communities,
  ads — actually fit a specific app and audience combination, and ranks them
  by realistic effort and return.
  Use this skill when the user asks about "how do I get users", "which marketing channel should I use",
  or says
  "how do I get my first 100 users", "should I do ads or cold outreach", "what channel fits my app",
  "where does my target customer actually hang out", "SEO vs. cold email for my app",
  "I don't know how to get users for this", "help me pick a growth channel".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "acquisition", "marketing-channels"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# User Acquisition Analyzer

This skill matches a specific app and target customer to the acquisition channels most likely to actually work — ranked by realistic effort, cost, and speed to first signal — instead of recommending a generic "do SEO and social media" list. It exists because channel choice should follow where the customer already is, not follow whatever channel is trendy.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- App is built or near-built and founder has no acquisition plan yet
- Founder is trying every channel at once with no traction and needs focus
- Founder is deciding between paid ads, cold outreach, content/SEO, or community engagement
- Founder has a specific advantage (existing audience, domain network, technical skill) that should shape channel choice
- Setting up the weekly experiment loop (per the user's own ES process) and needs a channel to test first

## Input Schema
```
product_description: string (required)
target_customer: string (required) — as specific as possible (role, industry, company size)
founder_assets: {
  existing_audience: string (optional) — e.g. "2k Twitter followers", "none",
  budget_for_ads: number (optional, default 0),
  time_available_per_week: string (optional),
  domain_network: string (optional) — e.g. "knows 50 real estate agents personally"
}
sales_motion: enum [self-serve, sales-assisted, high-touch-enterprise] (optional, infer if not given)
```

## Workflow
### Step 1: Find out where the target customer actually spends time
Use web_search to identify where `target_customer` congregates: specific subreddits, Slack/Discord communities, LinkedIn groups, industry forums, trade publications, or search behavior (do they Google their problem, or do they ask a peer?). This determines which channels are even reachable — a channel with no realistic access to the audience should be ruled out immediately, regardless of how well it worked for other SaaS products.

### Step 2: Match channel to sales motion
- **Self-serve, low price point**: content/SEO, communities, Product Hunt-style launches, and paid ads (if budget allows) tend to fit — customer can discover and buy without a human touch.
- **Sales-assisted (someone talks to the customer before they buy)**: cold outreach (per the user's own ES/cold-email process if applicable), LinkedIn, warm intros through `domain_network` fit better than pure content plays.
- **High-touch enterprise**: outreach and network/referral-based channels dominate early; content/SEO is a much longer-horizon play here and shouldn't be the first bet.

### Step 3: Weight by founder's actual assets
An `existing_audience` changes everything — if the founder has real reach already, activating it beats starting a new channel cold. A real `domain_network` (people who know and trust the founder in the target industry) is often the highest-signal, lowest-cost channel available and gets underweighted by generic advice. Zero budget rules out paid ads regardless of fit.

### Step 4: Rank channels by speed-to-signal, not just theoretical fit
For each viable channel, estimate how fast it can produce real signal (a reply, a signup, a "yes I'd pay for this") — this matters more early on than long-term scalability. Cold outreach and warm network asks typically produce signal in days; SEO/content typically takes months. Recommend starting with the fastest-signal channel that fits, then layering in slower-compounding channels once the message/product is validated.

### Step 5: Set up one channel as the first test, following one-mode-per-sprint discipline
Recommend exactly one primary channel to run as a focused sprint (matching the user's own ES process: one mode, 10-30 attempts/day, one week, hard thresholds for scale/pivot/kill) rather than spreading thin across three channels at once. Name the other viable channels as the backlog for subsequent sprints.

### Step 6: Self-Validation
- [ ] Channel recommendations are grounded in where the actual target customer is found (checked via web_search), not generic advice
- [ ] Founder's real assets (audience, network, budget, time) were factored in, not ignored
- [ ] Sales motion was matched correctly to channel type
- [ ] Output names exactly one channel to start with, not a scattered list
- [ ] Speed-to-signal was considered, not just theoretical channel fit

## Output Schema
```
{
  where_customer_is: string[],
  viable_channels: [{ channel: string, fit_reason: string, speed_to_signal: string, cost: string }],
  ruled_out_channels: [{ channel: string, why_ruled_out: string }],
  recommended_first_channel: string,
  sprint_plan: string
}
```

## Output Format
```markdown
# Acquisition Channel Analysis: <app name>

## Where Your Customer Actually Is
- ...

## Viable Channels
| Channel | Why It Fits | Speed to Signal | Cost |
|---|---|---|---|
| ... | ... | ... | ... |

## Ruled Out
- **<channel>**: <why it doesn't fit this app/founder/budget>

## Start Here: <recommended channel>
<why this one first, and the one-sprint test plan — target attempts/day, what a pivot/kill signal looks like>

## Backlog (next sprints)
- ...

## Next Step
Run `signup-conversion-tracker` once the channel is live to measure real results, or return here to test the next channel after this sprint's decision point.
```

## Error Handling
- If `target_customer` is too broad to locate ("everyone who owns a small business"), ask for narrowing before recommending channels — channel-customer fit can't be assessed against a vague audience.
- If founder has zero budget, zero existing audience, and zero domain network, say plainly that outreach/community engagement (time-cost only) is the realistic starting point, not paid channels.
- If web_search can't confirm where the audience congregates online (very offline-first customer, e.g. local service businesses), recommend offline/referral-based channels and say so rather than forcing a digital-only answer.
- If the founder insists on running 3+ channels simultaneously against the recommended one-mode discipline, note the tradeoff plainly (diluted attempts, harder to attribute what worked) but respect their choice.

## Examples
**Example 1**
User: "I built a tool for wedding photographers to deliver galleries faster. I know maybe 30 photographers personally from my old job."
→ Skill identifies domain_network as the strongest asset, recommends warm outreach to the 30 known photographers as the first-sprint channel (fastest signal, near-zero cost), flags photography Facebook groups/subreddits as backlog channels for later.

**Example 2**
User: "B2B SaaS for accounting firms, $50k marketing budget, no existing audience."
→ Skill checks where accounting firm decision-makers are (industry associations, LinkedIn, specific trade publications), recommends sales-assisted outreach + targeted LinkedIn ads as the first-sprint combination, rules out consumer-style Product Hunt-type launches as poor fit for the sales motion.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `signup-conversion-tracker` (S7-Growth) — tracks real results of the chosen channel
- `funnel-planner` (S8-Meta) — channel choice feeds the broader funnel design
- `ab-test-generator` (S7-Growth) — tests message variants within the chosen channel

### Fed By
- `unique-value-prop-audit` (S1-Research) — sharpened messaging should be used in whichever channel is chosen
- `launch-directory-submitter` (S1-Research) — launch is often the first acquisition test; this plans what comes after

### Feedback Loop
Weekly scale/pivot/kill decisions from the actual channel sprint should feed back into this skill's channel-ranking logic — a channel that consistently underperforms its predicted speed-to-signal for a given audience type should be deprioritized in future recommendations for similar audiences.

```yaml
chain_metadata:
  skill_slug: "user-acquisition-analyzer"
  stage: "research"
  timestamp: string
  suggested_next:
    - "signup-conversion-tracker"
    - "funnel-planner"
```
