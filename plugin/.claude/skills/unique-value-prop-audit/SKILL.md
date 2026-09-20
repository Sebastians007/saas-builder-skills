---
name: unique-value-prop-audit
description: >
  Audits whether a product's stated value proposition is actually distinct
  or just generic category language — a "purple cow" test against real
  competitor messaging.
  Use this skill when the user asks about "is my pitch generic", "value prop check",
  or says
  "does my value prop actually stand out", "is my tagline generic", "audit my positioning",
  "why does my homepage headline sound like everyone else's", "purple cow test my product",
  "help me sharpen my value proposition", "what makes my pitch different from competitors".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "positioning", "messaging", "differentiation"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S1-Research
---

# Unique Value Prop Audit

This skill tests a stated value proposition (headline, tagline, elevator pitch) against real competitor messaging to determine whether it's actually distinct or just interchangeable category language — the "purple cow" test: would this statement stand out in a field of competitors, or could you swap the company name and nobody would notice? It exists because most SaaS positioning is accidentally identical to everyone else's.

## Stage
This skill belongs to Stage S1: Research

## When to Use
- Founder has a headline/tagline/pitch and wants a gut check before publishing
- Homepage isn't converting and messaging is a suspect
- Founder notices their pitch "sounds like everyone else's" but can't articulate why
- After `competitor-teardown` and `feature-differentiator`, to turn real differentiators into sharp positioning language
- Before submitting to launch directories (Product Hunt, etc.) where the one-liner matters most

## Input Schema
```
value_prop_statement: string (required) — the headline, tagline, or pitch as currently written
product_description: string (required) — what it actually does, for whom
competitor_headlines: string[] (optional) — pull via competitor-teardown if not supplied
real_differentiators: string[] (optional) — from feature-differentiator output, if available
```

## Workflow
### Step 1: Run the swap test
Take `value_prop_statement` and literally ask: if you swapped in a competitor's name, would this statement still sound true and natural? If yes, it fails the purple cow test — it's generic category language, not a value prop. Common failure patterns to flag explicitly: vague outcome words with no specifics ("streamline your workflow," "all-in-one platform," "powerful and easy to use"), feature lists disguised as value props, and claims every competitor also makes (check against `competitor_headlines`).

### Step 2: Pull real competitor headlines if not supplied
Use web_search to grab the actual homepage headline/subheadline of 3-4 direct competitors (or reuse `competitor_headlines` / `competitor-teardown` output). Put them side by side with the user's statement — this is the clearest way to expose sameness, because generic phrasing patterns jump out immediately in a list.

### Step 3: Check the statement against real differentiators
If `real_differentiators` supplied (from `feature-differentiator`), check whether the value prop statement is actually built on one of them, or whether it's disconnected from what's genuinely different about the product. A value prop should be a sharp, specific claim rooted in a real differentiator — not aspirational marketing language layered on top of a commodity product.

### Step 4: Check specificity and provability
A strong value prop names a specific customer, a specific painful problem, and a specific outcome or number where possible ("cut invoice follow-up time from 3 hours/week to 10 minutes" beats "save time on invoicing"). Score the statement on how concrete and falsifiable its claim is — vague claims can't be disproven, which is itself a tell that they're not saying much.

### Step 5: Rewrite 2-3 sharper alternatives
Don't just critique — produce 2-3 rewritten versions of the value prop, each built on a real differentiator, specific to the named customer, and passing the swap test against the actual competitor headlines pulled in Step 2.

### Step 6: Self-Validation
- [ ] Swap test was actually applied line by line, not just asserted
- [ ] Real competitor headlines were checked (via input or web_search), not assumed
- [ ] Critique is specific (which phrase is generic and why) not just "make it better"
- [ ] Rewrites are grounded in a real differentiator, not just punchier generic language
- [ ] At least one rewrite is concrete/numeric where the product supports it

## Output Schema
```
{
  original_statement: string,
  swap_test_result: enum [passes, fails],
  generic_phrases_flagged: string[],
  competitor_comparison: [{ competitor: string, headline: string }],
  specificity_score: number,
  rewrites: string[]
}
```

## Output Format
```markdown
# Value Prop Audit: <product name>

## Current Statement
"<value_prop_statement>"

## Swap Test: **<PASS / FAIL>**
<explanation — could this be a competitor's line with the name changed?>

## Generic Phrases Flagged
- "<phrase>" — used by nearly every competitor in this category

## Side by Side
| Company | Headline |
|---|---|
| You | ... |
| Competitor A | ... |
| Competitor B | ... |

## Sharper Rewrites
1. "<rewrite grounded in real differentiator>"
2. "<rewrite grounded in real differentiator>"
3. "<rewrite, more specific/numeric>"

## Next Step
Run `launch-directory-submitter` to use the sharpened one-liner in launch copy, or `marketing-site-seo-audit` to check the full page against it.
```

## Error Handling
- If the product genuinely has no real differentiator yet (confirmed via `feature-differentiator` showing all table-stakes), say so honestly — no amount of copywriting fixes a commodity product; recommend finding a real wedge before polishing messaging.
- If `competitor_headlines` can't be found via web_search (obscure category), use the closest adjacent category's headlines as a comparison baseline and note the substitution.
- If the user's statement is already strong (rare but happens), say so plainly rather than manufacturing a critique — confirm the swap test pass and explain why it works.
- If the product serves multiple very different customer segments, flag that one value prop statement likely can't serve all of them well, and ask which segment matters most for this specific piece of copy.

## Examples
**Example 1**
User: "My tagline is 'The all-in-one platform for modern teams.' Does this work?"
→ Swap test fails instantly — this line could belong to hundreds of SaaS products unchanged. Flags "all-in-one" and "modern teams" as top offender phrases. Pulls 3 competitor headlines showing near-identical patterns. Rewrites grounded in the actual product's real differentiator.

**Example 2**
User: "We help small law firms manage cases better."
→ Passes partial specificity (names a customer) but fails on outcome specificity ("manage cases better" is vague/unfalsifiable). Rewrite proposes a numeric, provable outcome instead.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `launch-directory-submitter` (S1-Research) — sharpened one-liner feeds directly into launch copy
- `marketing-site-seo-audit` (S10-Growth) — audited value prop should be checked against full page copy
- `prd-writer` (S5-Planning) — the sharpened positioning can anchor the product spec's framing

### Fed By
- `feature-differentiator` (S1-Research) — supplies the real differentiators to ground rewrites in
- `competitor-teardown` (S1-Research) — supplies competitor headline data

### Feedback Loop
`signup-conversion-tracker` and `ab-test-generator` results on which headline version actually converts should feed back to refine which rewrite pattern this skill defaults to recommending.

```yaml
chain_metadata:
  skill_slug: "unique-value-prop-audit"
  stage: "research"
  timestamp: string
  suggested_next:
    - "launch-directory-submitter"
    - "marketing-site-seo-audit"
```
