# Execution Task Breakdown: `quote-discount-service`

## 🚀 First Slice (Implement First)
**Task ID `T1`** is marked as **First Slice — One AC End-to-End (< 100 lines)**. It implements pure Banker's rounding discount calculation logic without external network dependencies, proving AC-1 core math in isolation.

---

## 1. Task List & Interface Contracts

### Task `T1`: Core Banker's Rounding Calculator Logic (AC-1)
* **First Slice — One AC End-to-End (< 100 lines)**
- **Input:** Raw JSON line items (`partId`, `quantity`, `unitPrice`, `requestedDiscountPercent`).
- **Output:** Calculated line subtotals and grand total formatted to 2 decimal places using IEEE 754 Banker's rounding.
- **Done Signal:** `vitest tests/unit/quote-calculator.test.ts` passes 100% of test cases including 0.005 rounding edge cases.

### Task `T2`: Fastify Route & TypeBox Request Schema Validation (AC-1 / Boundaries)
- **Input:** Fastify HTTP app instance and TypeBox JSON schema definitions.
- **Output:** Endpoint `/api/v1/quotes/discount-eval` returning HTTP 400 (RFC 7807) on invalid payloads and HTTP 413 on payloads $>64\text{ KB}$.
- **Done Signal:** `supertest` integration test verifies HTTP 400 on negative quantity and HTTP 413 on 65KB payload body.

### Task `T3`: Redis Atomic Sliding-Window Rate Limiter Middleware (AC-2)
- **Input:** Fastify pre-handler hook and Redis client instance.
- **Output:** Rate limiter middleware enforcing 5 requests/minute per `clientId`, returning HTTP 429 with `Retry-After: 60` header on 6th request.
- **Done Signal:** Integration test executing 6 rapid requests for `clientId="client-99"` verifies 5th succeeds (HTTP 200) and 6th fails (HTTP 429).

### Task `T4`: ERP Price-Book Adapter with Redis Fallback Cache (AC-4) — ⚠️ HIGHEST RISK
- **Input:** Primary PostgreSQL connection pool and fallback Redis cache client.
- **Output:** `PriceBookAdapter` fetching prices from DB, triggering fallback to Redis with `isStalePricing: true` if DB times out ($>2000\text{ ms}$).
- **Done Signal:** Mock DB timeout test confirms adapter returns cached price within 50ms and sets `isStalePricing = true`.

### Task `T5`: High-Value HITL Approval Event Publisher (AC-3)
- **Input:** Final calculated quote payload from `T1` calculator.
- **Output:** Logic setting quote status to `PENDING_HITL_APPROVAL` and publishing event to BullMQ topic `hitl.quote.approval` if total $> €5,000.00$.
- **Done Signal:** Integration test with quote total €5,001.00 verifies BullMQ job enqueued and quote response status is `PENDING_HITL_APPROVAL`.

### Task `T6`: End-to-End Integration Suite & NFR Metric Verification
- **Input:** Wired Fastify service combining `T1`–`T5`.
- **Output:** Full E2E test suite running against Dockerized Postgres & Redis services.
- **Done Signal:** `pnpm test:e2e` passes 100% with P95 latency $< 250\text{ ms}$ verified under K6 benchmark.

---

## 2. Highest-Risk Task Designation

> **Highest-Risk Task:** **`T4` (ERP Price-Book Adapter with Redis Fallback)**  
> **Reason:** Manages dual-datasource state transitions under network timeouts ($>2,000\text{ ms}$). A bug in fallback handling can cause stale pricing to silently persist indefinitely after DB recovery or leak uncached `undefined` prices into quotes.

---

## 3. Task Dependency Graph & Seam Contracts

```mermaid
graph TD
    T1[T1: Calculator Core Math <br/> First Slice] -->|Exposes calculateDiscount | T2[T2: Fastify Gateway Route & Schemas]
    T2 -->|Integrates pre-handler| T3[T3: Redis Rate Limiter]
    T1 -->|Consumes getUnitPrice| T4[T4: Price-Book Adapter <br/> HIGHEST RISK]
    T1 -->|Triggers publishPendingApproval| T5[T5: HITL Event Publisher]
    T2 & T3 & T4 & T5 -->|Full Assembly| T6[T6: E2E Suite & NFR Benchmark]

    classDef firstSlice fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef highRisk fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    
    class T1 firstSlice;
    class T4 highRisk;