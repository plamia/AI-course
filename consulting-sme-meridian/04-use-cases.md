---
case: "Case A — Meridian Retail Group"
date: "2026-09-22"
input: "03-research-audit.md"
status: "provisional shortlist — validation required"
---

# Ten AI Use Cases — Meridian Italy

## 1. Audited Starting Point

**Scope:** Italian consumer electronics click-and-collect.

| Pain | Audited basis | Boundary |
|---|---|---|
| P1 — Fulfilment-status visibility | Customer reports describe unclear delivery status and a delayed collection update. [C12; C14] | Root cause, prevalence and relevance to Italian electronics pickup remain unverified. |
| P2 — Dependable communication and service recovery | A customer reports missing communication; Unieuro publishes pickup and payment routes. [C11; C15] | A competitive performance gap is not established. |
| P3 — Payment-change readiness | An official announcement describes a provisional payment-services agreement. [C09] | Current legal status and Meridian-specific implementation needs remain unverified. |

P1 and P2 are adjacent: P1 concerns knowing the operational state; P2 concerns communicating and acting on it.

**Guardrails:** No new research. No invented uplift or savings. Meridian's 7% cancellation rate is reference-case data, not a validated Italian baseline. SAP remains the inventory system of record; legacy CRMs coexist; no downtime or uncontrolled production writes are acceptable.

## 2. Scoring Method

**Value:** 1 = weak/indirect benefit; 3 = meaningful but uncertain benefit; 5 = potentially material impact on fulfilment outcomes.

**Feasibility:** 1 = major blockers; 3 = plausible pilot with integration and governance work; 5 = operationally ready with demonstrated data access, ownership and controls.

**Priority score = Value × Feasibility.**

Scores are comparative judgments, not ROI estimates. No candidate receives feasibility 5 because operational readiness has not been demonstrated.

## 3. Ten Candidates and Scores

| ID | Pain / AI type | Candidate and boundary | V | F | V×F |
|---|---|---|---:|---:|---:|
| U01 | P1 / Classical ML | **Pickup-readiness risk predictor:** predict late readiness from order events, store workload and stock-sync freshness; flag uncertainty, not guaranteed availability. | 5 | 3 | 15 |
| U02 | P2 / Generative | **Grounded status-message assistant:** draft Italian customer updates from verified order events; no invented dates or autonomous promises. | 4 | 4 | 16 |
| U03 | P2 / Agentic | **Exception-resolution coordinator:** gather order context, identify an accountable team, create approved tasks and track acknowledgement. No autonomous refunds or inventory changes. | 4 | 3 | 12 |
| U04 | P1 / Classical ML | **Stock-discrepancy risk detector:** identify suspicious SAP-to-commerce availability patterns and prioritise manual checks; never overwrite SAP. | 5 | 2 | 10 |
| U05 | P1 / Generative | **Order-timeline summariser:** turn verified events into a cited support-agent timeline, explicitly marking conflicting or missing data. | 3 | 4 | 12 |
| U06 | P1 / Agentic | **Cross-system evidence collector:** retrieve order, stock-sync and store-task records to assemble a discrepancy investigation packet. Read-only access. | 4 | 2 | 8 |
| U07 | P3 / Classical ML | **Payment-flow drift detector:** flag unusual changes in authentication and payment-error patterns for analyst review, not legal conclusions. | 2 | 2 | 4 |
| U08 | P3 / Generative | **Approved-policy comparison assistant:** compare compliance-approved requirements with checkout documentation; cite gaps for legal review. | 2 | 3 | 6 |
| U09 | P3 / Agentic | **Payment-control evidence collector:** assemble approved configuration, test and approval records into an audit packet; no compliance sign-off. | 3 | 2 | 6 |
| U10 | P2 / Generative | **Recurring failure-pattern analyst:** cluster redacted support cases and order-event narratives into evidence-linked patterns for product and operations teams. | 4 | 3 | 12 |

### One Rationale per Dimension

| ID | Value rationale | Feasibility rationale |
|---|---|---|
| U01 | Early warning could help teams intervene before a missed pickup promise; baseline and intervention benefit require validation. | Needs linked historical events, trustworthy readiness labels and a defined alert owner. |
| U02 | Clearer updates may reduce uncertainty and avoidable contacts; effect must be measured. | A draft-only pilot is bounded, but requires trusted status inputs, Italian-language review and delivery controls. |
| U03 | Accountable exception handling targets service recovery rather than adding another status display. | Requires CRM/task integration, permissions, escalation rules and staff adoption; begin in shadow mode. |
| U04 | Real discrepancy detection could prevent failed promises if phantom stock is a material local cause. | Ground truth and discrepancy labels are uncertain; SAP synchronisation and false-positive workload complicate deployment. |
| U05 | A consolidated timeline may shorten investigation effort without making unsupported customer promises. | Read-only summarisation is bounded, but conflicting identifiers and event semantics still need resolution. |
| U06 | Evidence gathering may reduce manual investigation work across fragmented systems. | Broad access, identity matching and inconsistent logs make integration difficult; value beyond U05 needs proof. |
| U07 | Operational anomalies may matter, but they do not establish readiness for a particular regulatory change. | Requires payment telemetry, sufficient labelled incidents, security approval and strict data minimisation. |
| U08 | Could support analysts, but current obligations and Meridian-specific gaps are not established. | Document assistance is plausible only with approved, versioned requirements and mandatory legal review. |
| U09 | Traceable evidence may reduce audit preparation effort once relevant controls are defined. | Depends on control ownership, repository access and accepted evidence formats that are not yet confirmed. |
| U10 | Recurring patterns could guide targeted fixes instead of relying on isolated complaints. | Can start offline with redacted cases, but needs a labelled sample, stable taxonomy and human verification of clusters. |

## 4. Deduplication and Partial-Overlap Review

**Dedup prompt:** Which of these are duplicates or near-duplicates? Consolidate near-duplicates; flag partial overlaps for review.

**Result:** Ten generated → ten retained. No full duplicates after applying the boundaries below.

| Partial overlap | Resolution |
|---|---|
| U01 / U04 | Keep separate: U01 predicts late readiness; U04 detects possible inventory discrepancies. Neither assumes the other is the cause. |
| U02 / U05 | Keep separate: customer-facing updates versus internal investigation timelines. Share event-access components where useful. |
| U03 / U06 | Keep separate: U03 coordinates accountable action; U06 retrieves and reconciles evidence. Avoid building duplicate connectors. |
| U03 / U10 | Keep separate: live exception handling versus periodic analysis of recurring problems. |
| U08 / U09 | Keep separate: interpretation assistance versus evidence assembly. Neither makes legal decisions. |

These boundaries resolve the partial overlaps for this draft; implementation ownership should confirm them before funding.

## 5. Initial Ranking

1. U02 — 16
2. U01 — 15
3. U03 — 12
4. U10 — 12
5. U05 — 12
6. U04 — 10
7. U06 — 8
8. U09 — 6
9. U08 — 6
10. U07 — 4

**Tie-break:** Prefer a distinct, actionable contribution to the audited opportunity over a supporting summarisation capability. U03 addresses live recovery; U10 supports recurring operational fixes; U05 is an enabling component.

## 6. Commodity Check and Swap

This is a bounded build-versus-configure assessment, not new vendor research. Multiple-vendor availability, actual switching costs and licensing have not been verified.

| Candidate | Commodity assessment | Decision |
|---|---|---|
| U02 — Status-message assistant | **Likely commodity at the generic capability level.** Event-grounded drafting is a reusable assistant pattern; integration alone does not establish novelty. | Remove from the custom-build top three. Assess existing platform capabilities before considering a build. |
| U01 — Readiness risk predictor | **Potentially non-commodity only in its Meridian-specific application:** labels, event semantics, calibration and operational thresholds. Predictive fulfilment tools may already cover the need. | Retain provisionally; compare existing platform features and a rules-based baseline before custom ML. |
| U03 — Exception coordinator | **Potentially non-commodity in cross-system responsibility and escalation logic.** The orchestration engine itself is not novel. | Retain provisionally; configure an existing workflow platform where possible. |
| U10 — Failure-pattern analyst | **Generic clustering is commodity-prone.** Potential custom value lies in linking patterns to Meridian events, an agreed taxonomy and accountable fixes. | Replacement for U02, conditional on proving value beyond existing analytics. Otherwise configure rather than build. |

**Swap applied:** U02 out → U10 in.

No candidate is declared demonstrably novel. The shortlist survives this preliminary check only as a set of bounded, context-specific opportunities—not as approval to build three bespoke AI products.

## 7. Final Top Three

| Rank | Candidate | Score | First validation gate |
|---|---|---:|---|
| 1 | **U01 — Pickup-readiness risk predictor** | 15 | Confirm usable readiness labels and an action owner; test whether ML improves on simple age/threshold rules. |
| 2 | **U03 — Exception-resolution coordinator** | 12 | Confirm routing rules and ownership; evaluate shadow-mode recommendations before allowing task creation. |
| 3 | **U10 — Recurring failure-pattern analyst** | 12 | Compare evidence-linked clusters with manual categorisation and existing analytics on a redacted sample. |

**Carry forward to Kata 1.6:** U01 as the provisional lead candidate, not an approved investment.

**Confirm before executive review:** Local problem size, data availability, operational ownership, incremental benefit over non-AI alternatives, and existing product capabilities. If a candidate fails these gates, rescore or replace it rather than defending the original ranking.