---
name: evergreen-webinar-funnel
description: >
  Builds an automated "just-in-time" webinar funnel that simulates a live
  session on-demand so leads can register and watch at a scheduled slot
  without the founder presenting live every time.
  Use this skill when the user asks about automating a proven webinar, or says
  "I want my webinar to run on autopilot", "build me an evergreen webinar funnel",
  "how do I sell without hosting live every time", "automate my webinar pitch",
  "set up a just-in-time registration page", "turn my live webinar into evergreen".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "webinar", "automation", "evergreen"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Evergreen Webinar Funnel

Takes a proven live webinar pitch and runs it on-demand around the clock, using scheduled "next available session" slots so it still feels time-bound rather than an obviously pre-recorded video. Only build this after the live version (`webinar-funnel`) has proven the pitch converts — automating an unproven pitch just scales a broken funnel faster.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- A live webinar pitch has already converted at least a handful of times and the founder wants to stop presenting it manually
- The founder wants webinar-style education-before-sale conversion without live hosting overhead
- Traffic volume justifies a 24/7 registration flow instead of scheduled live events
- `funnel-select` recommended this as a scaling step after `webinar-funnel`

## Input Schema
```
webinar_recording_source: string   # description of the proven live recording being repurposed
session_times_offered: string[]    # e.g. "15 min from now", "tomorrow 10am", "tomorrow 7pm"
offer_reveal_timestamp: string     # e.g. "42:00" — when the CTA should appear in the video
replay_window_hours: number
offer_name: string
offer_price: number
```

## Workflow
### Step 1: Confirm the pitch is proven, not experimental
Ask whether this exact webinar has converted live at least a few times. If not, recommend running `webinar-funnel` live first — automating an unvalidated pitch wastes ad spend at scale instead of at small volume.

### Step 2: Write the registration page with session-time framing
Offer 3-4 "next available" time slots (e.g., "Starting in 15 minutes," "Today at [time]," "Tomorrow at 10am," "Tomorrow at 7pm") generated dynamically relative to the visitor's registration time, with a countdown once a slot is picked to build urgency to actually show up.

### Step 3: Design the watch page to feel live without faking it
No scrub bar, no ability to skip ahead — plays linearly like a live session. A "people watching now" indicator is fine if realistic; do not fabricate a live chat with messages attributed to real people who aren't actually there. The offer CTA appears at `offer_reveal_timestamp`, not before.

### Step 4: Set the replay window
Time-limit replay access (typically 24-48 hours per `replay_window_hours`) and make sure any "limited time" framing in the offer is actually honored — don't show an "expiring" bonus again after it claims to expire.

### Step 5: Write the reminder and follow-up email sequence
Confirmation (session time + calendar link) → 1-hour-before reminder → 5-minute-before reminder → replay link (+4hrs after session) → offer reminder (+24hrs) → last chance before replay expires (+48hrs).

### Step 6: Self-Validation
- [ ] Session times are dynamically generated relative to registration time, not static/stale
- [ ] No fabricated live chat messages attributed to fake attendees
- [ ] The page doesn't explicitly claim to be live if it isn't — transparency about pre-recorded content is maintained where it matters
- [ ] Replay window and any "expiring" offer framing are both actually honored
- [ ] Offer CTA timing matches `offer_reveal_timestamp`, verified against the actual recording

## Output Schema
```
{
  "registration_page": { "session_times": string[], "copy": object },
  "watch_page": { "offer_reveal_timestamp": string, "copy": object },
  "offer_page": object,
  "email_sequence": [ { "timing": string, "purpose": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# Evergreen Webinar Funnel: <Offer Name>

## Flow
Traffic → Registration (pick a session time) → Watch Page (simulated live) → Offer Page → Checkout

## Registration Page
<session time options, copy>

## Watch Page
<live-like UI notes, offer reveal timing>

## Email Sequence
| Email | Timing | Purpose |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Registration rate | > 30% |
| Show rate | > 35% |
| Overall reg → purchase | > 2% |

## Ethical Guidelines
- Be transparent that sessions are pre-recorded where relevant, or avoid explicitly claiming "live" if not
- Never fabricate chat messages from people who aren't real
- Honor every stated deadline and replay window exactly as promised
```

## Error Handling
- If the pitch hasn't been validated live yet, stop and recommend `webinar-funnel` first rather than automating a guess.
- If the user wants to fake a live chat with scripted "attendee" messages presented as real people, refuse that specific request and offer an honest alternative (a real "watching now" counter, genuine past testimonials instead).
- If `offer_reveal_timestamp` isn't provided, ask for it — showing the CTA too early undercuts the education-first structure that makes webinars convert.
- If replay window promises conflict with actual system capability (e.g., "48-hour replay" but no expiry mechanism exists), flag the gap before it ships.

## Examples
**Example 1:** A SaaS founder's live webinar for a $997 onboarding service converted well in 4 live runs. The skill builds the evergreen version with 4 rotating session times, a 48-hour replay window, and an honest "pre-recorded training" framing in the footer while keeping the "just in time" registration urgency.

**Example 2:** A course creator wants fake attendee chat messages to make the room feel busier. The skill declines that specific piece, explains the trust risk, and offers a real "X people registered this week" stat and genuine past-attendee testimonials as the alternative.

**Example 3:** A consultant's live pitch has never run before — they want to go straight to evergreen to "save time." The skill recommends at least 2-3 live test runs first via `webinar-funnel` to validate the offer reveal timing and objection handling before automating it.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/registration-page.html`
- `templates/watch-page.html`

## Flywheel Connections
### Feeds Into
- `signup-conversion-tracker` (S7-Growth) — measures registration and show rates live
- `ab-test-generator` (S7-Growth) — tests session-time framing and offer reveal timing

### Fed By
- `webinar-funnel` — the live version this automates; must be proven first
- `funnel-copy` — supplies registration and offer page copy

### Feedback Loop
If show rate on the evergreen version is meaningfully lower than the live version was, the session-time framing or reminder timing is usually the culprit — compare against the original live funnel's reminder cadence before touching the offer itself.

```yaml
chain_metadata:
  skill_slug: "evergreen-webinar-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "signup-conversion-tracker"
    - "ab-test-generator"
```
