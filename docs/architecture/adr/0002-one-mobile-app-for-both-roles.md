# ADR-0002: One mobile app for both roles, and a separate ops console

- **Status:** Accepted (2026-09-28)
- **Drivers:** simplicity and time to market (attribute 3), operability (attribute 5); constraints
  "two engineers, one of them mobile" and "Android-first, cheap phones"; ASR-6 (progressive trust)

## Context

The founder expects the same person to post tasks and do tasks, switching whenever they like. One
engineer builds and releases the mobile app. The ops person, who is not technical, needs to see
everything about a task and freeze payouts or suspend accounts.

## Options

| | A. One app, both roles | B. Two apps (requester, doer) | C. A mobile website only |
| --- | --- | --- | --- |
| Same person in both roles | Natural: one login, one profile, a mode switch | Two installs and two logins for one person | Natural |
| Release work for one mobile engineer | One codebase, one store listing, one release | Two of everything | No store releases |
| App size on cheap phones | Carries both roles' screens | Each app smaller | Nothing installed |
| Push notifications, offline drafts | Full support | Full support | Weak on Android web: unreliable push, limited offline |
| Examples | Marketplaces where users both buy and sell | Ride-hailing, where riders and drivers are different people | |

Option C fails attribute 4: timely push notifications are the core of the doer experience. Option
B suits businesses where the two sides are different people. Delegate's founder describes the
opposite.

## Decision

**Option A.** One React Native app contains both roles, with a mode switch. One codebase means
one release process, simpler management, and one identity per person.

**The ops console is a separate web application**, not a hidden screen in the mobile app. Its user
has different needs (large screens, full history), different permissions, and must never have its
code shipped inside a public app where it could be found and probed.

## Consequences

**Good**
- One identity, one profile, one verification per person.
- One release pipeline for one mobile engineer.
- Shared components (chat, task cards, payments screens) serve both roles.

**Costs and obligations**
- **App size.** Everyone downloads both roles' screens. Watch the install size on cheap phones and
  load rarely used screens lazily.
- **Navigation complexity.** Two modes in one app need a clear switch and a clear sense of which
  mode you are in. This is design work for the mobile engineer.
- **The mode switch is presentation, not security.** Hiding doer screens from someone in requester
  mode protects nobody. The server checks every action against the user's verification level
  (ASR-6), whatever mode the app is in.
- **Two clients to support**: the mobile app and the ops console. The backend serves both, with
  separate authentication and permissions for ops.

## What would change this

- Usage data showing that very few people use both roles, while the doer side grows complex
  enough (earnings, schedules, retainers) to justify its own app.
- Install size becoming a measurable cause of drop-off on low-end phones.
