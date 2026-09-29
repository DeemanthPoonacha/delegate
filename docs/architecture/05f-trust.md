# 05f · Trust

**Status:** Draft 1. Tiers are computed by `identity`; each module enforces the tier its own
actions need ([04-modules.md](04-modules.md), "Where the rules live"). Sources: ASR-6 in
[01-requirements-and-drivers.md](01-requirements-and-drivers.md); the signup contradiction in
[00-discovery.md](00-discovery.md); [05b](05b-money.md), [05c](05c-matching-and-feed.md),
[05e](05e-sensitive-data.md).

> **How.** Trust design answers three questions:
>
> 1. **What does each level of trust unlock?** Ask for verification at the moment it becomes
>    necessary, not at the door. Friction at signup loses users; friction just before the first
>    payout is understood.
> 2. **How is a level earned and lost?** Derive it from facts (verified documents, completed tasks,
>    disputes), so it can always be explained and recomputed. Hand-set flags drift.
> 3. **How do we stop someone stealing a trusted account?** The more an account can do, the more
>    it is worth to an attacker. Protect the actions that move money or change identity.

## 1. Tiers

The founder's contradiction was "doer signup under 2 minutes" against "ID check before payout".
Progressive trust resolves it: signup stays fast, and each check arrives when it is needed.

| Tier | Earned by | Unlocks |
| --- | --- | --- |
| **T0 · Phone** | Phone login ([ADR-0006](adr/0006-managed-authentication.md)); age 18+ declared | Post tasks; browse non-sensitive tasks |
| **T1 · Verified** | ID document, liveness selfie and PAN through the ID provider, with names matching; a payout account whose holder name matches | Apply to tasks; receive payouts |
| **T2 · Trusted** | T1, plus 10 completed tasks, a Bayesian rating of at least 4.3, no lost disputes in 60 days, account at least 30 days old | Sensitive categories (insurance, government paperwork, anything touching a requester's accounts); tasks above ₹5,000 |

**Why T1 is required to apply, not only to be paid.** If unverified doers could apply, a requester
might choose one, and the task would sit in AwaitingPayment while the doer verified, or fail
([05a](05a-task-lifecycle.md)). It would also let unverified strangers see a requester's documents.
Signup stays under 2 minutes; verification happens at the first "Apply", through a "verify to
apply" prompt in the feed ([05c](05c-matching-and-feed.md)). ID verification through the provider
takes minutes, not days. **This changes the founder's wording** ("before their first payout") and
needs their agreement.

**Requesters** stay at T0 for ordinary use. Verification (PAN) is asked for only above a
cumulative spend, as an anti-money-laundering measure (section 4).

### Losing trust

Tiers are recomputed from facts whenever a relevant event arrives (`task.closed`,
`review.published`, `dispute.decided`), never set by hand:

- T2 drops to T1 automatically when a condition stops holding, such as a lost dispute or a rating
  below the threshold. Tasks already under way continue; new sensitive tasks are no longer shown.
- **Suspension** is separate from tiers: an ops action with a reason, which hides the account
  everywhere (filter F3 in 05c) and freezes its payouts (05b). Lifting it restores the computed
  tier.
- Ops can override a tier in either direction, **only with a recorded reason**, and the override
  expires rather than lasting forever.

### Enforcement

Each module states the tier its actions need, in one table per module that tests read:

| Action | Owner | Needs |
| --- | --- | --- |
| Post a task | tasks | T0 |
| Apply to a task | tasks | T1, or T2 for sensitive categories and tasks above ₹5,000 |
| Accept an application | tasks | Requester T0; **the doer's tier is checked again at this moment** (it may have dropped since applying) |
| Receive a payout | payments | T1, name-matched payout account not in cooling-off (section 3) |
| See a sensitive task in feed or push | matching | T2 (filter F4) |

`identity.getTrustTier(userId)` is the only source of the tier. A test runs every action against
every tier and asserts the table holds.

## 2. Uniqueness

**One verified identity, one account.** The ID provider's reference for a document is stored as a
keyed hash with a unique constraint. A second account presenting the same ID is refused at
verification. This stops banned doers returning under a new phone number, and makes
rating-farming with duplicate accounts expensive.

## 3. Account takeover

**The attack.** An attacker SIM-swaps a doer's phone number, receives the login OTP, signs in on a
new device and changes the payout account. The next payouts go to the attacker. A variant needs
no SIM swap at all: the attacker poses as a requester and asks the doer to "read out the code we
just sent you" (the chat filter in [05d](05d-realtime.md) blocks OTPs, which helps here too).

Phone OTP login alone cannot stop this: whoever holds the number holds the account. So the actions
that matter get extra protection.

**Sensitive actions:** change the payout account, change the phone number, change the verified
name, withdraw above a limit.

| Control | What it does | Cost to an honest doer |
| --- | --- | --- |
| **Name match** | A new payout account's holder name must match the verified name, checked by the bank verification | None |
| **Step-up check** | A liveness selfie, matched against the verification photo | About 30 seconds |
| **48-hour cooling-off** | The change takes effect 48 hours later | Payouts to the new account wait two days, once |
| **Notify every channel** | Push to **all previously registered devices**, plus email if on file, with a one-tap "This wasn't me" that freezes the account and payouts | None |
| **Payouts keep going to the old account** during cooling-off | The attacker gains nothing during the window | If the old account is closed, those payouts wait for the new one |
| **Extra scrutiny on new devices** | A sensitive action within 24 hours of first login on a new device needs ops review | Rare |

**Why every channel.** After a SIM swap, SMS and calls go to the attacker. The victim's old phone
still has the app and can still receive push over Wi-Fi, so the warning goes to every device that
was registered before the change, not to the phone number.

**Why the name match matters most.** The delay and the notice give the victim time to react; the
name match means that even an unnoticed attacker needs a bank account in the victim's name, which
defeats most takeovers on its own.

The 48-hour delay conflicts with the founder's "paid within 24 hours" promise for that one payout.
The app says so plainly when the doer changes accounts.

## 4. Fraud patterns and limits

| Pattern | Control | Where |
| --- | --- | --- |
| Duplicate accounts after a ban | One verified identity per account | Section 2 |
| Rating rings | Reviews only after a paid, closed task; Bayesian ratings; repeated reviews between the same pair count less | [05c](05c-matching-and-feed.md), `reviews` |
| Money laundering through inflated tasks | A per-task cap (₹25,000 at launch); monthly spend and earnings limits per account; requester PAN verification above a cumulative spend; alerts on repeated high-value tasks between the same pair | `tasks`, `payments` |
| Deals taken off the platform | Contact details blocked before hire; falling fees for repeat pairs | [05d](05d-realtime.md), [05b](05b-money.md) |
| Doers abandoning tasks | Completion rate feeds the tier and the ranking | Section 1, [05c](05c-matching-and-feed.md) |
| Requesters who dispute everything | Dispute rate tracked; above a threshold, disputes go to ops review before any automatic outcome | `disputes` |

Limits are data, like fees: versioned, and changeable without a deploy.

## Invariants

1. No payout goes to an account that is in cooling-off or failed the name match.
2. No doer below T1 has an active application; no doer below T2 holds a sensitive-category task.
3. One verified identity is linked to at most one account.
4. Every tier override and suspension has a recorded reason and an actor.
5. A tier is always reproducible from the facts it was computed from, plus recorded overrides.

## Questions for the founder

| Question | Draft answer |
| --- | --- |
| Verify before the first application, instead of before the first payout? | Yes (section 1) |
| Are the T2 thresholds right (10 tasks, 4.3, 30 days)? | Start there; tune with beta data |
| Per-task cap and monthly limits? | ₹25,000 per task; monthly limits to set with the CA |
| At what cumulative spend should requesters verify their PAN? | To set with the CA and lawyer |
| Is 48 hours an acceptable delay for payout account changes? | Yes, with a clear in-app explanation |
