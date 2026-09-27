---
project: EU Machinery Corp — ERP Modernisation & AI Sales-Ops
artefact: AI-Native Delivery Section
date: 2026-09-27
framework: EPAM AI-SDLC Maturity Framework v3.0
author: Delivery Manager / AI Delivery Lead
status: APPROVED
---

# AI-Native Delivery Strategy & Target Maturity Model

## 1. Executive Summary & Delivery Commitment
We commit to operating this engagement under an **AI-Augmented to AI-Native (L2 → L3)** delivery model. AI usage on this project is treated as a measured delivery metric rather than a passive productivity hope. Every SDLC phase carries explicit, falsifiable maturity targets, tools pre-cleared against the EPAM GenAI Allow-List, and telemetry-backed metrics with strictly defined denominators.

---

## 2. Per-Phase SDLC AI Maturity Roadmap

| SDLC Phase | Target Maturity (by Month N) | Adoption Metric & Defined Denominator | Tooling Baseline & Allow-List Status | Key Phase Risk | Measurement Source of Truth |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Intake** | **L2 Baseline** (Month 3) | **≥80%** of legacy integration tickets and feature requests parsed into structured API draft requirements via AI. <br>*(Denominator: Total incoming Jira intake tickets)* | **DIAL Platform** (Claude 3.5 Sonnet) <br>*(EPAM Pre-Approved)* | Uncritical acceptance of hallucinated legacy ERP schema fields during automated parsing. | Jira issue logs (`label:ai-triaged`) |
| **2. Plan** | **L2 Baseline** (Month 6) | **≥75%** of user stories contain AI-assisted draft Acceptance Criteria & dependency maps prior to sprint backlog locking. <br>*(Denominator: Total committed backlog User Stories)* | **M365 Copilot + EPAM BA Assistant** (DIAL) <br>*(EPAM Pre-Approved)* | Vague prompt context leading to incomplete edge-case acceptance criteria. | Confluence commit history & Jira field `ai_draft_ac` |
| **3. Build** | **L3 Frontier** (Month 9) | **≥85%** of API integration & portal PRs developed with AI copilot assistance, enforcing version-controlled rules. <br>*(Denominator: Total merged GitHub Pull Requests)* | **GitHub Copilot Enterprise + CodeMie** <br>*(EPAM Pre-Approved)* | Developer over-reliance leading to unhandled legacy ERP transaction exceptions. | GitHub Enterprise Telemetry + Gateway Logs |
| **4. Validate** | **L3 Frontier** (Month 10) | **≥90%** of automated integration tests and RAG price-book golden sets generated and executed via AI eval framework. <br>*(Denominator: Total test suite test cases)* | **CodeMie QA + DIAL RAG Eval Suite** <br>*(EPAM Pre-Approved)* | Overfitting golden-set evaluation prompts resulting in false-positive RAG quote accuracy. | CI/CD Pipeline execution logs & Eval Dashboard |
| **5. Handoff** | **L2 Baseline** (Month 11) | **≥80%** of site deployment runbooks, API gateway documentation, and user guides assembled with AI assistance. <br>*(Denominator: Total 9-site release packages)* | **DIAL Document Synthesizer + M365 Copilot** <br>*(EPAM Pre-Approved)* | Outdated API context files generating stale cutover instructions for site IT teams. | Repository release tag documentation |
| **6. Learn** | **L3 Frontier** (Month 12) | **100%** of bi-weekly retrospectives produce **≥1** version-controlled reusable asset (rule file, prompt, custom skill) committed to Git. <br>*(Denominator: 26 bi-weekly sprint retrospectives)* | **Git Repo** (`/.claude/skills`, `.cursor/rules`) + **DIAL Library** <br>*(EPAM Pre-Approved)* | Prompt decay and asset duplication without active deprecation governance. | Git commit logs under `/.claude/` directory |

---

## 3. Cost Attribution & Telemetry Infrastructure
AI cost is tracked as an explicit delivery metric alongside cycle time and defect density. 

1. **FinOps Granularity:** Token consumption, model selection, and API inference costs are captured at feature and team level via **Module 800 API Gateway Logs** (Azure API Management / DIAL Gateway).
2. **Alert Thresholds:** Automatic alerts trigger if token spend on sales-ops RAG indexing exceeds **€1,500/month** or if average prompt cost per generated quote exceeds **€0.12**.
3. **Daily Active Usage (DAU):** Core delivery team target is **>80% DAU**, cross-referenced against version-controlled asset creation (PRs, committed rules) to eliminate vanity login gaming.

---

## 4. Non-Negotiable Human-Owned Decision Boundary
While AI agents and copilots assist throughout the delivery lifecycle, **no agent makes binding commercial, architectural, or human decisions.** 

The following calls are strictly **Human-Owned**:
* **Commercial & Scope Commitments:** Contract changes, milestone sign-offs, price adjustments, and liability decisions stay exclusively with the **EPAM Delivery Manager** and **Client Executive Sponsor**.
* **High-Value Quote Sign-off:** Sales-Ops AI quote generation enforces a mandatory **Human-in-the-Loop (HITL)** UI gate. Any quote above **€5,000** or with a custom discount requires explicit human sales rep verification before transmission to a client.
* **Final Architectural & Gate Sign-off:** API integration security clearance, EU AI Act compliance certification, and production cutover execution require signed sign-off from the **Enterprise Architect** and **CyberGuard EU Auditor**.
* **People & Performance Management:** Staffing assignments, performance evaluations, and Champion designation remain 100% human-driven.

> *"The agent recommended it"* is contractually defined as invalid defence in any quality, security, or commercial review.