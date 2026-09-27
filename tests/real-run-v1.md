---
case: "Case A — Meridian Retail Group"
test: "Real run v2"
status: "PENDING — rerun not yet executed"
skill: "consulting-sme-meridian/SKILL.md"
---

# Real Run v2 — Evidence Record

## Purpose

Test the revised candidate-generation section after the first run counted
deterministic alternatives toward the required ten AI use cases.

This file is a prepared test record, not evidence of successful execution.

## First-Run Findings

The first run generated 12 candidates, but U02, U03, U07 and U08 were
explicitly deterministic/non-AI alternatives. At most eight candidates
were AI-enabled as described.

Additional findings:
- No agentic candidate or explanation of its omission.
- Some binding constraints lacked explicit evidence status.
- Some feasibility and switching-cost claims exceeded the supplied evidence.
- The agent's self-reported PASS results did not capture these weaknesses.

Preserve the original response separately as `tests/real-run-v1.md`.

## Single Specification Change

Changed only:
`Execution Procedure → Step 2 — Frame pains and generate candidates`.

The revised section:
- Requires at least ten genuinely AI-enabled candidates.
- Keeps deterministic alternatives in a separate comparison list.
- Requires specific AI behaviour and AI-type coverage.
- Requires explicit evidence status for every binding constraint.
- Requires counted checks before ranking.

Other first-run findings remain subject to review; this edit is not
claimed to resolve every issue.

## Rerun Inputs

Supply the same inputs used for the first run:
- `SKILL.md` — updated version
- `02-primary-signal.md`
- `03-research-audit.md`
- `05-canvas.md`
- `06-roi.md`
- `08-pre-mortem.md`

Do not silently add new research or validation results.

## Prompt to Execute

Follow the attached updated SKILL.md and run the full workflow on the
same supplied Meridian evidence.

Return all five output blocks.

For the candidate-generation check, explicitly count:
1. Qualifying AI-enabled candidates.
2. Separate non-AI alternatives.
3. Classical, generative and agentic coverage.
4. Candidates missing explicit binding-constraint evidence status.

Do not count deterministic baselines toward the ten AI candidates.
Report actual failures rather than automatically marking checks PASS.
Do not add external research or claim investment approval.

## Execution Record

Runtime/tool: NOT RECORDED
Execution date: NOT RECORDED
Fresh chat used: NOT RECORDED
Inputs actually supplied: NOT RECORDED
Output location: NOT RECORDED

## Actual Rerun Response

NOT YET AVAILABLE.

Paste the complete actual response here after executing the prompt.
Do not substitute an expected answer or an edited reconstruction.

## Verification Results

| Check | Expected result | Observed result | Verdict |
|---|---|---|---|
| AI-enabled candidate count | At least 10 distinct candidates with specific AI behaviour | Not observed | NOT RUN |
| Non-AI alternatives | Listed separately; none counted toward the AI minimum | Not observed | NOT RUN |
| Type coverage | Classical, generative and bounded agentic options, or a justified omission | Not observed | NOT RUN |
| Constraint provenance | Zero candidates missing explicit constraint evidence status | Not observed | NOT RUN |
| Output completeness | Five requested output blocks | Not observed | NOT RUN |
| Human authority | No investment approval or client commitment | Not observed | NOT RUN |

## Before/After Conclusion

Before: the first run counted non-AI alternatives toward the AI minimum
and overstated some evaluation results.

After: NOT YET OBSERVED.

Do not record FAIL → PASS until the actual rerun meets the stated checks.