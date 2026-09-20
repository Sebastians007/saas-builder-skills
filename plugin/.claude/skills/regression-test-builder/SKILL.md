---
name: regression-test-builder
description: >
  Turns a bug that was just fixed into a permanent test or checklist step so
  the exact same bug cannot silently come back in a future change.
  Use this skill when the user asks about "write a test for this bug fix",
  "make sure this doesn't break again", "how do I stop this from
  regressing", "add a regression test", "this bug came back, again", "I
  fixed this once already", or "lock this fix in".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "regression", "bug-fixing"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Testing
---

# Regression Test Builder

Takes a bug that just got fixed and converts it into a repeatable test or manual checklist step, so the fix is permanent instead of temporary. Bugs that come back are a trust killer with users — this skill exists so "we fixed that already" stays true.

## Stage
This skill belongs to Stage S7: Testing

## When to Use
- Immediately after fixing any bug that a real user hit or that was found in testing
- When the same bug has been fixed more than once (a clear signal nothing is locking it in)
- Before merging a bugfix, to attach proof it's covered
- When browser-verifier finds a bug during a verification pass
- When cleaning up before a launch, to make sure past fixes are actually locked in, not just "seemed to work at the time"

## Input Schema
```
bug_description: string       # what broke, in plain language
how_it_was_found: string      # user report, manual test, error log, etc.
root_cause: string (optional) # why it happened, if known
fix_summary: string (optional)
has_automated_tests: boolean (optional)  # does this app have a test suite at all?
```

## Workflow
### Step 1: Pin down the exact broken behavior
State precisely what was wrong: not "signup was broken" but "signup allowed duplicate emails because the uniqueness check ran client-side only." Vague bug descriptions produce regression tests that don't actually catch the regression.

### Step 2: Identify the trigger condition
What specific input, sequence, or state caused it? This becomes the exact reproduction steps for the test.

### Step 3: Write the regression test
If the app has an automated test suite: write the actual test (unit, integration, or e2e depending on where the bug lived) that fails on the old broken code and passes on the fix.
If the app has no automated test suite yet (common for early-stage solo builders): write a manual checklist step with exact reproduction steps and expected result, tagged clearly as "manual — run before every deploy that touches [area]."

### Step 4: Attach it to the right layer
Decide where this regression check belongs: a unit test near the function, an integration test on the API route, or a browser-verifier step on the user-facing flow. Bugs in validation logic get unit tests; bugs in user flow get browser-verifier steps.

### Step 5: Name it so future-you understands why it exists
Test/checklist names should reference the bug, not just the feature: "signup rejects duplicate email (regression: allowed dupes before 2026-09)" not "signup test 4."

### Step 6: Self-Validation
- [ ] The test reproduces the exact original trigger condition, not a generic version of the feature
- [ ] The test would have failed on the old, broken code (mentally verify this)
- [ ] The test/checklist step is placed somewhere it will actually get run again (test suite, or a standing pre-deploy checklist file)
- [ ] Naming makes it clear this exists because of a specific past bug

## Output Schema
```
{
  bug_id: string,
  original_bug: string,
  trigger_condition: string,
  test_type: "automated_unit" | "automated_integration" | "automated_e2e" | "manual_checklist",
  test_code_or_steps: string,
  where_it_lives: string,     // file path or "pre-deploy checklist"
  expected_result: string
}
```

## Output Format
```markdown
# Regression Test: [short bug name]

## What broke
[precise description]

## What triggered it
[exact steps/conditions]

## The regression check
Type: [automated / manual]
Location: [file path or checklist name]

\`\`\`
[test code, or numbered manual steps]
\`\`\`

Expected result: [what "still fixed" looks like]

## Add to standing checklist?
[yes/no — if yes, note it should go in the pre-deploy checklist for this app]
```

## Error Handling
- Root cause unknown, only symptom is known → write the test against the observable symptom (what the user saw) rather than blocking on root-cause analysis; note that root cause should still be investigated
- No test suite exists at all → default to a manual checklist step and say plainly that automated coverage isn't there yet; don't invent a test framework that isn't installed
- Bug was a one-time data issue, not a code bug → say so, and skip writing a regression test; suggest a data-integrity check instead if relevant
- Bug fix wasn't verified as actually fixed → flag this first; a regression test for an unconfirmed fix is worthless, hand off to browser-verifier before writing the test

## Examples
1. User: "I fixed the bug where the free trial didn't expire, write a test for it" → Skill writes an automated test setting a trial's end date in the past and asserting the account loses access, named to reference the original bug. Outcome: future changes to billing logic can't silently un-fix this.
2. User: "this duplicate email bug came back a second time" → Skill flags this as a repeat regression, checks why the first fix didn't stick (likely: no test was ever written), and this time places the check directly in the signup test file plus a note in the pre-deploy checklist.
3. User pastes a bug report with no test suite in the project → Skill produces a manual pre-deploy checklist step with exact repro steps instead of pretending an automated framework exists.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- browser-verifier (S7-Testing)
- ci-cd-pipeline-builder (S8-Deployment)
- incident-runbook-writer (S9-Operations)

### Fed By
- browser-verifier (S7-Testing)
- tech-debt-detector (S5-Planning)

### Feedback Loop
Track which regression tests fail repeatedly over time — a fix that keeps needing a new regression test signals the underlying code needs refactoring, not just more tests.

```yaml
chain_metadata:
  skill_slug: "regression-test-builder"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "browser-verifier"
    - "ci-cd-pipeline-builder"
```
