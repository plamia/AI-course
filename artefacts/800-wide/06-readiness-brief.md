# Cloud Operations & Support Readiness Brief

**Service:** Meridian Retail Group `cart-api`  
**Feature:** AI “summarise my cart”  
**Evidence:** `01-stack-map.md` through `05-cost-estimate.md`  
**Overall status:** 🔴 **NOT READY for unrestricted production**

---

## Executive summary

| Area | Current position |
|---|---|
| **Runtime** | Three `cart-api` replicas run on Kubernetes behind a load balancer and use Postgres, Redis, EPAM DIAL, and a language model. |
| **Top failure** | Pods enter `CrashLoopBackOff` with `OOMKilled` after deployment of the AI summary step. |
| **Monthly cost** | **$16,500/month:** $1,500 cloud rent and $15,000 AI usage. |
| **Cost decision** | **SHIP WITH MITIGATION** under a $12,000 monthly DIAL hard cap. |
| **Support owner** | L2 owns the documented OOM recovery; L3 owns changes requiring engineering work. |
| **Primary gap** | The complete rollback, paging, kill-switch, and gateway-control path is not yet implemented and tested. |

---

## Six readiness questions

### 1. How does it deploy and roll back?

**Status:** 🟠 **GAP — Platform/Release owner**

A push to `main` triggers GitHub Actions. The workflow:

1. Checks out the source.
2. Runs tests.
3. Builds and pushes the container image.
4. Loads the Kubernetes context.
5. Applies `deployment.yaml`.
6. Starts three `cart-api` replicas.

```text
Push to main
    ↓
GitHub Actions tests and builds
    ↓
Container image is pushed
    ↓
deployment.yaml is applied
    ↓
Kubernetes runs three replicas
```

The intended recovery is to restore the previous known-good image. However, the current workflow has no rollback gate and deploys the mutable `latest` tag. Reliable one-step rollback is therefore **not implemented or evidenced**.

Required rollback path:

```text
Deployment health check fails
    ↓
Stop promotion
    ↓
Restore the previous immutable image
    ↓
Run kubectl rollout status
    ↓
Verify pod readiness, latency, and error rate
```

The manifest and pipeline audits also found:

- No resource requests or limits.
- No readiness or liveness probes.
- Plaintext application secrets.
- No explicit safe rolling-update configuration.
- No immutable image version.
- No commit-SHA pinning for GitHub Actions.
- Long-lived credentials instead of OIDC.
- No image signing or provenance.
- No dependency or image scanning.
- No least-privilege workflow permissions.
- No tested rollback gate.

---

### 2. Who gets paged?

**Status:** 🟡 **PARTIAL — Operations owner needed**

The incident runbook defines a `PodCrashLoopBackOff` alert routed through **PagerDuty**. **L2 Application Support** owns the documented diagnosis and recovery.

The following information is not present in Katas 8.1–8.5:

- Named PagerDuty service.
- Active on-call rotation.
- Primary responder.
- Escalation contact and timeout.

**UNKNOWN — Operations owner needed** to provide and validate these details before release.

---

### 3. What is monitored?

**Status:** 🟡 **PARTIAL — Observability owner needed**

The stack map includes an observability stack covering the load balancer, application, Postgres, Redis, and EPAM DIAL.

Required operational signals:

- Kubernetes pod status.
- `CrashLoopBackOff` events.
- `OOMKilled` termination reason.
- Container memory consumption.
- Application latency.
- Application error rate.
- Load-balancer traffic.
- Recent deployment history.
- DIAL calls and retries.
- Input and output token volume.
- Cost per request.
- Accumulated budget consumption.

Exact dashboard links, alert thresholds, evaluation windows, and alert owners are not recorded.

**UNKNOWN — Observability owner needed** to provide and test the production dashboards and alerts.

---

### 4. What is the monthly cost and cap?

**Status:** 🟢 **ANSWERED**

| Cost item | Monthly estimate |
|---|---:|
| Cloud rent | $1,500 |
| AI input tokens | $9,000 |
| AI output tokens | $6,000 |
| **Total AI meter** | **$15,000** |
| **Total operating cost** | **$16,500** |

The **Checkout/Product squad and its P&L** own the feature spend. Infrastructure & Operations implements attribution, monitoring, and enforcement.

Required DIAL controls:

| Control | Required value |
|---|---|
| Attribution | `team=checkout` |
| Service | `service=cart-api` |
| Feature | `feature=cart-summary` |
| Environment | `environment=production` |
| Warning alert | **$9,000/month** |
| Critical alert | **$10,800/month** |
| Hard AI cap | **$12,000/month** |
| Hard-cap action | Refuse only the AI summary call |
| Safe fallback | Keep the normal cart and checkout flow available |

**Decision: SHIP WITH MITIGATION.**

At the current cost of **$0.005 per call**, the $12,000 cap supports approximately **2,400,000 calls/month**, compared with the forecast of 3,000,000 calls. Call volume or average token cost must decrease by at least **20%**.

---

### 5. What is the kill-switch?

**Status:** 🔴 **UNKNOWN — Product and Platform owners needed**

The required kill-switch must:

- Disable only the AI “summarise my cart” feature.
- Require no code change or deployment.
- Preserve the normal cart and checkout flow.
- Be available to an authorized operational owner.
- Record activation and restoration in an audit trail.

No implemented toggle, configuration key, activation procedure, test result, or authorized owner is identified in Katas 8.1–8.5.

---

### 6. Which support tier owns the top two ticket types?

**Status:** 🟡 **PARTIAL — Support owner needed**

| Ticket type | Initial owner | Procedure and escalation |
|---|---|---|
| `cart-api` is slow or unavailable after a release; pods show `CrashLoopBackOff` or `OOMKilled` | **L2 Application Support** | Follow `04-incident-runbook.md`. Confirm OOM evidence, inspect memory and deployment history, and perform approved rollback or temporary scaling. Escalate to **L3** when a code or platform change is required. |
| AI cart summary is unavailable, refused, or budget-capped while checkout remains healthy | **L1 Support** | Confirm that cart and checkout remain available and communicate the safe fallback. L1.5 gathers request IDs, timestamps, and error details. Escalate unexplained or recurring failures to **L2**. |

The approved L1 customer wording, playbook, and escalation thresholds for AI-summary failures are not recorded.

**UNKNOWN — Support/Product owner needed** to approve these items.

---

## Top failure and runbook

### Failure

Following deployment of the AI summary step:

- `cart-api` pods enter `CrashLoopBackOff`.
- Kubernetes reports `OOMKilled`.
- The incident begins approximately 20 minutes after deployment.
- Remaining pods absorb additional traffic.
- Application latency and error rate increase.

### Ranked causes

1. Missing or insufficient memory controls for the AI workload.
2. A memory leak in the AI summarisation code.
3. Additional load overwhelming the remaining healthy pods.

### Detection

- PagerDuty `PodCrashLoopBackOff` alert.
- Kubernetes `OOMKilled` termination reason.
- Rising memory consumption.
- Rising latency and error rate.
- Correlation with a recent deployment.

### L2 recovery procedure

1. Run:

   ```bash
   kubectl get pods -l app=cart-api
   ```

2. Confirm the termination reason:

   ```bash
   kubectl describe pod <pod-name>
   ```

3. Check Grafana memory metrics.
4. Review recent deployment history in GitHub Actions.
5. Check load-balancer traffic for an unusual spike.
6. If release-related, restore the previous known-good version.
7. If caused by a known traffic spike, temporarily scale the deployment:

   ```bash
   kubectl scale deployment cart-api --replicas=6
   ```

8. Add correct memory requests and limits.
9. Optimize and load-test the AI summarisation path.
10. Escalate to L3 if an application memory leak requires a code change.

**Runbook:** `04-incident-runbook.md`  
**Immediate owner:** L2 Application Support  
**Engineering escalation:** L3

---

## L1–L3 support handover

| Tier | Responsibility |
|---|---|
| **L1** | Receive the ticket, identify known cases, confirm that checkout remains available, and communicate the approved fallback. |
| **L1.5** | Gather request IDs, timestamps, DIAL response codes, deployment details, and diagnostic output. |
| **L2** | Inspect telemetry, confirm OOM or deployment correlation, and execute documented rollback, scaling, or configuration recovery. |
| **L3** | Change application or platform code when the documented recovery does not resolve the issue. |

---

## Maturity gap

**Performance Tracking is L2 — Tracked, not L3 — Governed.**

The team has documented its forecast cost and proposed budget thresholds. However, the following L3 governance evidence is still missing:

- Implemented DIAL cost attribution.
- Tested warning and critical alerts.
- Enforced $12,000 hard cap.
- Named budget and alert-review owners.
- Recurring output-per-cost reviews.
- Auditable approval for cap changes.

---

## Required actions before release

| Priority | Required action | Owner |
|---|---|---|
| **P0** | Implement immutable image versions and test one-step rollback. | Platform/Release |
| **P0** | Add resource requests/limits and readiness/liveness probes. | Platform + `cart-api` team |
| **P0** | Move plaintext credentials to an approved secret store. | Platform |
| **P0** | Implement and test the AI kill-switch and checkout-safe fallback. | Product + Platform |
| **P0** | Configure and test DIAL attribution, alerts, and the $12,000 hard cap. | Platform + Checkout budget owner |
| **P0** | Name the PagerDuty service, on-call rotation, and escalation contact. | Operations |
| **P1** | Implement the six missing CI/CD supply-chain controls. | Platform/DevSecOps |
| **P1** | Approve the L1 playbook for AI-summary and budget-cap tickets. | Support + Product |
| **P1** | Reduce forecast AI usage or token cost by at least 20%. | Checkout/Product |
| **P1** | Run rollback, alerting, kill-switch, and support-handover drills. | Operations + Support |

---

## Verdict

**NOT READY for unrestricted production operation and support.** The architecture, primary incident, monthly cost, DIAL cap proposal, and L2 recovery procedure are documented, but critical operational controls remain unimplemented or unverified.

**Primary blocker:** implement and test the complete safety and recovery path—immutable one-step rollback, production-ready deployment controls, confirmed PagerDuty ownership, DIAL cap enforcement, and the AI kill-switch—before release.