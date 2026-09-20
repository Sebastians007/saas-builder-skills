---
name: avatar-extraction
description: >
  Extracts one specific, real buyer for the SaaS product — not a demographic
  bucket — so every later headline, email, and pricing page is written to a
  single person instead of "our users" in general.
  Use this skill when the user asks about defining their target customer,
  ideal user, or buyer persona, or says
  "who is this actually for", "define my target customer", "who's my ideal user",
  "build a customer avatar", "who am I writing this copy for", "I don't know who I'm selling to",
  "give me a real persona not a demographic", "who is my ICP".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "positioning", "customer-research", "avatar"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Avatar Extraction

This skill builds one specific buyer — a real person with a job, a bad day, and a reason to act today — from whatever the founder already knows about their product and market. Copy written to "SaaS teams" or "busy professionals" converts nothing; copy written to one believable person converts because the reader recognizes themselves in the first line.

## Stage
This skill belongs to Stage S10: Copywriting

## When to Use
- Before writing any landing page, ad, or email — copy needs a named target, not a market segment
- The user has a product but describes their customer only in demographics ("small business owners", "developers")
- Multiple avatars are being written to at once and the copy is mushy as a result
- A pivot changed who the product actually serves and old copy no longer fits
- The user is about to run `headline-matrix` or `schwartz-awareness-mapper` and needs the input those skills require
- The user says the copy "sounds like it's for everyone and no one"

## Input Schema
```
product_or_service: string
known_customers: string?        # existing users, interviews, support tickets, reviews if any
market_context: string?         # from saas-idea-validator / underserved-market-finder if run
assumed_audience: string?       # who the founder currently thinks it's for
pricing_tier: string?           # which plan/tier this avatar buys
```

## Workflow
### Step 1: Pull the Real Person Out, Not a Segment
Ask for (or infer from existing research) three things about this one buyer:
- Who they are: their job, their day, what stage of the business/life they're in
- What they're actively trying to get done right now
- What's frustrating them today, specifically, not "inefficiency" in the abstract

Reject demographic-only answers ("35-45, tech-savvy, mid-market"). If that's all that's given, push back: ask what this person was doing five minutes before they searched for a product like this.

### Step 2: Extract What They've Already Tried
- What tools, workarounds, or competitors have they already used
- Why each of those failed or fell short specifically
- What they now believe about solving this problem (often wrong, and useful to know)

This step is what separates a real avatar from a guess — a person who has already tried and failed at something writes differently to than a person encountering the problem for the first time.

### Step 3: Surface the Emotional Driver Underneath the Rational One
Every SaaS buyer has a stated reason ("need better reporting") and a real one (afraid of looking incompetent in the next board meeting). Name both:
- Fear driving the search
- Status or control they're trying to protect or gain
- What relief looks like the moment the product works

### Step 4: Write the One-Paragraph Avatar
Compress Steps 1-3 into a paragraph specific enough that the founder could pick this person out of a room. No ranges, no "could be either." One person, one situation.

### Step 5: Self-Validation
- [ ] Avatar is one person, not a segment or range
- [ ] At least one specific failed attempt is named
- [ ] Emotional driver is distinct from the stated rational reason
- [ ] A stranger reading this avatar could write a Slack message this person would actually send
- [ ] No demographic-only description slipped through unchallenged

## Output Schema
```json
{
  "avatar_name": "string (a real-sounding first name, for internal shorthand)",
  "situation": "string",
  "actively_trying_to_do": "string",
  "daily_frustration": "string",
  "failed_attempts": ["string"],
  "current_belief_about_the_problem": "string",
  "emotional_drivers": { "fear": "string", "status_or_control": "string", "relief": "string" },
  "buys_which_tier": "string|null"
}
```

## Output Format
```markdown
# Primary Avatar: [Name]

**Situation:** [one or two sentences — job, stage, context]
**Actively trying to:** [outcome they want right now]
**Daily frustration:** [specific, not abstract]

## Already Tried and Failed
- [attempt 1] — failed because [reason]
- [attempt 2] — failed because [reason]

## What They Currently Believe
[the belief driving their search, even if it's wrong]

## Emotional Drivers
- Fear: [specific fear]
- Status/control: [what they're protecting or chasing]
- Relief: [what it feels like the moment this works]

## Use This Avatar For
Every headline, email, and page should be able to be read aloud to [Name] and sound like it's talking directly to them.
```

## Error Handling
- User only gives demographics → ask what this person did five minutes before searching for a solution; refuse to finalize on demographics alone
- Multiple very different customer types exist → build one avatar per distinct buying motivation, don't average them into a blur; recommend picking the highest-value one to lead with
- No customer data exists yet (pre-launch) → build the avatar from the founder's best guess of who has the problem worst, label it "hypothesis avatar," and flag it for validation against `saas-idea-validator` findings
- User wants a "broad" avatar to not exclude anyone → explain that broad avatars produce broad (ignored) copy; narrow avatars convert the right people and repel the wrong ones on purpose

## Examples
**Example 1**
User: "My product is project management software for agencies."
Skill: Pushes past "agency owners" to extract someone like "Dana, ops lead at a 12-person design agency, currently tracking three client retainers in spreadsheets that fall out of sync every Friday when invoices are due, already tried Asana and Trello but both required rebuilding the same template every project" — with emotional driver being fear of an invoice being wrong in front of a client.

**Example 2**
User: "I don't really know who my customer is yet, I just built the tool."
Skill: Builds a hypothesis avatar from the problem the tool solves, labels it clearly as unvalidated, and recommends running `saas-idea-validator` or pulling five support tickets/interviews before locking copy to it permanently.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- offer-extraction (S10-Copywriting)
- schwartz-awareness-mapper (S10-Copywriting)
- headline-matrix (S10-Copywriting)
- unique-value-prop-audit (S1-Research)

### Fed By
- saas-idea-validator (S1-Research)
- underserved-market-finder (S1-Research)
- competitor-teardown (S1-Research)

### Feedback Loop
Once copy built on this avatar ships, reply and conversion data from `signup-conversion-tracker` should confirm or correct the avatar — if the real buyers who convert don't match this description, re-run this skill rather than patch the copy.

```yaml
chain_metadata:
  skill_slug: "avatar-extraction"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "offer-extraction"
    - "schwartz-awareness-mapper"
```
