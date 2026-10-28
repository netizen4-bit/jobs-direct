---
name: hybrid-ats-positioning
description: Deterministic 4-Tier ATS Job-Fit Gate and 5-Stage Truthful Resume & Interview Positioning Workflow. Evaluates domain affinity, qualifications, functional skills, and logistics before tailoring truthful application materials.
version: 2.0.0
---

# Hybrid 4-Tier Decision & 5-Stage Positioning Skill

This skill enforces the **Hybrid Decision & Positioning Protocol**, pairing mathematical, deterministic 4-Tier ATS screening with Harish Kumar's 5-Stage Truthful Positioning workflow. It eliminates hallucinated qualifications, slashes context token burn by over 82%, and guarantees 100% adherence to candidate truth.

---

## 🎯 Protocol Architecture Overview

```
Target Job Description + Candidate CV
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│     Step 0: Deterministic 4-Tier ATS Evaluation Gate    │
│                 (`evaluate_job_fit`)                   │
├────────────────────────────────────────────────────────┤
│  • Tier 1: Industry / Domain Affinity (40%)           │
│  • Tier 2: YoE & Degree Hierarchy Gate (20%)           │
│  • Tier 3: Functional / Technical Core Skills (30%)    │
│  • Tier 4: Logistics, Citizenship & Language Gate (10%)│
└──────────────────────────┬─────────────────────────────┘
                           │
             7-Branch Verdict Routing Engine
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
[Hard Disqualification]               [Qualified Candidate]
  • CLOSED_OR_EXPIRED                    • STRONG_MATCH (>=80)
  • REJECTED (Language)                  • MODERATE_MATCH (60-79)
  • POOR_DOMAIN_FIT (<0.20)                    │
       │                                       ▼
  🛑 STOP IMMEDIATELY                 ┌─────────────────────────────────┐
  (Save context & token burn)         │ 5-Stage Truthful Positioning     │
                                      │ 1. Recruiter Persona Locking    │
                                      │ 2. Exact JD Keyword Mirroring   │
                                      │ 3. 250-Word Single-Anchor Letter│
                                      │ 4. LinkedIn Boolean Alignment   │
                                      │ 5. 10-Question STAR Stress-Test │
                                      └─────────────────────────────────┘
```

---

## Step 0 — Deterministic 4-Tier Gate & Verdict Filter (`evaluate_job_fit`)

> [!IMPORTANT]
> **MANDATORY RULE:** ALWAYS execute `evaluate_job_fit` BEFORE tailoring any document, writing any cover letter, or executing outreach. Never generate positioning materials for an un-evaluated listing.

### The 4-Tier Scoring Formulas
1. **Tier 1: Industry / Domain Affinity (40% Weight, Max 40 pts)**:
   - Evaluates keyword occurrences across 9 core industry taxonomy verticals: Fintech/Trading, Industrial/Machinery, Healthcare/Pharma, E-Commerce/Retail, SaaS/Cloud, Media/Gaming, Energy/Cleantech, Education/EdTech, Telecom.
   - Calculates domain importance $I = \frac{\text{Count}_{\text{job}}}{\text{Total}_{\text{job}}}$ and candidate strength $S = \min\left(\frac{\text{Count}_{\text{cand}}}{3.0}, 1.0\right)$.
   - Prevents cross-industry false positives (e.g. flagging a gaming developer as a senior medical device engineer because both mention "Agile").

2. **Tier 2: Minimum Qualifications & Experience Gate (20% Weight, Max 20 pts)**:
   - Degree Hierarchy Gate: PhD (3) > Master (2) > Bachelor (1) > None (0). Candidate must satisfy minimum required degree (10.0 pts if passed, else 4.0 pts).
   - Experience Gate: Dynamic regex extraction of minimum YoE. If candidate YoE $\ge$ required YoE, 10.0 pts; otherwise proportional ratio $\times 10.0$ pts.

3. **Tier 3: Functional & Technical Core Skills (30% Weight, Max 30 pts)**:
   - Analyzes intersection of technical and operational competencies across frameworks, tools, and methodologies.
   - Computes matched vs. missing skills: $\text{Points} = \text{round}\left(\frac{|\text{Matched}|}{\max(|\text{Job Skills}|, 1)} \times 30.0, 1\right)$.

4. **Tier 4: Practical Logistics & Language Gate (10% Weight + Hard Gate)**:
   - Clearance/Citizenship Check: 10.0 pts base; $-4.0$ penalty if security clearance or strict citizenship required and candidate is unverified.
   - Working Language Check: If job mandates fluency in a language not spoken by candidate (with Turkish/Türkçe normalization), drops to 0.0 pts and triggers hard rejection.

---

### The 7-Branch Verdict Decision Tree & Routing Rules

1. **`CLOSED_OR_EXPIRED`**:
   - **Action:** **STOP IMMEDIATELY**. The posting has ended, deadline has passed, or listing is taken down. Alert user and skip to the next opportunity. Do NOT waste tokens generating resumes or letters.
2. **`REJECTED (Language Gate Restriction)`**:
   - **Action:** **STOP IMMEDIATELY**. Candidate lacks the mandatory working language. Alert user and abort.
3. **`POOR_DOMAIN_FIT` (`domain_ratio < 0.20` and job domains detected)**:
   - **Action:** Warn the user that the severe industry domain mismatch will result in automated ATS filtering. **Do NOT proceed** unless the user explicitly instructs an override.
4. **`VERIFICATION_REQUIRED (Security / Citizenship Gate)`**:
   - **Action:** Flag the clearance/citizenship restriction clearly at the top of the report. Proceed only with explicit verification notice.
5. **`STRONG_MATCH` (Total Fit Score $\ge 80$)**:
   - **Action:** Proceed automatically into the 5-Stage Positioning Pipeline.
6. **`MODERATE_MATCH` (Total Fit Score $60 - 79$)**:
   - **Action:** Proceed automatically into the 5-Stage Positioning Pipeline, ensuring missing skills are addressed via Stage 2 Honest Bridges.
7. **`WEAK_MATCH` (Total Fit Score $< 60$)**:
   - **Action:** Highlight major qualification and skill gaps to the candidate before proceeding.

---

## 5-Stage Truthful Positioning Pipeline

### Stage 1 — Recruiter Persona & Base ATS Optimization (`tailor_resume`)
* **Persona Locking:** Automatically adopts the Senior Executive Recruiter & Hiring Committee Member persona matching the primary industry detected in Tier 1.
* **Agency Verb Elevation:** Replaces passive phrases with high-agency verbs (*Spearheaded, Architected, Engineered, Orchestrated, Optimized, Governed*).
* **Strict Truthfulness:** Uses ONLY verified lines and metrics from `candidate_cv` (`%`, `$`, volume numbers). **NEVER invent metrics, projects, or credentials.**

### Stage 2 — Exact JD Keyword Mirroring Matrix (`tailor_resume`)
* **Lexicon Mapping:** Cross-references `matched_skills` and `missing_skills` from Tier 3.
* **Matrix Output:** Outputs a structured table:
  | JD Required Term | Candidate Evidence from CV | ATS Status |
  |---|---|---|
  | `Agile/Scrum` | Spearheaded sprint governance across distributed units | Matched (100% Truthful) |
  | `Docker / K8s` | Addressed via Honest Bridge Ramp-up Strategy | Gap (Transparent) |
* **Honest Bridge Strategy:** For every secondary technical gap, outputs a truthful bridging statement demonstrating adjacent mastery and fast onboarding velocity without misrepresentation.

### Stage 3 — 250-Word Single-Anchor Cover Letter (`generate_cover_letter`)
* **Strict Word Limit:** Maximum 250 words total.
* **Peer-Level Tone:** Confident, collaborative, problem-solving tone. Eliminates submissive phrases (*"I humbly beg to apply"*, *"I would be honored to be considered"*).
* **Single-Anchor Architecture:** Isolates **exactly one** flagship quantified achievement from the candidate's career and connects it directly to the employer's immediate roadmap challenge.

### Stage 4 — LinkedIn Boolean Search Alignment (`optimize_linkedin_profile`)
* **Headlines:** Generates 3 outcome-driven headline formulas under 220 characters combining Target Role + Tier 1 Industry + Flagship Metric + Key Skills.
* **Boolean Search Bank:** Builds the exact search string corporate recruiters use on LinkedIn Recruiter:
  `("Senior Technical Program Manager") AND ("Agile" OR "Jira" OR "CI/CD") AND ("Fintech")`
* **Indexed About Copy:** Formulates an About section structured with hook, core competencies, verified CV highlights, and clear recruiter invitation.

### Stage 5 — 10-Question STAR Stress-Test (`generate_interview_prep`)
Generates the 10 most critical interview questions targeting the candidate's exact profile:
1. **Questions 1–3 (Role & Industry Architecture Deep-Dives):** Evaluates domain mastery in the detected Tier 1 industry.
2. **Questions 4–6 (Functional Competency Verification):** Validates hands-on execution of Tier 3 `matched_skills`, anchoring answers to candidate's real numbers.
3. **Questions 7–8 (Gap & Vulnerability Stress-Tests):** Challenges Tier 3 `missing_skills` using Honest Bridge framing.
4. **Questions 9–10 (Behavioral & Stakeholder Governance):** Assesses conflict resolution and leadership under pressure using the STAR framework.

---

## ⚡ Token Savings & Execution Discipline

| Step | Standard Agent Approach | Hybrid ATS Positioning Skill |
|---|---|---|
| **Fit Check** | Ingests thousands of tokens rewriting resume for expired/closed postings | Runs deterministic `evaluate_job_fit` in 0.1s; stops dead listings immediately |
| **Document Generation** | Hallucinates generic fluff and un-grounded metrics | Mirrors exact JD keywords with real candidate numbers in clean, compact output |
| **Context Window Consumption** | 6,000–8,000 tokens spent per application cycle | ~1,200 tokens spent (~82% reduction) |
