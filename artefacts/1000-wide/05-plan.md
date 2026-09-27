---
project: EU Machinery Corp — ERP Modernisation & AI Sales-Ops
artefact: Implementation & Rollout Plan
date: 2026-09-27
author: Delivery Manager
status: APPROVED
---

# Implementation & Rollout Plan: EU Machinery Corp

## 1. Milestone Roadmap

| Milestone ID | Date / Target | Entry Criterion | Exit Criterion | Single Accountable Owner |
| :--- | :--- | :--- | :--- | :--- |
| **MS-1: Architecture & API Spec Freeze** | Month 2 (Day 60) | Signed contract; Azure tenant access granted; legacy ERP schema docs received. | Cleansed price-book dataset signed off by Client PO; Azure Landing Zone provisioned; API spec approved. | Enterprise Architect |
| **MS-2: Core Integration & Portal MVP Staging** | Month 7 (Day 210) | MS-1 sign-off achieved; Azure API Gateway live in Staging. | 100% legacy ERP endpoints wrapped in Azure APIM; Customer Portal MVP live in staging with 100% test pass. | Integration Tech Lead |
| **MS-3: AI RAG Engine & Regulatory Clearance** | Month 9 (Day 270) | MS-2 sign-off achieved; price book indexed in Azure AI Search. | RAG quote accuracy ≥95% on golden set; HITL workflow active; CyberGuard EU compliance attestation signed. | AI Technical Lead |
| **MS-4: Site 1 Pilot Go-Live & Validation** | Month 10 (Day 300) | MS-3 sign-off achieved; Site 1 staff trained. | Site 1 fully cut over to modern middleware; zero transaction loss; local Site 1 IT sign-off. | Cutover / Ops Lead |
| **MS-5: 9-Site Full Cutover & Legacy Decommission** | Month 12 (Day 360) | MS-4 sign-off achieved; Cluster 1 & 2 UAT passed. | All 9 EU sites cut over; legacy ERP middleware shut down; legacy maintenance contract expired with 0 overhang. | Delivery Manager |

---

## 2. Governance Cadence & Decision Rights

### Named Executive Sponsors (Unblock Authority)
* **Client Executive Sponsor:** Chief Digital Officer (EU Machinery Corp) — holds written authority to unblock client site resources, sign off scope changes, and approve regulatory exceptions.
* **EPAM Executive Sponsor:** VP of Industrial Delivery — holds authority to reallocate global engineering capacity, approve contingency drawdowns, and handle commercial escalations.

### Governance Ceremonies

| Ceremony | Cadence | Required Attendees | Decision Rights & Purpose |
| :--- | :--- | :--- | :--- |
| **Executive Steering Committee** | Monthly (60 min) | Client CDO, EPAM Delivery VP, Delivery Manager, Client IT Director | - Approves Scope Change Requests (>€25k).<br>- Approves milestone schedule shifts (>1 week).<br>- Resolves unblocked inter-site policy or resource deadlocks. |
| **Sprint Review & Planning** | Bi-weekly (90 min) | Delivery Manager, Tech Leads, BA, Client PO, Site Champions | - Formally accepts completed User Stories against Acceptance Criteria.<br>- Locks Sprint Backlog scope for upcoming iteration.<br>- Reviews go-to-green actions for amber/red items. |
| **Bi-weekly Team Retrospective** | Bi-weekly (45 min) | Full Delivery Team, AI Champions | - Decision on process adjustments and rule-file updates.<br>- Votes on prompt/asset deprecation.<br>- Generates at least 1 version-controlled delivery asset per session. |

---

## 3. Change Management Strategy (Beyond Training)

### A. Resistance Handling Matrix

| Resistance Scenario | Root Cause / Pattern | Proactive Response Pattern |
| :--- | :--- | :--- |
| **1. Local Site IT Lead Pushback** | Fearing loss of operational autonomy over local ERP customisations during cutover. | Establish a **Site Engineering Working Group** in Month 4. Involve local leads directly in defining API gateway boundaries and local site fallback runbooks. |
| **2. Sales Rep Mistrust of AI Quotes** | Anxiety that AI quote generation will produce incorrect pricing and damage client relationships. | Enforce a **Human-in-the-Loop (HITL)** UI where reps review AI quote drafts with highlighted RAG price-book citations before sending. Run a 4-week side-by-side comparison pilot. |
| **3. Enterprise Security AI Data Leakage Fears** | Concern over PII or proprietary price tables leaking into public LLMs. | Provide direct access to CyberGuard EU audit reports and demonstrate Azure OpenAI private tenant isolation where zero client data is retained for model training. |

### B. Adoption Tracking Telemetry

| Adoption Behaviour | Target Threshold by Month 6 | Telemetry Collection Source |
| :--- | :--- | :--- |
| **AI Assistant Quote Utilization** | ≥70% of routine sales quotes drafted via AI Assistant. | Azure OpenAI Gateway API Logs & CRM workflow telemetry. |
| **Customer Portal Self-Service Ratio** | ≥50% of order-status lookups performed via self-service portal (vs phone/email). | Customer Portal Web Analytics (Mixpanel / Application Insights). |
| **Team Reusable Asset Contribution** | ≥10 team-contributed prompts/rules committed to Git repo per sprint. | Repository commit log under `/.claude/` or `.cursor/rules`. |

### C. Champion Network (EPAM AI Champion Playbook Aligned)

| Champion Role | Named Profile / Role | Budgeted Protected Time | Core Responsibility |
| :--- | :--- | :---: | :--- |
| **Sales-Ops AI Champion** | Senior Sales Operations Specialist | **20% (1 day/week)** | Promotes AI quote assistant adoption; tunes domain prompts; gathers rep feedback for RAG improvement. |
| **Field Engineering Champion** | Senior Site Tech Lead (Site 1) | **15% (0.75 day/week)**| Coordinates local site UAT; validates legacy API mapping; mentors local site IT staff during cutover. |
| **EPAM AI Delivery Champion** | Lead Software Engineer | **20% (1 day/week)** | Harvests sprint prompts/rules into version-controlled repo; maintains agent context files; tracks DAU telemetry. |

---

## 4. Stakeholder Map & Derived Communication Plan

### A. Stakeholder Map

| Stakeholder | Quadrant (Interest × Influence) | Key Concern | Engagement Signal Monitored |
| :--- | :--- | :--- | :--- |
| **1. Client Chief Digital Officer** | **High Interest / High Influence** | Missing 12-month legacy contract expiry; budget overruns. | Steering Committee attendance; turnaround time on escalated unblock requests (<48 hours). |
| **2. Head of Sales Operations** | **High Interest / High Influence** | AI quote errors damaging key B2B client trust; sales rep workflow friction. | Active participation in sprint reviews; weekly HITL quote approval turnaround velocity. |
| **3. Site IT Managers (9 EU Sites)** | **Medium Interest / High Influence** (Local Veto) | Production downtime or transactional loss during cutover weekend. | Local UAT sign-off speed; promptness of logging severity-1 defect reports (<5 business days). |
| **4. EPAM Delivery Team** | **High Interest / Low Influence** (Commercial) | Scope creep on undocumented legacy APIs destroying fixed-price margin. | Sprint velocity stability; weekly PR review cycle time; retrospective asset output. |

### B. Derived Communication Plan

| Audience | Information Delivered | Channel / Format | Cadence (Derived from Map) | Single Owner |
| :--- | :--- | :--- | :--- | :--- |
| **Client Executive Sponsor & Steering Committee** | Executive Health Dashboard (RAG status, Go-to-Green actions, Milestone burndown, Budget/Contingency burn). | Live Steering Deck + Async Email Readout | **Monthly** (Derived from High Influence / Strategic focus; async 24h alert triggered if Amber/Red). | Delivery Manager |
| **Sales Ops & Site IT Leads** | Functional Demos, System Release Notes, HITL AI Quote Guidelines, Cutover Runbooks. | Teams Live Demo + Confluence Knowledge Portal | **Bi-weekly** (Derived from High Interest / Operational focus; matches sprint delivery cycle). | Change & Training Lead + Champions |