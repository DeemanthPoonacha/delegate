# Concierge runbook

Twenty real tasks, fulfilled by hand over WhatsApp, for real money. No app, no automation, no
landing page with a waitlist. For three weeks the operator *is* Delegate.

This is not a demo. The requester is a real person paying real money, and if the work is bad they
have lost something. Treat every task as if the company already existed.

## The loop, per task

| Step | Who | What | Target |
| --- | --- | --- | --- |
| 1. Intake | Operator | Requester sends the task on WhatsApp, free-form. Do **not** offer a category menu. | — |
| 2. Scope | Operator | Restate the task in one message, name the price and the deadline, ask for a yes. | 15 min |
| 3. Match | Operator | Pick a doer from the roster by hand. Record why. | 30 min |
| 4. Brief | Operator | Send the doer the scope, the deadline and their pay, with the fee stated. | 15 min |
| 5. Do | Doer | The work. Operator stays available but does not do it for them. | per task |
| 6. Deliver | Doer → Operator → Requester | Operator checks the deliverable before it goes out, and logs what was missing. | — |
| 7. Pay | Operator | Requester pays by UPI. Doer is paid within 24 hours. | 24 h |
| 8. Close | Operator | Two questions to each side (below). Log everything. | 10 min |

Money in Phase 0 moves by direct UPI, not through any escrow. There is no platform, so there is no
regulated intermediary — which is exactly why [ADR-0001](../../docs/decisions/ADR-0001-payment-architecture.md)
stays off the critical path until Sprint 7.

## Rules that do not bend

1. **Never ask for a password, an OTP, a UPI PIN or a CVV.** If a task cannot be done without one,
   the doer prepares everything and the requester taps submit. If that is impossible, decline the
   task and log it — a task we cannot do safely is a finding, not a failure.
2. **The doer never claims to be the requester.** On any call: "I'm calling on behalf of
   [name], who has authorised me." Impersonating someone to a bank or a government body is out of
   scope permanently (PRD §7).
3. **Price before work.** No task starts without an agreed number.
4. **Log it the same day.** An unlogged task teaches nothing.
5. **Decline the prohibited list.** Licensed professional work, debt collection, surveillance,
   academic work submitted as someone's own, anything whose deliverable is another person's
   private data.

## Target mix across the 20 tasks

Deliberately spread, so the phase learns more than one thing:

| Slice | Target | Why |
| --- | --- | --- |
| Priced ₹100–150 | 5 | Tests [A5](../assumptions.md) at the low end |
| Priced ₹199–499 | 8 | The expected core |
| Priced ₹500+ | 4 | Where the margin actually is |
| Project-shaped, over 3 hours | 3 | Tests [A4](../assumptions.md) |
| In person | 3 | Tests [ADR-0007](../../docs/decisions/ADR-0007-physical-errands.md) |
| Repeat from the same requester | 5 | The north-star metric in miniature |

If demand does not arrive in this shape, do not force it — record the actual shape. That
distribution is itself a finding.

## The eight closing questions

**To the requester** (two, on WhatsApp, right after delivery):

1. Did you use it, or did you end up redoing it yourself? _(This is [A2](../assumptions.md).)_
2. What's the next thing you'd send me?

**To the doer:**

1. Was it worth your time at that rate?
2. What would have made it easier?

Log the answers verbatim. Paraphrase loses the finding.

## Quality bar before a deliverable goes out

The operator checks every deliverable. If it fails any of these, send it back once — and log that
it needed sending back, because that number is the argument for FR-15's templates:

- Does it answer the exact question asked, or an adjacent easier one?
- Is there a verifiable artefact — claim number, booking reference, link, photo with a timestamp?
- Would the requester have to do any further work to act on it?
- Is anything in it invented? _(Fabricated results are the fraud pattern that kills marketplaces.
  One instance means that doer is off the roster.)_

## Stop conditions

Stop the run and reconsider if any of these happen:

- Three consecutive requesters do not use the deliverable.
- A doer fabricates a result.
- Any task requires a credential we said we would never handle.
- Operator time per task exceeds 45 minutes on more than five tasks — at that point the manual
  model is not a preview of the product, it is a different business.
