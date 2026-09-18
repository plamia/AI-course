# K 5.W.9 - By-hand vs by-agent comparison

## What both produced
- A fully functional Python CLI (`src/logsum.py`) reading event logs and outputting summarized CSVs.
- A robust test suite (`tests/test_logsum.py`) covering standard grouping, normalisation, missing levels, malformed timestamps, empty inputs, exit codes, and `--min-count` filtering.
- A GitHub Actions CI workflow (`.github/workflows/ci.yml`) running tests on push and pull requests.
- Complete documentation artifacts including `spec.md`, `test-notes.md`, `ci-notes.md`, `refactor-notes.md`, and `questions.md`.

## Where the agent saved time
- **Boilerplate generation:** The agent instantaneously generated standard configuration files (like GitHub Actions workflows and CSV test fixtures) without manual syntax lookups.
- **Test scaffolding:** Setting up parameterised pytest fixtures and subprocess testing helpers was produced in a single pass rather than incremental trial and error.

## Where the agent went wrong or shorter
- **Edge-case nuance:** In an autonomous single-pass run, the agent initially omitted explicit handling for malformed timestamps (`None` bounds preservation) until prompted by the strict step-by-step spec review.
- **Path and module resolution:** The agent-generated test runner initially assumed flat execution, leading to `ModuleNotFoundError` when run via `-m src.logsum` until workspace environment variables (`PYTHONPATH`) and script paths were explicitly corrected.

## What the agent did better
- **Structural consistency:** The agent naturally applied clean function extraction (`process_row`, `read_events`, `write_summary`) and docstrings more consistently across the entire file during initial drafting than a manual incremental build.
- **Comprehensive coverage:** Generated a broader set of test assertions for edge cases and command-line defaults on the first attempt.

## What I learned about supervised vs async
- **Supervised work (human-in-the-loop):** Catches subtle semantic violations (like dropping log rows instead of preserving counts for malformed timestamps) immediately at each checkpoint.
- **Async agent work:** Highly efficient for scaffolding and multi-file generation, but requires rigorous automated gates (CI, strict pytest suites, and provenance notes) to prevent silent requirement drift.

## What I would do differently next time
- **Enforce upfront constraints:** Provide strict architectural guardrails (e.g., explicit module resolution rules and error exit codes) in the initial agent prompt to prevent environment-specific test failures.
- **Require incremental gates:** Break down async execution into smaller checkpoints (Spec -> Tests -> Code -> CI) rather than requesting a monolithic single-pass generation.