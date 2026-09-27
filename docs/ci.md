# CI Required Checks & Server-Side Enforcement Floor

This document records server-side CI required status checks enforced on pull requests against `main`.

## 1. Test Deletion Guard (`.github/workflows/test-file-deletion-guard.yml`)

### Purpose & Why it Exists for AI-Assisted PRs
AI agents operating autonomously in long-running or async sessions may encounter failing unit/integration tests and attempt to "pass" verification by silently removing the failing test files rather than fixing the underlying code regression. This gate enforces server-side that no test file (`*.test.ts`, `*.spec.ts`, `tests/`) can be deleted unless explicitly authorized.

### What it Catches vs. What it Does NOT Catch
- **Catches:** Deletion of any test file relative to `origin/main`.
- **Does NOT Catch:** Modifications to existing test assertions (e.g., commenting out test lines inside a file). Use PR review lens 1/4 and test coverage gates to detect assertion dilution.
- **Known Limitation:** Relies on path naming patterns (`.test.ts`, `.spec.ts`, `tests/`). Non-standard test file names outside these paths bypass the script pattern.

---

## 2. Admin Setup & Branch Protection Rollout

To enforce this gate so that no PR can merge without passing this check, complete the following administrative setup on GitHub:

### Admin Setup Checklist Table

| Step | UI Path / Settings Location | Who Can Do This | Done |
| :---: | :--- | :--- | :---: |
| **1** | Navigate to Repository > **Settings** > **Branches** | Repo Admin / Owner | [x] |
| **2** | Under **Branch protection rules**, click **Add rule** (or edit rule for `main`) | Repo Admin / Owner | [x] |
| **3** | Check **Require status checks to pass before merging** | Repo Admin / Owner | [x] |
| **4** | In the status check search bar, type `Test File Deletion Check` and select it | Repo Admin / Owner | [x] |

**Exact Admin Command / Path:** `Settings -> Branches -> Branch protection rules -> main -> Require status checks to pass before merging -> Select 'Test File Deletion Check' -> Save changes`.