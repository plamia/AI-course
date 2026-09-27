# PRD — AI Availability Assistant for Click-&-Collect

**Product:** Meridian Omnichannel Commerce Platform · **Date:** 2026-09-26 · **Status:** Ready for build

---

## Problem
Meridian loses ~7% of click-&-collect orders to cancellation at pickup because online
stock counts don't match shelf reality ("phantom stock"). A second, silent loss occurs
when uncertain shoppers abandon the reservation entirely.

## Vision
For click-&-collect shoppers who reserve online to avoid a wasted trip, the AI
availability assistant replaces an unreliable stock count with a **confidence-graded
collectability verdict** — so shoppers only reserve what they can actually pick up, and
Meridian recovers lost orders without shrinking the channel.

## Target User
Click-&-collect shoppers who reserve online specifically to avoid a wasted trip —
covering both the *committed reserver* lost at pickup (cancellation) and the
*fence-sitter* lost at reservation (abandonment).

## Success Metric
Phantom-stock cancellations fall from **7% baseline → ≤ 2%** within 90 days of rollout,
measured from the order-management cancellation-reason log, reported **per-region**.
**Guardrail:** click-&-collect order volume stays within **±3%** of pre-launch baseline
(so the metric can't be "won" by killing the channel).

## Top Stories & Acceptance Criteria

**S2 — Communicate uncertainty honestly (the refusal contract)**
- Below the display threshold → shopper sees "unknown", never "likely collectable".
- Missing/malformed confidence → default to "unknown" (fail-safe, never fail-open).
- NFR: "likely collectable" is correct ≥ 95% on the golden set.

**S1 — Show a collectability verdict**
- Shows one of three verdicts: "likely collectable" / "check before you go" / "unknown".
- Never shown as a raw stock count. SAP unreachable → "unknown — check before you go".
- NFR: verdict renders p95 < 1s.

**S11 — Clear "unknown" vs false "in stock"**
- A clear "unknown" state is always preferred over a false "in stock" to build trust.
- (Sequenced after S1 + S2 — depends on the verdict threshold existing.)

**S3 — Store-specific verdict**
- Verdict reflects the selected store's inventory + signals, not a regional average.
- No store-level data → "unknown" (never borrows another store's data).
- NFR: store change re-renders p95 < 1.5s.

**S10 — No personal data in prediction**
- Availability prediction uses no personal data → meets EU/JP consent rules (all 22 markets).

## Scope Boundary
**In:** confidence-graded verdict, explicit "unknown" state, per-store granularity,
audit logging of verdicts + confidence.
**Out:** real-time shelf-level RFID tracking, home-delivery availability, and stock
reservation/hold mechanics — *the assistant informs the decision; it does not lock inventory.*

---

## Decision Memory — DM-001

| Field | Entry |
|---|---|
| **Decision** | The assistant will **not** reserve or hold inventory; it only informs the shopper with a confidence-graded verdict. |
| **Context** | Phantom-stock cancellations stem from stock drift between online counts and shelf reality. A hold/lock mechanism could guarantee availability directly. |
| **Reasoning** | Inventory locking touches core order-management and SAP write-paths across 1,400 stores — a multi-quarter, high-risk change that would delay the trust-repair win. A read-only verdict ships faster, is reversible, and still moves the 7%→2% metric by preventing false positives at the source. |
| **Rejected alternative** | **Stock reservation/hold at reserve-time.** Rejected because it inverts the problem from "predict honestly" to "guarantee physically," multiplying scope, coupling the feature to write-path reliability, and risking the ±3% volume guardrail if holds fail. |
| **Owner / Date** | PM · 2026-09-26 |