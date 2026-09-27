---
case: "Meridian Retail Group — Omnichannel Commerce Platform (Case A)"
feature: "Click & Collect Cross-Channel Flow — Defect Log"
date: "2026-09-26"
author: "Functional QA Lead"
execution_method: "Playwright MCP Browser Agent (Path A) + Manual Trace Review"
source_cases: "01-test-cases.md (TC-01, TC-04, TC-08, TC-13)"
source_data: "02-test-data.json"
---

# 03-Defects: Click & Collect (Phase 1 Execution)

## Execution Summary
- **Cases Executed:** 4 (TC-01: Milano Happy Path, TC-04: First In-Store Pickup Account Merge, TC-08: SAP Timeout / Fallback at POS, TC-13: EU PSD2 SCA Payment Completion).
- **Pass Rate:** 2 Passed (`TC-01`, `TC-13`), 2 Defect Failures Logged (`TC-04`, `TC-08`).
- **Defect Count:** 2 confirmed actionable defects (1 Severity-1 Blocker, 1 Severity-2 Major).

---

## Defect Log (Sorted by Priority)

### DEF-01: Identity Stitching Collision Assigns Wrong Customer Loyalty Profile and Payment Methods
- **Title:** Identity merge collision links two distinct customer records during first in-store pickup, exposing Customer B's stored payment tokens to Customer A.
- **Steps to Reproduce:**
  1. Open `meridian.com` and log in as guest checkout using `alex.smith.collision@meridian-test.com` (`cust_us_collision_991`, `LY-US-COLLISION-DUP`).
  2. Complete item reservation for in-store pickup at NY store (`store_us_ny_03`).
  3. Store associate scans customer QR code at POS terminal.
  4. Identity Service invokes Auth0 account merge routine against legacy CRM records.
- **Expected Result:** System detects duplicate loyalty profile match, flags account for manual customer service review, and blocks automated merging to prevent cross-customer data exposure.
- **Actual Result:** Identity Service automatically merges the guest session into the pre-existing loyalty profile of a different customer with matching email hash, granting Customer A access to Customer B's saved credit card suffix and loyalty point balance.
- **Severity:** 1 (Blocker — GDPR violation & unauthorized financial data exposure).
- **Priority:** 1 (Act immediately; blocks US pilot rollout).
- **Reproduction Context:** Environment: QA Integration Cluster; Build: v1.4.2-rc3; Device: POS Tablet (Chrome/Playwright Agent). Frequency: 100% reproducible on collision dataset.
- **Evidence Attached:** Step trace log `playwright_trace_tc04_collision.zip`, Network request JSON payload showing merged token response.

---

### DEF-02: SAP ECC Timeout at POS Pickup Terminates Transaction Without Local Cache Fallback
- **Title:** SAP ECC inventory read timeout during store associate QR scan causes POS terminal to hang and aborts pickup confirmation instead of falling back to Redis read-cache.
- **Steps to Reproduce:**
  1. Store associate scans customer pickup QR code for order `ord_berlin_00831` at Berlin store (`store_de_berlin_04`).
  2. Apollo Gateway attempts inventory verification against SAP ECC adapter while SAP read latency exceeds 2000ms (simulated outage).
  3. SAP adapter request times out without triggering circuit breaker fallback.
- **Expected Result:** Apollo Gateway detects SAP timeout, trips circuit breaker, falls back to the local Redis read-cache, and displays an amber "Stock Unverified — Confirm with Floor Staff" banner while permitting counter checkout.
- **Actual Result:** POS terminal throws an unhandled HTTP 504 Gateway Timeout error, freezing the associate screen and forcing a hard terminal reboot, preventing the customer from collecting their reserved item.
- **Severity:** 2 (Major — Store-wide operational disruption during high-traffic windows).
- **Priority:** 2 (Fix before EU regional rollout).
- **Reproduction Context:** Environment: QA Integration Cluster; Build: v1.4.2-rc3; Network Condition: Simulated 2000ms latency on SAP OData adapter. Frequency: 100% reproducible under timeout conditions.
- **Evidence Attached:** Playwright execution step trace `playwright_trace_tc08_sap_timeout.json`, Gateway exception log snippet `ERR_SAP_TIMEOUT`.

---

## Unresolved Observations / Stories (Non-Actionable Leads)
- **Story-01:** When an EU customer completes a PSD2 SCA challenge via Stripe on mobile POS (`TC-13`), the biometric redirect modal occasionally takes up to 4,200ms to dismiss after successful authentication. No payment failure or data loss occurred, but associate UX is sluggish. Logged as a performance backlog item for Module 700.

---
- **Owner:** Functional QA Lead
- **Source & Freshness:** `01-test-cases.md`, `02-test-data.json`; last reviewed 2026-09-26 (Status: Logged)