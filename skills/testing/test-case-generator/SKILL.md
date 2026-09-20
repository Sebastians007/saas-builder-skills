---
name: test-case-generator
description: >
  Turns a feature description or user story into a concrete, numbered list of
  test cases covering the happy path and the obvious edge cases, before or
  right after the feature is built.
  Use this skill when the user asks about "how do I test this feature",
  "what should I check before shipping this", "write test cases for
  signup", "what could go wrong with this form", "give me a checklist for
  this feature", "what am I missing before I call this done", or
  "test plan for the checkout flow".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "qa", "test-planning"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Testing
---

# Test Case Generator

Produces a specific, numbered list of test cases for one feature: what a normal user does, what a confused user does, and what breaks it. The output is a checklist someone can actually run by hand or hand to browser-verifier to execute — not a vague "test it thoroughly" note.

## Stage
This skill belongs to Stage S4: Testing

## When to Use
- Right after writing a user story or PRD section for a feature, before code is written
- Right after a feature is built, before it's marked done
- When the founder says "I think this is done" and needs a gut check
- Before handing a feature to browser-verifier for real-browser execution
- When scoping what a bug fix needs to cover so it doesn't regress
- When a feature touches money, auth, or user data and needs extra scrutiny

## Input Schema
```
feature: string                 # short name, e.g. "password reset"
description: string             # what it's supposed to do, in plain language
user_story: string (optional)   # "As a X, I want Y, so that Z"
inputs: [string] (optional)     # form fields, params, uploads involved
tech_context: string (optional) # framework/stack, only if it changes what can break
risk_level: enum (optional)     # low | medium | high (money, auth, data-loss = high)
```

## Workflow
### Step 1: Restate the feature in one sentence
Confirm (in the output, not as a question back to the user unless truly ambiguous) what the feature is supposed to do. If the description is too vague to generate real test cases, make a reasonable assumption and state it rather than blocking.

### Step 2: List the happy path
Write the single, most common, everything-goes-right sequence of steps a real user takes. This is test case #1. Every other test case is a variation or a break of this path.

### Step 3: Generate input-variation cases
For every input field, param, or upload: empty, too long, too short, wrong type, special characters, duplicate submission, already-taken value (e.g. existing email), whitespace-only, copy-pasted with hidden characters.

### Step 4: Generate state and flow cases
Cases based on where the user is when they hit the feature: not logged in, logged in as wrong role, session expired mid-action, double-click / double-submit, back button after submit, refresh mid-action, feature triggered twice concurrently.

### Step 5: Generate failure and boundary cases
Network drops mid-request, server returns an error, third-party API (Stripe, email, etc.) is down, rate limit hit, very first user ever (empty database), very large dataset, zero results.

### Step 6: Tag by risk and priority
Mark each test case P0 (must pass before ship), P1 (should pass), or P2 (nice to check). Anything touching money, auth, or destructive actions is P0 by default.

### Step 7: Self-Validation
- [ ] Happy path is test case #1 and is unambiguous
- [ ] At least 3 input-variation cases per user-facing field
- [ ] At least 2 state/flow cases (not logged in, session/expiry)
- [ ] At least 2 failure cases (network/API failure, empty state)
- [ ] Every P0 case is something that would actually embarrass the founder if it broke in front of a user
- [ ] No case is vague ("test it works") — each one names the exact input and exact expected result

## Output Schema
```
{
  feature: string,
  happy_path: { steps: [string], expected_result: string },
  test_cases: [
    {
      id: string,           // TC-01, TC-02...
      category: "input" | "state" | "failure" | "boundary",
      priority: "P0" | "P1" | "P2",
      steps: [string],
      expected_result: string
    }
  ],
  open_questions: [string]  // only if input was genuinely ambiguous
}
```

## Output Format
```markdown
# Test Cases: [Feature Name]

## What it's supposed to do
[one sentence]

## Happy Path (TC-01)
Steps: ...
Expected: ...

## Test Cases

| ID | Priority | Category | Steps | Expected Result |
|----|----------|----------|-------|------------------|
| TC-02 | P0 | input | ... | ... |
| TC-03 | P1 | state | ... | ... |

## P0 count: X | P1 count: X | P2 count: X

## Open Questions (if any)
- ...
```

## Error Handling
- Feature description too vague to test → state the assumption made and proceed; flag it in Open Questions instead of stopping
- No inputs/fields given → infer likely fields from the feature name (e.g. "signup" implies email, password) and label them as assumed
- Risk level not given → infer from feature type (payments/auth/data-deletion = high) and say so
- User asks for test cases on something that isn't built yet → still generate them; note this is a pre-build test plan, useful as acceptance criteria
- Feature is trivial (e.g. static text change) → say so plainly and give a short 2-3 case list instead of padding to look thorough

## Examples
1. User: "write test cases for the password reset flow" → Skill outputs happy path (request reset, click email link, set new password, log in) plus cases: expired link, reused link, wrong email, email that doesn't exist (no user enumeration), password too weak, two reset requests in a row. Outcome: a P0-tagged checklist ready for browser-verifier.
2. User: "what should I check before shipping the Stripe checkout button" → Skill flags this as high-risk, generates cases for card declined, webhook not received, double-click double-charge, browser closed after payment before redirect. Outcome: founder sees double-charge risk before it happens to a real customer.
3. User: "is this login form done" (pastes vague description) → Skill assumes standard email/password login, states the assumption, generates cases including wrong password, locked account, SQL-injection-style input, case-sensitivity of email.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- browser-verifier (S4-Testing)
- edge-case-hunter (S4-Testing)
- user-acceptance-test-planner (S4-Testing)
- regression-test-builder (S4-Testing)

### Fed By
- user-story-writer (S2-Planning)
- feature-task-breakdown (S3-Building)

### Feedback Loop
When browser-verifier finds a bug a generated test case missed, feed that gap back so future test-case-generator runs on similar features include that category by default.

```yaml
chain_metadata:
  skill_slug: "test-case-generator"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "browser-verifier"
    - "edge-case-hunter"
```
