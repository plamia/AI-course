---
project: EU Machinery Corp — ERP Modernisation & AI Sales-Ops
artefact: Solution Outline
date: 2026-09-27
compliance_shape: Turn-key (EPAM-delivered solution)
author: Delivery Lead / Solution Architect
---

# Solution Outline: EU Machinery Corp ERP & AI Sales-Ops

## 1. High-Level Approach
We propose a modern, cloud-native integration and engagement platform built natively on EU Machinery Corp's existing Microsoft Azure enterprise tenant. The architecture decouples the 14-year-old custom ERP integration layer using Azure Integration Services (API Management, Logic Apps, Service Bus), establishing a secure, event-driven integration backbone. On top of this backbone, we deploy a high-performance B2B Customer Self-Service Portal (React / Azure App Service) for real-time order visibility, and an AI Sales-Ops Assistant leveraging Azure OpenAI and the DIAL framework. The AI assistant uses Retrieval-Augmented Generation (RAG) against enterprise price books with mandatory Human-in-the-Loop (HITL) approval workflows for high-value quote drafting, guaranteeing strict compliance with GDPR and the EU AI Act.

## 2. Compliance Shape
- **Shape Committed:** **Turn-key (EPAM-delivered solution)**.
- **AI Tooling & IP Baseline:** EPAM pre-approved AI tools (DIAL, CodeMie, GitHub Copilot) operating within EU-sovereign Azure regions. All PII/PHI processing complies with the EPAM Data Classification Matrix under an executed Data Processing Agreement (DPA) and DPO sign-off.

## 3. Delivery Phases

| Phase | Entry Criteria | Exit Criteria | Duration | Owner Role |
| :--- | :--- | :--- | :---: | :--- |
| **Phase 1: Discovery & Architecture Foundation** | - Signed contract & NDA.<br>- Access to legacy ERP schema docs.<br>- Key stakeholder availability. | - Signed API Integration Spec.<br>- Validated & cleansed price-book dataset.<br>- Provisioned Azure Landing Zone. | **2 Months** (M1–M2) | Enterprise Architect |
| **Phase 2: Integration Backbone & Portal Build** | - Phase 1 signed API Spec.<br>- Azure environment clearance. | - Core ERP endpoints migrated to Azure API Gateway.<br>- Customer Portal MVP in staging with 100% test coverage. | **5 Months** (M3–M7) | Delivery Lead |
| **Phase 3: AI Assistant Engine & Regulatory Audit** | - Staging portal live.<br>- Cleaned price-book dataset indexed in Azure AI Search. | - RAG accuracy ≥95% on test golden set.<br>- HITL workflow functional.<br>- Third-party EU AI Act audit clear. | **2 Months** (M8–M9) | AI Technical Lead |
| **Phase 4: Multi-Site Pilot & Production Cutover** | - Phase 3 sign-off.<br>- UAT approval from pilot site (Site 1). | - 9 EU sites cut over to modern middleware.<br>- Legacy middleware shut down.<br>- Zero transaction loss during cutover. | **3 Months** (M10–M12) | Operations / Cutover Lead |

## 4. Outsourced Capability Plan
- **Outsourced Capability:** Third-Party EU AI Act Regulatory Compliance Audit & External Penetration Testing.
- **Sub-Vendor Partner:** CyberGuard EU Security & Compliance Advisors (N&N Partner).
- **Integration Plan:** CyberGuard EU conducts continuous automated vulnerability scans during Phase 2/3 and performs an independent regulatory audit during Phase 3 prior to cutover.
- **Governance & Control:**
  - **Gate:** Hard Stop Gate before Phase 4 site rollout. Phase 4 cannot start without a signed Attestation Report from CyberGuard EU.
  - **Evidence:** CyberGuard EU Final Compliance Certificate & Penetration Test Remediation Report.
  - **Escalation Path:** If non-compliance is identified, an immediate joint escalation meeting is triggered between EPAM Delivery Lead, CyberGuard Principal, and Client Steering Committee with a mandatory 10-day remediation SLA.

## 5. Key Assumptions
1. Legacy ERP database schemas and API interfaces will remain frozen during Phase 2 integration development.
2. EU Machinery Corp provides dedicated legacy ERP domain specialists (minimum 15 hours/week) during Phase 1 Discovery and Phase 4 UAT.
3. Cleaned, machine-readable price-book data for quote generation will be formally validated and signed off by the Client Product Owner in Phase 1.

## 6. Client-Side Dependencies
1. Azure Tenant Enterprise Admin access provisioned within 10 business days of project kickoff.
2. Formal UAT defect resolution and sign-off turnaround within 5 business days per site review cycle.
3. Legacy ERP vendor support availability during the Phase 4 cutover weekend windows.

## 7. Out-of-Scope Statement
Core legacy ERP database schema re-engineering, hardware/infrastructure provisioning outside Azure EU regions, B2C consumer functionality, and legacy middleware maintenance post-Month 12 cutover are explicitly out of scope.