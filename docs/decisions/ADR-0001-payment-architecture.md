# ADR-0001: Payment and escrow architecture

- **Status:** Proposed
- **Blocks:** Phase 3 (Sprint 7). Lawyer engaged by Sprint 3.
- **Decider:** Founder, with a payments lawyer

## Context

The PRD's original escrow design is not legal as drafted. Under the RBI Payment Aggregator
Directions 2025, settlement on a merchant's instruction is restricted to merchants with domestic
turnover above ₹40 lakh, and the aggregator must complete full KYC and hold a direct contract
with every merchant
([Ikigai Law](https://www.ikigailaw.com/article/639/rbi-rewrites-the-payment-aggregator-rulebook)).
An individual doer earning ₹15,000 a month does not qualify as such a merchant.

Two hard constraints from NFR-10 and section 7 survive whatever we pick: customer money never
sits in a platform-owned operating account, and the platform's own database row is never the
authority on whether money moved.

## Options

| | A. Merchant of record + payout rails | B. Third-party bank escrow |
| --- | --- | --- |
| Shape | Platform collects as the merchant, pays doers as vendors | Funds sit in a bank escrow run by an escrow provider |
| Cost per transaction | Gateway fee only (~2–2.5%) | Gateway fee + escrow fee, typically a flat ₹5–15 |
| Legal position | Platform is counterparty to every task | Platform is an intermediary; cleaner risk |
| Tax exposure | GST may apply to the **full task value**, not just commission — needs a CA | GST on commission only, more defensible |
| Lead time | Weeks (PA onboarding) | Longer (escrow agreement, bank onboarding) |
| Fits a ₹150 task | Yes | No — a flat ₹10 escrow fee is half the ₹21 net |

## Recommendation

**Option A for Quick tier, Option B above ₹5,000.** A flat escrow fee is fatal on a ₹150 task
and trivial on a ₹25,000 project, and the tasks where escrow risk actually matters are the large
ones. Run merchant-of-record for everything at launch, and add escrow-provider settlement for
Project tier once volume above ₹5,000 justifies the second integration.

Hold this loosely. The GST question in Option A is the part that could invert the recommendation,
and it is a question for a chartered accountant, not for this repo.

## Consequences

- Phase 0 and Phase 1 move **no money in-app at all**. Concierge tasks are paid directly; this is
  a feature, not a shortcut, because it keeps a PA integration off the critical path for 13 weeks.
- `escrow.state` reconciles nightly against the gateway from Sprint 7 (FR-13, FR-18).
- If Option A holds, the platform appears on the doer's payout as the payer, which makes the
  TDS 194-O obligation ours. Budget an operator day a month for it.
- The Karnataka welfare fee (1% of payout, capped ₹1.50) is deducted in the payout module
  regardless of which option wins. See [COMP-3](../compliance/README.md).

## What would change this

A CA confirming that merchant-of-record triggers GST on gross task value. That alone makes
Option B cheaper at every price point above about ₹800, and would push Project tier to escrow
from day one.
