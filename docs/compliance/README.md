# Compliance tracker

Obligations that carry a deadline, a filing or a licence. Items marked **PRD** come from the
source document and its sources; items marked **added** were not in the PRD and need someone to
confirm they apply.

Status values: `not-started` · `in-progress` · `blocked` · `done` · `n/a`.
Owner is the operator unless a decision or an integration makes it an engineer's.

## Money and payments

| ID | Obligation | Trigger | Deadline | Owner | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
| PAY-1 | Settle payment architecture with a payments lawyer | Before Sprint 7 | Lawyer engaged by Sprint 3 | Founder | not-started | PRD, [ADR-0001](../decisions/ADR-0001-payment-architecture.md) |
| PAY-2 | Do not use PA split settlement to individual doers | Always | — | Engineer | not-started | PRD ([Ikigai Law](https://www.ikigailaw.com/article/639/rbi-rewrites-the-payment-aggregator-rulebook)) |
| PAY-3 | Customer funds never in a platform-owned operating account (NFR-10) | Always | — | Engineer | not-started | PRD |
| PAY-4 | Onboard with an RBI-authorised aggregator; full merchant KYC and contract | Sprint 7 | Lead time ~4–6 weeks | Founder | not-started | PRD |
| PAY-5 | Nightly escrow reconciliation against the gateway | Sprint 7 | — | Engineer | not-started | PRD §9 |
| PAY-6 | PCI-DSS scope avoided: no card data stored or transiting our servers (NFR-8) | Always | — | Engineer | not-started | PRD |

## Gig work — Karnataka

Applies from the first payout if [ADR-0003](../decisions/ADR-0003-launch-city.md) lands on Bangalore.

| ID | Obligation | Trigger | Deadline | Owner | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
| COMP-1 | Register with the Karnataka Gig Workers Welfare Board | First payout | Within 45 days | Operator | not-started | PRD ([United Consultancy](https://unitedconsultancy.com/gig-workers-welfare-fee-karnataka-government-order-13-02-2026/)) |
| COMP-2 | Maintain a machine-readable worker database | Registration | Ongoing | Engineer | not-started | PRD |
| COMP-3 | Deduct and remit the welfare fee: min 1% of payout, capped ₹1.50 per transaction for professional services | Every payout | Quarterly remittance | Engineer + operator | not-started | PRD ([Karma Management](https://karmamgmt.com/index.php/blog/karnataka-gig-workers-welfare-fee-2026-compliance-guide)) |
| COMP-4 | Map payout reporting to the state PWFVS system | Sprint 8 | Quarterly filing | Engineer | not-started | PRD |
| COMP-5 | Watch the constitutional challenge; HC declined a stay in July 2026 | Ongoing | Review quarterly | Founder | not-started | PRD ([Medianama](https://www.medianama.com/2026/07/223-karnataka-hc-gig-workers-act-welfare-fee/)) |
| COMP-6 | Keep the levy rate configurable per state, not hard-coded | Sprint 8 | — | Engineer | not-started | added |

## Data protection

| ID | Obligation | Trigger | Deadline | Owner | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
| DPDP-1 | Full DPDP compliance (Rules notified 13 Nov 2025) | — | 13 May 2027 | Founder | not-started | PRD NFR-9 |
| DPDP-2 | Consent notice, purpose limitation, and a grievance route — the Board is live and complaints can be filed now | Before first real user | Phase 0 | Founder | not-started | PRD NFR-9 |
| DPDP-3 | AES-256 at rest for KYC documents and vault entries; TLS 1.3 in transit | Sprint 2 | — | Engineer | not-started | PRD NFR-11 |
| DPDP-4 | Immutable audit log of escrow, dispute and admin actions, retained 7 years | Sprint 9 | — | Engineer | not-started | PRD NFR-12 |
| DPDP-5 | Data deletion and retention policy, including Phase 0 interview recordings | Phase 0 | Before first interview | Operator | not-started | added |

## Identity

| ID | Obligation | Trigger | Deadline | Owner | Status | Source |
| --- | --- | --- | --- | --- | --- | --- |
| KYC-1 | Do **not** assume Aadhaar authentication; it needs a ministry application and MeitY clearance | Always | — | Founder | not-started | PRD ([Khaitan & Co](https://www.khaitanco.com/thought-leadership/Aadhaar-authentication-for-private-entities)) |
| KYC-2 | DigiLocker ID + PAN + bank penny-drop as the launch verification path | Sprint 2 | — | Engineer | not-started | PRD |
| KYC-3 | Contract with a KYC vendor (Digio or Signzy) | Sprint 2 | Lead time ~2–3 weeks | Founder | not-started | PRD |

## Tax and corporate — not in the PRD

These are gaps. Each one needs a chartered accountant to confirm applicability before the
unit economics in PRD §11 can be trusted.

| ID | Obligation | Why it matters | Owner | Status | Source |
| --- | --- | --- | --- | --- | --- |
| TAX-1 | GST treatment: commission-only vs full task value under merchant-of-record | Could erase the ₹21 net on a ₹150 task | Founder + CA | not-started | added |
| TAX-2 | TDS under section 194-O on payments to doers | Platform becomes the deductor; monthly filing | Founder + CA | not-started | added |
| TAX-3 | GST registration and invoicing for the platform fee | Required before revenue | Founder + CA | not-started | added |
| CORP-1 | Entity incorporation, PAN, TAN, current account | Precondition for PAY-4 | Founder | not-started | added |
| CORP-2 | Terms of service, privacy policy, doer agreement | Required before the closed beta | Founder + lawyer | not-started | added |
| CORP-3 | Intermediary status and due diligence under the IT Act / IT Rules | Determines liability for user-posted tasks | Founder + lawyer | not-started | added |
| CORP-4 | DLT registration for transactional SMS (phone OTP, FR-1) | Blocks OTP delivery at scale | Engineer | not-started | added |
| CORP-5 | Play Store policy review: marketplace, payments and user-generated content | Blocks the Phase 5 release | Engineer | not-started | added |

## Review cadence

Re-read this file at the start of every phase and at every ADR acceptance. Update `Status`
in place; do not delete rows — a `n/a` with a reason is more useful later than a missing line.
