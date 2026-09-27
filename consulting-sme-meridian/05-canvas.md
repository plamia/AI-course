---
case: "Case A — Meridian Retail Group"
date: "2026-09-22"
use_case: "U01 — Pickup-readiness risk predictor"
status: "opportunity hypothesis — thresholds proposed, not observed"
---

# Opportunity Canvas — Predict Pickup-Readiness Risk

## 1. Problem
“I need to know whether my order will actually be ready before I travel to the store.”

**Evidence boundary:** A competitor review reports delayed collection updates, but concerns a coffee machine. The frequency and causes of this problem in Meridian's Italian electronics segment remain unverified. Meridian's case-wide 7% cancellation rate is not a local late-readiness baseline.

## 2. Users
**Primary:** Click-and-collect fulfilment staff and store supervisors handling consumer-electronics orders in selected Meridian stores in Italy.

**Sub-segments:** Staff preparing orders; supervisors resolving exceptions; customer-service agents communicating verified changes.

**Beneficiaries:** Customers ordering online for store collection.

**Proposed business owner:** David Park, Head of Retail Ops. Pilot participation and local ownership require confirmation.

## 3. Value
Reduce the share of eligible orders not ready by their original recorded pickup deadline by **at least 20% relative to a simple-rules control**, without increasing staff handling minutes per order.

**Measurement:** Late-readiness rate = orders ready after the original deadline, or not ready when it expires, divided by eligible orders whose deadlines have elapsed. Do not reset deadlines or exclude post-allocation cancellations to improve results.

This is a proposed success threshold, not a forecast. Confirm that usable deadlines exist before testing.

## 4. Assumptions — Three Falsifiable Claims

**A1 — Usable operational data exists.**
In a consecutive sample of **200 Italian electronics pickup orders** from proposed pilot stores, **≥90%** have a linkable order ID, store, original pickup deadline and recorded readiness outcome.

**Test:** Audit existing records before modelling. Below 90%, pause and address instrumentation; the predictor is not ready for a credible test.

**A2 — ML adds useful warning beyond simple rules.**
On a later, held-out period, at the **same alert volume**, the predictor identifies **≥10 percentage points more late-ready orders** than an agreed order-age/stock-sync threshold rule, with alerts issued **≥2 hours before the original deadline**.

**Test:** Time-based evaluation using only information available at prediction time. Set and freeze the staff-manageable alert budget before comparison. Below the threshold, prefer rules over custom ML.

**A3 — Acting on alerts improves fulfilment.**
In a prospective pilot, model-assisted handling reduces late-readiness by **≥20% relative to the rules-assisted control**, with average handling minutes per order **no higher than control**.

**Test:** Preassign comparable store-days to each approach, with the same intervention options and staffing constraints. Set sample size from the observed baseline before launch. An underpowered or inconclusive result does not pass.

## 5. Solution
Give store teams an early, prioritised warning when an order may miss its pickup deadline, with the relevant evidence and a suggested check. Staff verify stock or preparation status, choose an authorised action and send only confirmed customer updates. Start in shadow mode before a controlled operational pilot. The predictor does not change inventory, issue refunds, move deadlines or promise readiness automatically. Reuse existing platform capabilities where suitable; build custom ML only if it beats simple rules.

**Decision:** Proceed only after all three gates pass. If data fails, instrument first; if prediction fails, use rules; if outcomes fail, redesign the intervention before funding rollout.