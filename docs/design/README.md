# Design specs

One file per screen, written by the `ui-designer` agent or by hand, before the mobile ticket is
implemented. A spec names every state — empty, loading, populated, error, offline, pending,
rejected — and carries the final copy, not placeholders.

Mobile tickets waiting on a spec:

| Ticket | Screens | Sprint |
| --- | --- | --- |
| [S1-13](../backlog/sprint-01-tickets.md) | Phone entry, OTP entry, resend cooldown, error states | S1 |
| [S1-14](../backlog/sprint-01-tickets.md) | Profile editor, photo upload, inline validation | S1 |
| [S2-11](../backlog/sprint-02-tickets.md) | KYC explainer, DigiLocker handoff, PAN and bank entry, pending/failed/under-review | S2 |
| [S2-12](../backlog/sprint-02-tickets.md) | Doer home completeness prompts, verified badge | S2 |

## Generated Screens & Design System

The core UI screens and design system have been generated via **Stitch MCP** in project `2247593451938982513`:
- See [stitch-screens.md](stitch-screens.md) for full design system guidelines (*Executive Precision*), screen IDs, functional element breakdowns, and visual previews.

