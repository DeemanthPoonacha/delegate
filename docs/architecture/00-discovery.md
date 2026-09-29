# 00 · Discovery: the founder interview

The raw material every later document is built from. Answers are the founder's, in their words,
including the vague and contradictory ones. Regulatory statements are hearsay from the founder's
lawyer and must be verified before anything depends on them.

## The brief

> "I'm building Delegate, an app where people post small tasks they don't have time for, like
> calling their insurer, researching hotels or filling in forms. Other people with free time pick
> them up and get paid. Tasks take anywhere from 20 minutes to a few months and start at around
> ₹100. We're launching in one Indian city. I have a small team and about six months to launch."

## Round 1

**Q. Can a user switch between requester and doer? One app or two? Is onboarding the same?**
One account; people switch roles whenever they like, and many doers will also post. One app or
two is a technical decision. Requesters get in within a minute with a phone number. Doers need an
ID check before their first payout, but doer signup must take under 2 minutes.

**Q. Who is the target audience?**
Requesters: salaried professionals aged 25–40 in Bangalore; retired people who struggle with
government and insurance portals; NRIs arranging errands for parents in India. Doers: students,
homemakers on a career break, freelancers between gigs, domain experts such as insurance agents.
Almost all on Android; many doers on cheap phones.

**Q. What scale should we expect?**
"We want to be big, maybe 1 lakh users in the first year." Pressed: 300 completed tasks a week at
launch (month 6), 2,000 tasks a day hoped for by month 12. Peak hours unknown, probably evenings.

**Q. How does the money work? What gets cut, how is it received?**
The requester pays on choosing a doer. The platform holds the money until the requester approves,
then pays the doer, ideally within a day. Platform fee around 15–18%; who pays it (doer, requester
or both) is undecided. Tasks from ₹100–200 up to around ₹25,000. A lawyer mentioned an RBI rule
about holding other people's money; not yet investigated.

**Q. Do we manage payments ourselves or use Razorpay/PayU?**
The founder does not want to deal with banks. Otherwise, the architect's call.

**Q. What happens when a doer accepts a task and does not do the work?**
The doer is not paid, the requester is refunded, the doer is banned. The reverse also happens:
requesters who receive good work and refuse to approve it. One ops person handles complaints.

**Q. How do we judge the legality and legitimacy of a task?**
No illegal tasks, no impersonating the requester at a bank, nothing needing a professional licence
(legal, medical). The founder asks whether AI could check tasks.

**Q. What about privacy? Will credentials or bank details be shared?**
Never passwords, OTPs or UPI PINs: a hard line. Policy numbers and document scans (including
Aadhaar copies) will be shared and should disappear when the task ends. Doers give their bank
account for payouts.

**Q. Employ and train workers, or run a commission marketplace?**
Marketplace on commission, no employees. For the first few weeks the founder and the ops person
fulfil tasks by hand over WhatsApp to test whether people pay at all.

**Q. What is the deadline?**
Public launch in 6 months, beta users at month 4, an investor demo at month 3 that must look real.

**Q. What is the budget?**
Two engineers (one mobile, one backend who is also the architect) and one ops person.
Infrastructure under about ₹50,000 a month until the company raises.

**Q. AWS/GCP or our own infrastructure?**
No preference. $5,000 of AWS credits. The lawyer mentioned Indian data protection law.


**Q. If the app is down for an hour on a Saturday, what does it cost us? If we charge someone
twice or pay a doer twice?**
An hour down is annoying: complaints on Twitter, some tasks slip. Losing track of money or paying
twice ends the company, because it spreads through WhatsApp groups within a day. Trust matters
more than anything else.

**Q. When a task is posted, how quickly must doers see it?**
Within seconds, or another doer takes it. A student said she uninstalls if nothing appears for
two hours. Requesters of small tasks want a doer chosen within 20–30 minutes.

**Q. How does a task end?**
Post → doers apply → requester picks one and pays → doer works and submits → requester approves,
asks for one revision, or disputes. No response within 48 hours means auto-approval. Cancelling is
free before a doer is picked; after, the requester forfeits 10% to the doer. A doer who misses the
deadline loses the task, which reopens, and the requester is refunded. Ops settles disputes within
48 hours with a full or partial refund.

**Q. How are doers matched to tasks?**
Small tasks: fixed price set by the requester, doers apply, requester chooses. Bigger projects:
doers send a price and a pitch. Doers want to see only tasks in their skills; experts do not want
to scroll past ₹100 errands.

**Q. How do requester and doer communicate?**
A chat per task with photos and documents; calls maybe later. No phone numbers exchanged before a
doer is hired, to stop deals leaving the platform.

**Q. What does the team already know?**
Backend: TypeScript, Node, React, Python, Postgres, Mongo. Mobile: React Native. Nobody has built
payments. Nobody does DevOps.

**Q. What will be different in a year?**
Monthly retainers (a part-time personal assistant), recurring weekly tasks, AI help writing tasks,
more cities, Hindi and Kannada, business accounts with GST invoices, staged payments for large
projects, a secure document vault.

**Q. Can tasks be physical?**
Mostly phone and laptop work. NRIs ask for someone to queue at a government office, so maybe one
kind of physical errand. Never delivery.

**Q. What devices and networks?**
Cheap Android phones on patchy 4G. A half-written task must survive an app crash.

**Q. What do operations need?**
The ops person is not technical. She must see everything about a task and freeze a payout or ban
an account immediately.

**Q. What regulation applies?** *(lawyer's hearsay, unverified)*
Aadhaar verification is not easily available to startups, so another ID check is needed.
Karnataka's gig-worker welfare fee takes about 1% of payouts, with government reporting. The data
protection law applies. Money records must be kept for years. Tax has not been reviewed by a CA.

**Q. What does success look like?**
People coming back: completed tasks per requester per month.

## Contradictions found

Resolving these is where architecture starts.

| Contradiction | Why it matters |
| --- | --- |
| Doer signup under 2 minutes vs an ID check before payout | Points at progressive trust: verify at the moment it is needed, not at signup |
| Demo at month 3, beta at month 4, launch at month 6, two engineers | Time to market is a top driver; favour managed, familiar technology |
| "1 lakh users, we want to be big" vs ₹50k a month | Founders' numbers sound large; the real load has to be computed |
| "We hold the money" vs "I don't want to deal with banks" and the RBI rule | The requested money flow may not be legal as described |

## Still unasked

Questions no round has covered yet. Each needs a founder answer before the step that depends on it.

| Question | Needed by |
| --- | --- |
| How long must chat, deliverables and KYC documents be kept after a task closes, and who can see them? | Step 5 (data) |
| What notification channels are acceptable: push only, or SMS and WhatsApp too? Who pays for SMS? | Step 2 (context) |
| Who resolves a dispute when the ops person is away? Is there an escalation path? | Step 5 (disputes) |
| What reports does the business need: daily GMV, fill rate, cohort retention? Who reads them? | Step 3 (containers) |
| What must happen when a third party is down: gateway, KYC provider, push service? | Step 6 (operations) |
| Is there a referral or promotion scheme that moves money (credits, discounts)? | Step 5 (money) |
| Are there accessibility needs beyond the retired persona: large text, screen readers? | Step 3 (clients) |
| Will anyone other than the ops person need admin access, and with what limits? | Step 4 (modules) |
