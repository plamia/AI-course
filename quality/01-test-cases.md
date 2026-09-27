---
case: "Meridian Retail Group — Omnichannel Commerce Platform (Case A)"
feature: "Click & Collect Cross-Channel Flow — Test Suite"
date: "2026-09-26"
author: "Functional QA Lead"
source_plan: "00-test-plan.md"
---

# 01-Test Cases: Click & Collect (Phase 1)

## Reference In-Scope Surfaces (from `00-test-plan.md`)
1. **Web Reservation & Cart:** Item reservation on `meridian.com`.
2. **Identity Stitching & Account Merge:** Merging in-store loyalty with web accounts via Auth0.
3. **SAP-Sourced Inventory Check at Pickup:** Stock verification and decrement at store pickup counter.
4. **Cross-Region Loyalty-Points Credit:** Automated points crediting upon counter pickup.
5. **POS Pickup Confirmation & SCA:** Mobile POS terminal QR scan and PSD2 SCA payment completion.

---

## Hand-Written Seeds
- **Seed 1 (Web Reservation):** Customer reserves an item online at meridian.com for in-store pickup at the Milano Duomo store.
- **Seed 2 (Identity Stitching):** Unauthenticated web shopper checks out, entering an email matching an existing in-store loyalty account.
- **Seed 3 (SAP Inventory Check):** Store associate scans customer pickup QR at POS while SAP ECC inventory is fresh.
- **Seed 4 (Loyalty Credit):** Customer successfully collects a multi-item pickup order and receives loyalty points.
- **Seed 5 (POS SCA Confirmation):** EU customer completes PSD2 SCA payment challenge on mobile POS during pickup confirmation.

---

## Expanded Risk-Driven Test Suite

| ID | In-Scope Surface | Title / Scenario | Category | Priority | Path / Boundary | Preconditions & Steps | Expected User-Visible Outcome |
|---|---|---|---|---|---|---|---|
| **TC-01** | Web Reservation | Standard Happy-Path Reservation (Milano) | critical-path | 1 | positive / standard | 1. Browse catalog on meridian.com<br>2. Select Milano store pickup<br>3. Submit reservation | Item reserved; confirmation email received with pickup QR code within 60s. |
| **TC-02** | Web Reservation | Cross-Region Reservation (UK Customer, IT Store) | edge | 2 | positive / edge | 1. User with UK profile reserves item for Milano store pickup<br>2. Multi-currency cart conversion applied | Reservation succeeds with localized currency conversion and correct pickup location. |
| **TC-03** | Web Reservation | **Negative:** Reservation with Zero Stock / Phantom Stock | edge | 1 | negative / standard | 1. Reserve item that was just sold out in SAP ECC batch window | System rejects reservation, removes item from cart, and displays out-of-stock notice. |
| **TC-04** | Identity Stitching | First In-Store Pickup Account Merge | critical-path | 1 | positive / standard | 1. Web guest checks out using existing in-store loyalty email<br>2. Complete pickup at store | Auth0 links guest web account with physical loyalty history; points credit correctly. |
| **TC-05** | Identity Stitching | **Negative:** Identity Merge Collision / Conflicting Tiers | edge | 2 | negative / edge | 1. Web checkout email matches two separate legacy CRM records with conflicting tiers | System halts auto-merge, flags profile for manual CS review, and prevents unauthorized data exposure. |
| **TC-06** | Identity Stitching | Guest Checkout Without Existing Loyalty Profile | regression | 3 | positive / standard | 1. Complete web reservation as brand-new guest<br>2. Collect at store counter | System auto-enrolls guest into Meridian loyalty tier 1 and generates temporary member ID. |
| **TC-07** | SAP Inventory Check | Fresh Inventory Sync at POS Pickup | critical-path | 1 | positive / standard | 1. Associate scans customer pickup QR at POS<br>2. SAP inventory cache is fresh (<30s) | POS instantly displays verified stock status and green indicator for checkout. |
| **TC-08** | SAP Inventory Check | **Negative:** SAP ECC Timeout / Down During POS Scan | critical-path | 1 | negative / edge | 1. Associate scans pickup QR while SAP ECC is offline/timeout (>2000ms) | POS falls back to last-known Redis cache state, displays amber "Stock Unverified" warning, and prompts manual floor check. |
| **TC-09** | SAP Inventory Check | Edge-Window Pickup at 47h59m of 48h Window | edge | 3 | positive / edge | 1. Customer arrives 1 minute before 48h expiration to collect reservation | Reservation remains active; pickup completes successfully without auto-cancellation. |
| **TC-10** | Loyalty Credit | Full Order Loyalty Points Crediting | critical-path | 2 | positive / standard | 1. Complete pickup of 3 items<br>2. Associate confirms handover | Loyalty points (10 pts/$1) appear in customer mobile app within 30 seconds of pickup scan. |
| **TC-11** | Loyalty Credit | Partial Pickup Loyalty Points Proration | edge | 2 | positive / edge | 1. Customer picks up 2 out of 3 reserved items (1 item cancelled)<br>2. Confirm partial handover | Loyalty points are credited prorated solely for the 2 collected items; pending balance refunded. |
| **TC-12** | Loyalty Credit | **Negative:** Loyalty Credit Duplicate POS Scan | regression | 3 | negative / standard | 1. Associate scans pickup QR code twice in rapid succession | System detects duplicate transaction ID and blocks duplicate loyalty crediting. |
| **TC-13** | POS SCA Confirmation | EU Customer PSD2 SCA Payment Completion | critical-path | 1 | positive / standard | 1. EU customer checks out at POS requiring SCA<br>2. Complete 3DS biometric challenge on terminal | Stripe verifies SCA challenge; payment settles and order state updates to `COMPLETED`. |
| **TC-14** | POS SCA Confirmation | **Negative:** PSD2 SCA Challenge Failure / Declined | critical-path | 1 | negative / standard | 1. Customer fails biometric SCA challenge or card is declined | POS displays payment failure, preserves cart items, and prompts alternative payment method. |
| **TC-15** | POS SCA Confirmation | **Negative:** Klarna Split-Pay Cancelled Mid-Reservation | edge | 2 | negative / edge | 1. Select Klarna split-pay at checkout<br>2. Abort authorization mid-flow in Klarna app | Checkout service gracefully rolls back reservation, releases inventory hold, and returns user to cart. |

---
- **Owner:** Functional QA Lead
- **Source & Freshness:** `00-test-plan.md`; last reviewed 2026-09-26 (Status: Approved for Execution)