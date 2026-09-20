---
name: tech-stack-finder
description: >
  Recommends the right free-or-cheap tech stack (framework, hosting, database,
  auth) for a described app idea, weighing the founder's actual skill level
  and the tools they already use.
  Use this skill when the user asks about "what stack should I use", "what should I build this in",
  or says
  "what should I build this app with", "I'm not technical, what stack do I use",
  "should I use Cloudflare or Vercel", "what database should I pick",
  "help me choose a tech stack", "is this stack overkill for my idea",
  "what's the cheapest way to host this".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "tech-stack", "hosting", "infrastructure"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Tech Stack Finder

This skill produces a specific, justified tech stack recommendation (frontend, backend, database, auth, hosting, file storage) for one described app idea. It exists because non-technical founders lose weeks to "which framework" paralysis, or copy a stack from a YouTube tutorial that doesn't fit their skill level or budget. The output is a decision, not a survey of options.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has an app idea and no stack decided yet
- Founder is stuck between two or more frameworks/hosts and can't decide
- Founder inherited or copied a stack from a tutorial and wants a sanity check
- Founder already has infra (e.g. already pays for Cloudflare, already has a Hostinger account) and wants to reuse it instead of adding a new vendor
- Project is about to get more complex (e.g. adding auth, payments, file uploads) and current stack may not support it
- Someone asks "is X overkill" or "can I really build this myself"

## Input Schema
```
app_idea: string (required) — what the app does, one paragraph
user_skill_level: enum [non-technical, some-scripting, junior-dev, experienced-dev] (ask if unknown)
existing_tools: string[] (optional) — hosting/tools already paid for or familiar with
expected_scale: enum [prototype/validate, <1k users, 1k-100k users, 100k+ users] (default: prototype/validate)
must_haves: string[] (optional) — e.g. "real-time updates", "file uploads", "payments", "mobile app"
budget_per_month: number (optional, default: $0-25)
```

## Workflow
### Step 1: Pin down the real requirements
Ask (or infer from the idea) three things: does it need a database with relationships (Postgres-shaped) or just key-value/documents (KV-shaped)? Does it need real-time (websockets/live updates)? Does it need file storage (uploads, images, video)? Do not guess silently on anything that changes the stack materially — ask.

### Step 2: Check existing tools first
Before recommending anything new, check `existing_tools` and the user's memory/context for infra they already have (e.g. already deployed on Cloudflare Pages, already has a GitHub account, already pays for Hostinger). Reusing existing infra beats "best practice" every time for a solo non-technical founder — new vendors mean new logins, new bills, new failure points.

### Step 3: Match skill level to framework
- **non-technical / some-scripting**: recommend the framework the user's AI coding tool (Claude Code, Cursor) generates most reliably with the fewest moving parts — typically a single full-stack framework (e.g. Next.js on Vercel, or plain HTML/JS + Cloudflare Workers) over a split frontend/backend/microservices setup. Fewer repos, fewer deploy targets, fewer places to get stuck.
- **junior-dev / experienced-dev**: can weigh in tradeoffs (e.g. Next.js vs SvelteKit vs Remix) since they can debug framework quirks themselves.
Never recommend a stack requiring Kubernetes, Docker orchestration, or manual server management for prototype/validate scale — that's solving a problem the user doesn't have yet.

### Step 4: Pick the database and auth by shape, not hype
- Relational data (users have many orders, orders have many items) → Postgres-family (e.g. Supabase, Neon, or Cloudflare D1/Postgres depending on host).
- Simple key-value or document data, low relational complexity → KV store or lightweight document DB (e.g. Cloudflare KV/D1, Firebase).
- Auth: recommend a managed auth provider (e.g. Clerk, Supabase Auth, Auth.js) over hand-rolled auth for anyone below junior-dev skill level — password/session security bugs are the #1 way non-technical builders get burned.

### Step 5: Total cost and vendor count sanity check
List every vendor the recommended stack requires (hosting, DB, auth, storage, email, domain) and the monthly cost at `expected_scale`. If total vendor count exceeds 4 for a prototype-stage app, cut one — consolidate onto a platform that bundles more (e.g. Cloudflare bundles Workers + Pages + D1 + KV + R2 under one login and bill).

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] Every recommended tool has a free tier or costs under `budget_per_month`
- [ ] Stack matches `user_skill_level` (no unmanaged servers for non-technical users)
- [ ] Existing tools were checked and reused where sensible
- [ ] Data shape (relational vs KV) was actually reasoned through, not defaulted
- [ ] Auth recommendation matches skill level
- [ ] A named next skill is suggested for what comes after stack selection

## Output Schema
```
{
  recommended_stack: {
    frontend: string,
    backend: string,
    database: string,
    auth: string,
    hosting: string,
    file_storage: string | null
  },
  reasoning: string[],
  monthly_cost_estimate: string,
  vendor_count: number,
  reused_existing_tools: string[],
  rejected_alternatives: { option: string, why_rejected: string }[],
  next_step: string
}
```

## Output Format
```markdown
# Tech Stack Recommendation: <app name>

## The Stack
| Layer | Choice | Why |
|---|---|---|
| Frontend | ... | ... |
| Backend | ... | ... |
| Database | ... | ... |
| Auth | ... | ... |
| Hosting | ... | ... |
| File Storage | ... | ... |

## Monthly Cost at Your Scale
Estimated: $X/mo at <expected_scale>. Vendor count: N.

## What We Reused
- <existing tool>: kept because ...

## What We Rejected (and why)
- <alternative>: would have added complexity/cost without a real benefit because ...

## Next Step
Run `prd-writer` to turn this into a build spec, or `architecture-decision-writer` if you want the tradeoffs documented before committing.
```

## Error Handling
- If `app_idea` is too vague to determine data shape, ask one clarifying question ("does a user's data connect to other users' data, or is everyone's data separate?") rather than guessing.
- If the user demands a trendy framework that doesn't fit their skill level, name the risk plainly, then give them what they asked for as a secondary option.
- If `existing_tools` conflicts with the best-fit recommendation (e.g. they only know WordPress but need real-time features), say so directly and explain the tradeoff rather than silently picking one.
- If `expected_scale` is "100k+ users" but this is a first build, flag that premature scale-planning wastes time — recommend building for prototype scale and revisiting via `feature-roadmap-architect` later.
- If budget is $0 and the idea requires something with no free tier (e.g. heavy video transcoding), say so and suggest the cheapest paid path instead of pretending a free option exists.

## Examples
**Example 1**
User: "I want to build a tool where small gyms can text their members about class changes. I'm not technical, I already use Cloudflare for my other site."
→ Skill infers: relational data (gyms → members → messages), no real-time needed, non-technical skill level, existing Cloudflare account.
→ Output: Cloudflare Pages + Workers + D1 (Postgres-shaped, same vendor), Clerk or Supabase Auth for login, Twilio for SMS (unavoidable third vendor), no separate file storage needed.

**Example 2**
User: "Should I use MongoDB or Postgres for a project tracker app?"
→ Skill asks: does a project have many tasks, and do tasks have assignees/dependencies? User confirms yes.
→ Output: Postgres-family recommended over MongoDB — the data is inherently relational; MongoDB would require manual joins in application code, adding complexity without benefit.

**Example 3**
User: "My cofounder set us up with a Kubernetes cluster on GCP for our MVP that has 12 signups."
→ Skill flags this directly as overkill for validate-stage scale, recommends migrating to a single-vendor managed platform, and estimates the cost/time savings.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `prd-writer` (S2-Planning) — stack choice becomes a constraint in the product spec
- `architecture-decision-writer` (S2-Planning) — formalizes the tradeoffs into an ADR
- `cloudflare-deployer` (S5-Deployment) — if Cloudflare is chosen, hands off directly to deployment setup
- `trending-tech-scout` (S1-Research) — cross-check the recommendation against what's currently trending/well-supported

### Fed By
- `saas-idea-validator` (S1-Research) — confirms the idea is worth building before picking a stack

### Feedback Loop
If `architecture-decision-writer` or `tech-debt-detector` later find the chosen stack caused real friction, that should adjust this skill's default recommendations for similar skill-level/idea combinations going forward.

```yaml
chain_metadata:
  skill_slug: "tech-stack-finder"
  stage: "research"
  timestamp: string
  suggested_next:
    - "prd-writer"
    - "architecture-decision-writer"
```
