# Decision log

One file per decision that changes what gets built. Each ADR states the options, the trade-offs,
a recommendation and what evidence would overturn it. **Status is `Proposed` until the founder
writes `Accepted` and a date at the top of the file.** Nothing here is decided yet.

| ADR | Decision | Blocks | Status | Recommendation |
| --- | --- | --- | --- | --- |
| [0001](ADR-0001-payment-architecture.md) | Payment and escrow architecture | Phase 3 | Proposed | Merchant of record + payout rails, with a licensed PA; escrow provider only above ₹5,000 |
| [0002](ADR-0002-fee-split.md) | Who pays the platform fee | Phase 1 | Proposed | Doer-only, 18%, at launch |
| [0003](ADR-0003-launch-city.md) | Launch city | Phase 1 | Proposed | Bangalore |
| [0004](ADR-0004-minimum-task-value.md) | Minimum task value | Phase 1 | Proposed | ₹199 floor, "from ₹100" reserved for repeat bundles |
| [0005](ADR-0005-backend-stack.md) | Backend language and framework | Phase 1 | Proposed | Node + TypeScript, Postgres, Retool for ops |
| [0006](ADR-0006-project-tier-pricing.md) | Bidding vs rate card for Project tier | Phase 2 | Proposed | Budget range + pitch, no price bidding, in v1 |
| [0007](ADR-0007-physical-errands.md) | Location-bound errands in MVP | Phase 1 | Proposed | One physical sub-category only, Tier 2 gated |

## The four Phase 1 blockers

ADRs 0002, 0003, 0004 and 0005 must be `Accepted` before Sprint 1 starts. ADR-0001 must be
`Accepted` before Sprint 7 but needs a payments lawyer engaged by Sprint 3, because lead time on
a PA onboarding or an escrow agreement is measured in weeks, not days.

## An unresolved gap in the PRD

The PRD's unit economics (section 11) omit **GST and TDS under section 194-O**. Both change the
per-task net materially and one of them depends on ADR-0001: if the platform is merchant of
record, GST may apply to the full task value rather than to the commission alone. A ₹21 net on a
₹150 task has no room to absorb that. Treat every figure in section 11 as pre-tax until a
chartered accountant has reviewed ADR-0001. This is tracked as `TAX-1` in
[../compliance/README.md](../compliance/README.md).

## Template

```markdown
# ADR-NNNN: <decision>

- **Status:** Proposed | Accepted (YYYY-MM-DD) | Superseded by ADR-NNNN
- **Blocks:** <phase or sprint>
- **Decider:** <name>

## Context
## Options
## Recommendation
## Consequences
## What would change this
```
