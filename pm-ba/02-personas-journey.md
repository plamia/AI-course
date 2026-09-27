---
product: Meridian Omnichannel Commerce Platform
feature: AI Availability Assistant for Click-&-Collect
date: 2026-09-26
research_note: Personas synthesized from public retail/click-&-collect UX research 
  (NN/g journey mapping, BOPIS abandonment studies). Marked UNVERIFIED — validate 
  with Meridian's own cancellation logs + store-ops interviews before committing.
---

# Personas & Journey

## Persona A — "The Time-Boxed Reserver" (low risk tolerance, high urgency)
- **Goal** — Reserve an item online and pick it up on a tight schedule (lunch break, 
  after work) without driving to a store that turns out to be empty.
- **Friction** — Doesn't trust the website's stock count; a single cancelled pickup 
  wiped out her whole errand and she now assumes "online stock" is fiction.
- **Current workaround** — Phones the store before driving over to have a staff member 
  physically check the shelf, adding 10+ minutes and often a hold-music wait.

## Persona B — "The Opportunistic Grabber" (higher risk tolerance, low urgency)
- **Goal** — Grab a good deal or a nice-to-have item if it's conveniently collectable 
  on a trip he's already making anyway.
- **Friction** — Won't make a special trip; if collectability is uncertain he simply 
  abandons the reservation rather than risk a wasted detour, so Meridian loses the order 
  silently — no cancellation, just no purchase.
- **Current workaround** — Buys the item elsewhere (competitor with delivery) or 
  doesn't buy at all; treats Meridian click-&-collect as unreliable for anything he 
  actually needs.

> **Contrast:** A is a *committed* shopper Meridian loses at *pickup* (a cancellation); 
> B is a *fence-sitter* Meridian loses at *reservation* (an abandonment). The feature 
> must serve both a trust-repair job (A) and a nudge-to-commit job (B).

## Journey — Persona A: from intent to pickup

```mermaid
journey
    title Persona A — Reserve & Collect (current state)
    section Discover
      Sees item online, needs it today: 4: Shopper
    section Check availability
      Reads "In stock" on product page: 3: Shopper
      Distrusts it, phones the store: 2: Shopper
      Waits on hold for staff shelf-check: 1: Shopper
    section Reserve
      Confirms it's really there, reserves: 4: Shopper
    section Travel & collect
      Drives to store on tight schedule: 3: Shopper
      Item found and collected: 5: Shopper
    section Failure path (7% of the time)
      Told at counter item is phantom stock: 1: Shopper
      Errand wasted, trust broken: 1: Shopper