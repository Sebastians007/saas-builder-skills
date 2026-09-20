---
name: full-funnel-campaign-orchestrator
description: >
  Coordinates which copy piece — ad, landing page, email, onboarding message —
  goes where across a full SaaS campaign, sequencing the other copywriting
  skills in order and checking messaging stays consistent from first touch to
  paid conversion.
  Use this skill when the user asks about building a full campaign, keeping
  messaging consistent across channels, or planning a launch sequence, or says
  "build me a full campaign", "coordinate my ads, landing page, and emails", "plan my launch messaging",
  "make sure this all matches", "I have separate copy for everything and it feels disjointed",
  "run the full copywriting process", "what order do I write all this copy in".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "orchestrator", "campaign-planning", "messaging-consistency"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Full-Funnel Campaign Orchestrator

This skill sequences the other copywriting skills into one coherent campaign, so the ad, the landing page, the trial emails, and the pricing page all trace back to the same avatar, offer, and awareness stage instead of being written separately and sounding like five different products.

## Stage
This skill belongs to Stage S4: Copywriting

## When to Use
- Launching a new campaign (ads, landing page, email sequence) that needs one consistent story end to end
- Existing copy pieces were written at different times and now contradict each other in tone or promise
- Planning which S3-Funnel-Build type (opt-in, tripwire, SaaS trial, etc.) pairs with which copy piece
- A new pricing tier or feature launch needs a full messaging pass across every touchpoint
- The user wants a repeatable process instead of writing each piece from scratch every time
- The user says "I have all these copy skills, what order do I actually run them in"

## Input Schema
```
campaign_goal: string              # e.g. "launch new pricing tier", "cold outbound to new segment"
product_or_service: string
channels_involved: string[]        # e.g. ["ads", "landing page", "email sequence", "onboarding"]
funnel_type: string?               # from funnel-select/funnel-builder-orchestrator (S3-Funnel-Build), if already chosen (e.g. "Free Trial / SaaS", "Lead Magnet / Opt-in")
existing_avatar_or_offer: object?  # outputs from avatar-extraction / offer-extraction, if already run
```

## Workflow
### Step 1: Run or Confirm the Foundation Skills
Before any channel-specific copy is written, confirm these exist (run them if missing, in this order):
1. `avatar-extraction` — who this campaign is for
2. `offer-extraction` — what's actually being promised
3. `schwartz-awareness-mapper` — per channel, since cold ads and warm retargeting are at different stages

Do not proceed to channel copy until these three are locked. This is the step most campaigns skip, and it's why the ad and the landing page end up telling different stories.

### Step 2: Generate the Angle and Headline Layer

### Step 3: Build the Objection-Handling Layer
Run `objection-crusher` once and distribute its output across the funnel — trust objections near the top of the landing page, price objections in the pricing FAQ, complexity objections in onboarding emails. One objection map, reused everywhere it's needed, not five separate ad-hoc FAQ sections.

### Step 4: Map Copy to Funnel Stage
Assign each generated piece to its place in the funnel, matching the awareness stage of the audience at that touchpoint:
- Cold ad / cold outbound: pain or curiosity angle, unaware/problem-aware messaging rules
- Landing page: offer-led, solution/product-aware messaging, objection handling below the fold
- Trial/onboarding emails: product-aware, complexity and time-to-value objections handled
- Pricing/upgrade emails: most-aware, direct offer, price and guarantee stated plainly

If a funnel_type from S9-Funnels was specified, align this mapping to that funnel's actual step sequence rather than a generic assumption.

### Step 5: Consistency Check
Read every piece back to back and confirm:
- Same avatar addressed throughout (no shift from "you" meaning an ops lead to "you" meaning a developer)
- Same core promise stated consistently, not contradicted between the ad and the pricing page
- No touchpoint pitches an offer the reader isn't ready for yet (see `schwartz-awareness-mapper`)

### Step 6: Self-Validation
- [ ] Avatar and offer are locked before any channel copy was generated
- [ ] Every channel's copy is traceable back to the same avatar/offer/awareness inputs
- [ ] Objection-handling copy is placed once and reused, not duplicated inconsistently
- [ ] Each touchpoint's messaging matches its audience's actual awareness stage
- [ ] A read-through of all pieces in sequence tells one consistent story, not five

## Output Schema
```json
{
  "campaign_goal": "string",
  "locked_avatar_summary": "string",
  "locked_offer_summary": "string",
  "funnel_map": [
    { "touchpoint": "string", "awareness_stage": "string", "angle_used": "string", "objection_handled": "string|null" }
  ],
  "consistency_check_passed": "boolean",
  "consistency_issues_found": ["string"]
}
```

## Output Format
```markdown
# Campaign: [campaign goal]

## Foundation (locked)
- Avatar: [one-line summary, link to full avatar-extraction output]
- Offer: [one-line summary, link to full offer-extraction output]

## Funnel Map
| Touchpoint | Awareness Stage | Angle | Objection Handled |
|---|---|---|---|
| Cold ad | ... | ... | ... |
| Landing page | ... | ... | ... |
| Trial email 1 | ... | ... | ... |
| Pricing email | ... | ... | ... |

## Consistency Check
[Pass / issues found and where]

## Next Steps
- [which skill to run next for any missing piece]
```

## Error Handling
- User wants to jump straight to writing ads without an avatar or offer → stop and run `avatar-extraction` and `offer-extraction` first; explain that skipping this step is why campaigns come out sounding disjointed
- Channels given don't match any known funnel type → build the funnel map generically from the channels listed rather than forcing an ill-fitting S9-Funnels template
- Consistency check finds contradictions between existing pieces → flag exactly which pieces conflict and on what claim, then recommend which piece is likely correct (usually the most recently validated offer) rather than silently picking one
- Very large campaign with many touchpoints → prioritize mapping the highest-traffic touchpoints first and note which lower-priority pieces are deferred

## Examples
**Example 1**
User: "We're launching a new Pro tier. I need ads, a landing page, and 3 onboarding emails."

**Example 2**
User: "Our landing page and our cold email don't feel like they're selling the same thing."
Skill: Reads both, finds the landing page pitches a most-aware "start your trial" offer while the cold email is reaching a problem-aware cold audience, flags the awareness-stage mismatch as the root cause, and rewrites the cold email to lead with pain instead of the offer, keeping the landing page as-is since it correctly targets warmer traffic.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- funnel-planner (S1-Research)
- ab-test-generator (S10-Growth)
- signup-conversion-tracker (S10-Growth)

### Fed By
- avatar-extraction (S2-Audience-Positioning)
- offer-extraction (S2-Audience-Positioning)
- schwartz-awareness-mapper (S2-Audience-Positioning)
- ad-angle-multiplier (S4-Copywriting)
- objection-crusher (S4-Copywriting)

### Feedback Loop
Conversion data at each funnel stage from `signup-conversion-tracker` should be mapped back to the specific touchpoint and angle that produced it, so the next campaign run starts from what's already proven to work for this avatar instead of a blank page.

```yaml
chain_metadata:
  skill_slug: "full-funnel-campaign-orchestrator"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "ab-test-generator"
    - "signup-conversion-tracker"
```
