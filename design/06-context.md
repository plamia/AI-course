# CONTEXT.md — Meridian Availability Assistant
Feature: Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.7
Input: 04-ai-ac.md · 05-mockup.html
Author: Plamena Kichukova
Date: 25.09.2026

---

## Feature in one sentence
An AI availability indicator estimates whether an item is really collectable at a nearby
Meridian store, shown as a three-band confidence cue with a freshness timestamp and a
no-confirm fallback, so shoppers avoid a wasted click-&-collect trip.

## Who uses it
Click-&-collect shoppers on the product page (and the reserve/confirm and pickup screens).
The store associate is out of scope.

## Technical environment
- React + design-token system (tokens consumed from a machine-readable tokens file, not Figma).
- Stock data from SAP inventory sync; sync latency 15–30 min (data can be stale).
- Confidence estimate computed server-side and returned per store.
- Non-PII data only in the AI path (stock + store metadata; no customer identity/order history).

## Hard constraints
- MUST NOT guarantee a hold or present availability as certain.
- MUST NOT show a green "Likely on shelf" band on stock synced > 15 min ago.
- MUST NOT use absolute/binary "In stock" wording anywhere in the flow.
- GDPR/CCPA apply to any personalised surface; EU AI Act risk class unconfirmed → no personalisation until confirmed.
- Confidence band must be backed by a real confidence signal, not a guess (dependency on Architecture/Eng).

## Out of scope
Reservation holds logic, loyalty/points, pricing, web↔in-store identity linking.

## Related artefacts
- `06-spec.md` (build contract)
- `04-ai-ac.md` (six AI-AC clauses + thresholds)
- `05-mockup.html` (clickable 3-screen lo-fi prototype: green / amber / grey states)
- `03-decision.md` (why this change won)
- `01-journey-map.md` + `01-heuristics.md` (evidence)