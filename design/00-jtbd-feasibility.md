# 00 — JTBD & AI Feasibility Gate
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.1 (series root)
Author: Plamena Kichukova
Date: 25.09.2026

---

## 1 — Jobs-To-Be-Done (JTBD)

**When** I'm about to reserve an item for in-store pickup at a nearby Meridian store,
**as a** click-&-collect shopper,
**I want** to know whether the item is *actually* on the shelf right now (not just "in stock" in the system),
**so I can** avoid driving to the store for an order that gets cancelled at the counter.

> **Outcome clause tightened:** the real-world result is *a wasted trip avoided* — not "a stock widget," and not "an AI assistant." The measurable outcome is a reduction in the ~7% pickup-cancellation rate.

**Hidden solution-assumption removed:** the first draft ("I want a live stock indicator") named a UI property. Rewritten to name the shopper's outcome — *confidence the trip is worth it before leaving home.*

---

## 2 — Two-Branch AI Feasibility Gate

### Branch 1 — AI IN THE PROCESS (us using AI to design & deliver)  →  **YES**

| Check | Verdict | Note |
|---|---|---|
| Client permits AI tools for delivery? | Y | EPAM CodeMie pre-approved; third-party LLMs permitted with anonymised inputs. |
| Sensitive data kept out of AI inputs? | Y | Only non-PII stock + store metadata used; anonymised inputs required. |
| Approved toolset named? | Y | See tool list in §4. |

**Verdict line:** **YES** — AI tools are approved for delivery, provided all inputs are anonymised and no customer identity/order history enters any third-party tool.

---

### Branch 2 — AI IN THE PRODUCT (the availability assistant itself)  →  **CONDITIONAL**

| Check | Verdict | Note |
|---|---|---|
| Stock data ready & fresh enough for the promise? | C | SAP sync latency is 15–30 min → stock can be stale. The assistant must *estimate* and *express uncertainty*, not promise certainty. |
| Regulatory framework clear (GDPR/CCPA; AI Act class)? | C | GDPR/CCPA apply to any personalised surface; EU AI Act high-risk classification unconfirmed. Must confirm before any personalisation. |
| Worst case understood — who is harmed if the estimate is wrong? | C | A false "available" → wasted trip + eroded trust (the exact failure we're fixing). A false "unavailable" → lost sale. Confidence + fallback states are mandatory, not optional. |

**Verdict line:** **CONDITIONAL** — AI belongs in the product *only if* it (a) presents availability as a confidence-banded estimate rather than a promise, (b) ships an explicit low-confidence / refusal / fallback state, and (c) keeps all customer identity out of the AI path until EU AI Act classification is confirmed.

---

## 3 — Conditions to Proceed (carry-forward)

1. The assistant **must never promise certainty** on stale data — display a confidence band and last-sync timestamp.
2. A **fallback path** ("call the store to confirm" / "reserve with cancellation-friendly terms") must exist for low-confidence cases.
3. **No PII / order history** enters the AI path — availability estimate uses stock + store signals only.
4. **Confirm EU AI Act risk class** before any personalised surface is added.

---

## 4 — Approved Tool List (for the rest of the series)

| Purpose | Tool |
|---|---|
| Primary delivery / agent env | EPAM CodeMie (CodeMie Claude) |
| Multi-LLM critique | DIAL |
| Third-party LLM (anonymised inputs only) | Claude · GPT · Gemini |
| Lo-fi prototype (K 3.W.6) | v0 · Lovable · Claude Artifacts |
| Journey / diagram-as-code (K 3.W.2) | Mermaid |
| Synthesis (K 3.W.4) | Google Sheets / Excel |

**Rule for the series:** AI drafts; the human validates. All third-party inputs anonymised.

---

*Result: The job is a real user outcome (avoid a wasted trip), and the AI feature is CONDITIONALLY approved — proceed only with confidence-banding, fallback states, and PII exclusion.*