# scripts

| Script | What it does | Needs |
| --- | --- | --- |
| `create-project-board.sh` | Creates the Phase 1 Projects v2 board, adds every open sprint-1 and sprint-2 issue, and populates the custom fields | `gh auth refresh -s project` |
| `populate-board-fields.py` | Fills Sprint / Role / Estimate on an existing board from the ticket markdown. Re-runnable — use it after editing a ticket's role or estimate | `gh auth refresh -s project` |

Board: [Delegate — Phase 1](https://github.com/users/DeemanthPoonacha/projects/5) (#5), created 18 Sep 2026.

The 29 issues themselves were created from [`../docs/backlog/sprint-01-tickets.md`](../docs/backlog/sprint-01-tickets.md)
and [`../docs/backlog/sprint-02-tickets.md`](../docs/backlog/sprint-02-tickets.md). Those files stay
the source of truth for ticket wording — an issue body links back to its file. If a ticket's
acceptance criteria change, change the markdown and the issue together.
