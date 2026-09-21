---
name: self-improver
description: >
  Reviews a completed project retrospectively — what broke, what took too long, what
  worked — and turns those lessons into concrete changes to how the skill pack gets used
  next time, so the same mistakes don't repeat across projects.
  Use this skill when the user asks "what went wrong with this project", "let's do a
  retro", "why did this take so long", "what should we do differently next time", "we hit
  the same problem again", "postmortem this launch", "what can we learn from [project]",
  or "I feel like we keep repeating the same mistakes".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "retrospective", "process-improvement", "meta"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S11-Meta
---

# Self Improver

Runs a retrospective on a finished project or sprint and converts the findings into specific, actionable changes to how the skill pack gets used — not a vague "communicate better" lesson, but concrete edits like "always run compliance-checker before deployment" or "skip technical-spike-brief for features under 2 days." This is the skill that exists specifically to break repeating failure loops.

## Stage
This skill belongs to Stage S11: Meta

## When to Use
- A project just launched, shipped, or was killed and there's a natural pause to reflect
- The founder notices the same kind of problem happening again (e.g. "we always underestimate deployment time")
- After a `feature-roadmap-architect` milestone closes, to check if the plan matched reality
- Quarterly or after any project that ran significantly over time/budget
- Before starting a new project of a similar type, to pull forward lessons from the last one

## Input Schema
```
retro_request:
  project_name: string
  what_shipped: string              # what actually got built/launched
  timeline_planned_vs_actual: {planned: string, actual: string}
  known_pain_points: [string]       # things the founder already knows went wrong
  skills_used: [string]             # optional, which pack skills were invoked during the project
  prior_retros_available: bool      # whether past self-improver output exists to compare against
```

## Workflow
### Step 1: Reconstruct the Timeline
Lay out what actually happened, stage by stage, against what was planned. Be specific about where time was lost — "building took longer" is not useful, "auth flow took 3 weeks because OAuth provider config wasn't researched first" is.

### Step 2: Separate Process Failures from Bad Luck
Sort each pain point into one of three buckets:
- **Process gap** — a skill/step that should have been used but wasn't (fixable by changing the workflow)
- **Skipped step** — the right skill exists in the pack but was skipped under time pressure
- **Genuine unknown** — something nobody could have predicted (not a process fix, just a note)
Only the first two buckets produce actionable changes; don't manufacture a lesson from bad luck.

### Step 3: Check Against Prior Retros
If `prior_retros_available`, compare this project's pain points against past ones. Flag any repeat — the same failure showing up twice is the strongest signal something needs to change, not just be noted.

### Step 4: Convert Each Finding into a Concrete Change
For every process gap or skipped step, write a specific, checkable rule — not advice. Examples of the right specificity:
- Bad: "be more careful with compliance"
- Good: "run `compliance-checker` before every `cloudflare-deployer` call, no exceptions, even for internal tools"
Tie each rule to a specific skill in the pack where possible, so it becomes an actual workflow change, not a wish.

### Step 5: Flag Pack Gaps
If a pain point can't be traced to a skipped or misused skill because no skill covers that need, flag it as a candidate for `create-skill` or `category-designer` — don't force-fit an existing skill where none applies.

### Step 6: Write the Standing Rule List
Output a running list of "always do X" / "never skip Y" rules this project produced, meant to be checked at the start of the next similar project (this is what breaks the repeat-failure loop — the rules need to be surfaced next time, not just written once and forgotten).

### Step 7: Self-Validation
Before presenting, silently check:
- [ ] Is every lesson tied to a specific, checkable action (not vague advice)?
- [ ] Did I separate real process failures from bad luck instead of manufacturing lessons?
- [ ] Did I check for repeat failures against prior retros, if available?
- [ ] Did I flag genuine pack gaps to `create-skill`/`category-designer` rather than forcing a fit?
- [ ] Is the output short enough that the founder will actually reread it next time (not a wall of text)?

## Output Schema
```
{
  "project_name": string,
  "timeline_variance": string,
  "findings": [
    {
      "pain_point": string,
      "category": "process_gap" | "skipped_step" | "genuine_unknown",
      "is_repeat": bool,
      "fix_rule": string | null,
      "related_skill": string | null
    }
  ],
  "pack_gaps_flagged": [string],
  "standing_rules_added": [string]
}
```

## Output Format
```markdown
# Retrospective — <Project Name>

## Timeline
Planned: <x> | Actual: <y> | Variance: <why, in one line>

## What Worked
<short list — don't skip this, repeat the good parts on purpose>

## What Broke

| Pain Point | Category | Repeat? | Fix |
|---|---|---|---|
| ... | ... | ... | ... |

## Pack Gaps Found
<any need not covered by an existing skill — route to create-skill or category-designer>

## Standing Rules (carry forward to next project)
- Always: <rule>
- Never: <rule>
...

## Repeat Failures Flagged
<anything that has now happened 2+ times — treat as highest priority to fix>
```

## Error Handling
- Founder only wants to vent, not analyze: let them talk it out first, then ask permission before converting it into structured findings — don't force the format on a raw complaint.
- No prior retros exist for comparison: skip the repeat-failure check, note it as the first retro on record for this type of project.
- Pain point genuinely traces to bad luck (e.g. a third-party outage): log it honestly in the genuine_unknown bucket, don't stretch it into a fake process lesson.
- Multiple pain points trace to the same root cause: consolidate into one fix rule rather than listing near-duplicate lessons.
- Founder can't articulate what went wrong, just that "it felt hard": walk the actual timeline with them stage by stage until specific friction points surface — don't accept vague dissatisfaction as the final finding.

## Examples
**Example 1**
User: "the deployment pipeline deployment always takes way longer than expected. Third time now."
The skill checks this against prior retros, confirms it's a genuine repeat, traces it to skipped `env-secrets-manager` setup each time, and writes a hard standing rule: "always run env-secrets-manager before first cloudflare-deployer call on any new environment."
Outcome: a specific, checkable rule added to prevent a 4th recurrence.

**Example 2**
User: "We just launched Acme, let's do a quick retro."
The skill reconstructs the timeline, finds compliance work was rushed at the last minute (a skipped-step finding, not bad luck since `compliance-checker` existed and wasn't run early), and adds the standing rule to run compliance-checker at planning stage, not launch week.
Outcome: retro produces one concrete process change plus a "what worked" note to repeat (fast core build).

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `create-skill` (S11-Meta) — pack gaps found in retros become new skill candidates
- `category-designer` (S11-Meta) — repeated gaps across multiple retros can justify a new stage
- `feature-roadmap-architect` (S5-Planning) — timeline lessons feed into more realistic future estimates

### Fed By
- `compliance-checker` (S11-Meta) — compliance gaps found late are a common retro input
- `deal-review`-style operational skills across all stages — any completed project is fair input, but most directly `feature-roadmap-architect` (S2) and deployment skills (S5)

### Feedback Loop
Standing rules accumulate across projects into a growing checklist that gets checked at the start of every new similar project, which is the actual mechanism that stops the 6-month failure loop from repeating.

```yaml
chain_metadata:
  skill_slug: "self-improver"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "create-skill"
    - "category-designer"
```
