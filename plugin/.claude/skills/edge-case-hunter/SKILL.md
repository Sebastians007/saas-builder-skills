---
name: edge-case-hunter
description: >
  Actively hunts for the edge cases a feature spec left out — empty states,
  concurrent users, bad input, network failure, auth expiry, and other ways
  real usage differs from the demo path.
  Use this skill when the user asks about "what edge cases am I missing",
  "what could break this", "what did I not think of", "stress this idea
  before I build it", "poke holes in this feature", "what happens if two
  people do this at once", or "what's the worst thing a user could do here".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "testing", "edge-cases", "risk-review"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S7-Testing
---

# Edge Case Hunter

Reads a feature spec or built feature the way a mischievous user or an unlucky server would — actively looking for the gaps between "what the demo shows" and "what actually happens." This is adversarial by design: its job is to find problems, not to confirm the feature is fine.

## Stage
This skill belongs to Stage S7: Testing

## When to Use
- Before building, to pressure-test a spec while it's still cheap to change
- After building, as a second pass beyond the standard test-case-generator list
- When a feature involves shared/concurrent state (comments, likes, inventory counts, seats)
- When a feature involves money, deletion, or anything irreversible
- When the founder says "this should be simple" — simple features hide the most missed edges
- Before a feature goes in front of real users for the first time

## Input Schema
```
feature: string
spec_or_code_summary: string     # what exists — spec text, code excerpt, or plain description
data_touched: [string] (optional)  # e.g. "user balance", "inventory count", "shared doc"
external_deps: [string] (optional) # e.g. "Stripe", "SendGrid", "S3 upload"
concurrency_expected: boolean (optional)  # can multiple users hit this at once?
```

## Workflow
### Step 1: Map the "unhappy paths"
List every point where the feature assumes something goes right: user is logged in, input is valid, network is up, third party responds, only one user acts at a time. Each assumption is a candidate edge case.

### Step 2: Hunt empty and extreme states
First-ever use (empty database, zero items, new account with nothing in it), maximum scale (10,000 items in a list, huge file upload), and boundary numbers (0, negative, exactly at a limit, one over a limit).

### Step 3: Hunt concurrency and timing
Two users editing the same record, double-submit from a slow network, action triggered while a related background job is still running, clock/timezone edge cases (midnight rollover, daylight saving), rapid repeated actions (rage-clicking a button).

### Step 4: Hunt auth and permission edges
Session expires mid-action, user's role changes while they have a tab open, user tries to access another user's data by guessing a URL/ID, logged out in one tab but not another, token refresh failure.

### Step 5: Hunt failure of things outside your control
Third-party API times out or returns malformed data, payment succeeds but webhook is delayed or never arrives, email provider bounces silently, database write succeeds but response never reaches the client (did it double-run?).

### Step 6: Rank by (likelihood x damage)
For each edge case, rate likelihood (common / occasional / rare) and damage if it happens (annoying / data loss / money loss / security). Sort so the founder sees the dangerous-and-likely ones first.

### Step 7: Self-Validation
- [ ] At least one concurrency case is included if the feature touches shared or counted data
- [ ] At least one "what if the user is malicious/curious and edits the URL" case is included for anything with IDs in it
- [ ] Every case has a stated likelihood and damage rating, not just a description
- [ ] The list isn't padded with cases already covered by a standard test-case-generator happy-path list
- [ ] Every high-damage case includes a one-line suggested mitigation

## Output Schema
```
{
  feature: string,
  edge_cases: [
    {
      id: string,
      category: "empty_state" | "extreme_scale" | "concurrency" | "auth_permission" | "external_failure" | "timing",
      description: string,
      likelihood: "common" | "occasional" | "rare",
      damage: "annoying" | "data_loss" | "money_loss" | "security",
      suggested_mitigation: string
    }
  ]
}
```

## Output Format
```markdown
# Edge Case Hunt: [Feature Name]

## Highest Risk (fix before shipping)
1. [description] — likelihood: X, damage: X
   Mitigation: ...

## Worth Handling
- ...

## Low Priority / Note for Later
- ...

## Assumptions the Spec Made That Aren't Guaranteed
- ...
```

## Error Handling
- Spec is too thin to analyze → generate edge cases from the feature name alone (e.g. "comments" implies concurrent editing, spam, empty comment) and flag that the spec needs more detail
- Feature has no shared/concurrent data and no money involved → say so, and keep the list short instead of manufacturing risk that isn't there
- User pastes code instead of a spec → read the code for what it assumes (no null checks, no try/catch, no auth check) and turn each missing guard into an edge case
- Can't tell if concurrency is possible → assume yes for anything with more than one user in the product, and say why

## Examples
1. User: "what am I missing on the 'invite teammate' feature" → Skill finds: invite sent to already-registered email, invite sent twice, invitee never accepts, inviter's seat limit hit mid-invite, invite link reused after acceptance. Outcome: founder adds a seat-limit check before shipping.
2. User: "poke holes in this inventory count feature" (paste code) → Skill flags no locking on the decrement, meaning two simultaneous purchases could both succeed and oversell the last unit. Outcome: founder adds a database-level constraint before launch.
3. User: "this should be simple, just a delete button" → Skill flags: no confirmation step, no undo, cascading deletes not considered, user deletes something someone else is currently viewing. Outcome: founder adds a confirm dialog and soft-delete.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- test-case-generator (S7-Testing)
- browser-verifier (S7-Testing)
- security-review-lite (S7-Testing)

### Fed By
- user-story-writer (S5-Planning)
- data-model-diagrammer (S6-Building)

### Feedback Loop
When a shipped feature breaks in production from a case this skill missed, log the pattern so future hunts for similar features check it by default.

```yaml
chain_metadata:
  skill_slug: "edge-case-hunter"
  stage: "testing"
  timestamp: string
  suggested_next:
    - "test-case-generator"
    - "security-review-lite"
```
