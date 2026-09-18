# Phase 0 synthesis

Write this in week 3, from the notes and the two CSVs. It is the document Phase 1 is scoped from.
Fill every section; "not enough data" is a legitimate answer and more useful than a guess.

**Status:** _not started_ · **Written:** _(date)_ · **Author:** _(name)_

---

## 1. The verdict in three sentences

_Did people pay? Did doers deliver? Should Phase 1 start?_

## 2. Exit criteria

| Criterion | Target | Actual | Met? |
| --- | --- | --- | --- |
| People who paid real money | 10 | | |
| Tasks fulfilled end to end | 20 | | |
| Requester interviews | 30 | | |
| Doer interviews | 30 | | |
| Top 5 categories identified | yes | | |
| Blocking ADRs accepted | 4 | | |

## 3. Assumptions

Copy the verdict for each from [assumptions.md](../assumptions.md) with one line of evidence.

| ID | Assumption | Verdict | Evidence |
| --- | --- | --- | --- |
| A1 | Will pay ₹100–500 for delegable tasks | | |
| A2 | A stranger's shortlist is trusted enough to act on | | |
| A3 | Doers work at ₹150–300/hr | | |
| A4 | Errand requesters convert to project requesters | | |
| A5 | ₹199 is not a barrier | | |
| A6 | Doers accept an 18% cut | | |
| A7 | The PRD's 8 categories are right | | |

## 4. Demand: what people actually asked for

Categorise the 20 concierge tasks **after** the fact, from the requester's own words.

| Rank | Category | Tasks | Median price paid | Median fulfilment time | Repeat requests |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

- Categories from the PRD that **did not** appear: _(these should be cut from the launch 8)_
- Categories nobody predicted: _(these are the phase's most valuable finding)_

## 5. Supply: who actually delivered

| | Count |
| --- | --- |
| Doers interviewed | |
| Doers who accepted at least one task | |
| Doers who completed more than one | |
| Doers who dropped out mid-task | |
| Median effective hourly rate paid | |
| Objections to the 18% fee | |

## 6. What broke

Every task that went wrong, one line each: what happened, what it cost, and which FR would have
prevented it. This list is the real test-case backlog for Sprint 6 and Sprint 9.

## 7. Deliverable templates

For each of the top 5 categories: what did a *good* deliverable actually contain? This is the
direct input to FR-15 and the reason Sprint 6 cannot start before Phase 0 ends.

| Category | Required fields in a good deliverable | Verifiable artefact |
| --- | --- | --- |
| | | |

## 8. Unit economics, actual

Replace the illustrative figures in PRD section 11 with what the 20 tasks actually cost.

| | PRD assumption | Phase 0 actual |
| --- | --- | --- |
| Median task price | ₹500 | |
| Operator minutes per task (matching + support) | ~0 | |
| Tasks needing a support touch | few | |
| Disputes or refunds | under 5% | |
| Effective net per task | ₹73 | |

If operator time per task is above about 15 minutes, the auto-approval and template design in
FR-15/FR-17 is carrying more weight than the PRD assumed, and Sprint 6 needs more room.

## 9. What changes in the plan

| Change | Affects | Owner |
| --- | --- | --- |
| | | |

## 10. Recommendation

One of three, stated plainly:

- **Proceed to Phase 1** as scoped.
- **Proceed, narrowed** — fewer categories, different price floor, different city. Say exactly what.
- **Do not proceed.** What would have to change to revisit it.
