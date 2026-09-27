---
product: Meridian Omnichannel Commerce Platform
feature: AI Availability Assistant for Click-&-Collect
date: 2026-09-23
---

# Feature Frame

**Product** — Meridian's omnichannel commerce platform serving 1,400 stores across 22 countries, where online product pages and in-store shelf reality drift out of sync.

**Feature** — An AI availability assistant on the product page that estimates whether an item is really collectable at a nearby store before the shopper reserves it, using the SAP inventory sync plus store-level signals.

**Target user** — Click-&-collect shoppers who reserve online specifically to avoid a wasted trip, and who abandon or distrust the channel after a pickup cancellation.

**Expected behaviour** — When a shopper views an item and selects a nearby store, the assistant shows a confidence-graded collectability verdict ("likely collectable" / "check before you go" / "unknown") rather than a raw stock count, and never silently overstates availability.

**Success signal** — Phantom-stock cancellations at pickup drop from ~7% to ≤ 2% within 90 days of rollout, without reducing click-&-collect order volume.

**Out of scope** — Real-time shelf-level RFID tracking, home delivery availability, and stock reservation/hold mechanics (the assistant informs the decision; it does not lock inventory).