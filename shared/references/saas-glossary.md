# SaaS / App-Building Glossary

Shared terminology reference for all skills in this pack.

- **PRD** — Product Requirements Doc. What the app must do, for whom, and why. Written before any code.
- **ADR** — Architecture Decision Record. A short doc capturing one technical choice, the alternatives considered, and why.
- **MVP** — Minimum Viable Product. The smallest version of the app that is still real and testable by an actual user.
- **Golden path** — The main sequence of steps a typical user takes to get value from the app (e.g. signup → create first item → see result).
- **Edge case** — An input or situation outside the golden path that the app must still handle without breaking (empty input, network failure, expired session).
- **Activation** — The point a new signup reaches real value for the first time (not just "created an account").
- **Churn** — A paying or active user who stops using/paying for the app.
- **Tenant** — One customer organization's data/context in a multi-customer SaaS app. Tenant isolation = customer A can never see customer B's data.
- **Wrangler** — Cloudflare's CLI for deploying and managing Workers/Pages/D1/R2.
- **D1** — Cloudflare's serverless SQL database product.
- **Regression** — A previously-working feature that breaks again after a later change.
- **Scope creep** — A task quietly growing beyond what was originally planned, usually causing partial, broken results.
- **Flywheel connection** — In this pack, the note on each skill showing which skill's output should logically feed into which other skill next.
