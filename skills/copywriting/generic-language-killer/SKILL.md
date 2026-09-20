---
name: generic-language-killer
description: >
  Strips vague, corporate, or AI-sounding language out of SaaS copy and
  replaces it with specific, human wording — a final QA pass that catches
  "seamlessly empowers your workflow" before it ships.
  Use this skill when the user asks about copy that sounds generic, fluffy,
  or AI-written, or says
  "this sounds like every other SaaS site", "make this sound less corporate",
  "this reads like AI wrote it", "tighten this copy up", "cut the fluff from this page",
  "this sounds generic, fix it", "review this copy before it goes live".
license: MIT
version: "1.0.0"
tags: ["saas", "copywriting", "editing", "qa", "brand-voice"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S4-Copywriting
  adapted_from: "realkimbarrett/advertising-skills (MIT)"
---

# Generic Language Killer

This skill is the last pass before copy ships: it hunts down vague corporate filler, buzzword soup, and AI-sounding phrasing, and replaces each instance with something specific and human. It runs after the other copywriting skills, not instead of them — it's a QA layer, not a copy generator.

## Stage
This skill belongs to Stage S4: Copywriting

## When to Use
- Right before any landing page, email, or ad copy ships, as a final check
- The user reads their own copy back and it "sounds like every other SaaS site"
- Copy was drafted quickly (including by AI) and needs a specificity pass
- A page uses words like "seamless," "empower," "leverage," "cutting-edge," or "revolutionize" without realizing it
- Onboarding flow copy or in-app messaging feels stiff and corporate instead of like a person talking
- The user wants a repeatable check to run on every piece of copy before publishing

## Input Schema
```
copy_to_review: string
placement: string?           # e.g. "landing page hero", "onboarding email", "pricing page"
brand_voice_notes: string?   # any existing tone guidance to preserve
```

## Workflow
### Step 1: Flag Generic Phrases and Buzzwords
Scan for and flag the common offenders:
- Vague power verbs: "empower," "leverage," "unlock," "supercharge," "revolutionize"
- Meaningless modifiers: "seamless," "cutting-edge," "best-in-class," "robust," "innovative"
- Hedge phrases that say nothing: "help you achieve your goals," "take your business to the next level," "streamline your workflow"
- AI-tell patterns: overuse of "moreover"/"furthermore," triplet lists ("fast, reliable, and secure"), em-dash-heavy sentence padding, and summary sentences that restate what was just said

### Step 2: Replace With Specifics
For each flagged phrase, ask "specifically what does this mean for this product" and replace it:
- "Streamline your workflow" → "cut your weekly billing reconciliation from 2 hours to 15 minutes"
- "Best-in-class security" → "SOC 2 Type II certified, data encrypted at rest and in transit"
- "Empower your team" → "your ops lead sees every retainer status without asking three people in Slack"

If no specific fact is available to replace a vague claim, flag it rather than inventing a fake specific — a true vague statement beats a false specific one.

### Step 3: Cut Sentences That Restate Instead of Add
Any sentence that just rephrases the sentence before it gets cut. Every sentence must earn its place by adding new information, proof, or a new angle.

### Step 4: Read It Aloud Test
Check whether each line sounds like something a real founder would say to a friend over coffee, or like it was assembled from a marketing template. If it fails, rewrite it plainer.

### Step 5: Self-Validation
- [ ] Every flagged buzzword/vague phrase is either replaced with a specific or explicitly noted as needing real data to specify
- [ ] No sentence merely restates the one before it
- [ ] Final copy passes the read-aloud test
- [ ] Brand voice notes (if given) are respected — this is a clarity pass, not a full tone rewrite
- [ ] Nothing was invented to sound specific that isn't actually true about the product

## Output Schema
```json
{
  "placement": "string|null",
  "flags": [
    { "original_phrase": "string", "issue": "buzzword|vague_hedge|ai_tell|restated_sentence", "replacement": "string|null", "needs_real_data": "boolean" }
  ],
  "rewritten_copy": "string"
}
```

## Output Format
```markdown
# Copy Review: [placement]

## Flagged
| Original | Issue | Fix |
|---|---|---|
| "seamlessly empowers your workflow" | buzzword | "cuts your reconciliation time from 2 hours to 15 minutes" |
| ... | ... | ... |

## Needs Real Data (flagged, not invented)
- [claim that needs a real number/proof point before it can be made specific]

## Rewritten Copy
[full cleaned version, ready to paste]
```

## Error Handling
- No specific fact available to replace a vague claim → flag it openly rather than fabricating a stat; recommend the user supply the real number or drop the claim
- User's brand voice is intentionally more formal/corporate (e.g. enterprise/compliance-heavy SaaS) → respect that tone, apply the specificity fix without forcing a casual register that doesn't fit the buyer
- Copy is already specific and clean → say so plainly rather than manufacturing flags to justify the pass

## Examples
**Example 1**
User: "Review this: 'Our platform seamlessly empowers your team to unlock best-in-class productivity and take your workflow to the next level.'"
Skill: Flags all four phrases as content-free, asks what specifically changes for the team, and rewrites to: "Your team stops re-entering the same client data in three tools — one dashboard shows every project's real status."

**Example 2**
User: "This onboarding email sounds like it was written by AI."
Skill: Identifies the AI-tell pattern (triplet lists, restated closing sentence, "moreover" transitions), cuts the restated sentence, breaks the triplet into one specific concrete action step, and confirms the rewrite still matches the brand voice notes provided.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- marketing-site-seo-audit (S10-Growth)
- onboarding-flow-builder (S4-Building)

### Fed By
- objection-crusher (S4-Copywriting)
- full-funnel-campaign-orchestrator (S4-Copywriting)

### Feedback Loop
Copy that still underperforms after a generic-language pass points to an offer or avatar problem, not a wording problem — route back to `offer-extraction` or `avatar-extraction` rather than running another editing pass on the same weak premise.

```yaml
chain_metadata:
  skill_slug: "generic-language-killer"
  stage: "copywriting"
  timestamp: string
  suggested_next:
    - "marketing-site-seo-audit"
    - "onboarding-flow-builder"
```
