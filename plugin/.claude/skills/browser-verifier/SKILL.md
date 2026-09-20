---
name: browser-verifier
description: >
  Actually launches the running app in a real browser using the
  superpowers-chrome plugin (Chrome DevTools browser control) and clicks
  through the golden path plus edge cases before anyone is allowed to call a
  feature "done" — the antidote to claiming success without checking.
  Use this skill when the user asks about "is this actually working",
  "check this in the browser", "verify this feature works", "did that
  actually deploy correctly", "click through this and tell me if it
  works", "I think this is done, can you confirm", "test this live", or
  "don't just tell me it works, show me".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "browser-automation", "verification"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Testing
---

# Browser Verifier

This is the single most important skill in this pack. It exists because "the code compiles" and "it works" are different claims, and only one of them matters to a paying user. This skill opens the actual running app in a real Chrome browser, using the **superpowers-chrome** plugin (Claude Code's Chrome DevTools browser control), and clicks through it exactly like a human would — golden path first, then the edge cases from test-case-generator or edge-case-hunter. Nothing gets marked "done" on the strength of reading the code. It gets marked done because it was watched working.

## Stage
This skill belongs to Stage S4: Testing

## When to Use
- Before saying any feature, bug fix, or deploy is "done" — no exceptions
- After every deploy to a live URL (Cloudflare Pages/Workers preview or production)
- After merging a fix that regression-test-builder just wrote a check for
- When the founder has been burned before by features that looked done but weren't (this is the default assumption for this user — always verify)
- Any time test-case-generator or edge-case-hunter produced a list of cases — this skill is how those cases actually get run, not just written down
- Before telling the user "you're good to launch"

## Input Schema
```
app_url: string                    # the actual running URL — localhost or live
feature_or_flow: string            # what to verify
test_cases: [string] (optional)    # from test-case-generator / edge-case-hunter, if available
credentials: object (optional)     # test account login, only if needed and provided by user
critical: boolean (optional)       # true for anything touching money/auth/data
```

## Workflow
### Step 0: Confirm the superpowers-chrome plugin is available
This skill assumes the `superpowers-chrome` plugin is installed and its Chrome DevTools browser tools are loaded (via ToolSearch if deferred, as `mcp__claude-in-chrome__*` tools, or the equivalent Chrome DevTools MCP tools exposed by superpowers-chrome in this environment). If they are not available, stop and tell the user plainly: "I can't verify this in a real browser without superpowers-chrome connected — here's what to check by hand instead," then fall back to a manual click-through checklist. Never silently skip verification and report success anyway.

### Step 1: Open the real, running app
Navigate to the actual `app_url` — not a description of it, not a code read-through. If it's a local dev server, confirm it's actually running first (check the port responds) rather than assuming.

### Step 2: Walk the golden path exactly as a user would
Click the real buttons, type into the real fields, submit the real forms. Take a screenshot or read the page state after each meaningful step. Do not assume a click worked — check the resulting page state, not just that the click command didn't error.

### Step 3: Check for silent failures
Read the browser console for JavaScript errors. Read network requests for failed (4xx/5xx) calls that the UI might be swallowing silently. A feature that "looks fine" with a red console error or a failed API call underneath is not fine — flag it.

### Step 4: Run the edge cases
Work through the test cases supplied (or generate a minimal set on the spot if none were given: empty form submit, invalid input, logged-out access). Actually perform each one in the browser — don't reason about what "should" happen.

### Step 5: Verify the actual outcome, not just the absence of a crash
For each case, check the real result against the expected result: did the database actually get the record, did the email actually get sent (or at least did the API call succeed), did the redirect actually land on the right page, does a refresh preserve the change. "The page didn't crash" is not the same as "it worked."

### Step 6: Report exactly what was seen
State plainly what passed and what failed, with the specific evidence (screenshot description, console error text, network status code). Never write "should work" or "looks good" — only write what was directly observed.

### Step 7: Self-Validation
- [ ] The app was actually opened in a real browser via superpowers-chrome, not reasoned about from source code
- [ ] Every claimed-passing case has direct observed evidence (screenshot, page text, network status), not an inference
- [ ] Console and network were checked, not just visual appearance
- [ ] At least one failure/edge case was actually attempted in the browser, not just the happy path
- [ ] If superpowers-chrome wasn't available, this is stated explicitly rather than papered over
- [ ] Nothing is reported as "done" that wasn't actually clicked through

## Output Schema
```
{
  app_url: string,
  feature_or_flow: string,
  verification_method: "live_browser" | "manual_fallback_no_browser_tool",
  results: [
    {
      case: string,
      status: "pass" | "fail" | "blocked",
      evidence: string,          // what was actually observed
      console_errors: [string],
      network_issues: [string]
    }
  ],
  overall_verdict: "verified_working" | "verified_broken" | "not_verifiable"
}
```

## Output Format
```markdown
# Browser Verification: [Feature/Flow Name]

App checked: [URL]
Method: Live browser via superpowers-chrome

## Golden Path
Status: PASS / FAIL
Evidence: [what was actually seen]

## Edge Cases
| Case | Status | Evidence |
|------|--------|----------|
| ... | PASS/FAIL | ... |

## Console/Network Issues Found
- ...

## Verdict
[VERIFIED WORKING / VERIFIED BROKEN — do not ship / COULD NOT VERIFY — here's why]
```

## Error Handling
- superpowers-chrome / Chrome DevTools tools not available or fail to connect → say so directly, do not fall back to reading code and calling it verified; offer a manual step-by-step checklist for the human to run instead
- App isn't running / URL unreachable → report this as a blocking finding, not a skipped step; nothing can be verified until the app is actually up
- A click or navigation doesn't produce the expected page → treat this as a failed case, investigate console/network before concluding, and report the real error
- Credentials needed but not provided → ask the user for a test account, or use a public/no-auth flow if one exists; don't fabricate a login
- Feature appears to work visually but a network call underneath returned an error → report as FAIL; visual success does not override a failed request
- Time pressure to skip edge cases → still run at least the golden path and one failure case; a verification with zero edge cases checked should say so explicitly, not imply full coverage

## Examples
1. User: "I finished the signup form, is it done?" → Skill loads Chrome DevTools tools, navigates to the live dev URL, fills the form, submits, confirms a new user record appears (via a check in the UI, e.g. redirect to dashboard with the right email shown), checks console for errors. Outcome: catches that the confirmation email step silently 500'd even though the UI showed "success."
2. User: "did the Cloudflare deploy work" → Skill opens the live production URL directly (not localhost), clicks through the core flow, confirms it matches what was expected. Outcome: catches a stale cache serving the old version even though the deploy log said success.
3. User asks for verification but superpowers-chrome isn't connected → Skill states this plainly, does not claim to have verified anything, and hands over a manual checklist instead.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- regression-test-builder (S4-Testing)
- user-acceptance-test-planner (S4-Testing)
- incident-runbook-writer (S6-Operations)

### Fed By
- test-case-generator (S4-Testing)
- edge-case-hunter (S4-Testing)
- cloudflare-deployer (S5-Deployment)

### Feedback Loop
Every FAIL found here should generate a regression-test-builder entry so the same failure has a permanent check, and every category of bug found repeatedly should get added as a default case in test-case-generator.

```yaml
chain_metadata:
  skill_slug: "browser-verifier"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "regression-test-builder"
    - "user-acceptance-test-planner"
```
