# Feature Specification: AI Quote Discount & Rate Limiter Service (`quote-discount-service`)

## 1. Behaviour & Scenario
Sales Operations reps and B2B portal clients submit machinery spare-parts quote requests containing line items and target discount percentages. The `quote-discount-service` evaluates request parameters, validates client tier thresholds against the price-book database, enforces per-client rate limits (max 5 custom discount evaluations per client per minute), and outputs a calculated quote payload. If the finalized quote total exceeds €5,000, the service marks the quote status as `PENDING_HITL_APPROVAL` and routes it to the Human-in-the-Loop approval queue.

### Acceptance Criteria (Given / When / Then)

#### AC-1: Standard Discount Calculation (Under Tier Threshold)
- **Given** an authenticated B2B client with Tier-2 status and an active price-book session,
- **When** a quote request is submitted for 10 units of Part `PL-8812` with a requested 8% discount,
- **Then** the service calculates line-item pricing using IEEE 754 half-even (Banker's) rounding to 2 decimal places and returns HTTP 200 with status `APPROVED`.

#### AC-2: Client Rate Limit Exceeded Rejection
- **Given** a B2B client who has submitted 5 discount calculation requests within the last 60 seconds,
- **When** the client submits a 6th discount calculation request within the same 60-second window,
- **Then** the service rejects the request immediately with HTTP 429 Too Many Requests and sets the `Retry-After: 60` response header.

#### AC-3: High-Value Quote Routing to HITL Approval Queue
- **Given** a calculated quote payload with a net total exceeding €5,000.00,
- **When** the final discount calculation completes successfully,
- **Then** the service sets the quote status to `PENDING_HITL_APPROVAL`, dispatches an event to `hitl.quote.approval` queue, and suppresses final client pricing issuance until human sign-off.

#### AC-4: Stale Price-Book Snapshot Fallback
- **Given** the primary ERP Price-Book Database connection times out (>2000ms),
- **When** a quote calculation request arrives,
- **Then** the service falls back to the local Redis price-book snapshot, sets `is_stale_pricing: true` in the response body, and logs a warning.

---

## 2. Concurrency
- **State Locking:** Concurrent quote evaluations for the same `clientId` and `partId` combination use a Redis distributed lock (`redlock`) with a 3,000ms TTL.
- **Simultaneous Requests:** If a client issues two identical quote calculation requests simultaneously, the second request blocks until the first releases the lock or times out.
- **Race Condition Guard:** Rate limiter increments use atomic Redis `INCR` and `EXPIRE` operations inside a single pipeline to prevent race conditions during window resets.

---

## 3. Error States & Response Shapes
- **Standard Format:** All errors conform to the RFC 7807 Problem Details JSON format.
- **Validation Failures (HTTP 400):** Returned when line item quantities are $\le 0$, requested discounts exceed 50%, or part IDs do not exist in the price-book.
- **Error Payload Example:**
  ```json
  {
    "type": "https://api.eumachinery.com/errors/invalid-discount-request",
    "title": "Invalid Discount Percentage",
    "status": 400,
    "detail": "Requested discount 55% exceeds maximum allowed threshold of 50%.",
    "instance": "/api/v1/quotes/discount-eval"
  }