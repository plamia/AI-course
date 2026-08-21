# Model Selection Note

**Date:** 2025-06-12
**Author:** Plamena Kichukova — Developer
**Project:** Meridian Retail Group (MRG) — Omnichannel Commerce Platform (Case A)
**Task:** Summarize a raw cross-channel inventory defect report into a structured triage note (repro / expected / actual / severity / area) for the MRG platform squad.
**Committed location:** https://github.com/plamia/AI-course/blob/main/model-selection-note.md

---

## Evaluation Criteria

| # | Criterion | Why it matters for this task |
|---|-----------|------------------------------|
| 1 | Accuracy to source report | Triage notes must reflect only what the report stated; invented repro steps or root causes mislead the squad. |
| 2 | Format compliance | Output must follow the fixed triage template to be pasteable into the defect tracker. |
| 3 | Completeness | A useful triage note must capture every actionable detail — location, frequency, systems involved, and the suspected sync delay. |
| 4 | Actionability of area label | With 3 SIs and multiple legacy systems, a specific area label routes the defect to the right squad faster. |

---

## Prompt Used

You are a commerce platform delivery assistant. Read the defect report text
below and produce a triage note using EXACTLY this template:

**Repro steps:** (numbered)
**Expected:** 
**Actual:** 
**Severity:** (Low / Medium / High)
**Suggested area label:** 

Use only information present in the report. Do not invent repro steps or root causes.
Keep it under 120 words.

DEFECT REPORT:
"Title: Click & collect order cancelled at pickup — phantom stock
Customer ordered a home-goods item online for in-store pickup at the Milan
store. Online product page showed 3 in stock. At pickup, the store had 0 units —
order was cancelled. SAP ERP showed 0 at that store; the platform inventory view
showed 3. Happens intermittently during peak hours. The commercetools inventory
sync from SAP appears delayed. Expected online availability to match store
ground-truth stock."

---

## Output Comparison

### Model A: Anthropic Claude Opus 4.8 (via EPAM DIAL)
> **Repro steps:**
> 1. Order a home-goods item online for in-store pickup at the Milan store (product page shows 3 in stock).
> 2. Attempt to collect the order at the store during peak hours.
> 3. Observe the outcome at pickup.
> **Expected:** Online availability matches store ground-truth stock.
> **Actual:** Store had 0 units and the order was cancelled; SAP ERP showed 0 at the store while the platform inventory view showed 3. Occurs intermittently during peak hours; commercetools inventory sync from SAP appears delayed.
> **Severity:** High
> **Suggested area label:** Inventory sync (commercetools ↔ SAP)

### Model B: Google Gemini 3.1 Pro (via EPAM DIAL)
> **Repro steps:**
> 1. Order a home-goods item online for in-store pickup at the Milan store (product page shows 3 in stock).
> 2. Attempt to pick up the order at the store.
> **Expected:** Online availability to match store ground-truth stock.
> **Actual:** Store has 0 units (SAP ERP shows 0; platform shows 3) and the order is cancelled. The commercetools inventory sync from SAP appears intermittently delayed during peak hours.
> **Severity:** High
> **Suggested area label:** Inventory Sync

---

## Scorecard

| Criterion | Model A score (1–3) | Model A evidence | Model B score (1–3) | Model B evidence |
|-----------|---------------------|------------------|---------------------|------------------|
| Accuracy to source report | 2 | Content is accurate, but step 3 ("Observe the outcome at pickup") is non-sourced filler not present in the report. | 3 | Every element traceable to the report; no invented steps. |
| Format compliance | 3 | Follows the template precisely; clean field separation. | 3 | Follows the template precisely; clean field separation. |
| Completeness | 3 | Captured Milan, peak-hours frequency, SAP-vs-platform mismatch, and the suspected sync delay. | 3 | Captured the same details, compactly, including the sync-delay hypothesis. |
| Actionability of area label | 3 | "Inventory sync (commercetools ↔ SAP)" names the exact integration — routes straight to the responsible squad. | 2 | "Inventory Sync" is correct but generic; doesn't name the systems, so needs human refinement before routing. |
| **Total** | **11** | | **11** | |

---

## Decision

**Selected model:** Anthropic Claude Opus 4.8

**Rationale:** The two models tie at 11, so the decision falls on the highest-priority criterion for this multi-SI environment — actionability of the area label — where Claude won by naming the exact integration ("commercetools ↔ SAP"), routing the defect straight to the responsible squad. Gemini was cleaner on accuracy (Claude added one non-sourced repro step) and equally complete, but its generic "Inventory Sync" label would need human refinement before routing across three SIs. The label specificity outweighed the minor accuracy cost for a defect that must reach the right team fast.

---

## Active Constraint

**What could change this decision within 30 days:**
If the triage note is fed into an automated router that treats added repro steps as executable, Claude's non-sourced step becomes a correctness risk and the decision would shift toward Gemini's cleaner accuracy.

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2025-06-12 | Initial commit |
