# Maturity Gap Analysis

**Date:** 2026-08-25
**Author:** Plamena Kichukova — Developer
**Project:** Meridian Retail Group (MRG) — Omnichannel Commerce Platform (Case A)
**Committed location:** https://github.com/plamia/AI-course/blob/main/maturity-gap-analysis.md

---

## Scorecard

| Dimension | Level (L1 / L2 / L3) | Score (1.0 / 2.0 / 3.0) | Evidence (2–3 sentences) |
|---|---|---|---|
| AI Capabilities | L2 | 2.0 | More than 50% of team deliverables are produced with AI assistance today — including code generation, acceptance-criteria drafting, and defect triage. Results are consistent enough to rely on, but AI does not yet autonomously handle sub-tasks end-to-end, so we are augmented (L2), not agentic (L3). |
| Reusability | L2 | 2.0 | The team has recently moved to shared reuse: prompts, skills, agents, and a harness architecture are stored centrally and reused across squads. The Kata 2 acceptance-criteria template (peer-validated by a second engineer, committed to the repo, and shared via DIAL) is one concrete example. We do not yet have codified rules-as-code with automated self-improvement loops, so this is L2, not L3. |
| AI Champions | L2 | 2.0 | Champions are formally designated — the author and the delivery manager (Daniel Sallai) hold a mandate to drive AI adoption, and 3–4 further Champions exist across other teams. Because the role is designated (not merely enthusiast-driven) with at least one Champion on the team, this meets L2. It is not yet embedded across all core roles as a fully connected network, so it is not L3. |
| Performance Tracking | L2 | 2.0 | Productivity metrics are defined and measured in ADO/JIRA: Velocity (story points/iteration), Average Cycle Time, Average Lead Time, Throughput (stories/sprint), and Average Code Review lead time. These are measured continuously, not anecdotal. AI-specific cost tracking and regular formal AI-review cadences are not yet in place, so this is L2, not L3. |
| DAU | L2 | 2.0 | Estimated daily active use of AI tools across the team is above 70% (this is an estimate — we do not yet have tool-level telemetry to confirm it precisely). Usage is majority and habitual rather than occasional. Because it is an estimate above 70% but below a verified 80%, this is scored L2. |
| **Average** | L2 | **2.0** | (2.0 + 2.0 + 2.0 + 2.0 + 2.0) ÷ 5 = 2.0 |
| **Overall Level** | L2 | 2.0 | L1 = 1.0–1.9 / L2 = 2.0–2.9 / L3 = 3.0 |

---

## Gap Analysis

### Gap 1

**Dimension:** DAU
**Current level:** L2
**Why this gap is most damaging:** The >70% figure is an unverified estimate, so we cannot prove adoption depth or spot pockets of non-use that quietly erode the productivity gains the other dimensions depend on.
**Root cause:** There is no tool-level telemetry or defined measurement method for daily AI usage, so the number rests on impression rather than data — the exact "anecdote as metric" risk the maturity model penalizes.

---

### Gap 2

**Dimension:** AI Champions
**Current level:** L2
**Why this gap is most damaging:** AI adoption currently concentrates on a small designated group; if those few people are unavailable, adoption momentum and knowledge transfer stall — a delivery risk on an 80-person, three-SI program with a junior MRG product team.
**Root cause:** The Champion role is designated but not embedded into every core role with a formal cross-team network and cadence, so responsibility for adoption structurally sits with a handful of individuals rather than the whole team.

---

## 30-Day Improvement Plan

### Step 1 — addresses Gap 1 (DAU)

| Field | Value |
|---|---|
| **Action** | Enable and export tool-level usage telemetry (from EPAM DIAL / Copilot admin reporting) and publish a weekly DAU figure for the team in a shared dashboard, replacing the current estimate with a measured number. |
| **Owner** | Plamena Kichukova (Developer / Champion) |
| **Timeline** | 2026-09-24 |
| **Success metric** | A measured team DAU percentage is published for ≥2 consecutive weeks in the shared dashboard (binary: dashboard exists and shows a real number, or it does not). |

---

### Step 2 — addresses Gap 2 (AI Champions)

| Field | Value |
|---|---|
| **Action** | Establish a formal cross-team AI Champions network with a named Champion mapped to each core role (dev, QA, BA, design) and a recurring bi-weekly 30-minute sync, documented in a committed CHAMPIONS.md in the team repo. |
| **Owner** | Daniel Sallai (Delivery Manager) |
| **Timeline** | 2026-09-24 |
| **Success metric** | CHAMPIONS.md is committed listing ≥1 named Champion per core role (≥4 roles covered) and ≥1 recorded network sync has taken place within the 30-day window. |

---

## Peer Review

**Reviewer:** Viktor Karaulanov — Senior Front-End Engineer
**Date reviewed:** YYYY-MM-DD

| Review question | Reviewer answer |
|---|---|
| Is the evidence for each dimension specific and observable — not aspirational? | [One sentence] |
| Which score do you challenge, and why? | [At least one — dimension, proposed alternative score, reason] |
| Is each root cause a structural/behavioural cause — not a symptom? | Yes / No — [one sentence] |
| Are the success metrics measurable without asking the author? | Yes / No — [one sentence] |
| Would you sign off on this plan as a teammate? | Yes / No — [one sentence] |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-25 | Initial commit | Plamena Kichukova |
| 1.1 | YYYY-MM-DD | Post-review update | Plamena Kichukova |
