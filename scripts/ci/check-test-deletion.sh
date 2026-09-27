#!/usr/bin/env bash
set -euo pipefail

# TARGET_BRANCH defaults to origin/main or main
TARGET_BRANCH="${1:-origin/main}"

echo "==> Running Test-File Deletion Guard against $TARGET_BRANCH..."

# Identify deleted test files relative to target branch
DELETED_TESTS=$(git diff --name-only --diff-filter=D "$TARGET_BRANCH"...HEAD | grep -E '\.(test|spec)\.(ts|js|jsx|tsx)$|^tests/|__tests__/' || true)

if [ -z "$DELETED_TESTS" ]; then
  echo "✅ PASS: No test files were deleted in this PR."
  exit 0
fi

echo "⚠️ WARNING: The following test file(s) were deleted in this PR:"
echo "$DELETED_TESTS"
echo ""

# Check commit log for explicit override tag
OVERRIDE_FOUND=$(git log "$TARGET_BRANCH"...HEAD --grep="DELETE_TESTS:" -n 1 || true)

if [ -n "$OVERRIDE_FOUND" ]; then
  echo "✅ PASS: Authorized test deletion override detected in commit log ('DELETE_TESTS:' tag found)."
  exit 0
fi

echo "❌ FAIL: Test file deletion detected without authorization!"
echo "AI agents may NOT delete test files to resolve failing builds."
echo "To authorize intentional test deletion, include 'DELETE_TESTS: <reason>' in your commit message."
exit 1