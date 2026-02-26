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

### 4. Reconcile the $800K vs. $2.1M threshold contradiction
The decision tree (§8.2) and the break-even calculation (§4.3) give different answers to the same question:
- Decision tree uses $800K as the bank-fintech inflection point
- Break-even calculation shows $2.1M–$3.06M depending on comparison scenario

**Why it matters:** When writing requirements (e.g., "show user whether to use bank or fintech"), you need a single source of truth. Currently, a PM writing from this doc would get inconsistent user flows.

**Action:** Pick one methodology as canonical. Update the other to match. The document already flags this mismatch in a footnote (§8.2) — just resolve it.

**Effort:** 30 minutes. Re-run the break-even math or adjust the decision tree logic to align.

### 5. Define one success metric for v1
Not a full metrics framework — just answer: **What user behavior would make this product a success in 6 months?**

Examples of different answers (each changes the product scope):
- "A merchant switched providers after using the tool" → product needs decision-support and switching workflows
- "1,000 monthly active users" → product needs SEO + content strategy
- "Merchants reduce payment processing costs by 20% on average" → product needs integration with their actual systems

**Why it matters:** This forces scope discipline. A PRD without a success metric will expand to include everything.

**Effort:** 1–2 hours in a working session with leadership/design.

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
☐ Reconcile the $800K vs. $2.1M threshold
☐ Write one sentence: "We'll know v1 succeeded when ___"
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
