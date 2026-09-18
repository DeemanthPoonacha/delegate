# Assumption ledger

The four assumptions the PRD names, plus three the ADRs added. Each has a test, a threshold, and
what it means if it fails. **Update the Evidence and Verdict columns as the phase runs** — this
file is the output of Phase 0, more than the interview notes are.

Verdict: `untested` · `supported` · `refuted` · `mixed`.

## A1 — People will pay ₹100–500 for tasks they can technically do themselves

- **Test:** Concierge run. Count paying requesters, not interested ones.
- **Threshold:** 10 people pay real money. Below 6, the product does not exist.
- **If refuted:** The problem is not "no time", it is "not worth money". Re-examine whether the
  buyer is a consumer at all, or a small business with a budget line.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A2 — A stranger's shortlist is trusted enough to book from

- **Test:** In the concierge run, how many requesters act on the deliverable within 48 hours?
- **Threshold:** More than half act on it. If they redo the research themselves, we saved nobody
  any time.
- **If refuted:** Deliverable templates are not enough; the product needs verifiable artefacts
  (booking references, claim numbers) rather than recommendations. That narrows the category list
  hard.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A3 — Educated doers will work for ₹150–300 an hour with no commute

- **Test:** Doer interviews plus actual acceptance in the concierge run at those rates.
- **Threshold:** 10 of 30 interviewed doers accept a real task at the rate.
- **If refuted:** Supply costs more than the PRD assumes, which breaks the fee split in
  [ADR-0002](../docs/decisions/ADR-0002-fee-split.md) before it is even launched.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A4 — Errand requesters convert into project requesters

The economics depend on this one. ₹21 net on an errand never pays for anything; the ₹450 net on a
mid project does.

- **Test:** Of the requesters who paid for a Quick task, how many ask about something bigger
  within three weeks? Ask directly at task close.
- **Threshold:** 3 of 10. This is the weakest test in the phase — three weeks is too short to see
  a real conversion, so treat the result as directional only.
- **If refuted:** Delegate is two products with one shared app, and acquiring cheap-errand users
  is a cost, not a funnel. That changes the launch strategy more than it changes the build.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A5 — ₹199 is not a barrier to a first-time requester

- **Test:** Price half the concierge tasks at ₹199+ and half at ₹100–150. Compare take-up.
- **Threshold:** Take-up at ₹199 within 30% of take-up at ₹100.
- **If refuted:** [ADR-0004](../docs/decisions/ADR-0004-minimum-task-value.md) flips to a ₹100
  floor and the low price becomes a capped acquisition subsidy.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A6 — Doers accept an 18% cut

- **Test:** Tell every concierge doer the real fee before they take the task. Record objections
  verbatim.
- **Threshold:** Fewer than 3 of 10 object unprompted.
- **If refuted:** [ADR-0002](../docs/decisions/ADR-0002-fee-split.md) moves to a 15/2 split.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## A7 — The PRD's 8 categories are the right 8

- **Test:** Do not offer a category list in the concierge run. Ask what they need and categorise
  afterwards.
- **Threshold:** At least 5 of the PRD's 8 appear unprompted in real demand.
- **If refuted:** The category taxonomy in Sprint 2 and the deliverable templates in Sprint 6 are
  built on the wrong list, which is exactly the mistake this phase exists to prevent.
- **Evidence:** _(fill in)_
- **Verdict:** untested

## Known blind spots

Things Phase 0 will **not** tell us, so nobody should claim it did:

- Whether the marketplace matches without a human in the middle. An operator matched everything
  by hand; fill rate and time-to-match are unmeasured until the closed beta.
- Whether doers retain past month one. Three weeks cannot see a 30-day retention number.
- What disputes actually look like at volume. One or two disputes in 20 tasks is anecdote.
- Anything about the tax treatment in [TAX-1](../docs/compliance/README.md). That is a CA's
  answer, not a user's.
