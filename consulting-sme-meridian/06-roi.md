---
case: "Case A — Meridian Retail Group"
date: "2026-09-22"
use_case: "U01 — Pickup-readiness risk predictor"
currency: "EUR"
status: "illustrative ROI — confirm assumptions before executive review"
---

# Three-Scenario ROI — Pickup-Readiness Risk Predictor

## 1. Scope and Evidence Rules

Compare a model-assisted pickup workflow with a simple-rules workflow for a defined rollout cohort of Meridian's Italian consumer-electronics orders.

All commercial inputs are **U = unverified — confirm before exec review**.
**D = calculated output**, not independent evidence.

The base-case 20% reduction comes from the proposed target in 05-canvas.md. It is not an observed result. No external benchmarks or new research are introduced.

Scenarios are joint downside/base/upside planning cases, not probability estimates.

## 2. Assumptions and Proposed Ranges

| Driver | Pessimistic | Base | Optimistic | Provenance / validation needed |
|---|---:|---:|---:|---|
| Annual eligible orders in rollout cohort | 120,000 | 240,000 | 360,000 | U — validate Italian order volumes and adoption scope |
| Baseline late-readiness rate | 8% | 10% | 12% | U — measure against original pickup deadlines |
| Relative reduction versus simple rules | 10% | 20% | 30% | U — base is canvas target; validate incremental effect |
| Share of prevented late orders that preserve an otherwise lost sale | 25% | 40% | 50% | U — measure causal sales recovery; do not assume every late order is lost |
| Contribution per preserved sale | €40 | €50 | €60 | U — Finance to confirm after variable fulfilment costs |
| Avoided support contacts per prevented late order | 0.50 | 0.75 | 1.00 | U — validate using linked support records |
| Minutes per support contact | 6 | 8 | 10 | U — validate handling time |
| Loaded support cost per hour | €24 | €30 | €36 | U — Finance to confirm |
| Full deployment months before benefits start | 4 | 3 | 2 | U — validate delivery plan and readiness |

Order volumes represent the cohort actually covered by the workflow, not all Italian sales. Treatment effect must be measured at the workflow level, including staff use; no separate adoption multiplier is added.

## 3. Cost Lines

| Cost | Timing | Pessimistic | Base | Optimistic | Status |
|---|---|---:|---:|---:|---|
| Build, integration and evaluation | Upfront | €90,000 | €60,000 | €45,000 | U — obtain delivery estimate |
| Change management and training | Upfront | €30,000 | €20,000 | €15,000 | U — confirm stores, staff and training effort |
| Hosting, pipelines and platform run cost | Annual after launch | €18,000 | €12,000 | €9,000 | U — excludes inference and monitoring below |
| Model inference | Annual after launch | €6,000 | €4,000 | €3,000 | U — validate scoring frequency and compute |
| Monitoring, model maintenance and operational oversight | Annual after launch | €24,000 | €18,000 | €12,000 | U — confirm staffing and ownership |
| **Total upfront** | | **€120,000** | **€80,000** | **€60,000** | D |
| **Total recurring/year** | | **€48,000** | **€34,000** | **€24,000** | D |

Build includes prelaunch technical work; change management includes prelaunch training. Recurring lines start after launch.

No additional store-intervention labour is assumed. This is conditional on the canvas's no-increase-in-handling-time gate. If intervention adds labour, add that cost and recalculate.

## 4. Value Lines — Full Operating Year

| Value line | Pessimistic | Base | Optimistic | Treatment |
|---|---:|---:|---:|---|
| Prevented late-ready orders | 960 | 4,800 | 12,960 | D — order volume × baseline rate × relative reduction |
| Preserved sales | 240 | 1,920 | 6,480 | D — prevented late orders × sales-preservation share |
| Preserved sales contribution | €9,600 | €96,000 | €388,800 | D — included in cash-benefit proxy |
| Support time released | 48 hours | 480 hours | 2,160 hours | D — capacity only |
| Equivalent support capacity value | €1,152 | €14,400 | €77,760 | D — excluded from cash ROI |
| Additional cash cost savings | €0 | €0 | €0 | U — excluded until a real spending reduction is established |
| Risk avoided | €0 | €0 | €0 | U — not monetised; no evidenced incident frequency or severity |
| **Annual cash-benefit proxy** | **€9,600** | **€96,000** | **€388,800** | D — contribution only |

Revenue-related benefit is represented by incremental contribution, not gross revenue. Gross sales value is not estimated because no validated average order value is available.

Support capacity is not counted again as payroll savings. Zero entries mean excluded from this model, not proven absence of benefit.

## 5. Formulas and Timing

Let:
- N = annual eligible orders
- L = baseline late-readiness rate
- R = relative reduction versus simple rules
- S = sales-preservation share
- M = contribution per preserved sale
- C = annual recurring cost
- I = upfront investment
- d = deployment months

Annual cash-benefit proxy B = N × L × R × S × M.

Support hours released =
N × L × R × contacts avoided × minutes per contact ÷ 60.

After launch, monthly net contribution = (B − C) ÷ 12.

For month t after project start:
Cumulative net = −I + max(0, t − d) × (B − C) ÷ 12.

Payback is the first whole month when cumulative net is strictly positive.
If B ≤ C, there is no payback under the scenario.

Assumptions: upfront costs occur at project start; no benefits during deployment; recurring costs and benefits accrue evenly after launch. No seasonal ramp, discounting, tax or working-capital timing is modelled.

## 6. Scenario Results

| Result | Pessimistic | Base | Optimistic |
|---|---:|---:|---:|
| Annual operating benefit | €9,600 | €96,000 | €388,800 |
| Annual recurring cost | €48,000 | €34,000 | €24,000 |
| **Annual net after recurring cost** | **−€38,400** | **€62,000** | **€364,800** |
| Benefit in first 12 project months | €6,400 | €72,000 | €324,000 |
| Total cost in first 12 project months | €152,000 | €105,500 | €80,000 |
| **Net in first 12 project months** | **−€145,600** | **−€33,500** | **€244,000** |
| **12-month ROI: net ÷ total cost** | **−95.8%** | **−31.8%** | **305.0%** |
| **Payback from project start** | **None** | **Month 19** | **Month 4** |

All results are D, conditional on U inputs. The optimistic result combines favourable volume, effectiveness, margin and cost assumptions; it is an upside stress case, not a forecast.

Base-case interpretation: the model does not repay within the first project year. The pessimistic case does not cover ongoing operating costs.

## 7. Sensitivity — One Driver at a Time, ±20%

Metric: base-case annual net after recurring cost.
All other assumptions remain fixed. Percentage inputs move relatively, not by percentage points.

| Driver | −20% / +20% input | Annual net at −20% / +20% | Absolute net movement |
|---|---|---|---:|
| Eligible annual orders | 192,000 / 288,000 | €42,800 / €81,200 | €19,200 |
| Baseline late-readiness rate | 8% / 12% | €42,800 / €81,200 | €19,200 |
| Relative reduction | 16% / 24% | €42,800 / €81,200 | €19,200 |
| Sales-preservation share | 32% / 48% | €42,800 / €81,200 | €19,200 |
| Contribution per sale | €40 / €60 | €42,800 / €81,200 | €19,200 |
| Hosting/pipeline run cost | €9,600 / €14,400 | €64,400 / €59,600 | €2,400 |
| Inference cost | €3,200 / €4,800 | €62,800 / €61,200 | €800 |
| Monitoring/oversight cost | €14,400 / €21,600 | €65,600 / €58,400 | €3,600 |

**Top two validation priorities:**
1. Relative reduction in late-readiness.
2. Share of prevented late orders that actually preserves a sale.

Both are causally unverified and tie for the largest numerical sensitivity with the other multiplicative benefit drivers. They are prioritised because prediction alone proves neither effect.

For either selected driver, a −20% change moves payback to **month 26**; a +20% change moves it to **month 15**.

Additional capital check: changing total upfront cost by ±20% moves base payback to month 16 / month 22 respectively. It does not change annual operating net.

## 8. Decision and Confirmation Gates

**Decision:** Fund evidence gathering and a bounded pilot, not a rollout justified by this sketch.

Before executive review:
- Confirm cohort volume, original deadlines and the local late-readiness baseline.
- Demonstrate incremental operational benefit over simple rules.
- Establish whether improved readiness preserves otherwise lost sales.
- Obtain Finance-approved contribution margins and delivery/run-cost estimates.
- Confirm staff intervention does not add unbudgeted labour.
- Replace unverified inputs with evidence and rerun all three scenarios.

Do not use the reference case's 7% cancellation rate as a substitute for any of these measurements.