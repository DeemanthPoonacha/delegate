# Open questions

Every question the architecture is waiting on, collected from the documents in this folder and
grouped by who can answer it. Where a document proposes a draft answer, it is shown; a question is
closed when its owner accepts or replaces the draft, and the source document is updated.

**Blocks** says what cannot be finished without the answer.

## For the payments lawyer

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| L1 | May the platform hold requesters' money between payment and approval, and through what structure (gateway, escrow provider, other)? | None; the key open risk | The inside of the payments module | [01 R1](01-requirements-and-drivers.md), [05b](05b-money.md) |
| L2 | Must user data be stored in India? | Assumed yes | Auth vendor choice | [ADR-0006](adr/0006-managed-authentication.md) |
| L3 | Can the Karnataka welfare fee be deducted from doers, or must the platform bear it? | Platform bears it | Fee rules | [05b §4](05b-money.md) |
| L4 | Can the ID verification provider retain ID images on our behalf? | Prefer yes | Whether the verification bucket exists | [05e](05e-sensitive-data.md) |
| L5 | How long must verification records and money records be kept? | To confirm | Retention rules | [05e](05e-sensitive-data.md) |
| L6 | Is a masked Aadhaar copy acceptable as a shared task document? | To confirm | Chat and upload warnings | [05e](05e-sensitive-data.md) |
| L7 | What are the data-breach notification deadlines and recipients? | To confirm | Breach runbook | [06 §3](06-operations.md) |
| L8 | Is automated Welfare Board reporting required, or is a manual upload acceptable? | Manual at launch | Payout reporting | [02](02-context.md) |

## For the chartered accountant

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| C1 | Is GST due on the platform fee only, or on the whole task value? | To confirm | Ledger accounts; fee levels | [01 R2](01-requirements-and-drivers.md), [05b](05b-money.md) |
| C2 | What TDS obligations apply to doer payouts? | To confirm | Payout module | [01 R2](01-requirements-and-drivers.md) |
| C3 | Monthly spend and earnings limits per account, and the spend at which requesters must verify PAN | To set | Fraud limits | [05f §4](05f-trust.md) |

## For the founder: money and pricing

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| F1 | Accept the draft fee position: small or no requester fee, 12–15% doer fee, platform absorbs gateway and welfare fees? | Yes, as drafted | First fee rule version | [05b §4](05b-money.md) |
| F2 | Who bears the gateway fee on a refunded payment? | Platform, for now | Unit economics of cancellations | [05b](05b-money.md) |
| F3 | Is the platform fee charged on the doer's share after a cancellation? | Yes | Cancellation payout | [05b](05b-money.md) |
| F4 | Minimum task value: a hard floor, or a small flat fee below a threshold? | To decide | Posting rules | [05b §4](05b-money.md) |
| F5 | Is a first-task promotion affordable, and for how long? | To decide | Promotions budget | [05b §4](05b-money.md) |
| F6 | Per-task value cap at launch | ₹25,000 | Posting rules | [05f §4](05f-trust.md) |

## For the founder: task rules

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| F7 | How long does a doer have to deliver a revision? | 48 hours | Revision deadline | [05a](05a-task-lifecycle.md) |
| F8 | Can a doer raise a dispute, or only the requester? | Either, from InProgress | Dispute rules | [05a](05a-task-lifecycle.md) |
| F9 | Does the 10% forfeit apply if the doer has not started? | Yes | Cancellation rules | [05a](05a-task-lifecycle.md) |
| F10 | After a doer no-show, how long does the requester have to set a new deadline? | 24 hours | Reopen rules | [05a](05a-task-lifecycle.md) |
| F11 | Can the requester cancel during Review? | No | State machine | [05a](05a-task-lifecycle.md) |
| F12 | Are physical errands in scope, and if so which one? | Open | Location, travel radius, maps | [01](01-requirements-and-drivers.md), [05c](05c-matching-and-feed.md) |
| F13 | Who resolves disputes when the ops person is away? | Open | Dispute operations | [00](00-discovery.md) |

## For the founder: matching and chat

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| F14 | Do doers set availability windows, or is it inferred? | Set, with an "available now" toggle | Push candidates | [05c](05c-matching-and-feed.md) |
| F15 | Applicant cap per task | 20 | Feed filter F7 | [05c](05c-matching-and-feed.md) |
| F16 | May requesters exclude new doers? | No, at launch | Cold start | [05c](05c-matching-and-feed.md) |
| F17 | May people exchange phone numbers after hiring? | Yes | Content filter | [05d](05d-realtime.md) |
| F18 | Voice notes? | Not at launch | Chat scope | [05d](05d-realtime.md) |
| F19 | Can messages be edited or deleted? | No editing; delete hides but keeps | Chat scope | [05d](05d-realtime.md) |
| F20 | Notification channels beyond push: SMS, email, WhatsApp? | Push only at launch | External systems | [00](00-discovery.md), [02](02-context.md) |
| F21 | Should tasks be checked automatically before publishing (the "could AI check tasks?" idea)? | Pattern checks at launch; AI later | Moderation | [02](02-context.md) |

## For the founder: data and trust

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| F22 | How long after a task closes are files, chat and deliverables kept? | To decide with L5 | Deletion rules | [00](00-discovery.md), [05d](05d-realtime.md), [05e](05e-sensitive-data.md) |
| F23 | Adults only (18+) for both roles? | Yes | Children's-data obligations | [05e](05e-sensitive-data.md) |
| F24 | Verify doers before their first application, not their first payout? | Yes | Onboarding flow | [05f §1](05f-trust.md) |
| F25 | Are the T2 thresholds right (10 tasks, 4.3 rating, 30 days)? | Start there | Sensitive categories | [05f](05f-trust.md) |
| F26 | Is a 48-hour delay acceptable for payout account changes? | Yes | Account security | [05f §3](05f-trust.md) |
| F27 | Who besides the ops person needs admin access, and with what limits? | Open | Ops console roles | [00](00-discovery.md) |

## For the founder: business

| # | Question | Draft answer | Blocks | Source |
| --- | --- | --- | --- | --- |
| F28 | Which reports does the business need (GMV, fill rate, retention, margin per task), and who reads them? | Weekly margin by category, at minimum | Reporting | [00](00-discovery.md), [05b](05b-money.md) |
| F29 | Referral or credit schemes that move money? | Not at launch | Promotions account | [00](00-discovery.md) |
| F30 | Accessibility needs beyond larger text? | Large text and screen-reader labels | Mobile app | [00](00-discovery.md) |

## For the team: evaluations

| # | Question | Blocks | Source |
| --- | --- | --- | --- |
| T1 | Which authentication vendor meets the six criteria? | Sprint 1 | [ADR-0006](adr/0006-managed-authentication.md) |
| T2 | Which gateway: UPI support, payouts, fees per method, webhooks, sandbox, reconciliation reports? | Payments module | [ADR-0001](adr/0001-use-a-payment-gateway.md), [05b](05b-money.md) |
| T3 | Which ID verification provider, and can it keep images? | Onboarding | [02](02-context.md), [05e](05e-sensitive-data.md) |
| T4 | Staff authentication for the ops console: a provider or company single sign-on? | Ops console | [03](03-containers.md) |
| T5 | Confirm AWS cost estimates with the pricing calculator | Budget sign-off | [06 §5](06-operations.md) |
