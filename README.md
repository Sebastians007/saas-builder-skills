# saas-builder-skills

**Turn any AI into your app-building and growth team.**

83 AI-powered skills across 10 stages with a closed-loop flywheel. Research the idea, plan it properly, build one feature at a time, actually verify it works, deploy it, run it, build the funnel that sells it, write the copy, and grow it — with Claude Code or any AI agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-83-brightgreen)](skills/)

Works with: **Claude Code** · **ChatGPT** · **Gemini CLI** · **Cursor** · **Windsurf** · **any AI that reads text**

## Why this exists

Prompting an AI with "build me a SaaS app" produces broken, incoherent results — there's no spec, no plan, and nothing gets verified before it's called done. This pack forces the missing structure: a real PRD before code, one feature at a time, a real browser check (via the `superpowers-chrome` plugin) before anything is called "working," and a real tracked funnel instead of guessing what's converting.

Structurally adapted from three MIT-licensed source repos, fully rewritten and retargeted for a non-technical SaaS founder building on Claude Code + Cloudflare:
- [Affitor/affiliate-skills](https://github.com/Affitor/affiliate-skills) — the original 8-stage flywheel format (S1-S8)
- [ominou5/funnel-architect-plugin](https://github.com/ominou5/funnel-architect-plugin) — S9-Funnels (13 funnel types + router + copy skill)
- [rfstudioco/agentic_growth_team](https://github.com/rfstudioco/agentic_growth_team) — 8 growth-ops additions to S7 (dashboards, attribution, churn, activation)
- [realkimbarrett/advertising-skills](https://github.com/realkimbarrett/advertising-skills) — S10-Copywriting (direct-response frameworks)

## Repo structure

- `skills/{stage}/{skill-name}/SKILL.md` — the 83 skill definitions
- `shared/references/` — glossary + flywheel connection map
- `registry.json` — machine-readable skill catalog
- `.claude-plugin/` — Claude Code plugin manifest

### Install (Claude Code)

```bash
claude plugin marketplace add Sebastians007/saas-builder-skills
claude plugin install saas-builder-skills@saas-builder-skills
```

Or drop the `skills/*/*/` folders directly into `~/.claude/skills/` for a flat, no-plugin install.

## The 10-stage flywheel

```
S1 Research → S2 Planning → S3 Building → S4 Testing → S5 Deployment
    ▲                                                          │
    │                                                          ▼
S10 Copywriting ← S9 Funnels ← S8 Meta ← S7 Growth ← S6 Operations
```

### S1 — Research (10 skills)
tech-stack-finder · pricing-model-calculator · competitor-teardown · feature-differentiator · underserved-market-finder · saas-idea-validator · unique-value-prop-audit · launch-directory-submitter · user-acquisition-analyzer · trending-tech-scout

### S2 — Planning (7 skills)
**The anchor stage.** `prd-writer` and `mvp-feature-slicer` are the two skills that fix the "6 months, no working app" failure mode — they force real clarity before any code gets written.

prd-writer · architecture-decision-writer · tech-debt-detector · defensibility-calculator · user-story-writer · feature-roadmap-architect · mvp-feature-slicer

### S3 — Building (7 skills)
feature-task-breakdown · technical-spike-brief · data-model-diagrammer · api-endpoint-builder · ui-component-builder · auth-flow-builder · onboarding-flow-builder

### S4 — Testing (8 skills)
**The safety net.** `browser-verifier` uses the `superpowers-chrome` Claude Code plugin to actually load the app in a real browser and check it — not just assume the code is correct because it compiles.

test-case-generator · edge-case-hunter · regression-test-builder · browser-verifier · load-test-builder · accessibility-auditor · security-review-lite · user-acceptance-test-planner

### S5 — Deployment (4 skills)
Built for **Cloudflare** (Workers/Pages/D1/R2 + wrangler), not Vercel.

cloudflare-deployer · ci-cd-pipeline-builder · domain-dns-setup · env-secrets-manager

### S6 — Operations (5 skills)
Scoped for a solo founder or tiny team — no enterprise over-engineering.

monitoring-alerting-setup · backup-recovery-builder · multi-tenant-manager · incident-runbook-writer · seed-data-generator

### S7 — Growth (13 skills)
Post-launch only. All data-driven skills here point at **PostHog** (free tier, open-source) as the analytics backbone — no paid BI tools. `growth-dashboard-builder` is the flagship: one central place to see acquisition → activation → retention → revenue → referral, instead of guessing.

ab-test-generator · signup-conversion-tracker · in-app-nav-optimizer · app-performance-report · marketing-site-seo-audit · **growth-dashboard-builder** · revenue-dashboard-builder · attribution-mapper · checkout-funnel-auditor · pricing-page-optimizer · trial-to-paid-converter · cohort-churn-analyzer · aha-moment-mapper

### S8 — Meta (6 skills)
Cross-cutting utilities that operate on the pack itself.

category-designer · compliance-checker · create-skill · funnel-planner · self-improver · skill-finder

### S9 — Funnels (15 skills)
Real funnel *types* with page templates included, plus a router and a copy skill. Adapted from funnel-architect-plugin.

application-funnel · challenge-funnel · ecommerce-funnel · evergreen-webinar-funnel · group-funnel · high-ticket-funnel · membership-funnel · optin-funnel · product-launch-funnel · saas-funnel · tripwire-funnel · vsl-funnel · webinar-funnel · funnel-select · funnel-copy

### S10 — Copywriting (8 skills)
Direct-response copywriting frameworks, reframed for SaaS landing pages, onboarding, and pricing — not generic ad-agency copy.

avatar-extraction · offer-extraction · headline-matrix · objection-crusher · schwartz-awareness-mapper · ad-angle-multiplier · full-funnel-campaign-orchestrator · generic-language-killer

## Try it now

Not sure which skill to use? Just describe what you're doing — `skill-finder` (S8-Meta) will route you to the right 1-3 skills.

## License

MIT. See [LICENSE](LICENSE). Structurally inspired by the four repos listed above (all MIT) — content here is original, rewritten for a different context (non-technical SaaS founder, Claude Code, Cloudflare, PostHog).
