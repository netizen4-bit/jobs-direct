"""
JobsDirect Agent — Autonomous Career & Direct-ATS Hunting Engine powered by a local Ollama LLM.

Connects to a locally-running LLM (e.g. Qwen 2.5, Llama 3) via Ollama and uses the
deterministic 4-tier ATS evaluation, 5-stage truthful positioning, and B2B OSINT
verification tools from jobs_direct.py completely offline — no paid APIs or recurring SaaS required.

Usage:
    python agent.py
    Then type your job search, ATS fit evaluation, or positioning prompt into the terminal.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import asyncio
from typing import Any, Dict

try:
    from ollama import AsyncClient
except ImportError:
    AsyncClient = None

# Import tool functions from our local jobs_direct module
import jobs_direct

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OUTPUT_DIR = jobs_direct.OUTPUT_DIR

ollama_client = AsyncClient(host=OLLAMA_HOST) if AsyncClient else None

# ---------------------------------------------------------------------------
# Ollama Tool Definitions (Function-Calling Schema)
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": (
                "Search for live job postings across direct enterprise ATS boards (Greenhouse, Lever, Ashby, "
                "Workable, SmartRecruiters) and aggregators (LinkedIn, Himalayas, Kariyer.net, Remote.co). "
                "Supports portal filtering and freshness age checks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Job title, keywords, or skills to search for (e.g. 'Senior Technical Program Manager').",
                    },
                    "location": {
                        "type": "string",
                        "description": "Target geographic location or 'Remote'.",
                    },
                    "portal": {
                        "type": "string",
                        "description": "Target portal: 'direct_ats', 'linkedin', 'himalayas', 'kariyer', 'remote_co', 'careerhound', or 'all'.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of postings to return (default 10).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_job_details",
            "description": (
                "Fetch the complete job description, requirements, criteria, active status, "
                "and extracted recruiter contact emails from any job URL or posting ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id_or_url": {
                        "type": "string",
                        "description": "Full job URL or portal job identifier.",
                    },
                    "portal": {
                        "type": "string",
                        "description": "Source portal name or 'auto'.",
                    },
                },
                "required": ["job_id_or_url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_job_fit",
            "description": (
                "Deterministic 4-Tier Weighted ATS Evaluation Engine. Evaluates candidate fit across "
                "Tier 1 Domain Affinity (40%), Tier 2 Experience & Degree Gate (20%), Tier 3 Functional Skills (30%), "
                "and Tier 4 Logistics/Language Hard Gate (10%). Returns 7-branch verdict and score breakdown."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "candidate_profile": {
                        "type": "string",
                        "description": "Candidate's full resume, work experience, and skills text.",
                    },
                    "job_description": {
                        "type": "string",
                        "description": "Target job description text.",
                    },
                    "candidate_citizenship": {
                        "type": "string",
                        "description": "Optional candidate citizenship/residency status for clearance checks.",
                    },
                },
                "required": ["candidate_profile", "job_description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "tailor_resume",
            "description": (
                "Stage 1 & 2 Truthful Positioning: Adopts the Senior Recruiter persona for the detected industry, "
                "extracts real quantified lines from the candidate's CV (never invents metrics), and generates "
                "an Exact JD Keyword Mirroring Matrix, high-agency action STAR bullets, and an Honest Bridge strategy."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "candidate_cv": {
                        "type": "string",
                        "description": "Full candidate resume text.",
                    },
                    "job_description": {
                        "type": "string",
                        "description": "Target job description text.",
                    },
                    "target_role": {
                        "type": "string",
                        "description": "Target role title.",
                    },
                    "target_company": {
                        "type": "string",
                        "description": "Target employer name.",
                    },
                },
                "required": ["candidate_cv", "job_description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_cover_letter",
            "description": (
                "Stage 3 Truthful Positioning: Generates an authentic, high-converting cover letter under a strict "
                "250-word maximum. Adopts a confident peer-level problem-solving tone and anchors around exactly "
                "one verified quantified achievement from the candidate's profile."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "candidate_profile": {
                        "type": "string",
                        "description": "Candidate profile, CV, and achievements text.",
                    },
                    "job_description": {
                        "type": "string",
                        "description": "Target job posting text.",
                    },
                    "company_name": {
                        "type": "string",
                        "description": "Target company name.",
                    },
                    "job_title": {
                        "type": "string",
                        "description": "Target job title.",
                    },
                    "hiring_manager": {
                        "type": "string",
                        "description": "Optional hiring manager name.",
                    },
                },
                "required": ["candidate_profile", "job_description", "company_name", "job_title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "optimize_linkedin_profile",
            "description": (
                "Stage 4 Positioning: Optimizes candidate LinkedIn profile for recruiter search visibility. "
                "Generates 3 outcome-driven Headlines, a Recruiter Boolean Search Keyword Bank, and an indexed About section."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "candidate_cv": {
                        "type": "string",
                        "description": "Full candidate resume text.",
                    },
                    "target_job_title": {
                        "type": "string",
                        "description": "Target role (e.g. 'Senior Technical Program Manager').",
                    },
                    "target_industry": {
                        "type": "string",
                        "description": "Optional target industry vertical.",
                    },
                },
                "required": ["candidate_cv", "target_job_title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_interview_prep",
            "description": (
                "Stage 5 Truthful Positioning: Generates the 10 most likely interview questions and STAR answer frameworks "
                "by cross-referencing candidate CV achievements with JD requirements (deep-diving matched skills and stress-testing gaps)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "candidate_cv": {
                        "type": "string",
                        "description": "Full candidate resume text.",
                    },
                    "job_description": {
                        "type": "string",
                        "description": "Target job posting text.",
                    },
                    "target_role": {
                        "type": "string",
                        "description": "Optional target role title.",
                    },
                },
                "required": ["candidate_cv", "job_description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "osint_employer_recon",
            "description": (
                "Performs zero-cost OSINT reconnaissance on an employer domain: enumerates hidden career/ATS subdomains "
                "via SSL Certificate Transparency logs (crt.sh), fingerprints corporate mail infrastructure (Google/Microsoft/Zoho), "
                "and extracts Schema.org JSON-LD corporate metadata and social links."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Employer domain name or website URL (e.g. 'fluxon.com', 'canonical.com').",
                    },
                },
                "required": ["domain"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "enrich_hiring_contacts",
            "description": (
                "Enriches hiring team contacts and executes zero-bounce port-25 SMTP verification with random-probe "
                "catch-all bounce defense. Scrapes corporate pages, generates hiring manager email permutations, and logs verified contacts to CSV."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "domain": {
                        "type": "string",
                        "description": "Target employer domain (e.g. 'fluxon.com').",
                    },
                    "hiring_manager_first_name": {
                        "type": "string",
                        "description": "Optional first name of hiring manager or recruiter.",
                    },
                    "hiring_manager_last_name": {
                        "type": "string",
                        "description": "Optional last name of hiring manager or recruiter.",
                    },
                },
                "required": ["domain"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "export_to_docx",
            "description": (
                "Exports tailored resumes, cover letters, or evaluation reports into an executive-styled "
                "Microsoft Word document (.docx) on the user's Desktop."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Document title (e.g. 'Tailored_CV_Fluxon').",
                    },
                    "content": {
                        "type": "string",
                        "description": "Markdown or formatted plain text content to write into the document.",
                    },
                    "output_filename": {
                        "type": "string",
                        "description": "Optional filename (e.g. 'Fluxon_Application.docx').",
                    },
                },
                "required": ["title", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "track_application",
            "description": (
                "Manages and logs job applications in the local persistent CSV tracker on the Desktop."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "'add', 'list', or 'update'.",
                    },
                    "job_id": {
                        "type": "string",
                        "description": "Job URL or ID.",
                    },
                    "company": {
                        "type": "string",
                        "description": "Company name.",
                    },
                    "role": {
                        "type": "string",
                        "description": "Role / job title.",
                    },
                    "status": {
                        "type": "string",
                        "description": "Stage: 'scouted', 'applied', 'interviewing', 'offer', 'rejected'.",
                    },
                },
                "required": ["action"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_profile_or_page",
            "description": (
                "Scrapes any candidate profile page, portfolio website, GitHub, LinkedIn, or social media front page "
                "using a 2-tier waterfall (fast HTTP + Playwright headless browser). Extracts readable bio, text, "
                "emails, phones, and social links."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL of the profile or page to scrape.",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_jobs_from_profile",
            "description": (
                "Automated Profile-to-Job Matching Engine: Takes a candidate's profile URL (LinkedIn, GitHub, portfolio, personal bio), "
                "scrapes their page, extracts domain affinity and key skills, searches direct enterprise ATS boards & aggregators, "
                "and runs deterministic 4-Tier ATS fit scoring on all found opportunities."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "profile_url": {
                        "type": "string",
                        "description": "Full URL of candidate profile (e.g. 'https://linkedin.com/in/username', 'https://github.com/username').",
                    },
                    "location": {
                        "type": "string",
                        "description": "Target job location (default 'Remote').",
                    },
                    "portal": {
                        "type": "string",
                        "description": "'direct_ats', 'linkedin', 'himalayas', 'kariyer', 'remote_co', or 'all' (default 'all').",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of jobs to return (default 10).",
                    },
                },
                "required": ["profile_url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "prepare_job_application",
            "description": (
                "Automated end-to-end 5-Stage application packager: Fetches full job details, evaluates 4-Tier ATS fit, "
                "tailors STAR bullets with JD keyword mirroring, drafts a 250-word max cover letter, generates a 10-question "
                "interview prep blueprint, and optionally enriches hiring contacts with zero-bounce SMTP verification."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "job_id_or_url": {
                        "type": "string",
                        "description": "Job posting identifier or URL.",
                    },
                    "candidate_profile": {
                        "type": "string",
                        "description": "Candidate CV, skills, and background text.",
                    },
                    "portal": {
                        "type": "string",
                        "description": "Portal source ('direct_ats', 'linkedin', 'himalayas', 'kariyer', 'auto').",
                    },
                    "company_domain": {
                        "type": "string",
                        "description": "Optional employer domain (e.g. 'fluxon.com') to enrich hiring contacts.",
                    },
                },
                "required": ["job_id_or_url", "candidate_profile"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_salary_benchmark",
            "description": "Provides standard salary benchmark ranges and guidance for role compensation negotiations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Job role or title (e.g. 'Software Engineer', 'Project Manager').",
                    },
                    "location": {
                        "type": "string",
                        "description": "Geographic market ('US', 'Europe', 'Türkiye', 'Remote').",
                    },
                },
                "required": ["role"],
            },
        },
    },
]

# ---------------------------------------------------------------------------
# Tool Dispatcher
# ---------------------------------------------------------------------------
async def execute_tool(name: str, args: Dict[str, Any]) -> str:
    """Route a tool call to the correct JobsDirect module function."""
    print(f"\n  [🔧 Tool Call] {name}")
    print(f"      Args: {json.dumps(args, ensure_ascii=False)[:180]}")

    try:
        if name == "find_jobs_from_profile":
            result = await jobs_direct.find_jobs_from_profile(**args)
        elif name == "prepare_job_application":
            result = await jobs_direct.prepare_job_application(**args)
        elif name == "lookup_salary_benchmark":
            result = jobs_direct.lookup_salary_benchmark(**args)
        elif name == "search_jobs":
            result = await jobs_direct.search_jobs(**args)
        elif name == "get_job_details":
            result = await jobs_direct.get_job_details(**args)
        elif name == "evaluate_job_fit":
            result = jobs_direct.evaluate_job_fit(**args)
        elif name == "tailor_resume":
            result = jobs_direct.tailor_resume(**args)
        elif name == "generate_cover_letter":
            result = jobs_direct.generate_cover_letter(**args)
        elif name == "optimize_linkedin_profile":
            result = jobs_direct.optimize_linkedin_profile(**args)
        elif name == "generate_interview_prep":
            result = jobs_direct.generate_interview_prep(**args)
        elif name == "osint_employer_recon":
            result = await jobs_direct.osint_employer_recon(**args)
        elif name == "enrich_hiring_contacts":
            result = await jobs_direct.enrich_hiring_contacts(**args)
        elif name == "scrape_profile_or_page":
            result = await jobs_direct.scrape_profile_or_page(**args)
        elif name == "export_to_docx":
            result = jobs_direct.export_to_docx(**args)
        elif name == "track_application":
            result = jobs_direct.track_application(**args)
        else:
            result = f"Error: Unknown tool '{name}'"
    except Exception as e:
        result = f"Error executing {name}: {str(e)}"
        print(f"      [❌] {result}")
        return result

    print(f"      [✅] {len(str(result))} chars returned")
    return str(result)

# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are JobsDirect Agent v2.0 — an autonomous career strategy and direct-ATS job hunting agent "
    "running entirely on a local machine with no paid APIs.\n\n"
    "CAPABILITIES:\n"
    "- Direct-ATS & Multi-Portal Discovery (`search_jobs`, `get_job_details`): Search raw company ATS boards "
    "  (Greenhouse, Lever, Ashby, Workable, SmartRecruiters) and aggregators (LinkedIn, Himalayas, Kariyer.net).\n"
    "- Deterministic 4-Tier ATS Fit Engine (`evaluate_job_fit`): Always check job fit before tailoring.\n"
    "  Tier 1 Domain Affinity (40%), Tier 2 Qualifications Gate (20%), Tier 3 Core Skills (30%), Tier 4 Logistics (10%).\n"
    "- 5-Stage Truthful Positioning Pipeline:\n"
    "  1. Recruiter Persona & STAR Optimization (`tailor_resume`)\n"
    "  2. Exact JD Keyword Mirroring Matrix (`tailor_resume`)\n"
    "  3. 250-Word Single-Anchor Cover Letter (`generate_cover_letter`)\n"
    "  4. LinkedIn Boolean Keyword Alignment (`optimize_linkedin_profile`)\n"
    "  5. 10-Question STAR Stress-Test Prep (`generate_interview_prep`)\n"
    "- OSINT Double-Tap Outreach (`osint_employer_recon`, `enrich_hiring_contacts`): Enumerate hidden ATS subdomains via crt.sh, "
    "  fingerprint mail providers, and perform zero-bounce port-25 SMTP verification with random-probe catch-all defense.\n\n"
    "WORKFLOW RULES:\n"
    "1. Always evaluate job fit first using `evaluate_job_fit`.\n"
    "2. If verdict is CLOSED_OR_EXPIRED or REJECTED (Language Gate Restriction), STOP immediately and notify the user.\n"
    "3. Never invent candidate experience, metrics, or credentials. Always remain 100% truthful to the candidate's CV.\n"
    "4. When tailoring, use the candidate's real quantified numbers in STAR bullets and use Honest Bridges for secondary gaps.\n"
    "5. Use `export_to_docx` to save professional Word copies on Desktop when requested.\n"
)

# ---------------------------------------------------------------------------
# Agent Loop
# ---------------------------------------------------------------------------
async def run_agent(user_prompt: str):
    """Main agentic loop: send prompt → handle tool calls → repeat until done."""
    if not ollama_client:
        print("❌ Error: 'ollama' library is not available. Please install via pip install ollama.")
        return

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    print(f"\n{'='*60}")
    print("🤖 [JobsDirect v2.0] Processing your request...")
    print(f"{'='*60}\n")

    iteration = 0
    max_iterations = 15

    while iteration < max_iterations:
        iteration += 1
        print(f"⏳ [{iteration}/{max_iterations}] Reasoning & Orchestrating Tools...")

        try:
            response = await ollama_client.chat(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS,
                options={"temperature": 0.1},
            )
        except Exception as e:
            print(f"\n❌ Ollama connection error: {e}")
            print(f"   Ensure Ollama is running (`ollama serve`) and model '{MODEL_NAME}' is pulled.")
            break

        message = response.get("message", {})
        messages.append(message)

        if not message.get("tool_calls"):
            print(f"\n{'='*60}")
            print("✅ JobsDirect v2.0 — Final Strategic Report")
            print(f"{'='*60}")
            print(message.get("content", "(no response)"))
            break

        for tool_call in message["tool_calls"]:
            fn_name = tool_call["function"]["name"]
            fn_args = tool_call["function"]["arguments"]

            tool_result = await execute_tool(fn_name, fn_args)

            messages.append({
                "role": "tool",
                "content": str(tool_result),
                "name": fn_name,
            })
    else:
        print(f"\n⚠️  Reached maximum safety iteration limit ({max_iterations}). Stopping.")

# ---------------------------------------------------------------------------
# Interactive Terminal Entry Point
# ---------------------------------------------------------------------------
def main():
    """Interactive terminal loop — type a prompt, get autonomous career execution."""
    print(r"""
     _       _         ____  _               _   
    | | ___ | |__  ___|  _ \(_)_ __ ___  ___| |_ 
 _  | |/ _ \| '_ \/ __| | | | | '__/ _ \/ __| __|
| |_| | (_) | |_) \__ \ |_| | | | |  __/ (__| |_ 
 \___/ \___/|_.__/|___/____/|_|_|  \___|\___|\__|
                                                 
  Hybrid ATS Fit Engine & B2B OSINT Hiring Outreach (v2.0)
  Powered by Local Ollama · 100% Free & Open-Source
""")
    print(f"  Model:  {MODEL_NAME}")
    print(f"  Ollama: {OLLAMA_HOST}")
    print(f"  Output: {OUTPUT_DIR}")
    print("  Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            prompt = input("🎯 Enter your job search or positioning prompt:\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not prompt:
            continue
        if prompt.lower() in ("quit", "exit", "q"):
            print("👋 Goodbye!")
            break

        asyncio.run(run_agent(prompt))
        print()


if __name__ == "__main__":
    main()
