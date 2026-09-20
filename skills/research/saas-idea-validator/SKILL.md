---
name: saas-idea-validator
description: >
  Scores a raw app idea on demand signal, competition level, and feasibility
  before any code gets written, producing a go/pivot/kill recommendation.
  Use this skill when the user asks about "should I build this", "is this idea worth it",
  or says
  "is this a good idea", "should I build this app", "validate my idea before I start",
  "is there actually demand for this", "am I wasting my time building this",
  "score my SaaS idea", "should I pivot or keep going with this idea".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "idea-validation", "market-research"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# SaaS Idea Validator

This skill scores a described app idea on three axes — demand signal, competitive difficulty, and technical/business feasibility for this specific founder — and returns a clear go/pivot/kill call with reasoning. It exists to catch bad ideas before weeks of build time are sunk into them, without becoming validation-paralysis that blocks building entirely.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has a specific idea and wants a reality check before building
- Founder already built something and traction is flat — wants to know if the idea itself is the problem
- Comparing two or more ideas to decide which to pursue first
- After `underserved-market-finder` surfaces a niche, to confirm it's actually worth building for
- Founder is about to sink a large time investment (e.g. weeks of Claude Code sessions) and wants a gut check first

## Input Schema
```
idea_description: string (required) — what it does, for whom, one paragraph
founder_context: {
  skill_level: enum [non-technical, some-scripting, junior-dev, experienced-dev],
  time_available: string (optional) — e.g. "10 hrs/week",
  existing_audience: string (optional) — e.g. "2k newsletter subscribers", "none"
}
evidence_already_gathered: string (optional) — any user interviews, waitlist signups, forum research already done
```

## Workflow
### Step 1: Score demand signal (0-10)
Use web_search to check: search volume/interest patterns for the problem, forum complaints (Reddit, industry-specific forums) about this exact pain point, evidence of manual workarounds (spreadsheets, hacky processes people currently use — strong signal), and any `evidence_already_gathered` from the founder (real user interviews and waitlist signups outweigh any web research). Score low if the "demand" is only the founder's own hunch with zero external evidence.

### Step 2: Score competitive difficulty (0-10, where 10 = hardest to break in)
Run a lightweight competitor check via web_search (or reuse `competitor-teardown` output if available). Score based on: how many well-funded direct competitors exist, whether the category has an entrenched incumbent with strong network effects or switching costs, and whether this specific founder has any wedge (existing audience, domain expertise, underserved niche) that lowers the effective difficulty.

### Step 3: Score feasibility for this founder (0-10)
This is founder-specific, not generic. Weigh `founder_context.skill_level` against the technical complexity implied by `idea_description` (e.g. real-time collaboration, heavy AI usage, payments/compliance-heavy domains are harder for non-technical builders). Weigh `time_available` against a realistic build timeline. An idea can be objectively great and still score low here if this founder specifically can't execute it soon.

### Step 4: Weigh the three scores into a call
No idea needs a perfect score on all three. Common patterns: high demand + high competition + strong founder wedge = still a GO (niche in on the wedge). High demand + low feasibility = GO but recommend a scoped-down v1 or a no-code approach first. Low demand across every check = KILL or PIVOT the angle (route to `underserved-market-finder`). Decent everything but nothing outstanding = weak GO with a clear warning about what to prove fast (usually: get 10 real users talking to you before building more).

### Step 5: Give a specific next validation step if the score is borderline
If the call isn't a clean go or kill, don't just say "get more validation" — name the exact cheapest next test (e.g. "post in [specific named community] describing the problem and see if anyone responds with 'I need this'," "DM 10 people who posted this complaint and ask if they'd pay $X").

### Step 6: Self-Validation
- [ ] All three scores are backed by a stated reason, not just a number
- [ ] Demand signal used real search/evidence, not assumption
- [ ] Feasibility score is genuinely founder-specific, not generic
- [ ] Final call is unambiguous (Go / Pivot / Kill) even if nuanced in explanation
- [ ] If not a clean Go, a specific and cheap next validation step is named

## Output Schema
```
{
  idea: string,
  scores: { demand: number, competition_difficulty: number, feasibility: number },
  call: enum [Go, Weak Go, Pivot, Kill],
  reasoning: string,
  cheapest_next_validation_step: string | null
}
```

## Output Format
```markdown
# Idea Validation: <idea name>

## Scores (0-10)
| Axis | Score | Why |
|---|---|---|
| Demand Signal | X/10 | ... |
| Competitive Difficulty | X/10 | ... |
| Feasibility for You | X/10 | ... |

## Call: **<Go / Weak Go / Pivot / Kill>**

<2-4 sentence plain-language explanation of the call>

## If You Proceed
<what to prove fastest, and how>

## Next Step
Run `tech-stack-finder` and `prd-writer` if Go. Run `underserved-market-finder` if Pivot. If Kill, no shame — the fast no just saved you weeks.
```

## Error Handling
- If `idea_description` is too vague to score (e.g. "an app for productivity"), ask the user to narrow it to one specific user and one specific problem before scoring — a vague idea can't be honestly validated.
- If web_search turns up zero evidence either way (truly novel idea), say that explicitly — score demand as "unknown, not zero" and recommend the cheapest possible real-world test rather than guessing a number.
- If the founder has already gathered strong evidence (`evidence_already_gathered`, e.g. a waitlist with 200 signups), weight that far above general web research — real signal beats inferred signal every time.
- Never soften a Kill call to spare feelings — state it plainly with the reasoning, per the user's stated preference for direct feedback over encouragement.
- If two ideas are being compared, score both independently and present them side by side rather than picking a winner without showing the math.

## Examples
**Example 1**
User: "Idea: an app that helps freelance photographers automatically deliver and watermark client galleries. I'm non-technical, have 5 hrs/week, no existing audience."
→ Demand: 7/10 (real forum complaints, existing manual workarounds in Dropbox/Google Drive found via search). Competition: 6/10 (Pixieset and ShootProof exist and are established, but review complaints show pricing/complexity gaps). Feasibility: 4/10 (file handling + payments is nontrivial for non-technical + 5hrs/week). Call: **Weak Go** — recommend starting with a much smaller wedge (just the watermarking/delivery, not a full client gallery platform) to fit the time budget.

**Example 2**
User: "Idea: a to-do list app but for introverts."
→ Demand: 2/10 (no evidence found that "introvert" is a real market segmentation for to-do apps; category already saturated with generic to-do apps). Call: **Kill** — recommend `underserved-market-finder` to find a more specific, evidenced niche instead.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `prd-writer` (S5-Planning) — Go-scored ideas move directly into a product spec
- `tech-stack-finder` (S1-Research) — feasibility findings inform stack selection
- `underserved-market-finder` (S1-Research) — Pivot calls route back here for a new niche
- `mvp-feature-slicer` (S5-Planning) — Weak Go calls with a scoped-down recommendation feed the MVP slice directly

### Fed By
- `underserved-market-finder` (S1-Research) — supplies candidate niches to validate
- `competitor-teardown` (S1-Research) — supplies competitive difficulty data

### Feedback Loop
Once a validated idea is built and launched, real `signup-conversion-tracker` and `app-performance-report` data should be compared back against the original demand-signal score to calibrate how reliable this skill's scoring has been.

```yaml
chain_metadata:
  skill_slug: "saas-idea-validator"
  stage: "research"
  timestamp: string
  suggested_next:
    - "prd-writer"
    - "tech-stack-finder"
```
