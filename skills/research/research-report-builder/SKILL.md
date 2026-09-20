---
name: research-report-builder
description: >
  Orchestrates evidence gathering for a new idea, pivot, market question, or
  strategic uncertainty. Produces sourced research patches for project.json and
  a coherent Research section in the project hub. It does not force a universal
  go/pivot/kill verdict and does not run irrelevant research for existing feature
  work.
license: MIT
version: "5.0.0"
tags: ["research", "orchestrator", "market", "evidence"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  capability: discovery
---

# Research Report Builder

## Role

This is a Discover-phase specialist called by `project-orchestrator`.

It is not the universal front door.

## First Decision: What Research Is Actually Needed?

Classify the request.

### New company/product/market or major pivot
Potentially run:
- market-sizing;
- competitor-teardown;
- underserved-market-finder;
- trend research;
- user/buyer research.

### Existing feature
Usually skip TAM/SAM/SOM and generic competitor research. Inspect:
- current users;
- usage/analytics;
- feedback;
- current product/code;
- comparable feature patterns only if relevant.

### Website/brand redesign
Research:
- current site;
- audience;
- competitor messaging/design;
- analytics/search behavior if available.

### Service/offer
Research:
- market/category;
- competing offers/pricing;
- buyer pain/jobs;
- trust/evidence expectations;
- channel realities.

## Evidence Standard

For external claims:
- use current sources;
- keep URLs/source identifiers;
- date time-sensitive evidence;
- report ranges/disagreement instead of manufacturing precision.

## Output

Return a structured project-state patch containing:
- evidence summary;
- market/trend findings if relevant;
- competitor findings if relevant;
- user/job hypotheses;
- whitespace/opportunities;
- contradictions;
- confidence;
- unresolved gaps;
- sources.

Do not ask the user to stitch raw component outputs together.

## Strategic Recommendation

Research may recommend:
- proceed to Define;
- gather more evidence;
- narrow/change segment;
- reconsider the idea.

Avoid pretending research alone can make every final business decision.

Use language like:

> Evidence currently supports testing this direction, with medium confidence. The strongest opportunity is X; the largest uncertainty is Y.

## Positioning Handoff

When competitor/user evidence supports it, include 2-3 **positioning or differentiation candidates** for the Define phase.

Do not ask the user "what makes you different?" when the research exists to help answer that question.

## State/Hub

Return the patch to `project-state-manager`.

Let `hub-renderer` update the hub. Do not hand-edit hub HTML.
