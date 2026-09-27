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

## Pre-Mortem Context for this Repo
When running the `pre-mortem` skill on this codebase, evaluate findings against these explicit local operational facts:
- **ERP Sync Queue (`src/queues/erp-sync.queue.ts`):** Redis/BullMQ queue has a hardcoded 3-retry limit with exponential backoff; duplicate events MUST be handled idempotently using Redis transaction locks.
- **Database Access:** PostgreSQL via Prisma ORM (`src/adapters/erp/`). Raw SQL queries in `raw-queries.ts` bypass Prisma connection pooling and must be checked for connection leaks under load (>50 concurrent queries).
- **High-Value Quote Gate:** Quotes exceeding €5,000 trigger `HITLApprovalService`. Pre-mortem passes must verify that `HITLApprovalService` errors fail closed (block quote issuance).
- **Testing Runner:** Run unit and integration tests via `pnpm test` (`vitest`).