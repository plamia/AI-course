# EU Machinery Integration Service — Hot Context & Instructions

## Core Instructions & Rules
- Language & Runtime: TypeScript (v5.3+) / Node.js (v20 LTS).
- Package Manager: `pnpm` only (do NOT use `npm` or `yarn`).
- Architecture Boundary: All external ERP database calls MUST go through `src/adapters/erp/`. Direct SQL queries inside request handlers are strictly prohibited.
- Formatting & Style: Bi-weekly linting rules apply (`pnpm lint`). Zero ESLint errors or warnings allowed before commit.
- Testing Requirement: Every new feature or fix must include unit/integration tests running under `Vitest`. Test files live in `tests/` and end with `.test.ts`.

## Context Pointers
- Warm Context (Stack, Architecture & Patterns): Read `docs/context/stack.md` before making architectural or database schema changes.
- Cold Context (Historical ADRs & Incident Notes): Refer to `context/cold/` when modifying legacy middleware migration logic.
- Human-Owned Decisions: Any change touching `src/security/`, database migrations, or public API contracts requires explicit human review and PR approval.

## Execution Guardrails
- NEVER delete existing test files or drop test coverage thresholds (`vitest --coverage >= 85%`).
- NEVER commit secrets, API keys, or raw connection strings. Use environment variables defined in `.env.example`.
- Keep changes minimal and scoped to the task spec. Do NOT perform uninvited refactoring across module boundaries.