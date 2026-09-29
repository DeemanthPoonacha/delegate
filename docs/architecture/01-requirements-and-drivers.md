# 01 · Requirements and drivers

**Status:** Draft 2. Source: [00-discovery.md](00-discovery.md).

This document answers one question: **what forces shape Delegate's architecture?** Every later
decision should trace back to a line here. If a decision cannot, either the decision is
unjustified or this document is missing something.

Each section opens with a **How** note explaining the technique, so the document doubles as a
worked example.

## 1. Capacity, back of the envelope

> **How.** Turn the founder's business numbers into technical load. Write every estimate as a
> chain of multiplications with its assumptions labelled, so anyone can challenge one link. Round
> aggressively: the goal is the right order of magnitude, not precision. Then write down the
> *conclusion*, because the conclusion is the only part that shapes the design.

### Assumptions

| # | Assumption | Value | Basis |
| --- | --- | --- | --- |
| A1 | Tasks per day at month 12 | 2,000 | Founder's target |
| A2 | Tasks in year 1 | ~180,000 | Launch at ~45/day in month 6, ramping roughly linearly to 2,000/day by month 12: about 1,000/day average over ~180 days |
| A3 | Applications per task | 20 | Ceiling; small tasks will see fewer |
| A4 | Chat messages per task | 100 | Ceiling for small tasks; projects may exceed it but are rarer |
| A5 | Files per task | 3 on average, 10 at most | Photos, scans, deliverables |
| A6 | File size | 1 MB on average, 2 MB at most | Compressed phone photos and PDFs |
| A7 | Registered users at month 12 | 100,000 | Founder's "1 lakh" |
| A8 | Daily active users | 15% of registered = 15,000 | Typical for a marketplace; to be checked against real data |
| A9 | API calls per active user per day | 40 | Feed refreshes, opening tasks, chat history, profile |
| A10 | Evening peak | 30% of daily traffic in 3 hours, with 3× bursts | Founder: "probably evenings"; bursts from push notifications |

### Estimates

**Request rate**

- Reads: 15,000 users × 40 calls = 600,000 a day
- Writes: 2,000 tasks + 40,000 applications + 200,000 messages ≈ 250,000 a day
- Total ≈ 850,000 a day ÷ 86,400 seconds ≈ **10 requests a second on average**
- Evening: 30% × 850,000 ÷ 10,800 seconds ≈ 24 a second; with 3× bursts ≈ **75 a second at peak**
- **Design target: 100 requests a second.** The draft's 300 is harmless headroom, but it was a
  guess; 100 is derived.

**Database rows and size**

- Rows: 2,000 + 40,000 + 200,000 ≈ 242,000 a day ≈ **88M a year** at the month-12 rate
  (about 22M in year 1, using A2)
- Size: messages ~0.5 KB, applications ~1 KB → ~150 MB a day ≈ 55 GB a year; double it for
  indexes ≈ **110 GB a year**

**File storage**

- Typical: 2,000 × 3 files × 1 MB = 6 GB a day ≈ **2.2 TB a year**
- Ceiling: 2,000 × 10 × 2 MB = 40 GB a day ≈ 14.6 TB a year
- **Retention changes everything.** The founder wants shared documents deleted when a task ends.
  If task files are deleted 30 days after closing, and a task lives about 10 days on average, the
  steady state is roughly 6 GB × 40 days ≈ **240 GB**, not terabytes. How long deliverables must be
  kept is still an open question (see [00-discovery.md](00-discovery.md), *Still unasked*).

**Concurrent connections**

- Tasks in progress at any moment: ~3,000 (small tasks last a day or two; projects last weeks but
  are few)
- × 2 participants = 6,000 people with a live task; ~20% online at peak ≈ 1,200 chat connections
- Doers watching the feed: 15,000 × 10% online at peak ≈ 1,500
- **About 3,000 concurrent connections at peak**

**Money movements**

- Collections, payouts and refunds ≈ 5,000 a day ≈ **0.06 a second**

### What the numbers say

1. **Scale is not a driver.** 100 requests a second, 110 GB a year and 3,000 connections fit on
   one modest application server and one ordinary relational database. Nothing here needs
   sharding, microservices or a distributed database.
2. **At 10× (20,000 tasks a day) the answer barely changes**: about 1 TB of database a year and
   1,000 requests a second at peak, which is still a single larger database. The design does not
   need to anticipate that load; it only needs to avoid making it hard.
3. **Money volume is tiny, so money is hard for correctness reasons, not throughput ones.** Five
   thousand movements a day can each afford a careful, slow, fully logged path.
4. **The cost budget holds.** Nothing above approaches ₹50,000 a month. The real cost risk is
   paying for complexity (clusters, managed streaming, multi-region) the load does not need.

## 2. Quality attributes

> **How.** A quality attribute describes *how well* the system does something, not *what* it
> does. "Ratings" is a feature; "a rating can never be counted twice" is a quality. Make each one
> testable by writing it as a **scenario**: a stimulus, the conditions, and a measurable
> response. Then **rank them**. Attributes conflict, and the ranking is what settles the conflict
> when two engineers disagree at 11 pm. A ranking that does not say what loses is only a list.

| Rank | Attribute | Scenario and measure | Founder's words |
| --- | --- | --- | --- |
| 1 | **Financial correctness** | A payment request is retried, the server crashes mid-payout, or the gateway's callback arrives twice: **money moves exactly once**. Nightly reconciliation against the payment provider shows **zero unexplained differences**. Every paisa is traceable to a task and a cause, and the records are kept for years. When the system does not know whether money moved, it **stops and asks** rather than guesses. | "Losing track of money or paying twice ends the company." |
| 2 | **Security and privacy** | An ID scan or Aadhaar copy is shared for a task: it is encrypted at rest, every access is logged, and it is deleted within an agreed window after the task closes. A message containing an OTP, password or UPI PIN is blocked before delivery. An ops user sees only what their role needs. | "Never passwords, OTPs or UPI PINs." "Should disappear when the task ends." |
| 3 | **Simplicity and time to market** | Two engineers ship a demo at month 3 and a beta at month 4. Every component is either managed by a provider or already known by the team; **one deployable backend**; nothing requires expertise nobody on the team has. | "Investor demo in 3 months." "Nobody does DevOps." |
| 4 | **Timeliness** | A task is published during the evening peak: **every matching doer's phone shows it within 10 seconds** (95th percentile). A chat message between two online users arrives within 1 second. | "Within seconds, or another doer takes it." |
| 5 | **Operability** | The ops person freezes a payout or suspends an account: it **takes effect within 1 minute**, everywhere, including for work already in flight. She sees a task's full history, chat and money on one screen, and every ops action is recorded with who did it and why. | "Freeze a payout or ban an account immediately." |

**Why this order.** Correctness is first because a money error is the one failure the founder
called fatal. Security is second because leaked ID documents are both a trust failure and a
legal one. Simplicity ranks above timeliness because a system that meets the 10-second target
but misses the month-3 demo has no users to notify. Timeliness ranks above operability because
missed tasks drive doers away daily, while ops actions are rare.

**Deliberately traded away**

| Attribute | What we accept | What it costs |
| --- | --- | --- |
| **Availability** | 99.5% a month, about 3.6 hours of downtime. One region, one database with automated backups and failover, no active-active setup. For money, the system **fails closed**: if unsure, it pauses payments rather than risk a wrong one. | An occasional outage and some slipped tasks, which the founder called annoying but survivable |
| **Scalability beyond 10×** | Designed for 2,000 tasks a day with room to reach about 20,000 | Parts of the design will need rework past that point, when the company can afford it |
| **Strict freshness of the feed** | The feed may be a few seconds stale. Only money must be strongly consistent. | A doer may occasionally tap a task that has just been taken |

**Secondary attributes** (they matter, but lose to the five above in a conflict):
- **Usability on poor networks**: the app works on cheap Android phones on patchy 4G, and drafts
  survive a crash. Mostly the mobile app's concern; the backend's part is making every submit safe
  to retry.
- **Modifiability**: the year-2 roadmap (section 5) can be added without a rewrite.

## 3. Constraints

> **How.** Constraints are facts you do not get to choose. Separate them from decisions: "we use
> Postgres" is a decision, "the team knows Postgres" is a constraint. For each one, write what it
> implies, because an unexplained constraint gets forgotten.

| Kind | Constraint | Implication |
| --- | --- | --- |
| Team | Two engineers: one mobile, one backend who is also the architect | One backend codebase; no component that needs its own specialist |
| Skills | TypeScript, Node, React, Python, Postgres, Mongo, React Native | Choose from what is known; anything new must earn its learning cost |
| Skills | Nobody has built payments or done DevOps | Buy payments; use managed hosting, databases and queues |
| Time | Demo at month 3, beta at month 4, launch at month 6 | Scope is cut before quality is |
| Budget | Infrastructure under ₹50,000 a month; $5,000 of AWS credits | Pay-per-use managed services; the credits favour AWS |
| Clients | Android-first, cheap phones, patchy 4G | Small payloads; retry-safe writes; offline drafts |
| Clients | One mobile app for both roles; a separate internal ops console | Two clients with very different users and permissions |
| Regulation | An RBI rule restricts who may hold other people's money *(unverified)* | The money flow's legal shape is unknown; isolate it (see R1) |
| Regulation | Aadhaar authentication is not easily available *(unverified)* | ID verification goes through a third-party provider |
| Regulation | Data protection law applies *(unverified)* | Consent, deletion and breach handling are requirements, not extras |
| Regulation | Karnataka gig-worker welfare fee, about 1% of payouts, with government reporting *(unverified)* | Payouts must record the fee and produce reports |
| Regulation | Money records kept for years *(period unverified)* | Money history is append-only and never deleted |
| Business | One city at launch; commission marketplace; no employees | No multi-city logic yet, but no hard-coded city either |
| Business | Never passwords, OTPs or UPI PINs; no phone numbers before hiring | Message content is filtered on the server, not just the app |

**Hosting region.** Hosting in India is assumed. It may be required by regulation (unverified),
and it is the better choice for latency either way, so adopting it early costs nothing.

## 4. Architecturally significant requirements

> **How.** Most requirements do not shape the architecture: editing a profile is a form and a
> table, whatever the design. A requirement is **architecturally significant** when it is hard to
> change later, cuts across many parts of the system, or pushes a quality attribute to its limit.
> A useful test: *if we got this wrong, would fixing it take a week or a rewrite?*

| ID | Requirement | Why it is significant |
| --- | --- | --- |
| ASR-1 | Money is held from the moment a doer is chosen until the task ends, then released, refunded or split along **six paths**: approval, auto-approval, cancellation with a 10% forfeit, doer no-show, partial dispute outcome, full refund | A single "paid" flag cannot represent this. It needs an explicit lifecycle and a record of every movement, and it is attribute #1 |
| ASR-2 | Things happen **when nobody acts**: auto-approval after 48 hours, deadline lapse and reassignment, payout within 24 hours, the 48-hour dispute window, document deletion after closing | Needs durable scheduled work that survives restarts and deploys, and never runs twice. A timer in server memory is lost on restart |
| ASR-3 | A new task reaches every matching doer's phone **within 10 seconds** | Needs a fast path from "task saved" to "matching doers found" to "push sent", and a precise definition of *matching* |
| ASR-4 | A chat per task with files, **filtered for credentials and phone numbers**, locked when the task closes | Needs persistent connections alongside ordinary requests, and server-side checks on every message |
| ASR-5 | Sensitive documents are **encrypted, access-logged and deleted** after the task closes | Shapes how files are stored and served, and adds a deletion job (ASR-2) |
| ASR-6 | **Progressive trust**: anyone can post, a doer must be verified before being paid, and larger or sensitive tasks need more verification | A permission rule that every part of the system must check the same way |
| ASR-7 | Ops can freeze or suspend **within a minute**, with every action audited | Ops actions must go through the same rules as user actions, never through direct database edits |
| ASR-8 | Drafts survive a crash; submits on a flaky network **never create duplicates** | Every write that matters must be safe to retry, which starts at API design |

**Deliberately not significant:** profiles, categories, ratings, reviews, search filters, the
task gallery. Each is a feature with ordinary data. They do not need an architectural decision.

## 5. Likely changes

> **How.** Architecture is partly a bet on what will change. You do not build year-2 features now,
> but you avoid decisions that would make them expensive. For each likely change, ask: *what would
> we regret having hard-coded?*

| Change (founder's year-2 list) | Do not hard-code… |
| --- | --- |
| Staged payments for large projects | …one payment and one release per task. Money should be able to move in parts |
| Monthly retainers and recurring weekly tasks | …the idea that a task is created only by a person posting it |
| More cities | …the city. Store it on tasks and users from day one |
| Hindi and Kannada | …text in the backend. Error messages and notifications use keys, not sentences |
| Business accounts with GST invoices | …the assumption that every account is one individual |
| A secure document vault | …document access inside chat. Treat "who can see this file, until when" as its own concern |
| AI help writing tasks | Nothing needed now: it only suggests text before a normal post |

## 6. Risks and open decisions

> **How.** A risk is something that could invalidate the design. For each one, name the
> architectural response: usually you cannot remove a risk, but you can **contain** it so that
> when it resolves, only one part of the system changes.

**Risks**

| ID | Risk | Impact | Architectural response |
| --- | --- | --- | --- |
| R1 | The way we hold money between payment and approval may not be legal (the RBI rule) | High: could reshape the entire money flow | Put everything that touches money behind one module with a narrow interface, so the legal structure can change without touching tasks, chat or matching. **Get a payments lawyer's answer before designing that module's insides.** |
| R2 | Tax (GST, TDS) has not been reviewed | High: could change fees and who is the seller | Same containment as R1; fee calculation lives in one place |
| R3 | ID verification without Aadhaar depends on a third-party provider | Medium | Wrap the provider behind an interface; keep verification state in our own records |
| R4 | The team has built neither payments nor infrastructure | Medium | Buy and manage (constraints above); keep the number of moving parts small |
| R5 | The month-3 demo encourages shortcuts that become permanent | Medium | Anything faked for the demo is listed and tracked as debt |
| R6 | Deals move off the platform after the first task | High for the business | Mostly a product problem; the architecture's part is the server-side filtering in ASR-4 |

**Open decisions**

| Decision | Options on the table | Needed by |
| --- | --- | --- |
| How money is held between payment and approval | A third-party escrow service (draft proposal); others to be explored in step 5. **Check any per-transaction fee against a ₹100 task before choosing.** | Step 5 (money), after R1 |
| Who pays the platform fee | Doer, requester, or both (founder undecided) | Step 5 (money) |
| Is one physical errand type in scope? | Yes or no (founder unsure) | Step 2 (context): location, distance and safety |
| Retention periods for chat, deliverables and ID documents | Founder to answer | Step 5 (data) |

**Decisions made**

| Decision | Reasoning | ADR |
| --- | --- | --- |
| Use an established payment gateway rather than building payment handling | Buy what is not our advantage and is expensive to get wrong; nobody on the team has built payments | [ADR-0001](adr/0001-use-a-payment-gateway.md) |
| One mobile app for both roles; a separate internal ops console | One identity per person; one codebase for one mobile engineer. Ops is a different user with different needs | [ADR-0002](adr/0002-one-mobile-app-for-both-roles.md) |
| A modular monolith: one codebase and one database, run as API, realtime and worker processes | Money changes stay in one transaction; one pipeline for two engineers; the load needs nothing more | [ADR-0003](adr/0003-modular-monolith.md) |
| PostgreSQL for data, jobs and events; no separate broker | No dual writes: a change and its follow-up job commit together | [ADR-0004](adr/0004-postgres-for-data-jobs-and-events.md) |
| Files in private object storage via signed URLs | File bytes stay out of the API and database; deletion by storage policy | [ADR-0005](adr/0005-object-storage-for-files.md) |
| Managed authentication for phone login | Login and SMS abuse protection without building them; authorisation stays ours | [ADR-0006](adr/0006-managed-authentication.md) |
| Host on AWS Mumbai with ECS on Fargate and RDS, defined in CDK | No servers or cluster to run; uses the credits; data stays in India | [ADR-0007](adr/0007-hosting-on-managed-containers.md) |
