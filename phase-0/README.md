# Phase 0 — Validate

**Three weeks: Mon 21 Sep – Fri 9 Oct 2026. No code is written in this phase.**

Phase 0 exists because no primary research exists yet. Every persona, price point and conversion
assumption in the PRD is a hypothesis, and the unit economics are illustrative. The cheapest way
to find out whether this product should be built is to run it by hand, over WhatsApp, for twenty
real tasks.

## Exit criteria

From PRD section 10. Phase 1 does not start until all four are true:

1. **10 people pay real money** for a task fulfilled manually. Not "would pay" — paid.
2. **Top 5 categories identified** from actual demand, not from the PRD's list of 8.
3. Every assumption in [assumptions.md](assumptions.md) is marked supported, refuted or untested.
4. The four blocking ADRs (0002, 0003, 0004, 0005) are `Accepted`.

## Three weeks

| Week | Dates | Focus | Done when |
| --- | --- | --- | --- |
| 1 | 21–25 Sep | Recruiting and requester interviews | 15 requester interviews done; 40 doer applicants screened |
| 2 | 28 Sep – 2 Oct | Doer interviews and the concierge run opens | 30 doer interviews done; 8 tasks fulfilled and paid |
| 3 | 5–9 Oct | Concierge run and synthesis | 20 tasks total; synthesis written; ADRs decided |

Target is 30 requester and 30 doer interviews. Thirty is the PRD's number; the real signal usually
arrives around 12–15 per side, so if week 1 is unanimous, spend the surplus time on more concierge
tasks instead. Tasks that people paid for beat interviews they sat through.

## Daily cadence

- **Morning, 30 min.** Read yesterday's task log. Anything that went wrong becomes an interview
  question today.
- **During the day.** Interviews on a schedule; concierge tasks fulfilled as they arrive.
- **Evening, 20 min.** One row per interview in `research/participants.csv`, one row per task in
  `concierge/task-log.csv`, notes filed in `research/interviews/`. Do it the same day — recall
  degrades overnight and this is the entire output of the phase.

## Who does what

| Role | Phase 0 job |
| --- | --- |
| Founder | Recruiting, requester interviews, category strategy, ADR decisions |
| Operator | Concierge fulfilment — this person *is* the product for three weeks |
| Engineer(s) | **Not on this phase.** If they are idle, they are reading the compliance tracker and scoping S1, not writing code. |

## The files

| File | Use |
| --- | --- |
| [assumptions.md](assumptions.md) | The ledger. Update it as evidence arrives; it is the phase's real output. |
| [research/screener.md](research/screener.md) | Five questions to decide whether someone is worth an hour |
| [research/interview-requester.md](research/interview-requester.md) | 45-minute demand-side script |
| [research/interview-doer.md](research/interview-doer.md) | 40-minute supply-side script |
| [research/synthesis.md](research/synthesis.md) | The template the phase's conclusions go into |
| [concierge/runbook.md](concierge/runbook.md) | How to actually run 20 tasks by hand |
| [concierge/whatsapp-scripts.md](concierge/whatsapp-scripts.md) | Message templates, so fulfilment is consistent |
| [concierge/pricing-card.md](concierge/pricing-card.md) | What to charge, and what it costs us |

## Data handling

Real names, phone numbers and payment references are **gitignored** and stay out of the repo's
history. `participants.csv` and `task-log.csv` are local files; only their `.example.csv`
templates are tracked. Tell every participant what you are recording and delete recordings after
synthesis — DPDP's Board is live and accepting complaints now, even though full compliance is due
May 2027 (see [DPDP-2, DPDP-5](../docs/compliance/README.md)).
