# context-load-check.md

**Kata:** 5.1 — Set up the workspace
**Step 4 check:** Close and reopen the session. Ask: "Summarise the rule file you loaded, by section, and cite the filename."

## Prompt used
> Summarise the rule file you loaded, by section, and cite the filename.

## Response received

Summary of loaded rule file — `CLAUDE.md`

- **Project context:** Tiny CLI that summarises synthetic `events.csv` logs
  (columns: timestamp, level, service, message) and writes a counted summary.
  Synthetic data only — no production or customer records.
- **Conventions:** Source code lives in `src/`, tests live in `tests/`, data
  files live in `data/`. Keep functions small and single-purpose.
- **Utilities to prefer:** Python 3.11 standard library (avoid new
  dependencies), `ruff` for linting/formatting, `pytest` for tests.
- **Escalation gates:** Stop and ask before adding any dependency. Use
  synthetic data only — never paste real logs. Never overwrite `spec.md`
  after sign-off without asking first.

## Verification

- [x] All four required sections present (project context, conventions,
      utilities to prefer, escalation gates)
- [x] No invented framework/tooling details outside the sandbox brief
- [x] Filename correctly cited as `CLAUDE.md`
- [x] File is 22 lines — under the 30-line cap

## Caveat (read before treating this as final evidence)

This check was run in a chat session where `CLAUDE.md` had just been pasted
into context moments earlier — not a genuinely fresh session loading the
file from disk in a coding client (CodeMie Claude / Claude Code / Cursor)
pointed at the repo root. That's a materially weaker proof of persistence
than the kata intends.

**To get real evidence:** open your actual AI coding client fresh (new
window/session, no prior chat history), point it at the `logsum-sandbox`
repo root, and ask the same prompt with no other context supplied. Confirm
it can name and summarise `CLAUDE.md` without you repeating its contents.
Paste that transcript in place of this one, or alongside it, before
submitting the kata.

## Outcome

Rule file confirmed loadable and summarisable by section, with filename
cited — pending replacement of this check with a true fresh-session run
per the caveat above.
