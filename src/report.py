"""Standalone, print-friendly HTML report (open in browser -> Ctrl+P -> Save as PDF)."""

import html
from datetime import datetime
from typing import Dict, List


def build_html_report(rows: List[Dict], jd_title: str, jd_keywords: List[str]) -> str:
    e = html.escape
    cards = ""
    for r in rows:
        col = "#16a34a" if r["total_score"] >= .75 else "#0891b2" if r["total_score"] >= .6 else "#d97706" if r["total_score"] >= .45 else "#dc2626"
        cards += f"""
        <div class="card">
          <div class="top"><div><span class="rank">#{r['rank']}</span> <b>{e(r['name'])}</b><br>
          <small>{e(r.get('email') or '')} {e(r.get('phone') or '')}</small></div>
          <div class="score" style="color:{col}">{r['total_score']*100:.0f}%<small>{e(r['verdict']['label'])}</small></div></div>
          <p><b>Experience:</b> {e(str(r['experience_years']))} yrs &nbsp; <b>Education:</b> {e(r['education'])} &nbsp;
             <b>ATS:</b> {r['ats']['score']}/100</p>
          <p><b>Matched:</b> {e(', '.join(r['gap']['matched']) or '—')}<br>
             <b>Missing:</b> {e(', '.join(r['gap']['missing']) or '—')}</p>
          <p><b>Strengths:</b> {e(' '.join(r['insights']['strengths']))}<br>
             <b>Risks:</b> {e(' '.join(r['insights']['risks']))}</p>
          <p><b>Recommendation:</b> {e(r['verdict']['action'])}</p>
        </div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>Screening Report</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;max-width:900px;margin:30px auto;color:#1e293b;padding:0 18px}}
h1{{background:linear-gradient(90deg,#7c5cff,#22d3ee);-webkit-background-clip:text;color:transparent}}
.card{{border:1px solid #e2e8f0;border-radius:14px;padding:16px 20px;margin:14px 0;page-break-inside:avoid}}
.top{{display:flex;justify-content:space-between;align-items:center}}.rank{{background:#7c5cff;color:#fff;padding:2px 10px;border-radius:99px}}
.score{{font-size:2rem;font-weight:800;text-align:right}}.score small{{display:block;font-size:.75rem;color:#64748b}}</style></head>
<body><h1>AI Resume Screening Report</h1>
<p>Generated {datetime.now():%d %b %Y, %H:%M} &nbsp;|&nbsp; Role: <b>{e(jd_title)}</b> &nbsp;|&nbsp; Candidates: <b>{len(rows)}</b></p>
<p><b>Key requirements:</b> {e(', '.join(jd_keywords[:20]))}</p>{cards}</body></html>"""
