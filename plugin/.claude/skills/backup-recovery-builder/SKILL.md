---
name: backup-recovery-builder
description: >
  Builds a real, tested backup and recovery plan for a SaaS app's database
  and file storage, including an actual restore drill, not just a backup
  schedule nobody has verified works.
  Use this skill when the user asks about "how do I back up my database",
  "what happens if I lose my data", "set up backups for my app", "I've
  never tested my backups", "disaster recovery plan", "what if Cloudflare
  D1 gets corrupted", or "I'm scared of losing customer data".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "backups", "disaster-recovery", "ops", "database"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Operations
---

# Backup & Recovery Builder

Builds a backup plan sized to a small live SaaS — regular automated backups of the database and any user-uploaded files, a written restore procedure, and a scheduled drill that actually proves the restore works. A backup nobody has restored from is not a backup, it's a hope.

## Stage
This skill belongs to Stage S6: Operations

## When to Use
- The app just went live with real customer data and no backup plan exists
- The founder realizes they've never actually tried restoring from a backup
- Migrating databases or hosting providers (backup before, verify after)
- A near-miss happened (accidental delete, bad migration) that didn't lose data but could have
- Onboarding a first paying customer who asks about data durability
- Periodic review: it's been 3+ months since the last restore drill

## Input Schema
```
database: enum              # cloudflare-d1 | postgres | supabase | mysql | sqlite | other
file_storage: enum | none   # cloudflare-r2 | s3 | none
data_sensitivity: enum      # low | customer-pii | payment-data
current_backup_setup: string | none
acceptable_data_loss: string   # e.g. "up to 24 hours" (this is the RPO)
acceptable_downtime: string    # e.g. "a few hours" (this is the RTO)
team_size: number           # usually 1 for this pack's audience
```

## Workflow
### Step 1: Establish the real requirement (RPO/RTO in plain language)
Ask, in plain terms: "if you lost everything right now, how much data are you OK losing (last hour? last day?) and how long can the app be down while you fix it?" Translate the answer into RPO (recovery point objective) and RTO (recovery time objective) without using those acronyms with the user unless they use them first.

### Step 2: Pick the backup method for the actual stack
- **Cloudflare D1**: use `wrangler d1 export` on a schedule (Cloudflare Cron Trigger calling a Worker that exports and writes to R2), or Cloudflare's built-in D1 time-travel (30-day point-in-time recovery) as the first line of defense — cheap and often enough for a small app.
- **Postgres (Supabase, Neon, etc.)**: use the provider's built-in daily automated backups (usually on by default on paid tiers) plus a periodic manual `pg_dump` stored in R2/S3 as a second copy outside the provider.
- **File storage (R2/S3)**: enable versioning if available; for critical files, a weekly sync job to a second bucket/provider is cheap insurance against one provider having a bad day.
- Always keep backups in a different place than the primary data lives — a backup in the same database/account that gets deleted is not a real backup.

### Step 3: Automate it, don't rely on memory
Write the exact scheduled job (cron expression, trigger tool, destination). If nothing else, a nightly export triggered by a Cloudflare Cron Trigger or GitHub Actions scheduled workflow satisfies this for a small app — no need for enterprise backup software.

### Step 4: Write the restore procedure
Document, step by step, exactly what commands/clicks restore from the latest backup, including how to find the latest backup file and how to point the app at the restored data. This must be specific enough that a stressed founder at 2am can follow it without thinking.

### Step 5: Run (or schedule) an actual restore drill
This is the step most people skip and the whole point of this skill. Recommend restoring the latest backup into a throwaway/staging environment and verifying the data looks right — on first setup, and then on a recurring cadence (quarterly is reasonable for a small app). If the user is doing this live, walk them through it now rather than just describing it.

### Step 6: Self-Validation
- [ ] Backup method is automated, not "I'll remember to do it"
- [ ] Backup copy lives somewhere other than the primary data's own account/provider
- [ ] Restore procedure is written as literal steps, not a description of the concept
- [ ] A restore drill has either been run or is explicitly scheduled with a date
- [ ] RPO/RTO stated in plain language match what the backup method can actually deliver
- [ ] Plan is sized to a small app — no recommendation of enterprise backup tooling unless asked

## Output Schema
```
{
  rpo: string,
  rto: string,
  backup_jobs: [ { source: string, method: string, schedule: string, destination: string } ],
  restore_procedure: string[],
  drill_status: { last_run: string | "never", next_scheduled: string },
  risks_not_covered: string[]
}
```

## Output Format
```markdown
# Backup & Recovery Plan — <app name>

## Targets
- Acceptable data loss (RPO): <e.g. 24 hours>
- Acceptable downtime (RTO): <e.g. a few hours>

## Backup jobs
| Source | Method | Schedule | Stored Where |
|---|---|---|---|
| D1 database | wrangler d1 export via Cron Trigger | nightly 3am UTC | R2 bucket `backups/` |
| ... | ... | ... | ... |

## Restore procedure
1. ...
2. ...
3. Verify: <what "it worked" looks like>

## Restore drill
- Last tested: <date or "never — run this now">
- Next scheduled: <date, quarterly recommended>

## Known gaps
- ...
```

## Error Handling
- If the user has never backed up anything, don't overwhelm — set up the single most important backup (the primary database) first, then expand
- If data_sensitivity is customer-pii or payment-data, flag that backups themselves need to be encrypted/access-restricted, and note this overlaps with compliance-checker (S8-Meta)
- If the database platform has native point-in-time recovery (like D1 time-travel), recommend using it as the baseline before building custom export jobs — don't reinvent what's already provided
- If the user can't say what their acceptable data loss window is, default to "24 hours" and flag it as an assumption to revisit
- If a restore drill has never been run, treat that as the single highest-priority action item in the output, above any new tooling

## Examples
**Example 1**: User says "I just realized I have no backups and I have 40 paying customers." Skill sets RPO to 24h as a reasonable default, sets up nightly D1 export to R2 via a Cron Trigger, writes the restore steps, and schedules an immediate first drill.

**Example 2**: User says "we back up nightly but I've never tried restoring." Skill skips Steps 2-3 (already done), focuses on Step 4-5: writing the restore procedure and running a drill into a staging environment right now.

**Example 3**: User migrating from Supabase to a self-hosted Postgres. Skill treats the migration itself as a backup checkpoint — full dump before migration, verified restore into the new environment, drill run as part of the cutover.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- incident-runbook-writer (S6-Operations)
- compliance-checker (S8-Meta)

### Fed By
- cloudflare-deployer (S5-Deployment)
- data-model-diagrammer (S3-Building)

### Feedback Loop
Every restore drill result (success, time taken, gaps found) should update the restore procedure and the next drill date — a drill that reveals a problem is the plan improving, not failing.

```yaml
chain_metadata:
  skill_slug: "backup-recovery-builder"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "incident-runbook-writer"
    - "compliance-checker"
```
