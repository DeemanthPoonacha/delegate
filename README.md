# Delegate

A marketplace for delegating tasks — 20 minutes to 6 months, from ₹100, across every field.
One city, 8 categories, two task tiers, full escrow at MVP.

> Everyone deserves a personal assistant. People with money lack time; people with time want money.

**Status:** Phase 0 — Validate. No application code exists yet, and none should be written until
Phase 0 exits. The stack is deliberately undecided (see [ADR-0005](docs/decisions/ADR-0005-backend-stack.md)).

## Where things are

| Path | What it holds |
| --- | --- |
| [docs/prd.md](docs/prd.md) | The source PRD, exported from the Claude doc. Single source of truth for scope. |
| [docs/decisions/](docs/decisions/) | One ADR per open decision. Four of them block Phase 1. |
| [docs/compliance/](docs/compliance/) | Obligations tracker — RBI, DPDP, Karnataka welfare fee, tax. |
| [docs/backlog/](docs/backlog/) | FR-1…FR-28 with traceability, and the S1–S9 sprint plan. |
| [phase-0/](phase-0/) | The validation kit: interview scripts, concierge runbook, assumption ledger. |

## The plan in one table

| Phase | Weeks | Exit criteria |
| --- | --- | --- |
| 0. Validate | 1–3 | 10 people pay real money for a manually fulfilled task; top 5 categories identified |
| 1. Foundation | 4–7 | A doer can register, pass KYC and appear in a list |
| 2. Core loop | 8–13 | One end-to-end task completes on staging with no manual intervention |
| 3. Money and trust | 14–17 | 20 real tasks with real money; zero reconciliation errors |
| 4. Closed beta | 18–21 | 60% matched within 30 min; ≥4.2 rating; dispute rate under 10% |
| 5. Public launch | 22–26 | 300 tasks a week sustained for 3 weeks |

## Start here

1. Read [docs/prd.md](docs/prd.md) end to end — it is 12 sections and about 30 minutes.
2. Decide the four blockers in [docs/decisions/README.md](docs/decisions/README.md). Phase 1 cannot
   be scoped until payment architecture, fee split, launch city and minimum task value are settled.
3. Run [phase-0/README.md](phase-0/README.md). It is a three-week script with a daily cadence.

## Ground rules carried from the PRD

- Money never sits in a platform-owned operating account.
- A doer never needs the requester's password, OTP or UPI PIN. Sensitive flows are
  doer-prepares, requester-submits.
- Money is stored in paise as integers. Never floats.
- No category is added until the previous one holds a ≥4.3 average rating.
