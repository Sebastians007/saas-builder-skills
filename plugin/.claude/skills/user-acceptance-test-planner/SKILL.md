---
name: user-acceptance-test-planner
description: >
  Plans a short real-user (or founder-as-user) acceptance test pass before a
  feature or app gets called launch-ready — the final human-eyes check after
  automated and technical verification.
  Use this skill when the user asks about "is this ready to launch",
  "get someone to try this before I ship", "plan a final test before
  launch", "who should test this before real users see it", "acceptance
  test before going live", "final check before launch day", or "have I
  actually confirmed this works for a real person".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "uat", "launch-readiness"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Testing
---

# User Acceptance Test Planner

Plans the last checkpoint before calling something launch-ready: a short, structured pass where a real person (a tester, a friendly prospect, or the founder deliberately acting like a first-time user) uses the actual feature to accomplish an actual goal, with no hand-holding. This catches what browser-verifier's scripted clicks and test-case-generator's checklists can miss — confusion, friction, and "technically works but nobody would actually do this."

## Stage
This skill belongs to Stage S4: Testing

## When to Use
- Before calling any feature or app "launch-ready," as the final step after test-case-generator, browser-verifier, and security-review-lite have already run
- Before a launch day, demo, or first cold-outreach batch that will drive real people to the app
- When automated/scripted checks all pass but the founder still isn't confident it's actually good
- When onboarding a new feature that changes a core user flow (signup, checkout, core action)
- Not needed for tiny internal-only changes with no user-facing surface

## Input Schema
```
feature_or_app: string
target_user_profile: string        # who the real user is, in plain terms
prior_verification_done: [string] (optional)  # e.g. ["browser-verifier", "security-review-lite"]
tester_available: string (optional) # "founder only" | "friendly prospect" | "real customer"
launch_deadline: string (optional)
```

## Workflow
### Step 1: Confirm the technical checks already ran
Acceptance testing is the last step, not a replacement for the earlier ones. Check what's already been verified (browser-verifier for functional correctness, security-review-lite for safety, accessibility-auditor if user-facing). If none of those ran yet, say so and recommend running them first — UAT on a technically broken feature wastes the tester's time.

### Step 2: Define the single real goal the tester must accomplish
Not "click around and see what you think" — a specific outcome: "sign up, connect your email, and send your first campaign" or "upload a document and get a summary back." Vague UAT produces vague feedback.

### Step 3: Pick the tester and the honesty condition
Best: a real prospect from the target audience, with zero hints or hand-holding. Second best: the founder, deliberately playing dumb — using the app exactly as instructed with no prior knowledge, on a fresh account, without fixing anything mid-test. Never: the founder testing while mentally filling in gaps they know about ("oh I know that button does X" defeats the purpose).

### Step 4: Set the observation method
Decide how friction gets captured: watch over their shoulder / screen-share and note every pause, confused click, or "wait, what does this do," or have the tester think out loud and record it. Silence and "seems fine" from a tester is not useful data — the plan must force out where they hesitated.

### Step 5: Define pass/fail and what "acceptance" means
The feature passes acceptance if the tester reaches the goal without being told what to do next, in a reasonable time, and doesn't hit an error requiring the founder to intervene. Any of those failing means it's not launch-ready yet, regardless of what the automated checks said.

### Step 6: Capture findings as fix-or-ignore decisions
For every friction point or failure, the founder decides: fix before launch, fix after launch, or accept as-is. Don't let this turn into an open-ended redesign — timebox it to the launch deadline.

### Step 7: Self-Validation
- [ ] Prior technical verification (browser-verifier, security-review-lite) is checked as a prerequisite, not skipped
- [ ] The tester's goal is one specific, concrete action, not vague exploration
- [ ] The tester profile is not "someone who already knows how the app works"
- [ ] Every observed friction point is written down even if minor, then explicitly triaged (fix now / later / accept)
- [ ] The plan states a clear go/no-go criterion, not just "gather feedback"

## Output Schema
```
{
  feature_or_app: string,
  prerequisites_confirmed: [string],
  test_goal: string,
  tester_profile: string,
  observation_method: string,
  findings: [
    {
      moment: string,          // where in the flow it happened
      observation: string,     // what the tester did/said
      severity: "blocker" | "friction" | "minor",
      decision: "fix_before_launch" | "fix_after_launch" | "accept"
    }
  ],
  verdict: "launch_ready" | "not_yet" | "launch_ready_with_known_gaps"
}
```

## Output Format
```markdown
# UAT Plan: [Feature/App]

Prerequisites confirmed: [list, or "none yet — run these first"]

## Test Goal
[the one thing the tester must accomplish]

## Tester
[who, and why they're the right profile]

## How to Observe
[method]

## Findings (fill in after the test runs)
| Moment | Observation | Severity | Decision |
|--------|-------------|----------|----------|
| ... | ... | ... | ... |

## Verdict
[launch ready / not yet — with reason]
```

## Error Handling
- No real prospect available to test → use the founder in strict "pretend you know nothing" mode, and flag this as a weaker signal than a real outside tester; recommend getting a real tester before a big launch push if possible
- Prior verification steps skipped → recommend running browser-verifier and security-review-lite first; UAT is not a substitute for functional or security checks
- Tester reports "seems fine" with no detail → the plan should have forced a think-aloud or screen-share; treat silent approval as insufficient data, not a pass
- Launch deadline is very tight → timebox to a single 15-30 minute test on the one critical flow rather than skipping UAT entirely
- Findings reveal a fundamental confusion, not a small friction point → flag as a possible go-back-to-design issue, not just a test finding to patch over

## Examples
1. User: "is the onboarding flow launch-ready" → Skill confirms browser-verifier already ran, defines the goal as "sign up and reach the dashboard with your first project created," recruits a friendly prospect, watches them hesitate for 30 seconds on an unlabeled button. Outcome: button gets a label before launch, three other minor items get logged as fix-after-launch.
2. User: "I want to test this myself before showing anyone" → Skill instructs the founder to use a completely fresh incognito session, a fresh test account, and not skip any step even if they know a shortcut. Outcome: founder discovers the "forgot password" link is broken, something they'd never have hit by testing with saved credentials.
3. User: "launch is tomorrow, no time for a full test" → Skill timeboxes to one 15-minute test of the single most critical flow (e.g. checkout) with the founder as tester, explicitly notes this is a reduced-confidence pass, and flags what's not covered.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- onboarding-flow-builder (S3-Building)
- cloudflare-deployer (S5-Deployment)
- signup-conversion-tracker (S7-Growth)

### Fed By
- browser-verifier (S4-Testing)
- security-review-lite (S4-Testing)
- accessibility-auditor (S4-Testing)

### Feedback Loop
Friction points marked "fix after launch" should be tracked and revisited against real signup-conversion-tracker data to confirm whether they actually mattered.

```yaml
chain_metadata:
  skill_slug: "user-acceptance-test-planner"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "cloudflare-deployer"
    - "signup-conversion-tracker"
```
