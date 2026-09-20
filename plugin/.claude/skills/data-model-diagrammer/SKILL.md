---
name: data-model-diagrammer
description: >
  Design a database schema or data model for a feature or app from a plain-language
  description, output as an ER diagram description plus table definitions.
  Use this skill when the user asks about designing a database, planning tables,
  or says
  "what tables do I need for this", "design the schema for this feature",
  "how should I structure my database", "what fields does this table need",
  "help me plan my data model", "should this be one table or two",
  "what's the relationship between these", "set up my database structure".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "database", "schema", "data-model"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# Data Model Diagrammer

Turns a plain-language description of a feature or app into a concrete database schema: tables, columns, types, keys, and relationships, plus a text-based ER diagram anyone can read without special tools. Gets the data layer right before any backend code is written, since a bad schema is the most expensive thing to fix later.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- Starting a new feature that needs to store data and the tables don't exist yet
- The user describes what the app should do but hasn't thought about how data is structured
- Adding a feature to an existing app and needs to know if it's a new table, a new column, or a join table
- The user is unsure about one-to-many vs many-to-many for a relationship
- Migrating from a spreadsheet or no-database prototype into a real schema
- Before writing any migration file or ORM model

## Input Schema
```
feature_or_app_description: string   # plain language description of what needs storing
existing_tables: string[]?           # names/columns of tables that already exist
db_type: string?                     # postgres, sqlite, mysql, D1, etc. (default: postgres-style, notes portability)
scale_notes: string?                 # expected volume/growth if relevant (optional)
```

## Workflow
### Step 1: List the "things" (entities)
Read the description and pull out every noun that needs to persist (user, order, subscription, invite, etc.). Ignore transient UI state — only things that must survive a page refresh belong here.

### Step 2: Define each table
For each entity, list columns with types, nullability, and defaults. Always include: primary key (id), created_at, updated_at unless there's a clear reason not to. Use the simplest sensible type (don't over-normalize for an MVP).

### Step 3: Map relationships
For each pair of related entities, decide one-to-one, one-to-many, or many-to-many. For many-to-many, define the join table explicitly with its own name and any extra columns (e.g. role on a users_teams join).

### Step 4: Add constraints and indexes
Call out foreign keys, unique constraints (e.g. email must be unique), and indexes needed for expected query patterns (e.g. index on user_id for fast lookups).

### Step 5: Draw the ER diagram in text
Produce a readable text-based diagram (entity blocks with fields, arrows showing relationship type and direction) that doesn't require a diagramming tool to understand.

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] Every entity from the description has a table
- [ ] Every relationship has a clear cardinality (1:1, 1:many, many:many)
- [ ] No table is missing a primary key
- [ ] Foreign keys point to the correct parent table
- [ ] Nothing duplicates data that should live in one place (basic normalization)
- [ ] Naming is consistent (snake_case or camelCase picked once, applied everywhere)

## Output Schema
```json
{
  "tables": [
    {
      "name": "string",
      "columns": [
        {"name": "string", "type": "string", "nullable": "boolean", "default": "string | null", "notes": "string | null"}
      ],
      "primary_key": "string",
      "foreign_keys": [{"column": "string", "references": "table.column"}],
      "indexes": ["string"],
      "unique_constraints": ["string"]
    }
  ],
  "relationships": [
    {"from": "string", "to": "string", "type": "1:1 | 1:many | many:many", "via": "string | null"}
  ],
  "diagram": "string"
}
```

## Output Format
```markdown
# Data Model: <Feature/App Name>

## Tables

### users
| Column | Type | Null? | Default | Notes |
|---|---|---|---|---|
| id | uuid | no | gen_random_uuid() | primary key |
| email | text | no | | unique |
| created_at | timestamptz | no | now() | |

### <next table>
...

## Relationships
- users 1:many orders (orders.user_id -> users.id)
- users many:many teams via team_members (team_members.role)

## ER Diagram (text)
```
[users] --1:many--> [orders]
[users] --many:many, via team_members--> [teams]
```

## Migration notes
- <any db-specific notes, e.g. "D1 has no native uuid type, use TEXT">
```

## Error Handling
- If the description doesn't give enough detail to know a field's type, pick the sensible default and flag it as an assumption rather than blocking.
- If existing tables are provided, never redesign them wholesale — only add new tables/columns needed for the new feature, and flag any conflict.
- If a relationship is ambiguous (could be 1:many or many:many), ask one clarifying question before committing to a join table, since that changes the query patterns.
- If the target db_type has known constraints (e.g. Cloudflare D1 = SQLite, no native array/json indexing), call these out explicitly in migration notes.
- If the user asks for something that would require a full redesign of existing tables, stop and recommend architecture-decision-writer instead of quietly reworking their schema.

## Examples

**Example 1**
User: "I'm building a SaaS where teams can invite members and assign roles. What tables do I need?"
Skill does: identifies entities (users, teams, team_members join table with role column, invites), maps team_members as many:many join, invites as its own table with status/expiry, draws ER diagram.
Outcome: user hands the table definitions straight to a migration file.

**Example 2**
User: "Adding a 'saved reports' feature to my existing app. Users table already exists."
Skill does: reuses existing users table as-is, adds one new saved_reports table with user_id foreign key, 1:many relationship, no schema changes to existing tables.
Outcome: clean additive migration with zero risk to existing data.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- api-endpoint-builder (S6-Building)
- seed-data-generator (S9-Operations)
- multi-tenant-manager (S9-Operations)

### Fed By
- feature-task-breakdown (S6-Building)
- prd-writer (S5-Planning)

### Feedback Loop
When query performance issues or awkward joins show up during testing or operations, feed those findings back into this skill so future schemas index and normalize better from the start.

```yaml
chain_metadata:
  skill_slug: "data-model-diagrammer"
  stage: "building"
  timestamp: string
  suggested_next:
    - "api-endpoint-builder"
    - "seed-data-generator"
    - "multi-tenant-manager"
```
