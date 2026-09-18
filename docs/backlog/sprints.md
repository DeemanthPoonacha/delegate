# Sprint plan

Six phases, about 26 weeks, two-week sprints, two engineers and one operator. Phases and exit
criteria are the PRD's (section 10); the dates and the "cannot start until" column are this repo's,
anchored to a Phase 0 start of **Mon 21 Sep 2026**.

## Phases

| Phase | Weeks | Dates | Deliverable | Exit criteria |
| --- | --- | --- | --- | --- |
| 0. Validate | 1–3 | 21 Sep – 9 Oct 2026 | 30+30 interviews; 20 tasks fulfilled manually over WhatsApp | 10 people pay real money; top 5 categories identified |
| 1. Foundation | 4–7 | 12 Oct – 6 Nov 2026 | Auth, profiles, KYC, taxonomy, ops skeleton, CI | A doer can register, pass KYC and appear in a list |
| 2. Core loop | 8–13 | 9 Nov – 18 Dec 2026 | Post → feed → apply → accept → chat → submit → approve, escrow in test mode | One end-to-end task completes on staging with no manual step |
| 3. Money and trust | 14–17 | 4 Jan – 29 Jan 2027 | Escrow live, payouts, ratings, disputes, audit log | 20 real tasks with real money; zero reconciliation errors |
| 4. Closed beta | 18–21 | 1 Feb – 26 Feb 2027 | 100 requesters, 50 doers, invite-only, top-5 templates | 60% matched in 30 min; ≥4.2 rating; disputes under 10% |
| 5. Public launch | 22–26 | 1 Mar – 2 Apr 2027 | Play Store, referrals, suggested pricing, support workflow | 300 tasks a week for 3 weeks |

Phase 3 assumes a break over the new year. If that is wrong, everything after it moves a week earlier.

## Sprints S1–S9

| Sprint | Phase | Focus | Key tickets | Cannot start until |
| --- | --- | --- | --- | --- |
| S1 | 1 | Auth and profiles | Phone OTP, user table, profile editor, role toggle | ADR-0005 accepted; CORP-4 (DLT) in progress |
| S2 | 1 | KYC and categories | KYC vendor integration, tier gating, category seed, ops console read-only | KYC-3 contract signed |
| S3 | 2 | Task posting | Post flow, validation, attachments, draft persistence, prohibited-content check | ADR-0004 accepted (the floor is a validation rule) |
| S4 | 2 | Feed and matching | Scored feed query, filters, push fan-out, FCM | S3 |
| S5 | 2 | Bidding and acceptance | Applications, applicant list, accept flow, task state machine | ADR-0006 accepted |
| S6 | 2 | Chat and delivery | WebSocket chat, attachments, deliverable templates, submit and approve | S5; top-5 templates from Phase 0 |
| S7 | 3 | Escrow | Gateway integration, fund on accept, release on approve, reconciliation job | **ADR-0001 accepted; PAY-4 onboarding complete** |
| S8 | 3 | Payouts and reputation | Payout scheduling, welfare-fee and TDS deduction, ratings, review publishing rule | S7; COMP-1 registration filed |
| S9 | 3 | Disputes and admin | Dispute flow, ops queue, suspension, payout freeze, audit log | S7 |

## The long-lead items

Three things take weeks of someone else's time and will stall a sprint if started late:

| Item | Lead time | Start by |
| --- | --- | --- |
| Payments lawyer engaged, ADR-0001 settled (PAY-1) | 3–4 weeks | Sprint 3 |
| Payment aggregator onboarding, merchant KYC (PAY-4) | 4–6 weeks | Sprint 4 |
| KYC vendor contract — Digio or Signzy (KYC-3) | 2–3 weeks | Before Sprint 2 |

## Test strategy

From PRD section 10, unchanged:

- Unit tests on the task state machine, escrow transitions and the matching score — the three
  places money and trust break.
- Integration tests against gateway and KYC sandboxes.
- A seeded end-to-end script covering the full loop, run on every deploy.
- Manual QA on two low-end Android devices before each release.
- Phase 4 beta doubles as UAT: every dispute becomes a written test case.

## Definition of done, from Sprint 1

- Money handled as integer paise. No floats, enforced by lint.
- Every task state transition writes an audit row (NFR-12).
- No KYC document or deliverable passes through the app server — pre-signed URLs only.
- Strings externalised for later Hindi and Kannada (NFR-14), even though launch is English.
