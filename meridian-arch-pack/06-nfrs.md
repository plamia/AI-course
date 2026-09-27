# 06-NFRs: Meridian Enforceable Quality & Compliance Budgets
**Module:** 400 — Architecture (Wide Path)  
**Kata:** K 4.W.7  
**Status:** Approved for CI Fitness Function Encoding  

---

## 1. Overview
This document establishes 7 enforceable Non-Functional Requirement (NFR) budgets for Meridian Phase 1 (Unified Identity, Cart, and Checkout). Every budget is tied to specific L2 containers, governed by explicit targets, testable via automated CI checks or synthetic probes, and justified directly by Meridian business constraints and past incident learnings.

---

## 2. Enforceable NFR Budget Table

| # | NFR Metric / Invariant | Family | Responsible Container(s) | Target / Threshold | Automated Test Approach (CI / Runtime) | Meridian Justification | Anti-Pattern to Avoid |
|---|------------------------|--------|--------------------------|---------------------|----------------------------------------|-------------------------|------------------------|
| **1** | Cart-to-checkout p95 end-to-end latency | Latency | Apollo Gateway, Cart Service, Checkout Service | p95 < 1500ms (EU region, including PSD2 SCA round-trip) | Automated synthetic checkout probes executed nightly per region in CI pipeline | *"PSD2 SCA for EU payments"* — SCA round-trip dominates regional checkout time | Making synchronous blocking calls to legacy SAP ECC during the checkout hot path |
| **2** | Black Friday peak sustainable throughput | Reliability | Apollo Gateway, Cart Service, Checkout Service | 8000 RPS sustained, 12000 RPS burst (10 min window) | Automated load test (Locust/k6) executed on PR merge to release branch | *"Black Friday 2024 had a 40-minute outage in the EU region"* | Unbounded connection pools and lack of rate-limiting on public API endpoints |
| **3** | Inventory stock accuracy & phantom-stock rate | Quality | Inventory Read Cache (Redis), Kafka stock-event topic, Cart Service | < 2% phantom-stock cancellation rate on click-and-collect orders | Daily automated reconciliation script comparing Redis stock against SAP ECC ground truth | *"-7% of click-and-collect orders cancelled at pickup due to phantom stock"* | Hydrating inventory read-caches lazily on demand instead of event-streaming sync |
| **4** | Platform operational availability | Reliability | Apollo Gateway, Checkout Service, Auth0 SLA | 99.95% uptime per region per month (excluding planned maintenance) | 24/7 uptime monitoring + SLO error-budget alerting (pager trigger at 99.92%) | *"No acceptable downtime window — stores must keep selling throughout"* | Single points of failure in regional database instances without multi-AZ replication |
| **5** | Cloud compute cost per completed checkout | Cost | All Phase 1 hot-path microservices & AWS infrastructure | < $0.04 / completed checkout transaction (excluding third-party payment gateway fees) | Daily AWS Cost and Usage Report (CUR) allocation analysis broken down per container | *"$42M over 18 months budget ceiling"* + digital revenue growth targets | Unbounded auto-scaling groups or unoptimized memory/CPU resource requests |
| **6** | Identity authentication & token verification latency | Latency | Identity Service, Auth0 IDAM | p95 < 250ms for token verification and session refresh | Synthetic auth-flow probes executed every 60 seconds from regional edge nodes | *"Customer creates an account on web, can't use it in-store"* — identity must not gate POS | Making synchronous round-trips to Auth0 for every downstream microservice authorization check |
| **7** | EU SCA compliance & PII data isolation invariant | Security & Compliance | Checkout Service, Stripe Gateway, Data-Masking Pipeline | 100% of EU card payments complete PSD2 SCA; 0 PII fields outside documented PCI-DSS CDE | CI control-conformance static scan + nightly data residency egress audit | *"PSD2 SCA for EU payments"* and *"PCI-DSS Level 1 compliance mandate"* | Storing unmasked cardholder data or unencrypted PII in application logs or shared databases |

---
- **Owner:** Architecture & Quality Engineering Teams
- **Source & Freshness:** Meridian Reference Case A; last reviewed 2026-09-26 (Status: Accepted)