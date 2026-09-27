# Architectural Debate & Decision Record: Log Summary Caching Strategy

- **Feature / System**: Log Summariser Service (`/api/v1/logs/summary`)
- **Isolation Tier**: Tier A (Cross-Model Family Debate: Session A using `claude-3-7-sonnet` as Option A Defender, Session B using `gpt-4o` as Option B Defender).
- **Execution Date**: 2026-03-27
- **Status**: **DECIDED** (Option A selected with explicit reversal triggers)

---

## 1. The Architectural Fork
> **Question**: Should the Log Summariser Service adopt an **Option A: In-Process In-Memory LRU Cache (`lru-cache`)** or an **Option B: External Distributed Cache (Redis / Valkey)** for caching parsed query parameters and pre-aggregated log summaries?

---

## 2. Decision Criteria
1. **Latency & Overhead**: P95 API response time must remain $\le 50\text{ ms}$; cache lookup overhead must be $< 2\text{ ms}$.
2. **Operational & Deployment Complexity**: Zero additional external service dependencies or infrastructure management overhead for single-region deployment.
3. **Container Resource Footprint**: Service instance memory usage must not exceed the strict $256\text{ MB}$ RAM limits imposed by the Docker container policy.
4. **Horizontal Consistency**: Multi-node horizontal scaling consistency across load-balanced instances.

---

## 3. Debate Round 1: Initial Positions

### Option A Defender (In-Process LRU Cache) — *Claude 3.7 Sonnet*
> "Option A is the optimal choice for our target workload. In-process LRU caching delivers sub-millisecond ($< 0.1\text{ ms}$) retrieval latency by eliminating network serialization and IPC hops entirely. For our single-container baseline, adding an external Redis cluster introduces unnecessary operational complexity, connection pool management overhead, and a single point of network failure for a query optimization step that can be safely bounded in RAM at $10\text{ MB}$ (10,000 keys $\times$ 1 KB)."

### Option B Defender (External Distributed Redis) — *GPT-4o*
> "Option B is essential for production durability and horizontal scalability. In-process LRU caching fails when the service scales horizontally beyond one replica, leading to cache fragmentation, duplicated parsing work, and inconsistent pagination responses across load-balanced nodes. Redis guarantees global cache consistency, survives service pod restarts without cache-stampede degradation, and offloads heap garbage-collection pressure from the Node.js V8 runtime under high memory load."

---

## 4. Debate Round 2: Cross-Pollination & Attacks

### Option A's Attack on Option B (Dissent)
> "Option B introduces an external network round-trip ($2\text{ ms} - 8\text{ ms}$ TCP/TLS hop), which consumes $16\%$ of our total $50\text{ ms}$ P95 budget before execution starts. Furthermore, managing Redis clusters, VPC security groups, failover replicas, and connection pools for a simple log summary query parser is severe over-engineering that increases monthly infrastructure costs by $\approx \$60/\text{month}$ per environment with zero initial multi-node justification."

### Option B's Attack on Option A (Dissent)
> "Option A creates a hidden memory leak risk inside V8 heap space under high log cardinality. If unique log query filters flood the in-process cache, Node.js garbage collection pauses will spike API latency to $> 200\text{ ms}$. Additionally, when horizontal autoscaling spawns 5 instances during log surge incidents, each container must independently warm its cache, creating a cache-stampede load spike on the underlying database."

---

## 5. Side-by-Side Claim Matrix & Evidence Evaluation

| Category | Option A: In-Process LRU Cache | Option B: External Redis Cache | Evidence Tag |
| :--- | :--- | :--- | :--- |
| **Lookup Latency** | Sub-millisecond ($< 0.1\text{ ms}$) in V8 heap memory. | $2\text{ ms} - 5\text{ ms}$ network TCP round-trip. | `[evidence-backed]` |
| **Infra Cost & Complexity** | Zero external dependencies; zero added cost. | Requires provisioning managed Redis instance ($\approx \$60/\text{mo}$). | `[evidence-backed]` |
| **Multi-Node Consistency** | Local per-instance cache; inconsistent state across replicas. | Fully unified global cache across all application nodes. | `[evidence-backed]` |
| **GC / Memory Impact** | Increases Node.js heap footprint; potential GC pause spikes. | Offloads cached objects entirely out of application V8 heap. | `[assumption]` |
| **Cache Stampede Risk** | High during cold-start or auto-scaling pod rollouts. | Low; shared warm cache survives application pod restarts. | `[unknown]` |

---

## 6. Human Architectural Decision

- **Chosen Option**: **Option A (In-Process In-Memory LRU Cache)**
- **Driving Criterion**: *Operational & Deployment Complexity & Zero-Dependency NFR Budget*.
- **Rationale**: The log summariser service currently operates as a single-instance microservice. Introducing Redis adds infrastructure cost, network latency, and deployment complexity that violates our warm-context stack constraints. In-process LRU with a strict bounded cap ($5,000$ items $\approx 8\text{ MB}$) satisfies our latency budget ($< 1\text{ ms}$) without V8 heap exhaustion.

---

## 7. Reversal-Evidence Criteria (Falsifiable Triggers)

Revisit this architectural decision and trigger a migration to **Option B (Redis)** if **ANY** of the following signals occur:

1. **Horizontal Scaling**: The service scales to $> 3$ active container replicas in production, causing documented user complaints regarding inconsistent pagination reads.
2. **Memory Pressure**: V8 garbage collection pauses exceed $50\text{ ms}$ in APM telemetry, or container RAM usage exceeds $80\%$ ($204.8\text{ MB}$) under load within the next $60\text{ days}$.
3. **Cache Invalidation Frequency**: Database update frequency forces $> 500$ cache invalidations per minute, invalidating local caches faster than the hit-rate threshold ($< 40\%$ hit rate).