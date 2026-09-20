# v5 Architecture

## Problem v5 solves

The previous design treated a collection of specialist skills as if the collection itself were a workflow. That caused several failure modes:

1. category order was mistaken for execution order;
2. new edge cases caused stage reshuffles;
3. funnel work was promoted into a universal lifecycle step;
4. skills duplicated routing logic and embedded stale catalog copies;
5. multiple skills knew how to mutate the founder hub;
6. research produced premature strategic verdicts;
7. users were asked questions that the system could have drafted from evidence;
8. output conventions leaked into unrelated specialist skills.

v5 separates **orchestration, state, rendering, and specialist execution**.

## Four layers

### Layer A — Orchestration

`project-orchestrator`

Owns sequence, branching, blocking questions, handoffs, and lifecycle status.

### Layer B — State

`project-state-manager`

Owns `project.json`, assumptions, decisions, evidence, provenance, and updates.

No specialist writes arbitrary project state directly.

### Layer C — Presentation

`hub-renderer`

Reads state and generates `hub.html`.

The renderer has no authority to invent project facts.

### Layer D — Specialists

Research, strategy, planning, engineering, funnel, copy, testing, deployment, operations, growth, and meta skills.

Specialists accept scoped inputs and return scoped structured outputs. They do not decide the entire project journey.

## Lifecycle model

1. Understand
2. Discover
3. Define
4. Plan
5. Execute
6. Verify
7. Launch
8. Operate & Grow

The phases are a mental model, not a forced wizard.

## The highway rule

The orchestrator should prefer forward motion.

- Infer from existing evidence.
- Produce a useful draft.
- Mark assumptions visibly.
- Ask only if the missing answer changes the next meaningful action.
- Ask one compact question, not a form.
- A user correction updates state and re-routes downstream work.
- Reversible decisions do not deserve interrogation.
- Irreversible, expensive, security-sensitive, legal, or destructive decisions deserve an explicit gate.

## Conditional routing examples

### New SaaS
Research market/users → positioning → requirements/MVP → architecture/stack → build → verify → launch → analytics/operations.

### Existing app feature
Read current product/code → clarify outcome/acceptance criteria → scope → build → verify → deploy. Skip market sizing and funnel work.

### Brand/company website
Audit current brand/site → audience/positioning → IA/customer journey → copy/design → build site → accessibility/performance verification → launch.

### Service offer
Market/audience research → offer/differentiation → delivery model → optional funnel/copy → site/assets → launch/measure.

### Security fix
Inspect → reproduce → patch → regression/security verification → deploy → record decision. No marketing, TAM, or persona séance required.

## Gates

Hard gates exist only where they protect the user:

- destructive changes;
- production deployment;
- external spending;
- security-sensitive actions;
- legal/compliance claims;
- publishing/send actions;
- materially irreversible architecture decisions.

Everything else should bias toward a reversible draft.
