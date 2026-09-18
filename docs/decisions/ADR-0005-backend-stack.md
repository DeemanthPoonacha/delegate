# ADR-0005: Backend language and framework

- **Status:** Proposed
- **Blocks:** Phase 1 (Sprint 1 cannot start without it)
- **Decider:** Founder + backend engineer

## Context

Two engineers, one on React Native and one full-stack on backend, payments and the ops console.
The PRD leaves the choice open between Node with TypeScript and Django, and commits to a modular
monolith either way — the right call at 2,000 tasks a day.

## Options

| | Node + TypeScript | Django + DRF |
| --- | --- | --- |
| Shared types with the RN app | Yes — one schema, one set of types | No |
| Ops console | Build it, or use Retool | Django admin, free, immediately |
| Escrow state machine | Explicit; needs discipline on transactions | Explicit; ORM transactions are mature |
| Hiring in Bangalore | Deep pool | Deep pool |
| Payments SDKs (Razorpay, Digio) | First-class | First-class |

## Recommendation

**Node + TypeScript** (Fastify or NestJS), PostgreSQL 16, Drizzle or Prisma, Redis for the
notification queue and feed cache. Ops console on Retool, as the PRD's stack table already
anticipates.

The deciding factor is that the PRD already plans Retool for the ops console, which removes
Django's single biggest advantage. What remains is one language across the mobile app and the
server for a two-person team — the same person will be writing both sides on some sprints, and
sharing the task state machine's types between them is worth more than a free admin panel we
already decided not to use.

## Consequences

- Task state machine, escrow transitions and the matching score are shared TypeScript modules
  with unit tests — the three places the PRD says money and trust break.
- Money in paise as `bigint`, never `number`. Add a lint rule for it in Sprint 1.
- Retool becomes a dependency for FR-27; if that is unacceptable, budget two sprints for a plain
  React admin instead and this ADR should be re-opened.

## What would change this

The backend engineer being materially faster in Python. A stack the team is slow in beats a stack
the ADR prefers; ability to ship wins this argument.
