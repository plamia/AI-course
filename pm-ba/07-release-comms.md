# Release-Readiness & Communication Pack
**Feature:** AI Availability Assistant for Click-&-Collect
**Product:** Meridian Omnichannel Commerce Platform · **Release date target:** 2026-11-15
**Source of truth:** every claim below traces to 06-traceability.md

---

## 1. Release-Scope Confirmation

### ✅ IN — shipping this release (each line tagged to its story)
| In-scope behaviour | Story |
|---|---|
| Confidence-graded verdict on product page: "likely collectable" / "check before you go" / "unknown" | **S1** |
| Honest "unknown" state — never shows a positive verdict below the confidence threshold (fail-safe, never fail-open) | **S2** |
| Clear "unknown" always preferred over a false "in stock" | **S11** |
| Store-specific verdict — reflects the selected store, not a regional average | **S3** |
| No personal data used in the prediction (EU/JP consent compliant, all 22 markets) | **S10** |

### ❌ OUT — not part of this feature
- Real-time shelf-level RFID tracking
- Home-delivery availability
- Stock reservation / hold / lock mechanics *(the assistant informs; it does not lock inventory — see DM-001)*

### ⏸ DEFERRED — planned, not this release
- **S4** — "Verdict survives to pickup" monitoring instrumentation *(50% confidence; depends on stock-drift signals outside the assistant's control — deferred to a monitoring phase)*
- **S7** — Suggest an alternative nearby store with confirmed stock *(low RICE; revisit after baseline verdict proven)*

---

## 2. Open Risks

| Risk | Owner | One-line mitigation |
|---|---|---|
| **Per-region verdict accuracy below the 95% golden-set gate at launch** — model may miss the threshold in low-data markets. | ML Lead | Gate release per-region: markets below 95% ship in "unknown"-only mode until they pass. |
| **Fail-open regression** — a code change could let a positive verdict display below the confidence threshold, re-introducing phantom-stock cancellations. | Eng Lead | Automated contract test on every deploy: malformed/low confidence must default to "unknown". |
| **Guardrail breach** — over-cautious "unknown" verdicts suppress click-&-collect volume beyond the ±3% guardrail. | PM | Monitor volume daily per-region for 14 days; tune display threshold if volume drops toward the −3% edge. |

---

## 3. Stakeholder Notifications

### 📋 For Delivery Leads (scope + risk + timeline)
> **Subject: AI Availability Assistant — release scope & risks for 15 Nov**
>
> Shipping the confidence-graded collectability verdict (S1, S2, S3, S10, S11): three-state
> verdict, honest "unknown", per-store accuracy, no personal data. **Deferred:** pickup-survival
> monitoring (S4) and alternative-store suggestion (S7). **Out of scope:** any inventory
> hold/lock — read-only by design (DM-001).
>
> **Watch three risks:** (1) per-region accuracy may miss the 95% gate — markets below
> threshold launch in "unknown"-only mode; (2) fail-open regression — contract test blocks
> deploy if the fail-safe breaks; (3) volume guardrail (±3%) monitored daily for 14 days.
> Release gate = 95% golden-set accuracy per region. Target 15 Nov, phased per-region.

### 📣 For Business / External Stakeholders (value + timeline, plain language)
> **Subject: Fewer wasted trips — smarter click-&-collect availability, live 15 Nov**
>
> From 15 November, shoppers reserving for store pickup will see an honest availability
> signal instead of a raw stock number: **"likely collectable," "check before you go,"** or
> **"unknown"** — and we'll never falsely promise stock we can't confirm. This is built to
> cut pickup cancellations from ~7% toward our ≤2% target while keeping order volume steady.
> Rolling out region by region, starting with markets where accuracy is proven.

---

## 4. What's New / Release Note

*(Each bullet verified against 06-traceability.md — see check below)*

- 🟢 **Know before you go.** Product pages now show a clear collectability verdict for your chosen store — "likely collectable," "check before you go," or "unknown." *(S1)*
- 🟢 **No more false promises.** If we can't confirm stock with confidence, we say "unknown" instead of guessing — so you're never burned at the counter. *(S2, S11)*
- 🟢 **Store-accurate, not region-guessed.** The verdict reflects the exact store you selected, not an average across the region. *(S3)*
- 🟢 **Privacy by design.** Availability predictions use no personal data, meeting EU and Japan consent rules. *(S10)*

---

## 5. Spec Section to Update After Release

> **Update `04-stories-acs.md` → AI Eval Card** with the *observed* per-region golden-set
> accuracy and the production phantom-stock cancellation rate, replacing target thresholds
> with measured values once the 14-day monitor completes.