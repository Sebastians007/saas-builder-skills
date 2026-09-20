# Output Conventions

## Rule: Local files only, never a published Artifact

Every visual/document output this pack produces (research reports, roadmap boards, funnel maps, generated pages, briefs) is written as a **real local file inside the project folder** — plain HTML the user opens directly in their browser, or markdown/JSON alongside it.

**Never use the Artifact tool (claude.ai published pages) for pack output.** No `claude.ai/artifact/...` links. Everything lives on the user's own machine, in a folder they can see, back up, move, and open without a hosted link.

## Why

- The user owns the file outright — no dependency on a hosted claude.ai link staying available
- Works fully offline once generated
- Fits a local, file-based project folder workflow instead of a browser-tab workflow
- No ambiguity about who can view it or whether sharing permissions matter

## The pattern every "visual" skill follows

1. **Create a project folder** the first time a skill in a project runs (see naming convention below) — mirrors the pattern `funnel-builder-orchestrator` already established.
2. **Write real files into it** — a self-contained `.html` file (inline CSS/JS, no external published dependencies) for anything meant to be looked at, plus a `.json` or `.md` data file alongside it when the page needs to be regenerated from structured data (e.g. a roadmap board's card statuses).
3. **Tell the user the exact file path** and that they can open it directly in a browser (double-click, or drag into a browser tab). Never say "here's your link" — say "here's the file, open it in your browser."
4. **Updates are re-writes, not live browser interactivity.** If the user says "mark X as done," the skill edits the underlying data file and regenerates the HTML — it does not rely on client-side JavaScript writing back to a server, since there is no server. The page can still have visual polish and light client-side interactivity (tabs, filters, hover states) — it just doesn't persist state back to Claude on its own; Claude is the one who edits the file when asked.
5. **Progressive builds are real file re-writes.** For a report built in stages (e.g. `research-report-builder`), write the file early with placeholder/pending sections, then re-write the same file as each section completes — the user can refresh the open browser tab to see progress, same spirit as a live page, without ever publishing one.

## Project folder naming convention

**The root folder is the brand/business name — nothing else.** Exactly as the user would write it (proper case, e.g. `SmartBuzzAI`, not lowercased or slugified). Never append the offer, service, or project name to the root folder — the same way a company isn't named "CrowdStrike-Falcon-EDR" on disk, one business is one root folder no matter how many offers, services, or projects it has.

The offer/service/project name is a **detail that lives inside** the brand folder — as a subfolder named for what the output actually is, not for the specific offer:

```
SmartBuzzAI/
  research/          ← research-report-builder output
    report.html
    brief/research-report.md
    data/
  funnel/             ← funnel-builder-orchestrator output
    ...
  roadmap/            ← roadmap-visualizer output
    ...
```

**If the brand/business name isn't already known from context, ask for it before creating anything** — don't default to the offer name and don't guess. Reuse the existing brand folder if one already exists for this business; never create a second root folder for the same brand.

If a business runs the same *type* of project more than once (e.g. a second research pass after a pivot), reuse the same subfolder and update it (per the re-write convention above) rather than creating `research-2/` — the file's own content reflects what's current. Only create a dated or numbered variant if the user explicitly wants old and new kept side by side.

Standard subfolders inside each `[type]/` folder:
- `brief/` — the compiled report/brief as markdown, and any PDF export
- `data/` — JSON files backing any page that needs regeneration from structured state
- files at the `[type]/` root — the actual HTML page(s) the user opens

## Skills using this pattern

`research-report-builder`, `roadmap-visualizer`, `funnel-map-visualizer`, `funnel-builder-orchestrator` and the rest of S3-Funnel-Build's asset generators.
