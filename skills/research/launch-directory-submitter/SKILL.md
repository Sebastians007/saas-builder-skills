---
name: launch-directory-submitter
description: >
  Produces a submission checklist and ready-to-use copy templates for
  launching a finished app on Product Hunt, BetaList, Hacker News Show HN,
  and similar directories.
  Use this skill when the user asks about "where should I launch this",
  or says
  "help me launch on Product Hunt", "write my Show HN post", "where do I submit my app",
  "launch checklist for my app", "what directories should I submit to",
  "how do I write a Product Hunt tagline", "get my app in front of early users".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "launch", "product-hunt", "distribution"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Launch Directory Submitter

This skill produces a specific, ranked list of launch directories to submit a finished app to, plus ready-to-paste copy (tagline, description, first comment, Show HN title) tailored to each platform's actual norms. It exists because most first launches get one shot at each directory's algorithm/audience, and generic copy or wrong-platform norms waste that shot.

## Stage
This skill belongs to Stage S1: Research
(Listed under S1-Research in the master pack; used at the end of the build/launch cycle — treat as the research-and-prep step that precedes the actual launch day actions.)

## When to Use
- App is built and ready (or near-ready) for its first public launch
- Founder doesn't know which directories fit their specific product/audience
- Founder has a Product Hunt launch date set and needs the actual copy written
- Preparing a Show HN post and unsure of Hacker News's unwritten norms
- Re-launching a significantly updated product and needs a refreshed submission

## Input Schema
```
app_name: string (required)
value_prop_statement: string (required) — ideally the output of unique-value-prop-audit
product_description: string (required)
target_customer: string (required)
launch_readiness: enum [live-and-tested, live-but-rough, not-yet-live] (required)
screenshots_or_demo: boolean (optional) — whether visual assets exist yet
pricing: string (optional) — free / freemium / paid, relevant for platform fit
```

## Workflow
### Step 1: Check launch readiness before anything else
If `launch_readiness` is "not-yet-live," stop and say so plainly — launching an unfinished/untested product burns the one-shot nature of these directories (most communities don't give second chances for the same product). Recommend finishing via `browser-verifier` and basic QA skills first.

### Step 2: Match directories to the product, not a generic list
Not every product fits every directory. Recommend from this set based on fit:
- **Product Hunt**: best for consumer-adjacent or visually distinct B2B tools with a design/UX angle. Needs a hunter (or self-hunt), a launch-day plan, and visual assets.
- **Hacker News Show HN**: best for developer tools, technical/infrastructure products, or anything with an interesting build story. Audience punishes marketing-speak — technical honesty wins.
- **BetaList**: best for pre-launch or early-stage products still gathering an initial waitlist/beta audience.
- **Indie Hackers**: best for bootstrapped/solo-founder products, especially with a build-in-public angle.
- **Reddit (relevant subreddit)**: best when a specific, well-matched subreddit exists for the target customer — use web_search to find it and check its self-promotion rules before recommending.
- **G2/Capterra**: best for B2B tools once there are a few real users who can leave reviews — not a launch-day play, a slightly-later one.
Only recommend platforms that actually fit `target_customer` and `product_description` — recommending all of them regardless of fit wastes the founder's limited launch-day attention.

### Step 3: Write platform-specific copy
For each recommended platform, produce copy in that platform's actual format and voice:
- Product Hunt: tagline (≤60 chars), first comment (founder story + ask, not a sales pitch), gallery image suggestions.
- Show HN: title following the "Show HN: X – Y" format convention, first comment explaining what it does, why it was built, and inviting technical feedback (not "check out my SaaS").
- BetaList: short pitch + what problem it solves + who it's for.
- Reddit: a genuine post following that specific subreddit's norms (check rules via web_search), not a copy-pasted ad.

### Step 4: Build the launch-day checklist
Include: assets needed before submission (logo, screenshots/demo video, GIF if applicable), timing recommendations (e.g. Product Hunt launches perform best starting 12:01am PT), who to notify on launch day (existing audience, relevant communities), and a plan for responding to comments/questions within the first few hours (engagement in the first hour matters heavily on most of these platforms).

### Step 5: Self-Validation
- [ ] Readiness was checked before recommending any directory
- [ ] Directories recommended are matched to actual product/audience fit, not a blanket list
- [ ] Copy is written in each platform's actual voice/format, not one generic blurb reused everywhere
- [ ] Character/format constraints per platform respected (e.g. PH tagline length)
- [ ] A concrete launch-day checklist with timing is included

## Output Schema
```
{
  readiness_check: string,
  recommended_directories: [{ platform: string, fit_reason: string }],
  copy: [{ platform: string, assets: object }],
  launch_day_checklist: string[]
}
```

## Output Format
```markdown
# Launch Plan: <app name>

## Readiness Check
<go / not yet, with reasoning>

## Where to Launch
| Platform | Why It Fits |
|---|---|
| ... | ... |

## Copy

### Product Hunt
**Tagline:** "..."
**First comment:** "..."

### Show HN
**Title:** "Show HN: ... – ..."
**First comment:** "..."

(repeat per recommended platform)

## Launch Day Checklist
- [ ] ...

## Next Step
Run `user-acquisition-analyzer` to plan ongoing acquisition beyond launch day, or `signup-conversion-tracker` to measure what the launch actually drove.
```

## Error Handling
- If the product is B2B-only with no consumer angle and no interesting technical story, deprioritize Product Hunt and Show HN in favor of BetaList, relevant Reddit/industry communities, and direct outreach — say so rather than forcing a fit that isn't there.
- If `screenshots_or_demo` is false, flag that visual assets are required for most of these platforms and should be produced before submission.
- If the founder wants to launch on all platforms simultaneously, recommend against it — most of these communities notice and penalize obvious cross-posted spam; suggest a staggered sequence instead.
- If a suggested subreddit's self-promotion rules can't be confirmed via web_search, say so and recommend the founder check the subreddit's rules/wiki manually before posting.

## Examples
**Example 1**
User: "My app is a Chrome extension for tracking cold email replies, it's live and tested. Where should I launch?"
→ Skill recommends Product Hunt (visual, tool-shaped) and a specific sales/outreach-focused subreddit, deprioritizes Show HN (not a developer-tool story), writes tagline + first comment for each, builds the checklist.

**Example 2**
User: "I built a CLI tool for developers, not live yet."
→ Skill flags readiness first, recommends finishing testing, then when ready prioritizes Show HN heavily (strong fit) over Product Hunt (weaker fit for a CLI tool), writes the Show HN title/comment in that community's expected voice.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `user-acquisition-analyzer` (S1-Research) — launch is one channel; this hands off to planning sustained acquisition after it
- `signup-conversion-tracker` (S10-Growth) — measures the actual results of the launch
- `ab-test-generator` (S10-Growth) — can test alternate taglines/copy post-launch

### Fed By
- `unique-value-prop-audit` (S1-Research) — supplies the sharpened one-liner this skill builds copy around
- `browser-verifier` (S7-Testing) — confirms the app is actually ready before this skill greenlights a launch

### Feedback Loop
Actual launch performance (upvotes, signups, comments) tracked via `signup-conversion-tracker` should feed back to refine which platforms and copy patterns this skill recommends for similar product types in the future.

```yaml
chain_metadata:
  skill_slug: "launch-directory-submitter"
  stage: "research"
  timestamp: string
  suggested_next:
    - "user-acquisition-analyzer"
    - "signup-conversion-tracker"
```
