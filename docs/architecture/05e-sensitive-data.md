# 05e · Sensitive data

**Status:** Draft 1. Touches every module; enforced mainly in `identity`, `files`, `chat` and
`audit` ([04-modules.md](04-modules.md)). Sources: attribute 2 (security and privacy) and ASR-5 in
[01-requirements-and-drivers.md](01-requirements-and-drivers.md);
[ADR-0005](adr/0005-object-storage-for-files.md), [ADR-0006](adr/0006-managed-authentication.md).

> **How.** Privacy design runs in this order:
>
> 1. **Inventory.** List every kind of personal data, where it lives and who sees it. You cannot
>    protect what you have not listed, and after a breach you will be asked for exactly this list.
> 2. **Minimise.** The safest data is data you never hold. Every item you can avoid storing removes
>    a risk completely, which no control can do.
> 3. **Threat model.** For what remains, name who might misuse it and how. Each control must answer
>    a specific threat; encryption that protects against a threat you do not have is decoration.
> 4. **Control, log, delete.** Restrict access, record it, and delete on schedule.
>
> Legal points below are the founder's lawyer's to confirm. The design assumes the strict reading.

## 1. Inventory and classes

| Class | Meaning | Examples |
| --- | --- | --- |
| **Restricted** | Misuse enables identity theft or fraud | ID document images, PAN, bank account details, verification results, liveness selfies |
| **Confidential** | Personal, and may contain restricted data we cannot see | Task descriptions, attachments, chat, deliverables, phone numbers |
| **Profile** | Shown to other users by design | Display name, photo, bio, categories, ratings |
| **Operational** | Logs, metrics, analytics | Must contain **none** of the classes above |

Task attachments are **confidential by default, whatever they contain**: a requester may upload an
Aadhaar copy as a "policy document", and the system cannot tell.

| Data | Class | Lives in | Seen by | Kept for |
| --- | --- | --- | --- | --- |
| Phone number | Confidential | Auth provider; `identity` | The user; ops | Account lifetime |
| ID verification result and reference | Restricted | `identity` | Ops, with a reason | Legal retention period (to confirm) |
| ID document images | Restricted | Verification bucket, **only if the provider cannot hold them** | Ops, with a reason | As short as the law allows |
| Bank account for payouts | Restricted | **The gateway**; we keep its reference and the last 4 digits | The doer; ops (last 4 only) | Account lifetime |
| Task description | Confidential | `tasks` | Doers who can see the task; after hire, the chosen doer | Retention question |
| Attachments and deliverables | Confidential | Task files bucket | Requester; the hired doer **while the task is active** | Deleted after the task closes (period to confirm) |
| Chat | Confidential | `chat` | The two participants; ops during a dispute | Retention question |
| Ledger and audit | Operational, pseudonymous | `payments`, `audit` | Ops, finance | Years (legal) |

## 2. Minimise

The three decisions with the largest effect on risk:

1. **Let the ID verification provider keep the ID images** where it can, and store only its result
   and a reference. If it cannot, keep them in the verification bucket for the shortest period the
   law allows.
2. **Never store a full Aadhaar number.** Aadhaar has its own rules on storing numbers; the design
   keeps at most a masked number or none at all.
3. **Bank details live at the gateway.** Payouts use the gateway's saved-beneficiary reference, so
   a full account number never sits in our database.

Two more:

- **Adults only.** The data protection law treats under-18s as children, needing verifiable
  parental consent. Students are a core doer persona, so both roles require age 18+, declared at
  signup and confirmed by ID verification for doers.
- **The ledger and audit log hold IDs, not names.** They must be kept for years and cannot be
  edited. Keeping personal details out of them means a user can be erased everywhere else while
  the money records stay intact.

## 3. Threat model

| Threat | Example | Controls |
| --- | --- | --- |
| Stolen disk or backup | A database snapshot is copied | Storage encryption on the database, backups and buckets |
| A doer keeps copies | A doer saves a requester's documents to misuse later | Access ends when the task closes; downloads logged; sensitive categories need a higher trust tier ([05f](05f-trust.md)); report button |
| A curious or malicious insider | An ops account browses ID documents, or an engineer queries production | Need-to-know views; a reason recorded for every restricted access; alerts on unusual volume; no standing engineer access to production data |
| Account takeover | A SIM swap gives an attacker a doer's OTP login, and they change the payout account | Covered in [05f](05f-trust.md): payout changes are delayed and announced |
| Leaks through logs and third parties | A request body with a PAN lands in an error tracker; a push notification shows a message on a lock screen | Log redaction; scrubbed error reports; push text never contains message content |
| A compromised application server | An attacker runs code as the API | **Encryption at rest does not help here**: the application can decrypt what it can read. Minimisation, least privilege and access alerts limit the damage |

The last row is the one most designs get wrong. Storage encryption protects against lost disks,
not against your own application being taken over.

## 4. Controls

### Encryption

| Layer | Covers | Protects against |
| --- | --- | --- |
| TLS | Everything in transit | Interception |
| Storage encryption | Database, backups, both buckets | Stolen disks and snapshots |
| **A separate key for the verification bucket**, usable only by the roles that need it | ID documents | A leaked credential for the task bucket reaching ID documents |
| Field encryption with a managed key service | The few restricted fields we must keep, such as PAN | A database read by the wrong role or a leaked query result |

### Access

| Who | Can see | How it is enforced |
| --- | --- | --- |
| Requester | Their own tasks, chat and files | Ordinary authorisation in each module |
| Doer | A task's files and chat **only while hired and the task is active** | `files.getDownloadUrl` checks the task's state at the moment of each request; signed URLs last minutes |
| Ops | Task history, chat and files **during a dispute or investigation**; restricted data with a reason | The ops console asks for a reason; the reason goes to `audit` |
| Engineers | No production personal data by default | Temporary, logged access for incidents only |

**Every read of restricted data is logged** in `audit`: who, what, when and why. An alert fires when
any account reads far more than usual, such as an ops login opening 200 ID documents in an hour.

### Logs and third parties

- The logger redacts known sensitive fields (phone, PAN, message body, file names) before
  anything is written. Request and response bodies are not logged by default.
- Error reports are scrubbed the same way.
- Push notifications say "New message from Priya", never the message text: lock screens are
  public.
- **Every provider that receives personal data is listed**, with what it receives: auth provider
  (phone numbers), ID verification provider (ID documents), gateway (bank and payment details),
  push service (device tokens and notification text), storage and hosting (everything, encrypted).
  This list is what the data protection law's processor obligations are checked against.

## 5. Deletion

| What | How | Note |
| --- | --- | --- |
| Task files | Bucket lifecycle rule, a set number of days after the task closes | Enforced by storage, not by code that might not run |
| Chat and descriptions | A sweep in the worker after the retention period | Kept longer only if a dispute is open |
| ID images (if we hold them) | Verification bucket lifecycle rule | Shortest legal period |
| A user who asks to be erased | Profile anonymised, files deleted, chat content removed | Ledger and audit keep only IDs, as the law requires |
| **Backups** | Expire on their own schedule (for example 35 days) | Deleted data survives in backups until they expire; the privacy notice must say so |

**Crypto-shredding** is the option if backups must also forget quickly: each task's files and chat
are encrypted with their own key, and deleting the key makes every copy unreadable, including those
in backups. It adds key management per task, so it is recorded as an option for later, not a
launch requirement.

## 6. Obligations under the data protection law (to confirm)

| Obligation | Where it lands in the design |
| --- | --- |
| Clear notice and consent at signup, per purpose | Onboarding screens; consent records in `identity` |
| Use data only for the stated purpose | The inventory above; no reuse of chat or documents for other purposes |
| Access, correction, erasure and grievance requests | An ops workflow, plus the erasure path in section 5 |
| Breach notification to the regulator and affected users | The inventory makes scoping fast; a breach runbook in step 6 |
| Children's data | Adults only (section 2) |

## Invariants

1. No restricted or confidential data appears in logs, error reports or push notification text.
2. A doer cannot obtain a download link for a task's files unless hired and the task is active.
3. Every read of restricted data has an audit row with a reason.
4. The ledger and audit log contain no names, phone numbers or document contents.
5. No full Aadhaar number or full bank account number is stored.

## Questions for the founder and the lawyer

| Question | Why it matters |
| --- | --- |
| Can the ID verification provider retain ID images on our behalf? | Decides whether the verification bucket exists at all |
| How long must verification records and money records be kept? | Sets the restricted and ledger retention periods |
| How long after a task closes should files, chat and deliverables be kept? | Sets the lifecycle rules; disputes and repeat tasks pull in opposite directions |
| Is age 18+ acceptable for both roles? | Removes the children's-data obligations |
| Is a masked Aadhaar copy acceptable as a shared task document? | Decides whether the app warns or blocks when one is detected |
