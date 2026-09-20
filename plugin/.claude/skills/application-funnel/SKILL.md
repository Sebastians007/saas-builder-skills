---
name: application-funnel
description: >
  Builds an application/qualification funnel for high-ticket offers ($2,000+)
  that filters leads through a qualifying application before they can book
  a sales call, for coaching, consulting, agencies, and premium programs.
  Use this skill when the user asks about qualifying leads before a sales
  call, or says
  "I want people to apply before booking a call with me", "build me an application funnel",
  "how do I filter out tire-kickers before my sales calls", "I'm selling a high-ticket coaching program",
  "what should my application form ask", "I'm wasting time on calls with people who can't afford it".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "high-ticket", "qualification", "sales-call"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Application Funnel

Filters leads through a qualifying application before they ever get a calendar link, so every sales call is with someone who's actually a fit. Built for offers where the founder's time on calls is the scarce resource — $2,000+ coaching, consulting, agency, or premium program offers.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is $2,000+ and sold via a sales call, not self-checkout
- The founder is currently taking calls with unqualified people and wasting time
- `funnel-select` recommended `application-funnel` for a high-ticket offer needing qualification
- Booking volume is fine but close rate is low because too many calls are with bad-fit leads

## Input Schema
```
offer_name: string
price_range: string                # e.g. "$3,000-$5,000"
budget_thresholds: string[]         # multiple choice ranges for the application form
disqualification_criteria: string[] # e.g. "budget below $X", "no urgency", "commitment score < 7"
booking_tool: string?               # Calendly, etc.
```

## Workflow
### Step 1: Write the landing page
Bold outcome headline (result-focused, not method-focused), "this is for you if..." qualifier bullets, "this is NOT for you if..." disqualifier bullets (this alone pre-filters a chunk of bad-fit traffic before they even apply), client results with specific numbers, a 3-step process overview, short credibility-focused bio, "Apply Now" CTA (never "Buy Now" — applications should feel exclusive, not transactional), FAQ on process/time commitment.

### Step 2: Build the application form
Qualifying questions: current situation/revenue, #1 goal for next 90 days, what they've already tried, a 1-10 commitment scale, and an investment-readiness question. Logistics: budget range (multiple choice matching `budget_thresholds`), start timeline, best phone number. Apply `disqualification_criteria` to route weak-fit applicants away from the booking calendar (a polite "not right now" page, not silence).

### Step 3: Design the booking and confirmation flow
Only qualified applicants see the calendar booking link. Confirmation page sets expectations for the call — what to expect, how long it runs, what to prepare.

### Step 4: Write the post-application email sequence
App received (immediate) → social proof/case study (+24hrs) → call prep (day before) → reminder with calendar link and phone number (1hr before) → no-show follow-up with reschedule link if missed.

### Step 5: Set conversion benchmarks
Landing → start application 15%+, complete application 60%+, complete → book call 40%+, show rate 70%+, call → close 20%+.

### Step 6: Self-Validation
- [ ] "This is NOT for you if" section exists and actually filters, not just decorative copy
- [ ] Disqualification criteria are applied consistently, not just described
- [ ] CTA language says "Apply" not "Buy" — matches the qualification framing
- [ ] Unqualified applicants get a respectful response, not silence or a dead end
- [ ] Post-application sequence includes a no-show recovery step

## Output Schema
```
{
  "landing_page": object,
  "application_form_questions": [ { "question": string, "type": string, "purpose": string } ],
  "disqualification_logic": string[],
  "email_sequence": [ { "timing": string, "purpose": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# Application Funnel: <Offer Name>

## Flow
Landing Page → Application Form → Calendar Booking → Confirmation

## Landing Page
<copy including qualifier/disqualifier bullets>

## Application Form
### Qualifying Questions
### Logistics
### Disqualification Triggers

## Post-Application Email Sequence
| Email | Timing | Purpose |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Landing → start application | > 15% |
| Complete → book call | > 40% |
| Call → close | > 20% |
```

## Error Handling
- If `price_range` is under $2,000, flag that an application step may add unnecessary friction at that price point — recommend `high-ticket-funnel` or `vsl-funnel` instead unless there's a specific qualification need (e.g., a cohort program with limited seats).
- If `disqualification_criteria` is empty, ask for at least budget and commitment thresholds — an application with no actual filtering logic is just an extra-long contact form.
- If there's no plan for what happens to disqualified applicants, flag this — leaving them with no response is a bad experience and a wasted lead.
- If the landing page CTA says "Buy Now" or similar direct-purchase language, correct it — that framing conflicts with the qualification premise.

## Examples
**Example 1:** A business coach sells a $5,000 6-month program. Application asks about current revenue, 90-day goal, budget range ($3K-$5K / $5K-$10K / $10K+), and commitment score; anyone under $3K budget or scoring below 7 on commitment gets a "not right now, here's a free resource" page instead of a booking link.

**Example 2:** An agency sells $8,000/mo retainers. The skill builds disqualifiers directly into the landing page copy ("NOT for you if you're pre-revenue or need results in under 30 days") to reduce low-fit applications before they even start the form.

**Example 3:** A founder wants an application funnel for a $497 course. The skill flags that the price point doesn't typically justify an application-and-call sales process, and recommends `vsl-funnel` or `webinar-funnel` instead, since the friction of applying would likely suppress conversion without adding real qualification value at that price.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/application-page.html`

## Flywheel Connections
### Feeds Into
- `funnel-copy` — writes landing page qualifier/disqualifier copy and objection handling
- `high-ticket-funnel` — shares the long-form authority-building approach for the landing page
- `signup-conversion-tracker` (S7-Growth) — measures application and booking conversion

### Fed By
- `funnel-select` — confirms application qualification fits the price point
- `pricing-model-calculator` (S2-Planning) — confirms the $2,000+ threshold that justifies this funnel

### Feedback Loop
If show rate stays under 70%, the fix is usually the confirmation/reminder sequence, not the application form — check the call-prep and 1-hour-before reminder emails before questioning the application questions themselves.

```yaml
chain_metadata:
  skill_slug: "application-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "signup-conversion-tracker"
    - "high-ticket-funnel"
```
