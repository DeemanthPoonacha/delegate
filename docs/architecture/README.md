# Architecture, from scratch

This folder is a learning exercise: Delegate's architecture designed step by step, starting from a
founder interview rather than from the existing plan.

**Ground rule:** nothing here is copied from the PRD's architecture (section 8), data model
(section 9) or the recommendations in `docs/decisions/`. Those were written before this exercise
started. Every decision in this folder has to be derived here, from requirements, with its
reasoning written down. Where this folder and the PRD disagree, that is expected and interesting,
not an error.

## The method

Architecture works outside-in. Each step produces one document, and no step starts until the one
before it has been reviewed.

| Step | Question | Document | Status |
| --- | --- | --- | --- |
| 0 | What does the business actually need? | [00-discovery.md](00-discovery.md) | Done |
| 1 | What forces shape the system? | [01-requirements-and-drivers.md](01-requirements-and-drivers.md) | Draft 2 |
| 2 | Who and what does Delegate talk to? | [02-context.md](02-context.md) (C4 level 1) | Draft 1 |
| 3 | What are the deployable pieces? | [03-containers.md](03-containers.md) (C4 level 2) | Draft 1 |
| 4 | Where are the boundaries inside them? | `04-modules.md` | Not started |
| 5 | How do the hard parts work? | `05-*.md`, one per hard part | Not started |
| 6 | How is it run, watched and paid for? | `06-operations.md` | Not started |

Decisions made along the way are recorded as ADRs in `adr/`, numbered from 0001 independently of
`docs/decisions/`.
