# Stitch UI Design System & Screen Specifications

**Stitch Project ID:** `2247593451938982513`  
**Design System:** `assets/fb6917a229014055970ff2d587c75879` (*Executive Precision*)  
**Aesthetic:** Clean, high-trust fintech meets utilitarian productivity (CRED meets Linear). Deep Slate Navy (`#0F172A`), Trust Emerald (`#10B981`), Amber Attention (`#F59E0B`), and Slate Tinted Base (`#F8FAFC`). Typography: Plus Jakarta Sans with tabular Indian Rupee (`₹`) numerals.

---

## 1. Requester Home & Quick Task Post

* **Screen ID:** `98576c555c0e42bb86c988cde460231b`
* **Title:** Delegate - Requester Home
* **Target Device:** Mobile (Expo / React Native)
* **Backlog Traceability:** [S1-12 (Role toggle)](../backlog/sprint-01-tickets.md), [S3 (Task posting flow)](../backlog/sprints.md)
* **Screenshot Preview:** [View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1VGNfeH-e-2pb64ILJytmE0UVJqmOVIpKzVHgVuClajuDZGXZVkNw2OJnLtXAe4YxcFlacXMFUodW858fZQxrLj7kPP6EZHw9D1KgXFvv613LsH4uFppTmCquRQe_In8s8eQU1MgNjbGP6c8jo7NLcd-XAOgiYHguOTQTKLVYwqW0ovzKP11Hdh9_gn6qcF7GWjecNHazdvvg1kuTYqOYU_oa6XepJb5uUaZViO05r1SVyVQgmBw-ch5A)

![View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1VGNfeH-e-2pb64ILJytmE0UVJqmOVIpKzVHgVuClajuDZGXZVkNw2OJnLtXAe4YxcFlacXMFUodW858fZQxrLj7kPP6EZHw9D1KgXFvv613LsH4uFppTmCquRQe_In8s8eQU1MgNjbGP6c8jo7NLcd-XAOgiYHguOTQTKLVYwqW0ovzKP11Hdh9_gn6qcF7GWjecNHazdvvg1kuTYqOYU_oa6XepJb5uUaZViO05r1SVyVQgmBw-ch5A)

### Key Functional Elements
1. **Header & Persistent Role Switcher:**
   - Segmented pill toggle: `[Need a Task Done] (Active, navy #0F172A)` vs `[Earn as a Doer] (Outline)`.
   - City indicator (`Bengaluru ▾`) and notifications bell.
2. **Active Task Hero Card:**
   - Real-time status badge: `In Review 🟡`.
   - Escrow lock pill: `₹500 Held in Escrow 🔒 (Safe & Protected)`.
   - Quick CTA: `Review Deliverables & Release`.
3. **Sub-90-Second Task Creation Bar:**
   - One-tap errand prompt with suggested 1-tap chips (`Insurance Claim Call ₹150`, `Travel Deal Shortlist ₹500`, `Form Filling ₹100`).
4. **8 Launch Categories Grid:**
   - Travel & Bookings, Insurance & Claims, Research & Compare, Paperwork & EPF, Data Entry, Social Media, Tech & Code, Design.
5. **Trust & Safety Banner:**
   - Explicit reassurance: *"100% Escrow Protection. Doers are paid only after you approve. Never share OTPs or passwords."*

---

## 2. Doer Task Feed & Applications

* **Screen ID:** `b988edb4b6f94789a2ca7a4dd2da0775`
* **Title:** Delegate - Doer Task Feed
* **Target Device:** Mobile
* **Backlog Traceability:** [S4-01 (Doer feed & filters)](../backlog/requirements.md), [S5-01 (Task apply & bidding)](../backlog/requirements.md)
* **Screenshot Preview:** [View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1UMAol_7bMnPD9pT3A-PlQmafZ74PFeIKtAzQKXnISHGvGLaXgaeN801SjlIYW0EwWSHWaODm0Ni7EvUGnaqPQ4dekgMeVqqr3pBESuuVltU35ZN4yBjXYYLZyy1qLjR-eMfVij9S2IBWluKf5c1Mn2c6nILPQv5I4Ehnf5ZvbzVFbTb_GeMln7_IsQ4i88ouBsykmw5SeZ8W28QVumgArRN_Ed1v8xY8c7YUURJkGCM78peLZ1rQiys7I)

![View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1UMAol_7bMnPD9pT3A-PlQmafZ74PFeIKtAzQKXnISHGvGLaXgaeN801SjlIYW0EwWSHWaODm0Ni7EvUGnaqPQ4dekgMeVqqr3pBESuuVltU35ZN4yBjXYYLZyy1qLjR-eMfVij9S2IBWluKf5c1Mn2c6nILPQv5I4Ehnf5ZvbzVFbTb_GeMln7_IsQ4i88ouBsykmw5SeZ8W28QVumgArRN_Ed1v8xY8c7YUURJkGCM78peLZ1rQiys7I)

### Key Functional Elements
1. **Doer Ledger & Role Switcher:**
   - Header greeting with verified status: `Tier 1 Verified ✓`.
   - Daily performance ledger: `Today: 2 Completed • ₹650 Earned`.
   - Role switcher with `Earn as a Doer` highlighted.
2. **Filters Bar:**
   - Horizontal scrolling pills: `All (24)`, `⚡ Quick (<3h)`, `📋 Project Tier`, `Travel & Bookings`, `Insurance`, `Min ₹200+`.
3. **Escrow-Backed Task Cards:**
   - **Quick Errand (`₹500`):** Match score (`⚡ 98% Match`), deadline countdown (`⏱ Due in 4 hrs`), `Escrow Guaranteed 🔒`, and 1-tap apply.
   - **Micro-Errand (`₹150`):** Dedicated security callout: `🛡️ Doer-Guides-Requester: No credentials or OTPs required`.
   - **Project Tier (`₹4,000 – ₹6,500`):** Pitch count, multi-day timeline, and `Submit Pitch & Quote` button.

---

## 3. Task Deliverable Review & Escrow Release

* **Screen ID:** `3e9f758a9c6e400f905a10a468bd1441`
* **Title:** Delegate - Deliverable Review & Escrow Release
* **Target Device:** Mobile
* **Backlog Traceability:** [S6-01 (Chat & Deliverables)](../backlog/requirements.md), [S7-01 (Escrow Gateway)](../backlog/requirements.md)
* **Screenshot Preview:** [View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1WQsf-8EQv-N1-k-QQM2V3xPPKIntxZAm3m4_EG3A8fCVIG6zgf57omCOdqiesS-yhccOvvIxLmpuYn7kojwbs9TzZ0W7uQ4UBUCREL3TPZlRqsua2-hQl9Zxe2KwJCinH47tWSUXJFlZU9HMzieHZVqOhVIQETWQvgsOs4qRaFIYEmNoBiHZnkT2EfDdfYDrEREuncRjjE50bh9ns_oCfLs_NqY9vAWq6HAUlYQHVcdOAkZYKje6oieg)

![View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1WQsf-8EQv-N1-k-QQM2V3xPPKIntxZAm3m4_EG3A8fCVIG6zgf57omCOdqiesS-yhccOvvIxLmpuYn7kojwbs9TzZ0W7uQ4UBUCREL3TPZlRqsua2-hQl9Zxe2KwJCinH47tWSUXJFlZU9HMzieHZVqOhVIQETWQvgsOs4qRaFIYEmNoBiHZnkT2EfDdfYDrEREuncRjjE50bh9ns_oCfLs_NqY9vAWq6HAUlYQHVcdOAkZYKje6oieg)

### Key Functional Elements
1. **Sticky Escrow Header & Lifecycle Stepper:**
   - Top banner: `₹500 Secured in Escrow 🔒 — Funds are held safely and only released when you approve`.
   - Stepper: `Matched ✓` → `In Progress ✓` → `Under Review 🟡` → `Escrow Released`.
2. **Auto-Approval SLA Countdown:**
   - `Submitted 25m ago • Auto-approves in 47h 35m if unreviewed`.
3. **Category Deliverable Card (Proof of Work):**
   - Structured comparison table with verified coupon codes, net savings, direct booking URLs, and downloadable `Goa_Hotels_Comparison_Matrix.pdf`.
4. **1:1 Audit Trail & Security Reminder:**
   - Alert: `🛡️ Safety Notice: Never share passwords, OTPs, or UPI PINs. Doer prepares, requester books.`
5. **Bottom Decision Dock:**
   - Primary: `Approve & Release ₹500 🔓` (Emerald Green `#10B981`).
   - Secondary: `Request 1 Revision`.
   - Escalation link: `Dispute or report issue to Ops • 48h Resolution SLA`.

---

## 4. Doer KYC Verification & Earnings Dashboard

* **Screen ID:** `2c72743f5dc740fda6684ab53adfd4ee`
* **Title:** Delegate - Doer KYC & Earnings Dashboard
* **Target Device:** Mobile
* **Backlog Traceability:** [S1-10 (Profiles)](../backlog/sprint-01-tickets.md), [S2-11 (KYC & DigiLocker)](../backlog/sprint-02-tickets.md), [S8-01 (Payouts)](../backlog/requirements.md)
* **Screenshot Preview:** [View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1V3sKjON5tf6t1KhyL4dCOogma5UpyCj3ajtdTjzv41Batu_KTsEGKiEr5xkT2vXuY_BT6OyM3loktISbpRK908ylBbPFHZx3mFzbpn8ubWQhuM_3w9oYvrZfVYPKVPex7hYBYZUm7yi0Na0b4vZcVBRDhAKOPN3hsQSW9VuRFDI6suOB841H_hQPGJKOz-jcjoN_yK1O8sxB8Cm0sojzlBzzxFB4XIYMHWQK5yjXrsqnvnnnXVTPRnsqE)

![View Screenshot](https://lh3.googleusercontent.com/aida/AEtjO1V3sKjON5tf6t1KhyL4dCOogma5UpyCj3ajtdTjzv41Batu_KTsEGKiEr5xkT2vXuY_BT6OyM3loktISbpRK908ylBbPFHZx3mFzbpn8ubWQhuM_3w9oYvrZfVYPKVPex7hYBYZUm7yi0Na0b4vZcVBRDhAKOPN3hsQSW9VuRFDI6suOB841H_hQPGJKOz-jcjoN_yK1O8sxB8Cm0sojzlBzzxFB4XIYMHWQK5yjXrsqnvnnnXVTPRnsqE)

### Key Functional Elements
1. **Identity & Statutory Compliance:**
   - Masked phone and verified checkmark.
   - Trust badge: `RBI & DPDP Act 2023 Compliant Identity Vault`.
2. **Tier Progression Stepper:**
   - **Tier 1 (Active):** DigiLocker Govt ID & PAN verified. Unlocks tasks up to ₹5,000 and instant UPI payouts.
   - **Tier 2 (In Progress):** Bank Penny-Drop + 10 clean tasks bar. Unlocks sensitive categories (Insurance, EPF) and ₹5,000+ Project Tier.
3. **Transparent Earnings & Statutory Breakdown:**
   - Available balance: `₹4,250`.
   - Itemized deductions: Gross fees, 15% Platform fee, and Karnataka Gig-Worker Welfare Fund (PWFVS 1% capped ₹1.50).
   - Action: `Withdraw Now via IMPS/UPI`.
4. **Reputation Dossier:**
   - 4.9★ rating (24 reviews), 98% on-time completion, 0% dispute rate.
   - Specialization badges: `Travel & Research Specialist 🏅`, `Admin & Comparison Pro 🏅`.
