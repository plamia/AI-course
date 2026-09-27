---
product: Meridian Omnichannel Commerce Platform
feature: AI Availability Assistant for Click-&-Collect
date: 2026-09-24
research_note: Competitor approaches synthesized from public product pages, app-store 
  listings, and retail-UX reporting. Marked UNVERIFIED — confirm current behaviour 
  against live sites before committing scope.
---

# Competitive Map

## Comparison table

| Product | How it solves the "will it be there?" job (2 sentences) | Strength | Weakness | Differentiator dimension |
|---|---|---|---|---|
| **Target (Order Pickup / Drive Up)** | Shows a binary "In stock at [store]" flag driven by inventory sync, and lets the shopper reserve for same-day pickup. Confidence is implied, never shown — the count is presented as fact. | Fast, wide store coverage; strong same-day pickup flow. | Presents stock as certain even when it isn't → surprise cancellations at pickup; no honesty about uncertainty. | Certainty honesty |
| **Walmart (In-store / Pickup availability)** | Displays aisle-level location and a stock count per store to help shoppers find items fast. Availability is a raw number with no reliability signal. | Granular in-store location data; huge scale. | Raw counts drift from shelf reality; no fallback when the number is stale or wrong. | Reliability signalling |
| **Argos (Check & Reserve)** | Lets shoppers check stock at a chosen store and reserve for collection, historically strong on "reserve then collect." Availability is a store-level yes/no with limited transparency on freshness. | Purpose-built reserve-&-collect journey; trusted for the job. | Binary yes/no hides borderline cases; shopper can't tell a confident "yes" from a shaky one. | Confidence granularity |
| **US — Meridian AI Availability Assistant** | Instead of a raw count or binary flag, shows a **confidence-graded collectability verdict** ("likely collectable" / "check before you go" / "unknown") from SAP sync + store-level signals. Tells the shopper *when it doesn't know* rather than guessing. | Turns uncertainty into a decision the shopper can act on; repairs trust the failure path destroyed. | New model to build/tune; verdict accuracy must be proven per-region before it earns trust. | **Confidence-graded honesty** |

## Differentiator (verb + specific dimension)
**Tell the shopper whether an item is *really* collectable — with a visible confidence 
level and an explicit "unknown" state — so they never get confidently told "in stock" 
and then burned at the counter.**

*Measurable dimension:* the verdict distinguishes ≥3 states (likely collectable / check 
before you go / unknown) and never displays a positive verdict below a set confidence 
threshold — the opposite of the binary/raw-count approaches competitors ship.

## AI capability carried forward
**Confidence-scored availability prediction with an explicit refusal/"unknown" state.**

- **Why this over lifting a competitor feature:** no scanned competitor exposes 
  confidence to the shopper — they all present availability as certain (a count or a 
  yes/no). That gap *is* the differentiator, so the AI capability to carry forward is 
  our own: a prediction model that outputs a graded verdict **and abstains** ("unknown") 
  when confidence is low, rather than guessing.
- **Capability type:** retrieval + prediction (SAP inventory sync + store-level signals) 
  → classification into a confidence-graded verdict, with a hard refusal contract below 
  a threshold.
- **Carries into K 2.W.5:** this defines the AI Eval Card — confidence thresholds 
  (show vs "unknown"), the refusal contract, and the output-quality target 
  (phantom-stock cancellations ≤ 2%).