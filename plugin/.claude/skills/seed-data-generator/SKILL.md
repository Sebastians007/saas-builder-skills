---
name: seed-data-generator
description: >
  Generates realistic fake data for development, testing, and demos so an
  app can be built, tested, and shown off without touching real customer
  data.
  Use this skill when the user asks about "I need test data for my app",
  "generate fake users for my database", "seed my dev database", "I want
  to demo my app but have no real data yet", "create sample customers and
  orders", "populate my database for testing", or "how do I test this
  without using real customer info".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "seed-data", "testing", "demo", "database"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Operations
---

# Seed Data Generator

Generates realistic, structurally-correct fake data — users, organizations, records, transactions — so a founder can develop, test, and demo their app without ever touching real customer data. Produces both the data itself (or a script that generates it) and a plan for keeping it out of production.

## Stage
This skill belongs to Stage S6: Operations

## When to Use
- A new feature needs a populated database to actually look/work right during development
- Preparing a demo for an investor, customer, or launch video and the app currently looks empty
- Writing tests that need consistent, repeatable sample data
- The founder has been testing against real customer data (a red flag) and needs a safe alternative
- Onboarding a new team member who needs a dev environment that isn't empty
- Multi-tenant testing that needs multiple fake organizations with isolated data to verify tenant-scoping (pairs with multi-tenant-manager)

## Input Schema
```
data_model: string              # tables/entities from data-model-diagrammer, or described inline
record_counts: object           # e.g. { users: 50, organizations: 5, orders: 200 }
realism_level: enum             # minimal (Lorem-ipsum-grade) | realistic (varied, plausible names/values) | demo-polished (curated for showing off)
edge_cases_needed: boolean      # e.g. empty states, max-length strings, weird-but-valid emails
multi_tenant: boolean           # if true, spread records across multiple fake orgs
output_format: enum             # sql-inserts | seed-script (JS/Python/TS) | csv | ORM-fixtures
target_environment: enum        # local-dev | staging | demo (never production)
```

## Workflow
### Step 1: Pull or confirm the data model
Use the data model from data-model-diagrammer if it exists; otherwise ask for (or infer from the codebase) the entities and their fields, including required fields, foreign keys, and any fields with format constraints (email, phone, enum values).

### Step 2: Decide realism level and volume
Match volume to purpose: a handful of records is fine for a quick dev check; a demo needs enough variety to not look empty or robotic (real-sounding names, varied dates, a believable distribution — not all orders exactly $99.00). For load-testing volumes, defer to load-test-builder instead of generating thousands of rows here.

### Step 3: Generate data that respects relationships and constraints
Foreign keys must point to records that actually exist in the seed set. Respect NOT NULL, unique constraints, and enum value lists exactly as defined in the schema — broken seed data that violates its own schema is worse than no seed data. If multi_tenant is true, explicitly spread records across separate fake organizations with their own tenant_id, and make sure no fake record accidentally shares an ID across tenants (useful for verifying multi-tenant-manager's isolation logic).

### Step 4: Include useful edge cases (if requested)
When edge_cases_needed is true, deliberately include: an empty-state org with zero records, a user with a very long name, an email with a plus-alias, a record right at a numeric boundary (e.g. $0.00 order, max-length text field), and a record with an unusual-but-valid unicode name — these catch UI bugs real "clean" data won't.

### Step 5: Produce the output in the requested format
Write it as an idempotent seed script where possible (can be re-run without duplicating or erroring), not a one-time SQL dump — this makes it reusable every time the dev database is reset. For Cloudflare D1, prefer a `wrangler d1 execute` seed SQL file or a small Node seed script; for Postgres, a script using the existing ORM's client keeps it in sync with the schema automatically.

### Step 6: Flag the "never in production" boundary
Explicitly state where this data should run (local/staging/demo env only) and warn against ever running a seed script against the production database — recommend an environment check (e.g. refuse to run if `NODE_ENV=production` or the DB URL matches the prod connection string).

### Step 7: Self-Validation
- [ ] All foreign keys in generated data reference records that exist in the same seed set
- [ ] No required/NOT NULL field is left empty
- [ ] Enum/constrained fields only use valid values from the actual schema
- [ ] If multi_tenant is true, records are correctly partitioned across distinct fake tenants
- [ ] Script is safe to re-run (won't duplicate/crash) and refuses to run against production
- [ ] Data looks plausible enough for demo_polished level if requested — not "user1, user2, user3"

## Output Schema
```
{
  entities_seeded: [ { name: string, count: number } ],
  script_or_data: string,        # the actual script/SQL/CSV content, or a file reference
  output_format: string,
  safety_check: string,          # how prod is protected from accidental seeding
  edge_cases_included: string[]
}
```

## Output Format
```markdown
# Seed Data — <app name>

## What was generated
| Entity | Count | Notes |
|---|---|---|
| organizations | 5 | multi-tenant, isolated |
| users | 50 | 10 per org |
| orders | 200 | varied dates/amounts |

## Output
<seed script / SQL / file path>

## Safety
- Script checks: <e.g. "refuses to run if DATABASE_URL contains 'prod'">
- Intended environment: <local-dev / staging / demo>

## Edge cases included
- ...

## How to run it
<literal command, e.g. `node scripts/seed.js` or `wrangler d1 execute DB --file=seed.sql --local`>
```

## Error Handling
- If data_model is missing and can't be inferred from the codebase, ask for the entity list rather than guessing at a schema that may not match reality
- If record_counts is unset, default to a small realistic set (~10-50 per entity) appropriate for dev/demo, not load-testing volume
- If the user asks to seed data "into production to make it look active," refuse and explain why (fake data mixed into real customer data corrupts analytics, billing, and trust) — offer a demo/staging environment seed instead
- If output_format doesn't match the stack (e.g. asking for ORM fixtures with no ORM in use), default to plain SQL inserts or a simple script instead
- If multi_tenant is true but the app has no tenant/org concept yet, note that multi-tenant-manager should run first to establish the schema

## Examples
**Example 1**: User says "my app is empty and I want to show it to a friend tonight." Skill generates demo-polished data — 5 believable organizations, varied users, and a realistic-looking order history — as a one-command seed script for local dev.

**Example 2**: User building a multi-tenant B2B app wants to verify customers can't see each other's data. Skill generates 3 fake orgs each with their own users/records, explicitly non-overlapping, to be used as test fixtures for multi-tenant-manager's cross-tenant test cases.

**Example 3**: User admits they've been testing new features against real customer data in production. Skill flags the risk, generates an equivalent local seed dataset matching the schema, and adds an environment guard to prevent future scripts from touching prod.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- test-case-generator (S4-Testing)
- multi-tenant-manager (S6-Operations)
- user-acceptance-test-planner (S4-Testing)

### Fed By
- data-model-diagrammer (S3-Building)
- multi-tenant-manager (S6-Operations)

### Feedback Loop
Bugs found using seed data (missing edge cases, unrealistic distributions) should feed back into richer seed generation rules for next time.

```yaml
chain_metadata:
  skill_slug: "seed-data-generator"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "test-case-generator"
    - "multi-tenant-manager"
```
