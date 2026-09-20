---
name: ecommerce-funnel
description: >
  Builds a product-page-to-checkout funnel for physical or digital products,
  covering the product page, cart optimization, order bumps, post-purchase
  upsells, and cart-abandonment email recovery.
  Use this skill when the user asks about selling a physical or digital
  product online, or says
  "I want to sell a physical product", "build me a product page", "how do I reduce cart abandonment",
  "set up a post-purchase upsell", "I'm launching a Shopify-style store", "help me sell my digital download",
  "what should my product page include", "improve my add-to-cart rate".
license: MIT
version: "1.0.0"
tags: ["saas", "funnel", "ecommerce", "product-page", "checkout"]
compatibility: "Claude Code, ChatGPT, Gemini CLI, Cursor, Windsurf, any AI agent"
metadata:
  author: saas-builder-skills
  version: "1.0"
  stage: S9-Funnels
  adapted_from: "ominou5/funnel-architect-plugin (MIT)"
---

# E-Commerce Funnel

Optimizes the path from product page to purchase to post-purchase upsell for a physical or digital product. Applies even if the "product" is a one-time digital download sold from an app rather than a full storefront — the same page anatomy and cart psychology apply.

## Stage
This skill belongs to Stage S9: Funnels

## When to Use
- Selling a physical product (DTC brand, Shopify-style store)
- Selling a one-time digital product (template pack, dataset, asset bundle) from an app or site
- The user's add-to-cart or checkout completion rate is unclear or feels low
- Adding an order bump or post-purchase upsell to an existing checkout
- `funnel-select` recommended `ecommerce-funnel` for a one-time product under $500

## Input Schema
```
product_name: string
product_type: string              # "physical" | "digital"
price: number
key_benefits: string[]            # 3-5 bullets
has_reviews: boolean
order_bump_product: string?
post_purchase_upsell_product: string?
shipping_threshold_free: number?  # for physical products
```

## Workflow
### Step 1: Build the product page anatomy
Above the fold: product images (3-5, lifestyle + close-up), title, price (with any discount shown), star rating + review count, 3-5 benefit bullets, high-contrast add-to-cart button (full-width on mobile), trust badges (shipping/guarantee/secure checkout). Below the fold: detailed description in benefit language, size/usage guide if relevant, reviews with photos, comparison table, FAQ, related products.

### Step 2: Optimize the cart
Recommend a side-drawer cart instead of a redirect to a separate cart page. Add a free-shipping threshold nudge if `shipping_threshold_free` is set ("Add $X more for free shipping"), a cross-sell widget, and express checkout options (Apple Pay, Google Pay, Shop Pay) to cut clicks to purchase.

### Step 3: Write the order bump and post-purchase upsell
Order bump shown at checkout as a low-friction add-on. Post-purchase upsell uses one-click purchase (no re-entering payment) with the pattern: "Wait — add {{product}} for just ${{price}}?" and a clear, unhidden decline link.

### Step 4: Write the cart abandonment sequence
4-email sequence: reminder (+1hr), social proof (+24hr), discount (+48hr), final urgency (+72hr). Keep discount usage honest — don't offer it if the business can't sustain it as an expected norm.

### Step 5: Set benchmarks
Product page → ATC 8%+, ATC → checkout 50%+, checkout → purchase 65%+, order bump take rate 20%+, post-purchase upsell 12%+.

### Step 6: Self-Validation
- [ ] Add-to-cart button is above the fold and mobile-optimized
- [ ] Trust badges appear near the payment/checkout button, not just at the page bottom
- [ ] Cart uses a side-drawer pattern, not a full page redirect, where feasible
- [ ] Post-purchase upsell has a visible, unhidden decline option
- [ ] Cart abandonment sequence doesn't over-discount in a way that trains customers to always wait for a coupon

## Output Schema
```
{
  "product_page": { "sections": string[], "copy": object },
  "cart_optimizations": string[],
  "order_bump": object,
  "post_purchase_upsell": object,
  "abandonment_sequence": [ { "timing": string, "subject": string } ],
  "benchmarks": object
}
```

## Output Format
```markdown
# E-Commerce Funnel: <Product Name>

## Flow
Ad/Organic → Product Page → Add to Cart → Checkout → Order Bump → Upsell → Thank You

## Product Page
<above-the-fold and below-the-fold sections with copy>

## Cart Optimization
<side-drawer, free shipping nudge, cross-sell, express checkout>

## Order Bump / Post-Purchase Upsell
<copy>

## Cart Abandonment Email Sequence
| Email | Timing | Subject |
|---|---|---|

## Benchmarks to Track
| Metric | Target |
|---|---|
| Product page → ATC | > 8% |
| Checkout → purchase | > 65% |
```

## Error Handling
- If `key_benefits` reads like a spec sheet ("100% cotton") rather than a benefit ("stays soft after 50 washes"), rewrite toward outcomes before finalizing copy.
- If `has_reviews` is false and the product is new, don't fabricate review counts or star ratings — recommend a launch-period alternative (founder guarantee, "first 100 customers" framing) instead.
- If the product is digital but the workflow still recommends a shipping threshold nudge, drop that section — it doesn't apply.
- If checkout has more than 3 fields beyond payment info, flag that as excess friction and recommend trimming.

## Examples
**Example 1:** A SaaS founder sells a one-time $39 "Notion Dashboard Template" as a side product. Product page skips physical-product sections (shipping, size guide) and leans on screenshots, a "what's inside" bullet list, and a post-purchase upsell to a $97 template bundle.

**Example 2:** A DTC skincare brand launches a $34 serum. Product page includes lifestyle photography placeholders, ingredient benefit bullets, a free-shipping-at-$50 nudge, and a $12 order bump (travel-size companion product).

**Example 3:** A user reports 40% cart abandonment. The skill reviews the existing checkout, flags a 6-field checkout form as the likely cause, recommends trimming to email + shipping + payment, and writes the 4-email abandonment recovery sequence as a stopgap.

## References
- `shared/references/saas-glossary.md`
- `shared/references/flywheel-connections.md`
- `templates/product-page.html`

## Flywheel Connections
### Feeds Into
- `checkout-funnel-auditor` (S7-Growth) — deeper audit of the live checkout flow
- `ab-test-generator` (S7-Growth) — tests product page and cart variants
- `pricing-page-optimizer` (S7-Growth) — if the "product" is actually a SaaS plan being sold this way

### Fed By
- `funnel-select` — confirms e-commerce is the right funnel for this offer
- `funnel-copy` — writes benefit bullets and objection-handling copy

### Feedback Loop
If `checkout-funnel-auditor` finds a high checkout abandonment rate after this funnel ships, revisit the field count and trust badge placement here before assuming it's a pricing problem.

```yaml
chain_metadata:
  skill_slug: "ecommerce-funnel"
  stage: "funnels"
  timestamp: string
  suggested_next:
    - "checkout-funnel-auditor"
    - "ab-test-generator"
    - "funnel-copy"
```
