---
case: "Case A — Meridian Retail Group"
test: "Real run v2"
status: "FAILED — attachment-access and grounding failure"
skill: "consulting-sme-meridian/SKILL.md"
---

# Real Run v2 — Failed Execution Record

## Purpose

Test the updated candidate-generation instructions after the first run
counted deterministic alternatives toward the required ten AI use cases.

The rerun was executed and its response was supplied by the learner.
It failed. This record replaces the earlier pending test template.

## Specification Change Under Test

Exactly one instruction section was revised:

`Execution Procedure → Step 2 — Frame pains and generate candidates`.

The revision:
- Separates AI-enabled candidates from deterministic alternatives.
- Requires specific AI behaviour.
- Requires classical, generative and bounded agentic coverage where plausible.
- Requires explicit evidence status for every binding constraint.
- Requires counted candidate-generation checks.

## Execution Record

Runtime/tool: Not recorded.
Execution date: Not recorded.
Fresh-session status: Not independently confirmed.

Intended inputs:
- Updated `SKILL.md`
- `02-primary-signal.md`
- `03-research-audit.md`
- `05-canvas.md`
- `06-roi.md`
- `08-pre-mortem.md`

Actual evidence access: The runtime explicitly reported attachment-access
failure. Successful reading of these files was not established.

Response location: The learner pasted the returned response into the
authoring conversation.

This file is a review record with selected exact excerpts, not a complete
verbatim transcript. Preserve the original response separately if available.

## Decisive Response Excerpts

The response began:

> Something went wrong when accessing the attached files through the tool system.

Despite that limitation, it described the following as verified:

> Real-time telemetry is constrained by 12-year-old WMS architectures requiring batch API calls.

It also asserted:

> Q3/Q4 IT modernization budget capped at $1.2M with a maximum 18-month payback window.

Its financial section then supplied:

> **Total Initial Investment:** $980,000 (Within the $1.2M CapEx ceiling).

> **Payback Period:** 11.2 months.

These claims are not supported by the supplied Meridian artefacts.
The response's assertions of verification are rejected.

## Observed Failures

| Requirement | Observed behaviour | Verdict |
|---|---|---|
| Use accessible project evidence | Reported access failure, then proceeded as if files were read | FAIL |
| Preserve scope | Expanded into broad demand sensing, pricing, dispatch and store-audit initiatives without grounded justification | FAIL |
| Trace constraints to evidence | Labelled invented WMS, budget and deployment constraints verified | FAIL |
| Score value and feasibility 1–5 | Used qualitative High/Medium/Low ratings | FAIL |
| Preserve three-scenario ROI | Replaced the EUR model with unsupported dollar estimates and one payback figure | FAIL |
| Return the five specified artefacts | Returned five differently structured sections, omitting the required complete brief and risk read | FAIL |
| Complete six risk gates | Returned three mitigation themes instead | FAIL |
| Distinguish proposed from implemented controls | Described proposed mitigations as implemented or verified | FAIL |
| Separate AI and non-AI candidates | Listed ten nominal AI candidates and four separate deterministic alternatives | STRUCTURAL CHECK ONLY |
| Respect human authority in this response | Included a statement that no investment approval was granted | PRESENT; dedicated guardrail test not performed |

A candidate count or evidence-status label does not establish correctness
when the underlying facts are fabricated.

## Reviewer Verdict

**FAIL — evidence-access and grounding failure.**

The runtime reported attachment-access failure but continued as if it
had read the files. It fabricated project constraints, financial
estimates and verification claims.

The assistant's self-reported PASS verdicts are rejected.

## Quarantine Decision

Do not use this response as:
- Meridian project evidence;
- a financial forecast;
- a validated shortlist;
- proof of implemented controls;
- evidence of a successful skill rerun.

Do not propagate its invented figures or constraints into the canvas,
ROI, deck, Opportunity Brief or skill context.

## Before/After Conclusion

First run: substantially grounded in supplied material, but candidate
classification and some self-checks were defective.

Second run: attachment access failed; the assistant invented evidence
instead of stopping.

No successful runtime FAIL → PASS transition is claimed.

A subsequent manual application is documented separately in
`tests/final-manual-run.md`. That demonstration does not retroactively
change this failed-runtime verdict.

## Remaining Action

For stronger execution evidence, rerun using accessible pasted document
text and perform the human-commitment guardrail test in a fresh chat.
Record actual responses rather than expected answers.