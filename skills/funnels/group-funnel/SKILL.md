---
name: group-funnel
description: >
  Builds a 2-page funnel that drives free signups into a community group on
  Skool, Whop, Discord, Facebook Groups, or Circle, using a lead magnet as
  the hook and a dedicated community-focused thank-you page.
  Use this skill when the user asks about growing a community group, Skool,
  Discord server growth, or says
  "I want to grow my Skool community", "help me get more members in my Discord",
  "build a funnel for my Facebook group", "I'm launching a Whop community",
  "how do I get people to join my group", "build a community opt-in page".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "community", "lead-generation", "landing-page"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Group Funnel

A 2-page funnel built specifically for driving signups into a community group rather than just an email list. Works with any platform — Skool, Whop, Discord, Facebook Groups, Circle, Mighty Networks. The difference from a plain `optin-funnel` is the thank-you page: instead of just delivering a lead magnet, it actively sells the community itself and pushes the join click.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The founder is building or growing a community around their SaaS product or expertise (Skool, Discord, Whop, Facebook Group)
- The goal is community membership growth, not just an email list
- A free or paid community is the core product, or a feed for a paid offer later
- `funnel-select` recommended `group-funnel` because the destination is a named community platform
- Building a support/user community around an existing app (pairs with `onboarding-flow-builder` for in-app community prompts)

## Input Schema
```
community_platform: string        # "Skool" | "Whop" | "Discord" | "Facebook Group" | "Circle" | other
community_url: string
community_name: string
lead_magnet_name: string
lead_magnet_format: string
target_audience: string
community_perks: [ { "title": string, "description": string } ]   # 4 recommended
brand_name: string
```

## Workflow
### Step 1: Confirm the lead magnet AND the community value stand alone
Two things have to be sold here, not one: the free lead magnet (gets the email) and the community itself (gets the join click). If the community has no clear ongoing value beyond "more content," help the user name 3-4 concrete perks (live sessions, resource library, weekly challenges, direct access) before writing copy.

### Step 2: Write the opt-in page
Required sections in order: announcement top bar, hero (benefit headline + audience-specific sub-headline), lead magnet visual, 4-5 bullet benefits, opt-in form (name + email), social proof bar (member count, stars), privacy line. No navigation, no competing CTAs, no pricing.

### Step 3: Write the thank-you page
This page does the real work — deliver the lead magnet AND convert to a community join. Required sections: success confirmation, lead magnet delivery, community CTA card (headline selling the community + 4-perk grid + join button linking to `community_url` + "free to join" note if applicable), social share buttons.

### Step 4: Fill every placeholder
List out all variables the user must supply — lead magnet name, headline, target audience phrase, brand name/initial, bullet copy, CTA text, social proof numbers, avatar initials, perk titles/descriptions, community platform name. Don't leave brackets in the final copy.

### Step 5: Set benchmarks
Opt-in rate 25-50%+, thank-you-to-group-join 15-40%+, social share 3-15%+. Recommend `signup-conversion-tracker` to monitor live.

### Step 6: Self-Validation
- [ ] Opt-in page has zero navigation and zero competing CTAs
- [ ] Thank-you page clearly sells the community, not just "click here to join"
- [ ] All 4 community perks are specific, not generic filler ("great content!")
- [ ] Every bracketed placeholder has been replaced with real copy
- [ ] Community URL and platform name are correct and match `community_platform`

## Output Schema
```
{
  "pages": [
    { "name": "optin_page", "sections": string[], "copy": object },
    { "name": "thank_you_page", "sections": string[], "copy": object, "perks": array }
  ],
  "benchmarks": { "optin_rate": string, "group_join_rate": string, "social_share_rate": string }
}
```

## Output Format
```markdown
# Group Funnel: <Community Name> on <Platform>

## Flow
Traffic → Opt-In Page → Thank You Page → Community Join (<community_url>)

## Page 1: Opt-In Page
<section-by-section copy>

## Page 2: Thank You Page
<confirmation, delivery, community CTA card with 4 perks, share buttons>

## Benchmarks to Track
| Metric | Good | Great | Elite |
|---|---|---|---|
| Opt-in rate | 25% | 35% | 50%+ |
| Thank-you → group join | 15% | 25% | 40%+ |
| Social share | 3% | 8% | 15%+ |
```

## Error Handling
- If `community_perks` has fewer than 3 specific items, stop and help the user articulate real value before writing the thank-you page — a weak perks grid is the single biggest cause of low group-join rates.
- If `community_url` is missing or a placeholder, do not ship the thank-you page CTA with a broken link — flag it clearly.
- If the community is paid but the page copy implies free, correct that immediately — mismatched expectations kill trust and cause refund requests.
- If the platform is unusual (not Skool/Whop/Discord/Facebook/Circle), still build the funnel but note the CTA button should link directly to their signup/invite flow.

## Examples
**Example 1:** A SaaS founder building a project management tool starts a free Skool community for other indie SaaS builders as a distribution channel. Opt-in offers a "5 Free Tools Every Indie SaaS Founder Needs" checklist; thank-you page perks are Live Community, Resource Library, Weekly Build Challenges, Founder AMAs.

**Example 2:** A fitness coach runs a $29/mo Whop community. Opt-in page offers a free "7-Day Meal Plan," thank-you page clarifies the community is paid, shows perks (daily accountability, coach access, recipe library, challenges), and links to the Whop checkout instead of a free join.

**Example 3:** A GRC consultant grows a free Discord for compliance analysts. Lead magnet is a "SOC 2 Audit Prep Checklist"; community perks focus on peer Q&A, job postings, and weekly threat-intel roundups.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/opt-in-page.html`
- `templates/thank-you.html`

## Flywheel Connections
### Feeds Into
- `membership-funnel` — if the free community later becomes a paid tier
- `signup-conversion-tracker` (S7-Growth) — measures opt-in and join rates
- `onboarding-flow-builder` (S3-Building) — for the in-community welcome experience

### Fed By
- `funnel-select` — confirms a community platform destination fits the goal
- `funnel-copy` — supplies headline, bullet, and perk copy variants

### Feedback Loop
If thank-you-to-group-join rate stays under 15% after a few weeks, the perks grid is usually too generic — pull real member quotes or activity screenshots into the perks descriptions rather than rewriting the headline again.

```yaml
chain_metadata:
  skill_slug: "group-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "funnel-copy"
    - "signup-conversion-tracker"
    - "membership-funnel"
```
