# ADR-0007: Location-bound physical errands in MVP

- **Status:** Proposed
- **Blocks:** Phase 1 (category taxonomy, matching score, KYC gating)
- **Decider:** Founder

## Context

The PRD puts "physical delivery, transport and home services" permanently out of scope — Dunzo and
Urban Company own that — but two of the four requester personas depend on someone physically
going somewhere: Suresh's EPF paperwork and Ananya's request that a verified doer queue at a
government office for her father. Story 17 prices it at ₹300.

## Options

- **A. Purely remote MVP.** Simplest matching, no location, no physical-safety surface. Drops the
  most differentiated demand the PRD identified.
- **B. One physical sub-category.** "Government and paperwork — in person", Tier 2 doers only,
  inside the launch city.
- **C. Physical errands across all categories.** Location on every task, safety and insurance
  questions we cannot answer at this size.

## Recommendation

**Option B.** The queue-at-an-office task is the single clearest thing Delegate does that nothing
else does, and cutting it to simplify matching would remove the reason two personas show up. One
sub-category, Tier 2 gated, inside one city is a contained surface.

It is contained, not free: it introduces doer physical safety, a "doer did not show up" failure
mode that no remote task has, and a deliverable (a stamped document) that cannot be submitted as
a link. Sprint 3's deliverable templates need a photo-plus-timestamp artefact type for it.

## Consequences

- `task.location` is populated for this sub-category only; the matching score adds a distance term
  that is inert everywhere else.
- Tier 2 (ID + bank match + 10 clean tasks) gates it, which means it cannot launch on day one —
  no doer will have 10 clean tasks. Plan it for closed beta, not for the public launch sprint.
- The NRI requester persona (Ananya) cannot be validated in Phase 0 without it. Include at least
  three in-person concierge tasks in the Phase 0 run.

## What would change this

A doer safety incident, or Phase 0 showing that requesters will not trust a stranger with a
physical document. Either one closes the category and moves this to Option A.
