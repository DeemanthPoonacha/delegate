# ADR-0006: Bidding vs rate card for the Project tier

- **Status:** Proposed
- **Blocks:** Phase 2 (Sprint 5)
- **Decider:** Founder

## Context

The PRD specifies two tiers — Quick at a requester-set fixed price, Project with doer bidding
(FR-6, FR-11). Open bidding on a marketplace with no reputation history races to the bottom,
which pushes out exactly the doer persona the economics depend on: Arjun, the freelance developer
who will not scroll past ₹100 errands to underbid strangers.

## Options

- **A. Price bidding.** Doers name a price and a pitch. Maximum flexibility, race to the bottom.
- **B. Budget range + pitch, no price bidding.** The requester sets a range; doers apply within it
  and compete on the pitch and their category history.
- **C. Fixed rate card by category.** The platform prices the work. Cleanest for requesters,
  brittle across a 6-week app build and a 2-day CV rewrite.

## Recommendation

**Option B for v1.** The requester already has to state a budget range (FR-5), so the price signal
exists; letting doers undercut it only transfers margin away from supply we cannot yet replace.
Competing on pitch and category history also makes the specialisation badge (FR-25) mean
something, which is the mechanism that is supposed to let good doers charge more.

## Consequences

- FR-11 changes: an application carries a pitch and an accept-at-budget flag, not an arbitrary price.
- Requesters who set an unrealistic range get no applicants, so FR-7 (suggested price range) moves
  from P1 to P0 for the Project tier specifically.

## What would change this

Phase 0 or closed beta showing Project-tier fill rate below 60% because requesters set ranges too
low and doers have no way to counter. That is the signal to allow a counter-offer — which is
Option A with a floor, not open bidding.
