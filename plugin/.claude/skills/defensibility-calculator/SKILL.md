---
name: defensibility-calculator
description: >
  Assesses how hard a planned product actually would be for a competitor to copy, scores
  it across concrete defensibility factors, and recommends specific changes that would
  make it harder to clone — before the founder builds something anyone can replicate
  in a weekend with the same AI tools.
  Use this skill when the user asks about "is this idea defensible", "can someone just
  copy this", or says
  "won't someone just build this with AI too", "what's my moat here", "how do I make this
  harder to copy", "is this actually a business or just a feature", "everyone can build
  this now with Claude, what makes mine different", "score my idea's defensibility".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "defensibility", "moat", "competitive-strategy"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Planning
---

# Defensibility Calculator

Scores a planned product on how hard it would actually be for a competitor — especially one using the same AI coding tools — to copy, and gives specific, buildable recommendations to raise that score. AI coding tools have collapsed the cost of building software; a clean UI and a CRUD app is no longer a moat, it's a weekend project for anyone with the same tools. This skill forces the honest question before the build starts: what happens on day one when a competitor points an AI agent at your live app and says "build me this"?

## Stage
This skill belongs to Stage S5: Planning

## When to Use
- Right after a PRD is drafted, before committing engineering time to build it
- The user is excited about an idea that is mostly "a nice UI on top of an API"
- The user asks whether their idea is "just a feature" a bigger competitor could ship in a week
- Before fundraising or partnership conversations, where defensibility gets scrutinized
- Reassessing an existing live product that's getting copied or is worried about being copied
- As a gate before `feature-roadmap-architect` — defensibility-building features should be prioritized deliberately, not left to chance

## Input Schema
```
prd_path?: string                 # the PRD this idea is scored against
idea_summary?: string             # if no PRD yet, a free-text description
known_competitors?: string[]      # existing players in the space, if any
data_access?: string              # what proprietary or hard-to-get data, if any, the product touches
```

## Workflow
### Step 1: Separate the product from the feature
Ask: if a competitor rebuilt only the visible functionality (the screens, the CRUD, the obvious workflow), would they have your product, or would they be missing something? If the answer is "they'd have basically everything," that's the honest starting point — say so plainly rather than softening it.

### Step 2: Score across the real defensibility factors
Rate each factor Low / Medium / High, with a one-line reason:
- **Proprietary data or data network effects** — does usage generate data that makes the product better for everyone, and is that data hard to replicate cold?
- **Switching cost** — once a user is in, how painful is it to leave (data lock-in, workflow embedding, integrations built on top)?
- **Distribution advantage** — does the founder have an audience, channel, or relationship a copier doesn't (this is a real moat even for a simple product)?
- **Regulatory or trust barrier** — does the product require compliance, certification, or accumulated trust (e.g., handling sensitive data) that takes time to earn, not just build?
- **Workflow/domain depth** — does the product encode non-obvious domain knowledge (edge cases, industry-specific rules) that isn't visible from using the product, only from having built it?
- **Speed of iteration** — is the founder positioned to out-ship a copier consistently (small team, tight feedback loop), making "copy once" insufficient?

### Step 3: Call out the weakest factor honestly
Identify the single lowest-scoring factor as the real risk, not a diluted average. A product that's High everywhere except "anyone can copy the UI in a day" is still at risk if that's the only thing shipped in v1.

### Step 4: Recommend concrete moves, not vague advice
For each Low or Medium factor, give one or two specific, buildable actions — not "build a community" as abstract advice, but things like "add an integration that exports to the tool your target user already lives in, making switching cost real" or "start collecting the one data point competitors won't have because they didn't launch first." Avoid consultant-speak like "focus on brand" with nothing under it.

### Step 5: Give the honest bottom line
State plainly whether this is a defensible product, a defensible-if-executed-right product, or a feature dressed up as a product — the user contrarian-positioning preference means push back if the plan is chasing infrastructure/plumbing improvements instead of a real positioning or distribution edge.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Every factor has a Low/Medium/High rating with a specific one-line reason, not a generic statement
- [ ] The weakest factor is called out explicitly as the real risk, not buried in an average
- [ ] Every recommendation is a concrete, buildable action, not vague strategic language
- [ ] The bottom-line verdict is stated plainly, even if it's an uncomfortable answer

## Output Schema
```
{
  "product_summary": string,
  "factor_scores": [
    { "factor": string, "rating": "low" | "medium" | "high", "reason": string }
  ],
  "weakest_factor": string,
  "recommendations": [ { "factor": string, "action": string } ],
  "verdict": string
}
```

## Output Format
```markdown
# Defensibility Assessment: <product>

## Factor Scores
| Factor | Rating | Why |
|---|---|---|
| Proprietary data / network effects | <L/M/H> | <reason> |
| Switching cost | <L/M/H> | <reason> |
| Distribution advantage | <L/M/H> | <reason> |
| Regulatory/trust barrier | <L/M/H> | <reason> |
| Workflow/domain depth | <L/M/H> | <reason> |
| Speed of iteration | <L/M/H> | <reason> |

## Weakest Point
<the single biggest risk, stated directly>

## What Would Make This More Defensible
- <factor>: <specific, buildable action>
- <factor>: <specific, buildable action>

## Bottom Line
<plain verdict: real moat, moat-if-executed, or feature-not-a-product — and why>
```

## Error Handling
- If the idea is genuinely just a thin wrapper on someone else's API with no other angle, say so directly rather than manufacturing a moat that isn't there — this is a Kill-or-rethink signal, not something to soften.
- If the user has no known competitors yet, still score against the hypothetical "someone points an AI agent at your live app" scenario rather than skipping the assessment.
- If distribution/audience is the only real moat, say that explicitly — it's a legitimate and often the most realistic moat for a solo builder, not a lesser answer than "proprietary tech."
- If the user pushes back defensively, still give the honest score — softening this assessment defeats its purpose.
- If regulatory/trust barriers are claimed but not substantiated (e.g., "healthcare data" with no actual compliance work planned), rate that factor Low until real work exists, not High based on intent.

## Examples
**Example 1:** User has a PRD for an AI-powered resume builder. The skill scores it: proprietary data Low, switching cost Low (nothing keeps them after one resume), distribution Medium (user has a small following), domain depth Low, verdict: feature-not-a-product as currently scoped. Recommendation: build ongoing value (job tracking, application history) to raise switching cost, or find a genuinely underserved niche where domain depth becomes real.

**Example 2:** User has a compliance tool for tax preparers handling client documents (similar shape to a real product the user has shipped before). The skill rates regulatory/trust barrier High (real compliance work exists), switching cost Medium-High (client data lives in the system), workflow depth Medium, verdict: defensible-if-executed, with recommendation to deepen domain-specific rule coverage as the moat rather than UI polish.

**Example 3:** User asks to reassess a live app that a competitor just cloned key screens of. The skill scores current state, finds distribution and iteration speed as the only realistic remaining levers, and recommends shipping the next differentiating feature fast rather than trying to out-polish the clone.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-roadmap-architect` (S5-Planning) — defensibility-building features get prioritized explicitly in the sequence
- `unique-value-prop-audit` (S1-Research) — informs how the positioning should lean on the real moat, not a fake one
- `mvp-feature-slicer` (S5-Planning) — ensures the trimmed-down MVP still contains the one defensible piece, not just the easy-to-copy shell

### Fed By
- `prd-writer` (S5-Planning) — provides the scoped product to assess
- `competitor-teardown` (S1-Research) — gives real competitor context to score switching cost and distribution against

### Feedback Loop
If `competitor-teardown` or `app-performance-report` later shows the product actually got cloned or undercut, re-run this skill to check whether the original weakest factor was the cause, and feed that lesson back into how future ideas get scored.

```yaml
chain_metadata:
  skill_slug: "defensibility-calculator"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-roadmap-architect"
    - "unique-value-prop-audit"
    - "mvp-feature-slicer"
```
