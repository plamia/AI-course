# MRG `cart-api` — Critical-Risk Mitigation Design

**Solution:** Meridian Retail Group checkout and order-processing service  
**AI feature:** “Summarise my cart”  
**Source risk register:** `02-risks.csv`  
**Planning date:** 2026-09-27  
**Assessment status:** Proposed controls; implementation evidence and human approval required

## 1. Top critical risk

| Field | Value |
|---|---|
| Risk ID | T-08 |
| Element | `cart-api` process |
| STRIDE category | Denial of Service |
| Threat | An attacker sends oversized carts or repeatedly invokes the AI-summary endpoint, exhausting pod memory and causing `OOMKilled`, `CrashLoopBackOff`, rising latency, and checkout errors. |
| Likelihood | **High (5)** |
| Impact | **High (5)** |
| Score | **25 — Critical** |
| Primary CIA property | **Availability** |
| Existing evidence | The Module 800 incident showed `OOMKilled` following deployment of the AI-summary step. Resource limits, request bounds, and enforced DIAL budget controls were not evidenced as implemented. |

## 2. Blast radius

If T-08 succeeds, the known blast radius is:

- **3 of 3** `cart-api` replicas may become unavailable.
- **1** customer checkout service may be degraded or unavailable.
- **1** AI cart-summary feature may become unavailable.
- Up to **3,000,000 AI calls/month** are forecast.
- Up to **$15,000/month** of forecast AI spend is exposed without an enforced lower ceiling.
- The proposed DIAL hard cap is **$12,000/month**, but enforcement evidence is still required.
- The exact number of affected active customers and sessions is:

```text
UNKNOWN — Product/Operations owner needed
```

The top business consequence is loss of checkout availability. The AI summary feature must never be allowed to take down the normal cart and checkout path.

---

## 3. Defence-in-depth control triple

### 3.1 Preventive control — bounded AI-summary requests

| Field | Design |
|---|---|
| Control ID | PREV-08 |
| Control class | **Preventive** |
| Accountable owner | **K. Yoon — MRG Checkout Engineering Lead** |
| Deadline | **2026-10-04** |
| Threat property protected | **Availability** |
| STRIDE match | A Denial-of-Service threat consumes memory, request capacity, model capacity, and budget. This control rejects or bounds work before it can exhaust those resources. |

#### What the control does

Implement a bounded request policy for the AI-summary path:

- Maximum HTTP request body: **64 KiB**.
- Maximum cart line items: **100**.
- Maximum AI-summary requests: **10 requests per authenticated customer per minute**.
- Maximum model input: **4,000 tokens per request**.
- Maximum model output: **300 tokens per request**.
- Model-call timeout: **30 seconds**.
- Retry cap: **2 retries** for transient failures and **0 retries** for clear client errors.
- Maximum memory per `cart-api` container: **512 MiB**.
- Minimum requested memory per container: **256 MiB**.
- DIAL warning threshold: **$9,000/month**.
- DIAL critical threshold: **$10,800/month**.
- DIAL hard AI cap: **$12,000/month**.
- When an AI limit is reached, return the normal cart without an AI summary.

#### Acceptance criteria

The preventive control passes when:

1. A cart with **100 or fewer** line items may proceed to the summary path.
2. A cart with **101 or more** line items is rejected before a model call.
3. A request body over **64 KiB** is rejected.
4. The eleventh summary request from the same customer in one minute is rate-limited.
5. A model call exceeding **30 seconds** is terminated.
6. No request performs more than **2 transient retries**.
7. Rejection of the AI request does not prevent normal cart or checkout use.
8. Kubernetes enforces the requested memory values.
9. DIAL refuses AI usage after the **$12,000 monthly hard cap**.

#### Evidence required

- Application or gateway policy configuration.
- Kubernetes resource configuration.
- DIAL budget-policy configuration.
- Automated bypass tests for oversized carts, excessive request rate, timeout, retry, and cap behaviour.
- Test output showing that checkout remains available after AI-summary refusal.

---

### 3.2 Detective control — resource and abuse alerting

| Field | Design |
|---|---|
| Control ID | DET-08 |
| Control class | **Detective** |
| Accountable owner | **Priya Nair — MRG Site Reliability Engineering Lead** |
| Deadline | **2026-10-08** |
| Threat property protected | **Availability** |
| STRIDE match | Prevention may miss a new resource-exhaustion path. This control detects memory pressure, pod failure, request abuse, and unusual AI cost before all replicas or the budget are exhausted. |

#### What the control does

Configure correlated alerts for:

1. **Pod memory warning:** container memory exceeds **80% of its 512 MiB limit for 5 minutes**.
2. **Pod memory critical:** container memory exceeds **90% of its limit for 2 minutes**.
3. **Pod crash:** any `OOMKilled` event or `CrashLoopBackOff` state.
4. **Replica availability:** fewer than **2 of 3** replicas are ready for **2 minutes**.
5. **Error-rate spike:** errors exceed **2% for 5 minutes**.
6. **Latency spike:** p95 latency is greater than **2× the approved baseline for 5 minutes**.
7. **Request abuse:** AI-summary rate-limit denials exceed **20 requests in 5 minutes per customer identity**.
8. **Cost warning:** accumulated AI spend reaches **$9,000/month**.
9. **Cost critical:** accumulated AI spend reaches **$10,800/month**.
10. **Cost anomaly:** daily AI cost exceeds **2× the rolling seven-day daily average**.

#### Alert routing

- Pod, replica, error, and latency alerts route to the `cart-api` PagerDuty service.
- Cost alerts route to the SRE lead and Checkout/Product budget owner.
- A security notification is created when repeated rate-limit denials indicate deliberate abuse.
- Exact PagerDuty service and rotation details remain:

```text
UNKNOWN — Operations owner needed
```

#### Acceptance criteria

The detective control passes when a staging test:

- Produces at least one memory or pod-health alert.
- Produces a rate-limit or cost-policy event.
- Includes service, environment, customer or tenant identifier where permitted, request ID, threshold, and timestamp.
- Reaches the intended notification channel within **5 minutes**.
- Does not include authentication tokens, credentials, or prohibited PII.

#### Evidence required

- Dashboard and alert-rule references.
- Staging test command or procedure.
- Alert payload with secrets and PII redacted.
- Notification timestamp and delivery result.
- Named recipient or rotation.

---

### 3.3 Responsive control — out-of-band AI kill switch and fallback

| Field | Design |
|---|---|
| Control ID | RESP-08 |
| Control class | **Responsive** |
| Accountable owner | **Daniel Cho — MRG Production Operations Manager** |
| Deadline | **2026-10-11** |
| Threat property protected | **Availability** |
| STRIDE match | If resource exhaustion continues despite prevention and detection, this control contains the Denial-of-Service event by stopping new AI-summary calls while preserving the core cart and checkout service. |

#### What the control does

Provide an out-of-band feature switch:

```text
CART_SUMMARY_ENABLED=false
```

The switch must:

- Disable new AI-summary calls without an application code change.
- Require no model-provider response to operate.
- Remain accessible if `cart-api` pods are unhealthy.
- Preserve ordinary cart and checkout functions.
- Return the approved fallback message:

> “The cart summary is temporarily unavailable. Your cart and checkout are not affected.”

- Record who activated it, when, why, and when it was restored.
- Require authorized human activation in production.
- Be tested in staging every quarter and after material changes.

#### Activation procedure

1. The authorized human confirms the incident or attack signal.
2. The authorized human activates the out-of-band switch.
3. Operations confirms no new model calls are being sent.
4. Operations confirms normal cart and checkout requests remain successful.
5. Operations records the activation in the incident timeline.
6. Engineering investigates and drafts the durable fix.
7. A human incident commander approves restoration.

The agent or automated monitor may recommend activation but must not make the production kill-switch decision.

#### Acceptance criteria

The responsive control passes when a staging exercise proves:

1. New AI-summary calls stop within **60 seconds** of activation.
2. Normal cart and checkout requests remain available.
3. The user receives the approved fallback message.
4. DIAL call volume for this feature falls to **0 new calls** after in-flight requests finish.
5. Activation and restoration appear in the audit log.
6. The switch can be operated independently of the failing `cart-api` process.
7. The owner or documented backup can execute the procedure.

#### Evidence required

- Feature-flag or gateway-routing configuration.
- Staging activation and restoration log.
- Before-and-after DIAL call count.
- Successful normal checkout test during the disabled period.
- Audit event identifying the human operator.

---

## 4. Control ownership and delivery plan

| Control | Class | Named accountable owner | Deadline | Required verification |
|---|---|---|---|---|
| PREV-08 — bounded AI-summary requests | Preventive | K. Yoon, Checkout Engineering Lead | 2026-10-04 | Oversized, rate, timeout, retry, memory, and DIAL-cap bypass tests |
| DET-08 — resource and abuse alerting | Detective | Priya Nair, SRE Lead | 2026-10-08 | Staging alert and notification-delivery test |
| RESP-08 — out-of-band AI kill switch | Responsive | Daniel Cho, Production Operations Manager | 2026-10-11 | Staging activation, fallback, audit, and restoration exercise |

All three control deadlines fall within 30 days of the planning date.

The names above are assignments for the MRG reference case. The client must confirm that each person has the authority and access required for the assigned control.

---

## 5. Expected risk after controls

If all three controls are implemented and pass their bypass tests:

| Dimension | Before controls | Expected after controls | Rationale |
|---|---:|---:|---|
| Likelihood | High (5) | Low (2) | Request, rate, token, retry, memory, and cost limits reduce the chance that one abusive input or request stream exhausts the service. |
| Impact | High (5) | Medium (3) | Detection and the kill switch limit the effect primarily to the optional AI-summary feature while preserving checkout. |
| Severity | **25 — Critical** | **6 — Medium** | Residual availability risk remains because novel exhaustion paths, sudden traffic, dependency failure, or delayed human response are still possible. |

This expected score is provisional until the controls are implemented and tested.

---

## 6. Residual-risk acceptance contract

### 1. Risk statement

Because model calls and AI-summary processing consume finite memory, request capacity, provider capacity, and budget, a novel payload, coordinated abuse, dependency failure, or control bypass may still exhaust resources after the proposed controls are implemented. This could temporarily disable AI cart summarisation and, if isolation or fallback fails, degrade the normal `cart-api` checkout path.

### 2. Named owner

**K. Yoon — MRG Checkout Engineering Lead**

The owner is accountable for monitoring the residual risk, ensuring remediation work remains scheduled, and initiating re-evaluation when a trigger occurs.

### 3. Expiry date

**2026-10-27**

Acceptance expires 30 days after the planning date unless an authorized owner replaces it with the project’s approved risk-acceptance period.

### 4. Re-evaluation triggers

Re-evaluate this residual risk before the expiry date if any of the following occurs:

- Any production `OOMKilled` or `CrashLoopBackOff` event affects `cart-api`.
- Fewer than **2 of 3** replicas remain ready for more than **2 minutes**.
- AI-summary error rate exceeds **2% for 5 minutes**.
- AI-summary latency exceeds **2× baseline for 5 minutes**.
- AI spend reaches the **$9,000 warning** or **$10,800 critical threshold** earlier than forecast.
- The DIAL hard cap, retry policy, or rate-limit policy changes.
- A model, provider, prompt structure, or token limit changes.
- Maximum cart size or forecast traffic increases by more than **20%**.
- A new public resource-exhaustion technique affects the selected model or gateway.
- A bypass test, alert test, or kill-switch test fails.
- The AI feature gains any write, payment, inventory, or order-modification capability.

### 5. Approver

**Elena Petrova — MRG Director of Digital Commerce**

The approver must confirm that she is authorized to accept this client-side operational risk. Security, Engineering, or an AI assistant cannot accept the risk on her behalf.

### Acceptance status

```text
PENDING HUMAN APPROVAL
```

This document proposes the residual-risk contract. It does not constitute acceptance until the named approver signs and dates it.

---

## 7. Approval record

| Field | Required entry |
|---|---|
| Decision | Accept / Reject / Require additional controls |
| Approver | Elena Petrova — MRG Director of Digital Commerce |
| Signature or approved workflow reference | Pending |
| Decision date | Pending |
| Expiry date | 2026-10-27 |
| Conditions | All three controls implemented and their bypass tests passed |
| Evidence reference | To be produced in `04-evidence.md` |

---

## 8. Kata 9.5 implementation choice

The control selected for implementation and verification in Kata 9.5 is:

**PREV-08 — bounded AI-summary requests**

The bypass case will submit an oversized cart containing more than **100 line items** and verify that it is rejected before a model call occurs, while the normal cart and checkout path remains available.

The evidence pack must include:

- The control implementation or configuration.
- The exact test command.
- The prohibited input.
- Output proving the request was blocked.
- Output proving no model call occurred.
- Test date.
- Implementation reference.