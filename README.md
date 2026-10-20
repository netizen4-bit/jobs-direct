# JobsDirect-MCP

A local Model Context Protocol (MCP) tool for Agentic Workflows that automates multi-portal job search, 4-tier ATS fit evaluation, resume tailoring, cover letter generation, and application preparation. Built for job seekers, career switchers, and professionals to run completely locally and privately.

JobsDirect connects your AI assistant (Claude Desktop, Cursor, Antigravity) directly to global and regional job portals (LinkedIn, Himalayas, Kariyer.net, Remote.co, CareerHound, HiredChina). It autonomously searches job boards, scores candidate-to-job fit using a dynamic 4-tier ATS matching engine (eliminating false-positive domain mismatches), tailors your CV using the STAR framework, writes targeted cover letters, formats pre-filled application form answers, and exports ready-to-use Word (`.docx`) documents directly to your Desktop.

---

## 🛠️ Prerequisites

Before installing, you need a few basic tools installed on your computer:

1. **Python (3.10+)** — The programming language this runs on.
2. **Git for Windows/Mac** — Used to download this repository.
3. **An MCP-Compatible AI Client** — You need an AI to command the tool. Choose one:
   - **Claude Desktop** (Recommended for ease of use)
   - **Cursor IDE** (For developers)
   - **Antigravity CLI / IDE** (For local terminal users and pair programming)

---

## 🚀 Quick Start Guide

Open your terminal (Command Prompt or PowerShell on Windows, or Terminal on Mac/Linux) and run these commands:

```bash
git clone https://github.com/netizen4-bit/jobs-direct
cd jobs-direct
pip install -r requirements.txt
```

---

## 🔗 Connecting to your AI (MCP Client Configuration)

To let your AI use this tool, you must tell it where this folder is located on your computer.

Add **JobsDirect** to your MCP client configuration file (e.g., `claude_desktop_config.json` or `mcp_config.json`):

> ⚠️ **IMPORTANT**: You MUST replace the `args` path below with the exact location where you downloaded this folder on your computer.

```json
{
  "mcpServers": {
    "jobsdirect": {
      "command": "python",
      "args": ["C:\\YOUR\\EXACT\\PATH\\HERE\\jobs-direct\\jobs_direct.py"]
    }
  }
}
```

* *(Example for Windows: `"C:\\Users\\YOUR_NAME\\Documents\\jobs-direct\\jobs_direct.py"`)*
* *(Example for Mac/Linux: `"/Users/YOUR_NAME/Documents/jobs-direct/jobs_direct.py"`)*

---

## 📁 Project Structure

```
jobs-direct/
├── .github/
│   ├── FUNDING.yml
│   └── ISSUE_TEMPLATE/
│       └── feature_request.md
├── jobs_direct.py      # The core Bridge & Agent tools. Connects to your AI client.
├── requirements.txt    # Python dependencies
├── CODE_OF_CONDUCT.md  # Community guidelines
├── CONTRIBUTING.md     # Contribution guidelines
├── LICENSE             # MIT License
├── SECURITY.md         # Security policy
└── README.md           # Project documentation
```

---

## 🧰 Tools Reference & Prompting

### 🌐 Supported Job Portals

| Portal Key | Source | Primary Focus |
| :--- | :--- | :--- |
| **`linkedin`** | **LinkedIn** | Global, regional, and remote postings across all industries |
| **`himalayas`** | **Himalayas.app** | Curated remote tech jobs with transparent salary ranges |
| **`kariyer`** | **Kariyer.net** | Turkey's premier job portal for local and regional Turkish roles |
| **`remote_co`** | **Remote.co** | Top curated remote careers and global telecommute roles |
| **`careerhound`** | **CareerHound.io** | Hidden, direct-from-employer opportunities not on traditional job boards |
| **`hiredchina`** | **HiredChina.com** | International, bilingual, and expat opportunities in China & Asia |
| **`all`** | **Aggregated** | Runs search queries across all 6 portals simultaneously |

---

### 🧠 The Dynamic 4-Tier ATS Evaluation Engine (`evaluate_job_fit`)

Unlike basic keyword counters that match an applicant to the wrong industry simply because both job postings use generic words like *"Agile"*, *"KPIs"*, or *"Stakeholder Management"*, **JobsDirect** implements a **100% dynamic, candidate-agnostic 4-Tier Weighted ATS Engine**:

```
TOTAL ATS FIT SCORE (0 - 100) =
  ├── Tier 1: Dynamic Industry / Domain Affinity (40% Weight)
  │     Extracts the candidate's historical industry footprint and compares it
  │     against the employer's industry. Prevents functional title false positives
  │     (e.g., matching a heavy machinery PM to a crypto/forex broker).
  │
  ├── Tier 2: Minimum Qualifications & Experience Gate (20% Weight)
  │     Extracts required degree level (Bachelor's / Master's / PhD) and minimum
  │     Years of Experience (YoE) from the posting and verifies threshold satisfaction.
  │
  ├── Tier 3: Functional & Technical Core Skills (30% Weight)
  │     Evaluates toolset, methodologies, and technical stack intersections
  │     (Agile, Jira, APIs, ERP, Data Analytics, CI/CD, CRM, etc.).
  │
  └── Tier 4: Practical Logistics & Language Gate (10% Weight + Hard Gate)
        Checks required working languages, security clearance/citizenship gates,
        and geographic / remote compatibility.
```

---

### 💡 How to Structure High-Converting Job Search Prompts

Because JobsDirect operates autonomously, the quality of your output depends on clear instructions:

1. **Tool #1 (`search_jobs`)**: Finds open positions across LinkedIn, Himalayas, Kariyer.net, Remote.co, CareerHound, and HiredChina.
2. **Tool #2 (`get_job_details`)**: Fetches full requirements, responsibilities, and seniority criteria from any job ID or URL.
3. **Tool #3 (`evaluate_job_fit`)**: Runs the 4-tier ATS algorithm to calculate your match score (0–100) and highlight gaps.
4. **Tool #4 (`tailor_resume`)**: Rewrites your CV bullet points into quantified STAR stories (Situation, Task, Action, Result).
5. **Tool #5 (`generate_cover_letter`)**: Writes a compelling, authentic 3-act cover letter (The Hook, The Proof, The Close).
6. **Tool #6 (`prepare_job_application`)**: Bundles your application answers, screening questions, and direct apply link.
7. **Tool #7 (`export_to_docx`)**: Saves any generated text, resume, or report as an executive-formatted Word document (`.docx`) directly onto your Desktop.
8. **Tool #8 (`track_application`)**: Automatically logs your submitted applications into a central tracker file on your Desktop.
9. **Tool #9 (`lookup_salary_benchmark`)**: Provides global and regional salary ranges to guide compensation expectations.

---

### ⚡ The Chained Prompt Formula

Copy and paste this prompt formula directly into Claude Desktop, Cursor, or Antigravity:

```text
"I am searching for remote Senior Technical Project Manager or Operations positions in Europe and Türkiye.

Step 1: Use your search_jobs tool to find 5 open positions across LinkedIn, Himalayas, and Kariyer.net.
Step 2: Use your evaluate_job_fit tool to score each position against my attached background and pick the highest-scoring match.
Step 3: Use your tailor_resume and generate_cover_letter tools to craft customized application materials for that top position.
Step 4: Use your export_to_docx tool to save the tailored CV and cover letter directly to my Desktop as a Word document.
Step 5: Use your track_application tool to log this application into my tracker."
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## ☕ Support the Developer

If this tool saved you a day, and if you use my other open-source workflow tools, consider supporting the development. Your backing helps keep these small AI tools projects completely free.

[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/netizen4_bit)
