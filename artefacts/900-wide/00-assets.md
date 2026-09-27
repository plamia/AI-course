# MRG `cart-api` — Asset and Security Surface Inventory

**Solution:** Meridian Retail Group checkout and order-processing service  
**AI feature:** “Summarise my cart”  
**Related DFD:** `00-dfd.mmd`  
**Assessment status:** Initial delivery-team threat-model input; Security review required

## 1. Solution description

The Meridian Retail Group `cart-api` supports customer cart and checkout activity from the web storefront and mobile applications. Requests cross the public perimeter through a load balancer/API gateway and reach three Kubernetes replicas. The service reads and writes cart and order records in Postgres, uses Redis for sessions and caching, checks inventory, and submits tokenized payment-authorisation requests to an external payment provider. For the optional “summarise my cart” feature, `cart-api` sends cart content through the approved EPAM DIAL gateway to a language-model provider. Runtime and security signals are sent to the observability stack.

## 2. Sensitivity scale

| Rating | Meaning |
|---|---|
| **HIGH** | Exposure, modification, or loss could cause customer harm, account compromise, fraud, contractual impact, or a regulatory/security incident. |
| **MEDIUM** | Exposure or modification could disrupt operations or reveal internal or customer-related information, but does not normally provide direct account or payment access. |
| **LOW** | Intended public or aggregated operational information with limited harm if disclosed. |

## 3. Asset inventory

| # | Named asset | Location or processor | Sensitivity | Primary CIA property | AI surface? | Rationale |
|---:|---|---|---|---|---|---|
| 1 | Customer account identifiers and profile data | Postgres and identity claims processed by `cart-api` | **HIGH** | Confidentiality | Possible | Exposure could identify customers and enable account targeting or unauthorized correlation of shopping activity. |
| 2 | Customer authentication tokens and identity claims | Client, API gateway, identity provider, and request context | **HIGH** | Confidentiality / Integrity | No | Theft or tampering could allow account impersonation or unauthorized checkout actions. |
| 3 | Payment tokens and authorization references | `cart-api`, Postgres, and payment-provider exchange | **HIGH** | Confidentiality / Integrity | No | Exposure or manipulation could contribute to payment fraud even though raw card data is not intended to be stored. |
| 4 | Cart and order records | Postgres | **HIGH** | Integrity / Confidentiality | Yes | Unauthorized modification could change prices, quantities, recipients, or order status, while disclosure reveals customer purchase history. |
| 5 | Database credentials and `DATABASE_URL` | Kubernetes secret or approved secret manager | **HIGH** | Confidentiality | No | Compromise could grant direct access to customer, cart, and order records. |
| 6 | DIAL API credential | Kubernetes secret or approved secret manager | **HIGH** | Confidentiality / Availability | Yes | Compromise could enable unauthorized model calls, data transfer, cost abuse, or exhaustion of the AI budget. |
| 7 | AI prompts containing cart contents | `cart-api`, EPAM DIAL, and model provider | **HIGH** | Confidentiality / Integrity | Yes | Prompts contain customer-specific cart details and could accidentally include identifiers or malicious instructions from untrusted product content. |
| 8 | AI-generated cart summaries | EPAM DIAL response and `cart-api` response | **MEDIUM** | Integrity | Yes | Incorrect or manipulated summaries could misrepresent quantities, products, prices, or checkout information to the customer. |
| 9 | Inventory availability and reservation data | Inventory service and `cart-api` request context | **MEDIUM** | Integrity / Availability | No | Incorrect or unavailable inventory data could cause overselling, failed checkout, or incorrect availability information. |
| 10 | Redis session and cart-cache records | Redis | **HIGH** | Confidentiality / Integrity / Availability | Possible | Session exposure may disclose active carts, while tampering or eviction could cause account confusion or checkout disruption. |
| 11 | Application and security audit logs | Observability stack | **HIGH** | Integrity / Confidentiality | Yes | Logs may contain customer identifiers, request details, model metadata, and the evidence required for incident investigation. |
| 12 | DIAL usage, token, denial, and cost records | EPAM DIAL and observability stack | **MEDIUM** | Integrity / Availability | Yes | Tampering could conceal abuse or budget overruns and prevent reliable attribution to the Checkout team. |
| 13 | Kubernetes deployment configuration | Source repository and deployment pipeline | **MEDIUM** | Integrity / Availability | No | Unauthorized modification could deploy an untrusted image, weaken runtime controls, or make the service unavailable. |
| 14 | CI/CD credentials and deployment identity | GitHub Actions and cloud/Kubernetes identity system | **HIGH** | Confidentiality / Integrity | No | Compromise could provide a path to alter or deploy production workloads. |
| 15 | Public product names and descriptions | Storefront catalogue | **LOW** | Integrity | Yes | The information is intended for customers, but manipulated product text could become indirect prompt-injection content when included in an AI prompt. |
| 16 | Aggregate service-health metrics | Observability stack | **LOW** | Availability | No | Aggregated CPU, latency, and availability values contain limited customer information, although they remain operationally useful. |

## 4. Highest-sensitivity assets

The assets requiring the strongest protection are:

1. Customer identity and authentication material.
2. Payment tokens and authorization references.
3. Cart and order records.
4. Database and DIAL credentials.
5. AI prompts containing customer-specific cart contents.
6. Session records and security audit logs.
7. CI/CD deployment credentials.

A compromise of these assets could expose customer information, enable account or payment abuse, manipulate checkout behaviour, produce unbounded AI cost, or interfere with incident investigation.

## 5. Untrusted inputs

The following inputs must remain untrusted even when they originate from an internal or approved system:

- Customer-entered text and request parameters.
- Product names, descriptions, and seller-supplied catalogue content.
- Mobile and browser request headers.
- Identity claims until signature, issuer, audience, and expiry are validated.
- Inventory and payment-provider responses until their authenticity and schema are validated.
- Cart content inserted into the AI prompt.
- Language-model output returned through DIAL.
- Container images, dependencies, and CI actions until provenance and integrity are verified.

“Internal” or “retrieved from an approved source” does not make content trusted.

## 6. Access-scope observations

| Component | Required access | Access it should not have |
|---|---|---|
| API gateway | Validate identities and route approved API requests | Direct database write access |
| `cart-api` | Read/write the requesting customer’s cart and create authorized orders | Unrestricted access to all customer records or raw payment-card data |
| Inventory service | Read inventory and create bounded reservations | Customer profile, payment, or AI-gateway credentials |
| EPAM DIAL | Invoke approved models, enforce policy, attribute cost, and retain approved audit metadata | Direct access to Postgres, Redis, payment APIs, or customer-account administration |
| Language-model provider | Process the minimum approved prompt | Database, Redis, inventory, identity-provider, or payment-provider access |
| CI/CD runner | Build, scan, sign, and deploy through an approved identity | Long-lived production database or DIAL credentials |
| Observability platform | Receive approved telemetry and security events | Unredacted secrets, authentication tokens, or unnecessary prompt content |

## 7. Initial blast-radius statement

The precise number of affected customers, records, and orders is not present in the supplied project artefacts.

```text
UNKNOWN — Product/Data owner needed
```

Before risk scoring, the Product/Data owner must provide:

- Maximum customer records accessible by one `cart-api` identity.
- Maximum active sessions stored in Redis.
- Maximum orders or payment references accessible through one compromised service identity.
- Maximum AI calls and spend possible before the DIAL hard cap activates.
- Log-retention period and maximum number of customer-linked events retained.

The known AI financial ceiling proposed in Module 800 is a **\$12,000 monthly DIAL hard cap**, but implementation and enforcement still require evidence.

## 8. Assumptions requiring confirmation

1. Raw payment-card numbers are not stored or sent to the language model.
2. Payment processing uses tokenized payment references.
3. AI model calls are routed only through EPAM DIAL.
4. The AI prompt requires cart content but does not require customer PII.
5. Postgres and Redis are not publicly reachable.
6. Production secrets will be stored in Kubernetes Secrets or an approved secret manager rather than plaintext manifests.
7. Logs and traces redact credentials, authentication tokens, and prohibited personal data.

Until confirmed by the responsible owner, these remain assumptions rather than verified security controls.

## 9. Human review required

- **Architecture owner:** Confirm the DFD, data flows, and trust-boundary placement.
- **Product/Data owner:** Confirm data classification and quantify the blast radius.
- **Security owner:** Review asset sensitivity and access scope.
- **Privacy/Legal owner:** Confirm personal-data and payment-data obligations.
- **Platform owner:** Confirm network isolation, secrets handling, DIAL routing, and audit coverage.