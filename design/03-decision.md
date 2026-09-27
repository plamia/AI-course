# 03 — Decision: The Chosen Change
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.4
Input: 02-workshop.md · 03-synthesis.xlsx
Author: Plamena Kichukova
Date: 25.09.2026

---

## Chosen change

**A1 — Confidence-banded availability label on the product page.**

Replace the binary "In stock" label with a three-band confidence signal —
**"Likely on shelf"** (green) / **"Might be low"** (amber) / **"Can't confirm"** (grey) —
paired with a freshness timestamp ("stock checked 12 min ago"). This moves the truth about
availability upstream to Step 2 (the product page), before the shopper commits time and travel.

**Score:** Impact 5 × (6 − Effort 2) = **20** — the top quick-win in the matrix.

---

## Rationale vs the runner-up

The runner-up was a tie at **16** between **A2** (% + plain-language band) and
**B3** ("Reserve with free cancellation" default for amber/grey items). Of the two,
B3 is the more strategic pairing. B3 is a strong safety net, but it's a *mitigation* —
it softens the blow of a wasted trip rather than preventing it. **A1 attacks the root cause**
identified across the journey map (Step 7 drop-off) and the heuristic review (findings 1.1, 1.3,
2.1 — the over-confident label). Honest information at the moment of choice stops the wrong trip
from starting; free cancellation only refunds the wasted one. A1 also unblocks B3 and C1 later —
they all depend on a confidence signal existing first. We ship A1 first, then layer B3 as the
paired fallback.

---

## How we answer the fresh-session challenge

The attack surfaced four real failure modes. The decision holds, with these guardrails:

| Failure mode raised | Guardrail added |
|---|---|
| Amber/grey may kill conversion | Pair A1 with **B3 (free cancellation on amber/grey)** so uncertainty carries no commitment cost — protects conversion. |
| Timestamp still hides a 15–30 min blind window | Confidence band must **factor sync-age into the model** — an item synced 28 min ago cannot show green. Band ≠ timestamp alone. |
| Bands are meaningless without a real confidence model | This is now a **hard dependency logged for Architecture/Eng** — the band must be backed by a signal, not a guess. Flagged in the K 3.W.1 gate conditions. |
| Shoppers may not understand the bands | Plain-language labels ("Likely on shelf") + a one-line "Why?" tooltip; validated in K 3.W.8 task testing. |

---

## Score-vs-decision check

The score and the decision **agree** (A1 is both top-scored at 20 and chosen), so no override
rationale is needed. A1 is a genuine quick win (high impact, low effort) — not a big bet.

---

## Owner

**Sarah Chen (Head of CX)** — owns the change through prototype (K 3.W.6), handoff (K 3.W.7),
and validation (K 3.W.8).

---

*Result: One decided change (confidence-banded label) with a defensible score, a rationale that
beats the runner-up on root-cause grounds, four challenge-tested guardrails, and a named owner.*