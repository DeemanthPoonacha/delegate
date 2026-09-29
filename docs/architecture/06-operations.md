# 06 · Operations

**Status:** Draft 1. Sources: [01-requirements-and-drivers.md](01-requirements-and-drivers.md)
(attributes, the 99.5% availability trade-off, the ₹50,000 budget),
[03-containers.md](03-containers.md), [ADR-0007](adr/0007-hosting-on-managed-containers.md).

> **How.** Operations design answers four questions: how is the system **deployed**, how do we
> **know it is working**, how do we **recover when it is not**, and **what does it cost**? For a
> two-engineer team with no operations experience, the governing rule is: **every piece of
> operations work you build must be something you will actually look at or use.** A dashboard
> nobody opens and an alert everyone ignores are worse than none, because they create false
> confidence. Build the ladder one rung at a time (section 6).

## 1. Deploy

### Environments

| Environment | Purpose | Built from | External providers |
| --- | --- | --- | --- |
| Local | Development | Docker Compose: PostgreSQL and an S3-compatible store | Sandboxes, or fakes in tests |
| Staging | The demo, and the last check before production | The same CDK code as production, smaller and in one zone | Sandboxes (gateway, ID provider, auth) |
| Production | Real users and real money | CDK | Live accounts |

### The pipeline

```text
push to a branch ─► checks ─► merge to main ─► build one image ─► deploy to staging
                                                                      │
                               seeded end-to-end script on staging ◄──┘
                                                                      │
                                         manual approval ─► deploy to production
```

**Checks on every push:** lint (including the module dependency rule from
[04](04-modules.md)), type check, unit tests (task state machine, ledger, fee rules, trust table),
integration tests against a real PostgreSQL in a container.

**The end-to-end script** runs the whole loop on staging: post, apply, accept, pay in the sandbox,
chat, submit, approve, pay out. If it fails, production is not offered.

### Database changes without downtime: expand, then contract

During a deploy, old and new versions of the code run at the same time for a minute or two. Every
schema change must therefore work with **both**:

1. **Expand**: add the new column or table. Old code ignores it.
2. **Deploy** code that writes both old and new, then reads new.
3. **Backfill** existing rows.
4. **Contract**: in a later deploy, remove the old column.

Renaming a column in one step breaks whichever version is still running. Migrations run as their
own step before the new code starts.

### Deploying the realtime process

On a deploy the realtime process stops accepting new connections, then closes existing ones over a
minute or so. Apps reconnect with jittered backoff and sync by sequence number
([05d](05d-realtime.md)). Nothing is lost, because nothing lived in the socket.

### Running several copies

| Process | Copies at launch | Note |
| --- | --- | --- |
| API | 2, in two zones | So a deploy or a zone failure never takes it fully down |
| Realtime | 1, then 2 | Each copy listens to the same `NOTIFY` channel |
| Worker | 1, then 2 | The job library hands each job to one worker; sweeps take a database lock so only one copy runs each sweep, and they are idempotent anyway |

## 2. Know it is working

### Logs

Structured JSON, redacted ([05e](05e-sensitive-data.md)), with a **correlation ID** that follows
work across processes: the API request that accepted a task, the job that created the hold, the
webhook that funded it. Following one money flow from start to end must be a single search.

### Metrics that matter

Generic server metrics (CPU, memory) rarely tell you users are hurting. These do:

| Area | Metric | Why |
| --- | --- | --- |
| API | Request rate, error rate, latency (p95) | The standard health signals |
| Jobs | **Age of the oldest waiting job** | The earliest sign that timers, payouts or notifications have stalled |
| Sweeps | Time since each sweep last completed | A stopped sweep means auto-approvals and deadlines silently stop |
| Money | Webhook inbox backlog; payouts in Unknown; reconciliation differences | Attribute 1 |
| Matching | Time from publish to first push sent (p95) | Attribute 4's 10-second target |
| Realtime | Connected sockets; message delivery time (p95) | Attribute 4's 1-second target |
| Ops | Oldest open dispute | The 48-hour promise |

### Service level objectives

Targets taken straight from the quality attributes. Each one is measured, not assumed.

| Objective | Target | Error budget |
| --- | --- | --- |
| API availability | 99.5% of requests succeed, monthly | About 3.6 hours a month |
| Money correctness | Zero unexplained reconciliation differences | None |
| Payout speed | 99% of released payouts confirmed within 24 hours | 1% |
| New-task notification | p95 under 10 seconds from publish to push sent | 5% |
| Chat delivery | p95 under 1 second between online users | 5% |

An **error budget** is the failure you have agreed to accept. While the budget remains, ship
features; when it is spent, reliability work comes first. It turns "is the system reliable
enough?" from an argument into a number.

### Alerts

Two kinds only:

| Kind | Rule | Examples |
| --- | --- | --- |
| **Page** (a phone rings, any hour) | A user or money is being harmed now, and a person must act | API error rate high for 5 minutes; oldest job older than 10 minutes; a sweep has not run for 10 minutes; any payout in Unknown for an hour; reconciliation difference found |
| **Ticket** (next working day) | Something is degrading but can wait | Disk growing; a provider slower than usual; error budget burning faster than planned |

If a page does not need someone to act, it becomes a ticket or is deleted. Two engineers cannot
survive a noisy pager; they will start ignoring it, and then miss the real one.

**On-call:** the two engineers alternate weeks. The ops person is told about incidents that affect
users, and never paged for technical ones.

### Error tracking

An error tracker for the backend and the mobile app, with the same scrubbing as the logs.

## 3. Recover

### Recovery targets

| Term | Meaning | Target |
| --- | --- | --- |
| **RPO** (recovery point objective) | How much recent data we can afford to lose | 5 minutes, from point-in-time recovery |
| **RTO** (recovery time objective) | How long we can be down while recovering | 1 hour, inside the 99.5% budget |

### What protects what

| Failure | Protection | Recovery |
| --- | --- | --- |
| Database machine fails | Standby in a second zone | Automatic failover in a minute or two |
| Bad deploy | Previous image kept | Roll back in minutes |
| A bug corrupts data | Point-in-time recovery | Restore to a new database at the moment before the bug; repair from it |
| Whole region fails | Backups copied to AWS's Hyderabad region | Rebuild from CDK and the copied backup; hours, accepted as rare |
| Files deleted by mistake | Bucket versioning, with old versions kept only 7 days | Restore the previous version |

**Money after a restore.** Restoring to five minutes ago can lose ledger entries for money that
really moved. This is where the gateway being the source of truth ([ADR-0001](adr/0001-use-a-payment-gateway.md))
pays off: after any restore, reconciliation runs immediately, and any gateway transaction missing
from the ledger is posted through the normal path ([05b](05b-money.md)).

**Restore drills.** A backup that has never been restored is a hope, not a backup. Once a quarter,
restore production's backup into a scratch database and run the reconciliation and invariant
checks against it.

### When a provider is down

This answers the discovery question "what must happen when a third party is down?".

| Provider down | Users see | The system does |
| --- | --- | --- |
| Payment gateway | "Payments are temporarily unavailable" on pay and payout screens | Money actions wait; jobs retry with backoff; nothing is guessed (fail closed) |
| ID verification | "Verification is taking longer than usual" | Doers stay pending; everything else works |
| Push service | Nothing, if the app is open | In-app and realtime updates continue; pushes retry |
| Auth provider | New logins fail | Existing sessions continue until their tokens expire |
| Object storage | Attachments fail to load or upload | Text chat and everything else work |

### Runbooks

A one-page runbook each for the incidents most likely to happen or most damaging:

1. Reconciliation found a difference and payouts are paused.
2. Jobs are not being processed.
3. The payment gateway is down.
4. A suspected data breach (who decides, who is told, and the legal notification deadlines,
   which the lawyer must confirm).
5. A user reports their account was taken over ([05f](05f-trust.md)).

After every incident that pages: a short, blameless write-up of what happened, why, and what
changes. The question is always "what let this happen?", never "who did this?".

## 4. Security operations

- **Least privilege per process.** The API, realtime and worker each run with their own AWS role;
  only the roles that need the verification bucket's key can use it ([05e](05e-sensitive-data.md)).
- **No long-lived credentials.** Deploys authenticate from CI to AWS with short-lived tokens;
  application secrets live in AWS's secrets store, never in code or environment files.
- **Multi-factor login** for every AWS and GitHub account; the AWS root account locked away.
- **Rate limiting** at the load balancer, and in the API for expensive or sensitive endpoints.
- **Dependency updates** proposed automatically and reviewed weekly.

## 5. Cost

Order-of-magnitude monthly figures for production at the month-12 load, before credits. Prices
change; confirm with the AWS pricing calculator before relying on them.

| Item | Rough monthly cost |
| --- | --- |
| RDS PostgreSQL, small instance with a standby, ~200 GB | $130–170 |
| Fargate: 2 API, 1–2 realtime, 1–2 worker, small sizes | $70–110 |
| Application Load Balancer | $25–40 |
| NAT gateway and data transfer | $40–80 |
| CloudWatch logs and metrics | $20–60 |
| S3 (hundreds of GB with lifecycle deletion) | $5–30 |
| Secrets, keys, backups copied to Hyderabad | $15–30 |
| **Production total** | **about $300–520** |
| Staging (one zone, smaller) | about $80–120 |
| **AWS total** | **about $380–640 a month (roughly ₹32,000–54,000)** |

**What the numbers say**

1. **It fits the ₹50,000 budget, but not by much at the month-12 load.** Before that, traffic is far
   lower and smaller sizes suffice; the $5,000 of credits cover most of the first year.
2. **The usual surprises are not the servers.** NAT gateways, log volume and cross-zone traffic
   are where AWS bills grow unexpectedly. Use a free S3 endpoint inside the network instead of
   sending S3 traffic through NAT, keep logs 30 days, and do not log request bodies.
3. **The largest variable cost may not be AWS at all**: SMS for login codes, the authentication
   provider's per-user charge, the ID verification fee per doer, and gateway fees. Include them in
   the founder's unit economics.
4. **Set a budget alarm** at 80% of the monthly figure from day one.

## 6. The ladder: what to build when

Operations work arrives in step with the product, not all at once.

| Milestone | Operations in place |
| --- | --- |
| **Investor demo (month 3)** | Staging built from CDK; the pipeline with checks; error tracking; backups on |
| **Beta (month 4)** | Production; database standby; pages for money and stalled jobs; daily reconciliation; runbooks 1–3 |
| **Launch (month 6)** | SLO dashboards; on-call rota; a completed restore drill; runbooks 4–5; budget alarm; backups copied to Hyderabad |
| **After launch** | Tracing across processes; load test at 3× the expected peak; review the error budgets monthly |

## Invariants

1. Nothing in production is created by hand; everything comes from the CDK code.
2. Every schema change works with both the previous and the next version of the code.
3. Every page has a runbook, or it is not a page.
4. The quarterly restore drill passes the reconciliation and invariant checks.
