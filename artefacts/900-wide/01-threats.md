# MRG `cart-api` — STRIDE Threat List

**Solution:** Meridian Retail Group checkout and order-processing service  
**AI feature:** “Summarise my cart”  
**Inputs:** `00-dfd.mmd` and `00-assets.md`  
**Method:** STRIDE-per-Element  
**Assessment status:** Initial delivery-team threat enumeration; Security review required

## 1. STRIDE-per-Element rules

The following category constraints were applied:

| Element type | Applicable STRIDE categories |
|---|---|
| External entity | Spoofing, Repudiation |
| Process | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| Data flow | Tampering, Information Disclosure, Denial of Service |
| Data store | Tampering, Information Disclosure, Denial of Service |

Threats were generated for individual DFD elements and then deduplicated. Categories outside the applicable set for an element type were not used.

## 2. Threat list

| Element | Category | Threat | Notes |
|---|---|---|---|
| **Customer — external entity** | **Spoofing** | An attacker uses a stolen or replayed customer authentication token to impersonate another customer and access or modify that customer’s cart. | Targets authentication tokens and cart records. Primary properties: confidentiality and integrity. Token signature, issuer, audience, expiry, and session binding require verification. |
| **Payment provider — external entity** | **Spoofing** | An attacker impersonates the payment provider or forges an authorization response, causing `cart-api` to treat an unpaid order as authorized. | Targets payment authorization references and order integrity. Responses require authenticated transport, provider identity verification, and transaction correlation. |
| **Language-model provider — external entity** | **Repudiation** | The model provider could dispute processing a specific prompt or returning a harmful summary if requests and responses lack immutable correlation IDs and timestamps. | Targets AI audit evidence. DIAL request IDs, timestamps, model version, and policy result should support attribution. |
| **`cart-api` — process** | **Spoofing** | An attacker who obtains the `cart-api` service identity or credential can impersonate the service when calling Postgres, DIAL, inventory, or payment APIs. | Targets database and DIAL credentials. Primary property: confidentiality and integrity. Use scoped, short-lived workload identity rather than shared credentials. |
| **`cart-api` — process** | **Tampering** | A customer submits a crafted cart or order identifier and exploits missing object-level authorization to change another customer’s cart contents, quantity, delivery details, or order state. | Targets cart and order records. Primary property: integrity. Every read and write must be authorized against the authenticated customer identity. |
| **`cart-api` — process** | **Repudiation** | A customer or operator can deny performing a checkout or administrative recovery action if logs do not bind the identity, request ID, timestamp, action, and outcome. | Targets security audit logs and transaction evidence. Audit events must be tamper-resistant and correlated across the gateway, application, and payment provider. |
| **`cart-api` — process** | **Information Disclosure** | Verbose API errors, traces, or application logs expose authentication tokens, database connection details, payment references, cart contents, or AI prompts. | Targets credentials, customer data, payment references, and prompts. Logging and error responses require redaction and minimization. |
| **`cart-api` — process** | **Denial of Service** | An attacker sends oversized carts or repeatedly invokes the AI-summary endpoint, exhausting pod memory and causing `OOMKilled`, `CrashLoopBackOff`, latency, and checkout errors. | Targets service availability and AI budget. The existing incident evidence shows memory exhaustion is credible; request-size, rate, token, retry, and cost limits are required. |
| **`cart-api` — process** | **Elevation of Privilege** | Exploitation of the application or its overprivileged Kubernetes service account allows an attacker to access secrets or resources beyond the requesting customer’s cart. | Targets database credentials, DIAL credentials, CI/CD identity, and customer records. Service-account permissions and network access require least-privilege review. |
| **EPAM DIAL gateway — process** | **Tampering** | Malicious customer or catalogue text embedded in cart content acts as indirect prompt injection and changes the summary instructions, causing the model to ignore the approved prompt or misrepresent the cart. | AI-specific threat related to OWASP LLM01 Prompt Injection. Targets summary and cart integrity. Product descriptions and all retrieved content remain untrusted. |
| **Client → load balancer request — data flow** | **Tampering** | An attacker modifies or replays a cart or checkout request in transit or through a compromised client to change item IDs, quantities, prices, or idempotency values. | Targets cart and order integrity. TLS alone does not replace server-side authorization, schema validation, price recalculation, replay protection, and idempotency controls. |
| **`cart-api` → DIAL prompt — data flow** | **Information Disclosure** | Customer identifiers, payment references, or unnecessary cart metadata are included in the prompt and leave the application boundary for DIAL and the model provider. | AI-specific threat related to OWASP LLM02 Sensitive Information Disclosure. Targets customer data and AI prompts. Prompt construction must minimize and redact data. |
| **DIAL → model provider request — data flow** | **Denial of Service** | Repeated, oversized, or retry-amplified model requests consume token capacity and budget until AI summarisation is refused or dependent services slow down. | AI-specific threat related to OWASP LLM10 Unbounded Consumption. Targets availability and budget. DIAL warning, critical, and hard-cap enforcement require evidence. |
| **Postgres carts and orders — data store** | **Tampering** | A compromised `cart-api` identity or vulnerable query path modifies prices, ownership, payment state, or order status directly in Postgres. | Targets cart, order, and payment-reference integrity. Controls should include parameterized queries, row/object authorization, constrained database roles, and audit records. |
| **Redis sessions and cart cache — data store** | **Information Disclosure** | An attacker with network or credential access reads active session or cached cart records from Redis and uses them to expose or hijack customer activity. | Targets sessions and cart data. Redis must be private, authenticated, encrypted where required, access-scoped, and configured with appropriate retention. |

## 3. Coverage summary

| Element type | Threat rows | Applicable categories represented |
|---|---:|---|
| External entities | 3 | Spoofing, Repudiation |
| Processes | 7 | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| Data flows | 3 | Tampering, Information Disclosure, Denial of Service |
| Data stores | 2 | Tampering, Information Disclosure |
| **Total** | **15** | All element types covered |

## 4. Classical and AI-specific split

### Classical threats

- Customer-token impersonation.
- Forged payment-provider responses.
- Service-identity theft.
- Broken object-level authorization.
- Missing transaction audit evidence.
- Sensitive information in logs and error responses.
- Resource exhaustion and pod crashes.
- Overprivileged Kubernetes identity.
- Request tampering or replay.
- Postgres record tampering.
- Redis session disclosure.

### AI-specific threats

- Indirect prompt injection through product or cart content.
- Sensitive information included in prompts.
- Unbounded model usage, retries, and cost.
- Insufficient model request/response attribution.

The AI-specific findings do not replace the classical findings. Both threat sets apply to the same service.

## 5. Priority candidates for risk scoring

The following threats should receive particular attention in `02-risks.xlsx`:

1. **Unauthorized modification of another customer’s cart or order** through missing object-level authorization.
2. **Sensitive customer information leaving the application boundary** in an AI prompt.
3. **Indirect prompt injection** through untrusted product or cart content.
4. **AI and pod resource exhaustion** through oversized or repeated requests.
5. **Compromise of the `cart-api` service identity** and resulting access to Postgres, Redis, DIAL, or payment services.

No final severity or risk acceptance decision is made in this file. Likelihood and impact will be scored in Kata 9.3 using the course 5×5 method.

## 6. Human review required

- **Architecture owner:** Confirm that every referenced element and flow matches `00-dfd.mmd`.
- **Application owner:** Confirm authorization, validation, query, and logging behaviour.
- **Platform owner:** Confirm service-account scope, network controls, rate limits, DIAL limits, and data-store isolation.
- **Security owner:** Review STRIDE classification, remove non-credible threats, and identify missing attack paths.
- **Privacy owner:** Confirm which customer fields may enter prompts, logs, and third-party processing.