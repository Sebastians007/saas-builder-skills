---
name: multi-tenant-manager
description: >
  Plans and reviews data isolation and tenant-scoping for a multi-customer
  SaaS so one organization's data can never leak into another's.
  Use this skill when the user asks about "how do I separate customer
  data", "multi-tenant architecture", "can one customer see another's
  data", "add organizations to my app", "tenant isolation", "row-level
  security for customers", or "I'm worried about a data leak between
  accounts".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "multi-tenancy", "data-isolation", "security", "database"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Operations
---

# Multi-Tenant Manager

Plans and audits how a SaaS with multiple customer organizations (tenants) keeps each tenant's data strictly separated. This is the skill that catches the single most damaging bug class in B2B SaaS — one customer seeing another customer's data — before it ships, or finds it if it's already live.

## Stage
This skill belongs to Stage S6: Operations

## When to Use
- Adding "organizations" or "teams" to an app that started single-user
- Designing the database schema for a new multi-tenant app
- Reviewing existing code/queries for missing tenant checks before a security-sensitive customer signs
- A near-miss or actual report of cross-tenant data exposure
- Adding a new feature (e.g. file uploads, search, exports) that touches shared data and needs tenant scoping applied
- Preparing for a customer's security questionnaire or SOC 2-lite conversation

## Input Schema
```
tenant_model: enum            # single-db-shared-schema | single-db-schema-per-tenant | db-per-tenant
database: enum                # cloudflare-d1 | postgres | supabase | mysql | other
auth_system: string           # e.g. "custom JWT", "Clerk", "Supabase Auth"
existing_tenant_field: string | none   # e.g. "org_id" if it already exists
features_touching_data: string[]      # e.g. ["dashboard queries", "file uploads", "search", "exports", "admin panel"]
known_incidents: string | none        # any past cross-tenant leak, even a near-miss
```

## Workflow
### Step 1: Confirm the tenancy model
For a small SaaS on Cloudflare, the almost-always-right default is **single database, shared schema, every table has a `tenant_id`/`org_id` column**. Schema-per-tenant or database-per-tenant adds real operational cost (migrations run N times, backups multiply) and is only worth it at a scale or compliance tier this audience usually isn't at yet — flag that but don't force it if the user has a real reason.

### Step 2: Map every table and query path that touches tenant data
List every table that stores customer-created data. For each one, confirm it has a `tenant_id` column and a `NOT NULL` constraint on it. Then list every code path that reads data (API endpoints, admin panel, background jobs, exports, search) and check each one filters by the current user's tenant_id — not just at the UI layer, but at the query layer.

### Step 3: Enforce isolation at the lowest layer possible
Rank enforcement mechanisms from strongest to weakest and recommend the strongest one the stack supports:
1. Database-level (Postgres Row-Level Security policies tied to the session's tenant) — strongest, survives a forgotten WHERE clause
2. A shared query-builder/ORM helper that always injects `WHERE tenant_id = ?` and is the only sanctioned way to query — good middle ground, works on D1/MySQL where native RLS isn't available
3. Manual `WHERE tenant_id = ?` on every query — weakest, one missed clause is a leak; only acceptable in a very small, well-reviewed codebase

Cloudflare D1 has no native RLS, so for D1 apps recommend a mandatory query-helper pattern and flag it explicitly as the compensating control.

### Step 4: Check the auth and session layer
Confirm tenant_id is derived from the authenticated session/JWT server-side, never trusted from a client-supplied parameter (e.g. never `?org_id=123` in a URL that the server blindly trusts). Check that switching between organizations (if a user belongs to multiple) properly resets which tenant_id is active.

### Step 5: Write test cases for the leak
Produce concrete test scenarios: "User A in Org 1 requests resource X owned by Org 2 — expect 403/404, not data." Hand these off to test-case-generator or edge-case-hunter for full test authoring; this skill's job is to identify where the tests need to exist.

### Step 6: Self-Validation
- [ ] Every data table has a tenant scoping column identified
- [ ] Every listed feature/endpoint has a stated enforcement mechanism, not just "should be fine"
- [ ] Enforcement happens server-side at the query layer, not just hidden in the UI
- [ ] At least one cross-tenant test case is written per sensitive feature
- [ ] Recommendation matches the stack's real capabilities (no RLS recommended for D1)
- [ ] If known_incidents was provided, the specific leak path is explicitly addressed

## Output Schema
```
{
  tenant_model: string,
  enforcement_layer: string,
  tables: [ { name: string, tenant_column: string, has_not_null: boolean, gap: string | null } ],
  endpoints: [ { name: string, enforcement: string, gap: string | null } ],
  test_cases: string[],
  priority_fixes: string[]
}
```

## Output Format
```markdown
# Multi-Tenant Isolation Plan — <app name>

## Tenancy model
<single-db-shared-schema | schema-per-tenant | db-per-tenant> — <why>

## Enforcement layer
<primary mechanism> + <compensating control if applicable>

## Table audit
| Table | Tenant Column | NOT NULL? | Gap |
|---|---|---|---|
| projects | org_id | yes | none |
| files | org_id | no | missing constraint |

## Endpoint/feature audit
| Feature | Enforcement | Gap |
|---|---|---|
| dashboard queries | query-helper enforces org_id | none |
| exports | manual WHERE clause | risk — not using shared helper |

## Cross-tenant test cases to add
1. ...
2. ...

## Priority fixes (do these first)
1. ...
```

## Error Handling
- If the app is currently single-tenant and the user wants to add multi-tenancy, treat this as a schema migration project — surface that existing data needs a tenant_id backfill before enforcement can be turned on
- If existing_tenant_field is none and features_touching_data is non-empty, assume tenancy hasn't been designed yet and start from Step 1, not Step 2
- If known_incidents describes an actual leak, prioritize finding and closing that exact path above the general audit
- If the database is D1, never recommend Postgres RLS as if it's available — always name the query-helper pattern as the D1-appropriate control
- If the user wants database-per-tenant "for security," push back gently — shared schema with strong enforcement is usually safer AND cheaper at this scale, since isolation depends on code discipline either way

## Examples
**Example 1**: User says "I'm adding teams/orgs to my app, how do I make sure they can't see each other's stuff." Skill confirms shared-schema-with-org_id model, audits the existing tables (none have org_id yet), and outputs a migration plan plus a query-helper pattern to enforce it everywhere.

**Example 2**: User says "a customer says they briefly saw another company's project name in a dropdown." Skill treats this as known_incidents, traces likely cause (probably an unscoped autocomplete/search query), and prioritizes that endpoint's fix above the general audit.

**Example 3**: User on Postgres/Supabase asks for the strongest possible isolation. Skill recommends Postgres RLS policies tied to the authenticated tenant, since the stack supports it natively.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- security-review-lite (S4-Testing)
- edge-case-hunter (S4-Testing)
- compliance-checker (S8-Meta)

### Fed By
- data-model-diagrammer (S3-Building)
- auth-flow-builder (S3-Building)

### Feedback Loop
Any cross-tenant bug found in testing or production should be fed back as a new test case and a re-audit of the specific enforcement layer that missed it.

```yaml
chain_metadata:
  skill_slug: "multi-tenant-manager"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "security-review-lite"
    - "edge-case-hunter"
```
