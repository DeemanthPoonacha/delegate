# 05c · Matching and feed

**Status:** Draft 1. Owner module: `matching` ([04-modules.md](04-modules.md)). Sources:
attribute 4 (timeliness) and ASR-3 in
[01-requirements-and-drivers.md](01-requirements-and-drivers.md); doer personas in
[00-discovery.md](00-discovery.md); the publish walkthrough in [03-containers.md](03-containers.md).

> **How.** Matching is three problems that look like one. Name them separately, because each
> ranks something different for someone different:
>
> | Problem | Ranks | For |
> | --- | --- | --- |
> | **Feed** | Tasks | A doer browsing the app |
> | **Push** | Doers | A task that was just published |
> | **Applicants** | Doers | A requester choosing among applicants |
>
> For each: **filter, then rank.** Hard rules decide *whether* something can appear and are never
> traded against anything. A score decides the *order*. Start the score as a transparent weighted
> sum in SQL with weights in config, log what was shown, and tune from real data later.

## Capacity: what the feed actually searches

- Quick tasks are open for about 30 minutes to a few hours; projects for a few days.
- At 2,000 tasks a day that is roughly **1,000–1,500 open tasks** at any moment.
- A filtered, scored query over 1,500 rows takes milliseconds in PostgreSQL.

**No search engine, no cache.** Both would add a system to run and a second copy of the data to
keep in step, to speed up a query that is already fast. Revisit if open tasks pass about 50,000
or free-text search becomes a feature.

## Hard filters

A doer is never shown, or notified about, a task unless all of these hold. They apply to all three
problems.

| # | Filter | Why |
| --- | --- | --- |
| F1 | The task is Open and its deadline has not passed | Nothing else can be applied to ([05a](05a-task-lifecycle.md)) |
| F2 | The doer is not the requester | One person can hold both roles ([ADR-0002](adr/0002-one-mobile-app-for-both-roles.md)) |
| F3 | The doer is not suspended | Ops's suspension must take effect everywhere within a minute (attribute 5) |
| F4 | The doer's trust tier meets the task category's requirement | Sensitive categories need a higher tier (ASR-6); lower-tier doers do not see them at all |
| F5 | The price is not below the doer's hourly floor, if they set one | The expert persona: "do not show me ₹100 errands" |
| F6 | The doer has not already applied, and neither side has blocked the other | No repeats, no unwanted contact |
| F7 | The task has not reached its applicant cap (draft: 20) | Past the cap, applying is wasted effort for the doer |
| F8 | For a physical errand: the location is within the doer's travel radius | Only if physical errands are in scope |

Two cases are softer for the **feed** than for push: an unverified doer may see non-sensitive
tasks with a "verify to apply" prompt (the fastest route to verification), and a doer may switch
off the category filter to browse everything. **Push always applies every filter**: a
notification is an interruption and must be relevant.

These filters live in one SQL function used by all three paths, so they cannot drift apart. A
test asserts that no result from any path ever violates one.

## 1. The feed: ranking tasks for a doer

> **Teaching point.** A signal is only useful for ranking if it **varies between the items being
> ranked**. The feed ranks *tasks* for one doer, so the doer's own rating is the same for every row
> and cannot change the order. Doer-quality signals belong to the other two problems, where the
> items being ranked are *doers*.

| Signal | Weight | Measures | Range 0–1 |
| --- | --- | --- | --- |
| **Relevance** | 0.35 | Task category among the doer's chosen categories, plus how many tasks the doer has completed in it | 1 = a category the doer chose and has done often |
| **Freshness** | 0.20 | How recently the task was published | Decays over about 2 hours; quick tasks go to whoever is fast |
| **Price fit** | 0.15 | Task price relative to the doer's typical task value | Highest near what this doer usually takes |
| **Time fit** | 0.10 | Task's expected duration and deadline against the doer's availability | 1 = doable in the doer's stated window |
| **Requester quality** | 0.10 | The requester's approval and dispute history | Doers avoid requesters who dispute everything |
| **Open field** | 0.10 | Fewer applicants so far | A better chance of being chosen |

For a physical errand, **distance** replaces time fit.

**How this separates the two personas.** Kiran has completed many small tasks, so small tasks
score high on price fit and relevance for Kiran. The expert has set an hourly floor, so filter F5
removes ₹100 errands before scoring, and price fit ranks the project work they usually take above
the rest. One formula, two very different feeds.

**Stable paging.** Freshness changes every second, so a score computed on page 2 would reorder
page 1. The first request fixes a reference time; later pages pass it back, and every score is
computed "as of" that time. Paging then uses a cursor on (score, task ID) and never shows a task
twice.

**New tasks while browsing.** The realtime process ([03](03-containers.md), step 3) sends new
matching tasks to online doers as a "3 new tasks" banner. The list does not reshuffle under the
doer's thumb.

**Explainability.** The two signals that contributed most are returned with each task, so the app
can say "In your categories · posted 5 min ago".

## 2. Push: choosing doers for a new task

A notification costs the doer's attention. Send too many and doers switch notifications off,
and the 10-second promise (attribute 4) stops meaning anything. So push is capped, spread out and
widened only when needed.

**Candidates:** every doer who passes the hard filters, has chosen the category, has notifications
on, is inside their availability window and outside quiet hours.

**Score for each candidate**

| Signal | Why |
| --- | --- |
| Fit | The feed's relevance, price fit and distance, from the doer's side |
| Likely to respond | Recently active; has applied after past notifications |
| Quality | Bayesian rating (see section 3) and completion rate |

**Selection: a wave of 20, split three ways**

| Share | Who | Why |
| --- | --- | --- |
| 70% | Top scorers | The best chance of a fast, good match |
| 20% | New doers (see Cold start) | Otherwise they never get a first task |
| 10% | A random pick from the remaining candidates | Keeps the top from becoming the same people forever, and gives the tuning data a baseline |

**Waves.** If there is no application within 10 minutes, the next 20 are notified, up to a limit.
The first wave is sent immediately, which is what the 4–7 second budget in
[03](03-containers.md) measured.

**Per-doer caps.** At most 4 notifications an hour and a daily limit per doer. A doer who ignores
many in a row receives fewer until they are active again.

> **Why not simply "highly rated"?** The top 10 doers would receive every notification. They
> cannot take every task, so requesters wait; and everyone else sees nothing and leaves, which is
> exactly how the student persona churns ("nothing for two hours, I uninstall").

Each notification is a row in `matching.push_log` with a unique (task, doer) pair, so a retried job
never notifies the same doer twice about the same task.

## 3. Applicants: ranking doers for a requester

Here doer quality is exactly the right signal.

| Signal | Why |
| --- | --- |
| Bayesian rating | See below |
| Completion rate | Did they finish what they took on |
| Experience in this category | Tasks completed in the same category |
| Response time | How quickly they reply in chat |
| Trust tier | Verified doers ahead of the minimum |
| Price (project bids only) | Against the requester's budget range |

**Bayesian rating.** A doer with one 5-star review is not better than one with 4.8 from 50
reviews. Every doer's average is blended with the platform average, weighted by how few reviews
they have:

```text
bayesian = (C × platform_average + sum_of_ratings) / (C + number_of_ratings)     C ≈ 10
```

One 5-star review gives about 4.5 (with a platform average of 4.4); fifty reviews averaging 4.8 give
about 4.73. It also means a new doer starts at the platform average, not at zero.

**Show why, not only the order.** Each applicant card carries labels such as "12 tasks in
Travel", "New on Delegate" or "Replies in 5 min". The requester decides; the ranking only
suggests.

## Cold start

Relevance alone does not help a new doer: an experienced doer is just as relevant *and* has
ratings, so they win every comparison. New doers need deliberate help, for a limited time:

1. **Reserved push slots**: the 20% share above.
2. **A "New on Delegate" label and a small boost** in the applicant list, fading after 5
   completed tasks or 30 days.
3. **Rating starts at the platform average** (the Bayesian prior), never at zero.
4. **Starter tasks**: small, low-risk tasks the requester marks as open to newcomers.
5. **Hand matching during the closed beta**: ops places a new doer's first task, as in the
   concierge phase.

## Data

| Table or view | Owner | Holds | Kept up to date by |
| --- | --- | --- | --- |
| `tasks.open_tasks` (view) | tasks | Open tasks with the fields matching needs | Published read-only view ([04](04-modules.md)) |
| `matching.doer_profile` | matching | Categories, hourly floor, availability windows, travel radius, languages | The doer, through the app |
| `matching.doer_stats` | matching | Bayesian rating, completion rate, tasks per category, last active, response rate to notifications | Events: `review.published`, `task.closed`, app activity |
| `matching.ranking_config` | matching | Weights, wave size, caps, boost duration; versioned | Config changes, never code changes |
| `matching.push_log` | matching | Every notification sent, and whether the doer opened or applied | The push job |
| `matching.impression` | matching | Which tasks were shown to whom, at which position, and what happened | The feed endpoint |

**`doer_stats` is a read model.** It copies facts owned by other modules (reviews, tasks) into the
shape the ranking query needs, so the feed never joins across modules on every request. It is
disposable: it can be rebuilt at any time by replaying the source data. That is what makes it safe
to keep a copy.

**The logs will be the largest tables in the system.** 15,000 active doers seeing about 50 tasks a
day is about 750,000 impression rows a day, more than chat messages. Keep 90 days of raw rows and
roll older data up into daily totals.

## Tuning later

With the impression and push logs, after a few weeks of real use:

- **Apply rate by position**: if position 1 is applied to far more than position 5 regardless of
  task, the order matters and the weights are worth tuning.
- **Push response rate by share**: compare top scorers, new doers and the random 10%.
- **Time to first application** per task: the founder's 20–30 minute target.

Change one weight at a time, as a new config version, for a cohort, and compare. Machine learning
becomes worth considering once these logs hold months of data and the simple score has stopped
improving.

## Invariants

1. No feed, push or applicant result ever violates a hard filter.
2. No doer is notified twice about the same task.
3. No task notifies more doers than its wave limit allows.
4. No doer receives more notifications than their hourly and daily caps.

## Questions for the founder

| Question | Draft answer |
| --- | --- |
| Do doers set availability windows, or is availability inferred from activity? | Doers set them, with "available now" as a one-tap toggle |
| How many applicants should a task accept before it stops being shown? | 20 |
| Should a requester be able to exclude new doers from a task? | No at launch; new doers need a route in |
| Are physical errands in scope? (decides F8 and distance) | Still open, from step 1 |
