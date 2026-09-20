---
name: user-story-writer
description: >
  Converts PRD features and user flows into concrete user stories with specific, testable
  acceptance criteria that a developer or an AI coding agent can build against with no
  ambiguity left to fill in on its own.
  Use this skill when the user asks about "turn this into stories", "what should I tell
  Claude to build exactly", or says
  "write user stories for this feature", "break this PRD into buildable pieces", "the AI
  built something different than what I meant", "give me acceptance criteria for this",
  "I need to hand this off to a developer", "make this specific enough to build without
  guessing".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "user-stories", "acceptance-criteria", "spec"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S5-Planning
---

# User Story Writer

Turns a PRD's features and core user flows into individual user stories, each with acceptance criteria specific enough that a developer — or an AI coding agent — has no ambiguous gaps left to improvise on. This is the layer that stops "build the invoicing feature" from becoming five different guesses about what "done" means. Every acceptance criterion here should be something you can literally check off by testing it.

## Stage
This skill belongs to Stage S5: Planning

## When to Use
- Right after a PRD is finalized and it's time to make features buildable
- An AI coding tool built something different than what the user meant, and the root cause was an underspecified instruction
- Before `feature-task-breakdown` or any Stage S3 building skill — stories are the direct input to task breakdown
- A single feature needs to be handed to a developer (human or AI) with no follow-up questions needed
- The user has a feature list but flows and edge cases were never written down
- Before `test-case-generator` — acceptance criteria are what test cases get written against

## Input Schema
```
prd_path?: string                 # source PRD with must-have features and core flows
feature_name?: string             # narrow to one feature if not doing the whole PRD
persona?: string                  # target user, pulled from PRD if not given
```

## Workflow
### Step 1: Pull the feature and its flow from the PRD
For each Must-Have feature, find which core user flow it belongs to. A feature with no flow attached is a sign the PRD itself was underspecified — flag it and ask for the missing context rather than inventing one.

### Step 2: Write the story in standard form, but make the "so that" real
Use "As a [specific persona], I want to [action], so that [concrete outcome]." The "so that" clause must be a real outcome from the PRD's problem/outcome statement, not a restated action ("so that I can invoice clients" is weak; "so that I stop losing track of who owes me money" ties back to the actual pain).

### Step 3: Write acceptance criteria as testable Given/When/Then statements
Each criterion must be checkable by a specific action producing a specific result — no "works correctly," no "handles errors appropriately." Bad: "the form validates input." Good: "Given an invoice amount field left blank, when the user clicks Send, then the form shows 'Amount is required' and does not submit." Cover the happy path first, then the 2-4 most important edge/error cases per story — do not try to enumerate every possible edge case here (that's `edge-case-hunter`'s job in Testing).

### Step 4: Size each story to one sitting of work
If a story needs more than roughly a day of focused build time (or clearly bundles two unrelated behaviors), split it. A story like "user can manage invoices" is not a story — split into create, send, mark paid, view overdue.

### Step 5: Note explicit non-goals per story where it prevents scope creep
If a story is likely to invite extra scope (e.g., "send invoice" tempting someone to add scheduling/reminders), add a one-line "Not included:" note so the AI building it doesn't wander.

### Step 6: Order stories by the flow sequence
Present stories in the order a user would actually hit them in the core flow, not alphabetically or randomly — this ordering becomes useful input for `feature-roadmap-architect`.

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Every story ties to a real PRD feature and flow, not an invented one
- [ ] Every acceptance criterion is a specific, checkable Given/When/Then, not a vague adjective
- [ ] Every story covers at least the happy path plus meaningful error/edge cases
- [ ] No story bundles more than one distinct piece of buildable behavior
- [ ] Stories that could invite scope creep have an explicit "Not included" note

## Output Schema
```
{
  "feature": string,
  "stories": [
    {
      "id": string,
      "title": string,
      "as_a": string,
      "i_want": string,
      "so_that": string,
      "acceptance_criteria": [ { "given": string, "when": string, "then": string } ],
      "not_included": string[]
    }
  ]
}
```

## Output Format
```markdown
# User Stories: <feature/PRD name>

## Story <ID>: <short title>
**As a** <persona>, **I want to** <action>, **so that** <outcome tied to PRD problem>.

**Acceptance Criteria:**
- Given <condition>, when <action>, then <result>
- Given <condition>, when <action>, then <result>
- Given <error condition>, when <action>, then <result>

**Not included:** <scope boundary, if relevant>

---

## Story <ID>: <next story>
...
```

## Error Handling
- If a feature in the PRD has no clear user flow attached, stop and ask for the missing flow rather than guessing the steps.
- If the user asks for stories with no PRD at all, produce them from a quick feature description but flag that skipping the PRD risks inconsistent scope — recommend `prd-writer` first for anything beyond a single small feature.
- If a "story" is really an entire feature area (e.g., "billing"), split it into a set of stories rather than writing one giant one.
- If acceptance criteria would require a decision not yet made (e.g., what happens on payment failure, and no policy exists), list it as an open question rather than inventing behavior.
- If the persona is unclear, pull it from the PRD's target user section; if no PRD exists, ask once rather than defaulting silently.

## Examples
**Example 1:** User has a PRD for an invoicing app and asks for stories on the "send invoice" flow. The skill writes 3 stories — create invoice, send invoice, view send confirmation — each with 3-4 Given/When/Then criteria covering happy path plus missing-field and failed-send cases, and notes "Not included: payment reminders, recurring invoices."

**Example 2:** User says "the AI built login wrong, it didn't have a forgot-password flow." The skill writes a dedicated story for password reset with acceptance criteria covering the request, email/token, and expiry cases, so the gap can't recur.

**Example 3:** User pastes a rough feature list with no PRD and asks for stories directly. The skill writes stories for the clearest 2-3 features, flags that the rest are too vague to write testable criteria for yet, and recommends running `prd-writer` first for those.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `feature-task-breakdown` (S6-Building) — stories become concrete build tasks
- `test-case-generator` (S7-Testing) — acceptance criteria become the basis for test cases
- `ui-component-builder` (S6-Building) — story acceptance criteria define what the built UI must actually do

### Fed By
- `prd-writer` (S5-Planning) — supplies the features and flows stories are derived from
- `feature-roadmap-architect` (S5-Planning) — confirms which features are in the current phase before stories are written for them

### Feedback Loop
When `test-case-generator` or `browser-verifier` finds behavior that doesn't match any written acceptance criterion, that's a sign a story was missed or underspecified — feed it back here to add the missing story rather than patching the gap ad hoc in code.

```yaml
chain_metadata:
  skill_slug: "user-story-writer"
  stage: "planning"
  timestamp: string
  suggested_next:
    - "feature-task-breakdown"
    - "test-case-generator"
    - "ui-component-builder"
```
