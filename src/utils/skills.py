"""Skill detection, skill-gap analysis, contact extraction and ATS checks."""

import re
from typing import Dict, List, Optional

from src.utils.keyword_mapping import SKILL_GROUPS

# Friendly display names for canonical skill groups
GROUP_LABELS: Dict[str, str] = {
    "python": "Python", "data_science": "Data Science / ML", "javascript": "JavaScript",
    "java": "Java", "dotnet": ".NET / C#", "aws": "AWS", "azure": "Azure", "gcp": "Google Cloud",
    "docker": "Docker", "kubernetes": "Kubernetes", "sql": "SQL", "nosql": "NoSQL",
    "git": "Git", "ci_cd": "CI/CD", "agile": "Agile",
}

# Extra standalone skills worth detecting (not in groups)
EXTRA_SKILLS: List[str] = [
    "html", "css", "react", "angular", "vue", "typescript", "c++", "golang", "rust", "php", "ruby",
    "linux", "bash", "rest", "graphql", "microservices", "terraform", "ansible", "tableau", "power bi",
    "excel", "nlp", "computer vision", "spark", "hadoop", "kafka", "airflow", "figma", "selenium",
    "leadership", "communication", "problem solving", "teamwork", "project management", "testing",
]


DISPLAY = {"html": "HTML", "css": "CSS", "nlp": "NLP", "php": "PHP", "rest": "REST", "graphql": "GraphQL",
           "typescript": "TypeScript", "javascript": "JavaScript", "power bi": "Power BI", "golang": "Go",
           "c++": "C++", "bash": "Bash", "rust": "Rust", "ruby": "Ruby"}


def _has_term(text_lower: str, term: str) -> bool:
    term = term.lower().strip()
    if not term:
        return False
    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return re.search(pattern, text_lower) is not None


def detect_skills(text: str) -> List[str]:
    """Return display names of skills found in text (group-aware, word-boundary safe)."""
    low = text.lower()
    found: List[str] = []
    for group, terms in SKILL_GROUPS.items():
        # Skip very ambiguous short tokens when deciding group presence
        strong = [t for t in terms if len(t) > 2 or t in ("ml", "ai", "js", "s3")]
        if any(_has_term(low, t) for t in strong):
            found.append(GROUP_LABELS.get(group, group.title()))
    for s in EXTRA_SKILLS:
        if _has_term(low, s):
            found.append(DISPLAY.get(s, s.upper() if len(s) <= 4 and s not in ("rest", "rust", "ruby") else s.title()))
    seen, out = set(), []
    for s in found:
        if s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out


def skill_gap(jd_skills: List[str], resume_skills: List[str]) -> Dict[str, List[str]]:
    r = {s.lower() for s in resume_skills}
    matched = [s for s in jd_skills if s.lower() in r]
    missing = [s for s in jd_skills if s.lower() not in r]
    extra = [s for s in resume_skills if s.lower() not in {j.lower() for j in jd_skills}]
    return {"matched": matched, "missing": missing, "extra": extra}


def extract_contact(text: str, filename: str = "") -> Dict[str, Optional[str]]:
    email = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone = None
    for m in re.finditer(r"\+?\d[\d\s().-]{8,16}\d", text):
        if len(re.sub(r"\D", "", m.group(0))) >= 10:
            phone = m
            break
    linkedin = re.search(r"linkedin\.com/in/[\w-]+", text.lower())
    github = re.search(r"github\.com/[\w-]+", text.lower())
    # Name guess: first short line of letters, else filename
    name = None
    for line in re.split(r"[\n]", text[:300]):
        line = line.strip()
        if 3 <= len(line) <= 40 and re.fullmatch(r"[A-Za-z][A-Za-z .'-]+", line) and len(line.split()) <= 4:
            name = line.title()
            break
    if not name:
        base = re.sub(r"\.(pdf|docx|txt)$", "", filename, flags=re.I)
        name = re.sub(r"[_\-]+", " ", base).strip().title() or "Candidate"
    return {
        "name": name,
        "email": email.group(0) if email else None,
        "phone": phone.group(0).strip() if phone else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "github": github.group(0) if github else None,
    }


ACTION_VERBS = [
    "led", "built", "developed", "designed", "implemented", "launched", "optimized", "improved",
    "created", "managed", "delivered", "automated", "reduced", "increased", "architected", "deployed",
    "mentored", "analyzed", "migrated", "integrated",
]
SECTIONS = {
    "Summary": ["summary", "objective", "profile", "about me"],
    "Experience": ["experience", "employment", "work history", "internship"],
    "Education": ["education", "academic", "qualification"],
    "Skills": ["skills", "technologies", "tech stack", "competencies"],
    "Projects": ["projects", "portfolio"],
    "Certifications": ["certification", "certificate", "courses"],
}


def ats_check(text: str, contact: Dict[str, Optional[str]]) -> Dict:
    """Heuristic ATS-friendliness score (0-100) with human-readable checks."""
    low = text.lower()
    words = len(text.split())
    checks = []

    def add(label: str, ok: bool, pts: int, tip: str):
        checks.append({"label": label, "ok": ok, "points": pts if ok else 0, "max": pts, "tip": tip})

    add("Email present", bool(contact.get("email")), 10, "Add a professional email address.")
    add("Phone present", bool(contact.get("phone")), 5, "Add a reachable phone number.")
    add("LinkedIn / GitHub link", bool(contact.get("linkedin") or contact.get("github")), 5, "Link LinkedIn or GitHub.")
    for sec, keys in SECTIONS.items():
        weight = 10 if sec in ("Experience", "Education", "Skills") else 5
        add(f"{sec} section", any(k in low for k in keys), weight, f"Add a clear '{sec}' heading.")
    verbs = sum(1 for v in ACTION_VERBS if _has_term(low, v))
    add("Strong action verbs", verbs >= 4, 10, "Start bullets with verbs like built, led, optimized.")
    nums = len(re.findall(r"\b\d+(?:\.\d+)?\s*(?:%|x|k|\+|users|clients|projects|ms|million)", low))
    add("Quantified achievements", nums >= 2, 10, "Add numbers/metrics (e.g. 'cut latency by 35%').")
    add("Ideal length (150-1200 words)", 150 <= words <= 1200, 10, "Aim for 1-2 pages of focused content.")
    total_max = sum(c["max"] for c in checks) or 1
    score = round(100 * sum(c["points"] for c in checks) / total_max)
    return {"score": score, "checks": checks, "words": words}
