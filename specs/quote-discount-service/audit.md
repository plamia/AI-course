# Fresh-Session Audit Log: `quote-discount-service` Spec

**Context Isolation Standard:** **Tier A** (Spec drafted in Claude Code session; audit performed in an isolated, fresh OpenAI GPT-4o session with zero cross-conversation memory or shared repo state).

---

## 1. Audit Findings (Silent Omissions Identified)

### Finding 1: Floating-Point Currency Rounding Precision Omitted
- **Omission Location:** Section 1 (AC-1) & Section 3 (Validation).
- **Missing Detail:** The spec did not specify the rounding algorithm or decimal precision for multi-currency discount conversions (e.g., EUR to SEK/GBP), creating potential fractional cent discrepancies during ERP ledger reconciliation.
- **Production Impact:** Accumulation of fractional cent rounding errors across thousands of daily quotes, causing ERP invoice reconciliation jobs to fail during end-of-month financial settlement.

### Finding 2: Unreachable HITL Webhook Timeout SLA
- **Omission Location:** Section 1 (AC-3) & Section 5 (Integrations).
- **Missing Detail:** The spec did not define a timeout SLA or retry policy if the `hitl.quote.approval` event queue or downstream notification webhook is unreachable during high-value quote routing (>€5,000).
- **Production Impact:** Quotes >€5,000 hang indefinitely in `PENDING_HITL_APPROVAL` state with no notification sent to Sales Ops managers, causing high-value sales deals to stall silently.

### Finding 3: Redis Cluster Split-Brain Rate Limiter Behavior
- **Omission Location:** Section 2 (Concurrency).
- **Missing Detail:** The spec did not define behavior when Redis primary-replica failover occurs during atomic rate-limiter window increments (`INCR` / `EXPIRE`).
- **Production Impact:** During Redis failover, active client window counters reset prematurely, allowing clients to exceed the 5 req/min rate limit and trigger downstream ERP database overload.

---

## 2. Finding Resolutions

| Finding ID | Resolution Action | Resolution Rationale & Patch Location |
| :---: | :---: | :--- |
| **Finding 1** | **INCORPORATE** | **Patched in AC-1 & Section 1:** Added explicit requirement: *"All multi-currency pricing calculations MUST use IEEE 754 half-even (Banker's) rounding rounded strictly to 2 decimal places at line-item level before subtotal aggregation."* |
| **Finding 2** | **DEFER** | **Deferred to Ticket `EU-MCH-8421`:** Asynchronous webhook retry and fallback queuing for unreachable HITL consumers will be handled in Phase 3 under dedicated worker queue architecture. Re-visit condition: Phase 3 Kickoff. |
| **Finding 3** | **REJECT** | **Rejection Rationale:** Redis cluster split-brain resiliency is managed at Infrastructure level via Azure Cache for Redis Premium multi-region active-passive failover and is out of application spec scope. |