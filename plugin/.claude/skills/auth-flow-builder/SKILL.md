---
name: auth-flow-builder
description: >
  Plan and scaffold a secure, correctly-scoped auth flow (signup, login, session,
  password reset) for a SaaS app, calling out common security mistakes to avoid.
  Use this skill when the user asks about adding login/signup, setting up authentication,
  or says
  "add login to my app", "set up user accounts", "how do I handle passwords securely",
  "build a signup flow", "add password reset", "how should sessions work",
  "is my auth setup secure", "help me add authentication without messing up security".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "auth", "security", "sessions"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Building
---

# Auth Flow Builder

Plans and scaffolds a SaaS app's authentication flow — signup, login, session handling, password reset, and logout — scoped to exactly what the app needs right now, with the common security mistakes non-technical builders make called out explicitly before code is written. Auth is the one place where "just wing it with AI" causes real damage, so this skill front-loads the security checklist instead of bolting it on after.

## Stage
This skill belongs to Stage S3: Building

## When to Use
- Starting a new SaaS app that needs user accounts
- Adding password reset or "forgot password" to an app that only has login
- The user is unsure whether their current auth setup is secure
- Migrating from a third-party auth provider to custom auth, or vice versa
- Adding session/token handling for API access
- Before any endpoint that needs "is this user logged in" logic (should exist before api-endpoint-builder needs auth_required: true)

## Input Schema
```
app_description: string           # what the app is, roughly how many users expected
auth_method: string?              # email/password, magic link, OAuth, third-party (Clerk/Auth0/Supabase)
existing_setup: string?           # what's already in place, if anything
requirements: string[]?           # e.g. "must support teams", "need email verification"
```

## Workflow
### Step 1: Recommend build-vs-buy
For most non-technical founders, recommend a managed auth provider (Clerk, Supabase Auth, Auth0, Lucia, or similar) over hand-rolled password auth unless there's a specific reason not to (data residency, cost at scale, existing custom system). State the tradeoff plainly. If the user insists on custom, proceed but flag the extra security burden clearly.

### Step 2: Define the flows needed
List only the flows the app actually needs right now: signup, login, logout, session refresh, password reset, email verification, maybe OAuth. Don't scaffold flows the app doesn't need yet (e.g. skip team invites here — that's a separate feature).

### Step 3: Define session strategy
State clearly: session cookie vs JWT vs provider-managed session, where it's stored (httpOnly cookie strongly preferred over localStorage for tokens), expiry length, and refresh behavior.

### Step 4: Call out common mistakes explicitly
Check the plan against this list and flag any that apply:
- Storing plaintext or weakly-hashed passwords (must use bcrypt/argon2, never MD5/SHA1 alone)
- Storing auth tokens in localStorage (XSS risk — use httpOnly cookies)
- No rate limiting on login/signup/reset endpoints (brute force / abuse risk)
- Password reset tokens that don't expire or aren't single-use
- Leaking whether an email exists via different error messages on login vs signup
- Missing CSRF protection on cookie-based session flows
- No email verification gate before allowing sensitive actions

### Step 5: Scaffold the flow
Write the signup/login/reset handlers (or the provider integration code) with validation, rate limiting notes, and correct session handling per Step 3-4.

### Step 6: Self-Validation
Before presenting, silently confirm:
- [ ] Every mistake in the Step 4 checklist has been explicitly checked, not skipped
- [ ] Session storage choice is stated and justified
- [ ] Password reset tokens are single-use and time-limited
- [ ] No plaintext password ever touches logs, database, or client
- [ ] Scope is limited to flows the app actually needs now

## Output Schema
```json
{
  "recommendation": "managed_provider | custom",
  "provider": "string | null",
  "flows": ["signup", "login", "logout", "password_reset", "email_verification"],
  "session_strategy": {"type": "string", "storage": "string", "expiry": "string"},
  "security_checklist": [
    {"item": "string", "status": "ok | flagged", "note": "string"}
  ],
  "code_scaffold": "string"
}
```

## Output Format
```markdown
# Auth Flow: <App Name>

## Recommendation
<Managed provider (name) or custom, with 1-2 sentence reasoning>

## Flows in scope
- Signup
- Login
- Logout
- Password reset
- (others as needed)

## Session strategy
- Type: <cookie session / JWT / provider-managed>
- Storage: <httpOnly cookie, etc.>
- Expiry: <duration>

## Security checklist
| Item | Status | Note |
|---|---|---|
| Password hashing | OK | bcrypt via provider |
| Token storage | OK | httpOnly cookie |
| Rate limiting | FLAGGED | not yet implemented, add before launch |
| Reset token expiry | OK | 1 hour, single-use |

## Code
```<language>
<scaffolded signup/login/reset handlers or provider setup code>
```

## Verify
- <steps to test signup, login, reset flow manually or via curl>

## Before launch
- <any FLAGGED items from the checklist that must be resolved>
```

## Error Handling
- If the user wants to hand-roll password auth with no stated reason, recommend a managed provider once, then proceed with their choice if they insist — don't block.
- If requirements mention teams/orgs, scope only the core auth flow here and point to a separate feature-task-breakdown for team/role management — don't bundle it in.
- If existing_setup already has auth code, review it against the Step 4 checklist rather than rebuilding from scratch, and only flag/fix what's actually wrong.
- If the app is pre-revenue/prototype stage and the user wants to skip email verification for speed, allow it but flag it explicitly as a pre-launch todo, not silently omit it.
- If asked to store or log actual user passwords/tokens for debugging, refuse and explain why (security risk, likely compliance issue) and suggest a safe alternative (e.g. test accounts in a sandbox env).

## Examples

**Example 1**
User: "I'm building a new SaaS, need login and signup. Not technical, just want it secure."
Skill does: recommends Clerk or Supabase Auth over custom, scopes signup/login/logout/reset, session via provider-managed httpOnly cookies, checklist all green since provider handles hashing/rate limiting, scaffolds the provider integration code.
Outcome: founder gets working, secure auth without touching password hashing themselves.

**Example 2**
User: "I already built custom email/password auth with AI help, can you check if it's safe?"
Skill does: runs the existing code against the Step 4 mistake checklist, finds tokens stored in localStorage and no rate limiting on login, flags both with fixes, leaves working parts (bcrypt hashing) alone.
Outcome: two concrete, scoped fixes instead of a full auth rebuild.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- api-endpoint-builder (S3-Building)
- onboarding-flow-builder (S3-Building)
- security-review-lite (S4-Testing)

### Fed By
- data-model-diagrammer (S3-Building)
- architecture-decision-writer (S2-Planning)

### Feedback Loop
When security-review-lite finds an auth gap post-build, feed it back into this skill's mistake checklist so future auth flows catch it up front.

```yaml
chain_metadata:
  skill_slug: "auth-flow-builder"
  stage: "building"
  timestamp: string
  suggested_next:
    - "onboarding-flow-builder"
    - "api-endpoint-builder"
    - "security-review-lite"
```
