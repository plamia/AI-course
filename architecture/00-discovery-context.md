# 00 — Discovery Context (Four-Layer Architecture Context Pack)
Project: Meridian Retail Group — Omnichannel Commerce Platform
Case: A
Kata: K 4.W.1
Author: Plamena Kichukova
Date: 25.09.2026

## Material lifecycle
- **Owner:** Solution Architect (Meridian program)
- **Source & freshness:** Meridian Case A brief; last_reviewed: 25.09.2026
- **Status:** accepted (draft for downstream katas)
- **Review trigger:** brief revision · stakeholder change · regulation change · tech-stack decision · phase-boundary change

---

## Layer 1 — Business (why the system matters)

- **Scale & investment:** ~**$8.2B** retailer; board-approved **$42M, 18-month** program to unify commerce across **22 countries / 1,400 stores**.
- **Growth history (the root complexity):** MRG grew **through acquisitions** — each region runs its own e-commerce stack (some **Shopify**, some bespoke **.NET**, some **Magento**).
- **Market pressure:** fragmented per-region stacks block cross-region promotions and a unified customer experience; losing ground to online-native competitors.
- **Quantified revenue leak:** **~7% of click-&-collect orders cancelled at pickup** due to **phantom stock** — a direct, measurable loss.
- **Stakeholders:** Board (funding) · **CTO** (strangler-fig mandate, no rip-and-replace) · **Marco / Finance** (SAP finance, revenue recognition) · Regional GMs (22 markets) · Head of CX · Retail Ops.
- **Success measure:** phased unification (one cart, one loyalty, one checkout); phantom-stock cancellation reduced; cross-region promotions enabled.

## Layer 2 — Product (what user & channel it serves)

- **Customer-facing surfaces:** regional web storefronts (Shopify / .NET / Magento) · in-store **POS** · **click-&-collect** pickup · loyalty.
- **Unification promises:** **one cart**, **one loyalty program**, **one checkout** across regions.
- **Key user moments:**
  - Product page: is this item really collectable nearby? (availability — inherited from Design module).
  - Click-&-collect reserve → **pickup at counter** (the phantom-stock failure moment).
  - EU checkout requiring strong customer authentication.
  - Loyalty enrolment: one shopper today has **3–4 fragmented loyalty accounts** across regions.
- **Phase 1 focus:** unified **identity + cart + checkout**.

## Layer 3 — Engineering (how it's built & operated)

- **Target commerce platform:** **commercetools** (headless commerce) — the unification target the regional stacks migrate toward.
- **Identity:** **Auth0** for authentication. *(Note: Auth0 stores identity but does NOT do entity resolution — see Assumption 3.)*
- **Migration strategy:** **Strangler-fig, CTO-mandated — no rip-and-replace; no acceptable downtime window — stores must keep selling throughout.**
- **Legacy that must coexist:** **22 regional stacks** — Shopify (closed SaaS), bespoke **.NET** monolith, **Magento**; plus **6 CRMs** (Salesforce, Hubspot, Dynamics, regional loyalty DBs).
- **System of record:** **SAP ECC** — inventory ground truth (**read-only sync to platform**) + **finance**. *(ECC, not S/4HANA → batch reconciliation.)*
- **Illustrative external providers (stand-ins):** **Stripe** (payments) · **SendGrid** (email). Substitute real vendors when known.

## Layer 4 — Regulatory (what rules shape the system)

| Regulation | Concrete architectural implication |
|---|---|
| **PCI-DSS (Level 1)** | Cardholder data (CHD) must stay inside a documented CDE; 0 CHD/SAD stores or flows outside it → tokenised, isolated payment handling. |
| **PSD2 — SCA** | Strong Customer Authentication on the **EU checkout path** → adds an auth step + **latency cost**; must be a shared checkout capability, not per-stack (see Assumption 4). |
| **GDPR (EU)** | Lawful basis + data-residency for EU PII; **merging customer records across CRMs is a GDPR-sensitive operation** (see Assumption 3). |
| **CCPA (California)** | Consumer data-rights (access/delete/opt-out) for US customers. |
| **Local payment methods** | 22-country checkout must support region-specific payment methods → checkout is not one-size-fits-all. |

---

## Five implicit assumptions the brief never states
Each: the hinting quote → the unstated assumption → what breaks if wrong.

### 1. SAP ECC's inventory is batch-updated, not event-emitting
- **Hint:** *"MRG keeps SAP as inventory ground truth (read-only sync to platform)"* + *"~7% of click-&-collect orders are cancelled at pickup due to phantom stock."*
- **Assumption:** SAP ECC exposes inventory changes as a stream the platform can consume near-real-time. But ECC (not S/4HANA) almost certainly reconciles store inventory in **overnight batch**; POS decrements may sync to SAP hours later.
- **Breaks if wrong:** phantom stock is caused by **store-side** latency. If SAP is hours-stale on store stock, a "live inventory view" fed from SAP is **architecturally incapable** of fixing click-&-collect — you'd need real-time availability from the **POS layer directly**, contradicting "SAP as ground truth." The Phase 2 inventory design collapses on this distinction. **(Highest-severity assumption.)**

### 2. The 22 regional stacks share a reconcilable product/SKU model
- **Hint:** *"each region runs its own e-commerce stack (some Shopify, some bespoke .NET)"* + *"one cart."*
- **Assumption:** the same product in Italy's Magento and the US .NET monolith maps to a common SKU/catalog identity commercetools can unify.
- **Breaks if wrong:** acquisition-grown retailers rarely share SKU schemes, taxonomy, or tax/price models. "One cart" needs a **master-data / product-mapping layer** with per-region overrides — a program of its own, **not scoped in $42M**. Cross-region promotions are impossible without a shared taxonomy first.

### 3. Customer records across the 6 CRMs can be safely de-duplicated into one identity
- **Hint:** *"One customer can have 3–4 fragmented loyalty accounts across regions"* + *"Auth0 for identity."*
- **Assumption:** the same human across Salesforce, Hubspot, Dynamics and regional loyalty DBs can be matched/merged on a reliable key.
- **Breaks if wrong:** 3–4 fragmented accounts means **no shared key today**; matching is probabilistic. Merging wrong records is a **GDPR incident AND a trust disaster** (seeing another person's history/points). **Auth0 stores identity but does not do entity resolution** — that gap is unscoped; without it, "one loyalty" needs a manual consent/reconciliation flow that doesn't scale to $8.2B.

### 4. Legacy stacks can dual-run against shared services during strangler-fig
- **Hint:** *"Strangler-fig pattern mandated by CTO — no rip-and-replace"* + *"no acceptable downtime window — stores must keep selling throughout."*
- **Assumption:** Shopify Plus and the .NET/Magento monoliths can delegate identity/cart/checkout to the new platform while running their own storefronts.
- **Breaks if wrong:** **Shopify Plus is closed SaaS** — you cannot freely swap its native cart/checkout for commercetools. If Shopify can't delegate to shared PSD2/SCA + shared cart, "no rip-and-replace, no downtime" is **internally contradictory** for Shopify regions: either replace Shopify (rip) or run a divergent checkout there (not unified). The strategy silently assumes all 22 stacks are equally open — they aren't.

### 5. The read-only SAP sync is one-directional — but loyalty/promotions need writes back
- **Hint:** *"MRG keeps SAP as inventory ground truth (read-only sync to platform)"* + *"one loyalty program"* + SAP is *"for inventory and finance."*
- **Assumption:** the platform never needs to write to SAP.
- **Breaks if wrong:** loyalty redemptions, promotions, and price adjustments affect **finance and order value** — which live in SAP. If the platform issues discounts SAP finance never sees → **revenue-recognition and reconciliation errors at $8.2B scale** (a Marco/Finance escalation). The clean "read-only" boundary hides a required **write-back / eventing path into SAP finance** that no one has designed.

---

## Self-containment check
Pasting only this file into a fresh session is enough to reason about options in K 4.W.2:
✅ system type (acquisition-grown omnichannel commerce, strangler-fig unification) ·
✅ what it coexists with (SAP ECC batch + finance, 22 heterogeneous stacks incl. closed Shopify, 6 CRMs, commercetools, Auth0) ·
✅ what can quietly go wrong (5 Meridian-specific assumptions with failure modes).

*Result: A one-page, agent-readable context pack — four layers each with ≥3 concrete Meridian
items, plus five brief-specific implicit assumptions with hint quotes and failure modes.*