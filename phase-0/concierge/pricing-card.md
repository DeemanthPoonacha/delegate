# Concierge pricing card

Prices for the Phase 0 run. These are hypotheses being tested, not a rate card — the whole point
is to find out which ones people accept.

| Task | Price to requester | Paid to doer (82%) | Expected time | Tests |
| --- | --- | --- | --- | --- |
| Insurance claim logged, claim number returned | ₹150 | ₹123 | 40 min | A5, A6 |
| Doctor's appointment booked, earliest slot within 5 km | ₹150 | ₹123 | 30 min | A5 |
| School or admission form filled from saved details | ₹199 | ₹163 | 45 min | A1 |
| Lowest landed price across 4 sites, bank offers included | ₹250 | ₹205 | 1 h | A2 |
| Refund fought through a support chat to resolution | ₹299 | ₹245 | 1–2 h | A1 |
| Hotel shortlist: 3 options, prices, cancellation terms, links | ₹499 | ₹409 | 1.5 h | A2 |
| 15 flat listings called, 5 genuine owner contacts returned | ₹499 | ₹409 | 2 h | A2 |
| Government office queue, document collected | ₹399 + travel | ₹327 + travel | 3 h | ADR-0007 |
| CV and LinkedIn rewrite by someone in the field | ₹1,500 | ₹1,230 | 2 days | A4 |
| Competitor pricing table, dated, with sources | ₹2,000 | ₹1,640 | 1–2 days | A4 |

## What each one actually costs us

At an 18% doer-side fee ([ADR-0002](../../docs/decisions/ADR-0002-fee-split.md)) and roughly 2%
of gateway cost once payments are real:

| Price | Fee | Gateway | Welfare levy | Net |
| --- | --- | --- | --- | --- |
| ₹150 | ₹27 | ₹3 | ₹1.28 | ~₹23 |
| ₹499 | ₹90 | ₹10 | ₹1.50 | ~₹78 |
| ₹2,000 | ₹360 | ₹40 | ₹1.50 | ~₹318 |

Before GST and TDS, both of which are unresolved ([TAX-1, TAX-2](../../docs/compliance/README.md)).
In Phase 0 there is no gateway and no levy — payment is direct UPI — so log the *gross* and
compute net afterwards rather than deducting anything from what the doer is actually paid.

Operator time is the cost this table hides. If a ₹150 task takes 30 minutes of operator attention,
it loses money at any fee. Track it in `task-log.csv` and settle it in the synthesis.
