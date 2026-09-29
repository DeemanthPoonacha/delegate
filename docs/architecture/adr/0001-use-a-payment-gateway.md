# ADR-0001: Use an established payment gateway instead of building payment handling

- **Status:** Accepted (2026-09-28)
- **Drivers:** financial correctness (attribute 1), security (attribute 2), simplicity and time to
  market (attribute 3); constraint "nobody has built payments"; risks R1, R4

## Context

Delegate collects money from requesters, holds it while work is done, and pays doers or refunds
requesters along six different paths (ASR-1). Getting any of this wrong is the one failure the
founder called fatal. Nobody on the team has built payments, the team is two engineers, and a
demo is due at month 3.

Handling payments directly means holding card and UPI data, connecting to banks and card
networks, and meeting the security and regulatory obligations that come with both.

## Options

| | A. Build payment handling ourselves | B. Use an established Indian payment gateway |
| --- | --- | --- |
| Security | We store and protect payment data ourselves, and carry the full compliance burden | Card and UPI details never reach our servers; the gateway carries that burden |
| Correctness | Every edge case (timeouts, duplicate callbacks, partial failures) is ours to discover | Mature, well-tested flows; we still handle their notifications correctly |
| Time to build | Months, plus regulatory approvals | Days to a first sandbox payment |
| Cost | No per-transaction fee, but large fixed engineering and compliance cost | A per-transaction fee, typically around 2% |
| Team fit | Needs skills nobody has | Needs only API integration skills the team has |

Option A is not realistic for a startup: moving other people's money directly requires regulatory
authorisation that takes far longer than six months. It is recorded so nobody reopens it casually.

## Decision

**Option B.** Payment collection, and payouts where the provider offers them, go through an
established, regulated Indian payment gateway.

The fee is a deliberate investment. It buys security and correctness we could not build to the
same standard in time, and it moves the cost of *learning* payments (months of engineering, and
real money lost to mistakes along the way) onto a provider who has already paid it.

The choice of *which* gateway is a separate decision, made in step 5 against these criteria:
UPI support, payouts to bank accounts and UPI, support for holding and releasing funds (see
Consequences), reliable webhooks with retries, a complete sandbox, reconciliation reports, and
fees on a ₹100 transaction.

## Consequences

**Good**
- Card and UPI details never touch our systems, which keeps most payment-security obligations
  with the gateway.
- The first real payment can happen within the demo timeline.
- The team spends its time on the marketplace, not on banking.

**Costs and obligations**
- **About 2% of every transaction.** On a ₹100 task that is about ₹2 out of a ₹15–18 fee. It
  must be included in the unit economics.
- **The gateway becomes the source of truth for whether money moved.** Our records describe what
  we *believe* happened; the gateway's records say what *did*. We need a reconciliation job that
  compares the two and alerts on any difference (attribute 1).
- **Payments become asynchronous.** The gateway tells us about payments through webhooks, which
  can arrive late, twice or out of order. Every handler must be idempotent: processing the same
  notification twice must have the same effect as processing it once.
- **The gateway can be down.** When it is, money actions pause and the app says so, rather than
  guessing (fail closed, section 2 of the drivers document).
- **Vendor lock-in.** All gateway calls go through one payments module with our own interface, so
  switching providers, or adding an escrow provider, changes one module (risk R1's containment).

**What this does not decide.** A gateway moves money. It does not answer **who legally holds the
money** between the requester paying and the doer being paid. That is risk R1 and remains open
until a payments lawyer has answered it. The gateway chosen in step 5 must fit whatever structure
the lawyer approves.

## What would change this

- Transaction volume reaching the point where fees exceed the cost of a dedicated payments team,
  far beyond the 10× horizon of this design.
- No available gateway supporting the money-holding structure the lawyer requires. That would
  mean adding a second provider (for example an escrow provider), not building our own.
