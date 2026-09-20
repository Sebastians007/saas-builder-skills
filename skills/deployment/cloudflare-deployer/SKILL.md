---
name: cloudflare-deployer
description: >
  Deploys a tested app or feature to Cloudflare Workers or Pages correctly, running a
  pre-deploy checklist first so nothing broken or misconfigured ships.
  Use this skill when the user asks about deploying to Cloudflare, shipping a build,
  pushing to production, or says
  "deploy this to cloudflare", "ship this feature", "push this live",
  "how do I deploy my worker", "deploy to production", "wrangler deploy this",
  "is this ready to go live", "publish my pages site".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "cloudflare", "deployment", "wrangler"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Deployment
---

# Cloudflare Deployer

Takes a feature that has already passed testing and puts it live on Cloudflare Workers or Pages, safely and repeatably. It produces a pre-deploy checklist, the exact deploy commands to run, and a post-deploy verification pass so the founder knows the app actually works in production, not just that the command exited with code 0.

## Stage
This skill belongs to Stage S8: Deployment

## When to Use
- A feature or bug fix has passed testing (S4) and is ready to ship
- The user wants to deploy a Worker, Pages site, D1-backed app, or R2-backed app
- The user says "deploy", "ship", "go live", "push to production", or "publish"
- Something was deployed and is now broken, and the user needs a safe rollback
- Setting up a brand-new Cloudflare project for the first time (first deploy)
- Confirming an app is actually deploy-ready before running any commands

## Input Schema
```
project:
  type: "worker" | "pages" | "worker+d1" | "worker+r2" | "fullstack (worker api + pages frontend)"
  repo_path: string (local path to the project)
  wrangler_toml_path: string (optional, defaults to ./wrangler.toml)
  target_env: "dev" | "staging" | "production" (default: production)
  has_database: boolean (D1 involved?)
  has_storage: boolean (R2 involved?)
  custom_domain: string (optional)
  first_deploy: boolean
```

## Workflow
### Step 1: Confirm the feature is actually deploy-ready
Ask (or check for evidence) that the feature passed the testing stage: tests run, manual click-through done, no known open bugs. If there is no evidence testing happened, say so plainly and recommend running the testing skills first — do not silently deploy untested code.

### Step 2: Run the pre-deploy checklist
Check each of these and report pass/fail, don't just assume:
- `wrangler.toml` (or `wrangler.jsonc`) exists, has correct `name`, `main`, `compatibility_date`, and correct `account_id` if not using OAuth
- Build command runs clean locally (`npm run build` or equivalent) with zero errors
- All required env vars/secrets exist in the target environment (cross-check against `env-secrets-manager` skill if unsure)
- D1 bindings in `wrangler.toml` match actual database IDs (`wrangler d1 list`)
- R2 bindings match actual bucket names (`wrangler r2 bucket list`)
- No `console.log`-only debug code left gating real logic
- `.dev.vars` and any `.env` files are in `.gitignore` (never shipped, never committed)
- If Pages: build output directory matches what's configured in the Pages project settings
- Routes/custom domain config in `wrangler.toml` match what's actually wanted for this deploy

### Step 3: Choose the right deploy command
Give the exact command for the situation, not a generic one:
- Worker: `wrangler deploy` (add `--env staging` if using named environments)
- Pages (git-connected): push to the connected branch, or `wrangler pages deploy <dir>` for a manual deploy
- First deploy of a new Worker: `wrangler deploy` after `wrangler login` and confirming `account_id`
- D1 migrations that need to run before code that depends on them: `wrangler d1 migrations apply <db-name> --remote` BEFORE deploying the Worker that uses the new schema

### Step 4: Deploy
Run the command. Capture the deployed URL and the version/deployment ID Cloudflare returns — this is what you roll back to if something goes wrong.

### Step 5: Post-deploy verification
Do not mark the deploy done from the command output alone. Verify on the live URL:
- Hit the live URL/API and confirm a 200, not just "wrangler said success"
- Check the specific feature that was just shipped actually behaves correctly live
- Check Cloudflare dashboard → Workers → Logs (or `wrangler tail`) for any errors in the first few minutes of traffic
- If a custom domain is attached, confirm it resolves and serves the new version (see `domain-dns-setup` for DNS issues)

### Step 6: Self-Validation
Before presenting output, silently confirm:
- [ ] Pre-deploy checklist was actually run, not assumed
- [ ] The exact command(s) used are shown, not paraphrased
- [ ] A rollback path (previous deployment ID or `wrangler rollback`) is documented
- [ ] Live verification happened against the real URL, not just localhost
- [ ] Any failed checklist item blocked the deploy or was explicitly flagged as a known risk

## Output Schema
```
{
  deploy_ready: boolean,
  checklist: [ { item: string, status: "pass" | "fail" | "skipped", note: string } ],
  deploy_command: string,
  deployed_url: string,
  deployment_id: string,
  rollback_command: string,
  verification: [ { check: string, result: "pass" | "fail", detail: string } ],
  open_risks: [ string ]
}
```

## Output Format
```markdown
# Deploy Report — <project name>

## Pre-Deploy Checklist
- [x] wrangler.toml valid
- [x] build passes clean
- [ ] FAIL: missing secret `STRIPE_KEY` in production — blocked deploy

## Deploy
Command run: `wrangler deploy`
Deployed URL: https://your-app.workers.dev
Deployment ID: <id>

## Verification
- Live URL returns 200: yes
- Feature works live: yes / no — detail
- Error logs clean (first 5 min): yes / no

## Rollback
If something breaks: `wrangler rollback <previous-deployment-id>`

## Open Risks
- <anything skipped or uncertain>
```

## Error Handling
- No `wrangler.toml` found → this is a first-time setup, walk through creating one rather than guessing config
- Missing account_id/auth → tell the user to run `wrangler login` or `wrangler whoami`, don't fabricate credentials
- Secrets missing for target env → stop and hand off to `env-secrets-manager`, don't deploy with blanks
- User asks to deploy something with no evidence of testing → warn explicitly, ask to confirm before proceeding
- D1 migration pending but not applied → apply migrations first, never deploy code against a schema that isn't live yet
- Ambiguous target environment (user just says "deploy") → default to asking whether this is staging or production if the project has both configured; if only one environment exists, proceed with it

## Examples
**Example 1**
User: "deploy this to cloudflare, the login feature is done"
Skill runs the pre-deploy checklist, finds `wrangler.toml` is missing `compatibility_date`, fixes it, confirms secrets are set, runs `wrangler deploy`, verifies the live login page loads, reports the deployment ID and rollback command.

**Example 2**
User: "push my pages site live"
Skill checks the build output directory matches the Pages project settings, confirms the branch is connected correctly, either triggers a git-based deploy or runs `wrangler pages deploy dist`, then verifies the live URL serves the new build.

**Example 3**
User: "something broke after I deployed, help"
Skill pulls the last deployment ID, checks `wrangler tail` for the actual error, and gives the `wrangler rollback` command to that previous deployment ID immediately, then diagnoses the root cause after service is restored.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- ci-cd-pipeline-builder (S8-Deployment)
- monitoring-alerting-setup (S9-Operations)
- incident-runbook-writer (S9-Operations)

### Fed By
- browser-verifier (S7-Testing)
- security-review-lite (S7-Testing)

### Feedback Loop
- Failed deploys and post-deploy incidents should tighten the pre-deploy checklist so the same failure mode gets caught before the next deploy, not after.

```yaml
chain_metadata:
  skill_slug: "cloudflare-deployer"
  stage: "deployment"
  timestamp: string
  suggested_next:
    - "ci-cd-pipeline-builder"
    - "monitoring-alerting-setup"
```
