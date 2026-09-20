---
name: membership-funnel
description: >
  Builds a recurring membership or subscription funnel — landing page,
  low-friction signup, retention-focused onboarding, and a churn-reduction
  email sequence — for communities, content libraries, and recurring SaaS.
  Use this skill when the user asks about selling a recurring
  membership/subscription, or says
  "I want to build a membership site", "help me reduce churn", "build my subscription funnel",
  "how do I retain members after signup", "I'm launching a paid community", "what should my onboarding look like for a membership",
  "my members keep canceling".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "membership", "retention", "churn", "subscription"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Membership Funnel

Built for recurring revenue where retention matters as much as acquisition — a paid community, content library, or SaaS-adjacent membership. Unlike a one-time-purchase funnel, half of this skill's job is what happens AFTER signup, because a member who churns in month one is worse than a lead who never converted.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The offer is a recurring membership, community, or content-library subscription (not core SaaS software — use `saas-funnel` for that)
- Signups exist but churn is high or retention hasn't been deliberately designed
- `funnel-select` recommended `membership-funnel` for a recurring content/community model
- Building the onboarding-to-retention loop for an existing membership that only ever focused on acquisition

## Input Schema
```
membership_name: string
price_monthly: number
price_annual: number?
trial_or_low_ticket_entry: string   # e.g. "7-day free trial" or "$1 first month"
whats_inside: string[]              # content categories/features
community_component: boolean
```

## Workflow
### Step 1: Write the landing page
Headline focused on community/transformation, not just feature list. Hero visual (screenshot of member area or community). "What's inside" section by content category. Member testimonials emphasizing both community AND results. Simple pricing (1-2 plans max — more choices hurt conversion here). FAQ covering cancellation policy plainly (hiding it erodes trust and increases chargebacks). Final CTA to start trial/low-ticket entry.

### Step 2: Design signup for minimum friction
Trial or low-ticket entry point per `trial_or_low_ticket_entry`, not a hard full-price commitment upfront unless the brand and audience trust level supports it.

### Step 3: Build the retention-critical onboarding flow
This is the most important part of the whole funnel: welcome + profile setup (personalization) → "what's your #1 goal?" (tailor experience) → recommend first action (immediate value) → tour of key features (reduce overwhelm) → join the community if `community_component` is true (social accountability). The goal is a genuine quick win inside the first 48 hours.

### Step 4: Write the retention email sequence
Welcome (login + quick-start) → quick win at +24hrs → community intro at +3 days → weekly value email (recurring) → engagement check at +14 days if inactive → win celebration monthly → pre-renewal value recap → cancellation-save offer triggered on cancel request.

### Step 5: Specify churn reduction tactics
First-48-hours quick win, community engagement (members who engage churn significantly less), visual progress tracking, content drip instead of dumping everything at once, an annual plan incentive, and a real cancellation flow that offers a pause option and a short survey before the account actually closes.

### Step 6: Self-Validation
- [ ] Onboarding is designed to deliver a real result within 48 hours, not just a feature tour
- [ ] Cancellation policy is stated plainly on the landing page FAQ, not buried or hidden
- [ ] Pricing has 1-2 plans, not a confusing menu
- [ ] Retention email sequence exists past the welcome email, not just an acquisition sequence
- [ ] A cancellation-save flow exists (pause option, survey, or offer) rather than an instant, frictionless-to-lose cancel with nothing offered

## Output Schema
```
{
  "landing_page": object,
  "signup_flow": object,
  "onboarding_steps": [ { "step": number, "screen": string, "goal": string } ],
  "retention_email_sequence": [ { "timing": string, "purpose": string } ],
  "churn_tactics": string[],
  "benchmarks": object
}
```

## Output Format
```markdown
# Membership Funnel: <Membership Name>

## Flow
Landing Page → Signup (Trial/Low-Ticket) → Onboarding → Member Area → Retention Loop

## Landing Page
<copy>

## Onboarding Flow
| Step | Screen | Goal |
|---|---|---|

## Retention Email Sequence
| Email | Timing | Purpose |
|---|---|---|

## Churn Reduction Tactics
<list>

## Benchmarks to Track
| Metric | Target |
|---|---|
| Trial → paid conversion | > 40% |
| Monthly churn rate | < 5% |
| LTV:CAC ratio | > 3:1 |
```

## Error Handling
- If cancellation policy isn't stated anywhere in the plan, stop and ask for it before finalizing the landing page FAQ — an undefined cancellation policy is a legal and trust risk.
- If onboarding has more than 5 steps, warn that overwhelm itself becomes a churn driver and suggest trimming to the essential path to first value.
- If no retention email sequence exists past a single welcome email, flag that acquisition-only thinking is the most common reason membership businesses stall.
- If pricing shows 3+ plans for a membership (vs. SaaS with clear tiered value), question whether the complexity is warranted — most memberships convert better with 1-2 clear options.

## Examples
**Example 1:** A SaaS-adjacent membership offers a $29/mo content library plus community for solo consultants. Onboarding gets new members to post an intro in the community and bookmark their first resource within the first session; retention sequence includes a weekly "member spotlight" email.

**Example 2:** A fitness membership at $19/mo has 22% monthly churn. The skill identifies no onboarding flow exists (members land straight in a content dump) and builds a 5-step onboarding sequence targeting a workout completed within 48 hours as the quick win.

**Example 3:** A GRC-focused paid community charges $49/mo for compliance templates and peer support. Landing page FAQ states the cancellation policy plainly (cancel anytime, no penalty) and the retention sequence includes a monthly "new templates added" email to justify ongoing value.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/landing-page.html`
- `templates/onboarding-flow.html`

## Flywheel Connections
### Feeds Into
- `onboarding-flow-builder` (S3-Building) — implements the onboarding steps technically
- `cohort-churn-analyzer` (S7-Growth) — measures actual churn against the targets set here
- `trial-to-paid-converter` (S7-Growth) — owns ongoing trial-to-paid optimization

### Fed By
- `funnel-select` — confirms membership is the right recurring model vs. `saas-funnel`
- `group-funnel` — a free community that's converting to a paid membership tier

### Feedback Loop
If `cohort-churn-analyzer` shows churn concentrated in month one, the onboarding quick-win step defined here is likely not landing — revisit Step 3 before touching pricing or the retention email cadence.

```yaml
chain_metadata:
  skill_slug: "membership-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "onboarding-flow-builder"
    - "cohort-churn-analyzer"
    - "trial-to-paid-converter"
```
