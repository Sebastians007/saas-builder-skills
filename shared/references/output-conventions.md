# Output Conventions

## Rule 1: Local files only, never a published Artifact

Every visual/document output this pack produces is a **real local file inside the brand's project folder** — plain HTML the user opens directly in their browser. Never use the Artifact tool (claude.ai published pages). No hosted link. Everything lives on the user's own machine.

## Rule 2: The root folder is the brand name, flat, no nesting

One business = one root folder, named exactly as the user writes it (e.g. `SmartBuzzAI`, not slugified, never with an offer/service name appended — see the CrowdStrike test: a company isn't named "CrowdStrike-Falcon-EDR" on disk).

For a project this size, **keep every file flat in that root folder** — no `research/`, `brief/`, `data/` subfolders. A handful of files doesn't need nested directories:

```
SmartBuzzAI/
  hub.html          ← the one consolidated planning/status page (Rule 3)
  hub-data.json     ← structured data backing hub.html, regenerated from on every update
  brief.md           ← portable markdown copy of the hub's content
  [site files]       ← the actual product/website, if this business has built one (index.html, etc. — kept separate from the hub, see Rule 3)
```

Reuse the existing brand folder if one already exists; never create a second root folder for the same business.

## Rule 3: One consolidated hub page, not one page per skill

`research-report-builder`, `roadmap-visualizer`, and `funnel-map-visualizer` do **not** each create their own HTML file. They all write into the same `hub.html` — one page, sidebar navigation, each skill owning its own section. This replaces the earlier (wrong) approach of a separate `report.html`, `roadmap.html`, `funnel-map.html` per skill.

**Hub structure, in this order:**

1. **Dashboard** (always first/top) — project status at a glance: what stage it's at, most recent decisions, any open questions, quick context summary. This is what the founder should see the instant the page opens — not buried below research.
2. **Fundamentals** — the brand/offer in one paragraph: what it is, who it's for, current direction (updated on a pivot)
3. **Research** — from `research-report-builder`: market, competition, opportunity, recommendation
4. **Audience & Positioning** — avatar, offer, awareness stage
5. **Roadmap** — from `roadmap-visualizer`: phases/features board
6. **Funnel Map** — from `funnel-map-visualizer`: the funnel visualization
7. **Decisions Log** — a running, timestamped list of key decisions made across every session on this project. Every skill that makes or records a real decision appends one line here.

Sidebar is sticky, lists all 7 sections, jumps to each via anchor links. Each skill, when it runs:
- Reads the existing `hub.html`/`hub-data.json` if the brand folder already has one
- Updates only its own section's data in `hub-data.json`
- Regenerates the whole `hub.html` from `hub-data.json` (simplest correct approach — always a full re-render from data, never a hand-patched fragment)
- Appends a line to the Decisions Log if a real decision was made this run

The **actual product/website** (landing pages, the real app) is a separate set of files, not a hub section — the hub is where the founder tracks the project, the site is what customers see.

## Rule 4: Every HTML page goes through `impeccable`

Before finalizing **any** HTML output this pack produces — the hub page or the real product/website — invoke the `impeccable` skill (fall back to `taste-skill` if unavailable) to actually design the page, not just lay out functional HTML. This applies to `research-report-builder`, `roadmap-visualizer`, `funnel-map-visualizer`, `funnel-builder-orchestrator`, and every other page-generating skill in the pack.

## Why all of this

- Flat + one hub = a founder with one business has exactly one file to remember: `SmartBuzzAI/hub.html`
- Dashboard-first = the most current, most important information is what's visible on open, not buried under research nobody re-reads
- One file, regenerated from data = no risk of the hub, the roadmap, and the funnel map drifting out of sync with each other
- `impeccable` on everything = the pack's output actually looks like something a founder would show someone, not a functional-but-generic scaffold

## Skills using this pattern

`research-report-builder`, `roadmap-visualizer`, `funnel-map-visualizer` write into the shared hub. `funnel-builder-orchestrator` and the rest of S3-Funnel-Build's asset generators produce the separate real product/website files, and also apply Rule 4 (`impeccable`) to everything they generate.
