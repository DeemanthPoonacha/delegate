# Sprint 2 — KYC and categories

**Phase 1 · Weeks 6–7 · Exit: a doer can register, pass KYC and appear in a list.**

That exit criterion is the whole of Phase 1. After this sprint there is still no task, no feed,
no money — and that is correct.

Two tickets are gated on things outside engineering: the KYC vendor contract (S2-00) and the
category list, which comes out of the Phase 0 synthesis rather than out of the PRD.

14 tickets.

## Blocking, start before the sprint opens

### S2-00 — KYC vendor contract
`ops` · **Est:** 1d of work, 2–3 weeks of waiting · **Traces:** KYC-3 · **Depends:** —

Digio or Signzy. Sandbox credentials are usually available before the contract closes — get
those first so S2-02 is not blocked by procurement.

- [ ] Vendor chosen on price per verification, DigiLocker and PAN coverage, and sandbox quality
- [ ] Sandbox credentials in hand
- [ ] Contract signed, production credentials issued
- [ ] **Confirmed in writing that the flow uses DigiLocker, not Aadhaar authentication** (KYC-1)

---

## Identity verification

### S2-01 — Identity tier model
`be` · **Est:** 1.5d · **Traces:** PRD §7, FR-4 · **Depends:** S1-02

Three tiers from PRD §7. Tier 2 cannot be reached in Phase 1 — it needs 10 clean tasks — but the
model and the gate are built now so nothing has to be retrofitted around live users.

- [ ] `kyc_tier` on user: 0 (phone), 1 (ID + liveness + name match), 2 (+ bank match, 10 clean tasks)
- [ ] Tier transitions are one-way and audit-logged
- [ ] Tier 2 criteria encoded but unreachable until task history exists
- [ ] Unit tests on every transition, including the illegal ones

### S2-02 — DigiLocker ID verification
`be` · **Est:** 3d · **Traces:** FR-4, KYC-2 · **Depends:** S2-00, S2-01

- [ ] Vendor flow initiated from the app, callback verified by signature
- [ ] Name match against the profile name, with a fuzzy threshold and a manual-review fallback
- [ ] Vendor timeout or failure leaves the user re-attemptable, never stuck mid-state
- [ ] Every attempt audit-logged with the vendor's reference, not the document contents

### S2-03 — PAN verification
`be` · **Est:** 1.5d · **Traces:** KYC-2, TAX-2 · **Depends:** S2-02

PAN is not optional: it is what makes TDS under 194-O possible later. A doer without one cannot
be paid.

- [ ] PAN validated through the vendor, name matched
- [ ] PAN stored encrypted, masked everywhere it is displayed
- [ ] A doer without a verified PAN cannot reach Tier 1

### S2-04 — Bank account penny-drop
`be` · **Est:** 2d · **Traces:** KYC-2, FR-18 · **Depends:** S2-03

- [ ] Penny-drop through the vendor; account holder name matched against the verified ID
- [ ] Account number and IFSC encrypted at rest, masked in every response and log
- [ ] Failure is re-attemptable, rate-limited to 3 per user per day
- [ ] The verified account is what Sprint 8's payouts will use — no second entry point later

### S2-05 — Encrypted document storage
`be` · **Est:** 2d · **Traces:** NFR-11, DPDP-3 · **Depends:** S1-11

- [ ] AES-256 at rest for KYC documents and vendor payloads
- [ ] Access only through short-lived pre-signed URLs; no document passes through the app server
- [ ] Every access to a KYC document writes an audit row naming who read it
- [ ] Retention rule documented: what is deleted, when, and what the vendor keeps instead

### S2-06 — Verified badge and tier gating middleware
`be` · **Est:** 1.5d · **Traces:** FR-4 · **Depends:** S2-01

- [ ] A single middleware enforces a minimum tier per route — the gate lives in one place
- [ ] Verified badge exposed on the public profile; unverified profiles say so plainly
- [ ] A Tier 0 user hitting a Tier 1 route gets a clear "verify to continue", not a 403

---

## Categories

### S2-07 — Category taxonomy schema
`be` · **Est:** 1d · **Traces:** FR-5, PRD §9 · **Depends:** S1-02

- [ ] `category` per PRD §9: id, name, parent_id, deliverable_template_id, requires_kyc_tier
- [ ] Two levels only — category and sub-category
- [ ] `requires_kyc_tier` is what gates sensitive categories to Tier 2
- [ ] Categories are data, not an enum in code; adding one is a migration, not a release

### S2-08 — Seed the launch categories
`ops` + `be` · **Est:** 0.5d · **Traces:** FR-5, A7 · **Depends:** S2-07, **Phase 0 synthesis**

**Do not seed the PRD's 8 categories from the PRD.** Seed the top 5 that appeared in real Phase 0
demand. If the synthesis is not written, this ticket waits — that is the point of the phase.

- [ ] Top 5 categories from the synthesis, in the requesters' own words
- [ ] Sensitive categories (insurance, government paperwork) marked `requires_kyc_tier = 2`
- [ ] Categories that did not appear in Phase 0 are left out, not seeded "for later"

---

## Ops console

### S2-09 — Retool connection and read-only views
`be` · **Est:** 1.5d · **Traces:** FR-27 · **Depends:** S1-05

- [ ] Retool connected to staging over a read-only database role
- [ ] User list with tier, status and signup date; searchable by phone
- [ ] Doer list — **this is the list in the Phase 1 exit criterion**
- [ ] No write access from Retool yet; writes arrive in Sprint 9

### S2-10 — KYC review queue
`be` + `ops` · **Est:** 2d · **Traces:** FR-27, FR-4 · **Depends:** S2-02, S2-09

Name-match failures and vendor ambiguities need a human. Without this, a failed match is a dead
end for a real doer.

- [ ] Queue of KYC attempts needing review, with the vendor's reason
- [ ] Operator can approve or reject with a required note
- [ ] Every decision audit-logged against the operator, not against "system"
- [ ] The doer is notified either way, with a reason they can act on

---

## Mobile

### S2-11 — KYC flow screens
`mob` · **Est:** 3d · **Traces:** FR-4 · **Depends:** S2-02, S2-04

- [ ] Explains what is collected and why *before* the flow starts (DPDP-2)
- [ ] DigiLocker handoff and return, with the app surviving being backgrounded mid-flow
- [ ] PAN and bank entry with inline validation
- [ ] Pending, failed and under-review states are all designed — the failure path is the common one
- [ ] No KYC document is ever cached on the device

### S2-12 — Profile completeness and verification prompts
`mob` · **Est:** 1.5d · **Traces:** FR-3, FR-4 · **Depends:** S2-06, S2-11

- [ ] Doer home shows what is missing before they can take paid work
- [ ] One clear call to action, not a checklist of six
- [ ] Verified badge visible on their own profile once earned

---

## Hardening

### S2-13 — PII handling review
`be` · **Est:** 1d · **Traces:** DPDP-3, DPDP-5 · **Depends:** S2-05

A deliberate pass before Phase 2 doubles the surface area. Cheap now, expensive in March.

- [ ] Grep the codebase and the logs for PAN, account number, phone and document references
- [ ] Every one of them masked, encrypted or removed
- [ ] Retention and deletion documented per data type, including Phase 0 interview material
- [ ] A written list of every third party that receives user data, and what they get

---

## Sprint exit checklist — this is the Phase 1 gate

- [ ] A real doer signs up, completes DigiLocker + PAN + penny-drop, and reaches Tier 1
- [ ] That doer appears in the ops console doer list
- [ ] A failed name match lands in the review queue and an operator resolves it
- [ ] Categories are seeded from the Phase 0 synthesis, not from the PRD
- [ ] No KYC document or bank detail is readable in any log, response or Retool view
