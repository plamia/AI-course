# 02-Data-Method: Test Data Generation & PII Obfuscation Note
**Module:** 600 — Quality (Wide Path)  
**Kata:** K 6.W.3  
**Status:** Approved for QA Execution & GDPR Compliance  

---

## 1. Generation Method & Tooling
- **Tooling Used:** Approved AI Chat (EPAM DIAL / CodeMie) combined with deterministic synthetic formatting rules.
- **Variety Dimensions Exercised:** 
  1. *Country / Market Band:* Italy (`it_IT`), Germany (`de_DE`), Japan (`ja_JP`), UK (`en_GB`), and US (`en_US`).
  2. *Payment Methods:* Regional local methods (Postepay, SEPA, PayPay, LinePay) alongside global gateways (Visa/Mastercard 3DS, Klarna split-pay).
  3. *Identity Merge States:* Single resolved profiles, unresolved guest accounts, identity collisions (duplicate loyalty matches), and expired loyalty tiers.
  4. *Linguistic / Character Boundaries:* Latin scripts with accents, German compound nouns (`ß`, umlauts), Japanese Kanji/Kana, and special unicode injection symbols.

## 2. PII Safety & GDPR Compliance (Article 30)
- **Obfuscation Rule:** All personal identifiers (names, customer IDs, order IDs, email addresses) have been replaced with fully synthetic, non-production equivalents conforming to realistic structural patterns (e.g., `marco.rossi.synth1@meridian-test.it`, `cust_it_9928101`). 
- **Audit Trail:** In accordance with Asha Sundaram's office (Security & Compliance), this note records that zero production PII exists within `02-test-data.json`. All records are deterministically masked and isolated for test automation environments.

## 3. Explicit Exclusions (Out of Scope)
- **Unlaunched Regional Markets:** Records from geographical regions not scheduled for Phase 1 onboarding (e.g., South America or unlaunched European jurisdictions) have been strictly excluded per `00-test-plan.md`.

---
- **Owner:** Functional QA Lead & Data Quality Specialist
- **Source & Freshness:** `01-test-cases.md`; last reviewed 2026-09-26 (Status: Approved)