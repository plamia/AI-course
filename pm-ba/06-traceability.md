# Traceability Matrix — AI Availability Assistant

Links each top story to the outcome metric(s) from the Vision (K 2.W.2).

**Metrics:**
- **M1** — Phantom-stock cancellations: 7% → ≤ 2% (per-region, cancellation-reason log)
- **M2 (guardrail)** — Click-&-collect order volume within ±3% of baseline
- **M3 (quality gate)** — "likely collectable" accuracy ≥ 95% on golden set

| Story | M1: Cancellations ≤2% | M2: Volume ±3% (guardrail) | M3: Accuracy ≥95% | Linked to a metric? |
|---|:---:|:---:|:---:|:---:|
| **S2** — Refusal contract / honest "unknown" | ● | ○ | ● | ✅ |
| **S1** — Show collectability verdict | ● | ● | ● | ✅ |
| **S11** — Clear "unknown" vs false "in stock" | ● | ○ | — | ✅ |
| **S3** — Store-specific verdict (no regional avg) | ● | — | ● | ✅ |
| **S10** — No personal data in prediction | — | — | — | ⚠️ compliance gate |
| **S4** — Verdict survives to pickup | ● | ○ | — | ✅ |

**Legend:** ● moves directly · ○ supports/protects · — no link

## Flags (Step 7)

**Stories with no metric link:**
- **S10 (No personal data)** — moves no *outcome* metric. It is a **legal compliance gate**,
  not an outcome driver. **Decision: keep**, but flag it as a mandatory constraint rather
  than a metric-mover so it isn't mistaken for backlog value. (This is the honest exception
  the matrix is designed to surface.)

**Metrics with no story link:**
- **None.** Every metric has ≥ 1 story:
  - M1 driven by S1, S2, S3, S4, S11
  - M2 protected by S1 (guardrail — verdict must not suppress volume)
  - M3 driven by S1, S2, S3

**Coverage confirmed:** Every metric is moved by at least one story; the only unlinked
story (S10) is an intentional, documented compliance constraint.