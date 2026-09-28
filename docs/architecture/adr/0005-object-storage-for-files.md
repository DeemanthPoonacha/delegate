# ADR-0005: Files live in private object storage, uploaded and downloaded directly

- **Status:** Accepted (2026-09-28)
- **Drivers:** security and privacy (attribute 2), simplicity (attribute 3); clients on patchy 4G;
  ASR-5; capacity finding "retention decides storage"

## Context

Tasks carry photos, scans and deliverables, and doers upload ID documents for verification. The
capacity estimate puts task files at about 6 GB a day, and the founder wants shared documents
gone after a task ends. ID documents are the most sensitive data Delegate holds.

## Options

| | A. Files in the database | B. Object storage, through the API | C. Object storage, direct with signed URLs |
| --- | --- | --- | --- |
| Database size and backups | Grows by terabytes; backups slow | Unaffected | Unaffected |
| API load | Every byte through the API | Every byte through the API | None: the phone talks to storage directly |
| Retries on patchy 4G | Tie up API connections | Tie up API connections | Handled by storage |
| Access control | In our code | In our code | In our code: a URL is issued only after a permission check, and expires in minutes |

## Decision

**Option C**, in object storage such as Amazon S3:

- **Two private buckets**: task files, and verification documents. Nothing is ever public.
- **Uploads**: the app asks the API for an upload URL; the API checks permission, records the
  file as pending and returns a signed URL valid for a few minutes. The app uploads directly and
  confirms.
- **Downloads**: the same pattern, with every issued URL logged for verification documents.
- **Encryption at rest** on both buckets, with stricter key access and access logging on the
  verification bucket.
- **Deletion by policy**: lifecycle rules delete task files a set number of days after the task
  closes. The period is still an open question for the founder.

## Consequences

**Good**
- The API never carries file bytes; the database stays small.
- Deletion is enforced by storage policy, not by code someone might forget to run.

**Costs and obligations**
- **A file record and its object can disagree**: an upload that never completes, or a record for
  a missing object. A cleanup sweep removes pending records older than a day.
- **Uploaded content is untrusted.** Check file type and size when confirming the upload; malware
  scanning is a later decision.
- **Signed URLs can be shared while valid**, so they are kept short-lived.

## What would change this

- A regulatory requirement for how identity documents are stored, for example by the ID
  verification provider rather than by us. That would remove the verification bucket entirely.
