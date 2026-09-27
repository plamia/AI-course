---
case: "Case A — Meridian Retail Group"
date: "2026-09-22"
use_case: "U01 — Pickup-readiness risk predictor"
inputs:
  - "05-canvas.md"
  - "06-roi.md"
  - "07-deck.pdf"
review_method: "Independent review response supplied by learner"
status: "review recorded — recommended changes not yet applied"
---

# Pre-Mortem — Pickup-Readiness Predictor

## Review Scope

An independent AI review examined the supplied canvas, ROI and deck under
the assumption that the investment proceeded and failed.

This document consolidates that review. No new external research,
customer validation or operational results were introduced.

The reviewer response was supplied by the learner. Runtime details and
the full independent-session transcript are not recorded here.

## Executive Verdict

The materials support investigating the opportunity, not approving rollout.

The most consequential financial risk is that preventing late readiness
does not preserve otherwise lost sales. This could invalidate the cash
benefit even if the data, prediction and operational-intervention gates pass.

## Five Credible Failure Reasons

| ID | Failure reason | Basis in existing materials | Required response |
|---|---|---|---|
| F1 | Prevented late orders do not preserve sales. | Base ROI assumes 40% sales preservation, explicitly unverified. Customers may buy anyway, wait or switch channels. | Measure incremental completed sales and contribution against a credible control; account for returns and channel substitution. |
| F2 | ML does not improve on simple rules. | Canvas requires ≥10 percentage points more late orders detected at equal alert volume, ≥2 hours before deadline. No result demonstrates this. | Run the specified held-out comparison. Prefer rules or existing capabilities if incremental ML value is insufficient. |
| F3 | Readiness data is unusable. | The ≥90% completeness gate across 200 orders is proposed, not passed. | Audit linked order IDs, stores, original deadlines and readiness outcomes before modelling. The audit is not a substitute for pilot sample-size planning. |
| F4 | Interventions add unbudgeted labour. | Canvas requires no increase in handling minutes; ROI assumes no additional store-intervention labour. | Measure all alert-review and intervention effort. If labour rises, revise the workflow, costs and decision gates. |
| F5 | Actual late-readiness frequency is below the assumed range. | The ROI's 8–12% baseline is unverified. Meridian's 7% cancellation figure measures something different. | Establish the Italian electronics late-readiness baseline and recalculate the addressable problem. |

## Evidence Classification

| Item | Correct interpretation |
|---|---|
| Competitor collection complaint | A documented customer allegation involving a coffee machine; not independently corroborated or representative of Meridian. |
| Meridian's 7% cancellation rate | Fictional reference-case data; not a validated Italian electronics or late-readiness baseline. |
| Unieuro pickup/payment information | Published service descriptions; not proof of successful execution. |
| Customer-language problem sentence | Canvas framing, not an interview quotation. |
| 20% operational improvement | Proposed success threshold, not a measured effect. |
| 40% sales-preservation share | Unverified causal financial assumption. |
| Volumes, margins and costs | Unverified planning inputs. |
| ROI and payback | Calculations conditional on those inputs, not independently verified benefits. |

**Numerical correction:** The ROI build-cost range is €45,000–€90,000.
The base build estimate is €60,000; base total upfront cost, including
change management, is €80,000.

## Single Risk Most Likely to Kill the Investment

**F1 — Sales preservation is not demonstrated.**

The operational gates ask whether data is usable, ML beats rules and
staff intervention improves readiness. None independently establishes
incremental sales.

The base case counts €96,000 annual sales contribution and excludes
support capacity from cash benefits. If no sales contribution is
established, included annual cash benefit is €0 and operating net is
−€34,000 under the unchanged base recurring-cost assumption.
There would be no payback.

This is a stress condition, not a prediction that the benefit is zero.

## Required Additional Financial Gate

Before recommending rollout, require Finance and the evaluation owner to
agree on a credible measurement design for incremental sales contribution.

The design must distinguish:
- customers who would purchase anyway;
- genuinely preserved purchases;
- changes in channel or purchase timing;
- cancellations, returns and incremental operating costs.

Set the decision threshold before evaluation. Do not invent one from the
existing evidence. If no credible design is feasible, the revenue-led
ROI remains unvalidated.

## Recommended Changes

| Artefact | Proposed change | Status |
|---|---|---|
| `05-canvas.md` | Add a separate financial-validation requirement without claiming the three operational assumptions prove sales impact. | Pending |
| `06-roi.md` | Emphasise that sales-preservation is causally unverified and add the zero-sales-benefit stress condition. | Pending |
| `07-deck.pdf` | Elevate financial causality alongside the data gate; retain scenario payback and disclose negative first-year base ROI. | Pending |
| `SKILL.md` | Require separation of operational improvement from monetised benefit, with a baseline/control and financial validation owner. | Proposed improvement for Final Kata testing |

Do not append reviewer suggestions blindly to slide bodies: each revised
body must remain ≤30 words. Re-export the PDF only after accepted edits.

## Human Decisions

The agent may recommend validation options but must not:
- approve the investment or pilot;
- commit staff or expenditure;
- certify causal financial benefit;
- communicate client acceptance.

Problem selection, ethical boundaries, stage-gate approval, stakeholder
commitments and final value framing remain human-owned.

## Review Outcome

Independent critique received and recorded.
Investment approval: not given.
Validation results: none added.
Deck and upstream artefact patches: not yet applied.