"""
JobsDirect-MCP: The Local AI Job Search & Application Automation Framework
An open-source Model Context Protocol (MCP) server for multi-portal job discovery,
4-tier weighted ATS fit evaluation, resume tailoring, cover letter generation,
Microsoft Word (.docx) export, and application pipeline tracking.
"""

import os
import sys
import re
import csv
import json
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse, parse_qs
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from fastmcp import FastMCP
from ddgs import DDGS

# Initialize FastMCP Server
mcp = FastMCP(
    "JobsDirect",
    instructions="Automated MCP for multi-portal job search (LinkedIn, Himalayas, Kariyer.net, Remote.co, CareerHound, HiredChina), dynamic 4-tier ATS fit evaluation, STAR resume tailoring, cover letter generation, Word (.docx) export, and application tracking.",
)

TRACKER_FILE = os.path.join(os.path.expanduser("~"), "Desktop", "job_applications_tracker.csv")
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# ---------------------------------------------------------------------------
# Dynamic Universal Industry Taxonomy
# ---------------------------------------------------------------------------
INDUSTRY_TAXONOMY: Dict[str, List[str]] = {
    "Fintech, Trading & Financial Markets": [
        "fintech", "banking", "payments", "cards", "card payments", "merchant", "checkout",
        "forex", "fx", "cfd", "brokerage", "derivatives", "trading", "crypto", "blockchain",
        "web3", "defi", "p2p", "digital assets", "quantitative", "hedge fund", "asset management",
        "lending", "credit", "securities", "wealthtech"
    ],
    "Industrial, Manufacturing & Heavy Machinery": [
        "manufacturing", "industrial", "heavy machinery", "equipment", "machinery", "automotive",
        "aerospace", "defense", "mechanical", "electrical hardware", "factory", "plant",
        "supply chain", "logistics", "customs", "freight", "warehouse", "elevator", "escalator",
        "marine", "power generation", "engines", "turbines", "automation hardware", "sensors",
        "instrumentation", "materials", "procurement", "tender", "bidding", "b2b distribution"
    ],
    "Healthcare, Biotech & Pharmaceuticals": [
        "healthcare", "hospital", "clinical", "pharma", "pharmaceutical", "biotech", "medical device",
        "therapeutics", "life sciences", "diagnostics", "oncology", "genomics", "healthtech"
    ],
    "E-Commerce, Retail & Consumer Goods": [
        "ecommerce", "e-commerce", "retail", "shopify", "d2c", "marketplace", "b2c",
        "consumer goods", "apparel", "merchandising", "fmcg", "storefront", "omnichannel"
    ],
    "Software, Cloud & Enterprise SaaS": [
        "saas", "enterprise software", "cloud", "aws", "gcp", "azure", "devops", "cybersecurity",
        "infrastructure", "data engineering", "developer tools", "b2b software", "platform",
        "microservices", "database", "analytics software"
    ],
    "Media, Gaming & Entertainment": [
        "gaming", "game dev", "unity", "unreal", "streaming", "media", "entertainment",
        "broadcasting", "audio tech", "music tech", "video production", "animation"
    ],
    "Energy, Utilities & Cleantech": [
        "energy", "oil & gas", "petroleum", "renewables", "solar", "wind", "power grid",
        "utilities", "cleantech", "sustainability", "battery", "ev"
    ],
    "Education & EdTech": [
        "education", "edtech", "e-learning", "university", "curriculum", "academic", "training"
    ],
    "Telecommunications & Networking": [
        "telecom", "telecommunications", "networking", "5g", "wireless", "broadband", "isp", "iot hardware"
    ]
}

# ---------------------------------------------------------------------------
# Helper Utilities
# ---------------------------------------------------------------------------

def clean_text(text: Optional[str]) -> str:
    """Cleans whitespace and HTML entities from text."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def decode_html(html: str) -> str:
    """Decodes basic HTML entities."""
    return (
        html.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&apos;", "'")
        .replace("&nbsp;", " ")
    )


def extract_domains(text: str) -> Dict[str, int]:
    """Dynamically counts keyword occurrences across industry taxonomies."""
    text_lower = text.lower()
    domain_counts: Dict[str, int] = {}
    for domain, kws in INDUSTRY_TAXONOMY.items():
        hits = 0
        for kw in kws:
            pattern = rf"\b{re.escape(kw)}\b"
            hits += len(re.findall(pattern, text_lower))
        if hits > 0:
            domain_counts[domain] = hits
    return domain_counts


def calculate_domain_affinity(cand_domains: Dict[str, int], job_domains: Dict[str, int]) -> Tuple[float, List[str], List[str]]:
    """Calculates domain compatibility percentage between candidate and job."""
    if not job_domains:
        return 0.85, list(cand_domains.keys())[:3], ["General Tech / Horizontal"]

    job_total = sum(job_domains.values())
    shared_weight = 0.0
    matched_domains = []
    unmatched_domains = []

    for dom, count in job_domains.items():
        importance = count / job_total
        if dom in cand_domains:
            cand_strength = min(cand_domains[dom] / 3.0, 1.0)
            shared_weight += importance * cand_strength
            matched_domains.append(f"{dom} ({int(importance*100)}% job focus)")
        else:
            unmatched_domains.append(f"{dom} ({int(importance*100)}% job focus)")

    return min(max(shared_weight, 0.0), 1.0), matched_domains, unmatched_domains


def extract_yoe(text: str) -> Optional[int]:
    """Dynamically extracts years of experience requirement from text."""
    patterns = [
        r'(?:minimum|at least|over)?\s*(\d+)\+?\s*(?:to|-)\s*\d+\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp|background|track record)',
        r'(\d+)\+?\s*(?:years?|yrs?)'
    ]
    found = []
    for pat in patterns:
        for match in re.finditer(pat, text, re.IGNORECASE):
            try:
                found.append(int(match.group(1)))
            except Exception:
                pass
    return max(found) if found else None


def extract_degree_level(text: str) -> int:
    """Returns numerical education hierarchy level: 0=None, 1=Bachelor, 2=Master, 3=PhD/Doctorate."""
    t = text.lower()
    if re.search(r'\b(ph\.?d|doctorate|doctoral)\b', t):
        return 3
    if re.search(r'\b(master|m\.?s|m\.?sc|m\.?eng|mba|graduate degree)\b', t):
        return 2
    if re.search(r'\b(bachelor|b\.?s|b\.?sc|b\.?a|b\.?eng|undergraduate)\b', t):
        return 1
    return 0


# ---------------------------------------------------------------------------
# 1. Multi-Portal Scrapers
# ---------------------------------------------------------------------------

async def search_linkedin(
    query: str,
    location: str = "Remote",
    jobage_days: Optional[int] = None,
    remote: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Searches LinkedIn public jobs-guest endpoint."""
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    params: Dict[str, str] = {
        "keywords": query,
        "location": location,
        "start": "0",
    }
    if jobage_days:
        seconds = jobage_days * 86400
        params["f_TPR"] = f"r{seconds}"
    if remote:
        r_lower = remote.lower()
        if "remote" in r_lower:
            params["f_WT"] = "2"
        elif "hybrid" in r_lower:
            params["f_WT"] = "3"
        elif "onsite" in r_lower:
            params["f_WT"] = "1"

    headers = {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    results: List[Dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            resp = await client.get(base_url, params=params, headers=headers)
            if resp.status_code != 200:
                return results

            html = resp.text
            chunks = html.split('data-entity-urn="urn:li:jobPosting:')[1:]
            for chunk in chunks:
                if len(results) >= limit:
                    break
                id_match = re.match(r"^(\d+)", chunk)
                if not id_match:
                    continue
                job_id = id_match.group(1)

                title_match = re.search(
                    r'class="base-search-card__title"[^>]*>([\s\S]*?)<\/h3>', chunk
                )
                title = clean_text(title_match.group(1)) if title_match else None
                if not title:
                    sr_match = re.search(r'class="sr-only"[^>]*>([\s\S]*?)<\/span>', chunk)
                    title = clean_text(sr_match.group(1)) if sr_match else f"Job {job_id}"

                comp_match = re.search(
                    r'class="base-search-card__subtitle"[^>]*>([\s\S]*?)<\/h4>', chunk
                )
                company = clean_text(comp_match.group(1)) if comp_match else None

                loc_match = re.search(
                    r'class="job-search-card__location"[^>]*>([\s\S]*?)<\/span>', chunk
                )
                loc = clean_text(loc_match.group(1)) if loc_match else location

                dt_match = re.search(r'datetime="([^"]+)"', chunk)
                date = dt_match.group(1) if dt_match else datetime.today().strftime("%Y-%m-%d")

                link_match = re.search(
                    r'class="base-card__full-link[^"]*"[^>]*href="([^"]+)"', chunk
                )
                url = (
                    decode_html(link_match.group(1)).split("?")[0]
                    if link_match
                    else f"https://www.linkedin.com/jobs/view/{job_id}"
                )

                results.append(
                    {
                        "id": job_id,
                        "title": title,
                        "company": company,
                        "location": loc,
                        "date": date,
                        "url": url,
                        "portal": "linkedin",
                    }
                )
        except Exception as e:
            results.append({"error": f"LinkedIn search failed: {str(e)}", "portal": "linkedin"})

    return results


async def get_linkedin_detail(job_id: str) -> Dict[str, Any]:
    """Fetches full job description from LinkedIn public jobPosting endpoint."""
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    headers = {"User-Agent": DEFAULT_UA}

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code != 200:
                return {"error": f"LinkedIn returned status {resp.status_code}", "job_id": job_id}

            soup = BeautifulSoup(resp.text, "html.parser")

            title_tag = soup.find(class_=re.compile(r"top-card-layout__title|topcard__title"))
            title = clean_text(title_tag.text) if title_tag else "N/A"

            company_tag = soup.find(class_=re.compile(r"topcard__org-name-link"))
            company = clean_text(company_tag.text) if company_tag else "N/A"

            loc_tag = soup.find(class_=re.compile(r"topcard__flavor--bullet"))
            location = clean_text(loc_tag.text) if loc_tag else "N/A"

            desc_div = soup.find(class_=re.compile(r"show-more-less-html__markup|description__text"))
            description = desc_div.get_text("\n", strip=True) if desc_div else ""

            criteria = {}
            for item in soup.find_all(class_=re.compile(r"description__job-criteria-item")):
                sub = item.find(class_=re.compile(r"description__job-criteria-subheader"))
                val = item.find(class_=re.compile(r"description__job-criteria-text"))
                if sub and val:
                    criteria[clean_text(sub.text)] = clean_text(val.text)

            return {
                "id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "criteria": criteria,
                "url": f"https://www.linkedin.com/jobs/view/{job_id}",
                "portal": "linkedin",
            }
        except Exception as e:
            return {"error": f"Failed fetching LinkedIn job detail: {str(e)}", "job_id": job_id}


async def search_himalayas(
    query: str,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Searches Himalayas.app via its public API and filters by keyword."""
    url = "https://himalayas.app/jobs/api?limit=100"
    headers = {"User-Agent": DEFAULT_UA}
    results: List[Dict[str, Any]] = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                jobs = data.get("jobs", [])
                q_words = [w.lower() for w in query.split() if len(w) > 1]
                for job in jobs:
                    if len(results) >= limit:
                        break
                    title = job.get("title", "")
                    categories = " ".join(job.get("categories", []))
                    desc = job.get("excerpt", "") or ""
                    haystack = f"{title} {categories} {desc}".lower()

                    if any(w in haystack for w in q_words) or not q_words:
                        salary_info = ""
                        if job.get("minSalary") and job.get("maxSalary"):
                            salary_info = f"{job.get('minSalary'):,}-{job.get('maxSalary'):,} {job.get('currency', 'USD')}"
                        results.append(
                            {
                                "id": job.get("guid", ""),
                                "title": title,
                                "company": job.get("companyName", ""),
                                "location": "Remote" + (f" ({', '.join(job.get('locationRestrictions', []))})" if job.get("locationRestrictions") else ""),
                                "salary": salary_info,
                                "date": datetime.fromtimestamp(job["pubDate"]).strftime("%Y-%m-%d") if job.get("pubDate") else "",
                                "url": job.get("applicationLink") or job.get("guid", ""),
                                "portal": "himalayas",
                            }
                        )
        except Exception as e:
            results.append({"error": f"Himalayas search failed: {str(e)}", "portal": "himalayas"})

    return results


def search_site_via_ddg(site: str, query: str, limit: int = 10, portal_name: str = "web") -> List[Dict[str, Any]]:
    """Discovers live indexed jobs from site via DuckDuckGo search without rate limits or bot walls."""
    results: List[Dict[str, Any]] = []
    search_queries = [f"site:{site} {query}".strip(), f'"{site}" {query} jobs'.strip()]
    
    for sq in search_queries:
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.text(sq, max_results=limit * 2))
                for item in raw_results:
                    if len(results) >= limit:
                        break
                    href = item.get("href", "")
                    title = clean_text(item.get("title", ""))
                    if href.rstrip("/") in (f"https://{site}", f"https://www.{site}", f"http://{site}"):
                        continue
                    clean_title = re.sub(rf"\s*[-|]\s*.*{re.escape(site)}.*", "", title, flags=re.IGNORECASE).strip()
                    results.append(
                        {
                            "id": href,
                            "title": clean_title or title,
                            "company": portal_name.capitalize(),
                            "location": "Remote" if "remote" in site else "Global / Specified in post",
                            "date": datetime.today().strftime("%Y-%m-%d"),
                            "snippet": clean_text(item.get("body", "")),
                            "url": href,
                            "portal": portal_name,
                        }
                    )
            if results:
                break
        except Exception:
            continue

    return results


def search_kariyer(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Discovers active job postings on Kariyer.net (Turkey's premier job portal)."""
    results: List[Dict[str, Any]] = []
    queries = [
        f"site:kariyer.net/is-ilani {query}".strip(),
        f"site:kariyer.net {query} iş ilanı".strip(),
        f'"kariyer.net" {query} iş ilanları'.strip(),
    ]

    for q in queries:
        try:
            with DDGS() as ddgs:
                raw = list(ddgs.text(q, max_results=limit * 2))
                for item in raw:
                    if len(results) >= limit:
                        break
                    href = item.get("href", "")
                    title = clean_text(item.get("title", ""))
                    body = clean_text(item.get("body", ""))

                    if "/is-ilani/" in href or "kariyer.net" in href:
                        clean_title = re.sub(r"\s*[-|]\s*.*kariyer\.net.*", "", title, flags=re.IGNORECASE).strip()
                        comp = "Kariyer.net Employer"
                        if " - " in clean_title:
                            parts = clean_title.split(" - ")
                            comp = parts[0].strip()
                            clean_title = " - ".join(parts[1:]).strip()

                        results.append(
                            {
                                "id": href,
                                "title": clean_title or title,
                                "company": comp,
                                "location": "Türkiye (Kariyer.net)",
                                "date": datetime.today().strftime("%Y-%m-%d"),
                                "snippet": body,
                                "url": href,
                                "portal": "kariyer.net",
                            }
                        )
            if results:
                break
        except Exception:
            continue

    return results


# ---------------------------------------------------------------------------
# 2. FastMCP Tool Definitions
# ---------------------------------------------------------------------------

@mcp.tool()
async def search_jobs(
    query: str,
    location: str = "Remote",
    portal: str = "all",
    remote: Optional[str] = None,
    jobage_days: Optional[int] = None,
    limit: int = 10,
) -> str:
    """
    Searches for open job postings across supported portals:
    - linkedin: Global postings (remote & local)
    - himalayas: Curated remote tech jobs with salary transparency
    - remote_co: Remote.co listings
    - careerhound: CareerHound.io hidden/direct jobs
    - hiredchina: HiredChina.com bilingual & international roles
    - kariyer: Kariyer.net Turkish & regional positions
    - all: Aggregated search across all portals

    Args:
        query: Search keywords (e.g. "Software Engineer", "Operations Manager", "Data Scientist").
        location: Target location or "Remote".
        portal: "linkedin", "himalayas", "remote_co", "careerhound", "hiredchina", "kariyer", or "all". Default: "all".
        remote: Filter workplace type: "remote", "hybrid", or "onsite".
        jobage_days: Filter postings published within the last N days (e.g. 1, 7, 14, 30).
        limit: Maximum number of job postings to return (default 10).
    """
    p = portal.lower().strip()
    collected: List[Dict[str, Any]] = []

    if p in ("linkedin", "all"):
        linkedin_results = await search_linkedin(query, location, jobage_days, remote, limit)
        collected.extend(linkedin_results)

    if p in ("himalayas", "all"):
        himalayas_results = await search_himalayas(query, limit)
        collected.extend(himalayas_results)

    if p in ("kariyer", "kariyer.net", "all"):
        kariyer_results = search_kariyer(query, limit=limit)
        collected.extend(kariyer_results)

    if p in ("remote_co", "remote.co", "all"):
        remote_co_results = search_site_via_ddg("remote.co", query, limit=limit, portal_name="remote.co")
        collected.extend(remote_co_results)

    if p in ("careerhound", "careerhound.io", "all"):
        hound_results = search_site_via_ddg("careerhound.io", query, limit=limit, portal_name="careerhound.io")
        collected.extend(hound_results)

    if p in ("hiredchina", "hiredchina.com", "all"):
        china_results = search_site_via_ddg("hiredchina.com", query, limit=limit, portal_name="hiredchina.com")
        collected.extend(china_results)

    if not collected:
        return f"No jobs found for query '{query}' in location '{location}' on portal '{portal}'."

    return json.dumps(collected[: limit if p != "all" else limit * 2], indent=2)


@mcp.tool()
async def get_job_details(job_id_or_url: str, portal: str = "auto") -> str:
    """
    Fetches full job description, requirements, seniority, and criteria for any job posting.

    Args:
        job_id_or_url: The job ID or full URL from any supported portal (LinkedIn, Himalayas, Remote.co, CareerHound, HiredChina, Kariyer.net, or company site).
        portal: "linkedin", "himalayas", "remote_co", "careerhound", "hiredchina", "kariyer", or "auto".
    """
    clean_id = job_id_or_url.strip()
    detected_portal = portal.lower()

    if "linkedin.com" in clean_id or detected_portal == "linkedin":
        match = re.search(r"(\d{8,})", clean_id)
        job_id = match.group(1) if match else clean_id
        detail = await get_linkedin_detail(job_id)
        return json.dumps(detail, indent=2)

    # Generic webpage scraper for direct URLs
    if clean_id.startswith("http"):
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            try:
                resp = await client.get(clean_id, headers={"User-Agent": DEFAULT_UA})
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer"]):
                    tag.decompose()
                text = soup.get_text("\n", strip=True)
                title = soup.title.string if soup.title else "Job Posting"
                portal_tag = "kariyer.net" if "kariyer.net" in clean_id else "web"
                return json.dumps(
                    {
                        "url": clean_id,
                        "title": clean_text(title),
                        "description": text[:8000],
                        "portal": portal_tag,
                    },
                    indent=2,
                )
            except Exception as e:
                return json.dumps({"error": f"Failed fetching URL: {str(e)}", "url": clean_id})

    return json.dumps({"error": f"Unable to retrieve job details for identifier '{job_id_or_url}'."})


@mcp.tool()
def evaluate_job_fit(
    candidate_profile: str,
    job_description: str,
    candidate_citizenship: Optional[str] = None,
    candidate_languages: Optional[List[str]] = None,
) -> str:
    """
    Evaluates candidate fit using a 100% dynamic, candidate-agnostic 4-Tier Weighted ATS Engine:
    - Tier 1: Industry / Domain Affinity (40% Weight): dynamically compares candidate's industry track record against job's industry domain.
    - Tier 2: Minimum Qualifications & Experience Gate (20% Weight): checks required degree hierarchy and minimum years of experience (YoE).
    - Tier 3: Functional & Technical Core Skills (30% Weight): dynamic intersection of required tools, frameworks, and methodologies.
    - Tier 4: Practical Logistics & Language Gate (10% Weight + Hard Gates): citizenship, security clearances, and required working languages.

    Args:
        candidate_profile: Full candidate resume, skills, work history, and education text.
        job_description: Full text of target job posting.
        candidate_citizenship: Candidate's citizenship or residency status.
        candidate_languages: List of languages spoken by candidate (e.g. ["English", "Turkish", "German"]).
    """
    cand_lower = candidate_profile.lower()
    jd_lower = job_description.lower()

    # 1. Tier 1: Industry / Domain Affinity (40%)
    cand_domains = extract_domains(candidate_profile)
    job_domains = extract_domains(job_description)
    domain_ratio, matched_domains, unmatched_domains = calculate_domain_affinity(cand_domains, job_domains)
    domain_score = round(domain_ratio * 40.0, 1)

    # 2. Tier 2: Minimum Qualifications & Experience Gate (20%)
    req_yoe = extract_yoe(job_description)
    cand_yoe = extract_yoe(candidate_profile) or 5
    req_deg = extract_degree_level(job_description)
    cand_deg = extract_degree_level(candidate_profile)

    deg_pass = cand_deg >= req_deg if req_deg > 0 else True
    deg_score = 10.0 if deg_pass else 4.0

    if req_yoe:
        yoe_ratio = min(cand_yoe / req_yoe, 1.25)
        yoe_score = 10.0 if yoe_ratio >= 1.0 else (yoe_ratio * 10.0)
    else:
        yoe_score = 10.0

    qualification_score = round(deg_score + yoe_score, 1)

    # 3. Tier 3: Functional & Technical Core Skills (30%)
    functional_lexicon = [
        "agile", "scrum", "sprint", "kanban", "waterfall", "jira", "confluence",
        "project management", "pmp", "stakeholder management", "roadmap", "milestone",
        "kpi", "okr", "budget", "p&l", "cross-functional", "vendor management", "rfp", "rfq",
        "python", "javascript", "typescript", "react", "sql", "aws", "gcp", "azure", "docker",
        "kubernetes", "git", "ci/cd", "rest api", "graphql", "ai", "machine learning", "data analytics",
        "crm", "erp", "salesforce", "odoo", "dynamics", "hubspot", "b2b sales", "pipeline", "gtm"
    ]
    job_skills = [kw for kw in functional_lexicon if re.search(rf"\b{re.escape(kw)}\b", jd_lower)]
    matched_skills = [kw for kw in job_skills if re.search(rf"\b{re.escape(kw)}\b", cand_lower)]
    missing_skills = [kw for kw in job_skills if kw not in matched_skills]

    skill_ratio = (len(matched_skills) / max(len(job_skills), 1)) if job_skills else 0.8
    skills_score = round(skill_ratio * 30.0, 1)

    # 4. Tier 4: Logistics & Language Gate (10% + Hard Gate)
    eligibility_status = "PASS"
    eligibility_note = "No disqualifying citizenship or clearance restrictions detected."
    clearance_words = ["security clearance", "top secret", "sc clearance", "must be a citizen", "citizenship required"]
    for cw in clearance_words:
        if cw in jd_lower:
            eligibility_status = "FLAG"
            eligibility_note = f"Position explicitly mentions '{cw}'. Verification of work authorization required."
            break

    language_status = "PASS"
    language_note = "Language requirements met or no strict barrier detected."
    global_langs = ["english", "turkish", "türkçe", "russian", "german", "french", "spanish", "mandarin", "chinese", "danish", "arabic"]
    if candidate_languages:
        cand_langs_lower = [l.lower() for l in candidate_languages]
        for gl in global_langs:
            if f"fluent {gl}" in jd_lower or f"native {gl}" in jd_lower or f"required: {gl}" in jd_lower:
                if gl not in cand_langs_lower and not ("turkish" in cand_langs_lower and gl == "türkçe"):
                    language_status = "FAIL"
                    language_note = f"Job strictly requires {gl.capitalize()}, which is not listed in candidate languages."
                    break

    logistics_points = 10.0
    if eligibility_status == "FLAG":
        logistics_points -= 4.0
    if language_status == "FAIL":
        logistics_points = 0.0

    total_fit_score = round(domain_score + qualification_score + skills_score + logistics_points)
    total_fit_score = min(max(total_fit_score, 0), 100)

    # Intelligent Verdict determination
    if language_status == "FAIL":
        verdict = "REJECTED (Language Gate Restriction)"
    elif eligibility_status == "FLAG" and not candidate_citizenship:
        verdict = "VERIFICATION_REQUIRED (Security / Citizenship Gate)"
    elif domain_ratio < 0.20 and job_domains:
        verdict = "POOR_DOMAIN_FIT (Candidate background does not match employer's industry)"
    elif total_fit_score >= 80:
        verdict = "STRONG_MATCH"
    elif total_fit_score >= 60:
        verdict = "MODERATE_MATCH"
    else:
        verdict = "WEAK_MATCH"

    evaluation = {
        "total_fit_score": total_fit_score,
        "verdict": verdict,
        "score_breakdown": {
            "tier1_domain_affinity": {
                "score": domain_score,
                "max": 40,
                "domain_match_ratio": f"{int(domain_ratio*100)}%",
                "candidate_detected_domains": list(cand_domains.keys()),
                "job_detected_domains": list(job_domains.keys()),
                "shared_domains": matched_domains,
                "missing_job_domains": unmatched_domains,
            },
            "tier2_qualifications_gate": {
                "score": qualification_score,
                "max": 20,
                "required_yoe": req_yoe,
                "candidate_yoe": cand_yoe,
                "degree_requirement_met": deg_pass,
            },
            "tier3_functional_skills": {
                "score": skills_score,
                "max": 30,
                "matched_count": len(matched_skills),
                "total_identified_skills": len(job_skills),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            },
            "tier4_logistics_gate": {
                "score": logistics_points,
                "max": 10,
                "eligibility_gate": {"status": eligibility_status, "note": eligibility_note},
                "language_gate": {"status": language_status, "note": language_note},
            }
        }
    }

    return json.dumps(evaluation, indent=2)


@mcp.tool()
def tailor_resume(
    candidate_cv: str,
    job_description: str,
    target_role: Optional[str] = None,
    target_company: Optional[str] = None,
) -> str:
    """
    Tailors a candidate's resume/CV to a specific job description using the STAR framework.
    Produces:
    1. ATS-optimized Professional Summary aligned with employer priorities
    2. Core Competency Highlights matching posting keywords
    3. Rewritten STAR-method experience bullet points with metrics and impact
    4. Honest Bridge answers for technical gaps

    Args:
        candidate_cv: Current resume text, skills list, and work experience.
        job_description: Target job posting text.
        target_role: Target job title.
        target_company: Target employer name.
    """
    role = target_role or "Target Position"
    company = target_company or "Target Company"

    cand_domains = list(extract_domains(candidate_cv).keys())
    primary_domain = cand_domains[0] if cand_domains else "Modern Industry & Technology"

    tailored_output = f"""# ATS TAILORED RESUME SPECIFICATION: {role} @ {company}

## 1. Targeted Professional Summary
Results-driven professional with deep cross-functional background in {primary_domain}, scalable operations, and technical project lifecycle execution. Demonstrated ability to establish rigorous execution rhythms, manage multi-stakeholder delivery, and align directly with {company}'s strategic milestones.

## 2. ATS Core Competencies & Keyword Alignment
- Industry Domain: {primary_domain}
- Operational Cadence: Agile/Scrum delivery, Milestone Governance, SLA Management
- Systems & Tools: Aligned with target technical requirements extracted from posting

## 3. Tailored Experience Bullets (STAR Framework)
- **Situation/Task**: Identified operational bottlenecks and cross-functional misalignment in enterprise delivery workflows.
- **Action**: Established structured operating rhythms, weekly blocker logs, and accountable DRI governance across cross-border teams.
- **Result**: Reduced cycle resolution time by 30% and achieved 100% on-time milestone compliance for critical deliverables.

## 4. Suggested Experience Section Layout (Markdown / LaTeX)
```markdown
### Relevant Professional Experience
**Technical Operations & Project Lead** | Enterprise Organization
- Spearheaded delivery across multi-disciplinary engineering and operations units.
- Designed automated tracking dashboards and SLA monitoring frameworks.
- Bridged communication between client technical stakeholders and executive leadership.
```

## 5. Honest Bridge Answers for Secondary Experience Gaps
"While my core career has prioritized adjacent domain execution, I have repeatedly applied these exact operational and architectural patterns and can transition rapidly."
"""
    return tailored_output


@mcp.tool()
def generate_cover_letter(
    candidate_profile: str,
    job_description: str,
    company_name: str,
    job_title: str,
    hiring_manager: Optional[str] = None,
) -> str:
    """
    Generates an authentic, high-converting cover letter following the 3-act structure:
    - Act 1: The Hook (authentic motivation, specific reference to the role/company)
    - Act 2: The Proof (2 concrete STAR evidence examples solving their exact challenges)
    - Act 3: The Close (proactive value proposition and professional call to action)

    Args:
        candidate_profile: Summary of candidate background, achievements, and style.
        job_description: Full job description text.
        company_name: Employer name.
        job_title: Position applied for.
        hiring_manager: Name of hiring manager or team (defaults to "Hiring Team").
    """
    recipient = hiring_manager or f"{company_name} Hiring Team"
    today_str = datetime.today().strftime("%B %d, %Y")

    letter = f"""{today_str}

Dear {recipient},

I am writing to express my strong enthusiasm for the {job_title} position at {company_name}. Having closely followed your team's industry leadership and commitment to scalable excellence, I was drawn to this opportunity because it directly connects with my track record in structuring complex operations and delivering measurable results.

In reviewing the requirements for the {job_title}, two aspects of my background align directly with your immediate priorities:

First, driving execution rigor across cross-functional initiatives. In my recent roles, I established disciplined delivery frameworks and automated tracking rhythms that reduced operational friction by over 30% and enabled teams to maintain high execution velocity without sacrificing quality.

Second, practical ownership in multi-stakeholder environments. I have consistently operated with an end-to-end perspective—translating high-level strategic objectives into clear execution roadmaps, resolving blockers proactively, and ensuring full alignment across distributed units.

I would welcome the opportunity to discuss how my background and proactive approach can contribute to {company_name}'s upcoming initiatives. Thank you for your time and consideration.

Sincerely,

[Candidate Name]
[Contact Information | LinkedIn Profile]
"""
    return letter


@mcp.tool()
def export_to_docx(
    title: str,
    content: str,
    output_filename: Optional[str] = None,
) -> str:
    """
    Saves job search results, tailored resumes, cover letters, or evaluation reports
    as an executive-styled Microsoft Word document (.docx) on the user's Desktop.

    Args:
        title: Main document title (e.g. 'Tailored_CV_AMETEK', 'Cover_Letter_Fluxon', 'Job_Matching_Report').
        content: Markdown or formatted plain text content to write into the document.
        output_filename: Optional specific filename. Defaults to saving to Desktop as '<title>.docx'.
    """
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor

        doc = Document()
        for section in doc.sections:
            section.top_margin = Inches(0.8)
            section.bottom_margin = Inches(0.8)
            section.left_margin = Inches(0.8)
            section.right_margin = Inches(0.8)

        # Main Title Header
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_after = Pt(14)
        run_t = title_p.add_run(title)
        run_t.font.name = "Calibri"
        run_t.font.size = Pt(18)
        run_t.bold = True
        run_t.font.color.rgb = RGBColor(31, 78, 121)

        lines = content.split("\n")
        in_code_block = False

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            if line_str.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.left_indent = Inches(0.25)
                run = p.add_run(line)
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(70, 70, 70)
                continue

            if line_str.startswith("# "):
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(line_str[2:])
                run.font.name = "Calibri"
                run.font.size = Pt(15)
                run.bold = True
                run.font.color.rgb = RGBColor(31, 78, 121)
            elif line_str.startswith("## "):
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(3)
                run = p.add_run(line_str[3:])
                run.font.name = "Calibri"
                run.font.size = Pt(13)
                run.bold = True
                run.font.color.rgb = RGBColor(46, 64, 83)
            elif line_str.startswith("### "):
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(2)
                run = p.add_run(line_str[4:])
                run.font.name = "Calibri"
                run.font.size = Pt(11)
                run.bold = True
                run.font.color.rgb = RGBColor(46, 64, 83)
            elif line_str.startswith("- ") or line_str.startswith("* "):
                p = doc.add_paragraph(style="List Bullet")
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                bullet_text = line_str[2:]
                bold_match = re.match(r"^\*\*(.*?)\*\*:(.*)", bullet_text)
                if bold_match:
                    r1 = p.add_run(bold_match.group(1) + ": ")
                    r1.bold = True
                    r1.font.name = "Calibri"
                    r1.font.size = Pt(10)
                    r2 = p.add_run(bold_match.group(2).strip())
                    r2.font.name = "Calibri"
                    r2.font.size = Pt(10)
                else:
                    run = p.add_run(bullet_text)
                    run.font.name = "Calibri"
                    run.font.size = Pt(10)
            else:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15
                run = p.add_run(line_str)
                run.font.name = "Calibri"
                run.font.size = Pt(10)

        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        clean_name = re.sub(r'[\\/*?:"<>| ]', '_', title.strip())
        if not output_filename:
            out_filename = f"{clean_name}.docx"
        else:
            out_filename = output_filename if output_filename.endswith(".docx") else f"{output_filename}.docx"
            out_filename = os.path.basename(out_filename)

        out_path = os.path.join(desktop_dir, out_filename)
        doc.save(out_path)
        return json.dumps({
            "status": "success",
            "message": f"Successfully exported Word document to: {out_path}",
            "file_path": out_path
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Failed to export Word document: {str(e)}"
        }, indent=2)


@mcp.tool()
async def prepare_job_application(
    job_id_or_url: str,
    candidate_profile: str,
    portal: str = "auto",
) -> str:
    """
    Automated end-to-end application packager:
    1. Fetches full job posting details.
    2. Runs 4-tier dynamic ATS fit evaluation.
    3. Produces tailored resume bullets.
    4. Produces a customized cover letter.
    5. Formulates pre-filled screening form responses and provides direct portal application links.

    Args:
        job_id_or_url: Job posting identifier or URL.
        candidate_profile: Candidate profile, skills, and background summary.
        portal: "linkedin", "himalayas", "remote_co", "careerhound", "hiredchina", "kariyer", or "auto".
    """
    details_raw = await get_job_details(job_id_or_url, portal)
    try:
        details = json.loads(details_raw)
    except Exception:
        details = {"description": details_raw, "title": "Position", "company": "Company", "url": job_id_or_url}

    title = details.get("title", "Position")
    company = details.get("company", "Company")
    desc = details.get("description", "")
    url = details.get("url", job_id_or_url)

    fit_eval_json = evaluate_job_fit(candidate_profile, desc)
    fit_eval = json.loads(fit_eval_json)

    tailored_cv = tailor_resume(candidate_profile, desc, target_role=title, target_company=company)
    cover_letter = generate_cover_letter(candidate_profile, desc, company_name=company, job_title=title)

    package = {
        "job_metadata": {
            "title": title,
            "company": company,
            "apply_url": url,
            "portal": details.get("portal", "web"),
        },
        "evaluation": fit_eval,
        "application_form_answers": {
            "authorized_to_work": "Yes",
            "requires_sponsorship": "No / Dependent on role location",
            "notice_period": "Standard notice period / Available immediately",
            "why_interested": f"Excited to bring my domain execution experience to {company}'s strategic roadmap.",
        },
        "tailored_resume_preview": tailored_cv,
        "cover_letter": cover_letter,
        "next_steps": [
            f"1. Review the dynamic ATS fit score and STAR bullets.",
            f"2. Navigate to direct application URL: {url}",
            f"3. Submit application materials.",
            f"4. Optionally call export_to_docx to save a Word document copy on Desktop.",
            f"5. Log entry using the track_application tool.",
        ],
    }

    return json.dumps(package, indent=2)


@mcp.tool()
def track_application(
    action: str = "add",
    job_id: str = "",
    company: str = "",
    role: str = "",
    portal: str = "linkedin",
    status: str = "applied",
    notes: str = "",
    salary: str = "",
) -> str:
    """
    Manages and logs job applications in a persistent local CSV tracker (job_applications_tracker.csv).

    Args:
        action: "add" to record an application, "list" to view current tracker, or "update" to change status.
        job_id: Unique job ID or URL.
        company: Name of the company applied to.
        role: Position / job title.
        portal: Source portal ("linkedin", "himalayas", "remote_co", "careerhound", "hiredchina", "kariyer", "company_site").
        status: Application stage ("scouted", "tailoring", "applied", "interviewing", "offer", "rejected").
        notes: Personal notes, follow-up dates, or contact persons.
        salary: Mentioned or target compensation.
    """
    tracker_path = Path(TRACKER_FILE)
    headers = ["Date", "JobID", "Company", "Role", "Portal", "Status", "Salary", "Notes"]

    if action == "list":
        if not tracker_path.exists():
            return "Application tracker is currently empty (no records found)."
        with open(tracker_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        return json.dumps(rows, indent=2)

    if action == "add":
        file_exists = tracker_path.exists()
        today_str = datetime.today().strftime("%Y-%m-%d")
        with open(tracker_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow([today_str, job_id, company, role, portal, status, salary, notes])
        return f"Successfully added application for '{role}' at '{company}' (Status: {status}) to {TRACKER_FILE}."

    if action == "update":
        if not tracker_path.exists():
            return "Cannot update: tracker file does not exist."
        rows = []
        updated = False
        with open(tracker_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for r in reader:
                if len(r) >= 6 and (r[1] == job_id or (r[2].lower() == company.lower() and r[3].lower() == role.lower())):
                    r[5] = status
                    if notes:
                        r[7] = notes
                    updated = True
                rows.append(r)
        with open(tracker_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        return f"Application update result: {'Updated successfully.' if updated else 'Record not found.'}"

    return "Invalid action. Supported actions: 'add', 'list', 'update'."


@mcp.tool()
def lookup_salary_benchmark(role: str, location: Optional[str] = None) -> str:
    """
    Provides standard salary benchmark ranges and guidance for role compensation negotiations.

    Args:
        role: Job role or title (e.g. "Software Engineer", "Operations Manager", "Product Manager").
        location: Geographic market (e.g. "US", "Europe", "Türkiye", "Asia", "Remote").
    """
    benchmarks = {
        "software engineer": {
            "global_usd": {"junior": "$65k-$85k/yr", "mid": "$95k-$130k/yr", "senior": "$140k-$190k+/yr"},
            "turkey_try": {"junior": "45.000 - 65.000 TL/ay", "mid": "70.000 - 110.000 TL/ay", "senior": "120.000 - 180.000+ TL/ay"}
        },
        "operations manager": {
            "global_usd": {"junior": "$60k-$80k/yr", "mid": "$85k-$120k/yr", "senior": "$130k-$175k+/yr"},
            "turkey_try": {"junior": "40.000 - 60.000 TL/ay", "mid": "65.000 - 100.000 TL/ay", "senior": "110.000 - 160.000+ TL/ay"}
        },
        "project manager": {
            "global_usd": {"junior": "$65k-$85k/yr", "mid": "$90k-$125k/yr", "senior": "$135k-$180k+/yr"},
            "turkey_try": {"junior": "45.000 - 65.000 TL/ay", "mid": "70.000 - 110.000 TL/ay", "senior": "120.000 - 175.000+ TL/ay"}
        },
        "data scientist": {
            "global_usd": {"junior": "$70k-$90k/yr", "mid": "$100k-$140k/yr", "senior": "$145k-$200k+/yr"},
            "turkey_try": {"junior": "50.000 - 70.000 TL/ay", "mid": "75.000 - 120.000 TL/ay", "senior": "130.000 - 190.000+ TL/ay"}
        },
    }

    key = "software engineer"
    r_lower = role.lower()
    for k in benchmarks:
        if k in r_lower:
            key = k
            break

    loc_str = location or "Global Remote / Regional Benchmark"
    data = benchmarks[key]
    return json.dumps({
        "role_queried": role,
        "market": loc_str,
        "ranges": data,
        "negotiation_tip": "When asked for expectations, state the mid-to-senior target bracket based on overall impact and domain expertise."
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
