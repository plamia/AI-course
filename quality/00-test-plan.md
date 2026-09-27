---
case: "Meridian Retail Group — Omnichannel Commerce Platform (Case A)"
feature: "Click & Collect Cross-Channel Flow (Phase 1)"
date: "2026-09-26"
author: "Functional QA Lead & Architecture Team"
status: "Draft — Pending Review by David Park (Retail Ops) & Sarah Chen (CX)"
---

# 00-Test Plan: Meridian Click & Collect (Phase 1)

## 1. In Scope
- **Web Reservation & Cart:** Customer item reservation and cart staging on `meridian.com` across priority regional domains.
- **Identity Stitching & Account Merge:** Merging existing in-store loyalty accounts with the customer's web account via Auth0 authentication.
- **SAP-Sourced Inventory Check at Pickup:** Real-time stock verification and inventory decrement at store pickup counter via Redis read-cache / SAP ECC sync.
- **Cross-Region Loyalty-Points Credit:** Automated crediting of loyalty points upon successful in-store QR scan and counter pickup.
- **POS Pickup Confirmation & SCA:** Associate mobile POS terminal processing of customer QR codes and PSD2 SCA card-present/online payment completions.

## 2. Out of Scope & Rationale
- **SAP ECC Inventory Ground-Truth Correctness:** Excluded because inventory master record accounting and ledger reconciliation are owned by Finance (Marco Rossi) and governed by their internal ERP audit controls.
- **Legacy Regional Storks (Shopify / Magento / .NET Monoliths):** Excluded because Phase 1 focuses exclusively on commercetools headless unification; legacy stores being strangled away in Phase 3 are outside test scope.
- **Marketing Email & Automated CRM Campaigns:** Excluded from Phase 1 test scope as SendGrid notification campaigns run asynchronously and do not gate fulfillment or pickup.

## 3. Top-3 Risks
1. **Phantom-Stock Pickup Cancellations:** 
   - *Failure:* In-store inventory synchronization lags between Redis and SAP ECC, allowing a customer to reserve an item online that was already sold in-store.
   - *User Impact:* Customer arrives at the store after a 48-hour window only to be told their item is out of stock, causing intense frustration and immediate cart abandonment.
   - *Business Impact:* Direct revenue loss and worsening of the documented ~7% phantom-stock cancellation rate, harming retail associate trust.
2. **Identity Stitching & Loyalty Collision:** 
   - *Failure:* Probabilistic entity resolution incorrectly merges two distinct customers with similar email hashes or phone numbers into a single Auth0 profile.
   - *User Impact:* Customer A gains access to Customer B's stored payment methods, shipping addresses, and accumulated loyalty points.
   - *Business Impact:* Critical GDPR violation, severe reputational damage, and immediate escalation by Asha Sundaram (Security Lead).
3. **PSD2 SCA Failure on EU Pickup/Checkout Confirmation:** 
   - *Failure:* Regional payment gateway or Stripe SCA challenge fails or times out during mobile POS counter checkout in EU markets.
   - *User Impact:* Store associate cannot complete the sale at the counter, creating long checkout queues and forcing cash/offline workarounds.
   - *Business Impact:* Checkout conversion drop-off and potential regulatory non-compliance fines under European PSD2 mandates.

## 4. Entry Criteria
- Phase 1 microservices and Apollo Gateway deployed to the QA integration environment.
- SAP ECC sandbox environment seeded with realistic regional inventory deltas and stock fixtures.
- Auth0 identity provider and Auth Stubs configured for cross-region loyalty account merging.
- Approved acceptance criteria and user stories loaded into test management tooling.

## 5. Exit Criteria
- Critical-path test suite pass rate ≥ 95% across all regional browser and mobile profiles.
- Zero open Severity-1 (Blocker) defects or unmitigated phantom-stock reconciliation failures on priority test cases.
- Formal sign-off received from David Park (Head of Retail Ops) and Sarah Chen (Head of CX).

---
- **Owner:** Functional QA Lead
- **Source & Freshness:** Meridian Case A Brief; last reviewed 2026-09-26 (Status: Draft)