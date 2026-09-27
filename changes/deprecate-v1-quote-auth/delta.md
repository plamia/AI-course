# Change Delta: `deprecate-v1-quote-auth`

## 1. Preserved Behaviour (Up Front)
After this change, existing B2B portal callers invoking quote evaluation endpoints using valid `Authorization: Bearer <token>` headers must continue to receive valid pricing calculations without any change to calculation latency, calculation rounding, or payload schema.

---

## 2. ADDED
- **HTTP 401 Problem Details Response:** New RFC 7807 compliant error payload returned when an `Authorization` header is missing, malformed, or utilizes an unsupported scheme (e.g., `Basic` instead of `Bearer`).
- **Legacy Auth Usage Telemetry:** New Prometheus counter metric `http_requests_legacy_token_query_param_total` that increments whenever an incoming request attempts URL query parameter authentication (`?token=...` or `?api_key=...`).
- **Header Auth Integration Test Suite:** New test suite `tests/integration/auth-bearer-enforcement.test.ts` verifying header validation, token expiration, and query parameter rejection.

---

## 3. MODIFIED
- **Route Pre-Handler Hook (`src/routes/v1/quotes.ts`):** Fastify route pre-handler updated to validate tokens strictly via `request.headers.authorization`.
- **Auth Middleware (`src/middleware/auth.ts`):** Token extraction logic updated to strip `Bearer ` prefix before passing token payloads to JWT validation routines.
- **Swagger / OpenAPI Spec (`docs/openapi.yaml`):** Updated security scheme definitions to declare `BearerAuth` as the sole security requirement for `/api/v1/quotes/*`.

---

## 4. REMOVED
- **URL Query Parameter Token Extraction:** Complete removal of `request.query.token` and `request.query.api_key` lookup logic across all `/api/v1/quotes` handlers.
- **Unauthenticated Synchronous ERP DB Fallback:** Removal of `src/adapters/erp/legacy-sync-poll.ts`, which previously allowed unauthenticated requests to fall back to a direct PostgreSQL query if token parsing failed.
- **Legacy Response Metadata Property:** Removal of the undocumented response payload field `legacy_auth_mode: true` previously returned on query-parameter-authenticated calls.

---

## 5. REMOVED Audit (Generator vs. Human Audit)

### Generator Misses (Discovered During Audit)
- **Missed Item 1 (`legacy-sync-poll.ts` deletion):** The initial AI generator delta proposed "Refactor auth middleware to use headers". It completely missed that `src/adapters/erp/legacy-sync-poll.ts` was dead code after query parameter token removal and would remain in the repo as an unmaintained security bypass.
- **Missed Item 2 (`legacy_auth_mode: true` payload field):** The initial generator draft failed to detect that removing query parameter auth implicitly removed the `legacy_auth_mode: true` property in the returned JSON object, which downstream integration tests in client applications asserted against.

### Genuine "Complete" Justification
The REMOVED accounting across the 3 touched files (`src/routes/v1/quotes.ts`, `src/middleware/auth.ts`, `src/adapters/erp/legacy-sync-poll.ts`) is complete:
- `src/routes/v1/quotes.ts`: 0 remaining references to `request.query.token`.
- `src/middleware/auth.ts`: 0 remaining query parameter fallback branches.
- `src/adapters/erp/legacy-sync-poll.ts`: File permanently deleted from repository tree.

---

## 6. Risk Note & Proof Test

### Highest-Risk Preserved Behaviour
- **Risk:** Legacy Site 3 automated machinery batch jobs using hardcoded query parameter tokens (`?token=xyz`) in cron scripts will receive HTTP 401 Unauthorized responses instead of executing silent fallbacks.

### Why At Risk
Site 3 cron scripts are maintained by an external subcontractor, operate outside the primary B2B web portal code, and were not included in standard staging integration test runs.

### One Proof Test to Confirm Survival
Run `tests/integration/auth-bearer-enforcement.test.ts` to confirm:
1. Valid `Authorization: Bearer <token>` requests succeed with 100% calculation parity and response time `< 120ms`.
2. Requests attempting `?token=xyz` parameter auth return HTTP 401 with `http_requests_legacy_token_query_param_total` metric incremented by 1.

---

## 7. Comparative Delta Summary Table (CSV View)

```csv
change_type,summary,caller_visible_effect,severity
ADDED,HTTP 401 RFC 7807 Error Payload,New error format on missing header,LOW
ADDED,Telemetry Metric http_requests_legacy_token_query_param_total,Internal Prometheus metric addition,LOW
MODIFIED,Fastify Route Pre-Handler in src/routes/v1/quotes.ts,Requires Authorization Bearer header,MEDIUM
MODIFIED,JWT Auth Middleware in src/middleware/auth.ts,Enforces Bearer scheme parsing,MEDIUM
REMOVED,URL Query Param Token Extraction (?token=...),Breaks legacy URL-authenticated callers,HIGH
REMOVED,Unauthenticated ERP DB Fallback (legacy-sync-poll.ts),Eliminates unauthenticated DB access,HIGH
REMOVED,Response Property legacy_auth_mode,Removes undocumented JSON field,MEDIUM