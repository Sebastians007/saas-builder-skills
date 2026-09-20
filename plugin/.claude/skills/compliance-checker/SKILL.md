---
name: compliance-checker
description: >
  Audits a SaaS app against baseline legal and data-protection requirements before real
  users or paying customers sign up, covering privacy policy, terms of service, cookie
  consent, GDPR/CCPA data-subject basics, and a WISP-style data protection posture for
  apps handling sensitive personal or financial data.
  Use this skill when the user asks "are we legally okay to launch", "do we need a privacy
  policy", "is this GDPR compliant", "check our compliance before launch", "do we need
  cookie consent", "what data protection do we need for [sensitive data type]", "am I going
  to get sued for this", or "compliance review before we open signups".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "compliance", "grc", "data-privacy", "legal"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Meta
---

# Compliance Checker

Runs a baseline GRC-style audit of a SaaS app's legal and data-protection posture before it takes on real users. This is not a substitute for a lawyer, but it applies real control-mapping discipline — the same lens a GRC analyst uses on a WISP (Written Information Security Program) review — instead of generic "get a privacy policy" startup-blog advice. It checks what data the app actually collects, what jurisdiction's rules apply, and whether the controls on paper match what the app actually does.

## Stage
This skill belongs to Stage S8: Meta

## When to Use
- Before opening public signups or taking the first paying customer
- The app collects any personal data (email, name, IP, location, payment info, health, financial, or biometric data)
- The app serves EU or California residents (GDPR/CCPA triggers) even if the founder isn't based there
- The app touches financial, health, or other "sensitive" data categories that require a written security program
- A customer, investor, or partner asks for a security/compliance questionnaire and the founder has nothing to show
- Recurring quarterly check as the app adds features that touch new data types (e.g. adding payments, adding analytics tracking)

## Input Schema
```
compliance_check_request:
  app_name: string
  app_description: string          # what it does, one paragraph
  data_collected: [string]         # e.g. ["email", "name", "IP address", "payment card (via Stripe)", "usage analytics"]
  user_locations: [string]         # known or expected, e.g. ["US", "EU", "California"]
  third_party_processors: [string] # e.g. ["Stripe", "Google Analytics", "SendGrid", "AWS"]
  current_docs: {
    privacy_policy: bool,
    terms_of_service: bool,
    cookie_banner: bool,
    dpa_with_vendors: bool
  }
  sensitive_data_flag: bool        # health, financial account numbers, SSN, biometric, children's data
```

## Workflow
### Step 1: Data Inventory
List every category of personal data the app actually touches — not what the founder thinks it collects, but what the signup flow, analytics, payment integration, and support tools actually capture. Flag anything the founder didn't mention but that's implied by the stack (e.g. Stripe implies card data flows through even if never stored; Google Analytics implies IP + device fingerprinting).

### Step 2: Jurisdiction Mapping
Determine which regimes apply based on `user_locations` and data types:
- **GDPR** (EU/EEA users) — applies if ANY user is in the EU, regardless of where the company is based
- **CCPA/CPRA** (California) — applies at lower revenue/user thresholds than founders expect; check if the app meets the "sells/shares personal information" or 100k+ consumer thresholds, but recommend baseline compliance regardless below threshold since it's cheap insurance
- **State data breach notification laws** (US, all 50 states have one) — applies once the app stores any personal data
- **Sector-specific** — HIPAA if health data, GLBA/WISP-style if financial account data, COPPA if any chance of under-13 users

### Step 3: Document Gap Check
Score against these 4 baseline documents — for each, state Present / Missing / Present-but-inadequate:
1. **Privacy Policy** — must disclose: what's collected, why, who it's shared with, retention period, user rights (access/delete/export), contact method for requests
2. **Terms of Service** — must cover: acceptable use, liability limitation, termination rights, dispute resolution, IP ownership of user content
3. **Cookie/Tracking Consent** — required if using any non-essential cookies/analytics/ad pixels for EU or California users; must allow opt-out before tracking fires, not just a "we use cookies" banner
4. **Data Processing Agreements (DPAs)** with third-party processors (Stripe, analytics tools, email providers) — required under GDPR when a processor handles EU personal data

### Step 4: Data Protection Posture (WISP-style)
For apps flagged `sensitive_data_flag: true`, run a lightweight Written Information Security Program check — this is the GRC-rigor part:
- **Access control**: is data access role-restricted, or can any employee/admin see everything?
- **Encryption**: at rest and in transit — confirm, don't assume
- **Retention policy**: is there an actual defined retention/deletion schedule, or does data live forever by default?
- **Incident response**: is there any written plan for what happens if there's a breach? (Even a 1-page runbook counts as a start — point to `incident-runbook-writer` in S6-Operations)
- **Vendor risk**: are third-party processors themselves compliant (do they have their own SOC 2 / DPA)?
- **Data minimization**: is the app collecting more than it needs? Flag any field collected "just in case"

### Step 5: Data Subject Rights Readiness
Check whether the app can actually fulfill, not just promise, these rights within a reasonable timeframe (GDPR: 30 days):
- Right to access (export their data)
- Right to deletion (actually delete, including from backups/logs where feasible)
- Right to correction
- Right to portability (machine-readable export)
If the app has no way to do any of these except manually emailing a developer, flag it as inadequate even if the privacy policy promises it — promising a right you can't operationally deliver is itself a compliance gap.

### Step 6: Self-Validation
Before presenting, silently check:
- [ ] Did I check what data is ACTUALLY collected, not just what the founder listed?
- [ ] Did I flag every third-party processor as a data-sharing relationship needing a DPA?
- [ ] Did I distinguish "have a document" from "the document is accurate to what the app does"?
- [ ] Did I check operational ability to fulfill rights, not just policy language?
- [ ] Is every finding labeled with severity (Blocker / High / Medium / Low) so the founder knows what to fix before launch vs. later?
- [ ] Did I avoid giving legal advice framed as certainty — this is a baseline gap-check, not a legal opinion?

## Output Schema
```
{
  "app_name": string,
  "jurisdictions_triggered": [string],
  "findings": [
    {
      "area": string,           // e.g. "Privacy Policy", "Cookie Consent", "Data Retention"
      "status": "present" | "missing" | "inadequate",
      "severity": "blocker" | "high" | "medium" | "low",
      "detail": string,
      "fix": string
    }
  ],
  "data_subject_rights_ready": bool,
  "sensitive_data_program_status": string | null,
  "launch_recommendation": "ready" | "fix_blockers_first" | "not_ready"
}
```

## Output Format
```markdown
# Compliance Baseline Check — <App Name>

## Jurisdictions Triggered
<list, with why>

## Data Inventory
<table: data type | source | where it goes>

## Findings

| Area | Status | Severity | Detail | Fix |
|---|---|---|---|---|
| Privacy Policy | ... | ... | ... | ... |
| Terms of Service | ... | ... | ... | ... |
| Cookie Consent | ... | ... | ... | ... |
| DPAs with Vendors | ... | ... | ... | ... |
| Data Subject Rights | ... | ... | ... | ... |
| WISP / Security Posture (if sensitive data) | ... | ... | ... | ... |

## Blockers Before Launch
<numbered list, only "blocker" severity items>

## Recommendation
**<Ready to launch / Fix blockers first / Not ready>**

## Disclaimer
This is a baseline operational gap-check, not legal advice. For sensitive data (health, financial, children's data) or before fundraising/enterprise sales, get an actual lawyer to review.
```

## Error Handling
- Founder doesn't know what data is collected: don't skip the check — walk through the signup form, analytics tools, and payment flow to infer it, then flag assumptions as "unverified, confirm."
- No user location data available: default to treating the app as globally accessible (worst case) and flag both GDPR and CCPA as potentially triggered until proven otherwise.
- Founder says "we're too small for this to matter": correct this directly — GDPR has no size floor, and state breach notification laws apply from the first record stored. Don't let severity get downgraded because of company size alone.
- Sensitive data flagged but founder has no security budget: prioritize the free/cheap controls first (access restriction, encryption defaults most cloud providers already give you, a 1-page retention policy) over expensive audits.
- Conflicting or unclear answers about third-party vendors: list every vendor mentioned anywhere in the conversation (Stripe, analytics, email tools) even if not explicitly flagged as a "processor" by the founder — non-technical founders often don't realize these count.

## Examples
**Example 1**
User: "Can I open signups on BlackTally tomorrow? We handle tax prep client data."
The skill flags `sensitive_data_flag: true` (financial + potentially SSN-adjacent data), runs the WISP-style check, finds no written retention policy and no DPA with the hosting provider, and marks these as blockers.
Outcome: launch recommendation is "fix blockers first" with a 2-item punch list before go-live.

**Example 2**
User: "Quick check — do we need a cookie banner for a US-only app using Google Analytics?"
The skill notes CCPA applies if any California users are likely (almost certain for a US-only app) and Google Analytics counts as non-essential tracking, so opt-in/opt-out consent is needed for California traffic at minimum, GDPR-style consent recommended as a cheap global default.
Outcome: cookie consent marked "missing, medium severity" with a specific fix (add a consent banner before GA fires).

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- `cloudflare-deployer` (S5-Deployment) — blockers must clear before go-live deployment
- `incident-runbook-writer` (S6-Operations) — WISP gap findings often require a written incident response plan
- `security-review-lite` (S4-Testing) — compliance findings on data handling feed into the pre-launch security pass

### Fed By
- `auth-flow-builder` (S3-Building) — auth/data collection points determine what personal data actually flows through the app
- `multi-tenant-manager` (S6-Operations) — tenant data isolation posture is an input to the WISP-style review

### Feedback Loop
Each audit's findings are logged so recurring gaps (e.g. always missing DPAs) get flagged earlier in future builds via `self-improver`, tightening the default checklist over time.

```yaml
chain_metadata:
  skill_slug: "compliance-checker"
  stage: "meta"
  timestamp: string
  suggested_next:
    - "security-review-lite"
    - "incident-runbook-writer"
```
