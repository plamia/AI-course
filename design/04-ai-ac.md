# 04 — AI-Aware Acceptance Criteria
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.5
Input: 03-decision.md
Author: Plamena Kichukova
Date: 25.09.2026

Decided change (from K 3.W.4): Confidence-banded availability label on the product page
("Likely on shelf" / "Might be low" / "Can't confirm") + freshness timestamp, paired with
free cancellation on amber/grey items.

---

## User story

**As a** click-&-collect shopper,
**I want** the product page to show how confident the system is that an item is really on the
shelf at a nearby store, and how fresh that information is,
**so that** I only travel for a pickup I can trust — and never waste a trip on phantom stock.

---

## Base acceptance criteria (supplied — carried forward)

| # | Criterion |
|---|---|
| AC1 | WHEN a product has store stock data, THEN the product page shows an availability indicator per nearby store. |
| AC2 | WHEN no store within range has the item, THEN show "Not collectable nearby" + a delivery option. |
| AC3 | WHEN stock data is missing for a store, THEN omit that store (don't guess). |
| AC4 | WHEN the user taps a store, THEN show last-confirmed time + distance. |

---

## AI-specific acceptance criteria (six clauses — each testable)

### AI-AC1 — Confidence
> WHEN the system computes availability for a store, THEN it maps the result to exactly one of
> three bands using thresholds:
> - **"Likely on shelf" (green)** = confidence ≥ 80% **AND** stock synced ≤ 15 min ago
> - **"Might be low" (amber)** = confidence 50–79% **OR** stock synced 16–30 min ago
> - **"Can't confirm" (grey)** = confidence < 50% **OR** stock synced > 30 min ago
>
> **Testable:** for any item, exactly one band is shown, and the band matches the confidence % and
> sync-age inputs. An item synced 28 min ago can never display green.

### AI-AC2 — Refusal / fallback
> WHEN confidence < 50% **OR** the confidence model returns no result, THEN the system MUST NOT show
> a green/amber estimate; it shows **"Can't confirm — reserve with free cancellation"** and surfaces
> at least one fallback: (a) a nearby store with higher confidence, or (b) a home-delivery option.
>
> **Testable:** in every "Can't confirm" case, a free-cancellation reserve OR an alternative path is
> present. Zero dead-end grey states allowed.

### AI-AC3 — Latency
> WHEN the shopper opens a product page, THEN the availability band renders within **1.5 s (p95)**.
> IF the confidence service does not respond within **3 s**, THEN the page shows the grey
> "Can't confirm" state with a retry — it never spins indefinitely.
>
> **Testable:** p95 render ≤ 1.5 s measured in monitoring; timeout falls back to grey at 3 s, verified
> by fault injection.

### AI-AC4 — Disclosure
> WHEN any availability band is shown, THEN it MUST display the freshness timestamp
> ("stock checked X min ago") **AND** a one-tap "Why?" tooltip that states in plain language that the
> figure is an estimate based on data synced every 15–30 minutes.
>
> **Testable:** every band renders a timestamp and an accessible "Why?" affordance; the disclosure text
> is present in the DOM and screen-reader reachable. No band is shown as an unqualified fact.

### AI-AC5 — Feedback
> WHEN a shopper completes or cancels a pickup, THEN the system offers a one-tap
> **"Was it on the shelf? Yes / No"** prompt, and logs the response against the item + store + band
> shown, so estimate accuracy can be measured per band.
>
> **Testable:** feedback control appears post-pickup; each response is stored with item, store, band,
> and timestamp; accuracy-by-band is queryable (target: green-band false-positive rate < 5%).

### AI-AC6 — Negative AC
> The system **MUST NOT**:
> - show **"In stock"** or any absolute/binary availability wording anywhere in the flow;
> - display a **green** band on stock synced **> 15 min ago**;
> - reserve an amber/grey item **without** the free-cancellation option attached;
> - send the "Ready for collection" email **before** a confidence band ≥ 50% is confirmed at fulfilment.
>
> **Testable:** each forbidden behaviour has a corresponding failing test; presence of any is a release
> blocker.

---

## Three-Amigos check (to complete before build)

| Role | Confirms |
|---|---|
| Product / BA | Story + bands reflect the decided change and business goal (cut ~7% cancellation). |
| Engineering | Thresholds (80% / 50% / 15 / 30 min / 1.5 s / 3 s) are feasible against SAP sync. |
| QA | Every clause above is falsifiable and has a test case. |

---

## Falsifiability audit

Every clause carries a number, threshold, or observable condition:
AI-AC1 (80% / 50% / 15 / 30 min bands) · AI-AC2 (< 50% → fallback present) · AI-AC3 (1.5 s p95 / 3 s timeout)
· AI-AC4 (timestamp + "Why?" present in DOM) · AI-AC5 (< 5% green false-positive) · AI-AC6 (forbidden list, each a blocker).

---

*Result: A user story plus six testable AI-AC clauses that define how the availability assistant must
behave when it is unsure — turning "the estimate should be accurate" into thresholds QA can test.*