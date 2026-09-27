# Incident Diagnosis & Runbook: `cart-api` OOM Crash

## 1. Incident Diagnosis
**Symptoms:** Half of `cart-api` pods are in `CrashLoopBackOff`. Events show `OOMKilled`. Started 20 minutes after a deploy adding the AI summarise step. Latency and error rates are climbing.

### Ranked Hypotheses
| Rank | Hypothesis | Supporting Evidence | Cheapest Next Step to Confirm |
| :--- | :--- | :--- | :--- |
| **1** | **Memory limits too low/missing for the new AI payload.** | `OOMKilled` means Out Of Memory. The crash started exactly after deploying the memory-heavy AI feature. | Run `kubectl describe pod <pod-name>` to check if the container hit its memory limit, or if the node itself ran out of memory. |
| **2** | **Memory leak in the new AI summarise code.** | The crash took 20 minutes to happen, implying memory usage slowly crept up as users hit the new feature until it burst. | Check the observability metrics (Grafana) for `cart-api` memory usage over the last 30 minutes. Look for a steady upward slope. |
| **3** | **Traffic spike overwhelming the remaining pods.** | Latency is rising on the healthy pods as they absorb the load of the dead pods. | Check the load balancer metrics to see if incoming requests spiked unusually high at the same time. |

### Immediate Mitigation & Durable Fix
* **Immediate Mitigation:** Trigger the one-click rollback in the CI/CD pipeline to revert to the previous known-good version (without the AI feature) to stabilize the system and stop the customer-facing errors.
* **Durable Fix:** Update the `deployment.yaml` to include proper `resources.limits.memory` and `resources.requests.memory` (the exact gap we found in our Kata 8.2 audit), and optimize the AI payload size before redeploying.

---

## 2. Runbook Entry
*This is the playbook the support team will follow if this happens again, preventing an expensive escalation to L3 Engineering.*

| Runbook Section | Details |
| :--- | :--- |
| **Detection Signal** | Alert: `PodCrashLoopBackOff` fires in PagerDuty. Logs show `Reason: OOMKilled` for the `cart-api` service. |
| **Diagnosis Steps** | 1. Run `kubectl get pods -l app=cart-api` to confirm pod status.<br>2. Check Grafana memory metrics for the pod.<br>3. Check recent deployment history in GitHub Actions. |
| **Fix (Resolution)** | If memory is exhausted due to a known traffic spike, temporarily scale up the replicas: `kubectl scale deployment cart-api --replicas=6`. |
| **Rollback Path** | If the crash is tied to a recent deployment, immediately revert to the previous version using the CI/CD Rollback Gate. |
| **Owning Support Tier** | **L2 (Application Support)** - L2 can read the logs, confirm the OOM status, and execute the rollback or scale-up without needing to page L3 Engineering. |