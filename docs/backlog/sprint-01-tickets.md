# Sprint 1 — Auth and profiles

**Phase 1 · Weeks 4–5 · Exit: a user can sign up by phone, fill a profile and switch roles.**

Stack assumes [ADR-0005](../decisions/ADR-0005-backend-stack.md) (Node + TypeScript, Postgres,
Retool) is `Accepted`. If it lands on Django instead, the INFRA and backend tickets change shape
but the acceptance criteria do not.

15 tickets. Estimates are engineer-days for a two-person team: `be` backend, `mob` mobile,
`ops` operator or founder.

## Blocking, start immediately

### S1-00 — DLT registration for transactional SMS
`ops` · **Est:** 1d of work, 1–2 weeks of waiting · **Traces:** CORP-4 · **Depends:** —

Register the sender ID and OTP template on the DLT portal through the SMS provider. Nothing in
S1 delivers an OTP to a real phone until this clears, so it starts on day one of the sprint and
runs in the background.

- [ ] SMS provider chosen and account opened
- [ ] Sender ID registered, OTP template approved
- [ ] One real OTP delivered to a real phone on a staging number

---

## Infrastructure

### S1-01 — Repo bootstrap and TypeScript config
`be` · **Est:** 1d · **Traces:** — · **Depends:** ADR-0005

Workspace layout for `api/`, `mobile/` and `shared/`, with the shared package holding the types
both sides use. Strict TypeScript, ESLint, Prettier, commit hooks.

- [ ] `shared/` builds and is importable from both `api/` and `mobile/`
- [ ] `strict: true`, `noUncheckedIndexedAccess: true`
- [ ] **Lint rule forbidding floats for money.** Money is `bigint` paise everywhere; the rule
      fails the build on a `number` typed as an amount (PRD §9)
- [ ] README documents how to run each workspace

### S1-02 — Postgres, migrations and local environment
`be` · **Est:** 1.5d · **Traces:** PRD §9 · **Depends:** S1-01

- [ ] `docker-compose` brings up Postgres 16 and Redis locally
- [ ] Migration tool wired, with up and down verified on an empty database
- [ ] `user` table per PRD §9: id, phone, name, photo_url, kyc_tier, status, created_at
- [ ] Seed script creates a known test user

### S1-03 — Audit log foundation
`be` · **Est:** 1.5d · **Traces:** NFR-12, DPDP-4 · **Depends:** S1-02

The audit log is built in Sprint 1, not retrofitted in Sprint 9. Every state transition that
touches money, identity or an admin action writes a row, append-only.

- [ ] `audit_log` table: actor, action, entity, entity_id, before, after, created_at
- [ ] Writes are append-only — no UPDATE or DELETE grant on the table for the app role
- [ ] A helper that any module can call in the same transaction as the change it records
- [ ] Unit test proving a rolled-back transaction writes no audit row

### S1-04 — CI pipeline
`be` · **Est:** 1d · **Traces:** PRD §10 · **Depends:** S1-01

- [ ] Lint, typecheck, test and build run on every pull request
- [ ] Pipeline fails on a type error or a lint error, not just on a test failure
- [ ] Under 5 minutes end to end

### S1-05 — Staging environment
`be` · **Est:** 2d · **Traces:** NFR-4 · **Depends:** S1-04

- [ ] API deployed to AWS ap-south-1 (data residency)
- [ ] Managed Postgres and Redis, not containers on the app host
- [ ] Secrets in a secret manager, never in the repo or the image
- [ ] Deploy from a merge to `main`, with a documented rollback

### S1-06 — Error tracking and structured logs
`be` · **Est:** 0.5d · **Traces:** PRD §8 · **Depends:** S1-05

- [ ] Sentry catching unhandled errors in API and mobile
- [ ] Structured JSON logs with a request id that survives into the mobile client's error reports
- [ ] **No phone number, OTP, KYC document reference or bank detail appears in any log line** (DPDP-3)

---

## Auth

### S1-07 — OTP request endpoint
`be` · **Est:** 2d · **Traces:** FR-1 · **Depends:** S1-02, S1-00

- [ ] `POST /auth/otp` takes an Indian mobile number, sends a 6-digit code, returns nothing about
      whether the number is registered
- [ ] Code hashed at rest, 5-minute expiry, single use
- [ ] Rate limits in Redis: 3 per number per 15 min, 10 per IP per hour, 30 per number per day
- [ ] Provider failure returns a clean error and does not leave a half-created user

### S1-08 — OTP verify, sessions and refresh
`be` · **Est:** 2d · **Traces:** FR-1 · **Depends:** S1-07

- [ ] `POST /auth/verify` creates the user on first success, returns access and refresh tokens
- [ ] Access token short-lived; refresh rotates and revokes the old one
- [ ] 5 failed attempts locks that number for 30 minutes
- [ ] Logout revokes the refresh token server-side
- [ ] Every auth event writes an audit row

### S1-09 — DPDP consent notice at signup
`be` + `mob` · **Est:** 1d · **Traces:** DPDP-2 · **Depends:** S1-08

The Data Protection Board is live and accepting complaints now, even though full compliance is
due May 2027. A consent notice at signup is cheap today and expensive to retrofit.

- [ ] Notice states what is collected, why, and for how long
- [ ] Consent recorded with a version and a timestamp against the user
- [ ] Privacy policy reachable before the OTP is requested, not after

---

## Profiles

### S1-10 — Profile model and endpoints
`be` · **Est:** 2d · **Traces:** FR-3 · **Depends:** S1-02

- [ ] `doer_profile` per PRD §9: bio, categories[], hourly_floor, languages[], badge_categories[],
      completion_rate
- [ ] `GET`/`PATCH /me/profile`; a user can only read and write their own
- [ ] `hourly_floor` stored as integer paise
- [ ] Public profile view excludes phone number and anything KYC-related

### S1-11 — Photo upload via pre-signed URL
`be` · **Est:** 1.5d · **Traces:** NFR-8, PRD §8 · **Depends:** S1-10

Files never pass through the app server — that rule starts here, not at the KYC ticket.

- [ ] Server issues a short-lived pre-signed PUT; the client uploads directly to object storage
- [ ] Content-type and size enforced (max 5 MB, images only)
- [ ] Reads go through a pre-signed GET, no public bucket

### S1-12 — Role toggle
`be` + `mob` · **Est:** 1d · **Traces:** FR-2 · **Depends:** S1-10

One account holds both roles; the toggle switches the home screen, not the account.

- [ ] `active_role` persists per device and survives a reinstall via the server
- [ ] Switching to doer with no profile prompts to complete it
- [ ] No second signup, ever

---

## Mobile

### S1-13 — App skeleton, navigation and OTP screens
`mob` · **Est:** 3d · **Traces:** FR-1, NFR-6 · **Depends:** S1-07

- [ ] Expo app with typed navigation and the shared package wired in
- [ ] Phone entry, OTP entry, resend with a visible cooldown, error states
- [ ] Tokens in secure storage, never in AsyncStorage
- [ ] Runs on Android 9; install under 30 MB (NFR-6)
- [ ] Strings externalised for later Hindi and Kannada (NFR-14)

### S1-14 — Profile editor screens
`mob` · **Est:** 2.5d · **Traces:** FR-3 · **Depends:** S1-10, S1-11, S1-13

- [ ] Edit name, photo, bio, categories, hourly floor, languages
- [ ] Photo upload with progress and a retry
- [ ] Validation errors shown inline, per field
- [ ] Font scaling to 200% does not break the layout (NFR-13)

---

## Sprint exit checklist

- [ ] A real person signs up with a real phone number on staging and edits their profile
- [ ] The role toggle switches the home screen
- [ ] CI is green on `main` and staging deploys from a merge
- [ ] An audit row exists for every signup
- [ ] No secret, phone number or token appears in a log or in the repo
