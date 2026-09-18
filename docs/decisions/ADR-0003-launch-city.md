# ADR-0003: Launch city

- **Status:** Proposed
- **Blocks:** Phase 1 (compliance setup), Phase 0 (where interviews happen)
- **Decider:** Founder

## Context

Bangalore has the density of both personas — 55-hour-week IT managers and students with free
afternoons — and it is where Dunzo proved the errand habit exists. It also has a live gig-worker
levy from day one: minimum 1% of every payout, capped at ₹1.50 per transaction for professional
services, Welfare Board registration inside 45 days, a machine-readable worker database, quarterly
remittance and mapping to the state PWFVS system
([Karma Management](https://karmamgmt.com/index.php/blog/karnataka-gig-workers-welfare-fee-2026-compliance-guide),
[United Consultancy](https://unitedconsultancy.com/gig-workers-welfare-fee-karnataka-government-order-13-02-2026/)).
The Act is under constitutional challenge and the High Court declined to stay it in July 2026
([Medianama](https://www.medianama.com/2026/07/223-karnataka-hc-gig-workers-act-welfare-fee/)).

## Options

- **A. Bangalore.** Best density, live levy, most competition for supply.
- **B. Hyderabad or Pune.** No gig-worker Act in force, good graduate supply, thinner concentration
  of the high-income requester persona.
- **C. A tier-2 city (Indore, Coimbatore).** Cheapest supply, lowest willingness to pay, and the
  requester persona barely exists at ₹500 a task.

## Recommendation

**Bangalore.** The levy is ₹1.28 on a ₹150 task and ₹1.50 on a ₹25,000 one — materially irrelevant
per task. The real cost is fixed compliance overhead (registration, worker database, quarterly
filing) and it lands on the operator, not the engineers. Trading away the only city where both
sides of the marketplace are dense, to avoid roughly one operator-day a quarter, is a bad trade.

Marketplaces die of cold start, not of levies.

## Consequences

- Welfare Board registration due within 45 days of the first payout — tracked as COMP-3.
- The payout module carries PWFVS-compatible reporting from Sprint 8, not as a later retrofit.
- A second city inherits a different Act or none; keep the levy configurable per state from the
  start rather than hard-coding 1%.

## What would change this

The constitutional challenge succeeding, which would remove the levy entirely and make this moot.
Or Phase 0 finding that Bangalore doers already have better-paid gig options and will not take
₹150–300 an hour work.
