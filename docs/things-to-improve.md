# Things to Improve — Before Writing the PRD

Analysis from senior product owner perspective (FAANG).

---

## Tier 1: True Blockers
*Can't write a good PRD without resolving these.*

### 1. ✅ Resolve what product you're building — RESOLVED
The document treats "a guide for merchants" and "a comparison tool for merchants" as the same thing — they're not.
- A guide is content (informational, passive consumption)
- A comparison tool is software (interactive, decision-support)
- A calculator is a third thing entirely

**Decision (February 2026):** Hidden costs research will be integrated into the **existing comparison tool** as new UI features — e.g., breakeven calculator, fiscal cost explainer, bonification lifecycle alert. **Not a separate page.**

This determines that the architecture is additive (new features on top of existing data model), not greenfield.

### 2. Run 5–8 merchant interviews
The entire product thesis rests on the assumption that merchants will optimize their provider choice if given clear information. This may be wrong.

**Specific questions to answer:**
- How did you actually choose your current payment provider? (inertia vs. deliberate)
- Do you know when your terminal bonification expires?
- Have you ever switched providers? What triggered it?
- If you discovered you could save $20K/month, how long would it take you to act?

**Why it matters:** If merchants choose by inertia or accountant recommendation, the product design changes fundamentally. Current research assumes rational optimization; reality may be different.

**Effort:** 1 week to recruit, conduct, and synthesize.

**Interview guide:** See `docs/merchant-interview-questions.md`

### 3. ✅ Make the geographic scope decision: GBA/PBA vs. National — RESOLVED
This is not a nice-to-have deferral — it determines:
- Scraper architecture (how many providers to monitor per region)
- Data maintenance burden (different tax regimes per province)
- Regulatory coverage (IIBB rules vary by province)
- Go-to-market strategy and positioning

**Decision (February 2026):** v1 targets **PBA/GBA explicitly**. Data model and scraper architecture must be built to support additional provinces without refactoring (extensible by design). National expansion is a v2 goal.

---

## Tier 2: Fix Before PRD Draft Review
*Not blockers, but create contradictions that will confuse requirements writing.*

### 4. ✅ Reconcile the $800K vs. $2.1M threshold contradiction — RESOLVED

**Resolution (February 2026):** Both thresholds are correct — they measure different things and are not in conflict. A disambiguation note was added to §4.3, and the §8.2 decision tree was expanded with a methodological note making both explicit:
- $800K = **provider selection point**: volume at which seeking bank bonification is worth the switching effort
- $2.1M / $3.06M = **hardware TCO breakeven**: volume at which paying terminal rental (without bonification) is cheaper than each fintech

A merchant at $1.5M/month sits above the selection threshold but below the hardware breakeven — the correct recommendation is neither "use bank" nor "use fintech" but "get the bonification."

### 5. ✅ Define one success metric for v1 — RESOLVED

**Decision (March 2026):** *"We'll know v1 succeeded when the site receives 400+ monthly sessions from non-branded organic search."*

- Measured via Google Search Console → Performance → filter out branded queries → read clicks
- Baseline to be established March 2026 (first full month after custom domain propagation)
- Non-branded = real merchants finding the tool via search, not existing awareness

Rationale: v1 is a distribution problem. Organic reach is the bottleneck; engagement (simulator use, entity views) is a Tier 2 metric once distribution is proven.

See full decision record: `docs/plans/2026-03-02-v1-success-metric.md`

---

## What Can Wait
*Useful but not PRD blockers.*

**ARS normalization**
- The document uses hardcoded ARS amounts that will degrade with inflation
- Useful to normalize to % or real-value equivalents, but this is editorial cleanup, not a strategic blocker
- Can be done when turning research into the actual PRD document

**Competitive landscape analysis**
- It's useful to know what tools merchants use today (Excel? accountants? their bank?)
- But given the specificity of the Argentine market (tax complexity, provider ecosystem), existing tools are probably weak
- Lightweight competitive check is sufficient; deep analysis can wait

**Market sizing**
- Helpful for a pitch to leadership, not for writing user requirements
- Can be gathered in parallel with interviews

**Over-documented sections**
- §2.6 (chargebacks) and §3.5 (Fiserv infrastructure) are thorough but have lower product relevance
- Editorial cleanup for the actual PRD, not a blocker for requirements writing

---

## Minimum Viable Pre-PRD Checklist

```
☑ Decide: guide, calculator, or comparison tool (or composed)?
    → Integrate hidden costs features INTO existing comparison tool
☑ Decide: GBA/PBA only or national v1?
    → PBA/GBA v1 with extensible architecture for future provinces
☐ Run 5–8 merchant interviews
  ☐ How do you choose your payment provider? (current process)
  ☐ Do you know when bonification expires?
  ☐ Have you switched? What triggered it?
  ☐ If you found $20K/month savings, how long to act?
  → Interview guide ready: docs/merchant-interview-questions.md
☑ Reconcile the $800K vs. $2.1M threshold
    → Both are valid; they measure different questions. See §4.3 disambiguation note.
☑ Write one sentence: "We'll know v1 succeeded when ___"
    → 400+ monthly sessions from non-branded organic search (GSC)
```

Everything else in the research document is solid enough to write from. The analytical quality is strong — the pre-work needed is strategic, not analytical.

---

## Key Insights to Carry Forward

**Best findings to anchor the PRD in:**
- The 12-month bonification lifecycle (§4.4) is the single highest-leverage product insight
- The "month 13 trap" where costs reappear without warning is a genuine market failure
- The $800K → $2M+ volume threshold creates natural product segmentation (different advice for different business sizes)

**Strongest analytical work:**
- Sensitivity analysis (§4.5) — shows the product's recommendations are robust across assumption variations
- Confidence rating system (🟢🟡🔴) — transparency about data quality is valuable for positioning

---

*Document created from PRD-readiness analysis.*
