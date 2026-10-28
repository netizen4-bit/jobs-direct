---
name: osint-hiring-bypass
description: Double-Tap Application Strategy combining Direct-ATS dorking, crt.sh career subdomain enumeration, Schema.org metadata, and zero-bounce SMTP verification to reach hiring managers directly.
version: 2.0.0
---

# B2B OSINT Hiring Outreach & Double-Tap Application Strategy

This skill guides the agent through the **Double-Tap Application Strategy**: bypassing crowded aggregator job boards to discover direct employer ATS postings, conducting corporate OSINT reconnaissance, discovering decision-makers, and executing deliverability-verified peer outreach.

---

## 🚀 The Double-Tap Application Strategy

Applying exclusively through massive job boards (LinkedIn, Indeed) places candidates into applicant queues with 500+ competing submissions. The **Double-Tap Strategy** flips the odds:

```
[Target Search] ──► Direct Enterprise ATS Dorking (Greenhouse / Lever / Ashby)
                             │
                             ▼
[ATS Screen]    ──► Deterministic 4-Tier ATS Fit Pass (Score >= 60)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
      [Tap 1: ATS]                     [Tap 2: OSINT]
Direct ATS Submission             `osint_employer_recon`
(Tailored Resume + Answers)       • crt.sh Subdomain Enumeration
            │                     • MX Mail Fingerprinting
            │                     • Schema.org Identity Scrape
            │                                 │
            │                                 ▼
            │                     `enrich_hiring_contacts`
            │                     • Cloudflare XOR De-obfuscation
            │                     • Executive Email Permutations
            │                     • Port-25 Zero-Bounce SMTP Probe
            │                                 │
            └────────────────┬────────────────┘
                             ▼
              [Verified Direct HM Outreach]
        250-Word Single-Anchor Email to Hiring Manager
```

---

## 🔍 Phase 1: Direct Enterprise ATS Dorking (`portal="direct_ats"`)

Aggregators display expired, re-posted, or ghost jobs. Enterprise ATS boards represent active corporate hiring requisitions.

### Tool Call:
```python
search_jobs(query="Engineering Manager", portal="direct_ats", jobage_days=14)
```

### Targeted ATS Platforms:
* **Greenhouse:** `site:boards.greenhouse.io <query>`
* **Lever:** `site:jobs.lever.co <query>`
* **Ashby:** `site:jobs.ashbyhq.com <query>`
* **Workable:** `site:apply.workable.com <query>`
* **SmartRecruiters:** `site:jobs.smartrecruiters.com <query>`

---

## 🕵️ Phase 2: Employer OSINT Reconnaissance (`osint_employer_recon`)

Before contacting any team member, map the employer's digital footprint without expensive data broker APIs.

### Tool Call:
```python
osint_employer_recon(domain="company.com")
```

### Intelligence Gathered:
1. **Hidden Subdomain Enumeration via SSL Certificate Transparency (`crt.sh`):**
   - Discovers unlisted portal subdomains: `careers.*`, `talent.*`, `hr.*`, `apply.*`, `workday.*`, `greenhouse.*`.
2. **Mail Infrastructure Fingerprinting:**
   - Analyzes DNS MX records to determine deliverability characteristics:
     - **Google Workspace (`aspmx.l.google.com`):** Standard corporate inbox structure.
     - **Microsoft 365 (`protection.outlook.com`):** Strict spam filtering and enterprise firewalls.
     - **Zoho / Proton / Self-Hosted:** Custom deliverability routing.
3. **Schema.org Structured Metadata:**
   - Extracts legal company entity name, official corporate telephone, and verified social media channels.

---

## ✉️ Phase 3: Contact Discovery & Zero-Bounce Verification (`enrich_hiring_contacts`)

Never send cold outreach to unverified guesses. Bounced emails permanently damage your sending domain reputation.

### Tool Call:
```python
enrich_hiring_contacts(
    domain="company.com",
    hiring_manager_first_name="Jane",
    hiring_manager_last_name="Doe"
)
```

### Verification Pipeline:
1. **Cloudflare XOR De-obfuscator:**
   - Decodes emails hidden behind Cloudflare protection (`data-cfemail` and `/cdn-cgi/l/email-protection#`) from `/careers`, `/team`, and `/contact` pages.
2. **Executive Email Permutation Engine:**
   - Generates standard enterprise patterns:
     `jane.doe@company.com`, `j.doe@company.com`, `jane@company.com`, `doe.jane@company.com`, `jdoe@company.com`, `janedoe@company.com`.
3. **Talent & Department Aliases:**
   - Tests `careers@`, `talent@`, `recruiting@`, `hr@`, `jobs@`, `people@`.
4. **Port-25 Zero-Bounce SMTP Probe:**
   - Connects to primary MX host on port 25.
   - **Catch-All Bounce Defense:** Probes server with a random UUID address (`probe-xxxx@company.com`). If accepted (250), flags domain as `CATCH_ALL` to prevent false confidence.
   - **Recipient Verification:** Tests candidate addresses with `RCPT TO:<candidate@company.com>` without sending actual messages (`RSET` -> `QUIT`).
   - Returns verified deliverability statuses: `VALID`, `INVALID`, `CATCH_ALL`, `GREYLISTED`, `ERROR`.
   - Appends verified entries to `output/hiring_contacts_output.csv`.

---

## 🎯 Phase 4: Executing the Double-Tap Outreach

Once the candidate passes the 4-Tier ATS Gate ($\ge 60$) and contacts are verified:

1. **Tap 1 (Direct ATS Application):**
   - Submit the tailored STAR resume and screening form answers via the direct ATS URL.
2. **Tap 2 (Peer-Level Outreach within 24 Hours):**
   - Send the 250-word single-anchor email directly to the verified Hiring Manager address.
   - Example message framing:
     > *"Hi Jane, I just submitted my application for the Engineering Manager role through your Ashby portal. Rather than waiting in the queue, I wanted to share one specific metric: recently scaled our pipeline throughput by 35% using the exact CI/CD patterns outlined in your roadmap. Would love 5 minutes to share how this applies to your upcoming sprint."*
3. **Application Tracking:**
   - Log the outreach in `track_application(action="add", ...)`.

---

## 🛡️ Anti-Ban & Deliverability Guardrails

* **Cookieless Operation:** 100% public web and direct ATS discovery—never requires logging into personal accounts or using session scraping cookies.
* **Catch-All Detection:** Flags catch-all domains to prevent sending unverified emails that trigger spam bounces.
* **Support Banner Compliance:** Automatically formats CSV records with support and custom pipeline notices.
