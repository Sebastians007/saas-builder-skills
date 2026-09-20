---
name: tripwire-funnel
description: >
  Builds a low-ticket ($7-$47) tripwire offer funnel that turns cold leads
  into buyers fast, with an order bump and one upsell to lift average order
  value and offset ad spend.
  Use this skill when the user asks about a low-ticket first offer, order
  bumps, or turning leads into buyers, or says
  "I need a cheap first offer to turn leads into buyers", "what's a tripwire funnel",
  "help me build an order bump", "I want to offset my ad spend with a low-ticket sale",
  "how do I get people to buy something small before my main product", "build me an upsell flow".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "low-ticket", "upsell", "conversion"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# Tripwire Funnel

Converts free leads into paying customers with a deliberately cheap, high-value, low-friction first purchase, then immediately offers an add-on and an upsell. The point isn't to make money on the tripwire itself — it's to turn a "lead" into a "buyer," which changes how they respond to every future offer.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- The founder has an email list (from `optin-funnel`) but no buyers yet
- There's a small, specific piece of value that can be priced $7-$47 and delivered digitally
- Paid ads are running and need a low-ticket offer to offset acquisition cost
- The founder wants to build a "buyers list" before pitching the higher-priced core product
- `funnel-select` recommended `tripwire-funnel` for a sub-$50 price point with an upsell goal

## Input Schema
```
tripwire_product_name: string
tripwire_price: number            # typically 7-47
tripwire_description: string      # the ONE specific problem it solves fast
order_bump_product: string?
order_bump_price: number?
upsell_product: string?
upsell_price: number?
downsell_product: string?         # lighter version if upsell is declined
core_product_name: string         # what this ultimately leads toward
```

## Workflow
### Step 1: Sanity-check the tripwire offer
A good tripwire solves one specific problem fast, feels like 10x the price in value, delivers digitally (no shipping friction), and gives a real taste of the core product. If the proposed offer is vague or tries to cover too much, narrow it — "everything you need to start" is not a tripwire, "the exact email template that got us 40% open rates" is.

### Step 2: Build the flow
```
Opt-In → Tripwire Offer ($7-$47) → Order Bump → Upsell → (Downsell if declined) → Thank You
```
Write each page's purpose and required elements. The tripwire offer page needs urgency framing (why now) but should stay short — this isn't a long-form sales page.

### Step 3: Write the order bump
One checkbox add-on shown at checkout, priced $17-$37 above the tripwire, framed as "most customers add this." Pull copy pattern: "✅ ADD THIS: {{bump product}} — most customers add this because [one-sentence benefit]."

### Step 4: Write the upsell page
Congratulations framing first (they just bought — reinforce the good decision), pattern-interrupt ("wait, your order isn't complete"), one-click purchase button (no re-entering payment info), and an always-visible "no thanks" decline link — never hide it.

### Step 5: Model the economics
Show the user the expected revenue-per-lead math using realistic take rates (tripwire ~8%, bump ~30%, upsell ~15%) so they can sanity-check whether this funnel can be profitable at their ad cost per lead.

### Step 6: Self-Validation
- [ ] Tripwire price is under $50 and solves one specific problem
- [ ] Order bump is a natural complement, not a random unrelated product
- [ ] Upsell page has a visible, unhidden decline option
- [ ] Revenue-per-lead math is shown so the user can judge profitability before building
- [ ] Every offer in the chain visibly builds toward `core_product_name`

## Output Schema
```
{
  "pages": [
    { "name": "tripwire_offer", "price": number, "copy": object },
    { "name": "order_bump", "price": number, "copy": object },
    { "name": "upsell", "price": number, "copy": object },
    { "name": "downsell", "price": number, "copy": object }
  ],
  "economics_model": { "leads": number, "projected_revenue_per_lead": number },
  "benchmarks": object
}
```

## Output Format
```markdown
# Tripwire Funnel: <Tripwire Product Name>

## Flow
Opt-In → Tripwire ($<price>) → Order Bump (+$<price>) → Upsell ($<price>) → Thank You

## Tripwire Offer Page
<copy>

## Order Bump
<checkout add-on copy>

## Upsell Page
<congratulations, pattern interrupt, one-click offer, visible decline link>

## Economics Model (per 1,000 leads, illustrative)
| Step | Take Rate | Revenue |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Opt-in → tripwire purchase | > 8% |
| Order bump take rate | > 30% |
| Upsell take rate | > 15% |
```

## Error Handling
- If the tripwire price is set above $50, flag that it's drifting out of impulse-buy territory and ask if `ecommerce-funnel` or a direct offer might fit better.
- If no order bump or upsell is provided, still build the tripwire page but note the funnel is leaving revenue-per-lead on the table.
- If the "no thanks" decline link is missing from the upsell design, refuse to ship it without one — hiding the decline option is a dark pattern and a trust risk.
- If the tripwire product doesn't logically connect to `core_product_name`, flag the mismatch — a disconnected tripwire trains buyers to expect something the core product doesn't deliver.

## Examples
**Example 1:** A SaaS founder selling a $49/mo automation tool builds a $17 tripwire — a pre-built Zapier template pack — with a $27 bump (a companion "10 Automation Recipes" PDF) and a $97 upsell (a 1-hour setup call), all funneling toward trial signup for the core SaaS product.

**Example 2:** A course creator with a $297 course sells a $9 "swipe file" tripwire from cold Instagram traffic, with a $19 bump and a $47 upsell (mini-course), designed to convert cold leads into buyers before ever pitching the $297 course.

**Example 3:** A GRC consultant sells a $27 "Vendor Risk Assessment Template Pack" as a tripwire from a LinkedIn audience, upselling to a $197 "Compliance Audit Prep Kit," building toward a $3,000 consulting retainer as the core product.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/tripwire-offer-page.html`

## Flywheel Connections
### Feeds Into
- `checkout-funnel-auditor` (S7-Growth) — audits the tripwire/bump/upsell checkout flow once live
- `ab-test-generator` (S7-Growth) — tests bump/upsell offers and price points
- `high-ticket-funnel` / `application-funnel` — buyers list from this funnel becomes the audience for the core high-ticket pitch

### Fed By
- `optin-funnel` — supplies the lead list this funnel converts to buyers
- `funnel-copy` — writes the order bump and upsell copy

### Feedback Loop
If order bump take rate stays under 20%, the bump likely isn't a true complement to the tripwire — re-check with `funnel-copy` whether the "most customers add this" framing and the product pairing actually make sense together before touching price.

```yaml
chain_metadata:
  skill_slug: "tripwire-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "ab-test-generator"
    - "funnel-copy"
```
