# 07 — Validation Plan (Task-Based Usability Test)
Feature: Meridian Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.8
Input: 03-decision.md · 05-mockup.html
Author: Plamena Kichukova
Date: 25.09.2026

---

## Purpose
Prove the confidence-banded availability redesign works by watching shoppers *do tasks* —
not by asking whether they like it. Covers the happy path AND the low-confidence / fallback
path (the whole point of the feature).

## Method
- 5 unmoderated/moderated task prompts on the `05-mockup.html` prototype.
- 5 participants (matches the module rule of thumb).
- Record what they try, where they pause, and what they misunderstand — not opinions.
- Success = task completed without help + correct interpretation of the confidence cue.

---

## The 5 tasks (all phrased as "show me how you'd…")

### T1 — Happy path: check availability
> "Show me how you'd check whether these headphones are collectable at a store near you today."
- **Watching for:** does the shopper find and correctly read the green "Likely on shelf" band + freshness timestamp?
- **Pass:** locates the band and states, unprompted, that it's *likely/estimated*, not guaranteed.

### T2 — Low-confidence interpretation (amber)
> "Show me what you'd do if the store showed 'Might be low' for this item."
- **Watching for:** does the shopper understand it's uncertain, and notice the free-cancellation safety net?
- **Pass:** recognises the risk AND finds the "reserve with free cancellation" reassurance.

### T3 — Fallback path (grey / can't confirm)
> "Show me how you'd still get this item if your nearest store says 'Can't confirm'."
- **Watching for:** does the shopper use the fallback (alternative higher-confidence store OR home delivery)?
- **Pass:** reaches an alternative store or delivery without hitting a dead end.

### T4 — Disclosure comprehension
> "Show me how you'd find out why the app isn't 100% sure the item is there."
- **Watching for:** does the shopper find and understand the "Why?" tooltip / freshness timestamp?
- **Pass:** opens the disclosure and can explain, in their words, that stock data can be a few minutes old.

### T5 — Trust / decision outcome
> "Show me how you'd decide whether it's worth driving to the store for this item right now."
- **Watching for:** does the confidence band actually change the shopper's go/no-go decision?
- **Pass:** shopper references the band + freshness to justify travelling (green) or not (grey).

---

## Success metrics for the test
| Metric | Target |
|---|---|
| Task completion (T1–T5) | ≥ 4 of 5 participants complete each task unaided |
| Confidence-cue comprehension (T1, T4) | ≥ 4 of 5 correctly describe the band as an *estimate* |
| Fallback success (T3) | 5 of 5 reach an alternative store/delivery — zero dead ends |

## Risks
- Amber/grey may deter travel even when the item is present (over-caution) → watch T2/T5.
- "Why?" tooltip may be missed → watch T4 discoverability.
- Bands only as good as the confidence model → flagged to Architecture/Eng (from K 3.W.4).

---

*Result: Five task-based prompts (no opinion questions), including a low-confidence and a fallback
task, that validate whether the redesign actually changes shopper behaviour.*