# Design specs

Wireframes and design reference. A screen here names its states — empty, loading, populated,
error, offline, pending, rejected — and carries the final copy, not placeholders.

**These are not build input.** Architecture and implementation are decided in their own
sessions; this folder exists so those decisions are made against a settled picture of what each
screen does, not so the markup gets ported.

Mobile tickets these screens cover:

| Ticket | Screens | Sprint |
| --- | --- | --- |
| [S1-13](../backlog/sprint-01-tickets.md) | Phone entry, OTP entry, resend cooldown, error states | S1 |
| [S1-14](../backlog/sprint-01-tickets.md) | Profile editor, photo upload, inline validation | S1 |
| [S2-11](../backlog/sprint-02-tickets.md) | KYC explainer, DigiLocker handoff, PAN and bank entry, pending/failed/under-review | S2 |
| [S2-12](../backlog/sprint-02-tickets.md) | Doer home completeness prompts, verified badge | S2 |

## The design source

One canvas, one design system, twenty-three screens: **[canvas/](canvas/)**, live at
<https://claude.ai/code/artifact/75cb0b5e-085f-4818-ae4d-525c99a1723a>.

It unifies four earlier canvases and supersedes them. The system is "Quiet" — one typeface, one
colour, the ground inverting with the role — chosen over the three alternatives (Ledger, Signal,
Night desk) because it is the cheapest system to build and keep consistent, and because starving
the interface of colour is what makes escrow impossible to miss. That matters at ₹21 net on a
₹150 task.

The four mobile tickets above now have screens. `Phone`, `Otp`, `Profile`, `Kyc` and `KycPending`
did not exist in any earlier canvas — every one of them started at a logged-in home screen.

### Superseded

| Source | Status |
| --- | --- |
| [stitch-screens.md](stitch-screens.md) | Superseded. Kept for the screen IDs and previews; do not build from it. |
| Delegate Mobile UI (`7fe84f9b`) | Superseded — its 16 screens and 4 system options are folded into the source above |
| Delegate App UI (`f5b0b980`) | Superseded — its role-inversion idea is carried over |
| Delegate — Requester Flow UI (`93ddf484`) | Superseded. Showed a 10% requester fee, which contradicts ADR-0002. |

Only the canvas above is current. If a screen is not in it, it is not designed yet.
