---
name: api-endpoint-builder
description: >
  Design and scaffold a clean REST or API endpoint — routes, request/response shape,
  validation, and error cases — for one described feature.
  Use this skill when the user asks about building an API route, designing a backend
  endpoint, or says
  "build me an endpoint for this", "what should this API route look like",
  "design the request and response for this feature", "add an API for creating X",
  "how should I validate this input", "what error codes should this return",
  "scaffold the backend for this feature", "set up the route for this".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "api", "backend", "rest"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S6-Building
---

# API Endpoint Builder

Designs and scaffolds one clean API endpoint for a described feature: the route, method, request shape, response shape, validation rules, auth requirement, and every realistic error case. Keeps the endpoint scoped to exactly one operation so it can be built and verified in isolation instead of sprawling into a half-finished mini-framework.

## Stage
This skill belongs to Stage S6: Building

## When to Use
- A feature task from feature-task-breakdown calls for a new backend endpoint
- The user needs to add, update, or fetch data through an API and hasn't defined the contract yet
- An existing endpoint is growing unclear and needs its request/response shape nailed down
- The user is about to wire a frontend form to a backend and needs the API shape first
- Adding auth, validation, or error handling to an endpoint that currently has none
- Working in a Cloudflare Workers / Hono / Express / Flask-style backend and needs a route scaffold

## Input Schema
```
feature_description: string     # what this endpoint needs to do, plain language
resource: string?               # the entity it operates on (e.g. "invoice")
framework: string?              # e.g. Hono/Workers, Express, Flask, Next.js route handlers
auth_required: boolean?         # default: true unless stated otherwise
existing_endpoints: string[]?   # related routes already in the app, for consistency
```

## Workflow
### Step 1: Pin the single operation
Name exactly one thing this endpoint does (create invoice, list invoices, get invoice by id). If the request implies multiple operations, split into multiple endpoints — one route, one job.

### Step 2: Define the contract
Method + path (e.g. `POST /api/invoices`), request body/query/params shape, response shape on success, and status code. Keep naming consistent with any existing_endpoints provided.

### Step 3: Define validation rules
List every field's validation (required, type, format, min/max, uniqueness) before writing code. Flag which validations must happen server-side even if also checked client-side (never trust the client).

### Step 4: Define every realistic error case
Cover: missing/invalid auth (401/403), validation failure (400), not found (404), conflict/duplicate (409), rate limit if relevant (429), and unexpected server error (500). Give the actual response shape for each, not just the code.

### Step 5: Scaffold the code
Write the endpoint handler in the specified framework (or a reasonable default), including validation, auth check, the core logic as a clearly marked TODO/stub if business logic depends on other unbuilt pieces, and the error responses.

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] Endpoint does exactly one operation
- [ ] Every input field has a stated validation rule
- [ ] Every realistic error case has a defined response, not just a generic 500
- [ ] Auth requirement is explicit, not assumed
- [ ] Response shape is consistent with any existing endpoints shown
- [ ] Nothing trusts client-side validation alone

## Output Schema
```json
{
  "method": "string",
  "path": "string",
  "auth_required": "boolean",
  "request": {"body": "object", "query": "object", "params": "object"},
  "response_success": {"status": "number", "body": "object"},
  "errors": [
    {"status": "number", "case": "string", "body": "object"}
  ],
  "code_scaffold": "string"
}
```

## Output Format
```markdown
# Endpoint: <METHOD> <path>

**Auth required:** <yes/no, and what kind>

## Request
- Body: `{ field: type, ... }`
- Validation: <rule per field>

## Success Response
`<status>` 
```json
{ ... }
```

## Error Responses
| Status | Case | Body |
|---|---|---|
| 400 | invalid input | `{ "error": "..." }` |
| 401 | not authenticated | `{ "error": "..." }` |
| 404 | not found | `{ "error": "..." }` |

## Code scaffold
```<language>
<endpoint handler code, with TODO markers where business logic depends on unbuilt pieces>
```

## Verify
- <curl/fetch command or test to run to confirm the endpoint behaves as designed>
```

## Error Handling
- If the request bundles multiple operations under one endpoint idea, split it into separate endpoint designs and say so.
- If auth strategy isn't defined anywhere in the app yet, flag that auth-flow-builder needs to run first rather than guessing at a scheme.
- If the data shape depends on a table that doesn't exist yet, flag that data-model-diagrammer should run first, and scaffold against the assumed shape clearly marked as an assumption.
- If framework isn't specified, default to a simple, portable style (plain async handler) and note the framework assumption at the top of the output.
- If existing_endpoints show an inconsistent naming/response convention, don't silently pick one — point out the inconsistency and ask which convention to follow.

## Examples

**Example 1**
User: "I need an endpoint to let a logged-in user create an invoice."
Skill does: defines `POST /api/invoices`, auth required (session/JWT), validates amount/client_id/due_date, covers 400/401/404 (client not found)/500, scaffolds a Hono handler with TODO for the actual invoice creation logic pending data-model-diagrammer output.
Outcome: user has a testable, isolated endpoint spec to build and verify before touching the frontend.

**Example 2**
User: "Add a public endpoint to check if an email is already signed up, no login needed."
Skill does: defines `GET /api/check-email?email=`, auth_required false, adds rate limiting note (429) to prevent enumeration abuse, response shape `{ available: boolean }` only (no user data leak).
Outcome: catches a security consideration (email enumeration) the user hadn't thought about.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- ui-component-builder (S6-Building)
- test-case-generator (S7-Testing)
- security-review-lite (S7-Testing)

### Fed By
- data-model-diagrammer (S6-Building)
- feature-task-breakdown (S6-Building)
- auth-flow-builder (S6-Building)

### Feedback Loop
When security-review-lite or test-case-generator finds gaps (missing validation, unhandled error case), feed those back so future endpoint scaffolds include that case by default.

```yaml
chain_metadata:
  skill_slug: "api-endpoint-builder"
  stage: "building"
  timestamp: string
  suggested_next:
    - "ui-component-builder"
    - "test-case-generator"
    - "security-review-lite"
```
