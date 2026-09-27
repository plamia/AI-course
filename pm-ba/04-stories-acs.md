---
product: Meridian Omnichannel Commerce Platform
feature: AI Availability Assistant for Click-&-Collect
date: 2026-09-24
---

# User Stories & Acceptance Criteria

## Story backlog (8–12)

1. As a click-&-collect shopper, I want to see whether an item is really collectable at 
   a nearby store, so that I don't waste a trip.
2. As a shopper, I want to be told when the system is unsure about availability, so that 
   I can decide whether to risk the trip.
3. As a shopper, I want to pick a specific store, so that the verdict reflects the store 
   I'll actually visit.
4. As a shopper, I want the verdict to stay valid from reservation to pickup, so that I'm 
   not surprised at the counter.
5. As a shopper on a slow connection, I want the availability check to respond quickly, 
   so that I don't abandon the page.
6. As a store-operations lead, I want phantom-stock verdicts logged with their confidence 
   score, so that I can audit prediction accuracy per store.
7. As a shopper, I want an alternative nearby store suggested when my chosen store is 
   uncertain, so that I still have a viable pickup option.
8. As a multilingual shopper (EU/JP), I want the verdict in my language, so that I 
   understand the collectability signal.
9. As a shopper, I want the verdict to refresh if I return to the page later, so that I 
   don't act on stale data.
10. As a compliance owner, I want no personal data used in the availability prediction, 
    so that the feature meets EU/JP consent rules.
11. As a shopper, I want a clear "unknown" state rather than a false "in stock", so that 
    I trust the signal over time.
12. As a store associate, I want reserved-but-uncertain items flagged, so that I can 
    verify the shelf before the shopper arrives.

---

## Top 4 stories — Gherkin acceptance criteria (patched for error path + NFR)

### AC-1 (Story 1) — Show a collectability verdict
```gherkin
Given a shopper is viewing an item and has selected a nearby store
When the availability check completes
Then the page shows one of three verdicts: "likely collectable", "check before you go", 
     or "unknown"
And the verdict is never shown as a raw stock count.

# Error path
Given the SAP inventory sync is unreachable
When the shopper requests a verdict
Then the page shows "unknown — check before you go" and does not display any positive verdict.

# NFR
The verdict must render within p95 < 1s (latency).
```
### AC-2 (Story 2) - Communicate uncertainty honestly

Given the prediction confidence is below the display threshold
When the verdict is generated
Then the shopper sees "unknown" and never sees "likely collectable".

# Error path
Given the confidence score is missing or malformed
When the verdict is generated
Then the system defaults to "unknown" (fail-safe, never fail-open to a positive verdict).

# NFR
Verdict accuracy: on a labelled golden set, a "likely collectable" verdict must correspond to actual collectability >= 95% of the time (factuality/quality threshold).

### AC-3 (Story 3) - Store-specific verdict

Given a shopper selects Store X from the store picker
When the verdict is generated
Then the verdict reflects Store X's inventory + store-level signals, not a regional average.

# Error path
Given Store X has no store-level signal data
When the verdict is generated
Then the verdict falls back to "unknown" for that store rather than borrowing another store's data.

# NFR
Store selection change must re-fetch and re-render a verdict within p95 < 1.5s.

### AC-4 (Story 4) - Verdict survives to pickup
Given a shopper reserved an item shown as "likely collectable"
When the item is picked at the counter
Then the phantom-stock cancellation rate for such reservations is <= 2% (measured monthly, per region).

# Error path
Given stock is depleted between reservation and pickup
When the associate cannot fulfil the item
Then the shopper is notified before travel where possible, and the event is logged with the original confidence score for audit.

# NFR
100% of "likely collectable" verdicts are logged with their confidence score and timestamp (auditability/observability).

### AI Eval Card stub (Story 1/2 - the AI-capability story)
AI Eval Card - Availability Verdict Prediction

Capability:        Retrieval + prediction -> confidence-graded collectability verdict

Confidence threshold:
  - >= 0.85 confidence -> show "likely collectable"
  - 0.50 - 0.84        -> show "check before you go"
  - < 0.50 OR missing  -> show "unknown" (refuse to assert)

Refusal trigger:   confidence < 0.50, SAP sync unreachable, missing store-level signal,
                   or malformed score -> return "unknown". NEVER fail-open to positive.

Latency ceiling:   p95 < 1s for verdict render; p95 < 1.5s on store change.

Fallback contract: on any failure/uncertainty -> "unknown - check before you go".
                   Positive verdict is only ever shown above the display threshold.

Output-quality:    "likely collectable" is correct >= 95% on the golden set;
                   phantom-stock cancellations for positive verdicts <= 2% in production.

Gate vs monitor:   >= 95% accuracy = release gate; <= 2% cancellation = 14-day production monitor.

## Fresh-session adversary pass — findings captured
1. Fail-open risk — ...
2. Regional-average leak — ...
3. No auditability NFR — ...