"""Rule-based recruiter insights: verdicts, strengths/risks, interview questions."""

from typing import Dict, List

QUESTION_BANK: Dict[str, str] = {
    "python": "Walk me through a Python project where you optimized performance. What did you measure?",
    "data science / ml": "How do you choose between a simple model and a complex one for a business problem?",
    "javascript": "Explain the event loop and how you debug async issues in production.",
    "java": "How do you handle memory management and concurrency in a Java service?",
    "aws": "Describe an AWS architecture you designed. How did you handle cost and failure?",
    "azure": "Which Azure services have you used in production and why?",
    "google cloud": "How have you used GCP services to scale a workload?",
    "docker": "How do you keep Docker images small and secure?",
    "kubernetes": "Explain how you'd roll out a zero-downtime deployment on Kubernetes.",
    "sql": "How would you find and fix a slow SQL query?",
    "nosql": "When would you pick NoSQL over a relational database?",
    "git": "How do you resolve a tricky merge conflict on a shared branch?",
    "ci/cd": "Describe a CI/CD pipeline you built end to end.",
    "agile": "How do you handle changing requirements mid-sprint?",
    "leadership": "Tell me about a time you led a team through a difficult delivery.",
    "communication": "Describe how you explained a technical trade-off to a non-technical stakeholder.",
}


def verdict(score: float) -> Dict[str, str]:
    if score >= 0.75:
        return {"label": "Excellent Match", "tone": "great", "emoji": "🏆", "action": "Fast-track to interview"}
    if score >= 0.6:
        return {"label": "Strong Match", "tone": "good", "emoji": "✅", "action": "Recommend for interview"}
    if score >= 0.45:
        return {"label": "Potential Match", "tone": "mid", "emoji": "🟡", "action": "Review manually"}
    return {"label": "Weak Match", "tone": "low", "emoji": "⚠️", "action": "Likely not a fit"}


def build_insights(row: Dict, gap: Dict[str, List[str]]) -> Dict[str, List[str]]:
    strengths, risks = [], []
    if row["similarity"] >= 0.55:
        strengths.append(f"High semantic alignment with the job ({row['similarity']*100:.0f}%).")
    if row["keyword_coverage"] >= 0.6:
        strengths.append(f"Covers {row['keyword_coverage']*100:.0f}% of required keywords.")
    if len(gap["matched"]) >= 4:
        strengths.append(f"Matches {len(gap['matched'])} required skills: {', '.join(gap['matched'][:4])}.")
    if row["experience_score"] >= 0.9:
        strengths.append("Meets or exceeds the experience requirement.")
    if row["education_score"] >= 0.9:
        strengths.append("Education matches the requirement.")
    if row["certification_score"] >= 0.7:
        strengths.append("Holds relevant certifications.")
    if row["similarity"] < 0.35:
        risks.append("Low overall semantic match with the role.")
    if gap["missing"]:
        risks.append(f"Missing {len(gap['missing'])} skill(s): {', '.join(gap['missing'][:4])}.")
    if row["experience_score"] < 0.6:
        risks.append("Experience appears below the stated requirement.")
    if row["education_score"] == 0.0:
        risks.append("Required degree level not found.")
    if not strengths:
        strengths.append("No standout strengths detected for this role.")
    if not risks:
        risks.append("No major risks detected.")
    return {"strengths": strengths, "risks": risks}


def interview_questions(gap: Dict[str, List[str]], limit: int = 5) -> List[str]:
    qs = []
    for skill in gap["missing"]:
        q = QUESTION_BANK.get(skill.lower())
        if q:
            qs.append(f"[Gap: {skill}] {q}")
    for skill in gap["matched"]:
        q = QUESTION_BANK.get(skill.lower())
        if q:
            qs.append(f"[Verify: {skill}] {q}")
    if not qs:
        qs = ["Tell me about the project you're most proud of and your specific contribution.",
              "What is the hardest technical problem you solved recently?"]
    return qs[:limit]
