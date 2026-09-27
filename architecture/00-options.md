# 00-Options: Meridian Inventory & Cart-Bridge Read Model (Phase 1)
**Module:** 400 — Architecture (Wide Path)  
**Kata:** K 4.W.2 (Kata 4.2)  
**Status:** Generated — Awaiting Trade-Off Selection  

---

## Decision Under Evaluation
How the platform reads inventory and bridges online-to-in-store cart reservations while SAP ECC stays the single source of truth for inventory and finance, operating under a $42M/18-month budget with a junior internal product team and a mandatory strangler-fig cutover across 22 regional stacks.

---

### Option 1: Direct Synchronous OData/REST Query against SAP ECC (The Boring & Simple Option)
* **Core Idea in 3 Bullets:**
  - Storefronts and mobile POS apps make direct synchronous REST/OData queries to SAP ECC for real-time stock availability and cart validation.
  - No intermediate caching layer, event brokers, or asynchronous reconciliation pipelines are introduced.
  - Cart reservations are written synchronously into SAP ECC at checkout confirmation.
* **What it optimises for:** Absolute simplicity and zero synchronization drift; zero additional operational components for a junior internal team to manage.
* **What it sacrifices:** Latency (SAP ECC queries take 3–5 seconds, violating p95 $\le 1.5\text{s}$) and availability (if SAP ECC slows down or batches, storefront checkout completely freezes).
* **Hardest Meridian Constraint:** **SAP batch-update reality & latency limits** (SAP ECC cannot handle 1,400 stores and regional web traffic in real-time synchronous calls without catastrophic failure).

---

### Option 2: Event-Driven Read Model via Kafka & Outbox Pattern (The Scalable & Decoupled Option)
* **Core Idea in 3 Bullets:**
  - Introduce an asynchronous event-streaming pipeline using Apache Kafka and the Outbox pattern to hydrate a localized read-optimized Redis/PostgreSQL inventory cache.
  - Storefronts and POS queries query the local read-cache for sub-second stock availability checks ($\le 200\text{ms}$).
  - Checkout reservations update local stock optimistically, while background workers reconcile deltas back to SAP ECC during batch windows.
* **What it optimises for:** Sub-second latency, high availability during traffic spikes, and decoupling store operations from SAP batch constraints.
* **What it sacrifices:** Architectural simplicity; introduces eventual consistency challenges, dead-letter queues, and compensation Sagas when SAP rejects a reservation.
* **Hardest Meridian Constraint:** **Junior team operability vs. distributed systems complexity** (managing Kafka clusters, Outbox patterns, and eventual consistency is steep for a junior internal product team).

---

### Option 3: Bought Cross-Channel Inventory Micro-Service / SaaS Layer (The Outsourced Option)
* **Core Idea in 3 Bullets:**
  - Procure and integrate a pre-built commercial cloud inventory SaaS (e.g., HotWax Commerce or specialized OMS micro-service) to sit between regional stacks and SAP ECC.
  - The third-party SaaS handles multi-location inventory allocation, safety stock buffering, and real-time cart reservations out of the box.
  - Custom adapters sync the SaaS layer with SAP ECC and commercetools.
* **What it optimises for:** Time-to-market and offloading complex distributed inventory logic to a specialized vendor, reducing custom engineering burden.
* **What it sacrifices:** Budget and vendor lock-in; consumes a significant slice of the $42M budget on software licensing rather than core unification.
* **Hardest Meridian Constraint:** **18-month / $42M budget stage-gate pressure** (commercial SaaS licensing fees and complex integration connectors risk blowing the budget before regional strangler-fig cutovers are complete).

---

## Next Steps
All three options remain on the table. In subsequent workflow steps, trade-off scoring and architectural evaluation will be applied to select the definitive path forward (Option 2 selected in architectural baselining, balancing scalability with eventual consistency trade-offs).