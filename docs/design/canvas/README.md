# Delegate UI — the design source

Twenty-three artboards, one design system, one canvas. Live and clickable:
<https://claude.ai/code/artifact/75cb0b5e-085f-4818-ae4d-525c99a1723a>

These are the canvas's own files, copied verbatim. `canvas.json` is the index — frame
positions, titles and the annotations. Each `.dc.html` is one self-contained artboard at
390×844 (Android-first), except the two reference boards. They are ordinary HTML: open one in
a browser to read the layout. The `<x-dc>` wrapper and the `./support.js` line only matter
inside the canvas editor; locally they are inert.

## The system — "Quiet"

One typeface (Instrument Sans), one colour (`#0E7C5A`), hairline dividers, no cards.
**The only colour in the app is your money** — a screen with no money on it has no colour at
all. The ground inverts with the role: requester white, doer ink (`#0B0B0C`).

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#0B0B0C` | Text, primary actions, doer ground |
| Held | `#0E7C5A` (`#3FBF8F` on ink) | Money, and nothing else |
| Body | `#6E7076` (`#9A9CA3` on ink) | Secondary text — the lightest grey allowed on text |
| Rest | `#ECECEE` (`#26282D` on ink) | Hairlines and dividers |
| Fill | `#F6F6F7` (`#17181B` on ink) | Grouped reassurance blocks |
| Ring | `#C8CACE` | Empty steps and dots — never text |

Every figure carries `font-variant-numeric: tabular-nums`. Targets are ≥44px. Body text holds
4.5:1 on whichever ground it sits on.

## Reference boards

| File | What it is |
| --- | --- |
| `Main.dc.html` | The system: tokens, type scale, parts, the role inversion |
| `EscrowStates.dc.html` | Every escrow state × what each side sees × what the money is doing. **Build S7 from this board.** |

## Onboarding — Phase 1

| File | Screen | Ticket |
| --- | --- | --- |
| `Phone.dc.html` | Phone entry, consent notice before OTP | S1-13, S1-09 |
| `Otp.dc.html` | Six-digit code, resend cooldown, lockout copy | S1-13 |
| `Profile.dc.html` | Name, city, languages, which side you start on | S1-14, S1-12 |
| `Kyc.dc.html` | DigiLocker → PAN → penny-drop, three checks | S2-11 |
| `KycPending.dc.html` | Checking / name mismatch / human review | S2-11, S2-10 |

## The requester loop — Phase 2

| File | Screen | Traces to |
| --- | --- | --- |
| `HomeRequester.dc.html` | Home, persona tabs, running tasks, re-post row | FR-2, FR-22 |
| `Post.dc.html` | One screen, four fields, 90-second timer | FR-5, FR-6, FR-7 |
| `Applicants.dc.html` | Pick a doer — badge, rating, category history | FR-12, FR-4 |
| `Fund.dc.html` | Escrow funding — held, not sent | FR-13 |
| `TaskRoom.dc.html` | Chat with the pinned deliverable dock | FR-14, FR-15 |

## Delivery, the doer side, the money — Phase 2 into 3

| File | Screen | Traces to |
| --- | --- | --- |
| `Review.dc.html` | Deliverable review, approve and release, 48-hour countdown | FR-16, FR-17 |
| `HomeDoer.dc.html` | Doer home on ink ground | FR-2, FR-9 |
| `DoerFeed.dc.html` | Feed, filters, net earnings before applying | FR-9, FR-10, FR-11 |
| `Earnings.dc.html` | Payout with fee, welfare levy and TDS itemised | FR-18, COMP-3, TAX-2 |
| `Guardrails.dc.html` | Where your money is; the never-share list; dispute | FR-20, FR-24 |

## Later — not before Phase 4

`VoicePost` · `Gallery` · `Bids` · `Vault` · `Handoff` · `Bench`. Carried over from the earlier
canvases so the ideas are not lost. They map to deferred requirements (FR-24, FR-26, FR-28) and
should not be built before the closed beta.

## Decisions these screens encode

- **No booking fee on the requester side.** The 18% comes out of the doer's payout, so the price
  posted is the price paid — [ADR-0002](../../decisions/ADR-0002-fee-split.md).
- **The doer feed shows net earnings** with the gross struck through, before applying.
- **Deductions are named.** Platform fee, welfare levy and TDS each appear as their own line.
- **Doer prepares, requester submits** wherever a task touches an account.
