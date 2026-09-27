# MRG `cart-api` — PREV-08 Security Control Evidence

**Solution:** Meridian Retail Group checkout and order-processing service  
**Control:** PREV-08 — bounded AI-summary requests  
**Source mitigation:** `03-mitigation.md`  
**Evidence status:** Implemented and locally verified; production deployment is not claimed

---

## 1. Control identity

| Field | Evidence |
|---|---|
| Control ID | `PREV-08` |
| Control class | Preventive |
| Threat ID | `T-08` |
| Threat | Oversized or repeated AI-summary requests exhaust memory or capacity, causing `OOMKilled`, `CrashLoopBackOff`, latency, and checkout errors. |
| STRIDE category | Denial of Service |
| CIA property protected | Availability |
| Plain-language description | The control rejects an AI-summary request containing more than 100 cart line items before the model is called. Rejecting the optional summary does not disable the normal cart and checkout path. |
| Scope | MRG `cart-api` AI “summarise my cart” path |
| Named owner | K. Yoon — MRG Checkout Engineering Lead |
| Implementation | `security_controls/cart_summary_bounds.py` |
| Verification script | `security_controls/verify_cart_summary_bounds.py` |
| Source commit | `f8af43d1fbe5e0f36b63ae02b6940fad79948602` |
| Framework mapping | Provisional ISO/IEC 27001:2022 Annex A 8.26 — Application security requirements; Annex A 8.28 — Secure coding |
| Mapping status | The Security champion must confirm the client’s authoritative audit-framework mapping. |

### Implemented security behaviour

The implemented control enforces:

```text
Maximum AI-summary cart size = 100 line items
```

An AI-summary request containing **101 or more** line items:

1. Is rejected with `CART_SUMMARY_ITEM_LIMIT_EXCEEDED`.
2. Does not reach the model-call function.
3. Does not disable the normal cart or checkout path.

This implementation proves one bounded-input part of PREV-08. It does not claim that rate limits, token limits, timeouts, Kubernetes memory controls, or DIAL budget caps are already implemented.

---

## 2. Test method

### Test objective

Exercise the prohibited bypass case rather than only the happy path:

> Submit an oversized cart containing 101 line items and verify that it is rejected before any model call occurs while the normal checkout path remains available.

### Prohibited input

The verification script generates the following attack input:

```text
cart_id = security-test-cart
line items = 101
maximum allowed line items = 100
```

Each test item contains a product identifier, quantity, and unit price.

### Exact test command

```bash
python3 security_controls/verify_cart_summary_bounds.py \
  2>&1 | tee artefacts/900-wide/evidence/prev-08-test.log
```

### Exit-status check

```bash
echo $?
```

Expected successful exit status:

```text
0
```

### Implementation reference

```text
security_controls/cart_summary_bounds.py
commit: f8af43d1fbe5e0f36b63ae02b6940fad79948602
```

### Verification reference

```text
security_controls/verify_cart_summary_bounds.py
```

### Test-log path

```text
artefacts/900-wide/evidence/prev-08-test.log
```

### Test date

```text
2026-09-27
```

### Recorded test output

```text
CONTROL_ID=PREV-08
TEST_TYPE=BYPASS_CASE
INPUT_LINE_ITEMS=101
MAX_ALLOWED_LINE_ITEMS=100
CONTROL_RESULT=REJECTED
ERROR_CODE=CART_SUMMARY_ITEM_LIMIT_EXCEEDED
MODEL_CALL_COUNT=0
CHECKOUT_STATUS=AVAILABLE
BYPASS_TEST=PASS
```

### Pass criteria and results

| Requirement | Required result | Recorded result | Status |
|---|---|---|---|
| Oversized input supplied | `INPUT_LINE_ITEMS=101` | `INPUT_LINE_ITEMS=101` | **PASS** |
| Maximum bound enforced | `MAX_ALLOWED_LINE_ITEMS=100` | `MAX_ALLOWED_LINE_ITEMS=100` | **PASS** |
| AI-summary request rejected | `CONTROL_RESULT=REJECTED` | `CONTROL_RESULT=REJECTED` | **PASS** |
| Correct rejection code | `CART_SUMMARY_ITEM_LIMIT_EXCEEDED` | `CART_SUMMARY_ITEM_LIMIT_EXCEEDED` | **PASS** |
| Model call prevented | `MODEL_CALL_COUNT=0` | `MODEL_CALL_COUNT=0` | **PASS** |
| Core checkout preserved | `CHECKOUT_STATUS=AVAILABLE` | `CHECKOUT_STATUS=AVAILABLE` | **PASS** |
| Overall bypass test | `BYPASS_TEST=PASS` | `BYPASS_TEST=PASS` | **PASS** |
| Process exit status | `0` | `0` | **PASS** |

### Verification conclusion

The bypass test passed.

The decisive security evidence is:

```text
CONTROL_RESULT=REJECTED
MODEL_CALL_COUNT=0
CHECKOUT_STATUS=AVAILABLE
BYPASS_TEST=PASS
```

This demonstrates that:

- The prohibited 101-line-item request was rejected.
- The model boundary was not reached.
- The optional AI failure did not disable the normal checkout path.

---

## 3. Monitoring

### Implementation status

```text
DESIGN INTENT — not implemented or production-verified by this kata
```

The production application should emit a structured event whenever PREV-08 rejects a request:

```json
{
  "event": "cart_summary_request_rejected",
  "control_id": "PREV-08",
  "reason": "CART_SUMMARY_ITEM_LIMIT_EXCEEDED",
  "service": "cart-api",
  "feature": "cart-summary",
  "environment": "production",
  "line_item_count": 101,
  "maximum_line_items": 100,
  "request_id": "<generated-request-id>",
  "timestamp": "<UTC-timestamp>"
}
```

The monitoring event must not contain:

- Authentication tokens.
- DIAL credentials.
- Database credentials.
- Payment tokens.
- Customer PII.
- Full cart contents.

### Proposed production alert

| Field | Design intent |
|---|---|
| Metric | Count of `cart_summary_request_rejected` events |
| Warning threshold | More than 10 rejected oversized requests from one authenticated identity in 5 minutes |
| Security threshold | More than 20 rejected oversized requests across the service in 5 minutes |
| Service-impact threshold | AI-summary error or rejection rate greater than 2% for 5 minutes |
| Primary notification | `cart-api` PagerDuty service |
| Accountable owner | Priya Nair — MRG Site Reliability Engineering Lead |
| Security escalation | Notify the Security owner when repeated events indicate deliberate resource abuse |
| Current implementation status | Not implemented or verified in this kata |
| Missing operational detail | Named PagerDuty service and active rotation — Operations owner needed |

The alert should correlate:

- Request ID.
- Authenticated identity or approved pseudonymous identifier.
- Timestamp.
- API route.
- Rejection reason.
- Service and environment.

---

## 4. Audit trail

| Field | Evidence or design |
|---|---|
| Local verification log | `artefacts/900-wide/evidence/prev-08-test.log` |
| Control source | `security_controls/cart_summary_bounds.py` |
| Verification source | `security_controls/verify_cart_summary_bounds.py` |
| Implementation commit | `f8af43d1fbe5e0f36b63ae02b6940fad79948602` |
| Test date | `2026-09-27` |
| Local retention | Retained with the kata artefacts in version control |
| Production retention | `UNKNOWN — Security/Privacy owner needed` |
| Legal basis for production retention | `UNKNOWN — Privacy/Legal owner needed` |
| Kata immutability mechanism | Git commit history; no separate write-once storage |
| Production immutability mechanism | `UNKNOWN — Platform/Security owner needed` |
| Repository access | Restricted to authorized project contributors through repository access controls |
| Production log access | Intended for authorized Operations and Security personnel; implementation is not evidenced |
| Secret and PII handling | The verification log contains no credentials, tokens, payment data, customer PII, or full cart contents |

The kata evidence is a local verification artefact. It is not evidence that the control has been deployed to production or that production monitoring and retention controls are active.

---

## 5. Residual risk and decision

### Verified scope

This evidence verifies the following preventive bound:

```text
AI-summary requests containing more than 100 cart line items are
rejected before a model call while checkout remains available.
```

### Controls not yet verified

The following PREV-08 controls from `03-mitigation.md` remain outside this implementation:

- 64 KiB request-body limit.
- Per-customer request-rate limit.
- Maximum model input-token limit.
- Maximum model output-token limit.
- 30-second model timeout.
- Two-retry cap.
- Kubernetes memory request and limit.
- DIAL warning and critical thresholds.
- $12,000 monthly DIAL hard cap.
- Production alert routing.
- Out-of-band kill switch.

### Residual-risk owner

**K. Yoon — MRG Checkout Engineering Lead**

### Residual-risk status

```text
PENDING HUMAN APPROVAL
```

The implemented control reduces one resource-exhaustion path but does not eliminate T-08. Production approval still requires:

1. Implementation of the remaining preventive controls.
2. Verification of the detective alerts.
3. Verification of the responsive kill switch.
4. Bypass testing of all required controls.
5. Formal acceptance by the named client approver in `03-mitigation.md`.

---

## 6. Evidence summary

| Evidence question | Result |
|---|---|
| Is there a concrete implementation artefact? | **Yes** — `security_controls/cart_summary_bounds.py` |
| Is there a reproducible verification script? | **Yes** — `security_controls/verify_cart_summary_bounds.py` |
| Was the attack input exercised? | **Yes** — 101 line items against a maximum of 100 |
| Was the prohibited request rejected? | **Yes** — `CONTROL_RESULT=REJECTED` |
| Was the correct error code returned? | **Yes** — `CART_SUMMARY_ITEM_LIMIT_EXCEEDED` |
| Was the model call prevented? | **Yes** — `MODEL_CALL_COUNT=0` |
| Did normal checkout remain available? | **Yes** — `CHECKOUT_STATUS=AVAILABLE` |
| Is the implementation committed? | **Yes** — `f8af43d1fbe5e0f36b63ae02b6940fad79948602` |
| Is production deployment claimed? | **No** |
| Are production monitoring controls implemented? | **No — design intent only** |
| Are production audit controls implemented? | **No — not evidenced** |
| Is residual risk formally accepted? | **No — pending human approval** |

## 7. Evidence-pack verdict

**PASS for the locally implemented PREV-08 line-item bound.**

The test performed on **2026-09-27** proves that a 101-line-item AI-summary request is rejected before the model is called and that the normal checkout path remains available.

**Production-readiness status:** **PENDING.** The remaining request, rate, token, timeout, memory, DIAL-cap, monitoring, and kill-switch controls still require implementation and verification.