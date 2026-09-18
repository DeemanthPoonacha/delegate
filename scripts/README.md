# scripts

| Script | What it does | Needs |
| --- | --- | --- |
| `create-project-board.sh` | Creates the Phase 1 Projects v2 board with Sprint / Role / Estimate fields and adds every open sprint-1 and sprint-2 issue | `gh auth refresh -s project` |

The 29 issues themselves were created from [`../docs/backlog/sprint-01-tickets.md`](../docs/backlog/sprint-01-tickets.md)
and [`../docs/backlog/sprint-02-tickets.md`](../docs/backlog/sprint-02-tickets.md). Those files stay
the source of truth for ticket wording — an issue body links back to its file. If a ticket's
acceptance criteria change, change the markdown and the issue together.
