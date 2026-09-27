# 05-Patterns: Meridian Architecture Placed Pattern Catalog
**Module:** 400 — Architecture (Wide Path)  
**Kata:** K 4.W.6  
**Status:** Approved for Implementation  

---

## 1. Overview
This catalog records the design patterns relied upon for Meridian Phase 1 (Unified Identity, Cart, and Checkout). Unlike generic architectural advice, every pattern here is **placed** on specific containers or relationships from our C4 L2 diagram (`02-containers.mmd`), tied directly to a Meridian constraint, and weighed against a concrete trade-off. Over-engineered or misaligned patterns (such as enterprise Service Meshes or wholesale Event Sourcing) have been explicitly evaluated and rejected for Phase 1.

---

## 2. Placed Pattern Catalog

| Pattern | Where on L2 (Containers & Relationships) | Meridian Constraint Addressed | Trade-Off |
| :--- | :--- | :--- | :--- |
| **Strangler Fig** | Apollo Gateway routing requests between legacy regional stacks (Shopify, Magento, .NET) and commercetools. | CTO Mandate: No Big Bang; 22 regional stacks must coexist and stores must keep selling throughout the 18-month migration. | The Apollo Gateway routing layer becomes a critical single point of dependency; routing rules must be maintained until the final legacy stack is retired in Phase 3. |
| **Outbox** | Cart Service and Checkout Service persisting state changes into PostgreSQL RDS alongside outbox event tables, read by CDC workers for Kafka publishing. | ADR-002 requirement: Reliable asynchronous event publishing without distributed transactions or messaging locks. | Introduces Change Data Capture (CDC) operational overhead and eventual consistency debugging for the junior internal team. |
| **Bulkhead** | Applied across regional payment gateway integration pods, API connection pools, and checkout worker threads. | 22 countries require local payment methods (Postepay in Italy, PayPay in Japan, Klarna in EU); regional payment outages must not cascade. | Increases operational footprint (more worker pods and connection pools to configure and monitor); slightly less efficient resource pooling. |
| **Circuit Breaker** | Placed on outbound HTTP/gRPC relationships from Apollo Gateway and Checkout Service to SAP ECC and Stripe. | SAP ECC batch sync limits and external payment provider volatility; third-party or legacy failures must fail fast rather than cascading. | Requires careful tuning of failure thresholds and timeout windows; premature tripping can degrade user experience during transient network blips. |
| **BFF (Backend for Frontend)** | Placed between client surfaces and the core Apollo Gateway: Web Storefront BFF, Mobile Storefront BFF, and POS Client BFF. | Diverging client requirements (e.g., POS terminal needs specialized loyalty QR scanning and online-cart merging, whereas Web needs standard GraphQL federation). | Three distinct BFF codebases and routing paths to keep aligned with core gateway schema evolution. |
| **CQRS (Command Query Responsibility Segregation)** | Applied to the Inventory domain: Cart/Checkout services handle write commands, while Inventory Read Cache (Redis) handles high-frequency read queries. | High read-to-write ratio for stock availability checks ($\le 200\text{ms}$ p95) without saturating transactional DBs or SAP ECC. | Separation of read and write models introduces data synchronization lag (handled via Kafka events) and schema complexity. |

---

## 3. Evaluated & Explicitly Rejected Patterns for Phase 1

1. **Event Sourcing (Rejected for Phase 1):**
   - *Evaluation:* While useful for complete audit trails, persisting all state as an immutable append-only event log introduces excessive complexity, storage growth, and debugging hurdles for a junior internal MRG product team operating under an 18-month timeline. Deferred to future phases where financial audit mandates specifically require it.
2. **Service Mesh (Istio / Linkerd) (Rejected for Phase 1):**
   - *Evaluation:* Proposed by automated tools for cross-service mTLS and retries. Rejected because it is an infrastructure-level deployment pattern rather than an application design pattern, and its steep operational learning curve would overwhelm the junior internal product team.

---
- **Owner:** Architecture Team
- **Source & Freshness:** Meridian Reference Case A; last reviewed 2026-09-26 (Status: Accepted)