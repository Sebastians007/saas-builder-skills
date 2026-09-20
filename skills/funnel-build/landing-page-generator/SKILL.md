---
name: landing-page-generator
description: >
  Use this skill whenever a user wants to build, write, or generate a marketing landing page,
  sales page, or promotional web page. Trigger on phrases like: "build me a landing page for...",
  "write copy for my sales page", "I need a page that sells my...", "create a landing page",
  "help me write a page for my course / product / service / offer", "generate a marketing page",
  "write a homepage for...", "I need to convert visitors to...", or any situation where someone
  is building a website and needs persuasive, conversion-focused page copy.
  Also trigger when someone shares a product description, offer details, or target audience info
  and seems to be working on a web project — even if they don't say "landing page" explicitly.
  Always use this skill for landing pages, sales pages, lead gen pages, product pages, and
  squeeze pages. Don't wait for the perfect brief — if it's a marketing page, use this skill.
license: proprietary
version: "1.0.0"
tags: ["saas", "funnel", "asset-generation", "landing-page", "web-page-copy", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S3-Funnel-Build
  source: "internal (user-owned, not third-party)"
---

# Marketing Landing Page Generator

You help marketers, founders, freelancers, and agency owners go from idea to a complete, conversion-optimized marketing landing page — fast. Your output should be copy and structure that could go live, not a template to fill in later.

## Handling the input

Users will give you anything: a product name and one sentence, a full feature list, messy notes from a client call, a competitor URL, or a detailed brief. Work with what you have.

**If critical things are genuinely missing**, ask up to 3 targeted questions before writing. The only things that truly require an answer before starting:
- What is the product/offer? (can't proceed without this)
- Who is it for? (target audience — even a rough one)
- What's the primary action you want visitors to take? (buy, book a call, download, sign up)

Everything else — price, testimonials, specific features — can be inferred or handled with smart placeholders. If you can make a reasonable assumption, note it briefly and keep going. Don't hold the page hostage to information you can work around.


**Image assets — check before writing:**
Before writing page copy, check whether any images have been provided or generated
earlier in this session:
- Book cover / 3D mockup → use in hero section, right-aligned on desktop
- Lead magnet cover PNG → use as the opt-in page hero visual
- Product photo → use in hero or features section
- Headshot → use in bio / credibility section
- Logo → use in page header

If images ARE available: reference their file paths in the page copy where relevant
(e.g., in the hero section note: "Hero image: `[book-mockup.png]` — float right on desktop").

If no images are available: include explicit design directives in the Page Notes
section specifying what image is needed and where:
> "Hero section needs a product visual. Recommended: generate a 3D book mockup from
> your cover image using the `funnel-builder` Image Assets section, or use the
> lead magnet cover PNG from `lead-magnet-creator`."

**What to infer vs. ask:**
- Tone/voice: infer from the product and audience (a SaaS tool for developers ≠ a wellness course for moms)
- Price: **never invent a specific dollar amount.** If the price wasn't given, use `[PRICE]` exactly as written. Do not substitute $29, $97, $299, or any other number — a wrong price on a live page destroys trust instantly. The client will fill this in.
- Testimonials: write placeholder copy in the right format (`[Testimonial: 1-2 sentences from a happy customer about [specific result]]`)
- Features you're unsure about: use plausible examples and note them as assumptions

## What you produce

A complete landing page, structured in proven conversion order. Every section should have real, finished copy — not instructions for what to write, not empty brackets, but actual words a visitor would read.

---

### 🌐 Landing Page: [Product/Offer Name]

**Target visitor:** [Who this page is written for]
**Primary CTA:** [The one action you want them to take]
**Page goal:** [What conversion means here — purchase / signup / booking / download]

---

#### SECTION 1: Hero

The first thing a visitor sees. Make or break. You have about 3 seconds.

**Headline:** [Bold, benefit-led, specific. What does the visitor get or become? Avoid clever; be clear.]

**Subheadline:** [1–2 sentences expanding on the headline. Add specificity or handle the most obvious objection.]

**Primary CTA button:** [Action-oriented label — not "Submit", something like "Start My Free Trial" or "Get Instant Access"]

**Supporting detail:** [Optional: a trust signal near the button — "No credit card required" / "Join 4,200+ students" / "7-day money back guarantee"]

---

#### SECTION 2: The Problem (or: Why This Matters)

Speak directly to the pain, frustration, or gap the visitor is experiencing. This is where you earn their attention by proving you understand their world.

Write 2–4 short paragraphs or a bullet list of 4–6 pain points. Be specific. Generic pain ("Are you struggling to grow your business?") doesn't convert — specific pain does ("You're spending 3 hours a day on tasks that should take 20 minutes").

[COPY HERE]

---

#### SECTION 3: The Turning Point

A brief bridge — 1–2 sentences or a short paragraph — that pivots from the problem to the solution. This is the "there's a better way" moment.

[COPY HERE]

---

#### SECTION 4: Introducing [Product Name]

The solution reveal. Write 2–3 sentences introducing the product in plain language. Follow with a short list of 4–6 core benefits (not features — what does the visitor gain, save, or avoid?).

**Format:**
> [Product Name] is [what it is] that [what it does for the customer]. Unlike [alternative], it [key differentiator].

Then the benefit bullets:
- ✓ [Benefit 1]
- ✓ [Benefit 2]
- ✓ [Benefit 3]
- ✓ [Benefit 4]
- ✓ [Benefit 5]

---

#### SECTION 5: How It Works

Include this section whenever the product has a process, OR when it's a new/unfamiliar concept that visitors need to picture before they'll trust it. When in doubt, include it — a 3-step process section rarely hurts and often converts skeptics. Skip it only for products so familiar they need no explanation (e.g., a basic email newsletter).

If the product involves a process, use a simple 3-step format. Visitors trust things they understand.

**Step 1 — [Short name]:** [1–2 sentence description]
**Step 2 — [Short name]:** [1–2 sentence description]
**Step 3 — [Short name]:** [1–2 sentence description]

---

#### SECTION 6: Social Proof

Credibility through real results. If you have testimonials, use them. If not, write compelling placeholders in the exact format needed — the client can drop real quotes in.

Write 2–3 testimonial blocks:

> "[Specific result or transformation in 1–2 sentences. The more specific the outcome, the better — 'I increased revenue 40%' beats 'This was great.']"
> — [Name], [Title or context, e.g., "Marketing Director at XYZ" or "Freelance designer, 5 years experience"]

Also include 1 social proof summary line (e.g., "Trusted by 3,000+ teams across 40 countries" or "Rated 4.9/5 across 200+ reviews") — use a placeholder if needed.

---

#### SECTION 7: What's Included / Features Deep Dive

For products with multiple components, features, or modules — break them down here. This section converts fence-sitters who need the full picture.

Write each feature/module as a short block:

**[Feature name]**
[2–3 sentences. Lead with the outcome, then explain what it is and why it matters.]

Aim for 3–6 feature blocks, depending on the product complexity.

---

#### SECTION 8: The Offer (Pricing)

Anchor the value before revealing the price. Summarize everything they get, then present the pricing clearly.

**Everything you get:**
- [Item 1]
- [Item 2]
- [Item 3]
- [Bonus if applicable]

**Investment:** [PRICE] *(or: Starting at [PRICE] / [Payment plan])*

**CTA button:** [Repeat primary CTA]

**Risk reversal:** [Guarantee statement — e.g., "30-day money-back guarantee. If [specific outcome] doesn't happen, we'll refund you in full."]

---

#### SECTION 9: FAQ

Answer the 4–6 questions that are actually stopping people from buying. These aren't "how does it work" FAQ — they're objection-handling in disguise.

Think: What's the most common reason someone would talk themselves out of this? Answer that.

**Q: [Question]**
A: [Answer — honest, direct, 2–4 sentences]

*(Repeat for 4–6 questions)*

---

#### SECTION 10: Final CTA

The last section. Don't just repeat the button — give them one more reason to act now. Could be urgency, a reminder of the transformation, or a direct personal appeal.

**Closing headline:** [Motivational, forward-looking. What does their life/work look like after?]

[1–2 sentences of closing copy]

**Final CTA button:** [Same label as primary CTA]

---

### 📝 Page Notes *(for the builder)*

A short section at the end with implementation notes:

- **Recommended page length:** [Short / Medium / Long — and why]
- **Above-the-fold priority:** [What must be visible without scrolling on mobile]
- **Key A/B test to run first:** [The highest-leverage thing to test — usually the headline]
- **SEO meta title:** [Under 60 characters]
- **SEO meta description:** [Under 160 characters]
- **One thing that would make this page significantly better:** [Honest callout — missing testimonial, unclear pricing, no video, etc.]
- **Ready to build?** The HTML page is saved to your project folder and ready to open in a browser or paste into your page builder.

---

## Output format

Write the entire page as clean markdown. Every section should have real, finished copy. Use `[PLACEHOLDER: description]` format sparingly and only for things the client genuinely needs to supply — real testimonials, the actual price (always `[PRICE]` if not given, never a guessed number), specific stats only they would know.

After the page, add one line: *"Want this as a full HTML file you can drop into your site? Just say the word."*

## Tone calibration

Before writing, quickly assess:
- **Who's the buyer?** (Consumer vs. business, technical vs. non-technical, price-sensitive vs. outcome-focused)
- **What's the purchase decision like?** (Impulse vs. considered — a $27 ebook and a $5,000 consulting package need completely different approaches)
- **What voice fits?** (Direct response / authoritative / conversational / inspirational)

Then write the whole page in that register. Inconsistent tone is one of the fastest ways to kill trust on a landing page.

## What makes landing page copy actually work

The two things that kill most landing pages:
1. **Leading with features instead of outcomes.** "Our software has 47 integrations" → nobody cares. "Connect to every tool your team already uses — no switching, no extra logins" → that they care about.
2. **Writing for everyone and convincing no one.** The more specific the copy, the more a specific reader feels like it was written for them. Vague copy tries to include everyone and ends up resonating with no one.

Keep these in mind throughout. When in doubt, make it more specific and more outcome-focused.


## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`

## Flywheel Connections
### Feeds Into
- `cloudflare-deployer` (S8-Deployment) — ships the generated landing page HTML live
- `avatar-extraction` (S2-Audience-Positioning) — the page's messaging should be re-checked against the target avatar as it's refined

### Fed By
- `offer-extraction` (S2-Audience-Positioning) — supplies the offer details the page is built to sell
- `headline-hook-generator` — supplies the primary headline and hook the page opens with

### Feedback Loop
If `signup-conversion-tracker` or `ab-test-generator` shows a page underperforming, isolate whether the drop-off is above or below the fold before rewriting the whole page — most fixable losses are in the headline/hero, not the body copy.

```yaml
chain_metadata:
  skill_slug: "landing-page-generator"
  stage: "funnel-build"
  timestamp: string
  suggested_next:
    - "cloudflare-deployer"
    - "ab-test-generator"
```
