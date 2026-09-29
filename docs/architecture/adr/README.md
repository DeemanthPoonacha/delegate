# Architecture decision records

One file per decision that would be expensive to reverse. Numbered independently of
`docs/decisions/`.

| ADR | Decision | Status |
| --- | --- | --- |
| [0001](0001-use-a-payment-gateway.md) | Use an established payment gateway instead of building payment handling | Accepted |
| [0002](0002-one-mobile-app-for-both-roles.md) | One mobile app for both roles, and a separate ops console | Accepted |
| [0003](0003-modular-monolith.md) | A modular monolith, run as separate processes from one codebase | Accepted |
| [0004](0004-postgres-for-data-jobs-and-events.md) | PostgreSQL as the database, the job queue and the event channel | Accepted |
| [0005](0005-object-storage-for-files.md) | Files in private object storage, uploaded and downloaded directly | Accepted |
| [0006](0006-managed-authentication.md) | A managed authentication provider for phone login (vendor open) | Accepted |
| [0007](0007-hosting-on-managed-containers.md) | Host on AWS in Mumbai, on managed containers, defined as code | Accepted |

## How to write one

An ADR records *why*, for the person who joins in a year and asks "why on earth did they do
this?". The decision itself is usually one line. The value is in the rest:

- **Context:** the forces at play, linked to the drivers in
  [01-requirements-and-drivers.md](../01-requirements-and-drivers.md). A decision that cites no
  driver is a preference.
- **Options:** at least two real ones. Recording what you rejected, and why, stops the same debate
  from happening again.
- **Consequences:** the bad ones as well as the good. Every decision has a cost; an ADR that lists
  none has not been thought through.
- **What would change this:** the evidence that should reopen it. This is what makes a decision
  safe to make early.

ADRs are never edited after acceptance except to change their status. A changed mind is a new ADR
that supersedes the old one.

## Template

```markdown
# ADR-NNNN: <decision, as a sentence>

- **Status:** Proposed | Accepted (YYYY-MM-DD) | Superseded by ADR-NNNN
- **Drivers:** <links to quality attributes, constraints, ASRs>

## Context
## Options
## Decision
## Consequences
## What would change this
```
