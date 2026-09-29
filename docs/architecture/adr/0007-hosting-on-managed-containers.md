# ADR-0007: Host on AWS in Mumbai, on managed containers, defined as code

- **Status:** Accepted (2026-09-29)
- **Drivers:** simplicity (attribute 3), availability traded to 99.5% (drivers section 2);
  constraints "nobody does DevOps", "₹50,000 a month", "$5,000 of AWS credits", hosting in India;
  [ADR-0003](0003-modular-monolith.md) (three processes, one image)

## Context

Delegate runs three processes from one codebase (API, realtime, worker), a managed PostgreSQL
database and object storage. Nobody on the team does DevOps, the budget is ₹50,000 a month, and
there are $5,000 of AWS credits. Hosting in India is assumed for latency and possibly for
regulation.

## Options

| | A. Virtual machines we manage | B. Kubernetes | C. Managed containers (AWS ECS on Fargate) | D. A platform-as-a-service outside AWS |
| --- | --- | --- | --- | --- |
| Operating effort | Patching, scaling, restarts are ours | High: a cluster to run and upgrade | Low: AWS runs the machines | Lowest |
| WebSockets behind a load balancer | Yes | Yes | Yes (Application Load Balancer) | Varies by provider |
| Region in India | Yes | Yes | Yes | Varies; must be checked |
| Uses the AWS credits | Yes | Yes | Yes | No |
| Managed PostgreSQL alongside | Yes | Yes | Yes (RDS) | Varies |
| Skills needed | Linux administration | Kubernetes | Containers and some AWS | Minimal |

Kubernetes solves problems of many services and many teams; ADR-0003 chose one codebase for two
engineers. Virtual machines put patching and recovery on a team with no operations experience. A
platform outside AWS is attractive for simplicity, but gives up the credits and needs its India
region, WebSocket support and database checked one by one.

## Decision

**Option C**, in the AWS Mumbai region:

- **One container image**, started as `api`, `realtime` or `worker`, on ECS with Fargate.
- **RDS for PostgreSQL** with a standby in a second availability zone, automated backups and
  point-in-time recovery.
- **S3** for the two buckets ([ADR-0005](0005-object-storage-for-files.md)).
- **An Application Load Balancer** in front of the API and realtime processes.
- **All of it defined as code** with AWS CDK in TypeScript, the team's language. Nothing is created
  by hand in the console, so staging and production are built from the same definition.

## Consequences

**Good**
- No servers to patch; failed containers are replaced automatically.
- Staging is a smaller copy of production from the same code.
- The credits cover the first several months.

**Costs and obligations**
- **Some AWS to learn**: networking, IAM roles, ECS. Much smaller than Kubernetes, but real. Budget
  a week in the first sprint.
- **Watch the cost traps**: NAT gateways, log volume and cross-zone traffic are the usual surprises
  (see the cost estimate in [06-operations.md](../06-operations.md)).
- **Lock-in to AWS services** is accepted. The application itself is a plain container and a plain
  PostgreSQL database, so moving is work, not a rewrite.

## What would change this

- Operating AWS taking a noticeable share of engineering time after launch: move to a
  platform-as-a-service with an India region.
- Several teams and many services: the point at which Kubernetes starts to pay for itself.
