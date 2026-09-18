# CLAUDE.md — logsum-sandbox

## Project context
Tiny CLI that summarises synthetic `events.csv` logs
(columns: timestamp, level, service, message) and writes a counted summary.
Synthetic data only — no production or customer records.

## Conventions
- Source code lives in `src/`
- Tests live in `tests/`
- Data files live in `data/`
- Keep functions small and single-purpose.

## Utilities to prefer
- Python 3.11 standard library (avoid new dependencies)
- `ruff` for linting/formatting
- `pytest` for tests

## Escalation gates
- Stop and ask before adding any dependency.
- Use synthetic data only — never paste real logs.
- Never overwrite `spec.md` after sign-off without asking first.