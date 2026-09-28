# ADR-0004: PostgreSQL as the database, the job queue and the event channel

- **Status:** Accepted (2026-09-28)
- **Drivers:** financial correctness (attribute 1), simplicity (attribute 3), timeliness
  (attribute 4); capacity finding "scale is not a driver"; constraint "the team knows Postgres";
  ASR-1, ASR-2, ASR-3; [ADR-0003](0003-modular-monolith.md)

## Context

ADR-0003 made Delegate one codebase with one database, run as API, realtime and worker processes.
Three questions follow:

1. **Which database?** The team knows both PostgreSQL and MongoDB.
2. **How does work leave the request?** Publishing a task must trigger notifications; approving
   work must trigger a payout. These reactions must never be lost, and must never happen for a
   change that was rolled back.
3. **How do the three processes signal each other?** The realtime process must hear that a
   message was saved or a task was taken.

Timed work (ASR-2) also needs a home: auto-approval after 48 hours, deadline lapses, payouts,
document deletion.

The load is small: about 250,000 writes a day, or three events a second.

## Options

**Database**

| | PostgreSQL | MongoDB |
| --- | --- | --- |
| Transactions across several records | Mature, the default | Supported, but not the model the database is designed around |
| Relationships (tasks, applications, money, disputes) | Native: joins and foreign keys | Modelled in application code |
| Flexible fields (category-specific deliverables) | JSONB columns | Native |
| Team knowledge | Yes | Yes |

**Jobs and events**

| | A. A separate broker (RabbitMQ, SQS, Kafka) | B. PostgreSQL itself |
| --- | --- | --- |
| Consistency with the state change | **Dual write**: the database and the broker cannot commit together, so an event can be lost or sent for a rolled-back change. Needs an outbox table and a relay to fix | The job is inserted **in the same transaction** as the change: both happen or neither does |
| New infrastructure | One more system to run, secure, monitor and pay for | None |
| Throughput | Thousands to millions a second | Thousands a second; we need three |
| Replay and many independent consumers | Strong (especially Kafka) | Not needed yet |

## Decision

**PostgreSQL, managed, is the single datastore for everything except files.** It holds:

- **All module data**, one schema per module (ADR-0003).
- **The job queue.** A Postgres-backed job library (such as `pg-boss` or `graphile-worker`)
  stores jobs in tables. Any change that needs follow-up work inserts its job **in the same
  transaction**. The worker process runs the jobs, with retries.
- **Signals between processes** through `LISTEN/NOTIFY`. A notification carries only an
  identifier ("task 42 changed"); the data stays in the tables. A missed signal costs a refetch,
  never data.
- **Deadlines as data.** Timed work is a column (`review_deadline`, `task_deadline`) plus a
  **sweep** that runs every minute: "find everything overdue and process it". A missed run is
  caught by the next one.

Three rules apply to all of it:

1. **The database state is the truth.** Jobs and signals announce changes; they never carry the
   only copy of anything.
2. **Every job is idempotent.** Running it twice has the same effect as running it once, because
   jobs *will* run twice: after a crash, a timeout or a retry.
3. **Incoming payment webhooks go into an inbox table first.** The API stores the raw event and
   replies at once; the worker processes it. A duplicate webhook is detected by its event ID.

## Consequences

**Good**
- A state change and its follow-up work cannot disagree: no dual write anywhere.
- Nothing new to operate. One backup covers data, jobs and history.
- Sweeps make timed work self-healing.

**Costs and obligations**
- **Job pickup latency.** Postgres queues poll or wait on `NOTIFY`; pickup takes up to about a
  second. That fits inside the 10-second budget for new-task notifications (attribute 4), but it
  must be measured, not assumed.
- **The queue shares the database's capacity.** Heavy job tables need cleaning of finished jobs
  and an eye on table bloat.
- **`LISTEN/NOTIFY` is not durable** and its payload is small. Used only as a wake-up signal; the
  realtime process refetches state after reconnecting.
- **MongoDB is not used.** Category-specific data goes in JSONB columns instead.

## What would change this

- Sustained event volume in the thousands a second, or job traffic measurably slowing ordinary
  queries.
- Several independent systems needing the same event stream, or needing to replay history.

Either would justify a broker, fed from an outbox table so that the consistency guarantee above
survives the change.
