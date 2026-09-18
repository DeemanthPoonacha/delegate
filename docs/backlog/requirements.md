# Requirements and traceability

FR-1 to FR-28 from PRD section 5, with the sprint each one lands in and anything a decision has
changed since the PRD was written. **Priority is the PRD's; the Sprint and Notes columns are
this repo's.** P0 is required for launch, P1 is the next release.

| ID | Requirement | Priority | Stories | Sprint | Notes |
| --- | --- | --- | --- | --- | --- |
| FR-1 | Signup and login by phone OTP; email optional | P0 | 1 | S1 |  |
| FR-2 | Single account holds both roles; role toggle switches the home screen | P0 | 1, 7 | S1 |  |
| FR-3 | Profile: name, photo, bio, categories, hourly floor, languages spoken | P0 | 10, 26 | S1 |  |
| FR-4 | Doer video KYC against a government ID before first payout; verified badge on pass | P0 | 27 | S2 | Not Aadhaar — DigiLocker + PAN + penny-drop (KYC-1) |
| FR-5 | Post a task with title, description, category, tier, price or budget range, deadline, up to 5 attachments | P0 | 1 | S3 | Rejects Quick posts below the ADR-0004 floor |
| FR-6 | Two tiers: Quick (fixed price, requester-set, under 3 h) and Project (bidding, over 3 h) | P0 | 2, 3 | S3 | Project tier is budget-range + pitch, not price bidding (ADR-0006) |
| FR-7 | Suggested price range from median of last 50 completed tasks in the same category and tier | P1 | 31 | post-MVP | P0 for Project tier under ADR-0006; P1 for Quick |
| FR-8 | Prohibited-content check on publish: licensed-professional work, credential requests, impersonation, illegal acts | P0 | 30 | S3 |  |
| FR-9 | Doer feed sorted by match score; filters for category, tier, price floor, deadline | P0 | 7, 8 | S4 |  |
| FR-10 | Push notification to matching doers within 10 s of publish, capped at 20 doers per task | P0 | 11 | S4 |  |
| FR-11 | Apply (Quick) or bid with price and pitch (Project); one active application per doer per task | P0 | 2, 3 | S5 | Application carries a pitch, not an arbitrary price (ADR-0006) |
| FR-12 | Requester views applicants with rating, completed count, category history; accepts one | P0 | 26 | S5 |  |
| FR-13 | Escrow debit on acceptance via payment gateway; task cannot start until funds are held | P0 | 4 | S7 | Depends on ADR-0001; nothing to build until it is Accepted |
| FR-14 | 1:1 chat per task with text, images and documents; read receipts; chat locked after closure | P0 | 13, 14 | S6 |  |
| FR-15 | Category-specific deliverable templates with required fields (e.g. travel: 3 options, price, cancellation terms) | P0 | 14 | S6 |  |
| FR-16 | Deliverable submission moves task to Review; requester has 48 h to approve, request one revision, or dispute | P0 | 4, 14 | S6 |  |
| FR-17 | Auto-approval and release if the requester does not act within 48 h of submission | P0 | 9 | S6 |  |
| FR-18 | Payout to doer bank account or UPI within 24 h of release, platform fee deducted | P0 | 9 | S8 | Deducts platform fee, Karnataka levy (COMP-3) and TDS (TAX-2) in one place |
| FR-19 | Two-way rating (1–5) plus optional review, published only after both sides rate or 7 days pass | P0 | 26 | S8 |  |
| FR-20 | Dispute flow: escrow frozen, both sides submit statements, ops decision within 48 h, full or partial refund | P0 | 28 | S9 |  |
| FR-21 | Cancellation: free before acceptance; after acceptance, requester forfeits 10% to the doer | P0 | 4 | S5 |  |
| FR-22 | Re-post a completed task as a new one, pre-filled | P1 | 5 | post-MVP |  |
| FR-23 | Direct-invite a previous doer, bypassing the open feed | P1 | 6, 25 | post-MVP |  |
| FR-24 | Credential vault: requester stores details, grants per-task time-limited access, auto-revokes on closure | P1 | 29 | post-MVP |  |
| FR-25 | Specialisation badge after 10 completed tasks at ≥4.5 average in one category | P1 | 12 | post-MVP |  |
| FR-26 | Recurring booking: same doer, fixed weekly hours, auto-created weekly tasks | P1 | 25 | post-MVP |  |
| FR-27 | Ops console: dispute queue, task and chat inspection, escrow actions, account suspension, payout freeze | P0 | 33, 34 | S9 | Retool under ADR-0005; two extra sprints if built in React |
| FR-28 | Task browse gallery of example tasks with typical prices, for requester education | P1 | 32 | post-MVP |  |

## Counts

- P0: 20 requirements, all inside sprints S1–S9.
- P1: 8 requirements, none of which block the public launch.

## Where a decision has moved a requirement

| FR | Change | ADR |
| --- | --- | --- |
| FR-6, FR-11 | Project tier competes on pitch and history, not on price | [ADR-0006](../decisions/ADR-0006-project-tier-pricing.md) |
| FR-7 | Promoted to P0 for the Project tier, because a bad budget range now means zero applicants | [ADR-0006](../decisions/ADR-0006-project-tier-pricing.md) |
| FR-5 | Enforces a ₹199 floor except on re-posts to a previous doer | [ADR-0004](../decisions/ADR-0004-minimum-task-value.md) |
| FR-8 (doer feed) | Feed shows net earnings, not gross price | [ADR-0002](../decisions/ADR-0002-fee-split.md) |
| FR-13 | Blocked until the payment architecture is Accepted | [ADR-0001](../decisions/ADR-0001-payment-architecture.md) |
| FR-4 | Video KYC means DigiLocker + PAN + penny-drop, not Aadhaar | PRD, KYC-1 |

## Non-functional requirements

NFR-1 to NFR-15 live in PRD section 6 and are not restated here. Three of them are
build-order constraints rather than targets, and belong in Sprint 1's definition of done:

- **NFR-10** — customer funds never in a platform-owned operating account.
- **NFR-11** — AES-256 at rest for KYC documents and vault entries.
- **NFR-12** — immutable audit log from the first escrow transition, not retrofitted.
