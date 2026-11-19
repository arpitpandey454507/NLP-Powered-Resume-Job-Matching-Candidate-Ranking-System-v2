"""HTML/SVG building blocks (dependency-free, so charts render everywhere)."""

import html
import math
from typing import Dict, List

PALETTE = ["#7c5cff", "#22d3ee", "#ff5ca8", "#fbbf24", "#34d399", "#fb7185"]


def esc(x) -> str:
    return html.escape(str(x))


def hero() -> str:
    return """
    <div class="hero">
      <span class="badge"><i></i>AI-POWERED TALENT INTELLIGENCE</span>
      <h1>Hire smarter with <span class="grad">AI Resume Screener</span></h1>
      <p>Upload resumes, paste a job description and get instant semantic ranking, skill-gap analysis,
      ATS scoring and interview questions &mdash; in seconds.</p>
      <div class="pills">
        <span class="pill">🧠 Semantic Embeddings</span><span class="pill">🎯 Skill-Gap Analysis</span>
        <span class="pill">📡 Radar Comparison</span><span class="pill">🛡️ ATS Health Check</span>
        <span class="pill">🎤 Interview Questions</span><span class="pill">📄 Report Export</span>
      </div>
    </div>"""


def section(title: str, icon: str = "") -> str:
    return f'<div class="sec-title"><span class="bar"></span>{icon} {esc(title)}</div>'


def kpis(items: List[tuple]) -> str:
    cells = ""
    for i, (label, value, color) in enumerate(items):
        cells += (f'<div class="kpi" style="--c:{color};animation-delay:{i*0.08}s">'
                  f'<div class="v">{esc(value)}</div><div class="l">{esc(label)}</div></div>')
    return f'<div class="kpis">{cells}</div>'


def score_color(score: float) -> str:
    if score >= 0.75:
        return "#34d399"
    if score >= 0.6:
        return "#22d3ee"
    if score >= 0.45:
        return "#fbbf24"
    return "#fb7185"


def ring(score: float, size: int = 130, label: str = "MATCH") -> str:
    """Animated circular score gauge (SVG)."""
    r = size / 2 - 10
    c = 2 * math.pi * r
    pct = max(0.0, min(1.0, score))
    col = score_color(score)
    cx = size / 2
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <defs><linearGradient id="g{int(pct*1000)}{size}" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="{col}"/><stop offset="100%" stop-color="#7c5cff"/></linearGradient></defs>
      <circle cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="rgba(255,255,255,.09)" stroke-width="10"/>
      <circle cx="{cx}" cy="{cx}" r="{r}" fill="none" stroke="url(#g{int(pct*1000)}{size})" stroke-width="10"
        stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c*(1-pct):.1f}"
        transform="rotate(-90 {cx} {cx})" style="--len:{c:.1f};animation:draw 1.4s cubic-bezier(.2,.8,.2,1) both"/>
      <text x="50%" y="48%" text-anchor="middle" fill="#fff" font-family="Space Grotesk,sans-serif"
        font-size="{size*0.25:.0f}" font-weight="700">{pct*100:.0f}%</text>
      <text x="50%" y="66%" text-anchor="middle" fill="#9aa3c7" font-size="{size*0.085:.0f}"
        letter-spacing="2" font-family="Inter,sans-serif">{esc(label)}</text>
    </svg>"""


def chips(items: List[str], kind: str, limit: int = 14) -> str:
    if not items:
        return '<span class="muted">—</span>'
    out = "".join(f'<span class="chip {kind}">{esc(i)}</span>' for i in items[:limit])
    if len(items) > limit:
        out += f'<span class="chip {kind}">+{len(items)-limit} more</span>'
    return out


def bars(values: Dict[str, float]) -> str:
    rows = ""
    for i, (k, v) in enumerate(values.items()):
        rows += (f'<div class="bar-row"><span>{esc(k)}</span><div class="track"><div class="fill" '
                 f'style="width:{max(0,min(1,v))*100:.0f}%;animation-delay:{i*0.1}s"></div></div>'
                 f'<span>{v*100:.0f}%</span></div>')
    return f'<div class="bars">{rows}</div>'


def podium(rows: List[Dict]) -> str:
    """Top-3 podium. rows sorted by rank."""
    top = rows[:3]
    order = []
    if len(top) >= 2:
        order.append((top[1], "p2", "🥈"))
    order.append((top[0], "p1", "🥇"))
    if len(top) >= 3:
        order.append((top[2], "p3", "🥉"))
    cells = ""
    for i, (r, cls, medal) in enumerate(order):
        cells += (f'<div class="pod {cls}" style="animation-delay:{i*0.15}s"><div class="medal">{medal}</div>'
                  f'<div class="nm">{esc(r["name"])}</div><div class="sc" style="color:{score_color(r["total_score"])}">'
                  f'{r["total_score"]*100:.0f}%</div><div class="muted">{esc(r["verdict"]["label"])}</div></div>')
    cols = "1fr 1.15fr 1fr" if len(order) == 3 else ("1fr 1.15fr" if len(order) == 2 else "1fr")
    return f'<div class="podium" style="grid-template-columns:{cols}">{cells}</div>'


def candidate_card(r: Dict) -> str:
    v = r["verdict"]
    meta = " &nbsp;•&nbsp; ".join(x for x in [
        f"🧑‍💼 {esc(r['experience_years'])} yrs" if r["experience_years"] != "N/A" else "🧑‍💼 Exp N/A",
        f"🎓 {esc(r['education'])}", f"📜 {r['certifications']} cert(s)",
        f"✉️ {esc(r['email'])}" if r.get("email") else ""] if x)
    gap = r["gap"]
    return f"""
    <div class="glass" style="margin-bottom:14px">
      <div class="cand">
        <div style="text-align:center">{ring(r['total_score'])}</div>
        <div>
          <div><span class="rankbadge">#{r['rank']}</span><span class="nm">{esc(r['name'])}</span>
            <span class="tag {v['tone']}">{v['emoji']} {esc(v['label'])}</span></div>
          <div class="meta">{meta}</div>
          {bars({'Semantic': r['similarity'], 'Keywords': r['keyword_coverage'], 'Experience': r['experience_score'],
                 'Education': r['education_score'], 'Certs': r['certification_score']})}
          <div style="margin-top:12px"><b style="font-size:.8rem;color:#9aa3c7">MATCHED SKILLS</b><br>{chips(gap['matched'], 'ok')}</div>
          <div style="margin-top:6px"><b style="font-size:.8rem;color:#9aa3c7">MISSING SKILLS</b><br>{chips(gap['missing'], 'miss')}</div>
        </div>
      </div>
    </div>"""


def radar(series: List[Dict], axes: List[str], size: int = 420) -> str:
    """Multi-series radar chart. series = [{name, values(list 0..1), color}]"""
    n = len(axes)
    cx = cy = size / 2
    R = size / 2 - 62
    def pt(i, v):
        a = -math.pi / 2 + 2 * math.pi * i / n
        return cx + R * v * math.cos(a), cy + R * v * math.sin(a)
    grid = ""
    for lvl in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(f"{pt(i, lvl)[0]:.1f},{pt(i, lvl)[1]:.1f}" for i in range(n))
        grid += f'<polygon points="{pts}" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="1"/>'
    spokes, labels = "", ""
    for i, ax in enumerate(axes):
        x, y = pt(i, 1.0)
        spokes += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,.12)"/>'
        lx, ly = pt(i, 1.2)
        labels += (f'<text x="{lx:.1f}" y="{ly:.1f}" fill="#cfd5ff" font-size="12" text-anchor="middle" '
                   f'dominant-baseline="middle" font-family="Inter,sans-serif" font-weight="600">{esc(ax)}</text>')
    polys, legend = "", ""
    for k, s in enumerate(series):
        col = s.get("color", PALETTE[k % len(PALETTE)])
        pts = " ".join(f"{pt(i, v)[0]:.1f},{pt(i, v)[1]:.1f}" for i, v in enumerate(s["values"]))
        dots = "".join(f'<circle cx="{pt(i, v)[0]:.1f}" cy="{pt(i, v)[1]:.1f}" r="3.5" fill="{col}"/>'
                       for i, v in enumerate(s["values"]))
        polys += (f'<polygon points="{pts}" fill="{col}" fill-opacity=".18" stroke="{col}" stroke-width="2.4" '
                  f'stroke-linejoin="round"/>{dots}')
        legend += (f'<span style="display:inline-flex;align-items:center;gap:6px;margin:0 10px;font-size:.82rem">'
                   f'<i style="width:10px;height:10px;border-radius:3px;background:{col};display:inline-block"></i>{esc(s["name"])}</span>')
    return (f'<div style="text-align:center"><svg width="100%" style="max-width:{size}px" viewBox="0 0 {size} {size}">'
            f'{grid}{spokes}{polys}{labels}</svg><div>{legend}</div></div>')


def hbar_chart(rows: List[Dict], key: str = "total_score", title: str = "") -> str:
    """Horizontal ranked bar chart."""
    out = ""
    for i, r in enumerate(rows):
        col = PALETTE[i % len(PALETTE)]
        out += (f'<div class="bar-row" style="grid-template-columns:150px 1fr 52px;font-size:.88rem">'
                f'<span style="color:#eef0ff">{esc(r["name"])}</span>'
                f'<div class="track" style="height:14px"><div class="fill" style="width:{r[key]*100:.0f}%;'
                f'background:linear-gradient(90deg,{col},#22d3ee);animation-delay:{i*0.12}s"></div></div>'
                f'<span style="color:#fff;font-weight:700">{r[key]*100:.0f}%</span></div>')
    return f'<div class="glass"><div class="bars" style="gap:14px">{out}</div></div>'


def insights_html(ins: Dict[str, List[str]]) -> str:
    g = "".join(f"<li>{esc(x)}</li>" for x in ins["strengths"])
    b = "".join(f"<li>{esc(x)}</li>" for x in ins["risks"])
    return (f'<div class="ins-grid"><div class="ins good"><h4>💪 Strengths</h4><ul>{g}</ul></div>'
            f'<div class="ins bad"><h4>⚠️ Risks & Gaps</h4><ul>{b}</ul></div></div>')


def questions_html(qs: List[str]) -> str:
    return "".join(f'<div class="q">🎤 {esc(q)}</div>' for q in qs)


def ats_html(ats: Dict) -> str:
    rows = ""
    for c in ats["checks"]:
        icon = "✅" if c["ok"] else "❌"
        tip = "" if c["ok"] else f' <span class="muted">— {esc(c["tip"])}</span>'
        rows += f'<div class="check"><span>{icon}</span><span>{esc(c["label"])}{tip}</span></div>'
    return (f'<div class="glass" style="display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center">'
            f'<div style="text-align:center">{ring(ats["score"]/100, 130, "ATS")}</div><div>{rows}</div></div>')


def clean(markup: str) -> str:
    """Collapse whitespace/newlines so Streamlit's Markdown never treats indented HTML as a code block."""
    import re
    return re.sub(r"\s*\n\s*", " ", markup).strip()
