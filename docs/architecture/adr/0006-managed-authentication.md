# ADR-0006: Use a managed authentication provider for phone login

- **Status:** Accepted (2026-09-28). Vendor not yet chosen.
- **Drivers:** security (attribute 2), simplicity and time to market (attribute 3); constraint
  "nobody does DevOps"; ASR-6 (progressive trust)

## Context

Users log in with a phone number and a one-time code. The code itself is simple to build, but
the surrounding work is not: delivering SMS in India (sender and template registration), rate
limits, bot protection, and defence against **SMS pumping**, where attackers trigger codes to
premium-rate numbers to run up the SMS bill.

## Options

| | A. Build login on an SMS provider | B. A managed authentication provider |
| --- | --- | --- |
| Time to build | Days for the flow; ongoing work for abuse protection | Hours to integrate |
| SMS abuse protection | Ours to build | Usually included |
| Cost | SMS only | SMS plus a per-user charge that grows with users |
| Where user data lives | Our database | The provider's, which may be outside India |
| Exit | Nothing to exit | Must export users to switch |

## Decision

**Option B.** Phone login uses a managed provider. The **vendor** is chosen later, against these
criteria, by testing a real login from a phone in India:

| Criterion | Question |
| --- | --- |
| Data location | Can phone numbers and login data stay in India? |
| Indian SMS | Does the provider handle sender and template registration, and deliver reliably? |
| Cost | What does it cost at 1,000, 10,000 and 100,000 monthly users? |
| Abuse protection | Rate limits, bot checks, SMS pumping defence? |
| Exit | Can users be exported with their phone numbers? |
| Mobile SDK | Is there a maintained React Native SDK? |

Candidates include Amazon Cognito, Firebase Authentication and Clerk. (AWS IAM is not a
candidate: it controls access to AWS itself, not an app's users.)

Whichever vendor is chosen, these rules hold:

1. **The provider handles authentication only**: proving who someone is. **Authorisation** (what
   they may do, verification tiers, ASR-6) stays in our code.
2. **We keep our own users table with our own user IDs**, mapped to the provider's ID. Nothing
   else in the system stores the provider's ID. Switching vendors changes one mapping.
3. **The API verifies the provider's token on every request** and turns it into our user ID.
4. **The ops console uses separate staff authentication** with multi-factor login, never the
   app's phone login.

## Consequences

**Good**
- Login and abuse protection ship in days, not weeks.
- Less security-critical code of our own.

**Costs and obligations**
- **A per-user cost** that grows with success; re-check it at 10,000 users.
- **A new place where personal data lives**, which the data protection work must cover.
- **A runtime dependency**: if the provider is down, nobody can log in. Existing sessions keep
  working until their tokens expire.

## What would change this

- Per-user cost exceeding the cost of running login ourselves.
- No vendor able to keep user data in India, if the lawyer confirms that is required.
