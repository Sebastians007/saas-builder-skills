---
name: security-review-lite
description: >
  Runs a lightweight, pre-ship security pass for a small SaaS app — auth
  issues, exposed secrets, injection risks, and missing input validation —
  a sane baseline check, not a full penetration test.
  Use this skill when the user asks about "is this safe to ship",
  "check for security issues", "did I leak an API key", "is this
  vulnerable to SQL injection", "can someone hack this before I launch",
  "security check before going live", "am I exposing anything I
  shouldn't", or "review this for security holes".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "security", "pre-launch"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Testing
---

# Security Review Lite

A baseline security pass sized for a small SaaS shipped by a non-technical or solo founder using AI-assisted coding — the kind of app most likely to have a hardcoded API key, an unauthenticated admin route, or a form with zero input validation because nobody thought to check. This is not a penetration test and doesn't replace one before handling sensitive data at scale, but it catches the mistakes that actually happen in this workflow.

## Stage
This skill belongs to Stage S7: Testing

## When to Use
- Before any first launch or any deploy to a public URL
- Before pushing code to a public GitHub repo
- After adding any new form, API endpoint, or file upload
- After adding any third-party integration (payments, email, storage) that needs credentials
- Any time a founder says "this handles [money / user data / passwords]" — always run this before launch for those

## Input Schema
```
target: string                   # repo path, file, or live URL
handles_payments: boolean (optional)
handles_pii: boolean (optional)   # emails, names, addresses, anything personal
repo_is_public: boolean (optional)
backend: string (optional)        # Cloudflare Workers, Node, etc.
```

## Workflow
### Step 1: Scan for exposed secrets
Search the codebase (and git history if the repo is public or about to be) for API keys, database URLs, passwords, and tokens committed directly in source rather than loaded from environment variables/secrets storage. This is the single most common and most damaging mistake in AI-assisted app building — flag it as P0 immediately if found, and note that a leaked key needs to be rotated, not just deleted from the file.

### Step 2: Check authentication and authorization
Confirm every route that should require login actually checks for a valid session/token server-side (not just hides a button in the UI — a hidden button is not security). Confirm every route that should be scoped to "only this user's data" actually filters by the logged-in user's ID server-side, not just trusts an ID passed from the client (this is the most common real-world SaaS vulnerability: user A can view user B's data by changing a number in the URL).

### Step 3: Check input validation and injection risk
Look for any place user input reaches a database query, a file path, a shell command, or gets rendered back into HTML without escaping. Flag string-concatenated SQL, unsanitized file paths from user input, and any `dangerouslySetInnerHTML`/raw HTML insertion of user-provided text (XSS risk).

### Step 4: Check secrets and config for the deploy environment
Confirm environment variables/secrets are set in the actual hosting platform (e.g. Cloudflare's secret store) rather than only in a local `.env` that might get committed. Confirm `.env` and similar files are in `.gitignore`.

### Step 5: Check rate limiting and abuse surface on sensitive endpoints
Login, signup, password reset, and any endpoint that costs money per call (AI generation, email sending) should have some basic rate limiting or abuse protection — flag if completely open, even if a full solution isn't built yet.

### Step 6: Check third-party integration exposure
For payments (Stripe etc.), confirm webhook signatures are verified server-side, not trusted blindly. For any client-side API key, confirm it's actually meant to be public (e.g. a publishable key) and not a secret key exposed to the browser.

### Step 7: Self-Validation
- [ ] Explicitly checked for secrets in source and git history, not just current files
- [ ] Explicitly checked that data access is scoped server-side by logged-in user, not just client-side hidden
- [ ] Findings are marked P0 (exploit-ready, fix before shipping) vs P1 (should fix soon) vs P2 (hardening)
- [ ] This is stated clearly as a baseline pass, not a substitute for a real pentest if the app will handle serious money or sensitive data at scale
- [ ] Every P0 finding includes the specific fix, not just "this is insecure"

## Output Schema
```
{
  target: string,
  findings: [
    {
      id: string,
      category: "secrets" | "auth" | "injection" | "config" | "rate_limiting" | "third_party",
      priority: "P0" | "P1" | "P2",
      location: string,
      issue: string,
      fix: string
    }
  ],
  scope_note: string
}
```

## Output Format
```markdown
# Security Review (Lite): [Target]

Scope: baseline pre-ship check, not a full penetration test.

## P0 — Fix before shipping
- [location]: [issue] → Fix: [specific fix]

## P1 — Fix soon
- ...

## P2 — Hardening
- ...

## Summary
X P0, X P1, X P2. [One sentence on overall risk level for this specific app.]
```

## Error Handling
- Can't access the repo/code directly → work from what's described or pasted, and state clearly this is a partial review limited to what was shared
- Secret found in a public repo's history → flag as most urgent possible finding; explain that deleting the file isn't enough, the key must be rotated at the provider and history should be scrubbed or the repo made private
- App is pre-revenue/internal-only with no real user data yet → still run the check but note actual urgency is lower; don't manufacture panic over a tool nobody but the founder uses yet
- User wants a guarantee of "unhackable" → explicitly say that doesn't exist; this pass reduces the most common and most damaging mistakes, it isn't a certification
- Backend/stack unclear → ask or infer from context (e.g. package.json, wrangler.toml) rather than giving generic advice that doesn't apply to the actual stack

## Examples
1. User: "is this safe to push to GitHub" → Skill scans for a hardcoded Stripe secret key found in a committed config file. Outcome: key gets pulled into an environment variable and rotated before the repo goes public.
2. User: "check this API route" (fetches a user's invoice by ID) → Skill finds the route trusts the `userId` in the request body instead of the authenticated session, meaning any logged-in user can view any other user's invoice by changing a number. Outcome: route fixed to use the session's user ID server-side.
3. User: "security check before launch" on a small internal tool with no real customer data → Skill runs the checklist, finds nothing P0, notes overall risk is low given the tool's limited audience, and lists a couple of P2 hardening items for later.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- env-secrets-manager (S8-Deployment)
- compliance-checker (S11-Meta)
- browser-verifier (S7-Testing)

### Fed By
- auth-flow-builder (S6-Building)
- edge-case-hunter (S7-Testing)

### Feedback Loop
Every P0 found should be fed back into auth-flow-builder and api-endpoint-builder's default patterns so future-built endpoints don't repeat the same class of mistake.

```yaml
chain_metadata:
  skill_slug: "security-review-lite"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "env-secrets-manager"
    - "browser-verifier"
```
