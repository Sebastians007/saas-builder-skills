---
name: research-report-builder
description: >
  Runs the full research phase and compiles it into ONE coherent report —
  market size and growth, competition, target audience, opportunity, and a
  go/pivot/kill recommendation — instead of leaving the founder to stitch
  together five separate skill outputs themselves.
  Use this skill when the user asks about "research this idea", "give me a full
  market report", or says
  "do the research on this", "I want a complete picture before I decide",
  "research report for this idea", "tell me everything about this market",
  "give me a research summary", "start the research phase", "research this
  before I build anything", "I don't want to run five different skills myself".
license: MIT
version: "1.0.0"
tags: ["saas", "research", "orchestrator", "report", "market", "local-file"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.1"
  stage: S1-Research
---

# Research Report Builder

This is the orchestrator S1-Research was missing — the same role `funnel-builder-orchestrator` plays for S3-Funnel-Build. Run this once at the start of a real project and it sequences `market-sizing`, `competitor-teardown`, `underserved-market-finder`, and `avatar-extraction`, then compiles all four into a single, readable report — not four separate outputs the founder has to mentally assemble. This is the entry point for Stage S1; run this first, not the individual research skills piecemeal.

**Follows `shared/references/output-conventions.md`: writes into the brand's single consolidated `hub.html` (Research section) — never its own separate page — built progressively so there's something to look at while research is still running, and every page passes through `impeccable` before being called done.**

## Stage
This skill belongs to Stage S1: Research

## When to Use
- **Start here** for any new idea or pivot — this is the front door to the whole pack, before touching any individual research skill
- The founder wants one document to read, not five chat outputs to track
- Preparing something to show a co-founder, investor, or partner
- A pivot changed the market enough that the old research is stale and a fresh full pass is needed

## Input Schema
```
{
  brand_or_business: string       # required for the project folder name — ask if not already known from context
  idea_or_pivot: string           # what's being researched — the offer/product/service
  target_segment: string?         # if already narrowed, otherwise the skill helps find it
  geography: string?              # default: United States
  known_competitors: string[]?    # if the founder already knows some
}
```

## Workflow

### Step 1: Universal Intake
Same principle as `funnel-builder-orchestrator`: scan the conversation for what's already been said, ask only for genuine gaps, in one combined question — never a checklist of five separate questions. The minimum needed to start: what the offer/idea actually is, and roughly who it's for.

### Step 2: Confirm the Report Scope
Tell the user what will be built before building it:
> "I'll research [idea] and put together one report covering market size and growth, the competitive landscape, your target buyer, and where the real opportunity is — then give you a clear go/pivot/kill read. This takes a few minutes. Want me to go?"

Don't wait for elaborate confirmation — a simple "yes"/"go"/"do it" is enough, same as the funnel orchestrator's approval gate.

### Step 3: Set Up the Brand Folder and the Shared Hub Skeleton
Confirm the brand/business name if it isn't already clear from context — never default to the offer name. The root folder is the brand name alone, exactly as the user writes it (e.g. `SmartBuzzAI`, not slugified). **Check whether `[BrandName]/hub.html` already exists first** — if it does (from a prior roadmap or funnel-map run), read `hub-data.json` and add to it rather than creating a new folder or a competing page.

If no hub exists yet, create `[BrandName]/` with:
- `hub-data.json` — structured data for all 7 hub sections (Dashboard, Fundamentals, Research, Audience & Positioning, Roadmap, Funnel Map, Decisions Log) — this skill fills in Dashboard, Fundamentals, and Research; the other sections stay marked "not started yet" until `roadmap-visualizer`/`funnel-map-visualizer` run
- `hub.html` — rendered immediately from `hub-data.json`, with the Research section marked "researching..." and everything not yet started clearly labeled as such
- `brief.md` — written once research is compiled (Step 5)

Tell the user the file path right away: "I've started `[BrandName]/hub.html` — open it now, I'll fill in Research as each piece finishes." This is the fix for the single biggest failure mode found in testing: don't make the founder wait through a silent multi-minute run and then dump a wall of text — give them something to watch fill in.

### Step 4: Run the Component Skills in Sequence, Updating the Hub After Each One
Run each in order, feeding each one's relevant output into the next where it helps (e.g. the target segment found in Step 4c narrows the market sizing in Step 4a if it wasn't already run):

1. `market-sizing` — TAM/SAM/SOM and growth rate for the category → write into the Research section of `hub-data.json`, regenerate `hub.html`
2. `competitor-teardown` — the real competitive field, pricing, positioning, weaknesses → same
3. `underserved-market-finder` — whether there's a specific underserved niche within the category worth targeting → same
4. `avatar-extraction` — pulled forward from S2, run here too so the report includes a real target buyer, not just a market description → writes into the Audience & Positioning section, not Research

Each regeneration is a full re-render of `hub.html` from `hub-data.json`, never a hand-patched fragment — this is what keeps the hub internally consistent. Do not present each skill's raw output separately in chat as you go — the page is where progress is visible; chat gets a brief one-line update per completed section ("✓ Market sizing done — see the page").

### Step 5: Compile One Report and Update the Dashboard
Synthesize the four research outputs into the Research and Audience & Positioning sections of `hub-data.json`, regenerate `hub.html`, and write `brief.md` as a portable markdown copy of the Research section. This is not a copy-paste of four sections — write actual connective analysis: does the market size support the pricing implied by the competitive teardown? Does the underserved niche match who the avatar actually is? Contradictions between the four inputs are the most valuable thing this step can surface — call them out explicitly, don't smooth them over. Update the **Dashboard** section too: project stage is now "research complete," and append the go/pivot/kill call to the Decisions Log with a timestamp.

### Step 6: Give a Clear Recommendation
End with an explicit go/pivot/kill call, not just "here's the data, you decide." Base it on:
- **Go:** Market is real and growing, a genuine gap exists, a specific buyer is identifiable
- **Pivot:** Market or competition is fine, but the specific angle/segment needs to change
- **Kill:** Market is too small/declining, or genuinely saturated with no real gap

### Step 7: Run `impeccable` Before Calling the Hub Done
Before the final regeneration of `hub.html`, load and apply the `impeccable` skill (fall back to `taste-skill` if unavailable) to actually design the page — real typography, layout, and visual hierarchy, not just functional markup. This applies every time `hub.html` is regenerated, not only on first creation.

### Step 8: Self-Validation
- [ ] The brand folder and skeleton `hub.html` were created (or the existing hub reused) and the path given to the user *before* the first component skill ran, not after
- [ ] All four component skills actually ran (not skipped or assumed)
- [ ] `hub.html` was regenerated after each component finished, not just once at the end
- [ ] The Research section reads as ONE document with connective analysis, not four pasted sections
- [ ] Contradictions between findings are named, not glossed over
- [ ] A clear go/pivot/kill recommendation is given, not left open-ended, and logged to the Decisions Log
- [ ] `impeccable` (or `taste-skill`) was applied before the final save
- [ ] Next steps point to the correct next pack stage (S2-Audience & Positioning is mostly already done via avatar-extraction; point to `offer-extraction` and `funnel-select` next)

## Output Schema
```
{
  brand_folder: string
  hub_html_path: string
  brief_path: string
  idea: string
  market: { tam, sam, som, growth_rate, verdict }
  competition: { field, table_stakes, whitespace }
  underserved_niche: string | null
  avatar: object
  contradictions_found: string[]
  recommendation: string        # "go" | "pivot" | "kill"
  recommendation_reasoning: string
}
```

## Output Format

Chat progress updates (one line per completed section, while `report.html` fills in):
```
✓ Market sizing done — see the page
✓ Competitor teardown done — see the page
✓ Underserved niche check done — see the page
✓ Avatar built — see the page
```

Final chat message once compiled:
```
## Research Report Ready

**[Idea Name] Research** — added to [BrandName]/hub.html

Open the hub in your browser (double-click the file, or drag it into a tab)
and jump to the Research section. A portable copy of just the research is
also saved at [BrandName]/brief.md.

Recommendation: **[GO / PIVOT / KILL]**
```

Research section content structure (written into `hub.html`'s Research section, not a separate document):
```markdown
## Research

### Executive Summary
[3-4 sentences: what this is, the headline market finding, the headline competitive finding, and the bottom-line recommendation]

### Market Overview
[TAM/SAM/SOM and growth rate from market-sizing, with sources]

### Competitive Landscape
[Condensed competitor-teardown table and whitespace finding]

### The Opportunity
[Where underserved-market-finder's niche intersects with the avatar (see Audience & Positioning section) and the competitive whitespace — this is the synthesis, not a restatement]

### Contradictions & Open Questions
[Anything the four research streams disagreed on or left unclear — named explicitly]

### Recommendation: GO / PIVOT / KILL
[The call, with the reasoning tied directly back to the data above]
```

The avatar itself is written into the hub's separate **Audience & Positioning** section, not Research — keep them visually distinct even though both come from this same skill run.

## Error Handling
- **User wants to skip a component (e.g. "I already know my competitors"):** Accept what they provide, still run the skill to fill gaps and verify, rather than skipping entirely — their knowledge may be outdated or incomplete.
- **A component skill can't find real data (e.g. market-sizing has no source for a niche category):** Report the gap honestly in that section rather than silently omitting it or inventing a number.
- **Contradictory findings between components:** Surface explicitly in the report — this is a feature of running research as one report, not a bug to hide.
- **Idea is too vague to research:** Stop and ask for a specific offer/product description before running any component skill — vague input produces a report that looks thorough but says nothing.

## Examples

**Example 1:**
User: "Research this idea before I build anything: AI compliance review service for small accounting firms."
→ Confirms scope in one message, gets a go
→ Runs market-sizing (finds real TAM/growth data on AI governance services), competitor-teardown (finds the enterprise-vs-DIY-template gap), underserved-market-finder (confirms small/solo firms specifically are underserved), avatar-extraction (builds a real buyer)
→ Compiles one report noting the market is real and growing, competition has a genuine gap at the small-business tier, and gives a GO recommendation
→ Points to `offer-extraction` as the next step

**Example 2:**
User: "I want the full research on [idea] but I already talked to 10 potential customers."
→ Incorporates the interview data directly into the avatar-extraction step instead of building a hypothesis avatar
→ Still runs market-sizing and competitor-teardown fresh, since customer interviews don't substitute for market/competitive data

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `shared/references/output-conventions.md`

## Flywheel Connections
### Feeds Into
- offer-extraction (S2-Audience & Positioning) — the report's market/audience findings feed directly into sharpening the offer
- funnel-select (S3-Funnel-Build) — once the offer is set, the report's audience/price findings inform funnel type
- prd-writer (S5-Planning) — the report is real input for what the PRD should assume about market and users

### Fed By
- Nothing — this is the entry point of the whole pack for a new idea

### Feedback Loop
- If a project's real-world results (signups, conversion, churn) later contradict this report's findings (e.g. the market was smaller than estimated, or the avatar was wrong), re-run this skill with the corrected reality before making the next big decision on the same project.

```yaml
chain_metadata:
  skill_slug: "research-report-builder"
  stage: "research"
  timestamp: string
  suggested_next:
    - "offer-extraction"
    - "funnel-select"
```
