---
name: webinar-funnel
description: >
  Builds a 4-page live webinar funnel — registration, confirmation, webinar
  room, and offer page — for mid-to-high-ticket offers that need education
  before the sale.
  Use this skill when the user asks about running a webinar to sell a
  product, or says
  "I want to sell through a webinar", "build my webinar registration page",
  "help me set up a live training funnel", "how do I pitch my offer at the end of a webinar",
  "what should my webinar registration page say", "I'm doing a live masterclass to sell".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "webinar", "education", "mid-ticket"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Webinar Funnel

The highest-converting format for offers in the $297-$2,000+ range where the buyer needs to be taught something and trust the founder before paying. A live (or scheduled-live) webinar does the convincing that a static sales page can't.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is $200-$2,000+ and requires the buyer to understand a concept before they'll buy
- The founder is comfortable presenting live (or recording once and running scheduled sessions)
- `funnel-select` recommended `webinar-funnel` for a mid/high-ticket, education-first offer
- There's an existing audience worth inviting to a live event
- If the founder wants a fully automated, on-demand version instead, use `evergreen-webinar-funnel`

## Input Schema
```
webinar_title: string
webinar_date: string
learning_outcomes: string[]        # 3 specific things they'll discover
host_name: string
host_credentials: string
offer_name: string
offer_price: number
offer_bonuses: [ { "name": string, "value": number } ]
guarantee: string?
```

## Workflow
### Step 1: Write the registration page
Required elements: headline in the "Free [Live/Masterclass]: How to [Specific Result] in [Timeframe]" pattern, clear date/time with timezone handling, the 3 `learning_outcomes`, host bio with authority markers, a simple name+email registration form, urgency (seat limit or countdown), social proof from past attendees if any exist.

### Step 2: Write the confirmation page
Confirm registration, give a calendar-add link, restate date/time, and — critically — deliver a short piece of pre-webinar content (video, PDF, or post) to build anticipation and reduce no-shows.

### Step 3: Plan the webinar room page
Video embed, live chat/Q&A if live, an offer-reveal CTA that appears at the pitch point (not before), a downloadable handout, and a countdown for replay viewers to create urgency.

### Step 4: Write the offer (sales) page
Recap the transformation promised in the webinar, expand problem/solution, full benefit stack with bonuses (pull from `funnel-copy`), clear pricing vs. value comparison, testimonials/case studies, FAQ addressing top objections, a guarantee, and a final CTA with real urgency (bonus deadline or price increase).

### Step 5: Write the 8-email sequence
Confirmation → day-before reminder → day-of AM reminder → live-start reminder → replay+offer → case study → FAQ → last-chance. Map to actual send times relative to `webinar_date`.

### Step 6: Self-Validation
- [ ] Registration headline names a specific result and timeframe, not vague "training"
- [ ] Confirmation page includes anticipation-building content, not just a calendar link
- [ ] Offer CTA on the webinar room page only appears at the pitch point, not immediately
- [ ] Benefit stack values on the offer page are defensible, not inflated
- [ ] Guarantee is stated plainly if one exists

## Output Schema
```
{
  "pages": [
    { "name": "registration_page", "copy": object },
    { "name": "confirmation_page", "copy": object },
    { "name": "webinar_room_page", "copy": object },
    { "name": "offer_page", "copy": object, "benefit_stack": array }
  ],
  "email_sequence": [ { "timing": string, "subject": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# Webinar Funnel: <Webinar Title>

## Flow
Registration → Confirmation → Webinar Room → Offer Page

## Page 1: Registration
<copy>

## Page 2: Confirmation
<copy>

## Page 3: Webinar Room
<structure, pitch timing>

## Page 4: Offer Page
<copy, benefit stack, guarantee, FAQ>

## Email Sequence
| Day | Email | Subject |
|---|---|---|

## Benchmarks to Track
| Metric | Good | Great | Elite |
|---|---|---|---|
| Registration rate | 20% | 35% | 50%+ |
| Show-up rate | 25% | 40% | 60%+ |
| Offer conversion | 2% | 5% | 10%+ |
```

## Error Handling
- If `learning_outcomes` are vague ("learn about marketing"), push for specific, promise-shaped outcomes before writing the registration headline.
- If the offer price and webinar depth mismatch (a $2,000 offer pitched after a 20-minute webinar with no real teaching), flag that the education needs more depth to earn that price point.
- If there's no guarantee and the price is high-ticket, note that risk reversal materially affects webinar conversion and ask if one can be offered.
- If the founder has never run a live webinar before, suggest starting with `evergreen-webinar-funnel` isn't necessarily easier — recommend a small live test run first to validate the pitch before automating it.

## Examples
**Example 1:** A SaaS founder runs a "How to Cut Onboarding Time in Half" webinar to sell a $997/year done-for-you setup service. Registration promises 3 specific outcomes tied to onboarding metrics; offer page stacks bonuses (templates, a Loom review, 30-day support) against a $2,000 anchor value.

**Example 2:** A GRC consultant hosts a "SOC 2 in 90 Days" masterclass to sell a $1,500 compliance sprint package. Confirmation page delivers a pre-webinar SOC 2 gap-analysis worksheet to build anticipation and reduce no-shows.

**Example 3:** A course creator with 8,000 email subscribers but no webinar experience wants to sell a $497 course. The skill recommends a first live test webinar (not evergreen yet) to validate the pitch, with a plan to convert to `evergreen-webinar-funnel` once the offer sequence is proven.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/registration-page.html`

## Flywheel Connections
### Feeds Into
- `evergreen-webinar-funnel` — once the live pitch is proven, automate it
- `funnel-copy` — writes the offer page benefit stack and objection handlers
- `signup-conversion-tracker` (S7-Growth) — measures registration-to-purchase live

### Fed By
- `optin-funnel` / `group-funnel` — existing list is the registration audience
- `funnel-select` — confirms webinar fits the price point and audience temperature

### Feedback Loop
If show-up rate stays below 25%, the fix is almost always the confirmation page and reminder emails, not the registration page — re-check the anticipation content and reminder timing before rewriting the pitch itself.

```yaml
chain_metadata:
  skill_slug: "webinar-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "evergreen-webinar-funnel"
    - "funnel-copy"
    - "signup-conversion-tracker"
```
