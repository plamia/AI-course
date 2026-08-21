# Prompt Template: Draft Acceptance Criteria from a User Story

**Date:** 2025-06-12
**Author:** Plamena Kichukova — Developer
**Project:** Meridian Retail Group (MRG) — Omnichannel Commerce Platform (Case A)
**Model:** Claude Opus 4.8 (via EPAM DIAL)
**DIAL location:** https://chat.lab.epam.com/share/JoJAiNuNCcimSysC7vnUeC6NUPtVP4w3pdLS4k76bEGV6Wra8jQggocFAn5SjqYvQe77BA2xysbEZnB6e4oU4LNFpwz1sp7w2jJFs2SecXviSkP9GXM33LAhMcGCY49WGDrnNS2CoysA14kv4D6dU8qQ5
**Committed location:** https://github.com/plamia/AI-course/blob/main/prompt-template-acceptance-criteria.md

---

## Purpose

This prompt converts a raw user story into testable, Gherkin-style acceptance criteria for the BA cell, developers, and QA during sprint refinement on the MRG commerce platform.

---

## Variable Placeholders

| Placeholder | Description | Example value |
|---|---|---|
| `{{user_story}}` | The raw user story text, in "As a… I want… so that…" form | "As a returning customer, I want my loyalty points to be visible at checkout so that I can apply them to my order across web and in-store channels." |
| `{{context}}` | Relevant system/domain context the criteria must respect | "Unified loyalty on commercetools; points synced via Kafka; one Auth0 identity across web/mobile/POS; SAP = inventory ground truth." |
| `{{constraints}}` | Non-functional or compliance constraints to enforce | "GDPR consent before display; <500ms load; graceful degradation if loyalty service down; PSD2 SCA for EU cards." |
| `{{max_criteria}}` | Maximum number of acceptance criteria to return | "8" |

---

## Output Format Instruction

Return the acceptance criteria as a numbered list in Gherkin format (Given / When / Then), one scenario per item. Include at least one negative/edge case and one compliance-related criterion where relevant. Do not exceed `{{max_criteria}}` items. No preamble, no summary — output the numbered list only.

---

## Prompt Body

You are a business analyst assistant for a headless commerce platform. Convert the
user story below into testable acceptance criteria.

Return the acceptance criteria as a numbered list in Gherkin format (Given / When /
Then), one scenario per item. Include at least one negative/edge case and one
compliance-related criterion where relevant. Do not exceed {{max_criteria}} items.
No preamble, no summary — output the numbered list only.

Use only the information provided. Where the story is ambiguous, write the criterion
to the most reasonable interpretation and do not invent unrelated features.

USER STORY:
{{user_story}}

SYSTEM CONTEXT:
{{context}}

CONSTRAINTS:
{{constraints}}

---

## Test Run (Author)

**Input values used:**
- `{{user_story}}` = "As a returning customer, I want my loyalty points visible at checkout so I can apply them across web and in-store channels."
- `{{context}}` = "Unified loyalty on commercetools; points synced via Kafka; one Auth0 identity across web/mobile/POS; SAP = inventory ground truth."
- `{{constraints}}` = "GDPR consent before display; <500ms load; graceful degradation if loyalty service down; PSD2 SCA for EU cards."
- `{{max_criteria}}` = 8

**Output quality:** Output was usable as-is — 8 well-formed Gherkin criteria including a graceful-degradation edge case and a GDPR-consent compliance criterion.

---

## Peer Review

**Reviewer:** Viktor Karaulanov — Senior Front-End Engineer
**Date reviewed:** 2025-06-12
**Model used by reviewer:** Claude Opus 4.8 (via EPAM DIAL)

**Reviewer input values used:**
- `{{user_story}}` = "As a mobile app user, I want to save items to a wishlist so that I can purchase them later from any device where I'm signed in."
- `{{context}}` = "Wishlist feature on MRG headless platform (commercetools); Auth0 identity across iOS/Android/web; wishlist state persisted via commercetools Custom Objects API, synced near real-time; product availability and pricing fetched live at view time."
- `{{constraints}}` = "Sync across devices within 2s; GDPR export/deletion must include wishlist data; 100-item limit per user; guests cannot persist across sessions; discontinued/out-of-stock items flagged, not silently removed."
- `{{max_criteria}}` = 8

| Review question | Reviewer answer |
|---|---|
| Could you run the template without asking the author anything? | Yes — I did not need to ask anything. |
| Was the output format what you expected? | Yes — definitely, I am satisfied. |
| Would you use this template on your own work? | Yes — it looks very useful. |
| One concrete improvement suggestion | No suggestion. |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2025-06-12 | Initial commit | Plamena Kichukova |
| 1.1 | 2025-06-12 | Peer-reviewed by Viktor Karaulanov (Senior Front-End Engineer). Ran independently on a wishlist user story with `{{max_criteria}}=8` — returned exactly 8 consolidated Gherkin criteria, no help needed. Template validated; no changes required. | Plamena Kichukova |
