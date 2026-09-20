---
name: incident-runbook-writer
description: >
  Writes a short, practical runbook for what to do when production breaks,
  sized for a solo founder or a two-to-three-person team with no on-call
  rotation.
  Use this skill when the user asks about "what do I do when my site goes
  down", "write me an incident runbook", "I panicked when the app broke
  and didn't know what to do first", "how do I tell customers about an
  outage", "disaster response plan", or "what's my process if something
  breaks in production".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "incident-response", "runbook", "ops"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Operations
---

# Incident Runbook Writer

Writes a one-page, print-or-pin-able runbook that tells a stressed founder exactly what to do in the first 15 minutes of an outage or bad bug — check this, say this to customers, escalate to this person, log this. No enterprise incident-command-system roles, no 40-page playbook — just the minimum that keeps a small team from freezing when something breaks.

## Stage
This skill belongs to Stage S9: Operations

## When to Use
- The app is live with paying customers and there's no written plan for "what do I do if it breaks"
- After a real incident that went badly (slow response, confused communication, no record kept)
- Growing from solo founder to a small team and need to define who does what
- A customer/investor asks "what's your incident response process"
- Periodic review: monitoring-alerting-setup just went in, and alerts need a documented next step
- Onboarding a second person who needs to know what to do if they're the one who notices something's wrong

## Input Schema
```
team_size: number                  # usually 1-3 for this pack's audience
roles: string[] | none             # e.g. ["Sebastian - founder/eng"], empty if solo
customer_comm_channel: string      # e.g. "email list", "status page", "in-app banner", "none yet"
critical_systems: string[]         # from monitoring-alerting-setup output if available
has_status_page: boolean
past_incidents: string | none      # brief description of what's gone wrong before
```

## Workflow
### Step 1: Define severity levels simply
Skip enterprise SEV1-SEV5 taxonomies. Use three plain tiers:
- **Down** — app or a core flow (login, signup, payment) is unusable for customers
- **Degraded** — app works but slow, erroring intermittently, or a non-core feature is broken
- **Cosmetic** — visible but not blocking anyone from using the product

### Step 2: Write the first-15-minutes checklist
This is the core of the runbook — what to literally do, in order, the moment an alert fires or a bug is spotted:
1. Confirm it's real (check the monitoring dashboard / try to reproduce)
2. Check what changed recently (last deploy, last config change, any third-party status page — Cloudflare status, database provider status)
3. Decide severity (Down / Degraded / Cosmetic)
4. If Down: start a timestamped note (even a scratch doc) of what's happening as you go — this becomes the incident log
5. If Down and customer-facing: post a short status update (see Step 3)
6. Start fixing or rolling back — for a small app, "roll back the last deploy" is almost always the fastest fix and should be tried before deep debugging

### Step 3: Write the communication templates
For solo founders, over-communication is cheap insurance. Provide ready-to-send templates for:
- Initial "we're aware and looking into it" message (send within 15 min of confirming a Down incident)
- Update message (send every 30-60 min while Down, even if the update is "still working on it")
- Resolution message (what happened in plain language, what was done, no need for a full postmortem)
Specify exact channel: status page if one exists, otherwise email/in-app banner/social — pick what the input says the founder actually has.

### Step 4: Define who does what (even for a team of one)
For team_size = 1, this step just confirms the founder is doing everything and flags what to do if they're unreachable (e.g. a backup contact, or accepting that response will be delayed). For team_size > 1, assign clear single-owner roles: one person fixes, one person communicates — never both roles assumed by default without being said.

### Step 5: Write the after-it's-over checklist
Keep it short: write one paragraph on what happened and why, one sentence on what will prevent it next time (a new monitor, a new test, a code fix), and log it somewhere findable (a running incidents doc). This feeds back into monitoring-alerting-setup and test-case-generator.

### Step 6: Self-Validation
- [ ] Runbook fits on one page / can be read in under 2 minutes under stress
- [ ] First-15-minutes steps are literal actions, not vague guidance
- [ ] At least one communication template is ready to copy-paste, not just described
- [ ] Roles are assigned even if there's only one person
- [ ] "Roll back first, debug second" is present for Down incidents unless the user's stack makes rollback impractical
- [ ] Post-incident step captures a specific follow-up action, not just "review later"

## Output Schema
```
{
  severity_levels: [ { name: string, definition: string } ],
  first_15_minutes: string[],
  comm_templates: [ { trigger: string, channel: string, message: string } ],
  roles: [ { role: string, owner: string } ],
  post_incident_checklist: string[]
}
```

## Output Format
```markdown
# Incident Runbook — <app name>

## Severity levels
- **Down**: ...
- **Degraded**: ...
- **Cosmetic**: ...

## First 15 minutes (Down incident)
1. ...
2. ...

## Communication templates
### Initial notice (send within 15 min)
> "..."

### Update (every 30-60 min)
> "..."

### Resolved
> "..."

## Who does what
| Role | Owner |
|---|---|
| Fix it | <name> |
| Talk to customers | <name> |

## After it's over
- [ ] Write one paragraph: what happened
- [ ] Write one sentence: what prevents it next time
- [ ] Log it in <incidents doc location>
```

## Error Handling
- If team_size is 1, don't force multi-role structure — write it for one person wearing both hats, with a note on what happens if they're asleep/unreachable
- If customer_comm_channel is "none yet," recommend the lightest option (an email to the signup list, or a free status page like a simple Cloudflare Pages status.html) rather than requiring a paid status-page tool
- If past_incidents is provided, mine it for what specifically went wrong in communication or response speed and bake a fix into this runbook rather than writing generic advice
- If has_status_page is false and the app has more than a handful of customers, flag setting one up as a near-term action, but still deliver the runbook using the fallback channel today
- If the user wants a full incident command / postmortem process with formal roles (SEV levels, incident commander, scribe), push back that it's disproportionate for team_size ≤ 3 unless they have a specific reason (e.g. investor/compliance requirement)

## Examples
**Example 1**: Solo founder says "my app went down and I had no idea what to do, just refreshed the dashboard panicking." Skill writes a one-person runbook: check monitoring, check Cloudflare status page, try rollback first, send a one-line status email, log it afterward.

**Example 2**: Two-person team (founder + one contractor) wants a runbook before their first enterprise customer goes live. Skill assigns "fix it" to the contractor and "talk to customers" to the founder, adds a status page recommendation since the customer will expect visibility.

**Example 3**: User pastes a description of a bad past incident (took 3 hours to notice, customers found out via Twitter). Skill's post-incident section explicitly recommends monitoring-alerting-setup as the fix for slow detection, and a status page as the fix for the communication gap.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- monitoring-alerting-setup (S9-Operations)
- test-case-generator (S7-Testing)

### Fed By
- monitoring-alerting-setup (S9-Operations)
- backup-recovery-builder (S9-Operations)

### Feedback Loop
Every real incident logged should add a new monitor, test case, or comm-template fix back into the runbook so the next incident of the same shape is handled faster.

```yaml
chain_metadata:
  skill_slug: "incident-runbook-writer"
  stage: "operations"
  timestamp: string
  suggested_next:
    - "monitoring-alerting-setup"
    - "test-case-generator"
```
