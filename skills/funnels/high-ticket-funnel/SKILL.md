---
name: high-ticket-funnel
description: >
  Builds a long-form authority-and-proof sales funnel for offers $3,000+,
  combining content that warms cold traffic, a detailed sales page, and a
  booked-call CTA, for coaching programs, masterminds, and enterprise deals.
  Use this skill when the user asks about selling an expensive
  offer/program/service, or says
  "I'm selling a high-ticket program", "build me a long-form sales page",
  "how do I write case studies that sell", "help me price my premium offer without scaring people off",
  "I need a sales page that leads to a booked call", "what should my long-form sales page cover".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "high-ticket", "authority", "sales-page"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# High-Ticket Funnel

Every element of this funnel exists to build enough trust to justify a $3,000+ decision. Unlike `application-funnel`, which leads with qualification, this leans on authority content and a detailed long-form sales page to do the convincing before the call — better suited when the founder already has content/authority to lean on rather than needing to filter volume.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is $3,000+ (coaching programs, masterminds, done-for-you services, enterprise deals)
- The founder has existing authority content (blog, videos, case studies) that can warm cold traffic first
- `funnel-select` recommended `high-ticket-funnel` over `application-funnel` because qualification isn't the bottleneck — trust-building is
- The founder wants a detailed long-form pitch rather than a short application gate

## Input Schema
```
offer_name: string
price: number             # note: never displayed on the page itself
case_studies: [ { "client": string, "situation": string, "result": string, "timeline": string } ]
guarantee: string?
booking_tool: string?
```

## Workflow
### Step 1: Plan the authority content that warms traffic
Blog post, video, or case study that exists before the sales page — this does the job of earning attention before the pitch. If none exists yet, flag this as the highest-leverage missing piece.

### Step 2: Write the long-form sales page in this order
Headline (bold transformation statement) → opening story (empathize with the reader's situation) → the problem (articulated better than they'd state it themselves) → cost of inaction (what happens if they don't solve this) → the solution (the approach, not the product yet) → 3-5 case studies with real numbers → the offer (what's included, how it works) → who this is for/not for → about/credentials → investment frame (ROI, not cost) → FAQ (objection handling) → final CTA ("Apply Now" or "Book a Call").

### Step 3: Write case studies using the fixed template
Client (name, title) → situation (specific starting numbers) → challenge (what wasn't working) → solution (what was done together) → result (specific measurable outcome) → timeline → a direct quote. Populate from `case_studies`; if fewer than 3 exist, flag that this is the page's weakest point and prioritize collecting more before launch.

### Step 4: Apply high-ticket pricing psychology
Never show the price on the page — save it for the call. Frame everything as investment/ROI, not cost ("clients typically see X return within Y months"). Offer payment plans to reduce resistance. Anchor: "if this helps you add just one $10K client, it pays for itself 3x over" (using real, defensible numbers specific to the offer).

### Step 5: Set the CTA and booking flow
"Apply Now" or "Book a Call" — never a direct checkout button at this price point. Route to `application-funnel`'s booking flow if qualification is also needed.

### Step 6: Self-Validation
- [ ] Price never appears anywhere on the page
- [ ] At least 3 case studies exist with specific, real numbers (not vague "great results")
- [ ] The problem and cost-of-inaction sections are written in the reader's pain language, not feature language
- [ ] Investment framing is used throughout, not cost framing
- [ ] CTA leads to a call or application, never a direct-purchase button

## Output Schema
```
{
  "authority_content_plan": string,
  "sales_page_sections": [ { "section": string, "copy": string } ],
  "case_studies": array,
  "pricing_psychology_notes": string[],
  "benchmarks": object
}
```

## Output Format
```markdown
# High-Ticket Funnel: <Offer Name>

## Flow
Authority Content → Long-Form Sales Page → Application/Booking → Sales Call → Onboarding

## Long-Form Sales Page
<full section-by-section copy in fixed order>

## Case Studies
<using the fixed template, one per client>

## Pricing Psychology Notes
<investment framing, payment plans, ROI anchor>

## Benchmarks to Track
| Metric | Target |
|---|---|
| Sales page → apply/book | > 5% |
| Show rate | > 75% |
| Call → close | > 20-30% |
```

## Error Handling
- If fewer than 3 real case studies exist, don't fabricate them — build the page with what's real, flag the gap clearly, and recommend collecting testimonials as a priority before scaling traffic to this page.
- If the user wants to show price on the page, explain the psychology tradeoff (removes the qualifying conversation) but respect their decision if they insist — note it as a deviation from the recommended pattern.
- If no authority content exists at all and traffic is cold, warn that the sales page alone will likely underperform — recommend building at least one piece of warming content first.
- If ROI/investment claims in the copy aren't backed by real client data, flag them as unverifiable and suggest more conservative, defensible framing.

## Examples
**Example 1:** A business mastermind at $8,000/year has 5 real client case studies. The skill builds the full long-form page with all 5, uses an ROI anchor based on actual average client revenue increase, and routes the CTA to `application-funnel`'s qualification form since call volume is also a concern.

**Example 2:** A brand-new consultant has zero case studies yet for a $4,000 service. The skill builds the page structure but flags the case study section as the critical gap, suggesting 2-3 free or discounted pilot clients specifically to generate case study material before paid traffic starts.

**Example 3:** An enterprise software consultancy sells $15,000 implementation packages. The skill emphasizes credentials and "as featured in" trust builders in the About section since the buyer persona (enterprise IT decision-maker) weighs institutional credibility heavily.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/sales-page.html`
- `templates/booking-page.html`

## Flywheel Connections
### Feeds Into
- `funnel-copy` — writes the opening story, problem/cost-of-inaction, and objection-handling sections
- `application-funnel` — shares the booking/qualification flow when call volume needs filtering
- `signup-conversion-tracker` (S7-Growth) — measures sales-page-to-booking conversion

### Fed By
- `funnel-select` — confirms high-ticket authority-based approach fits over application-first
- `pricing-model-calculator` (S2-Planning) — confirms the $3,000+ threshold

### Feedback Loop
If sales-page-to-booking conversion is low despite strong traffic, the case study section is the most common weak point — check whether the numbers are specific and real before rewriting the headline or problem section.

```yaml
chain_metadata:
  skill_slug: "high-ticket-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "application-funnel"
    - "signup-conversion-tracker"
```
