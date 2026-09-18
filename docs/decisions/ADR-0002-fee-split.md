# ADR-0002: Who pays the platform fee

- **Status:** Proposed
- **Blocks:** Phase 1 (pricing copy, FR-5, FR-18)
- **Decider:** Founder

## Context

Section 11 of the PRD assumes 15% from the doer plus 2% from the requester. On a ₹150 task that
is ₹25 of platform revenue, ₹4 of gateway cost and ₹21 net — before the Karnataka levy and before
tax. The split also decides what number a first-time requester sees at checkout, which is the
moment the ₹100 brand promise either holds or breaks.

## Options

| Option | Requester sees | Doer receives on ₹500 | Risk |
| --- | --- | --- | --- |
| A. 15% doer + 2% requester | ₹510 on a ₹500 task | ₹425 | Two-line checkout; sticker shock at the low end |
| B. Doer-only, 18% | ₹500 flat | ₹410 | Doers feel the whole fee; leakage pressure |
| C. Requester-only, 18% | ₹590 | ₹500 | Kills the ₹100 promise outright |

## Recommendation

**Option B — doer-only at 18%.** The requester-facing price is the price, which is the single
clearest thing we can say in launch copy, and the marginal revenue versus Option A is small
(₹90 vs ₹85 on a ₹500 task). The cost is that doers carry the full fee, so the fee has to be
visible in the doer's feed **before** they apply, not after they deliver — otherwise it becomes
the reason they take the second task off-platform.

## Consequences

- Doer feed shows net earnings, not gross price (FR-8 acceptance criterion).
- FR-18 deducts fee, welfare levy and TDS in one place; the payout receipt itemises all three.
- Off-platform leakage becomes a doer-side problem, so FR-23 (direct-invite) matters more, not
  less — it has to be cheaper to stay than to leave.

## What would change this

Phase 0 finding that doers refuse work at an 18% effective cut. The concierge run records what
doers were actually paid and what they said about it; if three or more balk at 18%, move to
Option A and put the 2% on the requester as a "platform fee" line.
