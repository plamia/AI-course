---
opportunity: EU Machinery Corp — ERP Modernisation & AI Sales-Ops
date: 2026-09-27
gate_stage: EPAM Go/No-Go (GNG) Qualification Review
author: Delivery Lead / Opportunity Qualification Team
recommendation: BID WITH CONDITIONS
---

# Opportunity Qualification Memo: EU Machinery Corp

## 1. Fit Scoring (1–5)

| Dimension | Score | Rationale |
| :--- | :---: | :--- |
| **Capability Fit** | **4 / 5** | Strong Azure integration and portal track record; our pre-built sales-ops GenAI pattern covers quote draft and lead triage out of the box. |
| **Delivery Fit** | **3 / 5** | Hard 12-month expiry deadline across 9 sites creates tight scheduling pressure, particularly during legacy middleware cutover. |
| **Commercial Fit** | **3 / 5** | Fixed-price commercial model on custom legacy ERP integration requires strict scope bounding, liability capping, and assumption management. |
| **Strategic Fit** | **5 / 5** | High strategic alignment to expand EU industrial manufacturing accounts and establish an L3 reference architecture for Azure AI + ERP integration. |

## 2. Win Themes
1. **Accelerated Azure Integration Pattern:** Pre-built integration assets and API gateway wrappers for legacy industrial ERP systems, reducing middleware migration effort by 30%.
2. **GDPR & EU AI Act Governed Blueprint:** Production-ready, EU-sovereign Azure AI architecture with built-in PII redactors, prompt guardrails, and audit logging.
3. **Zero-Downtime Industrial Cutover Record:** Verifiable track record of executing phased multi-site manufacturing rollouts without stopping production lines.

## 3. Deal-Breakers (Mandatory GNG Conditions)
1. **Uncapped Liability on Legacy ERP Downtime:** We cannot accept uncapped contractual liability for business interruption caused by legacy system schema failures. *Condition:* Liability cap set at 100% of contract value, with legacy data extraction sign-offs owned by the client.
2. **Unbounded AI Accuracy Guarantees:** The client RFP implies zero-error automated quote generation. *Condition:* Scope must mandate a Human-in-the-Loop (HITL) approval gate for quote drafts above €5,000; our commercial commitment is for system capability, not model perfection without review.

## 4. Top 3 Delivery Risks

| Risk Description | Likelihood | Impact | Mitigation Strategy |
| :--- | :---: | :---: | :--- |
| **1. Undocumented Legacy ERP Integration Logic:** Custom 14-year middleware contains undocumented business logic. | **High** | **High** | Require a 4-week architectural discovery phase at project start with mandatory legacy API exit criteria before locked build. |
| **2. AI Quote Hallucination / Price Drift:** Model generates inaccurate line-item pricing or discount terms. | **Medium** | **High** | Implement strict Azure AI Search RAG guardrails, deterministic price-book lookup tables, and mandatory HITL verification. |
| **3. Multi-Site Rollout Bottleneck across 9 Sites:** Local site teams delay user acceptance testing (UAT). | **Medium** | **High** | Structure rollout into a pilot site followed by 2 phased site clusters, backed by automated integration test suites. |

## 5. Competitive Context

| Competitor Type | Expected Win Theme | Vulnerability / Our Counter-Position |
| :--- | :--- | :--- |
| **Global Systems Integrator** | Massive onshore presence and legacy ERP relationships. | High pricing, slow AI adoption, and heavy boilerplate governance. |
| **Niche EU Cloud Boutique** | Lower daily rates and local Azure agility. | Lack of enterprise multi-site risk controls and limited EU AI Act compliance frameworks. |

## 6. Qualification Recommendation

**BID WITH CONDITIONS.** We recommend progressing to Proposal Assembly subject to securing three mandatory terms during the Q&A window:
1. Liability cap limited to 1x total fee value.
2. Written confirmation that the AI Sales-Ops assistant operates under a Human-in-the-Loop (HITL) workflow for high-value quotes.
3. Commercial structure implemented as a fixed-price milestone contract bound by strict client dependency entry/exit criteria for legacy system access.