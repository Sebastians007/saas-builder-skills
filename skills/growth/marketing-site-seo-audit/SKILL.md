---
name: marketing-site-seo-audit
description: >
  Audits a SaaS app's public marketing/landing site for the basic SEO issues
  that actually affect organic signups - meta tags, heading structure, page
  speed, and mobile-friendliness - and returns a prioritized fix list, not a
  100-item generic checklist.
  Use this skill when the user asks about SEO problems, organic traffic, or
  why their landing page isn't showing up in search, or says
  "audit my landing page SEO", "why am I not showing up on google", "check my meta tags",
  "is my site mobile friendly", "my page speed seems slow", "review my SaaS site for SEO issues",
  "what's hurting my organic signups", "SEO checklist for my app's website".
license: MIT
version: "1.0.0"
tags: ["saas", "app-building", "growth", "seo", "marketing-site", "organic-traffic"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S10-Growth
---

# Marketing Site SEO Audit

This skill checks a SaaS app's public-facing marketing site against the specific SEO fundamentals that move organic signups (not domain authority tricks or link-building schemes) and returns a short prioritized list. It exists because most SEO checklists are 100 items long and a founder needs to know which 3 actually matter this week.

## Stage
This skill belongs to Stage S10: Growth

## When to Use
- The marketing site hasn't been checked for basic SEO since launch
- Organic traffic or organic signups are flat or unexplained
- signup-conversion-tracker showed Visit→Signup is weak and the traffic source itself needs checking
- Before a content or launch-directory push, to make sure the site itself isn't leaking value
- The user asks "why doesn't my page show up when I search for [my own product]"
- A redesign happened and the user wants to confirm SEO basics weren't broken in the process

## Input Schema
```
site_url: string?
pages_to_audit: array?           # defaults to homepage + pricing page if not specified
target_keywords: array?          # what the app should rank for, if known
current_organic_traffic: string? # rough sense of current traffic, if known
known_issues: string?            # anything the user already suspects
```

## Workflow
### Step 1: Confirm Scope
Default to auditing the homepage and pricing page (the two highest-intent pages for a SaaS site) unless the user names others. Don't try to audit an entire site's blog archive under this skill — that's a bigger project; flag it and stay focused on the core conversion pages.

### Step 2: Check On-Page Fundamentals
For each page, check for:
- Title tag: present, under ~60 characters, includes the primary keyword and isn't just the company name
- Meta description: present, under ~155 characters, states what the product does and who it's for (this affects click-through even though it's not a ranking factor)
- One H1 per page that matches what the page is actually about (not a slogan disconnected from the product)
- Logical heading hierarchy (H2s under the H1, not skipping to H3 or using headings for styling instead of structure)
- Alt text on meaningful images (not decorative ones)
- A single clear canonical URL (no duplicate content across http/https or www/non-www versions)

### Step 3: Check Page Speed Basics
Without needing a live speed-test tool, ask the user to check (or check via WebFetch/browser tools if available) whether the page loads reasonably fast on mobile. Common SaaS-site culprits to flag if visible in the code: unoptimized/uncompressed hero images, render-blocking scripts loaded before content, no lazy-loading on below-fold images, embedded videos autoplaying on load.

### Step 4: Check Mobile-Friendliness
Confirm the page has a responsive viewport meta tag, text is readable without zooming, tap targets (buttons/links) aren't crammed too close together, and the page doesn't require horizontal scrolling.

### Step 5: Check Indexability
Confirm the page isn't accidentally blocked (robots.txt disallow, noindex meta tag left over from a staging environment — this happens constantly after a redeploy and silently kills all organic traffic). This is the single most common and most damaging issue on early-stage SaaS sites; always check it first even before the polish items.

### Step 6: Prioritize the Fix List
Rank findings in this order of actual impact: (1) indexability blockers — nothing else matters if the page isn't indexed, (2) missing/broken title and meta description on the highest-intent pages, (3) mobile-friendliness breaks, (4) page speed issues, (5) heading structure cleanup. Don't present a flat alphabetical checklist.

### Step 7: Self-Validation
Before presenting output, confirm:
- [ ] Indexability was checked first and explicitly confirmed either way
- [ ] Findings are ranked by impact, not listed as a flat checklist
- [ ] Each finding names the specific page and the specific fix, not a generic "improve SEO"
- [ ] No generic "write more content" or "build backlinks" filler advice not tied to something actually observed

## Output Schema
```json
{
  "pages_audited": ["string"],
  "indexability_status": "indexed|blocked|unknown",
  "findings": [
    {"page": "string", "category": "indexability|meta_tags|headings|speed|mobile", "issue": "string", "fix": "string", "priority": "critical|high|medium|low"}
  ],
  "whats_fine": ["string"]
}
```

## Output Format
```markdown
# Marketing Site SEO Audit — [site URL]

## Indexability Check (checked first, always)
[Confirmed indexed / BLOCKED - explain exactly how / could not verify]

## Priority Fixes
1. [Critical/High] [Page]: [issue] → [specific fix]
2. ...

## Lower Priority
- [Page]: [issue] → [fix]

## What's Already Fine
- [item]

## Not Covered by This Audit
Content strategy, keyword research, backlinks, and blog SEO are separate efforts — this audit covers only the technical/on-page basics of the core conversion pages.
```

## Error Handling
- Site URL not accessible or not provided → ask for it directly; if the user only has a local/staging build, note that some checks (indexability, live speed) can't be verified until it's live
- No target keywords known → don't invent them; check structural fundamentals only and suggest they get one clear phrase describing what the product does and who it's for, since that phrase should anchor the title/H1/meta description
- User wants a full technical SEO crawl of the whole site → scope it down to the core conversion pages for this skill and flag that a full-site crawl is a bigger, separate effort
- Indexability appears blocked → treat as critical and say so first, before any other finding, since it makes every other fix pointless until resolved
- No way to measure actual page speed (no tool access) → state this limitation plainly and check for the common code-level culprits instead of guessing a speed score

## Examples
**Example 1**
User: "Nobody finds us on Google even when they search our exact product name."
Skill: Checks indexability first, finds a leftover `noindex` meta tag from when the site was on a staging subdomain, flags it as the single blocking issue, and notes everything else is secondary until that's fixed.

**Example 2**
User: "Check my pricing page for SEO issues."
Skill: Confirms indexability is fine, finds the title tag is just "Pricing" with no product name or keyword, the meta description is missing entirely, and the H1 says "Simple, Transparent Pricing" instead of naming what's being priced — gives exact replacement text for each.

**Example 3**
User: "My site feels slow on my phone."
Skill: Checks for a responsive viewport tag (present), then flags an uncompressed 4MB hero image and an autoplaying background video as the likely causes, ranks the image fix as higher priority since it's simpler to resolve.

## References
- `shared/references/saas-glossary.md` — SaaS/startup terminology
- `shared/references/flywheel-connections.md` — master skill connection map

## Flywheel Connections
### Feeds Into
- signup-conversion-tracker (S10-Growth)
- unique-value-prop-audit (S1-Research)
- user-acquisition-analyzer (S1-Research)

### Fed By
- cloudflare-deployer (S8-Deployment)
- domain-dns-setup (S8-Deployment)

### Feedback Loop
Once fixes ship, re-check indexability and re-run signup-conversion-tracker's Visit→Signup stage after a few weeks to see whether organic traffic quality (not just volume) actually improved.

```yaml
chain_metadata:
  skill_slug: "marketing-site-seo-audit"
  stage: "growth"
  timestamp: string
  suggested_next:
    - "signup-conversion-tracker"
    - "unique-value-prop-audit"
```
