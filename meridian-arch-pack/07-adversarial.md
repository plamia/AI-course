# 07-Adversarial: Meridian Phase 1 Pre-Mortem & Stress Review
**Module:** 400 — Architecture (Wide Path)  
**Kata:** K 4.W.8  
**Status:** Approved for Risk Acceptance & Phase 1 Hardening  

---

## 1. Overview
This document records the findings of an adversarial pre-mortem stress test against the Meridian Phase 1 Architecture Pack (`00` through `06`). Conducted via an independent session evaluating the system without confirmation bias, this review identifies the top 3 failure modes under 10× Black Friday load, hostile EU checkout inputs, and prolonged partner outages (SAP ECC & Stripe). Each break is paired with an actionable architectural patch or an explicitly named owner accepting the residual risk.

---

## 2. Stressor A: 10× Black Friday Peak Load (80,000+ RPS Surge)

| # | Failure Mode & Component | First User-Facing Symptom | Resolution: Patch vs. Accepted Risk |
|---|--------------------------|---------------------------|-------------------------------------|
| **A1** | **Inventory Read Cache (Redis) Thundering Herd:** When promotional flash-sale events drop, simultaneous cache expiry for top SKUs causes thousands of concurrent cache misses cascading directly into the PostgreSQL platform database and synchronous SAP fallbacks. | Store associates and shoppers experience spinning loaders (latency spikes > 4,000ms), followed by 504 Gateway Timeouts on product detail pages. | **Patch:** Implement asynchronous cache re-warming prior to flash-sale events and probabilistic early expiration (XFetch algorithm) in Redis read queries. |
| **A2** | **Kafka Outbox Producer Bottleneck:** Under massive checkout volume, database transaction throughput on the PostgreSQL Outbox table saturates disk I/O, delaying event publishing to Kafka and stalling inventory reconciliation. | Checkout succeeds, but confirmation emails and inventory stock decrements lag by several hours, creating false inventory availability. | **Patch:** Partition the outbox table by tenant/region and increase CDC Debezium worker polling threads; introduce backpressure on Checkout Service. |
| **A3** | **Apollo Gateway Thread Pool Starvation:** Heavy GraphQL query nesting from mobile and web storefronts exhausts the Gateway Node.js event loop during peak spikes. | Global API unavailability; all web and mobile storefronts fail to load, even for static browsing. | **Accepted Risk (Owner: Tomás Reyes, Lead Architect):** GraphQL query complexity analysis and depth limiting enforced at Gateway; any deeply nested queries exceeding cost limits will be rejected with HTTP 400 during peak. |

---

## 3. Stressor B: Hostile EU Checkout Inputs & PSD2 SCA/PII Tampering

| # | Failure Mode & Component | First User-Facing Symptom | Resolution: Patch vs. Accepted Risk |
|---|--------------------------|---------------------------|-------------------------------------|
| **B1** | **Replayed Payment Webhook Attacks:** Malicious actors intercept and replay Stripe asynchronous payment confirmation webhooks to trigger duplicate order fulfillment without secondary charges. | Inventory phantom-drains and multiple duplicate fulfillment orders generated for single payments. | **Patch:** Enforce strict cryptographic signature verification (Stripe-Signature header) and idempotency key caching in Redis for all inbound webhook endpoints at the API Gateway. |
| **B2** | **Loyalty-QR Injection at POS Terminals:** Compromised store-associate tablets inject malicious SQL/NoSQL payloads or forged JWT tokens into the `getCustomerCartByQR` GraphQL query parameter. | Unauthorized disclosure of PII, loyalty point theft, or privilege escalation across customer accounts. | **Patch:** Mandate strict parameter sanitization, RBAC scoping (`pos:cart:read`), and short-lived, hardware-bound associate session tokens verified by the Identity Service. |
| **B3** | **PSD2 SCA Bypass & Tampering:** Malicious EU shoppers manipulate client-side state during the 3D Secure / SCA challenge redirect to prematurely mark failed authentication as successful. | Checkout Service accepts unauthenticated payment tokens, resulting in high chargeback rates and PSD2 regulatory fines. | **Accepted Risk (Owner: Asha Sundaram, Security & Compliance Lead):** Checkout Service will strictly reject webhook settlement confirmations that lack cryptographic proof of SCA completion issued directly from Stripe's ACS server. |

---

## 4. Stressor C: Partner Outages (SAP ECC Down for 2 Hours / Stripe Degraded)

| # | Failure Mode & Component | First User-Facing Symptom | Resolution: Patch vs. Accepted Risk |
|---|--------------------------|---------------------------|-------------------------------------|
| **C1** | **SAP ECC Batch-Sync & Fallback Exhaustion:** When SAP ECC goes offline during a 2-hour batch window, inventory cache misses trigger continuous inline fallback queries that timeout and exhaust connection pools. | Store associates scanning QR codes at the POS receive unverified inventory errors ("Stock Unknown"), halting in-store click-&-collect fulfillment. | **Patch:** Implement an automated Circuit Breaker on SAP ECC calls. When SAP is detected down, trip the breaker immediately and fall back to last-known Redis cache state with an explicit UI banner: *"Live SAP sync paused; inventory based on last known cache."* |
| **C2** | **Stripe API Degradation / Latency Spikes:** Stripe payment authorization latency exceeds 10 seconds, blocking checkout worker threads across the platform. | Shoppers clicking "Place Order" see buttons freeze, leading to double-clicks, duplicate payment intents, and cart abandonment. | **Patch:** Implement asynchronous payment processing queues for non-instant checkout or fail-fast circuit breakers with friendly user messaging: *"Payment gateway is experiencing delays; please retry in 60 seconds."* |
| **C3** | **Regional CRM Sync Failure:** Regional CRMs (Salesforce/Dynamics) fail to sync customer loyalty updates during network partitions. | Loyalty points earned during offline store purchases fail to reflect in the customer's online account immediately. | **Accepted Risk (Owner: David Park, Retail Operations Lead):** Accept eventual consistency for loyalty point balance updates during regional CRM outages; offline transactions will buffer locally and sync automatically via Kafka once CRM connectivity is restored. |

---
- **Owner:** Architecture & Engineering Teams
- **Source & Freshness:** Meridian Reference Case A Adversarial Review; last reviewed 2026-09-26 (Status: Accepted)