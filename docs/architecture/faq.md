# Architecture FAQ

Questions a new engineer, an investor's technical advisor or the founder is likely to ask, with
short answers and a link to the full reasoning. If a question here is answered differently in a
linked document, the linked document wins.

## Shape of the system

**Why not microservices?**
Two engineers, about 100 requests a second at peak, and money that moves along six paths where
task state and money state must change together. Microservices would turn each of those into a
cross-network saga, to solve a scaling problem we do not have. One codebase with strict module
boundaries keeps money changes in one database transaction.
[ADR-0003](adr/0003-modular-monolith.md)

**Isn't a monolith going to become a tangle?**
It will unless the boundaries are enforced. Each module owns its own database schema, exposes one
public file, and a lint rule in CI fails the build on imports that cross a boundary or point up the
dependency map. [04-modules.md](04-modules.md)

**Can we split out a service later?**
Yes, one module at a time, through the interface it already has. Chat is the most likely first
candidate. [ADR-0003](adr/0003-modular-monolith.md), "What would change this"

**Why three processes if it is one codebase?**
The API serves requests; the realtime process holds chat connections so an API deploy does not drop
them; the worker runs timers, payouts and provider calls so they never slow a request. Same image,
three start commands. [03-containers.md](03-containers.md)

**Why no Kafka, RabbitMQ or Redis?**
A separate broker cannot commit together with the database, which risks losing an event or sending
one for a change that rolled back. PostgreSQL holds the job queue in the same transaction as the
change, and we need about three events a second. The feed needs no cache: it scans about 1,500 open
tasks. [ADR-0004](adr/0004-postgres-for-data-jobs-and-events.md),
[05c](05c-matching-and-feed.md)

**Why no Elasticsearch for the feed?**
Same reason: a filtered, scored query over about 1,500 open tasks takes milliseconds in PostgreSQL.
Revisit at about 50,000 open tasks or when free-text search becomes a feature.
[05c](05c-matching-and-feed.md)

**Why AWS and not Kubernetes?**
Managed containers (ECS on Fargate) in Mumbai: no servers or cluster to run, the AWS credits apply,
and data stays in India. Kubernetes pays off with many services and many teams.
[ADR-0007](adr/0007-hosting-on-managed-containers.md)

## Money

**Do we store card or UPI details?**
No. The payment gateway handles them; our servers never see them.
[ADR-0001](adr/0001-use-a-payment-gateway.md)

**How do we make sure nobody is paid twice?**
Every step may run more than once, and every step is idempotent: idempotency keys from the app, the
gateway's event IDs in a webhook inbox, a unique key on every ledger posting, and a status check
before retrying any timed-out payout. [05b §2](05b-money.md)

**Why a double-entry ledger instead of amount columns?**
Columns store the current answer and lose the history that produced it. Transfers between accounts
are append-only, always sum to zero, and let us prove where every paisa went, for years.
[05b §1](05b-money.md)

**How do we know our records match reality?**
A daily reconciliation against the gateway's settlement report. Any unexplained difference older
than a day pauses payouts. [05b §3](05b-money.md)

**Is holding money between payment and approval legal?**
Not yet confirmed. It is risk R1, waiting on a payments lawyer. The design contains it: whatever the
answer, only the inside of the payments module changes.
[01 §6](01-requirements-and-drivers.md), [05b](05b-money.md)

**Can we change fees without a deploy?**
Yes. Fee rules are versioned data, and each task keeps a snapshot of the rules it was accepted
under. [05b §4](05b-money.md)

## Tasks and matching

**Why is the task lifecycle a state machine?**
So that impossible states are impossible: every transition is listed with its trigger, guard and
effects, and anything not listed cannot happen. [05a](05a-task-lifecycle.md)

**What happens if the requester never responds after the doer submits?**
After 48 hours a sweep auto-approves and pays the doer. A dispute received before the deadline
always wins over the sweep. [05a](05a-task-lifecycle.md), "Races"

**Why doesn't everyone get notified about every task?**
Notifications are capped in waves of 20 (70% best matches, 20% new doers, 10% random) so doers do
not learn to ignore them, and so the same top doers do not get everything.
[05c §2](05c-matching-and-feed.md)

**How does a new doer get their first task?**
Reserved notification slots, a "New on Delegate" label, a rating that starts at the platform
average, starter tasks, and hand-matching in the beta. [05c](05c-matching-and-feed.md), "Cold start"

## Chat, data and trust

**What happens to a chat message if the network drops?**
It waits in the phone's outbox and is resent with the same ID; the server stores it once. The
database is the truth and the socket is only a doorbell. [05d](05d-realtime.md)

**Can users share OTPs or phone numbers in chat?**
OTPs, PINs, passwords and card numbers are blocked everywhere; phone numbers are blocked before a
doer is hired. The filter stops accidents and casual attempts, not a determined user.
[05d](05d-realtime.md), "The content filter"

**Where do Aadhaar copies and ID documents go?**
Ideally they stay with the ID verification provider and we keep only the result. Full Aadhaar and
bank account numbers are never stored. [05e §2](05e-sensitive-data.md)

**Can a doer keep a requester's documents after the task?**
Their access ends when the task closes; download links are checked on every request and last
minutes. They could still save a copy while hired, which is why sensitive categories need a higher
trust tier. [05e](05e-sensitive-data.md), [05f](05f-trust.md)

**Why must doers verify before applying, not before their first payout?**
An unverified doer who gets chosen would leave the task stuck waiting, and would see the
requester's documents. Signup still takes under 2 minutes; verification happens at the first
"Apply". [05f §1](05f-trust.md)

**What if someone steals a doer's phone number?**
Changing the payout account needs a name match with the verified identity, a selfie check, and a
48-hour cooling-off with alerts to every registered device. [05f §3](05f-trust.md)

## Running it

**What happens if the database fails?**
A standby in another zone takes over in a minute or two. For data corrupted by a bug, we restore to
a point in time and run reconciliation to recover any money movements.
[06 §3](06-operations.md)

**How much will it cost?**
Roughly $380–640 a month on AWS at the month-12 load, inside the ₹50,000 budget; less before then,
and the credits cover most of year one. SMS, authentication and verification fees may cost more than
the servers. [06 §5](06-operations.md)

**Who gets woken up at night?**
The engineer on call, alternating weekly, and only for problems a person must fix now. Everything
else becomes a ticket. [06 §2](06-operations.md)
