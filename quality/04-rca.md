---
case: "Meridian Retail Group — Omnichannel Commerce Platform (Case A)"
feature: "Click & Collect Cross-Channel Flow — Root-Cause Analysis"
date: "2026-09-26"
author: "Functional QA Lead & Architecture Team"
source_defect: "DEF-02 (SAP ECC Timeout at POS Pickup)"
---

# 04-RCA: SAP ECC Timeout & Missing Cache Fallback at POS Pickup

## 1. Defect Summary (from `03-defects.md`)
- **Title:** SAP ECC timeout during store associate QR scan causes POS terminal to hang and aborts pickup confirmation instead of falling back to Redis read-cache.
- **Severity & Priority:** Severity 2 (Major) / Priority 2 (Fix before EU regional rollout).
- **Observed Impact:** When SAP ECC read latency exceeds 2000ms during in-store store associate QR scanning, the Apollo Gateway throws an unhandled HTTP 504 Gateway Timeout error, freezing the POS terminal, forcing a terminal reboot, and blocking the customer from collecting their reserved item.

---

## 2. Root-Cause Analysis & Condition Statement
- **Investigation & Hypotheses Explored:**
  1. *Hypothesis 1 (Network Timeout):* TCP keep-alive settings on the Apollo Gateway are too short. *(Ruled out: network traces show standard 30s keep-alives; the failure is downstream at the adapter sync layer).*
  2. *Hypothesis 2 (Missing Circuit Breaker / Cache Fallback):* The Checkout Service makes synchronous blocking calls to the SAP OData adapter without an active circuit breaker or fallback rule to query the local Redis inventory read-cache when SAP is unresponsive. *(Confirmed: integration logs show zero fallback attempts to Redis upon SAP HTTP 504).*
- **Root-Cause Condition Statement:**
  > The condition that made this bug possible was that the Apollo Gateway checkout resolution path invoked a synchronous, blocking OData call to SAP ECC for real-time inventory verification without an active circuit breaker or stale-cache fallback mechanism configured for timeout events.

---

## 3. Guard Test (Preventative Test Case)
*This guard test exercises the underlying condition (SAP timeout vulnerability) across multiple regional SKUs and payment channels, ensuring the bug cannot return through a neighbouring input.*

- **ID:** GT-01 (Guard Test for SAP Timeout Fallback)
- **Category:** `regression` / `critical-path`
- **Priority:** 1
- **Path / Boundary:** negative / edge
- **Preconditions:** 
  1. Redis inventory read-cache contains last-known valid stock state for test SKU `MRG-SHIRT-BLK-L`.
  2. SAP ECC inventory adapter is artificially throttled to simulate a 3,000ms response timeout.
- **Steps to Reproduce:**
  1. Associate scans customer pickup QR code at POS terminal for an order containing SKU `MRG-SHIRT-BLK-L`.
  2. Apollo Gateway triggers inventory verification; SAP adapter hits timeout threshold (>2,000ms).
  3. Observe system behavior at POS terminal and Gateway response headers.
- **Expected Outcome:** The circuit breaker trips within 2,000ms, bypasses the failing SAP adapter, queries the local Redis read-cache for the last known inventory state, returns a successful response with an amber UI warning ("Stock Unverified — SAP Sync Paused"), and allows the associate to complete counter checkout without crashing or freezing.

---

## 4. Recommended Fix
- **Engineering Recommendation:** Implement a resilience Circuit Breaker pattern (e.g., via Resilience4j or OTel-instrumented gateway policies) on all SAP ECC OData inventory calls with a strict 2,000ms timeout threshold, configured to gracefully degrade to the local Redis inventory read-cache and emit an unverified stock warning banner rather than throwing a blocking HTTP 504 error.

---
- **Owner:** Functional QA Lead & Test Automation Engineer
- **Source & Freshness:** `03-defects.md`; last reviewed 2026-09-26 (Status: Approved)