---
name: vsl-funnel
description: >
  Builds a Video Sales Letter funnel that replaces long-form sales copy
  with a persuasive video and a delayed CTA, followed by a streamlined
  order page, for offers in the $97-$2,000 range.
  Use this skill when the user asks about a video sales letter, VSL, or a
  video-led sales page, or says
  "I want to sell with a video instead of a long sales page", "build me a VSL funnel",
  "help me script my sales video", "when should the buy button appear on my video page",
  "I have a video that sells my product, how do I structure the page", "write my VSL script".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "vsl", "video", "sales-page"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# VSL Funnel

Uses a single persuasive video to do the job a long-form sales page would otherwise do, with the buy button revealed after a timed delay so the pitch lands before the ask. Works well for founders who'd rather record a video once than write and constantly tweak long-form copy.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is $97-$2,000 and the founder is comfortable presenting on camera or via voiceover
- A long-form sales page exists but isn't converting and video might land better
- `funnel-select` recommended `vsl-funnel` for a mid-ticket offer with no live-call requirement
- The founder wants a minimal, distraction-free page (headline + video + CTA only)

## Input Schema
```
product_name: string
price: number
video_length_minutes: number
cta_reveal_percent: number         # what % of the video plays before the CTA appears (typically 60-80%)
guarantee: string?
has_upsell: boolean
```

## Workflow
### Step 1: Script the video using the proven VSL structure
Hand off scripting to `funnel-copy` using this 7-part framework as the outline: pattern interrupt (0:00-0:30) → story/problem (relatable pain) → solution reveal (the product as the bridge) → proof (testimonials, case studies, credentials) → offer stack (product + bonuses with value anchoring) → price reveal & close (guarantee, urgency) → FAQ/objection handling. Scale timestamps to `video_length_minutes`.

### Step 2: Build the page layout
Minimal by design: headline (optional, above video) + video + CTA only. No navigation, no distractions. Dark background keeps focus on the video. Video should autoplay (muted with an unmute prompt on mobile), with no scrub bar so viewers can't skip to the pitch.

### Step 3: Set the timed CTA reveal
The CTA button stays hidden until the video reaches `cta_reveal_percent` of its runtime — this ensures the pitch (proof, offer stack) lands before the ask. Flag to the user this needs actual video-player event tracking to implement (timeupdate listener against playback position).

### Step 4: Build the order page
Streamlined order form, guarantee restated, a few testimonials as final reassurance. If `has_upsell` is true, plan a single one-click upsell after purchase with a visible decline option — don't stack more than one.

### Step 5: Write the thank-you/delivery page
Confirm purchase, deliver access/login details, set expectations for next steps.

### Step 6: Self-Validation
- [ ] Page has no navigation menu or competing links
- [ ] CTA reveal timing is set and matches `cta_reveal_percent`, not shown from the start
- [ ] Video script covers all 7 structural beats, not just a product pitch
- [ ] Order page has a stated guarantee if one exists
- [ ] Any upsell has a visible decline option

## Output Schema
```
{
  "video_script_outline": [ { "section": string, "timestamp_range": string, "purpose": string } ],
  "page_layout": { "sections": string[] },
  "cta_reveal_seconds": number,
  "order_page": object,
  "benchmarks": object
}
```

## Output Format
```markdown
# VSL Funnel: <Product Name>

## Flow
Traffic → VSL Page → Order Page → Thank You / Upsell

## Video Script Outline
| Section | Timestamp | Purpose |
|---|---|---|

## Page Layout
<minimal structure notes, CTA reveal timing>

## Order Page
<copy, guarantee, upsell if applicable>

## Benchmarks to Track
| Metric | Target |
|---|---|
| Watch 25% → watch 75% | > 40% |
| Click CTA → purchase | > 5% |
```

## Error Handling
- If `video_length_minutes` is under 5, warn that the full 7-part structure may feel rushed — suggest either trimming sections deliberately or extending runtime.
- If no video exists yet, this skill can produce the script outline but should flag clearly that the page can't be built until the video is recorded.
- If the CTA is set to reveal at 0% (immediately visible), flag that this defeats the VSL's core mechanic — the pitch needs to land before the ask.
- If `price` is high-ticket ($2,000+) with no live sales call anywhere in the flow, note that `high-ticket-funnel` or `application-funnel` may convert better at that price point since VSLs work best where the video alone can close the sale.

## Examples
**Example 1:** A course creator has a $297 course and wants to replace their underperforming long-form sales page with video. The skill scripts a 14-minute VSL with CTA reveal at 65% (~9 minutes in), keeps the page to headline+video+CTA, and adds a single $47 upsell after purchase.

**Example 2:** A SaaS founder wants a VSL for a $1,200 annual plan. The skill flags that annual SaaS plans at this price often benefit from a demo call instead, but proceeds with the VSL as requested, emphasizing ROI-focused proof in the offer stack section.

**Example 3:** A founder has a 3-minute product demo video and wants to use it as a VSL for a $197 product. The skill flags that 3 minutes is tight for the full 7-part structure, recommends condensing to pattern interrupt → solution → proof → close, and adjusts CTA reveal to 70%.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/vsl-page.html`

## Flywheel Connections
### Feeds Into
- `funnel-copy` — writes the full video script from this outline
- `ab-test-generator` (S7-Growth) — tests CTA reveal timing and headline presence
- `checkout-funnel-auditor` (S7-Growth) — audits the order page once live

### Fed By
- `funnel-select` — confirms VSL fits the price point and no-live-call requirement
- `optin-funnel` / `tripwire-funnel` — often the traffic source feeding into a VSL

### Feedback Loop
If `click CTA → purchase` conversion is weak but `watch 75%` is strong, the issue is the order page or price framing, not the video — check `checkout-funnel-auditor` before re-scripting the VSL.

```yaml
chain_metadata:
  skill_slug: "vsl-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "ab-test-generator"
    - "checkout-funnel-auditor"
```
