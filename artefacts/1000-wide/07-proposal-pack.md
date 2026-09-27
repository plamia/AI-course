---
buyer: EU Machinery Corp
project: ERP Integration, Customer Portal & AI Sales-Ops Modernisation
proposal_value: €1,738,000
commercial_model: Fixed-Price Milestone Contract
status: RECONCILED & APPROVED FOR DEFENCE
date: 2026-09-27
author: Delivery Manager / Bid Team
---

# Enterprise Proposal Pack: EU Machinery Corp Modernisation

## Section 1: Executive Summary
*(See standalone file [`07-exec-summary.md`](./07-exec-summary.md) for full executive brief)*

---

## Section 2: RFP Response Matrix

Every evaluation criterion from `00-rfp.md` is addressed below with direct cross-references to supporting upstream delivery evidence (Modules 100–900):

| RFP Evaluation Criterion | Weight (%) | How EPAM Meets the Requirement | Supporting Evidence & Artefacts |
| :--- | :---: | :--- | :--- |
| **1. Solution Fit & Architecture** | **35%** | Decoupled Azure Integration Services architecture (APIM/Logic Apps), React B2B portal, and Azure OpenAI RAG engine with Human-in-the-Loop workflows. | `02-solution.md`<br>Architecture Pack (M400)<br>Feature Evidence Chain (M500) |
| **2. Commercials & Price Competitiveness** | **25%** | Transparent fixed-price milestone model (€1,738,000) based on 99.0 FTE-Months. Sourced token costs (€25k) and separate contingency (€176.8k). | `03-staffing.xlsx`<br>`04-estimate.xlsx`<br>Cloud Platform Cost Model (M800) |
| **3. Team Capability & References** | **20%** | Blended delivery team led by Principal DM Marcus Vance (30% On / 40% NS / 30% Off). Verified manufacturing integration reference from Atlas Copco. | `03-staffing.xlsx`<br>Opportunity Brief (M100) |
| **4. AI Governance & Responsible AI** | **10%** | Pre-approved DIAL framework, EU-sovereign Azure regions, PII redactors, and independent EU AI Act audit by sub-vendor CyberGuard EU. | `06-ai-native.md`<br>Security Evidence Pack (M900) |
| **5. Delivery Risk & Governance** | **10%** | Explicit 15% contingency reserve, monthly CDO Steering Committee, bounded assumption register, and protected 20% AI Champion network. | `04-estimate.xlsx`<br>`05-plan.md`<br>QA Test Report (M600) |
| **TOTAL** | **100%** | | |

---

## Section 3: Reconciled Component Summaries & Artefact Links

### 3.1 Qualification & Stance
* **Status:** Bid with Conditions (GNG Approved).
* **Key Terms:** 1x contract liability cap, mandatory HITL UI gate for quotes >€5k, 5-day UAT auto-acceptance clause.
* **Source File:** [`01-qualification.md`](./01-qualification.md)

### 3.2 Technical Solution & Outsourced Capability
* **Compliance Shape:** Turn-key (EPAM-delivered solution on client Azure tenant).
* **Delivery Arc:** 4 Phases across 12 months (Discovery $\rightarrow$ Integration/Portal Build $\rightarrow$ AI Engine/Audit $\rightarrow$ Multi-Site Cutover).
* **Outsourced Sub-Vendor:** CyberGuard EU (EU AI Act Regulatory Compliance & Pen-Testing). Gated under continuous Month 6–9 reviews with a hard exit stop prior to Phase 4 rollout.
* **Source File:** [`02-solution.md`](./02-solution.md) & [`02-review.md`](./02-review.md)

### 3.3 Staffing Plan
* **Selected Variant:** **Balanced Variant (99.0 FTE-Months)** — 30% Onshore / 40% Nearshore / 30% Offshore.
* **Ramp Profile:** Staggered onboarding (35% M1 $\rightarrow$ 70% M2 $\rightarrow$ 100% M3).
* **Source Sheet:** [`03-staffing.xlsx`](./03-staffing.xlsx)

### 3.4 Commercial Estimate & Financials
* **Base Effort:** €990,000 (99 FTE-Mo @ €10,000/mo avg blended rate).
* **Delivery Impacts:** €118,800 (Ramp lag 5%, Sub-vendor coordination 3%, Client dependency wait 4%).
* **Direct Pass-Throughs:** €45,000 (CyberGuard EU Audit) + €25,000 (Azure OpenAI Inference Budget).
* **Direct Delivery Cost:** **€1,178,800**.
* **Risk Contingency Reserve:** **€176,820** (15% explicit line item).
* **Target Gross Margin:** **€382,380** (22% gross margin).
* **Total Proposal Fixed Price:** **€1,738,000**.
* **Source Sheet:** [`04-estimate.xlsx`](./04-estimate.xlsx)

### 3.5 Delivery & Rollout Plan
* **Hard Cutover Date:** Month 12 (Day 360) across all 9 EU sites.
* **Executive Sponsors:** Client Chief Digital Officer & EPAM VP of Industrial Delivery.
* **Change Management:** 3 AI Champion roles with 15–20% budgeted protected time.
* **Source Files:** [`05-plan.md`](./05-plan.md) & [`05-timeline.md`](./05-timeline.md)

### 3.6 AI-Native Delivery Commitments
* **Maturity Target:** L2 Baseline by Month 6 $\rightarrow$ L3 Frontier by Month 12 across all 6 SDLC phases.
* **Tooling Baseline:** DIAL, GitHub Copilot Enterprise, CodeMie, M365 Copilot (All EPAM Pre-Approved).
* **Non-Automated Boundary:** Binding contracts, high-value quotes (>€5k), architectural sign-offs, and performance management are 100% human-owned.
* **Source File:** [`06-ai-native.md`](./06-ai-native.md)

---

## Section 4: Cross-Artefact Reconciliation Audit Log

During assembly, the bid team audited the draft artefacts for internal contradictions and applied the following synchronisations:

1. **Estimate vs. Staffing Reconciliation:** Verified that `04-estimate.xlsx` calculates base effort directly from the **Balanced Staffing Variant (99.0 FTE-Months)** in `03-staffing.xlsx` (€990,000).
2. **Plan vs. Solution Phase Alignment:** Synchronised phase names and durations between `02-solution.md` and `05-plan.md` (Phase 1: M1–M2; Phase 2: M3–M7; Phase 3: M8–M9; Phase 4: M10–M12).
3. **AI Tooling Budget Reconciliation:** Confirmed that the Azure OpenAI token and vector search inference costs referenced in `06-ai-native.md` are explicitly funded as a **€25,000** line item in `04-estimate.xlsx` sourced from Module 800 gateway telemetry logs.
4. **Commercial Model vs. RFP Constraint:** Corrected early draft tendencies toward T&M, aligning the proposal to a **Hybrid Milestone Fixed-Price Contract** to honor `00-rfp.md` constraints while bounding risk via `04-estimate.xlsx` assumptions.

---

## Section 5: Open-Items Log (Pre-Bid Defence Steering Inputs)

| Item ID | Open Item Description | Impact / Severity | Target Resolution Date | Accountable Owner |
| :--- | :--- | :--- | :--- | :--- |
| **OPEN-01** | Confirm client Azure enterprise admin access turnaround SLA during Day 14 Q&A window. | Low Schedule Risk | Day 14 (Q&A Close) | Delivery Manager |
| **OPEN-02** | Formalize Client PO sign-off workflow for Phase 1 price-book data cleansing. | Medium Scope Risk | Day 30 (Submission) | Lead BA |
| **OPEN-03** | Finalize Data Processing Addendum (DPA) execution terms with sub-vendor CyberGuard EU. | Low Compliance Risk | Day 45 (Shortlist) | Legal / Commercial Lead |