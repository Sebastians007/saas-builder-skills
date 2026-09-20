# Master Flywheel Connection Map

The full 8-stage loop this pack is built around. Each stage's output should hand off to the next — the point is to stop vague, one-shot "build me an app" prompts from producing broken results, by forcing a real pipeline.

```
S1 Research  ──▶  S2 Planning  ──▶  S3 Building  ──▶  S4 Testing
    ▲                                                       │
    │                                                       ▼
S8 Meta   ◀──  S7 Growth  ◀──  S6 Operations  ◀──  S5 Deployment
```

## Stage S1 — Research
tech-stack-finder, pricing-model-calculator, competitor-teardown, feature-differentiator, underserved-market-finder, saas-idea-validator, unique-value-prop-audit, launch-directory-submitter, user-acquisition-analyzer, trending-tech-scout

## Stage S2 — Planning
prd-writer, architecture-decision-writer, tech-debt-detector, defensibility-calculator, user-story-writer, feature-roadmap-architect, mvp-feature-slicer

## Stage S3 — Building
feature-task-breakdown, technical-spike-brief, data-model-diagrammer, api-endpoint-builder, ui-component-builder, auth-flow-builder, onboarding-flow-builder

## Stage S4 — Testing
test-case-generator, edge-case-hunter, regression-test-builder, browser-verifier, load-test-builder, accessibility-auditor, security-review-lite, user-acceptance-test-planner

## Stage S5 — Deployment
cloudflare-deployer, ci-cd-pipeline-builder, domain-dns-setup, env-secrets-manager

## Stage S6 — Operations
monitoring-alerting-setup, backup-recovery-builder, multi-tenant-manager, incident-runbook-writer, seed-data-generator

## Stage S7 — Growth
ab-test-generator, signup-conversion-tracker, in-app-nav-optimizer, app-performance-report, marketing-site-seo-audit

## Stage S8 — Meta
category-designer, compliance-checker, create-skill, funnel-planner, self-improver, skill-finder

## The core rule

Never jump straight from "I have an idea" (S1) to code (S3). `prd-writer` and `mvp-feature-slicer` (S2) exist specifically to force clarity first — that gap is the single biggest cause of AI-built apps that look done but don't actually work.
