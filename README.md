# saas-builder-skills

**Turn any AI into your app-building and growth team.**

87 AI-powered skills across 11 stages, **ordered to match how you actually build** — not filed alphabetically by category. Research the idea as one coherent report (market size, competition, audience — not five disconnected outputs), define the real person you're building for, build the actual funnel so you have something to look at, then plan, build, test, deploy, and grow it — with Claude Code or any AI agent.

**Every visual output is a real local file, never a published Artifact.** Research, roadmap, and funnel-map skills all write into one consolidated `hub.html` per brand — sidebar nav, Dashboard first, flat in a folder named for the brand alone (e.g. `SmartBuzzAI/hub.html`, not nested, not slugified). Every page passes through `impeccable` before it's called done. See `shared/references/output-conventions.md`.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-87-brightgreen)](skills/)

Works with: **Claude Code** · **ChatGPT** · **Gemini CLI** · **Cursor** · **Windsurf** · **any AI that reads text**

## Why this exists

Prompting an AI with "build me a SaaS app" produces broken, incoherent results — there's no spec, no plan, and nothing gets verified before it's called done. This pack forces the missing structure: a real PRD before code, one feature at a time, a real browser check (via the `superpowers-chrome` plugin) before anything is called "working," and a real tracked funnel instead of guessing what's converting.

**v4.0.0 fixed a real problem found in production use:** the original stage numbers were filed by category (Research, Planning, Building... Copywriting, Asset Generation last), not by when you actually need them. Running the pack end-to-end on a real project surfaced two concrete failures — audience definition was buried at stage 10 when it's needed right after research, and nothing produced a visual asset until the very end. The stages below are reordered to fix both.

Structurally adapted from four MIT-licensed source repos, fully rewritten and retargeted for a non-technical SaaS founder building on Claude Code + Cloudflare:
- [Affitor/affiliate-skills](https://github.com/Affitor/affiliate-skills) — the original flywheel format
- [ominou5/funnel-architect-plugin](https://github.com/ominou5/funnel-architect-plugin) — funnel routing/visualization skills
- [rfstudioco/agentic_growth_team](https://github.com/rfstudioco/agentic_growth_team) — growth-ops additions (dashboards, attribution, churn, activation)
- [realkimbarrett/advertising-skills](https://github.com/realkimbarrett/advertising-skills) — direct-response copywriting frameworks

## Repo structure

- `skills/{stage}/{skill-name}/SKILL.md` — the 87 skill definitions
- `shared/references/` — glossary + flywheel connection map
- `registry.json` — machine-readable skill catalog
- `.claude-plugin/` — Claude Code plugin manifest

Note: `skills/funnel-build/` includes 13 proprietary skills (funnel-builder-orchestrator and the individual asset generators) — owned outright, not third-party or MIT-adapted like the rest of the pack. See their `license: proprietary` frontmatter.

### Install (Claude Code)

```bash
claude plugin marketplace add Sebastians007/saas-builder-skills
claude plugin install saas-builder-skills@saas-builder-skills
```

Or drop the `skills/*/*/` folders directly into `~/.claude/skills/` for a flat, no-plugin install.

## The 11-stage flywheel

```
S1 Research → S2 Audience & Positioning → S3 Funnel Build → S4 Copywriting → S5 Planning
    ▲                                                                                │
    │                                                                                ▼
S11 Meta ← S10 Growth ← S9 Operations ← S8 Deployment ← S7 Testing ← S6 Building ◄──┘
```

### S1 — Research (12 skills)
**`research-report-builder` is the entry point — start here for any new idea or pivot.** It orchestrates `market-sizing` (new — real TAM/SAM/SOM and growth rate, sourced, not invented), `competitor-teardown`, `underserved-market-finder`, and `avatar-extraction` into one compiled report instead of leaving you to stitch together separate skill outputs yourself.

research-report-builder · market-sizing · tech-stack-finder · pricing-model-calculator · competitor-teardown · feature-differentiator · underserved-market-finder · saas-idea-validator · unique-value-prop-audit · launch-directory-submitter · user-acquisition-analyzer · trending-tech-scout

### S2 — Audience & Positioning (4 skills)
**Moved here from the old "Copywriting" stage.** You need to know who you're building for right after research, not eight stages later. `avatar-extraction` builds one real buyer, not a demographic; `copy-framework-selector` picks the right classic framework (AIDA/PAS/BAB/PASTOR/StoryBrand/QUEST) based on their awareness stage.

avatar-extraction · offer-extraction · schwartz-awareness-mapper · copy-framework-selector

### S3 — Funnel Build (15 skills)
**The visual checkpoint.** Once audience and positioning are known, pick the funnel type and build the actual assets — a real page you can look at — before sinking time into deep planning. `funnel-builder-orchestrator` runs the whole build end-to-end (landing page + emails + thank-you page + more) in one pass; `funnel-select`/`funnel-map-visualizer` handle routing and visualization without triggering a full build.

funnel-select · funnel-map-visualizer · **funnel-builder-orchestrator** · lead-magnet-creator · landing-page-generator · email-sequence-generator · thank-you-page-generator · webinar-script-generator · vsl-script-generator · social-content-pack · headline-hook-generator · upsell-page-generator · quiz-flow-generator · challenge-content-generator · affiliate-promo-kit

### S4 — Copywriting (4 skills)
Refinement on copy that already has a real draft behind it from S3 — not where copy starts from scratch.

objection-crusher · ad-angle-multiplier · full-funnel-campaign-orchestrator · generic-language-killer

### S5 — Planning (8 skills)
**The anchor stage for the actual product build.** `prd-writer` and `mvp-feature-slicer` are the two skills that fix the "6 months, no working app" failure mode — they force real clarity before any code gets written. `roadmap-visualizer` turns the plan into a live tracked board instead of a markdown file nobody reopens.

prd-writer · architecture-decision-writer · tech-debt-detector · defensibility-calculator · user-story-writer · feature-roadmap-architect · mvp-feature-slicer · roadmap-visualizer

### S6 — Building (7 skills)
feature-task-breakdown · technical-spike-brief · data-model-diagrammer · api-endpoint-builder · ui-component-builder · auth-flow-builder · onboarding-flow-builder

### S7 — Testing (8 skills)
**The safety net.** `browser-verifier` uses the `superpowers-chrome` Claude Code plugin to actually load the app in a real browser and check it — not just assume the code is correct because it compiles.

test-case-generator · edge-case-hunter · regression-test-builder · browser-verifier · load-test-builder · accessibility-auditor · security-review-lite · user-acceptance-test-planner

### S8 — Deployment (4 skills)
Built for **Cloudflare** (Workers/Pages/D1/R2 + wrangler), not Vercel.

cloudflare-deployer · ci-cd-pipeline-builder · domain-dns-setup · env-secrets-manager

### S9 — Operations (6 skills)
Scoped for a solo founder or tiny team — no enterprise over-engineering. `twelve-factor-auditor` checks the app against the decades-old Twelve-Factor App standard (config, statelessness, dev/prod parity) before/after a first production deploy.

monitoring-alerting-setup · backup-recovery-builder · multi-tenant-manager · incident-runbook-writer · seed-data-generator · twelve-factor-auditor

### S10 — Growth (13 skills)
Post-launch only. All data-driven skills here point at **PostHog** (free tier, open-source) as the analytics backbone — no paid BI tools. `growth-dashboard-builder` is the flagship: one central place to see acquisition → activation → retention → revenue → referral, instead of guessing.

ab-test-generator · signup-conversion-tracker · in-app-nav-optimizer · app-performance-report · marketing-site-seo-audit · **growth-dashboard-builder** · revenue-dashboard-builder · attribution-mapper · checkout-funnel-auditor · pricing-page-optimizer · trial-to-paid-converter · cohort-churn-analyzer · aha-moment-mapper

### S11 — Meta (6 skills)
Cross-cutting utilities that operate on the pack itself.

category-designer · compliance-checker · create-skill · funnel-planner · self-improver · skill-finder

## Try it now

Not sure which skill to use? Just describe what you're doing — `skill-finder` (S11-Meta) will route you to the right 1-3 skills.

## License

MIT. See [LICENSE](LICENSE). Structurally inspired by the four repos listed above (all MIT) — content here is original, rewritten for a different context (non-technical SaaS founder, Claude Code, Cloudflare, PostHog).
