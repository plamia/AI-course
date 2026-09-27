# 01 — Heuristic Review (Nielsen's 10)
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.2
Screens reviewed: product-page availability label · reservation confirmation · pickup-counter email
Method: AI-generated in a fresh session; human-audited against the evidence rule.
Author: Plamena Kichukova
Date: 25.09.2026

> Evidence rule: every finding names the violated heuristic AND quotes the screen element.
> Findings that miss either part were discarded.
> Audit result: 9 of 9 AI findings confirmed; 4 heuristics correctly discarded.

---

## SCREEN 1 — Product page availability label

| # | Heuristic violated | Quoted element | Why it fails |
|---|---|---|---|
| 1.1 | **#1 Visibility of system status** | Green label **"In stock"** — "no timestamp, no last-updated indicator, no confidence level" | Stock syncs every 15–30 min and can be stale, but the label presents it as real-time truth, hiding the actual system state. |
| 1.2 | **#5 Error prevention** | Store selector that "shows no indication of which stores have reliable stock" | Letting the shopper pick a store with no reliability signal fails to prevent the foreseeable phantom-stock cancellation before it happens. |
| 1.3 | **#2 Match between system & real world** | The absolute term **"In stock"** | In the real world stock is uncertain (~7% phantom), yet the wording claims a certainty the system doesn't have. |

## SCREEN 2 — Reservation confirmation

| # | Heuristic violated | Quoted element | Why it fails |
|---|---|---|---|
| 2.1 | **#1 Visibility of system status** | **"Ready for pickup"** — "no mention that stock is only estimated… availability was not physically verified" | Reports a confirmed physical state that was never actually checked, misrepresenting system status. |
| 2.2 | **#5 Error prevention** | Confirmation screen with "no fallback offered if the item turns out to be missing" | No safeguard (alternate store, hold-and-verify) at the moment of reservation, so the known failure path is not designed out. |
| 2.3 | **#2 Match between system & real world** | **"Ready for pickup"** | Implies a physically staged item — doesn't match reality since nothing was verified on the shelf. |

## SCREEN 3 — Pickup-counter email

| # | Heuristic violated | Quoted element | Why it fails |
|---|---|---|---|
| 3.1 | **#1 Visibility of system status** | **"Your order is ready for collection"** — sent when "physical availability on the shelf was never verified" | Asserts a verified-ready state that reflects no actual physical check. |
| 3.2 | **#9 Help users recognise, diagnose & recover from errors** | Only outcome offered: **"cancellation + refund"** | When the item is missing, the user gets no diagnosis or genuine recovery path (alternate store/item/rain-check) — just a dead-end reversal after a wasted trip. |
| 3.3 | **#3 User control and freedom** | **"cancellation + refund"** as the sole option at the counter | The user is trapped in an unwanted state with only one forced exit and no alternative to still get the goods they came for. |

---

## Discarded (per evidence rule)

| Discarded | Why discarded |
|---|---|
| #6 Recognition, #7 Flexibility, #8 Minimalist, #10 Help | No screen element could be quoted to support a violation — excluded to avoid AI false positives. |

---

## Link back to the journey map

- **1.1, 1.2, 1.3** cluster on **Step 2 (product page)** → confirms the redesign target: honest, confidence-banded availability upstream.
- **2.1, 2.2, 2.3** show the over-promise propagating through reservation — the *best point to prevent the error* (2.2).
- **3.1** carries the false certainty into the email; **3.2, 3.3** are the dead-end at **Step 7/8** → the mandatory fallback/HITL state flagged in the K 3.W.1 gate.

---

*Result: Nine evidence-backed violations across three screens, clustering on the over-confident "In stock" label and the missing fallback — the exact moments the journey should be redesigned.*