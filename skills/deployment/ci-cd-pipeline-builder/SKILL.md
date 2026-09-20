---
name: ci-cd-pipeline-builder
description: >
  Sets up a right-sized GitHub Actions pipeline that deploys automatically to Cloudflare
  on push, without over-engineering it for a solo project.
  Use this skill when the user asks about automating deploys, setting up CI/CD,
  or says
  "set up github actions for this", "automate my deploys", "I want deploys on push",
  "set up a CI/CD pipeline", "auto-deploy to cloudflare when I push", "stop me from making manual deploy mistakes",
  "add a build check before deploy".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "cloudflare", "ci-cd", "github-actions"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Deployment
---

# CI/CD Pipeline Builder

Builds a GitHub Actions workflow that deploys a Cloudflare Workers or Pages app automatically when code is pushed, sized correctly for a solo founder or a two-person team — one workflow file, one or two environments, no unnecessary approval gates or multi-stage pipelines that only make sense at a company with a real ops team.

## Stage
This skill belongs to Stage S8: Deployment

## When to Use
- Manual `wrangler deploy` is getting error-prone or forgotten
- The user wants deploys to happen automatically when they push to `main`
- The user wants a build/test check to block a broken deploy
- Setting up a staging branch that auto-deploys separately from production
- The project has grown past "just me running commands locally" but is still small
- The user is about to add a second contributor and wants deploys to not depend on one person's laptop

## Input Schema
```
project:
  type: "worker" | "pages" | "fullstack"
  repo: "github owner/repo"
  has_tests: boolean
  branches: { main: "production" | "staging", other branches used? }
  wants_staging_env: boolean (deploy preview branches separately from prod?)
  package_manager: "npm" | "pnpm" | "yarn"
```

## Workflow
### Step 1: Right-size the pipeline
Before writing anything, decide how much pipeline this project actually needs. Default for a solo founder: one workflow file, triggered on push to `main` (deploy to prod) and optionally on push to `staging` (deploy to a staging Worker/Pages env). Do not add manual approval gates, multi-job matrices, or separate lint/test/build/deploy jobs unless the user asks — one job that does build → test (if tests exist) → deploy is enough.

### Step 2: Set up the Cloudflare API token
Explain (don't do it for them, this requires their dashboard):
1. Cloudflare dashboard → My Profile → API Tokens → Create Token → "Edit Cloudflare Workers" template (or custom with Workers Scripts:Edit / Pages:Edit permissions as needed)
2. Copy the token, add it to GitHub repo → Settings → Secrets and variables → Actions → New repository secret, named `CLOUDFLARE_API_TOKEN`
3. Add `CLOUDFLARE_ACCOUNT_ID` as a second repo secret

### Step 3: Write the workflow file
Create `.github/workflows/deploy.yml`. Example for a Worker:
```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build --if-present
      - run: npm test --if-present
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
```
Adjust for Pages (`wrangler pages deploy <dir>` command in the wrangler-action `command` field) or for a staging branch trigger (add a second job or a branch-conditional `command`).

### Step 4: Add the test gate, only if tests exist
If `has_tests` is true, make the deploy step depend on the test step passing (default GitHub Actions behavior — steps run in order and a failed step stops the job). If there are no tests yet, don't fake a test gate; note that adding `test-case-generator` output later will make this gate meaningful.

### Step 5: Add a staging environment, only if asked
If `wants_staging_env` is true, add a second trigger on push to a `staging` branch that deploys to a separately named Worker/Pages project or a `--env staging` in `wrangler.toml`. Keep it as one extra `on.push.branches` condition, not a separate pipeline system.

### Step 6: Verify the pipeline works
Have the user push a trivial commit (or push it yourself if operating in the repo) and confirm the Action runs green in the GitHub Actions tab, and that the live URL reflects the change.

### Step 7: Self-Validation
- [ ] Pipeline is one workflow file, not an over-engineered multi-stage system
- [ ] Secrets are referenced via `secrets.*`, never hardcoded in the YAML
- [ ] The deploy step only runs after build/test steps succeed
- [ ] Confirmed with a real push, not just "the YAML looks right"
- [ ] Matches the project's actual size — no staging env added unless asked for

## Output Schema
```
{
  workflow_file_path: ".github/workflows/deploy.yml",
  triggers: [ { branch: string, deploys_to: string } ],
  required_secrets: [ string ],
  test_gate_enabled: boolean,
  verified_with_live_push: boolean
}
```

## Output Format
```markdown
# CI/CD Pipeline — <project name>

## What was set up
- Push to `main` → deploys to production via `wrangler deploy`
- (if applicable) Push to `staging` → deploys to staging environment

## Required GitHub secrets (add these yourself)
- CLOUDFLARE_API_TOKEN
- CLOUDFLARE_ACCOUNT_ID

## Workflow file
`.github/workflows/deploy.yml` — [contents above]

## Verified
- Test push ran green: yes/no
- Live URL updated after push: yes/no

## Not added (on purpose)
- No manual approval gates — not needed at this size
- No staging environment — add later if you bring on a second dev
```

## Error Handling
- Repo secrets not set yet → give exact setup steps, don't proceed as if they exist
- No tests in the project → skip the test gate, say so plainly, don't fabricate a passing test step
- User wants a complex multi-environment pipeline for a solo project → push back gently, recommend starting with the minimal version and only escalating when there's a real second person or real traffic to justify it
- Wrangler action version drifts (breaking changes between major versions) → pin the action to a known-working major version (`@v3`) rather than `@latest`
- Existing workflow file already present → read it first, modify in place rather than overwriting blind

## Examples
**Example 1**
User: "set up github actions for this so I stop forgetting to deploy"
Skill creates `.github/workflows/deploy.yml` triggered on push to `main`, walks the user through adding the two Cloudflare secrets, and verifies with a test push.

**Example 2**
User: "I want a staging branch that deploys separately"
Skill adds a second trigger on push to `staging` deploying to a separately named staging Worker, keeping the same single workflow file.

**Example 3**
User: "can you add tests before deploy so broken code doesn't go live"
Skill checks whether tests exist; if not, tells the user to run `test-case-generator` first, then wires the resulting test command into the pipeline as a blocking step.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- cloudflare-deployer (S8-Deployment)
- monitoring-alerting-setup (S9-Operations)

### Fed By
- regression-test-builder (S7-Testing)
- cloudflare-deployer (S8-Deployment)

### Feedback Loop
- If a deploy breaks something the pipeline's checks didn't catch, add that specific check (build error, missing env var, failed test) to the pipeline so the same class of failure is caught automatically next time.

```yaml
chain_metadata:
  skill_slug: "ci-cd-pipeline-builder"
  stage: "deployment"
  timestamp: string
  suggested_next:
    - "cloudflare-deployer"
    - "monitoring-alerting-setup"
```
