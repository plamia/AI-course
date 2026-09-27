# SPEC.md — Meridian Availability Assistant
Feature: Cross-Channel Availability / Click-&-Collect Assistant
Case: A — Meridian Retail Group
Kata: K 3.W.7
Input: 04-ai-ac.md · 05-mockup.html
Author: Plamena Kichukova
Date: 25.09.2026

---

## User story
As a click-&-collect shopper, I want the product page to show how confident the system is that
an item is really on the shelf nearby, and how fresh that info is, so that I only travel for a
pickup I can trust.

## Base AC (carried forward)
- AC1: product page shows an availability indicator per nearby store when stock data exists.
- AC2: no store in range → "Not collectable nearby" + delivery option.
- AC3: stock missing for a store → omit that store (don't guess).
- AC4: tap a store → show last-confirmed time + distance.

---

## Components (≥ 2, with states + tokens)

### 1. AvailabilityIndicator
Inline confidence band on the product page and reserve/confirm screens.

| State (variant) | Trigger | Label | Color token | Typography |
|---|---|---|---|---|
| `likely` (green) | confidence ≥ 0.80 AND sync ≤ 15 min | "Likely on shelf" | `color.status.success-muted` | `typography.label.s` |
| `might-be-low` (amber) | confidence 0.50–0.79 OR sync 16–30 min | "Might be low" | `color.status.warning-muted` | `typography.label.s` |
| `cannot-confirm` (grey) | confidence < 0.50 OR sync > 30 min OR no result | "Can't confirm" | `color.status.neutral-muted` | `typography.label.s` |
| `loading` | estimate pending | skeleton shimmer | `color.surface.subtle` | — |

Placement: inline, right of the store name. Always paired with a freshness timestamp
(`typography.caption.xs`, `color.text.subtle`) and a "Why?" tooltip.

### 2. StoreList
List of nearby stores ranked by confidence, then distance.

| State | Behaviour | Tokens |
|---|---|---|
| `populated` | stores ranked confidence→distance; each row shows AvailabilityIndicator | `spacing.sm`, `color.border.subtle` |
| `empty` | no store in range → "Not collectable nearby" + delivery CTA | `color.text.subtle` |
| `error` | confidence service timeout (>3s) → grey "Can't confirm" + retry | `color.status.neutral-muted` |

---

## Refined AI-AC (≥ 3, 6-slot template: Component · Variant · Color token · Typography · Placement · Visual gate)

### AI-AC1 — Confidence
- **Component:** AvailabilityIndicator
- **Variant:** `likely` / `might-be-low` / `cannot-confirm`
- **Color token:** `color.status.success-muted` / `warning-muted` / `neutral-muted`
- **Typography:** `typography.label.s`
- **Placement:** inline, right of the store name on the product page
- **Visual gate:** WHEN confidence ≥ 0.80 AND sync ≤ 15 min → `likely` (green). WHEN sync > 15 min → green is suppressed and band drops to amber/grey. Exactly one band renders.

### AI-AC2 — Refusal / Fallback
- **Component:** AvailabilityIndicator (`cannot-confirm`) + StoreList
- **Variant:** `cannot-confirm` (grey)
- **Color token:** `color.status.neutral-muted`; fallback CTA `color.action.primary`
- **Typography:** `typography.label.s` (band), `typography.body.s` (fallback text)
- **Placement:** grey band on product page; fallback block directly below (alt higher-confidence store + home-delivery CTA)
- **Visual gate:** WHEN `cannot-confirm` → a green/amber estimate MUST NOT render; a "Reserve with free cancellation" CTA + at least one fallback path MUST be visible. Zero dead-end grey states.

### AI-AC4 — Disclosure
- **Component:** FreshnessTimestamp + WhyTooltip (attached to AvailabilityIndicator)
- **Variant:** always-on (all bands)
- **Color token:** `color.text.subtle` (timestamp), `color.text.link` ("Why?")
- **Typography:** `typography.caption.xs`
- **Placement:** timestamp directly under the band; "Why?" as inline link opening a tooltip
- **Visual gate:** WHEN any band renders → freshness timestamp ("stock checked X min ago") AND a screen-reader-reachable "Why?" disclosure MUST be present. No band shown as an unqualified fact.

---

## Negative AC (carried verbatim from AI-AC6 — MUST NOT)
The system MUST NOT:
- show "In stock" or any absolute/binary availability wording anywhere in the flow;
- display a green (`likely`) band on stock synced > 15 min ago;
- reserve an amber/grey item without the free-cancellation option attached;
- send the "Ready for collection" email before a confidence band ≥ 0.50 is confirmed at fulfilment.
> Each forbidden behaviour is a release blocker.

---

## Tokens (referenced)
`color.status.success-muted` · `color.status.warning-muted` · `color.status.neutral-muted`
· `color.surface.subtle` · `color.text.subtle` · `color.text.link` · `color.action.primary`
· `color.border.subtle` · `typography.label.s` · `typography.caption.xs` · `typography.body.s`
· `spacing.sm`

## Asset / data references (resolvable)
- Prototype: `05-mockup.html` (green / amber / grey states, 3 screens).
- Confidence + sync-age fields: returned server-side per store from the SAP-backed confidence service (`GET /stores/{id}/availability` → `{confidence: float, syncedMinutesAgo: int}`).
- Latency budget: p95 render ≤ 1.5s; timeout → grey at 3s (AI-AC3).

---

## Definition of Handoff Done — all 6 pass

- [x] User story + base AC present → SPEC.md top
- [x] ≥ 3 AI-AC refined to component / variant / token / placement / visual gate → AI-AC1, AI-AC2, AI-AC4
- [x] CONTEXT.md covers feature + audience + environment + constraints + out-of-scope → `06-context.md`
- [x] SPEC.md lists ≥ 2 components with states + token references → AvailabilityIndicator + StoreList
- [x] Asset / data reference explicit and resolvable → `05-mockup.html` + `/stores/{id}/availability`
- [x] Negative AC ("must NOT") carried into SPEC.md → Negative AC section (verbatim from AI-AC6)

*Result: An agent-ready handoff (CONTEXT.md + SPEC.md + 3 refined AI-AC) that passes all six
Definition-of-Handoff-Done checks — enough for an AI coding agent to build without follow-up.*