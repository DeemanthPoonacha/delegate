# ADR-0004: Minimum task value

- **Status:** Proposed
- **Blocks:** Phase 1 (FR-5 validation), all launch copy
- **Decider:** Founder

## Context

"From ₹100" is the brand promise and the thing that distinguishes Delegate from Upwork. The PRD's
own arithmetic undercuts it: a ₹150 task nets ₹21, a single dispute on it destroys the margin on
twenty more, and break-even needs roughly 5,500 completed tasks a month.

## Options

| Floor | Net per task | What it costs |
| --- | --- | --- |
| A. ₹100 | ~₹13 | Brand promise intact; margin cannot carry one support touch |
| B. ₹199 | ~₹29 | Promise weakens; still clearly below every competitor |
| C. ₹299 | ~₹45 | Safe margin; no longer a micro-errand product |

## Recommendation

**₹199 floor for open posting, with "from ₹100" kept for repeat and bundled tasks.** A doer who
has already done this requester's insurance call three times can do the fourth at ₹100 because
there is no re-explaining, no matching cost and near-zero support risk. That makes the ₹100 price
a *reward for the repeat habit* — which is the north-star metric — instead of an acquisition
subsidy on the highest-risk, highest-support transaction we have.

## Consequences

- FR-5 rejects a Quick-tier post below ₹199 unless it is a re-post to a previous doer (FR-22, FR-23).
- Launch copy says "from ₹100 with your regular doer", not "tasks from ₹100".
- Phase 0's concierge run must include at least five tasks priced at ₹100–150 anyway, to learn
  whether the low end is what actually pulls people in.

## What would change this

Phase 0 showing that requesters will not try the product at ₹199 but will at ₹100. If the ₹100
price is genuinely what converts a first-timer, then it is a marketing cost and belongs in the
CAC line, not in the unit economics — and this ADR flips to Option A with a capped number of
subsidised first tasks per account.
