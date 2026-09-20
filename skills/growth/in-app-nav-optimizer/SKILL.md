---
name: in-app-nav-optimizer
description: >
  Reviews a SaaS app's internal navigation and information architecture to
  find the confusing paths that make users get lost, give up, or churn, and
  produces a specific list of what to rename, merge, move, or remove.
  Use this skill when the user asks about confusing navigation, users getting
  lost, or menu/IA problems, or says
  "users can't find things in my app", "my nav feels cluttered", "people get lost after signup",
  "where should this feature live in the menu", "should I combine these two pages",
  "is my app's navigation confusing", "review my sidebar/menu structure", "users keep asking where X is".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "ux", "information-architecture", "retention"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
---

# In-App Navigation Optimizer

This skill audits a live app's menu, sidebar, and page structure the way a new user experiences it, flags every place someone could get lost or take the wrong path, and gives a short list of renames/moves/merges ranked by how many users hit that path. It exists because founders who built the app know where everything is and can't see the maze they built.

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- Support tickets or user questions repeatedly ask "where do I find X"
- signup-conversion-tracker flagged Signup → Activation as the biggest drop-off
- The app has grown past its original 3-4 pages and now has 10+ menu items
- The user wants a second opinion before adding yet another nav item
- A new feature was just built and needs a home in the existing structure
- Users abandon mid-task and support has to walk them through basic navigation

## Input Schema
```
app_description: string          # what the app does, who it's for
current_nav_structure: string    # list/screenshot description of menus, sidebar, tabs
core_user_jobs: array?           # the 3-5 things users come to the app to do
known_confusion_points: string?  # support tickets, user complaints, if any
page_or_feature_count: number?
```

## Workflow
### Step 1: List the Core User Jobs
Before touching the nav, get the 3-5 things a user actually comes to do (not every feature — the top jobs). If the user can't name them, derive them from signup-conversion-tracker's "first key action" definition or ask directly: "what does someone do in your app in their first 10 minutes that proves they got value?"

### Step 2: Map Current Navigation Against Those Jobs
For each core job, trace the exact click path a new user would take from login to completing it. Count clicks. Note anywhere the path requires knowing something not visible on screen (a hidden menu, a feature named differently than the user would guess, a setting buried three levels deep).

### Step 3: Flag Nav Anti-Patterns
Check the structure against this list:
- Items named with internal jargon instead of the user's own words (e.g. "Workspace Config" instead of "Settings")
- More than 7 top-level items (cognitive overload — group or cut)
- Two or more items that sound like they do the same thing
- A core job requiring more than 3 clicks from login
- A feature that exists but has no nav entry point at all (orphaned page)
- Settings/admin items mixed into the same level as daily-use items
- No visible "you are here" indicator across multi-step flows

### Step 4: Rank Fixes by Impact
Order recommendations by which core job they unblock, not by how easy the fix is to code. A rename that fixes the #1 job's confusion outranks a full nav redesign that touches rarely-used admin pages.

### Step 5: Write Specific Before/After for Each Fix
Never say "improve navigation clarity" — say exactly: rename X to Y, move X from menu A to menu B, merge X and Y into one item called Z, add a nav entry for orphaned page X under menu Y.

### Step 6: Self-Validation
Before presenting output, confirm:
- [ ] Every core user job has a traced click path with a click count
- [ ] Every recommendation is a specific rename/move/merge/remove, not a vague suggestion
- [ ] Recommendations are ranked by which core job they fix, most important first
- [ ] No recommendation adds nav complexity without removing something else, unless justified

## Output Schema
```json
{
  "core_jobs": ["string"],
  "job_paths": [
    {"job": "string", "click_path": ["string"], "click_count": "number", "friction": "string|null"}
  ],
  "anti_patterns_found": ["string"],
  "recommendations": [
    {"priority": "number", "change_type": "rename|move|merge|remove|add", "before": "string", "after": "string", "impacts_job": "string"}
  ]
}
```

## Output Format
```markdown
# Navigation Audit

## Core User Jobs & Click Paths
| Job | Path | Clicks | Friction |
|---|---|---|---|
| [job] | Login → [step] → [step] | [n] | [issue or none] |

## Anti-Patterns Found
- [pattern found, with example]

## Recommendations (ranked)
1. [Change type]: "[before]" → "[after]" — fixes friction on [job]
2. ...

## Do Not
- Add new top-level nav items to fix this (grouping/renaming existing items almost always beats adding more)
- Redesign the whole nav at once — ship the top 1-2 fixes, then recheck with signup-conversion-tracker
```

## Error Handling
- No current nav structure provided → ask the user to list every menu item and page, or describe a screenshot; don't guess at a typical SaaS nav
- Core user jobs unclear → derive from signup-conversion-tracker's activation event if available, otherwise ask directly
- User wants a full redesign for a 6-month-old app with working nav → push back; recommend the top 1-2 fixes first, redesigns are expensive and risky mid-growth
- Confusion reported but no specifics ("people get lost") → ask for actual support tickets or session recordings if available; without specifics, do a structural audit only and flag it as based on structure, not observed behavior
- Nav is genuinely fine (jobs take 1-2 clicks, no anti-patterns) → say so plainly rather than inventing problems to justify the audit

## Examples
**Example 1**
User: "Users keep emailing support asking where billing settings are."
Skill: Traces the click path to billing settings, finds it's nested under "Account" → "Preferences" → "Plan," three levels deep and not obviously labeled; recommends moving it to a top-level "Billing" item since it's a job enough users hit to generate repeat support tickets.

**Example 2**
User: "My sidebar has 12 items now and feels cluttered but I don't know what to cut."
Skill: Maps the 12 items against the 4 core jobs, finds only 5 are used for core jobs and the rest are admin/rare-use items; recommends grouping the other 7 under a single "More" or "Settings" collapsible section, ranked by usage.

**Example 3**
User: "We just shipped a new reporting feature, where should it live in the nav?"
Skill: Checks whether reporting supports one of the core jobs or is a secondary/admin feature, places it accordingly (top-level if core, nested if secondary), and gives the exact label to use based on how users describe the feature in their own words (from support tickets or interviews if available).

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- signup-conversion-tracker (S10-Growth)
- ab-test-generator (S10-Growth)
- accessibility-auditor (S7-Testing)

### Fed By
- signup-conversion-tracker (S10-Growth)
- onboarding-flow-builder (S6-Building)

### Feedback Loop
After shipping nav fixes, re-run signup-conversion-tracker on the same activation stage to confirm the click-path fix actually raised the conversion rate rather than just feeling cleaner.

```yaml
chain_metadata:
  skill_slug: "in-app-nav-optimizer"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "signup-conversion-tracker"
    - "ab-test-generator"
```
