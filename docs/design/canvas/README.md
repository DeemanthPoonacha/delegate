# Delegate UI — the design source

Twenty-three artboards, one design system, one canvas. Live and clickable:
<https://claude.ai/code/artifact/75cb0b5e-085f-4818-ae4d-525c99a1723a>

These are the canvas's own files, copied verbatim. `canvas.json` is the index — frame
positions, titles and the annotations. Each `.dc.html` is one self-contained artboard at
390×844 (Android-first), except the two reference boards. They are ordinary HTML: open one in
a browser to read the layout. The `<x-dc>` wrapper and the `./support.js` line only matter
inside the canvas editor; locally they are inert.

## The system — "Quiet"

One typeface (Instrument Sans), one colour, hairline dividers, no cards.
**The only colour in the app is your money** — a screen with no money on it has no colour at all.

Every colour is one of eleven tokens, declared as CSS custom properties on `body` and overridden
on the root element when the theme is dark. Nothing in these files is a raw hex.

| Token | Light | Dark | Use |
| --- | --- | --- | --- |
| `--bg` | `#FFFFFF` | `#0B0B0C` | The ground |
| `--surface` | `#F6F6F7` | `#17181B` | Grouped reassurance blocks |
| `--line` | `#ECECEE` | `#26282D` | Hairlines and dividers |
| `--text` | `#0B0B0C` | `#F6F6F7` | Primary copy and figures |
| `--body` | `#6E7076` | `#9A9CA3` | Secondary text |
| `--faint` | `#9A9CA3` | `#6E7076` | Dots, rings, placeholders — **never text** |
| `--money` | `#0E7C5A` | `#3FBF8F` | Money, and nothing else |
| `--money-hi` | `#0A5E44` | `#5FD3A6` | Link hover |
| `--accent` | `#0B0B0C` | `#F6F6F7` | Primary action fill |
| `--on-accent` | `#FFFFFF` | `#0B0B0C` | Text on that fill |
| `--on-money` | `#FFFFFF` | `#05130C` | Text on a money fill |

### Theme

Every board carries a `theme` tweak (`light` / `dark`). Light is the default on both sides.
In the editor it is in the Tweaks tab; in code it swaps one declaration block on the root element,
so a real implementation is `prefers-color-scheme` plus a manual override — no second stylesheet.

`--faint` fails 4.5:1 on both grounds by design. It is for dots, rings and input placeholders.
If it is ever holding words a person has to read, that is a bug.

### Theme is the person's. Role is the tab.

The doer side used to be ink because it was the doer side. That cannot survive a dark-mode
preference: a requester who picks dark would lose the signal, and a doer who prefers light would
be denied it. So neither side owns a ground any more. Role is carried by the
**Get help / Earn** tabs, which sit on every root screen.

The old look is still one click away — set a doer board's theme to dark.

### One scale

| | Value |
| --- | --- |
| Root top padding | `52px` on every phone board |
| Side padding | `24px` |
| Display | `28px / 600 / −1px` — exactly one per screen |
| Row title | `16px / 500` · Body `15px / 400` · Label `13px / 500` |
| Primary button | `54px`, radius `12px` · Secondary `48px` |
| Touch targets | ≥ `44px` |
| Figures | always `font-variant-numeric: tabular-nums` |

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
