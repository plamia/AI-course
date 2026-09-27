# 02 — Generative Workshop Plan
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.3
Input: 01-journey-map.md · 01-heuristics.md
Author: Plamena Kichukova
Date: 25.09.2026

---

## 1 — The one decision to close

> **Do we show estimated availability with a confidence cue at the product page,
> or do we hide availability until a store physically confirms it?**

This is a real either/or with consequences: showing an estimate risks over-promising on stale data (SAP sync 15–30 min); hiding it until confirmation risks losing the sale to a competitor. The workshop must pick a direction.

**Decision-owner:** Sarah Chen (Head of CX)

---

## 2 — Goals & tasks (decide vs explore)

| Type | Item |
|---|---|
| **DECIDE** | Choose one direction: (A) show confidence-banded estimate at product page, or (B) hide until store-confirmed. |
| **DECIDE** | Agree the minimum fallback the chosen direction must ship (from the K 3.W.1 mandatory-condition list). |
| **EXPLORE** | How to express uncertainty honestly without killing conversion. |
| **EXPLORE** | What the recovery/alternative-store path looks like when confidence is low. |
| **EXPLORE** | Where in the journey the truth about availability should first appear. |

---

## 3 — Timeboxes (30 min)

| Time | Segment | Activity |
|---|---|---|
| 5m | **Frame** | State the decision + show the journey drop-off (Step 7) and the 9 heuristic findings. |
| 15m | **Diverge** | HMW + idea generation (no judging). |
| 10m | **Converge** | Cluster ideas, straw-poll, decision-owner writes the call in one sentence, reads it aloud, facilitator records it. |

---

## 4 — Participants

| Name | Role | Why in the room |
|---|---|---|
| Sarah Chen | Head of CX (decision-owner) | Owns the experience call and signs the decision. |
| David Park | Retail Ops | Knows shelf reality + why stock goes phantom. |
| Marco Rossi | Regional GM | Grounds the fix in real store constraints across regions. |
| [Eng lead] | Engineering lead | Knows SAP sync limits + what's technically feasible. |

---

## 5 — Out of scope

- Pricing
- Loyalty / points reconciliation
- Web↔in-store identity linking

---

## 6 — How-Might-We questions (10) — clustered into 3 themes

### Theme A — Make availability honest at the moment of choice
*(from heuristic findings 1.1, 1.3, 2.1 — the over-confident "In stock" label)*

1. HMW help a shopper on the product page understand that "in stock" is an estimate, not a guarantee — without scaring them off?
2. HMW show *how fresh* the stock information is at the moment the shopper is deciding?
3. HMW let a shopper feel confident a trip is worth it *before* they leave home?
4. HMW express "we're fairly sure" vs "we're not sure" in a way a shopper reads instantly?

### Theme B — Prevent the wasted trip before it starts
*(from heuristic findings 1.2, 2.2 — no reliability signal, no error prevention)*

5. HMW help a shopper choose a store that's actually reliable, not just nearby?
6. HMW catch a low-confidence order at reservation time, before the shopper commits to travel?
7. HMW give the shopper a way to have the item held-and-verified before they set off?

### Theme C — Turn the counter dead-end into a recovery
*(from heuristic findings 3.2, 3.3 — dead-end refund, no user control)*

8. HMW, when an item turns out to be missing, help the shopper still get what they came for?
9. HMW keep a shopper in control at the counter instead of forcing a single refund exit?
10. HMW turn a failed pickup into a moment that rebuilds trust rather than destroys it?

---

## 7 — Ideas (3 per theme) — diverge now, judge in K 3.W.4

### Theme A ideas
- **A1.** Confidence-banded label: "Likely on shelf" (green) / "Might be low" (amber) / "Can't confirm" (grey), with a "stock checked 12 min ago" timestamp.
- **A2.** Replace binary "In stock" with a % + plain-language band ("High confidence — updated 8 min ago").
- **A3.** A small "Why we're not 100% sure" tooltip explaining the 15–30 min sync in one honest sentence.

### Theme B ideas
- **B1.** Per-store reliability badge in the store selector ("This store's stock is usually accurate").
- **B2.** At reservation, if confidence is low, prompt: "Want us to confirm on the shelf before you travel?" (hold-and-verify).
- **B3.** "Reserve with free cancellation" default for amber/grey items, so committing costs nothing.

### Theme C ideas
- **C1.** If missing at counter, instantly show "Available at [Store B], 6 min away — reserve now?" alternative-store rescue.
- **C2.** One-tap "Ship it to me free instead" recovery when the shelf check fails.
- **C3.** Automatic goodwill gesture (small voucher / priority next time) plus a clear apology, to rebuild trust after a failed trip.

---

## 8 — Convergence note (to complete during the run)

> Decision recorded by Sarah Chen: _______________________________________
> (one sentence, read aloud, captured here before the room closes)

If no decision is written in the last 10 minutes → **extend or reschedule**. A workshop that closes no decision is a meeting.

---

*Result: A runnable 30-min workshop anchored to one real decision, with 10 HMWs naming user moments (not features) and 9 divergent ideas ready for impact × effort scoring in K 3.W.4.*