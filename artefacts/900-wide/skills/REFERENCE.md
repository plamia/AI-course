# MRG cart-api Security Skill Reference

`SKILL.md` contains the executable rules and refusal guardrails. This file
contains project context, architecture, assets, risk schema, ownership,
evidence, OWASP context, and platform governance.

## Project

| Field | Value |
|---|---|
| System | Meridian Retail Group `cart-api` |
| Feature | AI “Summarise my cart” |
| Function | Checkout and order processing |
| Users | Web storefront and mobile-app customers |
| Runtime | Kubernetes |
| Replicas | 3 expected |
| Database | Postgres |
| Cache/session store | Redis |
| Inventory | Inventory service |
| Payment | External provider using tokenized references |
| AI gateway | EPAM DIAL |
| Model | External language-model provider through DIAL |
| Observability | Metrics, logs, traces, usage, and cost |
| Production status | Not ready for unrestricted production |
| Top risk | T-08 — AI-summary resource exhaustion/DoS |
| Verified local control | PREV-08 rejects more than 100 line items before model invocation |
| PREV-08 production deployment | Not claimed |
| DIAL warning | $9,000/month |
| DIAL critical threshold | $10,800/month |
| DIAL hard cap | $12,000/month |

## Mandatory DFD components

The DFD must include:

1. Customer/client.
2. Load balancer/API gateway.
3. Kubernetes `cart-api`.
4. Postgres.
5. Redis.
6. Inventory service.
7. External payment provider.
8. EPAM DIAL gateway.
9. External language-model provider.
10. Observability stack.

Ownership does not remove a component from the DFD.

## Required flows

| Flow | Required content |
|---|---|
| Customer → gateway | Customer request, authentication material, cart/checkout parameters; untrusted |
| Gateway → identity provider | Token validation or identity verification |
| Identity provider → gateway | Identity claims and validation result |
| Gateway → `cart-api` | Authenticated request and identity context |
| `cart-api` ↔ Postgres | Cart and order reads/writes |
| `cart-api` ↔ Redis | Session and cart-cache reads/writes |
| `cart-api` ↔ Inventory | Availability and reservation request/response |
| `cart-api` ↔ Payment | Tokenized authorization request/response |
| `cart-api` → DIAL | Minimum-approved cart-summary prompt |
| DIAL ↔ model | Governed model request and untrusted response |
| `cart-api` → gateway | Cart, checkout, and optional summary response |
| Components → observability | Redacted security, usage, error, latency, and cost telemetry |

## Trust boundaries

Expected boundaries:

1. Public client/perimeter.
2. Application/API perimeter.
3. Application services.
4. Protected data stores.
5. Governed AI gateway.
6. External providers.
7. Operations and audit systems.

At least 2 boundaries are required.

## Untrusted inputs

Treat these as untrusted until validated:

- Customer text and request parameters.
- Browser/mobile headers.
- Unvalidated identity claims.
- Product names and descriptions.
- Seller catalogue content.
- Inventory responses.
- Payment-provider responses.
- Cart content inserted into prompts.
- Model output.
- Container images.
- Dependencies and CI actions.
- Deployment manifests.
- Third-party API responses.

## Expected asset fields

Every asset must have:

```text
ID
Asset
Location
Sensitivity
Primary CIA property
AI surface
Rationale
```

Expected assets include:

| Asset | Sensitivity | AI surface |
|---|---|---|
| Customer account identifiers/profile data | HIGH | Possible |
| Authentication tokens/identity claims | HIGH | No |
| Payment tokens/authorization references | HIGH | No |
| Cart/order records | HIGH | Yes |
| Database credentials | HIGH | No |
| DIAL credentials | HIGH | Yes |
| AI prompts containing cart data | HIGH | Yes |
| AI-generated summaries | MEDIUM | Yes |
| Inventory/reservation data | MEDIUM | No |
| Redis sessions/cache | HIGH | Possible |
| Application/security audit logs | HIGH | Yes |
| DIAL usage/cost records | MEDIUM | Yes |
| Kubernetes deployment configuration | MEDIUM | No |
| CI/CD credentials/deployment identity | HIGH | No |
| Product names/descriptions | LOW/MEDIUM | Yes |
| Aggregate health metrics | LOW | No |

## STRIDE rules

| Element type | Allowed categories |
|---|---|
| External entity | Spoofing, Repudiation |
| Process | Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege |
| Data flow | Tampering, Information Disclosure, Denial of Service |
| Data store | Tampering, Information Disclosure, Denial of Service |

Every threat must map to an element present in the DFD.

Required threat fields:

```text
Threat ID
Element
Element type
STRIDE category
Threat
Target asset
CIA property
Classification
OWASP category
Owner/review needed
```

## OWASP LLM Top 10

Exactly these 10 categories are required:

| ID | Category | MRG relevance |
|---|---|---|
| LLM01 | Prompt Injection | Catalogue/cart content may act as indirect instructions |
| LLM02 | Sensitive Information Disclosure | Prompt may contain customer data |
| LLM03 | Supply Chain | DIAL, model, dependencies, images, CI |
| LLM04 | Data and Model Poisoning | Catalogue/input data may be manipulated |
| LLM05 | Improper Output Handling | Summary is returned to customers |
| LLM06 | Excessive Agency | N/A if no model tools/write access exist |
| LLM07 | System Prompt Leakage | Requires review |
| LLM08 | Vector and Embedding Weaknesses | N/A if no vector store/RAG exists |
| LLM09 | Misinformation | Summary may misrepresent products or quantities |
| LLM10 | Unbounded Consumption | Requests, retries, tokens, and cost may exhaust resources |

Each row requires applicability, rationale, target asset, CIA property, and
evidence or missing-evidence text.

## Risk-register schema

The exact required header is:

```csv
id,element,category,threat,classification,owasp_category,asset,cia_property,likelihood,likelihood_rationale,impact,impact_rationale,severity,band,reachability,blast_radius,owner_needed,notes
```

The old header is invalid:

```csv
"#","Element","Category","Threat","Likelihood","L rationale","Impact","I rationale","Severity","Notes"
```

Every data row must contain exactly 18 CSV fields.

| Field | Rule |
|---|---|
| `id` | Unique risk identifier |
| `element` | Existing DFD element |
| `category` | Valid STRIDE category |
| `threat` | Concrete threat |
| `classification` | `Classical` or `AI-specific` |
| `owasp_category` | `LLM01`–`LLM10` or `—` |
| `asset` | Asset from inventory |
| `cia_property` | CIA property or combination |
| `likelihood` | Integer 1–5 |
| `likelihood_rationale` | Evidence-based rationale |
| `impact` | Integer 1–5 |
| `impact_rationale` | Evidence-based rationale |
| `severity` | `likelihood × impact` |
| `band` | Low/Medium/High/Critical |
| `reachability` | Reachable, Partially reachable, or Not currently reachable |
| `blast_radius` | Count or `UNKNOWN — <owner> needed` |
| `owner_needed` | Named owner or responsible role |
| `notes` | Evidence, assumptions, or review notes |

Scoring:

```text
severity = likelihood × impact

1–4: Low
5–9: Medium
10–14: High
15–25: Critical
```

Text labels belong only in `band`. Do not put them in numeric fields. Do not
embed reachability, blast radius, or owner only inside `notes`. Do not include
post-mitigation scores in the initial register.

## Known critical risk

| Field | Value |
|---|---|
| ID | T-08 |
| Threat | Oversized/repeated AI-summary requests exhaust memory, model capacity, or budget |
| CIA | Availability |
| Incident | `OOMKilled` and `CrashLoopBackOff` after AI-summary deployment |
| Replica scope | 3 `cart-api` replicas |
| Potential blast radius | 3 of 3 replicas |
| Customer/session count | Unknown — Product/Data/Operations owner needed |
| Residual-risk owner | K. Yoon — MRG Checkout Engineering Lead |
| Proposed approver | Elena Petrova — MRG Director of Digital Commerce |
| Status | Pending human approval |

## Evidence status

| Item | Status |
|---|---|
| PREV-08 line-item bound | Locally implemented |
| PREV-08 bypass test | Passed for 101 line items |
| Production deployment | Not claimed |
| Kubernetes resource controls | Not fully evidenced |
| Probes | Not fully evidenced |
| Immutable image | Not fully evidenced |
| Secret-store integration | Not fully evidenced |
| CI supply-chain controls | Not fully evidenced |
| DIAL hard-cap enforcement | Not fully evidenced |
| Alert routing | Not fully evidenced |
| Out-of-band kill switch | Not fully evidenced |
| Residual-risk acceptance | Pending human approval |
| Production approval | Not approved |

## Ownership

| Area | Owner/status |
|---|---|
| Application | MRG Product/Checkout |
| Kubernetes, Postgres, Redis | Operations |
| Inventory | Operations/integration owner |
| Payment | Payment/platform owner |
| DIAL/model provider | Operations/provider owner |
| Observability | Operations |
| PREV-08 | K. Yoon — Checkout Engineering Lead |
| Detective controls | Priya Nair — SRE Lead |
| Kill switch | Daniel Cho — Production Operations Manager |
| Residual-risk approver | Elena Petrova — Director of Digital Commerce |
| Architecture | Owner name required |
| Privacy/legal | Owner name required |
| PagerDuty/on-call | Operations owner name required |

These are proposed assignments, not proof of approval or authority.

## Platform compatibility and governance

| Platform | Use | Data/audit requirement | Posture |
|---|---|---|---|
| EPAM DIAL | Governed model gateway | Confirm residency, policy, usage, cost, and audit logs | Preferred when approved |
| CodeMie | EPAM delivery/agent runtime | Confirm workspace residency and audit | Conditional |
| Claude Code | Repository analysis/Skills | Confirm confidential-data approval and audit | Conditional |
| GitHub Copilot | Repository/CI assistance | Confirm enterprise residency and audit | Conditional |
| Amazon Q | AWS assistance | Confirm account, region, and CloudTrail | Conditional |
| GitLab Duo | GitLab assistance | Confirm group tenancy and audit | Conditional |
| Cursor | IDE assistance | Confirm enterprise telemetry and residency | Conditional |
| Tabnine | IDE assistance | Confirm enterprise deployment and logging | Conditional |

Before using any platform, confirm residency, retention/deletion, training-use
restrictions, audit logging, access control, DPA/contractual coverage,
project approval, and whether personal, payment, confidential, or regulated
data is permitted.

## Final governance status

```text
Production approval: NOT APPROVED
Residual-risk acceptance: PENDING HUMAN APPROVAL
```