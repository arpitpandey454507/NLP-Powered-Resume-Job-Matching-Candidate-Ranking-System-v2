import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"
os.environ["USE_TF"] = "0"
os.environ["USE_JAX"] = "0"

import io
import json
import time
from typing import Dict, List, Tuple

import pandas as pd
import streamlit as st

from src.utils.parser import extract_text_from_file
from src.utils.resume_extractor import extract_all_resume_features
from src.utils.skills import detect_skills, skill_gap, extract_contact, ats_check
from src.processing.nlp import extract_keywords, normalize_text
from src.processing.embedding import get_embedder, embed_texts, cosine_similarity_matrix
from src.scoring import compute_scores
from src.insights import verdict, build_insights, interview_questions
from src.samples import SAMPLE_JD, SAMPLE_RESUMES
from src.report import build_html_report
from src.ui.styles import CSS
from src.ui import components as ui

st.set_page_config(page_title="AI Resume Screener", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
st.markdown(CSS, unsafe_allow_html=True)


def md(markup: str) -> None:
    st.markdown(ui.clean(markup), unsafe_allow_html=True)


@st.cache_resource(show_spinner=False)
def load_embedder():
    return get_embedder()


# ------------------------------------------------------------------ weights / presets
PRESETS = {
    "🎯 Balanced": (0.40, 0.30, 0.15, 0.10, 0.05),
    "💼 Senior Role": (0.30, 0.25, 0.30, 0.10, 0.05),
    "🚀 Entry Level": (0.35, 0.40, 0.05, 0.15, 0.05),
    "☁️ Cloud Role": (0.30, 0.30, 0.15, 0.10, 0.15),
}
W_KEYS = ["w_sim", "w_kw", "w_exp", "w_edu", "w_cert"]
for k, v in zip(W_KEYS, PRESETS["🎯 Balanced"]):
    st.session_state.setdefault(k, v)
st.session_state.setdefault("jd_text", "")
st.session_state.setdefault("demo_mode", False)


def apply_preset(name: str) -> None:
    for k, v in zip(W_KEYS, PRESETS[name]):
        st.session_state[k] = v


def load_demo() -> None:
    st.session_state["jd_text"] = SAMPLE_JD
    st.session_state["demo_mode"] = True


def clear_demo() -> None:
    st.session_state["demo_mode"] = False
    st.session_state["jd_text"] = ""
    st.session_state.pop("results", None)


# ------------------------------------------------------------------ sidebar
with st.sidebar:
    md('<div style="text-align:center;padding:6px 0 10px"><div style="font-size:2.4rem">🤖</div>'
       '<div style="font-family:Space Grotesk,Inter,sans-serif;font-weight:700;font-size:1.25rem">Resume Screener <span class="grad">AI</span></div>'
       '<div class="muted">Smart hiring dashboard</div></div>')
    st.markdown("##### ⚡ Quick Presets")
    c1, c2 = st.columns(2)
    names = list(PRESETS)
    for i, n in enumerate(names):
        (c1 if i % 2 == 0 else c2).button(n, use_container_width=True, on_click=apply_preset, args=(n,), key=f"preset_{i}")

    st.markdown("##### 🎚️ Scoring Weights")
    w_sim = st.slider("Semantic Similarity", 0.0, 1.0, step=0.05, key="w_sim", help="Overall meaning match between JD and resume")
    w_kw = st.slider("Keyword Coverage", 0.0, 1.0, step=0.05, key="w_kw", help="Share of JD keywords/skills found in the resume")
    w_exp = st.slider("Experience Match", 0.0, 1.0, step=0.05, key="w_exp", help="Years of experience vs requirement")
    w_edu = st.slider("Education Match", 0.0, 1.0, step=0.05, key="w_edu", help="Degree level vs requirement")
    w_cert = st.slider("Certifications", 0.0, 1.0, step=0.05, key="w_cert", help="Relevant certifications")
    total_w = w_sim + w_kw + w_exp + w_edu + w_cert
    if total_w == 0:
        st.warning("Increase at least one weight to proceed.")
    else:
        parts = {"Semantic": w_sim, "Keywords": w_kw, "Experience": w_exp, "Education": w_edu, "Certs": w_cert}
        md(ui.bars({k: v / total_w for k, v in parts.items()}))
        st.caption(f"Weights are auto-normalised (total {total_w:.2f}).")

    st.divider()
    st.markdown("##### 🔑 Keyword Options")
    num_keywords = st.slider("Top keywords to extract", 5, 30, 15)
    use_synonyms = st.checkbox("Use skill synonyms", value=True, help="Group related skills (Python → Django, Pandas)")
    shortlist_cut = st.slider("Shortlist threshold", 0.30, 0.90, 0.60, 0.05, help="Candidates at or above this score are shortlisted")
    st.divider()
    if st.session_state["demo_mode"]:
        st.button("🧹 Exit demo mode", on_click=clear_demo, use_container_width=True)
    else:
        st.button("✨ Load demo data", on_click=load_demo, use_container_width=True,
                  help="Instantly fills a sample JD and 4 sample resumes - perfect for presentations")

# ------------------------------------------------------------------ hero + inputs
md(ui.hero())

left, right = st.columns([1.15, 1], gap="large")
with left:
    md(ui.section("Job Description", "📝"))
    jd_text = st.text_area("Paste the job description", key="jd_text", height=250, label_visibility="collapsed",
                           placeholder="Responsibilities...\nRequirements (e.g. 4+ years experience, Python, AWS)...\nNice to haves...")
    st.caption(f"{len(jd_text.split())} words")
with right:
    md(ui.section("Upload Resumes", "📂"))
    if st.session_state["demo_mode"]:
        md('<div class="glass"><b>✨ Demo mode is ON</b><br><span class="muted">Using 4 built-in sample resumes: '
           + ", ".join(SAMPLE_RESUMES) + ". Upload your own files after exiting demo mode.</span></div>")
        uploaded_files = []
    else:
        uploaded_files = st.file_uploader("Upload resume files", type=["pdf", "docx", "txt"], accept_multiple_files=True,
                                          label_visibility="collapsed")
        if uploaded_files:
            st.caption(f"{len(uploaded_files)} file(s) ready")

go = st.button("🚀  Analyze Candidates", type="primary", use_container_width=True)


# ------------------------------------------------------------------ analysis
def run_analysis() -> None:
    if not jd_text.strip():
        st.error("Please provide a job description.")
        return
    sources: List[Tuple[str, str]] = []
    if st.session_state["demo_mode"]:
        sources = list(SAMPLE_RESUMES.items())
    else:
        if not uploaded_files:
            st.error("Please upload at least one resume file (or try ✨ Load demo data).")
            return
        for uf in uploaded_files:
            try:
                sources.append((uf.name, extract_text_from_file(uf.name, io.BytesIO(uf.getvalue()))))
            except Exception as e:  # noqa: BLE001
                st.warning(f"Failed to parse {uf.name}: {e}")
    if not sources:
        st.error("No resumes could be processed.")
        return

    with st.status("Analysing candidates...", expanded=True) as status:
        st.write("🧠 Loading language models...")
        embedder = load_embedder()
        st.write("📝 Reading the job description...")
        jd_clean = normalize_text(jd_text)
        jd_keywords = extract_keywords(jd_clean, top_k=num_keywords, use_synonyms=use_synonyms)
        jd_skills = detect_skills(jd_text)

        records: List[Dict] = []
        meta: Dict[str, Dict] = {}
        for i, (fname, raw) in enumerate(sources, 1):
            st.write(f"📄 Parsing resume {i}/{len(sources)}: {fname}")
            clean = normalize_text(raw)
            feats = extract_all_resume_features(clean)
            records.append({
                "filename": fname, "text": clean,
                "keywords": extract_keywords(clean, top_k=num_keywords, use_synonyms=use_synonyms),
                "experience_years": feats["experience_years"], "education": feats["education"],
                "certifications": feats["certifications"], "recent_roles": feats["recent_roles"],
            })
            contact = extract_contact(raw, fname)
            meta[fname] = {"contact": contact, "skills": detect_skills(raw), "ats": ats_check(raw, contact),
                           "roles": feats["recent_roles"]}

        st.write("🔗 Computing semantic similarity...")
        emb = embed_texts(embedder, [jd_clean] + [r["text"] for r in records])
        sim = cosine_similarity_matrix(emb)
        st.write("⚖️ Scoring and ranking...")
        df = compute_scores(jd_clean, jd_keywords, records, sim, w_sim, w_kw, w_exp, w_edu, w_cert)

        rows: List[Dict] = []
        for rec in df.to_dict("records"):
            m = meta[rec["filename"]]
            gap = skill_gap(jd_skills, m["skills"])
            rec.update({
                "name": m["contact"]["name"], "email": m["contact"]["email"], "phone": m["contact"]["phone"],
                "skills": m["skills"], "gap": gap, "ats": m["ats"], "roles": m["roles"],
                "verdict": verdict(rec["total_score"]),
            })
            rec["insights"] = build_insights(rec, gap)
            rec["questions"] = interview_questions(gap)
            rows.append(rec)
        status.update(label="Analysis complete ✔", state="complete", expanded=False)

    title = (jd_text.strip().splitlines() or ["Role"])[0][:80]
    st.session_state["results"] = {"rows": rows, "jd_keywords": jd_keywords, "jd_skills": jd_skills, "title": title,
                                   "time": time.strftime("%H:%M:%S")}
    st.toast("Analysis complete! 🎉", icon="✅")


if go:
    run_analysis()

# ------------------------------------------------------------------ results
res = st.session_state.get("results")
if not res:
    md('<div class="glass" style="text-align:center;margin-top:18px"><div style="font-size:2.2rem">👆</div>'
       '<b>Paste a job description, add resumes, and hit Analyze.</b><br>'
       '<span class="muted">New here? Click <b>✨ Load demo data</b> in the sidebar for an instant walkthrough.</span></div>')
    st.stop()

rows: List[Dict] = res["rows"]
n = len(rows)
shortlisted = [r for r in rows if r["total_score"] >= shortlist_cut]
avg = sum(r["total_score"] for r in rows) / n
best = rows[0]

md(ui.section("Overview", "📊"))
md(ui.kpis([
    ("Candidates screened", n, "#7c5cff"),
    ("Top score", f"{best['total_score']*100:.0f}%", "#34d399"),
    ("Average score", f"{avg*100:.0f}%", "#22d3ee"),
    (f"Shortlisted (≥{shortlist_cut*100:.0f}%)", len(shortlisted), "#ff5ca8"),
    ("Skills required", len(res["jd_skills"]), "#fbbf24"),
]))

md(ui.section("Top Candidates", "🏆"))
md(ui.podium(rows))

tabs = st.tabs(["🏅 Leaderboard", "📡 Compare", "🔍 Deep Dive", "📋 Data & Export"])

# ---- Leaderboard
with tabs[0]:
    md(ui.section("Overall Ranking", "📈"))
    md(ui.hbar_chart(rows))
    md(ui.section("Candidate Cards", "🧑‍💼"))
    for r in rows:
        md(ui.candidate_card(r))
    with st.expander("🔑 Job description keywords & required skills"):
        md("<b>Required skills detected</b><br>" + ui.chips(res["jd_skills"], "extra", 30))
        md("<br><b>Top keywords</b><br>" + ui.chips(res["jd_keywords"], "extra", 40))

# ---- Compare
with tabs[1]:
    md(ui.section("Radar Comparison", "📡"))
    names = [r["name"] for r in rows]
    picked = st.multiselect("Select candidates to compare (up to 4)", names, default=names[:min(3, n)], max_selections=4)
    axes = ["Semantic", "Keywords", "Experience", "Education", "Certs"]
    series = []
    for r in rows:
        if r["name"] in picked:
            series.append({"name": r["name"], "values": [r["similarity"], r["keyword_coverage"], r["experience_score"],
                                                         r["education_score"], r["certification_score"]]})
    if series:
        cA, cB = st.columns([1, 1], gap="large")
        with cA:
            md('<div class="glass">' + ui.radar(series, axes) + "</div>")
        with cB:
            sel = [r for r in rows if r["name"] in picked]
            tbl = pd.DataFrame({
                "Candidate": [r["name"] for r in sel],
                "Total": [round(r["total_score"] * 100) for r in sel],
                "Skills matched": [len(r["gap"]["matched"]) for r in sel],
                "Skills missing": [len(r["gap"]["missing"]) for r in sel],
                "Experience (yrs)": [r["experience_years"] for r in sel],
                "ATS": [r["ats"]["score"] for r in sel],
            })
            st.dataframe(tbl, hide_index=True, use_container_width=True)
            winner = max(sel, key=lambda r: r["total_score"])
            md(f'<div class="glass">🏆 <b>{ui.esc(winner["name"])}</b> leads this comparison with '
               f'<b>{winner["total_score"]*100:.0f}%</b> &mdash; {ui.esc(winner["verdict"]["action"])}.</div>')
    else:
        st.info("Pick at least one candidate.")

# ---- Deep dive
with tabs[2]:
    md(ui.section("Candidate Deep Dive", "🔍"))
    who = st.selectbox("Choose a candidate", [f"#{r['rank']} · {r['name']}" for r in rows])
    r = rows[int(who.split("·")[0].strip().lstrip("#")) - 1]
    v = r["verdict"]
    md(f'<div class="glass"><div class="cand"><div style="text-align:center">{ui.ring(r["total_score"], 150)}</div><div>'
       f'<span class="nm">{ui.esc(r["name"])}</span> <span class="tag {v["tone"]}">{v["emoji"]} {ui.esc(v["label"])}</span>'
       f'<div class="meta">✉️ {ui.esc(r["email"] or "n/a")} &nbsp;•&nbsp; 📞 {ui.esc(r["phone"] or "n/a")} &nbsp;•&nbsp; '
       f'🧑‍💼 {ui.esc(r["experience_years"])} yrs &nbsp;•&nbsp; 🎓 {ui.esc(r["education"])}</div>'
       f'<b>Recommended action:</b> {ui.esc(v["action"])}<br><br>{ui.chips(r["skills"], "extra", 20)}</div></div></div>')
    md(ui.section("Strengths & Risks", "💡"))
    md(ui.insights_html(r["insights"]))
    md(ui.section("Skill Gap", "🎯"))
    md("<b>✅ Matched</b><br>" + ui.chips(r["gap"]["matched"], "ok", 30) +
       "<br><br><b>❌ Missing</b><br>" + ui.chips(r["gap"]["missing"], "miss", 30) +
       "<br><br><b>➕ Extra skills</b><br>" + ui.chips(r["gap"]["extra"], "extra", 30))
    md(ui.section("Suggested Interview Questions", "🎤"))
    md(ui.questions_html(r["questions"]))
    md(ui.section("ATS Health Check", "🛡️"))
    md(ui.ats_html(r["ats"]))

# ---- Data & export
with tabs[3]:
    md(ui.section("Results Table", "📋"))
    table = pd.DataFrame([{
        "Rank": r["rank"], "Candidate": r["name"], "Verdict": r["verdict"]["label"],
        "Total": r["total_score"] * 100, "Semantic": r["similarity"] * 100, "Keywords": r["keyword_coverage"] * 100,
        "Experience": r["experience_score"] * 100, "Education": r["education_score"] * 100,
        "Certs": r["certification_score"] * 100, "ATS": r["ats"]["score"],
        "Exp (yrs)": r["experience_years"], "Degree": r["education"], "Email": r["email"],
        "Matched skills": ", ".join(r["gap"]["matched"]), "Missing skills": ", ".join(r["gap"]["missing"]),
    } for r in rows])
    pct = lambda: st.column_config.ProgressColumn(format="%.0f%%", min_value=0, max_value=100)  # noqa: E731
    st.dataframe(table, hide_index=True, use_container_width=True, column_config={
        "Total": pct(), "Semantic": pct(), "Keywords": pct(), "Experience": pct(), "Education": pct(), "Certs": pct(),
        "ATS": st.column_config.ProgressColumn(format="%d", min_value=0, max_value=100),
    })
    md(ui.section(f"Shortlist ({len(shortlisted)})", "⭐"))
    if shortlisted:
        md("".join(f'<span class="chip ok">⭐ {ui.esc(r["name"])} · {r["total_score"]*100:.0f}%</span>' for r in shortlisted))
    else:
        st.info("No candidate meets the current threshold. Lower it in the sidebar.")
    md(ui.section("Export", "📦"))
    d1, d2, d3 = st.columns(3)
    d1.download_button("⬇️ Full results (CSV)", table.to_csv(index=False).encode("utf-8"), "resume_scores.csv", "text/csv",
                       use_container_width=True)
    short_df = table[table["Candidate"].isin([r["name"] for r in shortlisted])]
    d2.download_button("⭐ Shortlist (CSV)", short_df.to_csv(index=False).encode("utf-8"), "shortlist.csv", "text/csv",
                       use_container_width=True, disabled=short_df.empty)
    d3.download_button("📄 Report (HTML → PDF)", build_html_report(rows, res["title"], res["jd_keywords"]).encode("utf-8"),
                       "screening_report.html", "text/html", use_container_width=True,
                       help="Open the file and press Ctrl+P to save as PDF")

md('<div class="muted" style="text-align:center;margin:36px 0 8px">Built with Streamlit · spaCy · Sentence-Transformers · '
   f'Last analysed at {res["time"]}</div>')
