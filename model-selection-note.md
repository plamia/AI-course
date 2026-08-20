# Model Selection Note

**Date:** 2025-06-12
**Author:** Plamena Kichukova — Developer
**Project:** AI-course (personal learning repo — github.com/plamia/AI-course).
**Task:** Summarize a raw GitHub bug-report issue into a structured triage note (repro steps, expected vs. actual, severity, area label) for maintainer review.
**Committed location:** https://github.com/plamia/AI-course/blob/main/model-selection-note.md

---

## Evaluation Criteria

| # | Criterion | Why it matters for this task |
|---|-----------|------------------------------|
| 1 | Accuracy to source issue | Triage notes must reflect only what the reporter stated; invented repro steps mislead maintainers. |
| 2 | Format compliance | Output must follow the fixed triage template (Repro / Expected / Actual / Severity / Area) to be pasteable into the issue. |
| 3 | Completeness | A useful triage note must extract every actionable detail, including environment and version info. |
| 4 | Conciseness | Maintainers triage dozens of issues; a bloated summary wastes review time. |

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

### Model A: GPT-4o (via EPAM DIAL)
> **Repro steps:**
> 1. Open the 'Cash Register' JavaScript Algorithms challenge.
> 2. Type quickly in the code editor to trigger autocomplete.
> **Expected:** Editor remains responsive while autocomplete appears.
> **Actual:** Autocomplete popup freezes the entire page for 2-3 seconds; reproducible every time.
> **Severity:** Medium
> **Suggested area label:** area: learn / editor

### Model B: Claude 3.5 Sonnet (via EPAM DIAL)
> **Repro steps:**
> 1. Navigate to 'Cash Register' challenge (JS Algorithms course).
> 2. Type rapidly in the editor.
> 3. Observe autocomplete popup behavior.
> **Expected:** Editor stays responsive during autocomplete.
> **Actual:** Whole page freezes 2-3s on autocomplete; occurs every time. Env: Chrome 125, Windows 11; extensions disabled, no change.
> **Severity:** Medium
> **Suggested area label:** platform: editor

---

## Scorecard

| Criterion | Model A score (1–3) | Model A evidence | Model B score (1–3) | Model B evidence |
|-----------|---------------------|------------------|---------------------|------------------|
| Accuracy to source issue | 3 | No invented details; matches issue exactly. | 3 | No invented details; matches issue exactly. |
| Format compliance | 3 | Followed the template fields precisely. | 3 | Followed the template fields precisely. |
| Completeness | 2 | Omitted the browser/OS environment and the "extensions disabled" detail. | 3 | Captured Chrome 125 / Windows 11 and the extensions-disabled test. |
| Conciseness | 3 | Tight, under word limit. | 3 | Slightly longer but still under 120 words. |
| **Total** | **11** | | **12** | |

---

## Decision

**Selected model:** Claude 3.5 Sonnet

**Rationale:** Claude won on my highest-priority actionable criterion, completeness, because it preserved the environment details (Chrome 125, Windows 11) and the "extensions disabled" diagnostic step that a maintainer needs to reproduce the bug. Both models were accurate and format-compliant, but GPT-4o's main shortcoming was dropping the environment and diagnostic information, forcing a maintainer to re-read the original issue to triage properly.

---

## Active Constraint

**What could change this decision within 30 days:** If issue volume grows and cost-per-run becomes a constraint, GPT-4o's slightly lower latency and cost could outweigh Claude's completeness edge for high-volume triage.

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2025-06-12 | Initial commit |
