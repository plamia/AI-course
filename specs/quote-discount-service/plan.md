# Architectural Component Plan: `quote-discount-service`

## 1. Component Overview & Architecture

The service consists of 5 modular components wired cleanly inside the Fastify application container:

```text
[HTTP Client] 
     │
     ▼
(1) Fastify Gateway Routes & TypeBox Validation (`src/routes/v1/quotes.ts`)
     │
     ├─► (2) Redis Atomic Rate Limiter (`src/services/rate-limiter.service.ts`)
     │
     └─► (3) Quote Discount Calculator (`src/services/quote-calculator.service.ts`)
              │
              ├─► (4) ERP Price-Book Adapter & Fallback Cache (`src/adapters/erp/price-book.adapter.ts`)
              │
              └─► (5) HITL Event Publisher (`src/events/hitl-publisher.service.ts`)