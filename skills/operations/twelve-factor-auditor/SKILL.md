---
name: twelve-factor-auditor
description: >
  Audits a SaaS app against the Twelve-Factor App methodology (2011, still the
  cloud-native standard) and reports exactly which of the 12 rules the app is
  breaking, in plain language, with a concrete fix for each.
  Use this skill when the user asks about "is my app cloud-native", "am I doing
  this the right way", or says
  "check my app against best practices", "is my config setup okay", "am I doing
  anything that will bite me later", "review my app's architecture for cloud
  readiness", "why does dev work but prod breaks", "audit this against the
  twelve-factor app", "is this app portable/scalable the right way".
license: MIT
version: "1.0.0"
tags: ["saas", "operations", "architecture", "cloud-native", "best-practices"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Operations
---

# Twelve-Factor Auditor

Checks a SaaS app's actual codebase and config against the 12 rules from the Twelve-Factor App methodology — the standard, decades-tested set of practices for cloud-native apps that survive restarts, scale correctly, and don't break moving from dev to production. Reports which rules are broken, why it matters concretely (not just "best practice"), and the specific fix.

## Stage
This skill belongs to Stage S9: Operations

## When to Use
- Before a first production deploy, as a sanity check
- After `cloudflare-deployer` reports something behaving differently in prod than in dev
- When the app is growing past "just me testing it" into real users
- Periodically, as a health check alongside `tech-debt-detector`
- When something breaks on restart or redeploy that worked a moment ago

## Input Schema
```
{
  repo_path: string          # path to the app's codebase
  check_scope: string[]      # (optional) specific factors to check, default: all 12
}
```

## Workflow

### Step 1: Locate Config and Entry Points
Find the app's config loading (env vars, wrangler.toml, .env files), the main entry point(s), and any background/scheduled jobs.

### Step 2: Check Each Factor
Walk through all 12, checking the actual code/config, not just asking the user:

1. **Codebase** — one codebase tracked in git, many deploys (not copy-pasted variants per environment)
2. **Dependencies** — explicitly declared (package.json/wrangler.toml), never assumed to exist on the host
3. **Config** — stored in env vars (wrangler secrets, .dev.vars), never hardcoded in source — check for literal API keys/URLs/passwords in code
4. **Backing services** — treated as attached resources (D1, R2, external APIs) swappable via config, not hardcoded connection details
5. **Build, release, run** — strictly separated stages; check the deploy pipeline doesn't let code changes bypass the build/test step
6. **Processes** — stateless; check nothing relies on in-memory state surviving between requests (a real risk with Workers — each request can hit a cold instance)
7. **Port binding** — self-contained, doesn't rely on a runtime-injected web server (mostly N/A for Workers, still worth confirming no assumptions leak in)
8. **Concurrency** — scales via the process model, not by one giant long-running process holding state
9. **Disposability** — fast startup, graceful shutdown; check nothing breaks if a Worker instance is killed mid-request
10. **Dev/prod parity** — check dev and prod use the same backing services (same D1 binding pattern, not SQLite locally and D1 in prod) and deploys happen close together in time, not big infrequent batches
11. **Logs** — treated as event streams (Cloudflare's own logging/tail), not written to local files that vanish when the instance recycles
12. **Admin processes** — one-off tasks (migrations, data fixes) run as one-off processes using the same code/config as the app, not separate ad-hoc scripts with their own hardcoded settings

### Step 3: Score Each Factor
Pass / Partial / Fail for each of the 12, with the specific evidence found (file/line where relevant).

### Step 4: Prioritize Fixes
Not all 12 matter equally for a small SaaS. Rank findings by actual risk: hardcoded secrets (factor 3) and dev/prod parity breaks (factor 10) are usually the highest-impact fixes; port binding (factor 7) is often moot on Workers.

### Step 5: Self-Validation
- [ ] All 12 factors actually checked against real code/config, not assumed
- [ ] Every "Fail" has a concrete file/location, not a vague statement
- [ ] Fixes are proportional to a solo/small-team app, not enterprise-scale advice
- [ ] Report is ranked by real risk, not just listed 1-12 in order

## Output Schema
```
{
  factors: {
    number: number
    name: string
    status: string        # "pass" | "partial" | "fail"
    evidence: string
    fix: string            # empty if pass
  }[]
  top_priority_fixes: string[]   # ranked, max 3
}
```

## Output Format
```
## Twelve-Factor Audit

| # | Factor | Status | Finding |
|---|--------|--------|---------|
| 1 | Codebase | ✅/⚠️/❌ | ... |
| 2 | Dependencies | ... | ... |
...
| 12 | Admin Processes | ... | ... |

### Fix These First
1. [Highest-risk finding + specific fix]
2. [Second]
3. [Third]

### Everything Else
[Lower-priority findings, still listed but not urgent]
```

## Error Handling
- **No codebase yet (pre-build):** Explain this is a post-build check; point to `architecture-decision-writer` for pre-build architecture guidance instead.
- **Config genuinely can't be inspected (secrets redacted):** Ask the user to confirm secrets are in wrangler secrets/env vars rather than reading actual values — never ask for the real secret values.
- **App isn't on Cloudflare:** Adapt factor 7 (port binding) and factor 11 (logs) guidance to the actual host instead of assuming Workers.
- **Everything passes:** Say so plainly, don't invent findings to seem thorough.

## Examples

**Example 1:**
User: "can you check my app follows cloud best practices before I launch"
→ Walk all 12 factors against the actual repo
→ Find a hardcoded API key in a config file (factor 3) and no dev/prod parity (factor 10 — using different DB setups)
→ Rank those two as top-priority fixes, list the rest as lower-priority notes

**Example 2:**
User: "my app works locally but breaks in production"
→ Focus first on factor 10 (dev/prod parity) and factor 3 (config)
→ Find the app reads a local .env file that doesn't exist in the Workers runtime
→ Recommend moving those values to wrangler secrets

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- env-secrets-manager (S8-Deployment) — factor 3 (config) findings feed directly into fixing secret handling
- tech-debt-detector (S5-Planning) — non-urgent findings become tracked tech debt

### Fed By
- cloudflare-deployer (S8-Deployment) — a deploy that behaves differently than dev is the usual trigger to run this audit

### Feedback Loop
- Findings that recur across multiple app audits (e.g. always failing factor 3) should become a standing check in `create-skill`'s template or a written directive so future builds don't repeat it.

```yaml
chain_metadata:
  skill_slug: "twelve-factor-auditor"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "env-secrets-manager"
    - "tech-debt-detector"
```
