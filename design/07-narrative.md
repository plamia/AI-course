# 07 — Redesign Narrative (1-Pager)
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.8
Input: 03-decision.md · 05-mockup.html
Author: Plamena Kichukova
Date: 25.09.2026

---

## The problem
Meridian loses **~7% of click-&-collect orders** to cancellation at pickup because the product
page shows a binary **"In stock"** label that doesn't match shelf reality ("phantom stock").
Shoppers discover the failure at the worst possible moment — the counter, after driving over.

## The change
Replace the binary label with a **three-band confidence cue** —
"Likely on shelf" / "Might be low" / "Can't confirm" — plus a **freshness timestamp** and, on
amber/grey, **free cancellation** and a **fallback** (alternative store or home delivery). The
truth about availability moves upstream to the product page, before the shopper commits to travel.

## The benefit
- Shoppers only travel for pickups they can trust → **fewer wasted trips**.
- Honest uncertainty + free cancellation protects conversion instead of killing it.
- Dead-end refunds become **recovery paths** → trust is rebuilt, not destroyed.

## Cost (rough order-of-magnitude)
| Discipline | Cost | Notes |
|---|---|---|
| **Engineering** | **M–L** | New confidence service backed by SAP sync-age; `AvailabilityIndicator` + `StoreList` components; latency budget (p95 ≤ 1.5s). Confidence *model* is the biggest unknown. |
| **Design** | **S** | Change already prototyped (`05-mockup.html`); needs token mapping + production states. |
| **Content** | **S** | Band labels + "Why?" disclosure + honest confirmation/email copy in the agreed tone of voice. |

## Expected outcome metric (one number to move)
> **Cut click-&-collect pickup cancellation from ~7% to < 3%** within one quarter of launch.

Supporting signals:
- Green-band false-positive rate **< 5%** (from AI-AC5 post-pickup feedback).
- Fallback usage tracked on amber/grey (are wasted trips being prevented, not just refunded?).

---

*Result: A 1-page narrative with benefit, engineering/design/content cost, and one testable
outcome number (7% → <3%) the team can check after launch.*