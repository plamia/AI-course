# Kata 8.5 — Monthly Cost Estimate and DIAL Cost Cap

**Service:** Meridian Retail Group `cart-api`  
**Feature:** AI “summarise my cart”  
**Estimate period:** One month  
**Decision:** Ship with mitigation  
**Currency:** USD

## 1. Scope and assumptions

This estimate separates:

1. **Cloud rent** — infrastructure that remains approximately constant in the short term.
2. **AI meter** — usage-based model costs that scale with calls, tokens, retries, and traffic.

| Item | Assumption |
|---|---:|
| Application pods | 3 |
| Database | 1 Postgres instance |
| Cache | 1 Redis instance |
| Load balancer | 1 |
| Estimated cloud rent | $1,500/month |
| AI input tokens per call | 1,200 |
| AI output tokens per call | 200 |
| AI calls per month | 3,000,000 |
| AI input-token price | $2.50 per 1M tokens |
| AI output-token price | $10.00 per 1M tokens |

The cloud-rent figure is supplied by the exercise and includes the three pods, Postgres, Redis, and load balancer.

The AI calculation uses the exercise-provided planning rates. Before production approval, the team must confirm the actual model, region, pricing tier, and current published provider prices.

## 2. Pricing verification record

| Field | Value |
|---|---|
| Provider/model | Exercise planning model; production model must be recorded before release |
| Input price used | $2.50 per 1M tokens |
| Output price used | $10.00 per 1M tokens |
| Source | Exercise input; verify against the selected provider’s current official pricing page |
| Verification status | Planning estimate only—production price verification required |
| Pricing pages | https://openai.com/api/pricing/ and https://www.anthropic.com/pricing |

No claim is made that these rates correspond to a particular current model until the production model and its official price list have been confirmed.

## 3. Line-by-line monthly cost calculation

### 3.1 Cloud rent

```text
3 application pods
+ 1 Postgres database
+ 1 Redis cache
+ 1 load balancer
= approximately \$1,500/month