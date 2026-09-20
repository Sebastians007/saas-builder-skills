---
name: ad-angle-multiplier
description: >
  Takes one core SaaS offer and generates multiple genuinely distinct
  marketing angles and hooks from it, so testing covers real different ideas
  instead of five minor rewrites of the same ad.
  Use this skill when the user asks about generating more ad ideas, creative
  variation, or new angles for a campaign, or says
  "give me more ad angles", "I need new hooks for this offer", "we're out of ad ideas",
  "these ads all feel the same", "generate different angles to test", "scale my ad testing",
  "our CTR is dropping, we need fresh creative".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "ad-angles", "creative-testing", "positioning"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Ad Angle Multiplier

This skill takes one locked offer and multiplies it into distinct marketing angles — different core ideas, not different adjectives on the same idea. It exists for the moment testing plateaus because every new ad is really the same ad wearing a different headline.

## Stage
This skill belongs to Stage S4: Copywriting

## When to Use
- Ad performance is flattening and new creative is needed, not just new copy
- The founder has one offer but only one angle they keep rewriting
- Preparing a batch of test creative for a new channel (ads, cold email, LinkedIn outbound)
- Feeding `full-funnel-campaign-orchestrator` with enough real variation to run a proper weekly test sprint
- The user's Execution Squad outreach sprint needs 10-30 attempts/day of genuinely different messages, not the same message copy-pasted
- The user says every ad they write "feels the same" or CTR/reply rate has stalled

## Input Schema
```
core_promise: string                  # from offer-extraction
primary_avatar: object?               # from avatar-extraction, if run
awareness_stage: string?              # from schwartz-awareness-mapper, if run
channel: string?                      # e.g. "cold email", "LinkedIn ad", "Facebook ad"
angle_count_requested: number?        # default 12
```

## Workflow
### Step 1: Confirm the Offer Is Locked First
This skill multiplies angles on ONE offer — it doesn't multiply offers. If `core_promise` is missing or unclear, recommend running `offer-extraction` first; generating 12 angles on a fuzzy offer just produces 12 fuzzy ads.

### Step 2: Generate Angles Across Six Distinct Sources
Produce at least one angle in each category, using the avatar and awareness stage if available to sharpen specifics:
- **Pain** — leads with the specific frustration of the status quo ("Still reconciling invoices in three spreadsheets?")
- **Desire** — leads with the outcome state, the after-picture ("Every client's retainer status, one glance, always current")
- **Proof** — leads with a number, result, or case study ("Agencies using [product] cut billing errors by 80%")
- **Identity** — speaks to who the reader is or aspires to be ("For ops leads who refuse to let a client see a billing mistake")
- **Contrarian** — challenges a common belief in the market ("More project management features won't fix this. Better retainer tracking will.")
- **Urgency** — the real cost of continuing to wait, not manufactured scarcity

### Step 3: Enforce Genuine Distinctness
Each angle needs to work as a completely separate ad if the others were deleted — different opening line, different core idea, different reason to keep reading. Reject a batch where angles only differ by synonym swaps.

### Step 4: Write the Hook Line for Each
An angle alone isn't testable — write the actual first line (the hook) a prospect would see, in the format appropriate to the channel (ad headline, cold email first line, LinkedIn post opener).

### Step 5: Self-Validation
- [ ] All six angle sources are represented (or explicitly noted as skipped with reason)
- [ ] No two angles could be mistaken for rewrites of each other
- [ ] Every angle has an actual hook line written, not just a category label
- [ ] Angles are specific to this product and avatar, not generic enough to run for a competitor
- [ ] If a channel was specified, hook format matches that channel's norms

## Output Schema
```json
{
  "core_promise": "string",
  "channel": "string|null",
  "angles": [
    { "source": "pain|desire|proof|identity|contrarian|urgency", "angle_summary": "string", "hook_line": "string" }
  ],
  "recommended_test_order": ["string"]
}
```

## Output Format
```markdown
# Ad Angles: [product name]

## Pain
**Angle:** [summary]
**Hook:** "[actual first line]"

## Desire
**Angle:** [summary]
**Hook:** "[actual first line]"

## Proof
...

## Identity
...

## Contrarian
...

## Urgency
...

## Recommended Test Order
1. [angle] — [why test this first]
2. [angle]
3. [angle]
```

## Error Handling
- No offer given → recommend running `offer-extraction` first; state that angle variation on an unclear offer doesn't produce useful test data
- User asks for angles but keeps rejecting them as "too different from our brand" → clarify that testing genuinely different angles is the point; if brand voice constraints are real, apply them as a tone filter after the angle is chosen, not before it's generated
- No proof points available for the proof angle → mark it as placeholder and recommend pulling a real stat before running that specific angle live
- Requested count is very high (50+) → generate a strong 12-18 with real distinctness rather than padding to the requested number with filler variants

## Examples
**Example 1**
User: "We keep running the same 'save time with automation' ad and CTR is dropping."
Skill: Generates six distinct angles including a contrarian one ("Automation isn't the problem. You're automating the wrong step.") and an identity one ("For the ops lead tired of being the human sync layer between three tools"), each with a real hook line ready to run, plus a recommended test order starting with pain and contrarian since desire has already been tested heavily.

**Example 2**
User: "I need 15 cold email openers for our outbound sprint this week."
Skill: Produces angles formatted as cold email first lines rather than ad headlines, front-loads pain and proof (higher reply-rate categories for cold outbound), and flags which angles pair with the current awareness stage from `schwartz-awareness-mapper` if that was already run.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- ab-test-generator (S10-Growth)
- full-funnel-campaign-orchestrator (S4-Copywriting)

### Fed By
- offer-extraction (S2-Audience-Positioning)
- schwartz-awareness-mapper (S2-Audience-Positioning)

### Feedback Loop
Reply-rate and CTR data from the live sprint should be logged back against each angle source — angles that consistently underperform get dropped from future batches, and winning angle sources get weighted higher next time this skill runs for the same avatar.

```yaml
chain_metadata:
  skill_slug: "ad-angle-multiplier"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "ab-test-generator"
    - "full-funnel-campaign-orchestrator"
```
