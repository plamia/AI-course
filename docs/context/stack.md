# Warm Context: Stack, Architecture & Pattern Catalog

## 1. Technical Stack Overview
- **Runtime & Language:** Node.js 20 LTS, TypeScript 5.3 (ESNext target, strict mode enabled).
- **Web Framework:** Fastify v4.x (chosen over Express for throughput and schema validation performance).
- **Database & ORM:** PostgreSQL 15 via Prisma ORM v5.x; raw SQL permitted ONLY for complex reporting queries under `src/adapters/erp/raw-queries.ts`.
- **Integration & AI:** Azure API Management Wrapper, Azure OpenAI via DIAL SDK (`@epam/dial-sdk` v1.4.0).
- **Testing Stack:** Vitest v1.2+, Supertest for Fastify HTTP integration testing.

## 2. Key Architectural Constraints & NFR Budgets
- **ERP Middleware Decoupling:** All legacy 14-year ERP calls pass through an event-driven queue (`src/queues/erp-sync.queue.ts`) via Redis / BullMQ.
- **Latency Budget:** API endpoints under `src/routes/v1/` must execute in `< 120ms` (p95).
- **Human-in-the-Loop Gate:** Quote generation workflows above €5,000 must invoke `HITLApprovalService` before returning a finalized payload.
- **Data Residency:** All Azure OpenAI model deployments must strictly point to `westeurope` or `northeurope` regions.

## 3. Preferred Code Patterns & Examples

### API Route Pattern (Fastify + TypeBox)
```typescript
import { FastifyInstance } from 'fastify';
import { Type } from '@sinclair/typebox';

export async function erpRoutes(app: FastifyInstance) {
  app.post('/api/v1/quotes', {
    schema: {
      body: Type.Object({
        clientId: Type.String(),
        lineItems: Type.Array(Type.Object({ partId: Type.String(), qty: Type.Number() }))
      })
    }
  }, async (request, reply) => {
    // Controller logic delegates immediately to Service layer
    const result = await app.quoteService.generateQuote(request.body);
    return reply.status(201).send(result);
  });
}