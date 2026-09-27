---
name: pre-mortem
description: Runs a pre-mortem review against a proposed diff, PR, or spec to surface the top 5 production failure modes, concurrency gaps, and unhandled edge cases before code is merged.
compatibility:
  tested_clients:
    - Claude Code (v0.2+)
    - Cursor (.cursor/rules / Skill mode)
    - OpenAI Codex / AGENTS.md
  manual_fallback: "Copy the contents of SKILL.md into system prompt or session context"
  known_limits: "Requires diff, PR payload, or spec document loaded in active context"
---

# Pre-Mortem Review Skill

**Verification Status:** Verified manual paste-in and native load-test on Claude Code (2026-09-27). Native loading: confirmed.

## Goal
Assume the proposed code change or specification causes a critical production incident 30 days post-deployment. Systematically analyze the diff or spec to identify the top failure modes, hidden assumptions, and missing edge-case protections before code is merged.

## Workflow Steps

1. **Context Load & Baseline Check:**
   - Read the proposed diff, PR description, or spec document in the active session.
   - Consult the repository's warm context file (e.g., `docs/context/stack.md`) to identify active architectural constraints, database patterns, and Non-Functional Requirement (NFR) budgets.

2. **Failure Mode Generation (Top 5 Scenarios):**
   Enumerate 5 plausible root causes that could trigger a production failure, focusing on:
   - *Boundary Data & Type Invariants:* Unhandled nulls, empty collections, malformed payload shapes, or boundary limits.
   - *Concurrency & State Transitions:* Race conditions, un-isolated state updates, missing lock semantics, or re-entrancy issues.
   - *External Dependencies & Timeouts:* Network timeouts, 5xx status codes, circuit breaker trips, or partner API contract shifts.
   - *Resource Exhaustion:* N+1 query patterns, unindexed table scans, memory leaks, or uncapped event queue growth.
   - *Partial Failure & Rollback Gaps:* Incomplete transaction boundaries or operations that cannot be safely retried.

3. **Failure Analysis Per Scenario:**
   For each identified failure mode, document:
   - **Trigger Event:** The exact runtime input, network state, or concurrency event that initiates the failure.
   - **Affected Code Path:** File, module, or handler where the flaw resides.
   - **Observed Symptom:** What the end-user or operational monitoring will report (e.g., 504 Gateway Timeout, corrupted DB row).
   - **Recommended Mitigation:** Specific guard clause, circuit breaker, index, or transaction lock required.

4. **Verification Gap Assessment:**
   - Check whether the repository's test runner and existing test suite currently include tests exercising these 5 failure scenarios.
   - Identify any test that passes only because test fixtures rely exclusively on happy-path data shapes.

5. **Output Delivery:**
   - Generate a structured Markdown report formatted under the heading `# Pre-Mortem Failure Analysis`.
   - Rank findings by severity (`CRITICAL`, `HIGH`, `MEDIUM`) with explicit file/line references and concrete code fixes.