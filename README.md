# JobsDirect-MCP v2.0

A local, agentic Model Context Protocol (MCP) framework and autonomous career intelligence engine that combines **multi-portal & direct-ATS job discovery**, a **deterministic 4-tier ATS fit evaluation gate**, **5-stage truthful positioning** (Harish Kumar methodology), and **B2B OSINT hiring manager reconnaissance with zero-bounce port-25 SMTP verification** — all running locally with zero recurring SaaS subscriptions and slashing LLM context token consumption by over **82%**.

JobsDirect connects your AI coding assistant (**Antigravity**, **Claude Desktop**, **Cursor**) or local **Ollama** agents directly to live enterprise hiring pipelines. It bypasses crowded aggregators by dorking direct ATS boards (Greenhouse, Lever, Ashby, Workable, SmartRecruiters), detects expired or closed postings automatically in English and Turkish, scores candidate-job compatibility through a dynamic 4-tier weighted ATS gate, tailors high-agency STAR resumes without hallucinated metrics, formats 250-word single-anchor cover letters, and conducts zero-cost OSINT reconnaissance to uncover verified Hiring Manager contacts for high-conversion double-tap applications.

**Built for Immediate ROI:** JobsDirect replaces **$40–$150/month career, resume-tailoring, and email enrichment SaaS tools** (such as Teal, Jobscan, Hunter, or Apollo) by executing live ATS discovery, deterministic scoring, and zero-bounce email verification locally on your machine at zero recurring cost.

---

## ⚡ Token Effectiveness & Benchmark

AI coding agents running unconstrained web-scraping and resume-tailoring loops quickly suffer from **context window exhaustion** (ingesting thousands of tokens of noisy HTML, broken links, expired job boards, and hallucinated experience guesses).

JobsDirect-MCP v2.0 pairs native FastMCP backend tools with structured **Agent Skills** (`hybrid-ats-positioning` and `osint-hiring-bypass`) to enforce deterministic filtering before generation:

### 4-Phase Application Cycle Benchmark

| Phase | Unconstrained Scraping Loop | JobsDirect-MCP v2.0 + Skills | Token Savings |
|---|---|---|---|
| **1. Multi-Portal & ATS Discovery** | **~1,400 tokens**<br>*(Ingests raw DOM trees, tracking pixels, expired listings)* | **~300 tokens**<br>*(Direct ATS dorking; pre-filtered for active listings)* | **-78.6%** |
| **2. 4-Tier ATS Fit Scoring** | **~1,800 tokens**<br>*(Lengthy LLM qualitative guessing on fit and domain)* | **~220 tokens**<br>*(Deterministic 4-Tier math; instant 7-branch verdict)* | **-87.8%** |
| **3. 5-Stage Hybrid Positioning** | **~2,400 tokens**<br>*(Hallucinates fluffy bullet points and long cover letters)* | **~480 tokens**<br>*(Exact JD keyword matrix + 250-word single-anchor letter)* | **-80.0%** |
| **4. Hiring Manager OSINT & Verification** | **~1,400 tokens**<br>*(Ingests catch-all email guesses and raw page text)* | **~240 tokens**<br>*(Local crt.sh enum + zero-bounce port-25 SMTP verification)* | **-82.9%** |
| **Total Context Spent** | **~7,000 tokens** | **~1,240 tokens** | **~82.3% Total Reduction** |

---

## 📊 Industry Competitive Analysis

How JobsDirect-MCP v2.0 compares across the industry landscape:

| Capability / Feature | Browser Auto-Clicker Bots (Easy-Apply Spammers) | Basic Keyword / Vector Resume Matchers | Cloud Career & B2B Email SaaS ($50–$150/mo) | JobsDirect-MCP v2.0 (Local Hybrid Engine) |
|---|---|---|---|---|
| **1. Account Safety & Anti-Ban Protection** | ❌ **High Risk:** Browser automation with session cookies frequently triggers permanent LinkedIn bans. | ⚠️ **Neutral:** Static file processing; does not interact with live platforms. | ⚠️ **Variable:** Cloud-hosted scrapers often hit rate limits and captcha blocks. | ✅ **100% Cookieless:** Zero login credentials or session cookies required; queries public endpoints & direct ATS boards. |
| **2. Cross-Industry False Positive Prevention** | ❌ **None:** Blasts applications indiscriminately to any matching job title. | ❌ **High False Positives:** Flags mismatches because unrelated industries share generic terms ("Agile", "KPIs"). | ⚠️ **Basic:** Relies on generic industry tags from paid databases. | ✅ **Deterministic 40% Tier 1 Engine:** Dynamic industry taxonomy isolates true domain footprint and prevents cross-vertical mismatch. |
| **3. Hard Qualification, Clearance & Language Gates** | ❌ **Ignored:** Ingests rejection emails after applying to roles requiring security clearances or foreign languages. | ❌ **Ignored:** Vector proximity scores high even when candidate lacks mandatory degree or years of experience. | ⚠️ **Partial:** Manual user filtering required; no automated gate logic. | ✅ **Strict 7-Branch Verdict Tree:** Enforces degree hierarchy, YoE thresholds, security clearances, and multi-language requirements before tailoring. |
| **4. Expired & Closed Job Filtering** | ❌ **None:** Continues spamming applications to closed and dead listings. | ❌ **None:** Matches resumes against cached or dead job descriptions. | ⚠️ **Delayed:** Aggregator feeds refresh on hours-to-days delay, showing ghost positions. | ✅ **Real-Time Closure Engine:** Regex and deadline date parsing in English & Turkish stops wasted token burn immediately. |
| **5. Resume & Cover Letter Positioning** | ❌ **None:** Submits generic static PDF to every opening. | ❌ **Hallucinated Fluff:** Generates fabricated metrics, projects, and buzzword-stuffed walls of text. | ⚠️ **Template-Based:** Rigid web forms and generic AI rewriters that sound robotic. | ✅ **5-Stage Truthful Positioning:** 100% grounded in real CV metrics; Exact JD Keyword Mirroring Matrix + 250-word single-anchor cover letter. |
| **6. Hidden ATS Board Discovery** | ❌ **Aggregator-Only:** Trapped inside crowded aggregator job boards with 500+ applicants per post. | ❌ **None:** No discovery mechanisms. | ⚠️ **Limited:** Aggregates mainstream feeds; requires manual portal navigation. | ✅ **Direct ATS Dorking:** Dorks Greenhouse, Lever, Ashby, Workable, and SmartRecruiters plus `crt.sh` career subdomain enumeration. |
| **7. Hiring Manager Contact Discovery & Verification** | ❌ **None:** Zero contact enrichment capability. | ❌ **None:** Document matcher only. | ⚠️ **Paywalled:** Charges $40–$150/mo for monthly credit pools; unverified guesses cause domain bounces. | ✅ **Zero-Cost OSINT & Port-25 SMTP:** Cloudflare XOR decoding + executive permutation + local port-25 zero-bounce verification with catch-all bounce defense. |
| **8. Cost & Data Privacy** | ⚠️ **Subscription / Freeware:** High ban liability; stores credentials in plain text. | ⚠️ **Token Heavy:** Ingests thousands of unconstrained LLM tokens per document. | ❌ **Expensive ($600–$1,800/yr):** Proprietary lock-in; candidate resumes uploaded to commercial third-party clouds. | ✅ **100% Free & Open-Source:** Runs locally on your machine with 82% token savings; candidate data never leaves local storage. |

---

## 🧠 The Dynamic 4-Tier ATS Evaluation Engine & 5-Stage Hybrid Pipeline

```
                              TARGET JOB POSTING
                                       │
                                       ▼
 ┌───────────────────────────────────────────────────────────────────────────┐
 │               STEP 0: DETERMINISTIC 4-TIER ATS EVALUATION                 │
 ├───────────────────────────────────────────────────────────────────────────┤
 │  Tier 1: Industry / Domain Affinity (40% Weight, Max 40 pts)              │
 │          • Analyzes candidate footprint across 9 Industry Taxonomies      │
 │          • Prevents functional false-positives (e.g. Fintech vs Heavy Ind)│
 │                                                                           │
 │  Tier 2: Minimum Qualifications & Experience Gate (20% Weight, Max 20 pts)│
 │          • Degree Hierarchy Gate: PhD (3) > Master (2) > Bachelor (1)     │
 │          • Minimum YoE Regex Check: candidate_yoe / req_yoe ratio         │
 │                                                                           │
 │  Tier 3: Functional & Technical Core Skills (30% Weight, Max 30 pts)      │
 │          • Dynamic intersection of tools, frameworks, and methodologies   │
 │          • Tracks matched_skills vs. missing_skills                       │
 │                                                                           │
 │  Tier 4: Practical Logistics & Language Gate (10% Weight + Hard Gates)    │
 │          • Security clearance / citizenship verification check            │
 │          • Mandatory working language check (with Turkish normalization)   │
 └─────────────────────────────────────┬─────────────────────────────────────┘
                                       │
                         7-Branch Verdict Decision Tree
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 ▼                                           ▼
      [DISQUALIFICATION GATES]                    [QUALIFIED CANDIDATES]
      • CLOSED_OR_EXPIRED (Listing dead)          • STRONG_MATCH (Score >= 80)
      • REJECTED (Language mismatch)              • MODERATE_MATCH (Score 60-79)
      • POOR_DOMAIN_FIT (Domain < 0.20)                      │
                 │                                           ▼
           🛑 STOP PIPELINE               ┌─────────────────────────────────────┐
           (Zero token burn)              │   5-STAGE TRUTHFUL POSITIONING      │
                                          ├─────────────────────────────────────┤
                                          │ 1. Recruiter Persona Locking        │
                                          │ 2. Exact JD Keyword Mirroring Matrix│
                                          │ 3. 250-Word Single-Anchor Letter    │
                                          │ 4. LinkedIn Boolean Keyword Bank    │
                                          │ 5. 10-Question STAR Interview Prep  │
                                          └──────────────────┬──────────────────┘
                                                             │
                                                             ▼
                                          ┌─────────────────────────────────────┐
                                          │      DOUBLE-TAP OSINT OUTREACH      │
                                          ├─────────────────────────────────────┤
                                          │ • Direct Enterprise ATS Submission  │
                                          │ • crt.sh Career Subdomain Discovery │
                                          │ • Cloudflare XOR Email Decoding     │
                                          │ • Port-25 Zero-Bounce SMTP Probe    │
                                          │ • Direct Hiring Manager Email Pitch │
                                          └─────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
jobs-direct/
├── skills/
│   ├── hybrid-ats-positioning/
│   │   └── SKILL.md             # 4-Tier decision gate & Harish Kumar 5-stage truthful positioning protocol
│   └── osint-hiring-bypass/
│       └── SKILL.md             # Double-tap outreach: direct-ATS dorking, crt.sh enum & zero-bounce SMTP
├── output/                      # Auto-created portable directory for verified hiring contacts CSV
├── jobs_direct.py               # FastMCP Server exposing 16 core tools (Search, Fit, Tailor, OSINT, SMTP, Profile Matching, Disk Persistence)
├── agent.py                     # Autonomous interactive agent runner for local LLMs (Ollama / Qwen)
├── requirements.txt             # Core Python dependencies
├── CODE_OF_CONDUCT.md           # Community guidelines
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── SECURITY.md                  # Security policy
└── README.md                    # Project documentation, benchmarks & competitive analysis
```

---

## 🛠️ MCP Tools Reference (Full 16-Tool Suite)

JobsDirect-MCP v2.0 exposes **16 native MCP tools** designed for end-to-end career intelligence and automated job matching:

### 🚀 1. `find_jobs_from_profile` *(Automated Profile-to-Job Matching Engine)*
* **Input:** `profile_url` (str, e.g. LinkedIn, GitHub, or portfolio URL), `location` (str, default "Remote"), `portal` (str, default "all"), `limit` (int, default 10)
* **What it does:** The ultimate one-click career automation tool. Takes a candidate's profile URL, automatically scrapes and extracts their career footprint and domain via our cookieless 2-tier waterfall + DDGS public snippet engine, queries direct enterprise ATS boards & aggregators, executes deterministic 4-Tier ATS scoring on all found opportunities, and outputs a ranked leaderboard of matched positions with direct application URLs, while **automatically creating a dedicated results folder** (on Desktop and in `output/`) containing `job_matches.csv`, `job_matches_report.md`, `job_matches_report.docx`, and JSON snapshots.

### 🌐 2. `scrape_profile_or_page` *(Cookieless Web & Social Scraper)*
* **Input:** `url` (str)
* **What it does:** Scrapes candidate profile pages, portfolio sites, GitHub repositories, or company web pages using a high-performance 2-tier waterfall (fast HTTP with desktop browser headers + Playwright headless fallback). Features a **smart DDGS public snippet fallback** for LinkedIn authwalls, extracting public bio, role titles, work highlights, Cloudflare XOR-obfuscated emails, phone numbers, and social links completely cookieless with zero account ban risks.

### 3. `search_jobs`
* **Input:** `query` (str), `location` (str, default "Remote"), `portal` (str, default "all"), `remote` (str), `jobage_days` (int, default 14), `limit` (int, default 10)
* **What it does:** Searches open postings across direct enterprise ATS boards (`boards.greenhouse.io`, `jobs.lever.co`, `jobs.ashbyhq.com`, `apply.workable.com`, `jobs.smartrecruiters.com`) and major aggregators (LinkedIn, Himalayas, Kariyer.net, Remote.co, CareerHound, HiredChina) with automated English & Turkish expiration pre-filtering.

### 4. `get_job_details`
* **Input:** `job_id_or_url` (str), `portal` (str, default "auto")
* **What it does:** Fetches complete job requirements, seniority criteria, active expiration status, and extracts plaintext and Cloudflare XOR-obfuscated recruiter emails directly from the listing HTML.

### 5. `evaluate_job_fit`
* **Input:** `candidate_profile` (str), `job_description` (str), `candidate_citizenship` (optional str), `candidate_languages` (optional list[str])
* **What it does:** Executes the deterministic 4-Tier ATS Evaluation Engine (40% Domain Affinity, 20% Qualifications Gate, 30% Core Skills, 10% Logistics/Language Gate). Returns numerical scores and routes through the 7-Branch Verdict Decision Tree.

### 6. `tailor_resume`
* **Input:** `candidate_cv` (str), `job_description` (str), `target_role` (optional str), `target_company` (optional str)
* **What it does:** Stage 1 & 2 Positioning: Adopts the Senior Recruiter persona for the detected Tier 1 domain, extracts real quantified lines from the candidate's CV (never invents metrics), and generates an **Exact JD Keyword Mirroring Matrix**, high-agency action-verb STAR bullets, and an **Honest Bridge Strategy** for missing skills.

### 7. `generate_cover_letter`
* **Input:** `candidate_profile` (str), `job_description` (str), `company_name` (str), `job_title` (str), `hiring_manager` (optional str)
* **What it does:** Stage 3 Positioning: Generates a high-converting cover letter under a strict **250-word limit** in a confident peer-level problem-solving tone, anchored to **exactly one verified quantified achievement** mapped to the JD's primary challenge.

### 8. `optimize_linkedin_profile`
* **Input:** `candidate_cv` (str), `target_job_title` (str), `target_industry` (optional str)
* **What it does:** Stage 4 Positioning: Generates 3 outcome-focused Headlines (<220 chars), a **Recruiter Boolean Search Keyword Bank** (exact strings used on LinkedIn Recruiter), and an indexed About section.

### 9. `generate_interview_prep`
* **Input:** `candidate_cv` (str), `job_description` (str), `target_role` (optional str)
* **What it does:** Stage 5 Positioning: Cross-references candidate CV achievements with JD priorities to construct the **10 most likely interview questions** and STAR answer blueprints (covering Role Architecture, Functional Verification, Gap Stress-Tests with Honest Bridges, and Behavioral Leadership).

### 10. `osint_employer_recon`
* **Input:** `domain` (str)
* **What it does:** Zero-cost OSINT reconnaissance:
  * **SSL Certificate Transparency (crt.sh):** Enumerates hidden HR, career, talent, and direct ATS subdomains (`careers.*`, `talent.*`, `hr.*`, `workday.*`, `greenhouse.*`).
  * **Mail Infrastructure Fingerprinting:** Determines whether the employer uses Google Workspace, Microsoft 365, Zoho, Proton, or self-hosted SMTP via DNS MX.
  * **Schema.org JSON-LD Extraction:** Extracts legal company name, official telephone, contact email, and structured social profiles.

### 11. `enrich_hiring_contacts`
* **Input:** `domain` (str), `hiring_manager_first_name` (optional str), `hiring_manager_last_name` (optional str)
* **What it does:** Deep-scrapes corporate pages (`/careers`, `/team`, `/contact`) for Cloudflare XOR emails and phone numbers, generates executive email permutations, executes **zero-bounce port-25 SMTP verification with random-probe catch-all bounce defense**, and appends verified contacts to `output/hiring_contacts_output.csv`.

### 12. `prepare_job_application`
* **Input:** `job_id_or_url` (str), `candidate_profile` (str), `portal` (str, default "auto"), `company_domain` (optional str)
* **What it does:** Complete 5-Stage end-to-end packager: pulls JD details, runs 4-Tier evaluation, generates tailored STAR resume bullets, generates 250-word cover letter, creates 10-question interview prep blueprint, and optionally performs zero-bounce SMTP enrichment for the hiring team in a single call.

### 13. `export_to_docx`
* **Input:** `title` (str), `content` (str), `output_filename` (optional str), `photo_path` (optional str)
* **What it does:** Formats and exports tailored resumes, cover letters, or evaluation reports as an executive-styled Microsoft Word (`.docx`) document directly onto the user's Desktop. When exporting resumes, it automatically applies an Executive 2-Column Template with a styled Profile Photo slot (or auto-embeds the photo if `photo_path` is provided).

### 14. `track_application`
* **Input:** `action` ("add", "list", "update"), `job_id`, `company`, `role`, `portal`, `status`, `notes`, `salary`
* **What it does:** Persistently manages and logs job applications in a central CSV tracker (`job_applications_tracker.csv`) on the Desktop.

### 15. `lookup_salary_benchmark`
* **Input:** `role` (str), `location` (optional str)
* **What it does:** Provides instant market compensation benchmark ranges across Junior, Mid, and Senior tiers for role negotiations (USD and local TRY currencies).

### 📁 16. `save_search_results_folder` *(Automated Operations & Disk Archiver)*
* **Input:** `candidate_name` (str), `ranked_jobs_json` (str), `candidate_snapshot_json` (optional str), `report_markdown` (optional str)
* **What it does:** Organizes and permanently archives job matching results and operations by creating structured folders in both `output/` and directly on the user's `Desktop/Job_Search_Results/<candidate_name>_<date>/`. Generates `job_matches.csv`, executive `.docx` report, markdown summary, and metadata JSON files in one step.

---

## 📦 Prerequisites & Quick Setup

### 1. Prerequisites
* **Python (3.10+)**
* **Git**
* An MCP-compatible client (**Antigravity CLI / IDE**, **Claude Desktop**, **Cursor**) or a local **Ollama** setup.

### 2. Manual Installation
```bash
git clone https://github.com/netizen4-bit/jobs-direct.git
cd jobs-direct
pip install -r requirements.txt
```

### 3. Automatic Installation in Google Antigravity
If you are using Google Antigravity, you can install and configure JobsDirect-MCP v2.0 completely automatically. Simply paste the following prompt directly into your Antigravity chat:

````markdown
Install and configure the JobsDirect MCP server into my Antigravity setup:

1. Clone or pull the repository from https://github.com/netizen4-bit/jobs-direct into a permanent directory at `~/.gemini/antigravity/jobs-direct`.
2. Automatically install all missing Python dependencies from `requirements.txt` (`pip install -r requirements.txt`).
3. Register the server in Antigravity's global MCP configuration (`~/.gemini/config/mcp_config.json`):
   - Server name: `jobsdirect`
   - Command: `python`
   - Args: Full absolute path to `jobs_direct.py` (ensure Windows backslashes are escaped)
   - Environment variables: Set `JOBSDIRECT_CONTACTS_OUTPUT` to the absolute path of `output/hiring_contacts_output.csv` inside the repo.
4. Copy the bundled agent skills (`skills/hybrid-ats-positioning` and `skills/osint-hiring-bypass`) into `~/.gemini/config/skills/`.
5. Run a sanity check to verify that `jobs_direct.py` and `agent.py` import cleanly, and confirm once all 16 MCP tools are registered.
````

---

## 💻 Standalone Autonomous CLI Runner (`agent.py`)

JobsDirect includes a native CLI runner so you can execute job hunting, ATS fit scoring, and contact enrichment completely standalone without a desktop GUI:

```bash
# Ensure Ollama is running, then launch:
python agent.py
```

Type your objective directly into the terminal prompt:
> *"Find 5 Senior DevOps positions on direct ATS boards, evaluate my fit against my resume, tailor a STAR resume for the best match, and verify the hiring manager's email at the company."*

---

## 🔌 Connecting to Your AI Client (MCP JSON Configuration)

Add JobsDirect to your MCP configuration file (e.g. `claude_desktop_config.json`, `mcp_config.json`, or Cursor MCP settings):

> ⚠️ **Note on Windows Paths:** In JSON strings, backslashes must be escaped (`\\`) or written with forward slashes (`/`) to prevent invalid escape errors.

```json
{
  "mcpServers": {
    "jobsdirect": {
      "command": "python",
      "args": [
        "C:\\YOUR\\PATH\\TO\\jobs-direct\\jobs_direct.py"
      ],
      "env": {
        "JOBSDIRECT_CONTACTS_OUTPUT": "C:\\YOUR\\PATH\\TO\\jobs-direct\\output\\hiring_contacts_output.csv"
      }
    }
  }
}
```

* *(Alternative Windows forward slashes: `"C:/YOUR/PATH/TO/jobs-direct/jobs_direct.py"`)*
* *(macOS / Linux: `"/Users/YOUR_NAME/Documents/jobs-direct/jobs_direct.py"`)*

---

## 🧠 Using the Built-in Agent Skills

JobsDirect includes native Agent Skills under `skills/`:

* **`hybrid-ats-positioning`**: Enforces the 4-Tier ATS screening gate and 5-stage truthful positioning workflow before document generation.
* **`osint-hiring-bypass`**: Executes the double-tap strategy: direct-ATS dorking, `crt.sh` career subdomain enumeration, and zero-bounce port-25 SMTP verification.

To install the skills directly into Claude Code or compatible agents:
```bash
npx skills add netizen4-bit/jobs-direct --skill hybrid-ats-positioning
npx skills add netizen4-bit/jobs-direct --skill osint-hiring-bypass
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ☕ Support & Custom Career Pipeline Consulting

**Support Open-Source Development:**  
If JobsDirect-MCP saves your team from monthly career/ATS SaaS subscriptions or cuts your LLM token spend, consider backing ongoing development. Your support keeps these local AI, ATS, and OSINT tools free and actively maintained.

[![Patreon](https://img.shields.io/badge/Patreon-Support%20Me-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/netizen4_bit)

**💼 Need a Custom Career Pipeline or Agentic Automation?**  
Need a tailored MCP server, enterprise ATS integration, or autonomous Agentic workflow built specifically for your team? Reach out via [LinkedIn](https://www.linkedin.com/in/nihatkasim) for custom integration and consulting.
