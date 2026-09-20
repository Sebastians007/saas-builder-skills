---
name: product-launch-funnel
description: >
  Builds a Jeff Walker-style Product Launch Formula funnel using a sequence
  of 3 pre-launch content videos to build anticipation before opening cart
  for a limited window, for offers $297-$2,000+.
  Use this skill when the user asks about a multi-week product launch or
  cart-open/cart-close sequence, or says
  "I'm doing a big product launch", "build me a PLF-style funnel", "help me plan my pre-launch content",
  "how do I build anticipation before opening cart", "I want a limited-time cart open window",
  "set up my launch sequence".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "product-launch", "anticipation", "urgency"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Product Launch Funnel

Builds anticipation over 1-2 weeks with three free pre-launch content (PLC) videos, then opens cart for a hard, real deadline. This is a bigger commitment than a webinar or challenge — it suits a major launch (new course, new product line, annual re-launch) rather than an evergreen sales motion, since the cart-close mechanic only works if it's genuinely limited.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- A significant new offer ($297-$2,000+) is launching and justifies a multi-week buildup
- The founder has (or can create) 3 pieces of genuinely valuable teaching content to release in sequence
- `funnel-select` recommended `product-launch-funnel` for a major course/membership/high-ticket launch
- This is not meant to run constantly — it's an event, typically once or twice a year per offer

## Input Schema
```
offer_name: string
offer_price: number
plc_video_topics: [ { "sequence": number, "title": string, "core_teaching": string } ]  # 3 videos
launch_start_date: string
cart_open_date: string
cart_close_date: string
```

## Workflow
### Step 1: Confirm this is genuinely a launch, not routine sales
Ask whether cart will actually close after `cart_close_date` — if the founder plans to quietly reopen it next week, this funnel format is the wrong choice; recommend `vsl-funnel` or `webinar-funnel` for an always-on motion instead. A fake deadline destroys trust the first time someone catches it.

### Step 2: Write the opt-in/waitlist page
Captures leads for the launch list 2-4 weeks before launch starts.

### Step 3: Plan the 3 PLC video pages
PLC 1 (The Opportunity) — shows the gap/opportunity, day 1 of launch. PLC 2 (The Transformation) — teaches a real concept, proves credibility, day 3-4. PLC 3 (The Blueprint) — gives an actionable framework and seeds the offer, day 6-7. Each page needs the video, key takeaways listed below it, an engagement CTA, a countdown to the next video or cart open, and social share buttons.

### Step 4: Write the sales page for cart-open
Full offer presentation opens on `cart_open_date`. This is where `offer_price` and the full benefit stack appear — the PLC videos should NOT reveal price, only build toward the offer.

### Step 5: Plan cart close
A real, enforced deadline on `cart_close_date`. Final urgency push in the last 24-48 hours before close.

### Step 6: Write the full email sequence
Welcome → PLC1 launch + reminder → PLC2 launch + reminder → PLC3 launch → cart open → social proof → FAQ/objections → 24hr warning → cart close.

### Step 7: Self-Validation
- [ ] Cart close date is a real, enforced deadline — confirmed with the founder, not assumed
- [ ] Price is not revealed until the cart-open sales page, not in the PLC videos
- [ ] Each PLC video delivers genuine standalone value, not just teasers
- [ ] The offer is seeded (mentioned as "coming") in every PLC video, not hidden until cart open
- [ ] Email sequence timing maps to the actual `launch_start_date` through `cart_close_date` window

## Output Schema
```
{
  "opt_in_page": object,
  "plc_pages": [ { "sequence": number, "title": string, "key_takeaways": string[] } ],
  "sales_page": object,
  "email_sequence": [ { "day": number, "subject": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# Product Launch Funnel: <Offer Name>

## Flow
Opt-In/Waitlist → PLC 1 → PLC 2 → PLC 3 → Cart Open (Sales Page) → Cart Close

## Opt-In / Waitlist Page
<copy>

## PLC Video Pages
| Sequence | Title | Key Teaching | Timing |
|---|---|---|---|

## Cart-Open Sales Page
<copy>

## Email Sequence
| Day | Email | Subject |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Opt-in → watch PLC1 | > 60% |
| Sales page → purchase | > 5% |
```

## Error Handling
- If the founder can't commit to a real cart-close deadline, refuse to build the artificial-scarcity framing and recommend a different funnel type (`vsl-funnel`, `webinar-funnel`) that doesn't depend on a hard close.
- If `plc_video_topics` are thin or repeat the same idea 3 times, push for genuine progression — opportunity → transformation → blueprint should each teach something new.
- If price appears anywhere in the PLC video plans, flag it — revealing price early undercuts the "sideways sales letter" structure that makes PLF work.
- If the launch window is under 8 days total, warn that there may not be enough time to build real anticipation and suggest extending or switching formats.

## Examples
**Example 1:** A course creator launches a new $697 SaaS-for-marketers course twice a year. Three PLC videos cover "the opportunity in no-code marketing tools," "a live teardown of a real client's stack," and "the exact 5-step blueprint," with cart open for exactly 5 days.

**Example 2:** A SaaS founder wants to "launch" a feature update with fake urgency and reopen it whenever needed. The skill declines that framing, explains why repeated fake deadlines erode trust, and recommends `saas-funnel` or `vsl-funnel` for an ongoing sales motion instead.

**Example 3:** A membership site owner runs an annual re-launch of a $1,200 program. PLC videos are timed around a real cohort start date (the actual scarcity — limited onboarding capacity), making the cart-close deadline genuine rather than artificial.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/plc-video-page.html`

## Flywheel Connections
### Feeds Into
- `funnel-copy` — writes PLC video scripts and the cart-open sales page
- `signup-conversion-tracker` (S7-Growth) — measures the full launch funnel
- `membership-funnel` — if the launched offer is a recurring membership/cohort

### Fed By
- `funnel-select` — confirms a full launch format is justified over a lighter funnel
- `optin-funnel` — supplies the waitlist this launch converts

### Feedback Loop
If sales-page conversion is weak despite strong PLC engagement, the issue is usually the offer stack or price framing on the cart-open page, not the pre-launch content — review with `funnel-copy` before re-scripting the videos for the next launch cycle.

```yaml
chain_metadata:
  skill_slug: "product-launch-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "signup-conversion-tracker"
```
