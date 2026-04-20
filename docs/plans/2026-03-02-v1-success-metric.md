# v1 Success Metric — Decision Record

**Date:** 2026-03-02
**Branch:** reasearch/hidden-costs
**Status:** ✅ Decided

---

## Decision

> **"We'll know v1 succeeded when the site receives 400+ monthly sessions from non-branded organic search."**

---

## Rationale

### Why organic sessions (not engagement)?

The product's theory of value is: *merchants who are searching for fee information find this tool and use it to make a better decision.* Organic sessions measure the first half of that chain — reach — which is the current bottleneck.

Engagement depth (simulator use, entity views) is meaningful but secondary: without distribution, there are no users to engage. v1 is a distribution problem, not a feature problem.

### Why non-branded?

Non-branded queries (e.g. "comisiones cobro tarjeta argentina", "cuanto cobra mercado pago") signal that real merchants are finding the tool when searching for answers — not people who already know the product exists. Branded traffic (searches for "cobrocontarjeta" or "monitor comisiones") inflates the number without validating the thesis.

### Why 400?

- 400/month ≈ 13/day from organic search
- Realistic for a niche, high-intent Argentine market tool within 6 months of SEO work
- Low enough to be achievable; high enough to prove the channel works

### Why not Option 3 (composite: sessions + simulator use)?

Composite metrics are more accurate but harder to act on. If the composite fails, you don't know which half to fix. For v1, a single metric forces focus: does the tool get found? Simulator engagement becomes a Tier 2 metric once distribution is proven.

---

## How to Measure

**Tool:** Google Search Console (already configured)

**Steps:**
1. Open Search Console → Performance → Search results
2. Filter: Date range = last 28 days (rolling)
3. Filter: Query → "Does not contain" → `cobrocontarjeta` (exclude branded)
4. Read: **Total clicks** (not impressions — clicks = sessions)

**Check frequency:** Monthly, on the first of each month.

**Baseline:** Establish baseline in March 2026 (first full month after custom domain propagation).

---

## What This Metric Does NOT Tell You

- Whether the user compared providers (engagement quality)
- Whether the user switched providers (downstream action)
- Whether the content answered their question (satisfaction)

These are valid Tier 2 metrics for v2 planning. They are tracked by GA4 (`simulator_use`, `entity_view`, `outbound_click`) and available for analysis — they just don't gate v1 success.

---

## Related Decisions

- Product type: comparison tool (not guide), additive architecture — see `things-to-improve.md` §1
- Geographic scope: PBA/GBA v1, extensible architecture — see `things-to-improve.md` §3
- Merchant validation: 5–8 interviews still pending — see `things-to-improve.md` §2
