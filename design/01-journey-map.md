# 01 — Journey Map: Click-&-Collect (As-Is)
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.2
Input: 00-jtbd-feasibility.md
Author: Plamena Kichukova
Date: 25.09.2026

---

## Actor
Click-&-collect shopper reserving an item for in-store pickup at a nearby Meridian store.

## Journey — what happens today (including cancellation)

| # | Phase | Action | Emotion | Frustrations (≤3) | Drop-off? |
|---|---|---|---|---|---|
| 1 | Search | Searches for the item online, filters to a nearby store | 🙂 Hopeful | • Not sure which store is truly closest with stock | No |
| 2 | Product page | Sees a green **"In stock"** label on the product page | 😊 Confident | • Label gives no confidence level or last-updated time<br>• No sign the number could be stale | No |
| 3 | Reserve | Reserves the item for store pickup | 🙂 Committed | • No mention that stock is only estimated<br>• Reservation feels like a guarantee | No |
| 4 | Confirmation | Gets a reservation confirmation email/screen | 😌 Reassured | • "Ready for pickup" wording implies certainty<br>• No fallback if it's not there | No |
| 5 | Travel | Drives to the store (15–30 min) | 😐 Neutral | • Time and fuel already spent on an unverified promise | No |
| 6 | Counter check | Associate checks the shelf | 😟 Anxious | • Waits at the counter with no self-service status<br>• No warning this could fail | No |
| 7 | **Discovery** | **Item is missing — phantom stock** | 😠 **Angry / betrayed** | • **Wasted a full trip**<br>• **Trust in the "In stock" label destroyed**<br>• **Only found out at the worst possible moment** | ✅ **YES — DROP-OFF** |
| 8 | Aftermath | Cancellation + refund offered | 😔 Disappointed | • Refund doesn't return the wasted time<br>• Likely won't use click-&-collect again | No |

---

## Drop-off (whole-journey redesign target)

**Step 7 — Discovery at the counter.**
The worst-emotion moment (😠 angry/betrayed) is where the ~7% cancellation rate materialises.
The redesign must move the *truth about availability* **upstream to Step 2 (product page)** — before the shopper commits time and travel — so the failure at Step 7 never happens.

> Note: the *busiest* interaction is the product page (Step 2), but the *worst-emotion* step is the counter (Step 7). The fix is to surface honest, confidence-banded availability at Step 2 so Step 7 stops being a surprise.

---

## Optional — Mermaid flowchart

```mermaid
flowchart TD
    A[1. Search item online] --> B[2. Product page: In stock label]
    B --> C[3. Reserve for pickup]
    C --> D[4. Confirmation email]
    D --> E[5. Drive to store]
    E --> F[6. Associate checks shelf]
    F --> G[7. Item MISSING - phantom stock]:::dropoff
    G --> H[8. Cancellation and refund]

    classDef dropoff fill:#ffdddd,stroke:#cc0000,stroke-width:3px;