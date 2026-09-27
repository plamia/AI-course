---
product: Meridian Omnichannel Commerce Platform
feature: AI Availability Assistant for Click-&-Collect
date: 2026-09-23
---

# Vision

## Vision (revised)
For click-&-collect shoppers who reserve online to avoid a wasted trip, Meridian's 
AI availability assistant replaces an unreliable stock count with a confidence-graded 
collectability verdict the shopper can act on — so shoppers only reserve what they can 
actually pick up, and Meridian recovers orders lost to phantom-stock cancellations 
without shrinking the channel.

## Problem statement
Meridian loses ~7% of click-&-collect orders to cancellation at pickup because online 
stock counts don't match shelf reality ("phantom stock").

## Target user
Click-&-collect shoppers who reserve online specifically to avoid a wasted trip.

## Outcome metric
Phantom-stock cancellations at pickup fall from a measured 7% baseline to ≤ 2% within 
90 days of rollout, **measured from the order-management cancellation-reason log**, 
**while click-&-collect order volume stays within ±3% of the pre-launch baseline** 
(the guardrail), reported per-region so no single market's failure hides in the average.

## AI critiques captured (fresh session)
1. Metric had no guardrail — could be "won" by killing click-&-collect volume.
2. "Trustworthy verdict" was undefined and unmeasurable — no accuracy threshold.
3. The 90-day target had no baseline source and blended 1,400 stores into one average.

## What changed after critique
- Added a guardrail metric (order volume ±3%) so the outcome can't be gamed.
- Named the measurement source (order-management cancellation-reason log).
- Required per-region reporting so regional failures surface.
- Verdict-accuracy threshold noted as a spec-level requirement (moved to the AI Eval 
  Card in K 2.W.5, where quality thresholds belong).