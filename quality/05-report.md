---
case: "Meridian Retail Group — Omnichannel Commerce Platform (Case A)"
feature: "Click & Collect Cross-Channel Flow — Executive Test Report"
date: "2026-09-26"
author: "Functional QA Lead"
sources: "00-test-plan.md, 01-test-cases.md, 02-test-data.json, 03-defects.md, 04-rca.md"
status: "Draft — Pending Sign-Off by Eva Müller (VP Digital) & David Park (Retail Ops)"
---

# 05-Test Report: Click & Collect (Phase 1 Rollout)

## 1. Coverage
- **What Was Tested:** We exercised the end-to-end Click & Collect cross-channel flow across 15 test cases (covering 5 realistic and 10 edge-case PII-safe records from `02-test-data.json`). In-scope surfaces tested include: web reservations (`meridian.com`), identity stitching and account merging via Auth0, SAP-sourced inventory checks at store pickup counter, cross-region loyalty-points crediting, and POS terminal pickup confirmation under PSD2 SCA.
- **What Was Excluded (Out of Scope):** SAP ECC inventory ground-truth correctness (owned by Finance / Marco Rossi), legacy regional storefronts (Shopify, Magento, .NET monoliths scheduled for Phase 3 strangler-fig), and async marketing email campaigns (SendGrid). Cross-region multi-currency settlement edge cases were partially sampled but left for Phase 2 hardening.

## 2. Pass Rate & Defect Density
- **Overall Execution Result:** 15 test cases executed | 13 Passed | 2 Failed (Defects logged).
- **Pass Rate Breakdown by Category:**
  - **Smoke / Critical-Path:** 5/5 passed (100%)
  - **Regression:** 3/3 passed (100%)
  - **Edge Case:** 5/7 passed (71.4%) — *Failures concentrated in identity merge collision (`TC-05` / `DEF-01`) and SAP timeout fallback (`TC-08` / `DEF-02`).*
- **Defect Density per Surface:**
  - *Identity Stitching & Account Merge:* 1 Defect / 3 Cases (Density: 0.33)
  - *SAP Inventory Check at Pickup:* 1 Defect / 4 Cases (Density: 0.25)
  - *Web Reservation & Cart:* 0 Defects / 4 Cases (Density: 0.00)
  - *Loyalty-Points Credit:* 0 Defects / 2 Cases (Density: 0.00)
  - *POS SCA Confirmation:* 0 Defects / 2 Cases (Density: 0.00)

## 3. Top 2 Problematic Areas
1. **Identity Merge Collisions (`DEF-01`):** The automated Auth0 identity stitching routine incorrectly merged distinct customer profiles sharing similar email hashes during first in-store pickup, violating GDPR data isolation boundaries and exposing stored payment methods.
2. **SAP ECC Timeout & Missing Cache Fallback (`DEF-02`):** During simulated SAP ECC latency spikes (>2000ms), the Apollo Gateway throw blocking HTTP 504 errors instead of failing over to the local Redis inventory read-cache, freezing POS terminals and halting counter fulfillment.

## 4. 5-Item Improvement Backlog (Ranked by Impact)
1. **Add Held-Stock Token at Reservation (`DEF-02 Mitigation`)**
   - *Why it matters:* Prevents inventory race conditions by writing a held-stock token to the cart during web reservation, ensuring SAP staleness cannot phantom-cancel orders at pickup.
   - *Owner:* Engineering (Tomás Reyes' team) | *Priority:* P1
2. **Enforce 30s SAP Freshness Ceiling with Redis Fallback (`DEF-02 RCA Fix`)**
   - *Why it matters:* Implements a Circuit Breaker pattern with a 2,000ms timeout on SAP OData calls, enforcing a 30s freshness ceiling and falling back to Redis read-cache with a warning banner.
   - *Owner:* Engineering (Tomás Reyes' team) | *Priority:* P1
3. **Single Deterministic Identity-Merge Resolution Rule (`DEF-01 Fix`)**
   - *Why it matters:* Replaces automated heuristic merging with a strict deterministic rule (oldest verified loyalty account wins; ambiguous matches route to manual Customer Service queue) to close Asha Sundaram's cross-customer data leak risk.
   - *Owner:* Engineering + Privacy & Security (Asha Sundaram) | *Priority:* P1
4. **PSD2 SCA Failure Recovery Flow & 10-Minute Hold**
   - *Why it matters:* Prevents immediate cart cancellation when an EU payment SCA challenge times out or fails, holding the reservation for 10 minutes to reduce checkout drop-off in European markets.
   - *Owner:* Engineering + CX (Sarah Chen) | *Priority:* P2
5. **Daily Cross-Region Pickup Telemetry Dashboard**
   - *Why it matters:* Wires real-time telemetry of cross-region pickup attempts, latency distributions, and inventory sync errors into the executive rollout dashboard, giving David Park the operational visibility needed before expanding to country #3.
   - *Owner:* Data Engineering + Retail Ops (David Park) | *Priority:* P3

## 5. Residual Risk
- **Unmitigated Exposure:** If Phase 1 goes live before P1 backlog items #1, #2, and #3 are resolved, Meridian faces a 2%–5% risk of store-level checkout freezes during SAP network jitters and potential GDPR regulatory exposure from identity-merge collisions. 
- **Compensating Controls:** Until P1 fixes are deployed to production, store associates are briefed to use manual floor-verification check sheets when POS terminals encounter timeout errors, and Customer Service agents are placed on standby for manual identity-resolution escalations.

## 6. Release Recommendation
- **Draft Verdict:** **HOLD** (Do not roll out Click & Collect to the next two countries until P1 backlog items #1, #2, and #3 are remediated and re-tested via guard test `GT-01`).
- **Accountable Sign-Off:** 
  - *VP Digital (Eva Müller):* _______________________ *(Pending)*
  - *Head of Retail Ops (David Park):* _______________________ *(Pending)*

---
- **Owner:** Functional QA Lead
- **Source & Freshness:** Full artefact chain (`00` through `04`); last reviewed 2026-09-26 (Status: Draft Release Recommendation)