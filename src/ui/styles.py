"""Global CSS for the premium dark 'aurora' theme."""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root{
  --bg:#070914; --panel:rgba(255,255,255,.045); --panel2:rgba(255,255,255,.075);
  --line:rgba(255,255,255,.10); --txt:#eef0ff; --mut:#9aa3c7;
  --p1:#7c5cff; --p2:#22d3ee; --p3:#ff5ca8; --ok:#34d399; --warn:#fbbf24; --bad:#fb7185;
}
html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif !important; }
.stApp{
  background:
    radial-gradient(900px 500px at 8% -10%, rgba(124,92,255,.28), transparent 60%),
    radial-gradient(800px 500px at 100% 0%, rgba(34,211,238,.18), transparent 60%),
    radial-gradient(700px 500px at 50% 110%, rgba(255,92,168,.14), transparent 60%),
    var(--bg) !important;
  color:var(--txt);
}
header[data-testid="stHeader"]{background:transparent !important;}
#MainMenu, footer{visibility:hidden;}
.block-container{padding-top:1.4rem !important; max-width:1250px;}
h1,h2,h3,h4{font-family:'Space Grotesk',sans-serif !important; color:var(--txt) !important; letter-spacing:-.01em;}
p, label, span, li{color:var(--txt);}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#0d1030 0%,#090b1f 100%) !important;
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] *{color:var(--txt);}

/* ---------- Hero ---------- */
.hero{
  position:relative; overflow:hidden; border-radius:26px; padding:42px 44px; margin-bottom:22px;
  background:linear-gradient(120deg,rgba(124,92,255,.35),rgba(34,211,238,.18) 55%,rgba(255,92,168,.25));
  border:1px solid var(--line); box-shadow:0 20px 60px rgba(124,92,255,.25);
}
.hero:before{
  content:""; position:absolute; inset:-60%; 
  background:conic-gradient(from 0deg, transparent, rgba(255,255,255,.10), transparent 30%);
  animation:spin 14s linear infinite;
}
.hero > *{position:relative; z-index:1;}
.badge{
  display:inline-flex; gap:8px; align-items:center; padding:6px 14px; border-radius:999px;
  background:rgba(255,255,255,.10); border:1px solid var(--line); font-size:.78rem; font-weight:600; letter-spacing:.06em;
}
.badge i{width:8px;height:8px;border-radius:50%;background:var(--ok);box-shadow:0 0 12px var(--ok);animation:pulse 1.6s infinite;}
.hero h1{font-size:3rem; line-height:1.05; margin:16px 0 10px; font-weight:700;}
.grad{background:linear-gradient(90deg,#a78bfa,#22d3ee,#ff5ca8,#a78bfa); background-size:300% 100%;
  -webkit-background-clip:text; background-clip:text; color:transparent !important; animation:shine 6s linear infinite;}
.hero p{color:#cfd5ff; font-size:1.08rem; max-width:720px; margin:0;}
.pills{display:flex; gap:10px; flex-wrap:wrap; margin-top:22px;}
.pill{padding:7px 14px; border-radius:12px; background:rgba(0,0,0,.28); border:1px solid var(--line); font-size:.85rem; color:#dfe3ff;}

/* ---------- Generic ---------- */
.glass{background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:22px;
  backdrop-filter:blur(14px); transition:transform .25s, border-color .25s, box-shadow .25s;}
.glass:hover{border-color:rgba(124,92,255,.5); box-shadow:0 12px 40px rgba(124,92,255,.18);}
.sec-title{display:flex; align-items:center; gap:10px; margin:26px 0 12px; font-family:'Space Grotesk','Inter',sans-serif; font-size:1.35rem; font-weight:700;}
.sec-title span.bar{width:5px; height:22px; border-radius:4px; background:linear-gradient(180deg,var(--p1),var(--p2));}
.muted{color:var(--mut) !important; font-size:.88rem;}

/* ---------- KPI ---------- */
.kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(190px,1fr)); gap:14px; margin:8px 0 6px;}
.kpi{padding:18px 20px; border-radius:18px; background:var(--panel); border:1px solid var(--line); position:relative; overflow:hidden;
  animation:rise .7s both;}
.kpi:after{content:""; position:absolute; right:-30px; top:-30px; width:100px; height:100px; border-radius:50%;
  background:radial-gradient(circle,var(--c,#7c5cff),transparent 70%); opacity:.35;}
.kpi .v{font-family:'Space Grotesk','Inter',sans-serif; font-size:2.1rem; font-weight:700;}
.kpi .l{color:var(--mut); font-size:.82rem; text-transform:uppercase; letter-spacing:.08em;}

/* ---------- Podium ---------- */
.podium{display:grid; grid-template-columns:1fr 1.15fr 1fr; gap:16px; align-items:end; margin:10px 0 8px;}
.pod{border-radius:22px; padding:22px 16px; text-align:center; background:var(--panel); border:1px solid var(--line); position:relative; animation:rise .8s both;}
.pod.p1{background:linear-gradient(180deg,rgba(251,191,36,.20),rgba(255,255,255,.04)); border-color:rgba(251,191,36,.55); padding-bottom:34px; box-shadow:0 0 50px rgba(251,191,36,.18);}
.pod.p2{background:linear-gradient(180deg,rgba(203,213,225,.16),rgba(255,255,255,.04)); border-color:rgba(203,213,225,.4);}
.pod.p3{background:linear-gradient(180deg,rgba(251,146,60,.16),rgba(255,255,255,.04)); border-color:rgba(251,146,60,.4);}
.pod .medal{font-size:2.4rem; filter:drop-shadow(0 6px 14px rgba(0,0,0,.5));}
.pod .nm{font-weight:700; font-size:1.05rem; margin:6px 0 2px;}
.pod .sc{font-family:'Space Grotesk','Inter',sans-serif; font-size:2.2rem; font-weight:700;}
.pod.p1 .sc{font-size:2.8rem;}

/* ---------- Candidate card ---------- */
.cand{display:grid; grid-template-columns:150px 1fr; gap:22px; align-items:center;}
.cand .nm{font-family:'Space Grotesk','Inter',sans-serif; font-size:1.35rem; font-weight:700;}
.rankbadge{display:inline-block; padding:3px 11px; border-radius:999px; font-size:.75rem; font-weight:700; background:linear-gradient(90deg,var(--p1),var(--p2)); color:#fff; margin-right:8px;}
.tag{display:inline-block; padding:3px 11px; border-radius:999px; font-size:.75rem; font-weight:600; margin-left:4px;}
.tag.great{background:rgba(52,211,153,.18); color:#6ee7b7; border:1px solid rgba(52,211,153,.5);}
.tag.good{background:rgba(34,211,238,.16); color:#67e8f9; border:1px solid rgba(34,211,238,.5);}
.tag.mid{background:rgba(251,191,36,.16); color:#fcd34d; border:1px solid rgba(251,191,36,.5);}
.tag.low{background:rgba(251,113,133,.16); color:#fda4af; border:1px solid rgba(251,113,133,.5);}
.meta{color:var(--mut); font-size:.85rem; margin:6px 0 10px;}
.chip{display:inline-block; padding:4px 11px; margin:3px 5px 3px 0; border-radius:10px; font-size:.78rem; font-weight:500;}
.chip.ok{background:rgba(52,211,153,.14); color:#6ee7b7; border:1px solid rgba(52,211,153,.4);}
.chip.miss{background:rgba(251,113,133,.12); color:#fda4af; border:1px solid rgba(251,113,133,.4); text-decoration:line-through; text-decoration-color:rgba(251,113,133,.5);}
.chip.extra{background:rgba(124,92,255,.14); color:#c4b5fd; border:1px solid rgba(124,92,255,.4);}

/* mini bars */
.bars{display:grid; gap:9px; margin-top:6px;}
.bar-row{display:grid; grid-template-columns:110px 1fr 46px; gap:10px; align-items:center; font-size:.8rem; color:var(--mut);}
.track{height:8px; border-radius:99px; background:rgba(255,255,255,.08); overflow:hidden;}
.fill{height:100%; border-radius:99px; background:linear-gradient(90deg,var(--p1),var(--p2)); animation:grow 1.2s cubic-bezier(.2,.8,.2,1) both;}

/* insight boxes */
.ins-grid{display:grid; grid-template-columns:1fr 1fr; gap:14px;}
.ins{border-radius:16px; padding:16px 18px; border:1px solid var(--line);}
.ins.good{background:rgba(52,211,153,.07); border-color:rgba(52,211,153,.35);}
.ins.bad{background:rgba(251,113,133,.07); border-color:rgba(251,113,133,.35);}
.ins h4{margin:0 0 8px; font-size:1rem;}
.ins li{margin:4px 0; font-size:.9rem; color:#dfe3ff;}
.q{padding:12px 16px; border-left:3px solid var(--p2); background:rgba(34,211,238,.06); border-radius:0 12px 12px 0; margin:8px 0; font-size:.92rem;}
.check{display:flex; gap:10px; align-items:flex-start; padding:7px 0; border-bottom:1px dashed var(--line); font-size:.88rem;}

/* ---------- Streamlit widgets ---------- */
.stButton>button, .stDownloadButton>button{
  border-radius:14px !important; border:1px solid var(--line) !important; font-weight:600 !important;
  background:var(--panel2) !important; color:var(--txt) !important; transition:all .25s !important;
}
.stButton>button:hover, .stDownloadButton>button:hover{transform:translateY(-2px); border-color:var(--p1) !important; box-shadow:0 8px 26px rgba(124,92,255,.35);}
.stButton>button[kind="primary"]{
  background:linear-gradient(90deg,var(--p1),var(--p2),var(--p3)) !important; background-size:200% 100% !important;
  border:none !important; color:#fff !important; font-size:1.05rem !important; padding:.7rem 1rem !important; animation:shine 5s linear infinite;
  box-shadow:0 10px 34px rgba(124,92,255,.45);
}
.stTextArea textarea, .stTextInput input{
  background:rgba(255,255,255,.05) !important; border:1px solid var(--line) !important; border-radius:14px !important; color:var(--txt) !important;
}
.stTextArea textarea:focus{border-color:var(--p1) !important; box-shadow:0 0 0 3px rgba(124,92,255,.25) !important;}
[data-testid="stFileUploaderDropzone"]{
  background:rgba(124,92,255,.07) !important; border:2px dashed rgba(124,92,255,.5) !important; border-radius:18px !important; transition:all .25s;
}
[data-testid="stFileUploaderDropzone"]:hover{background:rgba(124,92,255,.14) !important; border-color:var(--p2) !important;}
.stTabs [data-baseweb="tab-list"]{gap:6px; background:var(--panel); padding:6px; border-radius:16px; border:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{border-radius:12px; padding:8px 18px; color:var(--mut); font-weight:600;}
.stTabs [aria-selected="true"]{background:linear-gradient(90deg,var(--p1),var(--p2)) !important; color:#fff !important;}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"]{display:none;}
[data-testid="stExpander"]{background:var(--panel); border:1px solid var(--line) !important; border-radius:16px !important;}
div[data-testid="stDataFrame"]{border-radius:16px; overflow:hidden; border:1px solid var(--line);}

/* ---------- Animations ---------- */
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes shine{to{background-position:300% 0}}
@keyframes pulse{50%{opacity:.35; transform:scale(1.4)}}
@keyframes rise{from{opacity:0; transform:translateY(22px)}to{opacity:1; transform:none}}
@keyframes grow{from{width:0}}
@keyframes draw{from{stroke-dashoffset:var(--len)}}
@media(max-width:800px){.cand{grid-template-columns:1fr}.ins-grid{grid-template-columns:1fr}.podium{grid-template-columns:1fr}.hero h1{font-size:2.1rem}.hero{padding:28px}}
</style>
"""
