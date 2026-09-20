---
name: env-secrets-manager
description: >
  Sets up and audits environment variables and secrets across dev, staging, and
  production for a Cloudflare Workers app using wrangler, so keys never get committed
  or leaked.
  Use this skill when the user asks about managing API keys, env vars, or secrets,
  or says
  "how do I add a secret to my worker", "where do my API keys go", "set up my env vars for production",
  "did I accidentally commit a key", "my secret isn't showing up in production", "manage secrets across environments",
  "rotate this API key".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "cloudflare", "secrets", "security"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Deployment
---

# Environment & Secrets Manager

Sets up environment variables and secrets correctly across dev, staging, and production for a Cloudflare Workers app, and audits an existing project for leaked keys or missing secrets before a deploy. The core rule this skill enforces: secrets live in `wrangler secret` (or the dashboard), never in `wrangler.toml`, never in a committed `.env` file.

## Stage
This skill belongs to Stage S5: Deployment

## When to Use
- Setting up a new project's env vars/secrets for the first time
- A deploy is failing because a required secret isn't set in that environment
- The user isn't sure whether their API keys are safely handled or accidentally exposed
- Adding a new third-party API key (Stripe, OpenAI, etc.) to an existing app
- Rotating a compromised or expiring key
- Setting up separate keys for dev/staging/prod (e.g. Stripe test vs. live keys)

## Input Schema
```
project:
  wrangler_toml_path: string
  environments: [ "dev" | "staging" | "production" ]
  secrets_needed: [ { name: string, used_for: string, per_env_different: boolean } ]
  non_secret_vars_needed: [ { name: string, value: string } ]
  check_for_leaks: boolean
```

## Workflow
### Step 1: Separate secrets from plain config
Draw the line clearly: non-secret config (feature flags, public URLs, environment names) goes in `[vars]` in `wrangler.toml` and is fine to commit. Anything that grants access — API keys, database credentials, signing secrets, tokens — is a secret and never goes in `wrangler.toml` or any committed file.

### Step 2: Set up local dev secrets
Create a `.dev.vars` file in the project root (not `.env` — Wrangler's convention is `.dev.vars`) with `KEY=value` lines for local development. Confirm `.dev.vars` is listed in `.gitignore`. If it isn't, add it immediately, before anything else.

### Step 3: Set production/staging secrets via Wrangler
For each secret, run:
```
wrangler secret put SECRET_NAME
```
(prompts for the value interactively, never appears in shell history). Repeat per environment if using named environments: `wrangler secret put SECRET_NAME --env staging`. For bulk setup, `wrangler secret bulk <file.json>` can push multiple at once from a local JSON file that itself must never be committed.

### Step 4: Confirm what's actually set
Run `wrangler secret list` (and `--env staging` / `--env production` as applicable) to see which secret names exist per environment — note this shows names only, never values, by design. Cross-check this list against `secrets_needed` from the input to catch anything missing before a deploy.

### Step 5: Audit for leaks
Before any deploy or when explicitly asked, check for secrets that shouldn't be where they are:
- Search the repo for hardcoded key patterns (e.g. `sk_live_`, `sk-`, long hex/base64 strings assigned to variables named like keys) — flag any match for review
- Confirm `.dev.vars`, `.env`, `.env.local` are all in `.gitignore`
- Check `wrangler.toml`'s `[vars]` section for anything that looks like it should be a secret instead
- If using git, check `git log` for a file that was committed and later removed — removal doesn't erase it from history; a leaked key found this way must be rotated, not just deleted

### Step 6: Rotate a compromised or expiring key
1. Generate the new key at the provider (Stripe, OpenAI, etc.)
2. `wrangler secret put SECRET_NAME` with the new value (overwrites cleanly, no downtime for the update itself)
3. Deploy so the Worker picks up the new binding
4. Revoke the old key at the provider only after confirming the new one works live
5. If the key was ever committed to git history, treat it as permanently compromised even after rotation — rotating doesn't erase the leak, it just stops it from being useful going forward

### Step 7: Self-Validation
- [ ] No secret exists in `wrangler.toml`, `.env`, or any committed file
- [ ] `.dev.vars` and any local secret files are confirmed in `.gitignore`, not assumed
- [ ] Secrets set per-environment match what each environment actually needs (test keys in dev/staging, live keys only in production)
- [ ] `wrangler secret list` output was checked against the required list, not skipped
- [ ] Any leak found triggered a rotation recommendation, not just a "delete the line" fix

## Output Schema
```
{
  environments_checked: [ string ],
  secrets_status: [ { name: string, dev: "set"|"missing", staging: "set"|"missing", production: "set"|"missing" } ],
  plain_vars_in_wrangler_toml: [ string ],
  gitignore_covers_secret_files: boolean,
  leaks_found: [ { file: string, pattern_matched: string, in_git_history: boolean } ],
  rotation_needed: [ string ]
}
```

## Output Format
```markdown
# Secrets Audit — <project name>

## Secrets status
| Secret | Dev | Staging | Production |
|---|---|---|---|
| STRIPE_KEY | set (test) | set (test) | set (live) |
| OPENAI_KEY | set | missing | missing |

## Plain config (safe, in wrangler.toml)
- ENVIRONMENT=production
- API_BASE_URL=https://api.example.com

## Leak check
.gitignore covers .dev.vars/.env: yes/no
Hardcoded keys found in repo: none / <file:line — flagged>
Keys found in git history: none / <found, rotation required>

## Action needed
- Set OPENAI_KEY in staging and production: `wrangler secret put OPENAI_KEY --env staging`
- Rotate STRIPE_KEY (found in git history at commit <hash>)
```

## Error Handling
- Deploy fails with an undefined variable error → almost always a missing secret in that specific environment; check `wrangler secret list --env <env>` before anything else
- User wants to "just put the key in the code to test quickly" → refuse this specific shortcut, use `.dev.vars` instead, it's just as fast and doesn't create a leak risk
- A `.env` file (not `.dev.vars`) already exists and is being read by custom code → note Wrangler doesn't read `.env` natively; either migrate to `.dev.vars` or ensure the custom loader also isn't committing the file
- Key found already committed to git → treat as compromised regardless of whether it's since been deleted from the working tree; recommend rotation, not just a `.gitignore` fix
- Same secret name needed with different values per environment (e.g. Stripe test vs. live) → use named environments in `wrangler.toml` and set the secret separately per `--env`, never reuse a live key in dev/staging
- User unsure which values are secret vs. safe to commit → default to treating anything that authenticates or authorizes as a secret; when in doubt, treat it as a secret

## Examples
**Example 1**
User: "how do I add my Stripe key to my worker"
Skill explains the dev/prod split: test key into `.dev.vars` for local dev, live key via `wrangler secret put STRIPE_KEY` for production, confirms `.dev.vars` is gitignored.

**Example 2**
User: "my deploy is failing, says API key is undefined"
Skill runs `wrangler secret list --env production`, finds the secret was only ever set for dev, sets it for production, redeploys, verifies.

**Example 3**
User: "did I accidentally commit a key at some point"
Skill scans the repo and git history for key-shaped strings, finds one in an old commit, confirms it's still live at the provider, and walks through rotating it immediately.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- cloudflare-deployer (S5-Deployment)
- security-review-lite (S4-Testing)

### Fed By
- security-review-lite (S4-Testing)
- ci-cd-pipeline-builder (S5-Deployment)

### Feedback Loop
- Every leak or missing-secret incident found should be added to the pre-deploy checklist in `cloudflare-deployer` so the same category of mistake is caught automatically before the next deploy.

```yaml
chain_metadata:
  skill_slug: "env-secrets-manager"
  stage: "deployment"
  timestamp: string
  suggested_next:
    - "cloudflare-deployer"
    - "security-review-lite"
```
