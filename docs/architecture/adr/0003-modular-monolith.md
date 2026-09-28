# ADR-0003: A modular monolith, run as separate processes from one codebase

- **Status:** Accepted (2026-09-28)
- **Drivers:** financial correctness (attribute 1), security (attribute 2), simplicity and time to
  market (attribute 3), operability (attribute 5); capacity finding "scale is not a driver";
  constraints "two engineers", "nobody does DevOps", "₹50,000 a month"; ASR-1, ASR-2, ASR-4

## Context

Delegate's parts do very different things: identity, tasks, chat, disputes, payments. That
difference argues for firm boundaries between them. The question is whether those boundaries
should be **logical** (modules in one codebase, one database) or **physical** (separate services,
each with its own database, talking over the network).

Three findings from [01-requirements-and-drivers.md](../01-requirements-and-drivers.md) weigh on
the answer:

- The load is small: about 100 requests a second at peak and 110 GB of data a year. One server
  and one database handle it even at 10×.
- The team is two engineers, and nobody does DevOps.
- Money moves along six paths (ASR-1), and each one changes task state and money state together.
  The founder called a money error fatal.

Two parts of the system do behave differently at runtime. Chat holds thousands of long-lived
connections (ASR-4), and timed work such as auto-approval, payouts and deletions must run without
a user request (ASR-2).

## Options

**A. Microservices.** Six services (authentication, users, tasks, chat, disputes, payments), each
with its own database.

**B. A modular monolith as a single process.** One codebase, one database, one deployable that
serves requests, chat connections and background work.

**C. A modular monolith as several processes.** One codebase and one database, as in B, but
started in three roles: an **API** process for requests, a **realtime** process for chat and live
updates, and a **worker** process for scheduled and background jobs.

| Driver | A. Microservices | B. Single process | C. Several processes |
| --- | --- | --- | --- |
| 1. Financial correctness | Every money path crosses services and needs a saga with compensating steps | One database transaction per change | One database transaction per change |
| 2. Security | Six network surfaces; authentication repeated between services | One perimeter | One perimeter |
| 3. Simplicity | Six pipelines, six databases, service discovery, distributed tracing | One of everything | One codebase and pipeline; three start commands |
| 4. Timeliness | Neutral | A deploy drops every chat connection; heavy jobs can slow requests | Chat and jobs isolated from API deploys and load |
| 5. Operability | A task's full history needs data from five databases | One query | One query |
| Cost | Highest | Lowest | Close to lowest |

### The deciding scenario

A requester accepts a doer and pays.

- **In B and C,** marking the application accepted, moving the task to Matched and recording the
  pending payment happen in **one database transaction**: all of it or none of it.
- **In A,** the task service asks the payment service to charge, and the call times out. The task
  service cannot tell whether the charge happened. Retrying risks charging twice; not retrying
  risks a paid task still shown as Open. Closing that gap needs a saga, idempotency keys, an
  outbox and retries, for **each of the six money paths**.

Option A spends most effort exactly where attribute 1 says mistakes are least affordable, to
solve a scaling problem the capacity estimate shows we do not have. Its structural weak point is
also visible in the draft split: the task service depended on every other service, which is a
**distributed monolith**, with the coupling of a monolith plus the failure modes of a network.

## Decision

**Option C.** Delegate is one codebase and one PostgreSQL-compatible relational database, divided
into modules with strict boundaries, and run as three processes:

| Process | Runs | Why it is separate |
| --- | --- | --- |
| **API** | Requests from the mobile app and the ops console | The ordinary request path |
| **Realtime** | Chat and live updates over persistent connections | Deploying the API must not drop every conversation |
| **Worker** | Timers, payouts, webhook processing, deletions, notifications | Timed work runs without a request, survives restarts, and never slows the API |

All three can run on the same machine at launch. They are separate processes so that they can be
restarted, deployed and scaled separately, not because they need separate hardware yet.

Module boundaries are defined in step 4. The first draft is identity, tasks, matching, chat,
disputes, payments and notifications.

## Consequences

**Good**
- Any change to tasks and money together is one transaction. Most of attribute 1's risks become
  ordinary database guarantees.
- One deploy pipeline, one database to back up, one place to look when something breaks.
- The ops console reads a task's whole history with one query.
- It fits the budget with room to spare.

**Costs and obligations**
- **Boundaries are enforced by discipline, not by the network.** Nothing stops one module from
  reading another's tables except rules we set and check. From the first commit:
  - each module owns its tables, in its own database schema;
  - modules call each other only through a published interface, never by importing internals;
  - a lint rule on imports enforces this in CI.
  Without these rules the codebase decays into a tangle that can never be split.
- **The database is a single point of failure.** Accepted in section 2 of the drivers document
  (99.5% availability). It is mitigated with a managed database, automated backups and a standby
  replica.
- **Every deploy ships every module.** A bug in chat can block a payments fix. Mitigated by a
  fast pipeline and a test suite focused on money and state changes.
- **The realtime process needs a way to hear about events** from the API and worker processes,
  such as "new message saved" or "task taken". The mechanism is chosen in step 3.

## What would change this

- **A module with a genuinely different scaling or reliability need**, such as chat outgrowing
  one realtime process. Extract that module alone, through its existing interface.
- **The engineering team growing past about three independent teams** that block each other's
  deploys. That is the organisational trigger for services.
- **A regulatory requirement to isolate money handling** in its own system, for example as a
  condition of the payment structure the lawyer approves under risk R1.

In each case the path is to **extract one module**, not to redesign the system. Clean module
boundaries are what make that possible.
