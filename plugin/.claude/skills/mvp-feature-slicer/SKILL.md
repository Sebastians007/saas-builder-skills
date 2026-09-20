---
name: mvp-feature-slicer
description: >
  Cuts an overly ambitious feature list down to the smallest version that is still a real,
  testable product — directly targets the most common failure mode of non-technical
  founders scoping too big and never shipping anything.
  Use this skill when the user asks about "what's actually in v1", "help me cut this
  down", or says
  "I keep adding features and never launching", "this feature list is way too big", "what's
  the smallest version of this I could actually ship", "help me cut scope", "I want to
  build everything before launch", "what can wait until after launch", "trim this down to
  an MVP".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "mvp", "scope-cutting", "prioritization"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Planning
---

# MVP Feature Slicer

Takes an already-large or growing feature list and cuts it down to the smallest set that still makes a real, testable product — one a real user could actually use to get the core outcome and that would tell you something true if it flopped. This exists because the single most common way non-technical founders using AI tools fail isn't bad code, it's never shipping because the definition of "v1" kept growing. This skill's job is to say no to more things than it says yes to.

## Stage
This skill belongs to Stage S5: Planning

## When to Use
- Right after a PRD is written, if the Must-Have list still has more than ~8 items
- The user has been building for weeks/months with no launch date because "just one more feature" keeps getting added
- The user explicitly asks what to cut, or seems reluctant to cut anything themselves
- Before `feature-roadmap-architect`, to make sure Phase 1 is actually minimal
- Revisiting a stalled build to find the smallest shippable slice of what already exists

## Input Schema
```
prd_path?: string
feature_list: string[]            # the current (likely too large) feature list
target_launch_window?: string     # e.g. "2 weeks", optional but sharpens the cut
target_user?: string              # pulled from PRD if available
```

## Workflow
### Step 1: Restate the one outcome the MVP must prove
Pull directly from the PRD's problem/outcome statement. The test for every feature in this skill is: does this feature have to exist for the target user to get that ONE outcome and for you to learn whether they actually want it? Nothing else qualifies, no matter how reasonable it sounds.

### Step 2: Run every feature through the cut test
For each feature ask three questions in order:
1. Does the core flow completely fail to deliver the outcome without this? (if no → cut)
2. Could a manual/ugly workaround substitute for this at small scale — you doing it by hand, a spreadsheet, a canned email? (if yes → cut, do manually for now)
3. Is this solving a problem you've actually confirmed the target user has, or one you're guessing they might eventually hit? (if guessing → cut)
Anything that survives all three is a true MVP feature. Be explicit that surviving means "cannot skip," not "would be good to have."

### Step 3: Name the manual workaround for every cut feature
For each cut, state exactly what the founder does by hand instead (e.g., "no automated email receipts — send them manually from your own inbox for the first 20 customers"). This makes the cut feel safe rather than like losing functionality, and it's often literally the founder's plan.

### Step 4: Stress-test the remaining list against real usability
Check that what's left isn't so stripped down it's unusable or embarrassing to show a real user — MVP means minimum, not broken. If a truly essential piece of UX (e.g., any way to log in) got cut by the mechanical rule, add it back and say why it's the exception.

### Step 5: Set a hard cap and justify going over it
Default target: 5-7 features for v1. If the surviving list is longer, force another pass — ask which single feature the founder would keep if they could only ship one, then rebuild outward from there. If the user insists on keeping more after a real pass, that's their call, but state clearly that every feature added is time before they learn anything from real users.

### Step 6: Give a one-sentence "define done" test
State a concrete, observable condition for when the MVP is launchable (e.g., "done = a real stranger can sign up, create one invoice, and get paid, without you helping them"). This becomes the actual finish line instead of a moving target.

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Every kept feature is justified as directly required for the ONE outcome, not "nice to have"
- [ ] Every cut feature has a named manual workaround, not just "later"
- [ ] Final list is 5-7 items unless there's an explicit, stated reason for more
- [ ] The "define done" sentence is a single observable, testable condition
- [ ] Nothing essential for basic usability (login, ability to actually use the core flow) was cut mechanically without being caught in Step 4

## Output Schema
```
{
  "core_outcome": string,
  "mvp_features": string[],
  "cut_features": [ { "feature": string, "reason": string, "manual_workaround": string } ],
  "define_done": string
}
```

## Output Format
```markdown
# MVP Scope: <product name>

**The one outcome this MVP must prove:** <outcome>

## Ship in v1
- <feature> — required because: <reason it survives the cut test>
- ...

## Cut for now
- ~~<feature>~~ — do this manually instead: <workaround> — revisit when: <trigger, e.g. "past 20 users">
- ...

## Define Done
<one sentence, observable, testable finish line>
```

## Error Handling
- If the user resists every proposed cut, name the actual cost plainly (each week spent on non-essential features is a week without real user feedback) and ask them to pick the single feature they'd keep if forced to choose one — rebuild the list from there.
- If no PRD exists to pull the core outcome from, ask for it directly before slicing — without one clear outcome, "cut vs keep" has no test to run against.
- If the existing feature list is already small (5 or fewer), confirm it passes the cut test rather than cutting further for its own sake — don't manufacture cuts.
- If a cut feature turns out to be a hard technical dependency for a kept one (e.g., cutting "user accounts" but keeping "save your data"), catch the contradiction and either restore it or cut the dependent feature too.
- If the user has already spent significant time building the larger list, don't guilt them — reframe the cut as "what ships this week" versus "what's already built and can launch as Phase 2," using `feature-roadmap-architect` next.

## Examples
**Example 1:** User has a PRD for a CRM with 14 must-have features and no launch date after 3 months of building. The skill runs the cut test, keeps 6 (add lead, log a touch, see follow-up due list, basic auth, one pipeline view, manual note field), cuts 8 with named manual workarounds (e.g., no tagging system yet — use a naming convention), and gives the done test: "a real user can add 5 leads and know who to follow up with today without touching a spreadsheet."

**Example 2:** User says "I don't want to cut anything, all of these matter." The skill asks which single feature they'd keep if forced to pick one, uses that answer to rebuild the list outward, and shows the founder the actual time cost of the full list versus the trimmed one.

**Example 3:** User has a stalled 6-month build with a lot of code already written. The skill treats this as "what's the smallest already-built slice that's launchable this week," identifies which existing features form one complete flow, and defers the rest to a Phase 2 roadmap rather than cutting code that already exists.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-roadmap-architect` (S5-Planning) — the MVP list becomes Phase 1; cut features become later phases
- `feature-task-breakdown` (S6-Building) — MVP features get broken into buildable tasks next
- `user-acceptance-test-planner` (S7-Testing) — the "define done" sentence becomes the acceptance test for launch readiness

### Fed By
- `prd-writer` (S5-Planning) — supplies the full feature list and core outcome this skill slices down
- `defensibility-calculator` (S5-Planning) — flags which feature is the actual moat, so it doesn't get cut by mistake

### Feedback Loop
After launch, if `signup-conversion-tracker` or early user feedback shows a cut feature was actually essential, feed that back into future MVP scoping — the cut test should get sharper about what "core" really means for this specific product category over time.

```yaml
chain_metadata:
  skill_slug: "mvp-feature-slicer"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-roadmap-architect"
    - "feature-task-breakdown"
    - "user-acceptance-test-planner"
```
