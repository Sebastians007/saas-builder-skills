---
name: optin-funnel
description: >
  Builds a simple 2-page email list funnel — a squeeze page that trades a
  lead magnet for an email address, and a thank-you page that delivers it
  and points to the next step.
  Use this skill when the user asks about building an email list, lead magnets,
  or a squeeze page, or says
  "I need to grow my email list", "help me build a lead magnet funnel", "what's a squeeze page",
  "I want to collect emails before I launch", "build me an opt-in page", "how do I get people's emails",
  "I have a free PDF/checklist to give away", "set up my lead capture page".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "lead-generation", "email-list", "landing-page"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Opt-In Funnel

The simplest funnel there is: one page to capture an email in exchange for something free, one page to deliver it and point to what's next. This is usually the first funnel a founder should build — before there's a product to sell, there should be a list of people who want to hear from them.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The founder has no email list yet and no product ready to sell
- There's a free resource (PDF, checklist, template, mini-course, free tool) worth trading for an email
- `funnel-select` recommended `optin-funnel` as the primary or fallback funnel
- Building the top-of-funnel step before a `tripwire-funnel`, `webinar-funnel`, or `saas-funnel` trial
- The user wants to validate interest in an idea before building the full product (pairs with `saas-idea-validator`)

## Input Schema
```
lead_magnet_name: string
lead_magnet_format: string        # "PDF" | "checklist" | "template" | "video" | "tool" | "spreadsheet"
target_audience: string
core_benefit: string              # what the lead magnet helps them do/avoid
next_step_after_optin: string?    # "tripwire offer" | "webinar" | "free trial" | "community" | "none yet"
brand_name: string
```

## Workflow
### Step 1: Confirm the lead magnet is genuinely useful
The whole funnel dies if the free thing isn't worth an email address. Ask: "Would a stranger trade their email for this, or is it just filler?" If it's vague ("a free guide"), push for something specific and immediately usable — a template, a checklist, a calculator, not a generic ebook.

### Step 2: Write the squeeze page
Single-purpose page, no navigation, no competing links. Required sections in order: benefit-driven headline, sub-headline naming exactly what they get, visual mockup of the lead magnet, 3-5 bullet points of what's inside, email opt-in form, one-line social proof, privacy reassurance line. Pull headline and bullet copy from `funnel-copy`.

### Step 3: Write the thank-you page
Confirm the opt-in, deliver the lead magnet inline (not just "check your email" — always give a direct link too), and introduce exactly one next step. If `next_step_after_optin` is set, that determines what shows here: a tripwire offer, a webinar registration link, a free trial signup, or a community invite.

### Step 4: Set delivery and follow-up
Specify the immediate delivery mechanism (auto-download link + email) and a short 2-3 email welcome sequence that delivers more value before ever asking for anything else.

### Step 5: Set benchmarks to track
Give the user real targets to check against once live: opt-in rate 25-50%+, thank-you page CTA click 10-30%+. Point to `signup-conversion-tracker` for ongoing measurement.

### Step 6: Self-Validation
- [ ] Squeeze page has no navigation menu or competing links
- [ ] Headline and bullets focus on the lead magnet's benefit, not its format
- [ ] Thank-you page delivers the asset immediately, not just via email
- [ ] Exactly one next-step CTA on the thank-you page — not three competing offers
- [ ] Benchmarks and a measurement plan are included

## Output Schema
```
{
  "pages": [
    { "name": "squeeze_page", "sections": string[], "copy": object },
    { "name": "thank_you_page", "sections": string[], "copy": object }
  ],
  "email_sequence": [ { "timing": string, "purpose": string } ],
  "benchmarks": { "optin_rate": string, "thankyou_cta_click": string }
}
```

## Output Format
```markdown
# Opt-In Funnel: <Lead Magnet Name>

## Flow
Traffic → Squeeze Page → Thank You Page

## Page 1: Squeeze Page
<section-by-section copy>

## Page 2: Thank You Page
<section-by-section copy, delivery link, next-step CTA>

## Welcome Email Sequence
| Email | Timing | Purpose |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Opt-in rate | 25-50%+ |
| Thank-you CTA click | 10-30%+ |
```

## Error Handling
- If no lead magnet exists yet, stop and help define one before building pages — an empty promise kills trust immediately.
- If the user wants to skip the thank-you page and redirect straight to a sales page, warn that this looks aggressive and hurts trust; recommend at minimum acknowledging the opt-in first.
- If `next_step_after_optin` is "none yet," still build the thank-you page but leave the CTA section as a placeholder with a clear note to fill in once decided.
- If the lead magnet format doesn't match its claimed value (e.g., "comprehensive guide" that's one page), flag the mismatch.

## Examples
**Example 1:** A SaaS founder building a project management tool has no product live yet but wants to validate demand. The skill builds a squeeze page offering a "5 Project Management Mistakes Killing Your Team's Deadlines" checklist, with the thank-you page inviting signups to the private beta waitlist as the next step.

**Example 2:** A course creator has a "30-Day Content Calendar Template" and wants list growth before launching a $297 course. Thank-you page next step is set to "tripwire offer" — a $17 companion workbook — turning some subscribers into buyers same-day.

**Example 3:** A GRC/compliance consultant offers a "SOC 2 Readiness Checklist" to freelance analysts. Squeeze page bullets emphasize time saved and audit-fail avoidance rather than the checklist's page count.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/squeeze-page.html`
- `templates/thank-you.html`

## Flywheel Connections
### Feeds Into
- `tripwire-funnel` — natural next step for a fresh opt-in list
- `webinar-funnel` / `evergreen-webinar-funnel` — opt-in list becomes webinar registration pool
- `saas-funnel` — opt-in list can be nurtured into free trial signups
- `signup-conversion-tracker` (S7-Growth) — measures this funnel once live

### Fed By
- `funnel-select` — confirms opt-in is the right funnel to build first
- `saas-idea-validator` (S1-Research) — the lead magnet often doubles as an idea validation test

### Feedback Loop
If `signup-conversion-tracker` shows opt-in rate well under 25%, the fix is almost always the lead magnet's perceived value or the headline — re-run `funnel-copy` for headline variants before touching page design.

```yaml
chain_metadata:
  skill_slug: "optin-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "signup-conversion-tracker"
    - "tripwire-funnel"
```
