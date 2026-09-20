---
name: skill-finder
description: >
  Recommends the 1-3 right skills from the 52-skill pack for whatever the founder is
  trying to do right now, described in plain language, so they don't have to memorize
  every skill name or guess which stage something belongs to.
  Use this skill when the user asks "which skill do I need for this", "what should I use
  to do X", "I don't know where to start", "is there a skill for X", "what's in this pack",
  "help me find the right tool for this task", "I want to do X but don't know the skill
  name", or "list what's available for [stage/topic]".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "meta", "discovery", "navigation"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Meta
---

# Skill Finder

Takes a plain-language description of what the founder is trying to do and maps it to the 1-3 actual skills in the pack that fit, using the full skill reference table below. This exists so a non-technical founder never has to memorize 52 skill names — they just say what they're stuck on.

## Stage
This skill belongs to Stage S11: Meta

## When to Use
- The founder describes a problem or task but doesn't know a skill exists for it
- Multiple skills seem plausible and they need to know which one to start with
- Onboarding to the pack for the first time and wanting a tour of what's available
- Mid-project and unsure whether the next step is a S3-Building task or a S4-Testing task
- `create-skill` returns "no match found" and a second opinion is wanted before scaffolding something new

## Input Schema
```
finder_request:
  task_description: string     # plain language, whatever the founder actually typed
  project_stage_hint: string   # optional, e.g. "just starting", "about to launch", "already live"
  urgency: string               # optional, "right now" vs "planning ahead"
```

## Workflow
### Step 1: Extract the Core Verb and Object
Identify what action the founder wants (research, plan, build, test, deploy, run, grow, or fix/improve-the-process) and what it's acting on (an idea, a feature, a user flow, the infra, a metric, the pack itself). This maps almost directly to the 8 stages.

### Step 2: Match Against the Reference Table
Scan the full 52-skill table below for slugs whose one-line description matches the extracted verb+object. Don't just keyword-match the slug name — read the description, since founders describe things in their own words, not skill-name words.

### Step 3: Narrow to 1-3 Candidates
If more than 3 skills plausibly match, narrow using `project_stage_hint` and urgency — pick the skill that acts, not just informs, when time is short. If genuinely 2 skills are both needed (e.g. one plans, one builds), say so explicitly rather than forcing a single pick.

### Step 4: Check for No Match
If nothing in the table genuinely fits, say so plainly instead of forcing a weak match. Recommend `create-skill` to scaffold something new, or `category-designer` if it looks like a whole new category of work.

### Step 5: Explain the Pick in One Line Each
For each recommended skill, give one plain-language sentence on why it fits this specific ask — not just the skill's generic description repeated back.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Did I read the founder's actual words, not just pattern-match a slug name?
- [ ] Is the recommendation 1-3 skills, not a dump of everything remotely related?
- [ ] If no good match exists, did I say so instead of forcing one?
- [ ] Did I give a reason specific to their ask, not a generic skill description?
- [ ] Did I check the right stage given their `project_stage_hint`?

## Output Schema
```
{
  "task_description": string,
  "recommended_skills": [
    {"slug": string, "stage": string, "why_this_fits": string}
  ],
  "no_match": bool,
  "fallback_action": string | null   // e.g. "run create-skill" if no_match is true
}
```

## Output Format
```markdown
# Skill Match

## What you're trying to do
<restated in one line>

## Recommended
1. `<slug>` (Stage) — <why this fits your specific ask>
2. `<slug>` (Stage) — <why, if a second is needed>
3. `<slug>` (Stage) — <why, if a third is needed>

## Start Here
<which one of the above to invoke first, if order matters>

## If nothing above fits
<note only if genuinely no match — points to create-skill or category-designer>
```

## Error Handling
- Task description is too vague ("help me with my app"): ask one clarifying question narrowing to a stage (research/plan/build/test/deploy/run/grow) before recommending anything.
- Task spans multiple stages at once (e.g. "launch my whole app"): recommend a short sequence across stages rather than a single skill, and say so.
- Founder names a skill that doesn't exist in the pack: don't pretend it exists — check the table, and if it's not there, recommend the closest real match or `create-skill`.
- Task is really a `funnel-planner` or `self-improver` job (cross-cutting, not a single-stage task): recommend those meta skills directly rather than a narrow single-stage skill.
- Multiple equally-good matches with no way to rank: present all of them and say they're equally valid entry points, let the founder pick based on where they want to start.

## Reference: Full 52-Skill Table

### S1-Research
| Slug | What it does |
|---|---|
| tech-stack-finder | Recommends a tech stack fit for the app's requirements and team skill level |
| pricing-model-calculator | Works out pricing tiers and price points based on value delivered and market comps |
| competitor-teardown | Breaks down a competitor's product, pricing, and positioning |
| feature-differentiator | Finds what feature(s) would meaningfully differentiate from competitors |
| underserved-market-finder | Identifies market segments competitors are ignoring |
| saas-idea-validator | Tests a SaaS idea against basic viability signals before building |
| unique-value-prop-audit | Checks whether the value proposition is clear and differentiated |
| launch-directory-submitter | Plans and executes submissions to launch directories (Product Hunt etc.) |
| user-acquisition-analyzer | Analyzes which acquisition channels fit the product and audience |
| trending-tech-scout | Surfaces relevant emerging tech/tools worth evaluating |

### S2-Planning
| Slug | What it does |
|---|---|
| prd-writer | Writes a product requirements document |
| architecture-decision-writer | Documents a technical architecture decision and its tradeoffs |
| tech-debt-detector | Flags accumulating technical debt before it compounds |
| defensibility-calculator | Assesses how defensible the product/business is against copycats |
| user-story-writer | Converts requirements into user stories |
| feature-roadmap-architect | Builds a sequenced feature roadmap |
| mvp-feature-slicer | Cuts a feature set down to the smallest viable version |

### S3-Building
| Slug | What it does |
|---|---|
| feature-task-breakdown | Breaks a feature into concrete engineering tasks |
| technical-spike-brief | Scopes a time-boxed research spike before building something uncertain |
| data-model-diagrammer | Diagrams the data model/schema |
| api-endpoint-builder | Designs and scaffolds API endpoints |
| ui-component-builder | Builds UI components |
| auth-flow-builder | Builds authentication/authorization flows |
| onboarding-flow-builder | Builds the new-user onboarding experience |

### S4-Testing
| Slug | What it does |
|---|---|
| test-case-generator | Generates test cases from requirements |
| edge-case-hunter | Finds edge cases likely to break the app |
| regression-test-builder | Builds regression test suites |
| browser-verifier | Verifies behavior in a real browser |
| load-test-builder | Builds load/stress tests |
| accessibility-auditor | Audits accessibility compliance |
| security-review-lite | Lightweight security review pass |
| user-acceptance-test-planner | Plans user acceptance testing |

### S5-Deployment
| Slug | What it does |
|---|---|
| cloudflare-deployer | Deploys the app to Cloudflare infrastructure |
| ci-cd-pipeline-builder | Builds CI/CD pipelines |
| domain-dns-setup | Sets up domain and DNS configuration |
| env-secrets-manager | Manages environment variables and secrets |

### S6-Operations
| Slug | What it does |
|---|---|
| monitoring-alerting-setup | Sets up monitoring and alerting |
| backup-recovery-builder | Builds backup and recovery processes |
| multi-tenant-manager | Manages multi-tenant data isolation and architecture |
| incident-runbook-writer | Writes incident response runbooks |
| seed-data-generator | Generates seed/demo data |

### S7-Growth
| Slug | What it does |
|---|---|
| ab-test-generator | Designs A/B tests |
| signup-conversion-tracker | Tracks and analyzes signup conversion |
| in-app-nav-optimizer | Optimizes in-app navigation for engagement |
| app-performance-report | Reports on app performance metrics |
| marketing-site-seo-audit | Audits marketing site SEO |

### S8-Meta
| Slug | What it does |
|---|---|
| category-designer | Designs new skill categories/stages for the pack |
| compliance-checker | Audits baseline legal/compliance posture (privacy, GDPR/CCPA, WISP-style) |
| create-skill | Scaffolds new SKILL.md files in the pack's format |
| funnel-planner | Plans the signup-to-retention funnel and maps skills to each stage |
| self-improver | Turns project retrospectives into concrete process improvements |
| skill-finder | Recommends the right skill(s) for a plain-language task description |

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map (full detail behind the table above)

## Flywheel Connections
### Feeds Into
- Every skill in the pack — this is the entry point that routes to any of the other 51 skills
- `create-skill` (S11-Meta) — when no match exists

### Fed By
- None — this is a cross-cutting utility skill meant to be the first stop, not downstream of anything

### Feedback Loop
Repeated "no match" results for similar tasks get logged and surfaced to `create-skill`/`category-designer`, so the table itself grows more complete over time instead of staying static.

```yaml
chain_metadata:
  skill_slug: "skill-finder"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "create-skill"
    - "category-designer"
```
