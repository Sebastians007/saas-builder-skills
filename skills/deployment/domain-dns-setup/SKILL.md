---
name: domain-dns-setup
description: >
  Connects a custom domain to a Cloudflare-hosted Worker or Pages app with correct DNS
  records and SSL, and flags the common gotchas before they cause downtime.
  Use this skill when the user asks about connecting a domain, fixing DNS,
  or says
  "connect my domain to cloudflare", "point my domain at this app", "set up SSL for my domain",
  "my custom domain isn't working", "DNS isn't propagating", "add a subdomain for this",
  "why is my site showing not secure".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "cloudflare", "dns", "domains"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S8-Deployment
---

# Domain & DNS Setup

Connects a custom domain (or subdomain) to a Cloudflare-hosted Worker or Pages app, with the DNS records set up correctly the first time and SSL working, instead of the trial-and-error most founders do when they've never touched DNS before.

## Stage
This skill belongs to Stage S8: Deployment

## When to Use
- The app is deployed on a `*.workers.dev` or `*.pages.dev` URL and needs a real domain
- The user bought a domain and wants it pointed at the app
- SSL is showing "not secure" or a certificate error
- DNS changes were made and the site isn't resolving yet
- Adding a subdomain (e.g. `app.example.com`) for a new environment or product
- Diagnosing why a working app suddenly isn't reachable at its domain

## Input Schema
```
domain:
  root_domain: string (e.g. example.com)
  subdomain: string (optional, e.g. app, api)
  registrar: string (where the domain was bought — may or may not be Cloudflare)
  domain_already_on_cloudflare: boolean (nameservers pointed at Cloudflare?)
  target: "worker" | "pages project"
  ssl_mode_needed: "Full" | "Full (strict)" (default: Full strict once cert is live)
```

## Workflow
### Step 1: Confirm the domain is on Cloudflare's nameservers
If the domain wasn't registered through Cloudflare, it needs to be added as a Cloudflare zone first: dashboard → Add a Site → enter domain → Cloudflare gives two nameservers → update those at the registrar (GoDaddy, Namecheap, etc.). This step alone can take a few hours to propagate. Confirm zone is "Active" in the Cloudflare dashboard before proceeding.

### Step 2: Choose the connection method
- **Worker**: Workers & Pages → select the Worker → Settings → Domains & Routes → Add Custom Domain → enter the domain/subdomain. Cloudflare handles the DNS record and SSL automatically.
- **Pages**: Workers & Pages → select the Pages project → Custom domains → Set up a custom domain → enter the domain/subdomain. Same automatic handling.
- Manual DNS route (only if not using the built-in custom domain UI): add a `CNAME` record (subdomain) or `A`/`AAAA` (root, using Cloudflare's proxy IPs or CNAME flattening) pointed at the `*.workers.dev` / `*.pages.dev` target, with the orange-cloud proxy turned ON.

### Step 3: Set SSL/TLS mode correctly
Dashboard → SSL/TLS → Overview. Use **Full** or **Full (strict)** — never "Flexible" for an app serving dynamic content, since Flexible can cause redirect loops with apps that enforce HTTPS internally. Full (strict) requires the origin present a valid cert; for Workers/Pages this is handled automatically since Cloudflare is both edge and origin.

### Step 4: Handle CAA records if the domain has them
If a `CAA` record exists on the zone restricting which certificate authorities can issue certs, it must explicitly allow Cloudflare's CA (letsencrypt.org, pki.goog, digicert.com are the common ones Cloudflare uses) or the automatic SSL cert issuance will fail silently. Check dashboard → DNS → Records for existing `CAA` entries before assuming SSL will "just work."

### Step 5: Verify propagation and live status
- DNS propagation can take anywhere from a few minutes to 48 hours depending on the record's previous TTL; check with `dig <domain>` or a propagation checker, don't assume it's instant
- Confirm the SSL cert is issued: dashboard → SSL/TLS → Edge Certificates should show the domain covered
- Load the domain in a real browser (not cached) and confirm it serves the app, not a Cloudflare error page or the old host

### Step 6: Self-Validation
- [ ] Zone is active on Cloudflare before any record changes were made
- [ ] Correct connection method used (custom domain UI, not manual DNS, unless manual was necessary)
- [ ] SSL mode is Full or Full (strict), not Flexible
- [ ] CAA records checked, not assumed absent
- [ ] Verified live in a real browser, not just "the dashboard says active"

## Output Schema
```
{
  domain: string,
  zone_status: "active" | "pending" | "not on cloudflare",
  connection_method: string,
  dns_records_added: [ { type: string, name: string, value: string, proxied: boolean } ],
  ssl_mode: string,
  caa_check: "clear" | "blocking - fixed" | "not checked",
  live_verified: boolean,
  propagation_note: string
}
```

## Output Format
```markdown
# Domain Setup — <domain>

## Zone status
Cloudflare nameservers: active / pending

## Connection
Method: Custom Domain (Workers & Pages UI)
Target: <worker/pages project name>

## SSL
Mode: Full (strict)
Cert status: issued / pending

## CAA check
No blocking CAA records found. / Found CAA blocking Let's Encrypt — added exception.

## Verified live
Loaded https://<domain> in browser: works / not yet (propagating, check back in X)

## Gotchas hit
- <anything unusual found>
```

## Error Handling
- Domain registered elsewhere and nameservers not yet updated → this is step 1, do not attempt DNS records until the zone shows active on Cloudflare
- "Not secure" warning right after setup → almost always propagation delay or SSL mode set to Flexible; check both before assuming a deeper problem
- CAA record blocking cert issuance → identify it explicitly by name in the DNS records list, don't just say "SSL isn't working"
- Subdomain vs root domain confusion → clarify which one the user means before adding records; `example.com` and `www.example.com` and `app.example.com` are three different records
- Domain was working, now isn't → check for recent changes to the DNS records, SSL mode, or an expired registration before assuming a Cloudflare-side outage
- User wants email on the same domain (MX records) → note this is a separate concern from app hosting; don't touch existing MX records when adding app-related DNS entries

## Examples
**Example 1**
User: "connect example.com to my worker"
Skill confirms the zone is active on Cloudflare, adds the domain via Workers & Pages → Domains & Routes, sets SSL to Full (strict), and verifies example.com loads the app live.

**Example 2**
User: "my site says not secure after I pointed the domain here"
Skill checks SSL/TLS mode (finds it set to Flexible), switches to Full (strict), confirms the cert has issued, and reloads to verify the warning is gone.

**Example 3**
User: "I added the DNS record but nothing's happening"
Skill checks propagation status with `dig`, checks for a blocking CAA record, and confirms whether the record was even added to the correct zone (common mistake: editing DNS at the registrar instead of at Cloudflare after nameservers were switched).

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- cloudflare-deployer (S8-Deployment)
- marketing-site-seo-audit (S10-Growth)

### Fed By
- cloudflare-deployer (S8-Deployment)

### Feedback Loop
- Any DNS/SSL failure mode found here (a CAA block, a propagation surprise) should get logged so the next domain setup for this founder checks it upfront instead of rediscovering it.

```yaml
chain_metadata:
  skill_slug: "domain-dns-setup"
  stage: "deployment"
  timestamp: string
  suggested_next:
    - "cloudflare-deployer"
    - "marketing-site-seo-audit"
```
