# Backlog

| File | What it is |
| --- | --- |
| [requirements.md](requirements.md) | FR-1…FR-28 with priority, story trace, target sprint, and what the ADRs changed |
| [sprints.md](sprints.md) | Phases 0–5 with dates, sprints S1–S9, blockers and long-lead items |
| [sprint-01-tickets.md](sprint-01-tickets.md) | S1 broken into 15 tickets — auth, profiles, infrastructure |
| [sprint-02-tickets.md](sprint-02-tickets.md) | S2 broken into 14 tickets — KYC, categories, ops console |

User stories (30 across seven epics) are not duplicated here — they live in PRD section 4 and the
`Stories` column in `requirements.md` points into them by number.

## How to use this during Phase 0

Do not groom the backlog yet. Phase 0 exists to find out whether the top five categories in the
PRD are the real ones, and the deliverable templates in S6 depend on that answer. Adding tickets
before the interviews are synthesised is building on a hypothesis.

What Phase 0 *should* change here: the category list, the deliverable templates, the price floor
in FR-5, and possibly the fee model in FR-18.

## Ticket conventions

- IDs are `S<sprint>-<nn>`, stable once assigned. `S1-00` and `S2-00` are the non-engineering
  blockers that must start before the sprint opens.
- Every ticket names the role (`be`, `mob`, `ops`), an estimate in engineer-days, what it traces
  to (an FR, an NFR or a compliance ID), and what it depends on.
- Acceptance criteria are checkboxes. A ticket is done when they are all ticked, not when the
  code merges.
- S1 and S2 are ticketed because Phase 0 findings barely touch them. **S3 onward is deliberately
  not ticketed yet** — the deliverable templates and category taxonomy those sprints build on are
  Phase 0 outputs.

One ticket is explicitly gated on Phase 0: [S2-08](sprint-02-tickets.md) seeds the launch
categories from the synthesis, not from the PRD's list of 8.
