# questions.md — Kata 5.8

## Question 1: Where is the grouping rule?
- **Files read:** `spec.md`, `src/logsum.py`
- **Answer:** The grouping rule is defined in `spec.md` under the "Grouping rule" section, stating that the group key is the tuple `(service, level)` after normalisation. In the implementation (`src/logsum.py`), this is enforced in the `main()` function where each row's normalised service and level form the dictionary key `group_key = (service, level)`.
- **File-line citations:**
  - `spec.md:23-25` ("Grouping rule: Group key is the tuple (service, level)...")
  - `src/logsum.py:73-74` (`group_key = (service, level)`)
- **Unverifiable items:** None.

## Question 2: How is missing level handled?
- **Files read:** `spec.md`, `src/logsum.py`, `tests/test_logsum.py`
- **Answer:** According to the specification, rows with missing levels are grouped under `level = "UNKNOWN"` and still counted. In the implementation, `process_row()` checks if the level string is empty or whitespace; if so, it assigns `"UNKNOWN"`, otherwise it uppercases the trimmed level.
- **File-line citations:**
  - `spec.md:37` ("Missing level: grouped under level = 'UNKNOWN'; still counted.")
  - `src/logsum.py:23-25` (`level = level_raw.upper() if level_raw else "UNKNOWN"`)
  - `tests/test_logsum.py:51-61` (`test_missing_level_edge_case`)
- **Unverifiable items:** None.

## Question 3: How do I run tests and CI locally?
- **Files read:** `.github/workflows/ci.yml`, `tests/test_logsum.py`
- **Answer:** You can run tests locally by invoking `pytest` with `PYTHONPATH` set to the current directory so Python can resolve the source package. CI runs automatically on GitHub Actions using Python 3.11, installing `pytest` and executing the test suite.
- **File-line citations:**
  - `tests/test_logsum.py:19-20` (`env["PYTHONPATH"] = os.getcwd()`)
  - `.github/workflows/ci.yml:25-27` (`PYTHONPATH=. python -m pytest -v`)
- **Unverifiable items:** None.

---

## Verification

- **Citation 1 (`spec.md:23-25`):** Correct. Accurately points to the grouping rule definition.
- **Citation 2 (`src/logsum.py:73-74`):** Correct. Points directly to where `group_key` tuple is formed in the main loop.
- **Citation 3 (`spec.md:37`):** Correct. Points to the missing level edge case rule.
- **Citation 4 (`src/logsum.py:23-25`):** Correct. Points to the ternary expression handling empty levels (`"UNKNOWN"`).
- **Citation 5 (`tests/test_logsum.py:51-61`):** Correct. Accurately points to the missing level test.
- **Citation 6 (`tests/test_logsum.py:19-20`):** Correct. Points to the test environment setup.
- **Citation 7 (`.github/workflows/ci.yml:25-27`):** Correct. Points to the CI test execution step.