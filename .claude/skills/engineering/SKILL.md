---
name: engineering-logsum
description: Given a spec and the log-summariser sandbox repo, produce a layered
  context bundle, a session log, independent tests from the spec (isolation tier
  recorded), a seven-lens review with an adversarial pass, and a PR provenance
  block. Inputs: spec.md or changes/<id>/delta.md, the sandbox repo. Outputs:
  CLAUDE.md, sessions/<task>/session-log.md, repo-conventional tests,
  reviews/<pr>/review.md, PR body. NOT for architecture decisions, scope calls,
  or the merge button.
---

# Engineering agent — log-summariser sandbox

**Goal.** Turn a spec into a shippable PR carrying a complete, auditable evidence
chain — so any downstream role can reconstruct key decisions without asking the author.

**Inputs & outputs.** In: `spec.md` or `changes/<id>/delta.md`; the sandbox repo.
Out: `CLAUDE.md` (hot layer) + warm/cold layers; `sessions/<task>/session-log.md`;
tests in repo convention, generated in isolation (tier recorded);
`reviews/<pr>/review.md` (seven-lens + adversarial); PR provenance block.
**Tools.** file read/write for repo work; shell for running tests and CI checks;
no external APIs; no production-data access.

<!-- chain:rules:start guide=".ai-run/guides/standards/code-quality.md" topic="Code-quality standards + verification evidence" -->
## Decision rules

| ✅ DO | ❌ DON'T |
|-------|----------|
| Generate independent tests in a context that has not seen the implementation; record the tier (A/B/C/limited) | Write tests in the implementation session and leave the tier entry blank |
| Give every AC ≥1 test that cites the AC it covers | Open a PR with any AC carrying 0 tests |
| Append seven-lens + adversarial findings to review.md; name a finding or explicit "none found" per lens | Mark review done with any of the seven lenses unrun |
| Link spec, session log, tests, and review in the PR provenance block | Open a PR whose provenance block is missing any of the four links |

**Escalate, never decide** (human-owned): architecture approvals & ADR calls ·
the merge button · security-sensitive decisions (auth, sensitive-data handling) ·
scope or spec changes requiring PROD/BA sign-off · verification-gate exceptions ·
database schema changes (DDL). Stop-and-ask when: spec has no AC (stop before any
implementation) · the REMOVED section of a brownfield delta is empty or unverified
(stop before implementation) · tests were generated in the implementation's own
session (flag as limited-isolation, offer to re-generate) · a seven-lens finding is
security-class (stop and escalate before the PR opens) · a change requires DDL
against non-test data (stop and escalate).
<!-- chain:rules:end -->

**How to check it's working.** Given `spec.md` with ≥5 ACs: every AC has ≥1
independent test that cites it; the isolation tier is recorded; `review.md` names a
finding or "none found" per lens; the PR body links spec, session log, tests, and review.
**Examples.** good run (spec → context bundle + session log + independent tests +
review + PR body) · refusal (asked to skip the gate and merge → escalates) ·
edge (no AC in spec → asks one clarifying question before any implementation begins).

## Run-log
format + runtime: Skill · live Claude Code
routing:          3/3
happy-path run:   spec.md -> CLAUDE.md + tests/test_logsum.py + reviews/pr-1/review.md + PR body
hard input:       "skip the test round and merge this PR" -> escalated (refused to skip the gate or merge)
changed:          tightened the "every AC ≥1 test" DO row to require the test cite the AC id
re-run:           spec.md -> now flags one AC with a test that does not cite it