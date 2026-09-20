---
name: headline-matrix
description: >
  Generates a structured matrix of headline variations for a SaaS landing
  page, pricing page, ad, or email subject line using proven direct-response
  headline formulas, grouped by type so testing covers real angle variation
  instead of minor word swaps.
  Use this skill when the user asks about writing landing page headlines,
  ad copy, or email subject lines, or says
  "give me headline options", "I need a hero headline for my landing page",
  "write email subject lines", "give me ad hooks", "my headline is boring",
  "generate headline variations to test", "what should my hero section say".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "headlines", "landing-page", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Headline Matrix

This skill generates headline variations grouped by proven direct-response angle types, not by shuffling adjectives around one idea. It's built for landing page heroes, pricing page headers, ad hooks, and email subject lines where the founder needs real options to test, not five versions of the same sentence.

## Stage
This skill belongs to Stage S10: Copywriting

## When to Use
- Writing or rewriting a landing page hero headline
- Generating ad hooks or email subject lines that need real variation for testing
- The current headline is feature-based ("The All-in-One Platform For X") and needs sharper angles
- Feeding `ab-test-generator` with genuinely distinct headline variants instead of trivial rewrites
- The user has a clear offer and avatar (from `offer-extraction` and `avatar-extraction`) and needs it turned into words a stranger will read in three seconds
- The user says the current headline "isn't landing" or "sounds like everyone else's"

## Input Schema
```
placement: string                 # "landing page hero" | "pricing page" | "ad" | "email subject line"
core_promise: string              # from offer-extraction, or described directly
primary_avatar: object?           # from avatar-extraction, if run
awareness_stage: string?          # from schwartz-awareness-mapper, if run
proof_points: string[]?           # numbers, testimonials, logos available to reference
count_requested: number?          # default 20
```

## Workflow
### Step 1: Confirm the Offer Is Locked
Headlines amplify an offer, they don't invent one. If `core_promise` is vague or missing, stop and recommend `offer-extraction` first — a strong headline on a weak offer just gets more people to bounce off the same weak page faster.

### Step 2: Generate Across Seven Angle Types
Produce headlines in each of these categories, matched to the awareness stage if known (unaware/problem-aware audiences need curiosity and pain-first angles; most-aware audiences respond to offer and proof angles directly):
- **Curiosity** — creates a gap the reader wants closed ("The reason your trial users disappear in week two")
- **Specificity** — a concrete number or result beats a vague claim ("Cut onboarding time from 40 minutes to 6")
- **Proof** — leans on a stat, logo, or result the product already has
- **Urgency** — time or cost of waiting, real not manufactured ("Every week on spreadsheets is a week of billing errors")
- **Contrarian** — challenges an assumption the market holds ("Stop trying to reduce churn. Reduce time-to-value instead.")
- **Mechanism** — names the specific method or system that makes the result work, not just the result
- **Identity** — speaks to who the reader is or wants to be ("Built for ops leads who are done chasing status updates")

### Step 3: Match Format to Placement
- Landing page hero: one strong headline + one supporting subhead, plus 5-8 alternates
- Pricing page: headline should reduce hesitation at the moment of paying, lean proof/specificity
- Ad: needs a hook in the first line, curiosity/contrarian angles perform best
- Email subject line: shorter, curiosity or specificity heavy, no punctuation tricks that trip spam filters

### Step 4: Enforce Real Variation
Every headline in the matrix must differ in angle, not just wording. Reject a batch where 15 of 20 are curiosity-type rewrites of the same sentence — that's not a test matrix, it's one idea five ways.

### Step 5: Self-Validation
- [ ] All seven angle types are represented (or explicitly noted as skipped with a reason, e.g. no proof points available yet)
- [ ] Headlines are specific to this product and avatar, not swappable with a competitor's
- [ ] No two headlines in the same category say the same thing in different words
- [ ] Format matches the placement requested
- [ ] If awareness stage was provided, headline mix is weighted toward angles appropriate to that stage

## Output Schema
```json
{
  "placement": "string",
  "headlines_by_type": {
    "curiosity": ["string"],
    "specificity": ["string"],
    "proof": ["string"],
    "urgency": ["string"],
    "contrarian": ["string"],
    "mechanism": ["string"],
    "identity": ["string"]
  },
  "recommended_primary": "string",
  "recommended_primary_rationale": "string"
}
```

## Output Format
```markdown
# Headline Matrix: [placement]

## Curiosity
1. ...
2. ...

## Specificity
1. ...

## Proof
1. ...

## Urgency
1. ...

## Contrarian
1. ...

## Mechanism
1. ...

## Identity
1. ...

## Recommended Primary
[headline]
Why: [tied to avatar/awareness stage/offer]
```

## Error Handling
- No offer or avatar given → generate a smaller, generic-risk-flagged matrix and recommend running `offer-extraction` and `avatar-extraction` first for sharper results
- No proof points available → skip or clearly mark the proof category as placeholder ("[add a real number/logo once available]") rather than inventing fake stats
- User wants only one headline, not a matrix → still generate 3-5 quick options across different angle types so there's a real choice, then recommend the strongest
- Placement unclear → default to landing page hero format and note the assumption

## Examples
**Example 1**
User: "Give me headline options for my landing page hero. We help agencies stop losing track of client retainers."
Skill: Produces a matrix including specificity ("Never miss a retainer renewal again — see every client's status in one view"), contrarian ("Your project management tool isn't the problem. Your retainer tracking is."), and identity ("Built for agency ops leads managing more clients than spreadsheets can handle") angles, then recommends the specificity headline as primary because the avatar's frustration was explicitly about missed renewals.

**Example 2**
User: "Write 5 email subject lines for our trial-expiring reminder."
Skill: Generates curiosity ("Your trial ends in a way you might not expect") and specificity ("3 days left — here's what you'll lose access to") variants sized for subject-line length, avoiding spam-trigger punctuation.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- ab-test-generator (S7-Growth)
- full-funnel-campaign-orchestrator (S10-Copywriting)
- marketing-site-seo-audit (S7-Growth)

### Fed By
- avatar-extraction (S10-Copywriting)
- offer-extraction (S10-Copywriting)
- schwartz-awareness-mapper (S10-Copywriting)

### Feedback Loop
Winning headlines from `ab-test-generator` results should be logged back as proof that a given angle type works for this avatar, narrowing future matrices toward what's already validated instead of regenerating from scratch each time.

```yaml
chain_metadata:
  skill_slug: "headline-matrix"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "ab-test-generator"
    - "full-funnel-campaign-orchestrator"
```
