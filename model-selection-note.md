# Model Selection Note

**Date:** 2025-06-12
**Author:** Plamena Kichukova — Developer
**Project:** AI-course (github.com/plamia/AI-course)
**Task:** Summarize a raw GitHub bug-report issue into a structured triage note (repro steps, expected vs. actual, severity, area label) for maintainer review.
**Committed location:** https://github.com/plamia/AI-course/blob/main/model-selection-note.md
*(Note: confirm this file is pushed and the link resolves before marking review item #9 complete.)*

---

## Evaluation Criteria

| # | Criterion | Why it matters for this task |
|---|-----------|------------------------------|
| 1 | Accuracy to source issue | Triage notes must reflect only what the reporter stated; invented repro steps or details mislead maintainers. |
| 2 | Format compliance | Output must follow the fixed triage template (Repro / Expected / Actual / Severity / Area) to be pasteable into the issue. |
| 3 | Completeness | A useful triage note must extract every actionable detail, including environment, frequency, and diagnostic steps already tried. |
| 4 | Conciseness | Maintainers triage dozens of issues; a bloated summary wastes review time. |

---

## Method Note

Each prompt was run **once** per model for this comparison. Latency and cost were **not** measured and are therefore not scored criteria; any reference to them appears only as a flagged, unverified hypothesis in the Active Constraint section. A follow-up multi-run pass (5×/model) is recommended before high-volume rollout to confirm the completeness difference below is systematic rather than a single-sample artifact.

---

## Prompt Used

You are an open-source project maintainer assistant. Read the GitHub issue text
below and produce a triage note using EXACTLY this template:

**Repro steps:** (numbered)
**Expected:** 
**Actual:** 
**Severity:** (Low / Medium / High)
**Suggested area label:** 

Use only information present in the issue. Do not invent repro steps or versions.
Keep it under 120 words.

ISSUE:
"Title: Editor autocomplete freezes on large JS challenge
I'm on the JavaScript Algorithms course, the 'Cash Register' challenge.
When I type fast in the editor, autocomplete popup freezes the whole page for
2-3 seconds. Happens every time. Chrome 125 on Windows 11. Tried disabling
extensions, no change. Expected the editor to stay responsive."

---

## Output Comparison

### Model A: Anthropic Claude Opus 4.8 (via EPAM DIAL)
> **Repro steps:**
> 1. Open the JavaScript Algorithms course, 'Cash Register' challenge.
> 2. Type quickly in the editor to trigger the autocomplete popup.
> **Expected:** The editor stays responsive while autocomplete is active.
> **Actual:** The autocomplete popup freezes the whole page for 2-3 seconds; happens every time. Occurs on Chrome 125 / Windows 11; persists with extensions disabled.
> **Severity:** Medium
> **Suggested area label:** editor / autocomplete

### Model B: Google Gemini 3.1 Pro (via EPAM DIAL)
> **Repro steps:**
> 1. Navigate to the JavaScript Algorithms course, 'Cash Register' challenge (Chrome 125 on Windows 11).
> 2. Type fast in the editor.
> **Expected:** The editor stays responsive.
> **Actual:** The autocomplete popup freezes the whole page for 2-3 seconds.
> **Severity:** Medium
> **Suggested area label:** Editor

---

## Label Validation

Neither model's suggested label should be accepted verbatim. Checked against the freeCodeCamp label taxonomy (github.com/freeCodeCamp/freeCodeCamp/labels):

- `editor / autocomplete` (Model A) — **not a valid label**; no such compound label exists in the taxonomy.
- `Editor` (Model B) — **not a valid label**; the repo uses lowercase prefixed labels, not a bare `Editor`.
- **Correct label (human-selected against live taxonomy):** the closest maintained match for an editor UI freeze is **`platform`** combined with **`type: bug`**.

Label selection requires a human check against the live taxonomy regardless of model choice.

---

## Scorecard

| Criterion | Model A score (1–3) | Model A evidence | Model B score (1–3) | Model B evidence |
|-----------|---------------------|------------------|---------------------|------------------|
| Accuracy to source issue | 3 | No invented details; all content traceable to the issue. | 3 | No invented details; all content traceable to the issue. |
| Format compliance | 3 | Clean template; repro steps kept separate from environment/actual detail. | 2 | Follows template, but folds environment ("Chrome 125 on Windows 11") into a repro step rather than the Actual/environment line — awkward for triage scanning. |
| Completeness | 3 | Captured environment (Chrome 125 / Win 11), "happens every time," AND "persists with extensions disabled." | 1 | Dropped both "happens every time" (frequency) and "extensions disabled" (diagnostic already tried) — forcing a maintainer to re-read the issue. |
| Conciseness | 3 | Tight, well under word limit. | 3 | Very tight, under word limit. |
| **Total** | **12** | | **9** | |

---

## Decision

**Selected model:** Anthropic Claude Opus 4.8

**Rationale:** Claude Opus 4.8 wins clearly (12 vs. 9) on completeness, the highest-priority criterion for triage. It preserved all three actionable details a maintainer needs — environment, frequency ("happens every time"), and the diagnostic already attempted ("extensions disabled") — while Gemini 3.1 Pro dropped the latter two. Gemini also lost a format point by embedding environment info inside a repro step. Both were equally accurate and concise. The final label is human-selected against the live taxonomy before paste.

---

## Active Constraint

**What could change this decision within 30 days:**

1. **Cost / latency (unverified).** *Hypothesis only — not measured here.* If issue volume grows and cost-per-run or latency becomes a binding constraint, a cheaper or faster model could outweigh Claude's completeness edge. Requires actual per-run measurement before acting.
2. **Single-run sampling.** This comparison rests on one run per model. If a 5×/model re-run shows Gemini reliably captures the missing details (i.e., the omission was a one-off), the completeness gap narrows and the decision should be revisited.
3. **Prompt fix closes the gap.** If an explicit "always include frequency, environment, and any diagnostics already tried" instruction reliably fixes Gemini's omissions, the models could converge and the choice would shift toward secondary criteria (cost/latency).

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2025-06-12 | Initial commit |
| 2.0 | 2025-06-12 | Switched compared models to Claude Opus 4.8 and Gemini 3.1 Pro; scored against real single-run outputs; adjusted Method Note to reflect single run; updated label validation and Active Constraint accordingly. |
| 2.1 | 2025-06-12 | Updated Project to AI-course and corrected committed-location URL to github.com/plamia/AI-course. |
