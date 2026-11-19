# 🤖 AI Resume Screener — Premium Edition

A redesigned, presentation-ready resume screening dashboard: dark "aurora" glassmorphism UI, animated score rings,
podium leaderboard, radar comparison, skill-gap analysis, ATS health check, interview-question generator and report export.

## ✨ New in this edition
- **Complete UI redesign**: animated gradient hero, glass cards, neon progress bars, custom tabs
- **One-click Demo Mode**: sample JD + 4 resumes, perfect for live presentations
- **Podium + animated score rings** and ranked bar chart
- **Skill-Gap Analysis**: matched / missing / extra skills per candidate
- **Radar chart comparison** of up to 4 candidates
- **Strengths & Risks insights** and hiring verdicts (Excellent / Strong / Potential / Weak)
- **Interview question generator** based on each candidate's gaps
- **ATS Health Check** (sections, contact info, action verbs, metrics, length)
- **Contact extraction** (name, email, phone, LinkedIn, GitHub)
- **Shortlist threshold** + exports: full CSV, shortlist CSV, printable HTML/PDF report
- Results persist while you explore tabs; presets now update the sliders correctly
- Better keyword matching (checks resume text and synonyms, not just top-k keywords)

## 🎯 Overview

This tool helps HR professionals and recruiters quickly identify the best candidates by:
- **Semantic Analysis**: Understanding resume meaning beyond keywords
- **Multi-Factor Scoring**: Experience, education, skills, and certifications
- **Smart Keyword Matching**: Groups related technologies (Python → Django, Pandas, etc.)
- **Interactive Dashboard**: Visual rankings and detailed metrics

## Features
- Upload multiple resumes (PDF, DOCX, or TXT)
- Paste a job description
- **Smart Keyword Extraction** with synonym grouping (e.g., Python → Django, Pandas, NumPy)
- **Semantic Similarity** using `all-MiniLM-L6-v2` embeddings
- **Experience Years Matching** - automatically extracts and matches experience requirements
- **Education Matching** - detects and matches degree requirements (PhD, Masters, Bachelors, Diploma)
- **Certification Detection** - identifies and scores certifications
- **Recent Roles Extraction** - extracts job titles and positions
- **Weighted Multi-Factor Scoring** with customizable weights
- **Interactive Dashboard** with dual visualizations
- **CSV Export** with all metrics

## Quickstart

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. Run the app:

```bash
streamlit run app.py
```

4. In the UI:
- Paste the job description
- Upload resumes
- Click Analyze

## Notes
- The app attempts to lazily download `en_core_web_sm` if missing.
- For PDFs, it tries `pdfplumber` first then falls back to `PyPDF2`.
- Embeddings use `sentence-transformers/all-MiniLM-L6-v2` (downloads on first run).

## 📁 Project Structure
```
ai-resume-screener/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore rules
└── src/
    ├── __init__.py
    ├── scoring.py            # Multi-factor scoring logic
    ├── processing/
    │   ├── embedding.py      # Sentence transformer embeddings
    │   └── nlp.py            # Keyword extraction with synonym support
    └── utils/
        ├── __init__.py
        ├── parser.py         # PDF/DOCX/TXT text extraction
        ├── keyword_mapping.py  # Skill groups and synonym mapping
        └── resume_extractor.py # Experience, education, certs extraction
```

## Scoring System

The total score is a weighted combination of:

1. **Semantic Similarity** (default: 0.4) - Meaning-based similarity using embeddings
2. **Keyword Coverage** (default: 0.3) - Exact skill keyword matches with synonym expansion
3. **Experience Match** (default: 0.15) - Years of experience vs JD requirement
4. **Education Match** (default: 0.1) - Degree level matching
5. **Certifications** (default: 0.05) - Certification relevance

### Keyword Mapping

The system groups related technologies:
- **Python** → Django, Flask, FastAPI, Pandas, NumPy, TensorFlow, PyTorch
- **JavaScript** → Node.js, React, Vue, Angular, TypeScript
- **Cloud** → AWS, Azure, GCP (grouped separately)
- **Databases** → SQL variants, NoSQL variants

### Experience Extraction

Automatically extracts experience from:
- Direct mentions: "5 years of experience"
- Date ranges: "2020 - Present" or "Jan 2020 - Dec 2023"
- Calculates total years from work history

### Education Detection

Recognizes:
- PhD, Doctorate
- Masters (MS, MBA, M.Tech, MCA)
- Bachelors (BS, B.Tech, BE, BCA, B.Com)
- Diploma, Certificate

### Certification Patterns

Detects:
- Cloud certifications (AWS, Azure, GCP)
- Professional certs (PMP, Scrum, Agile)
- Vendor certifications (Microsoft, Oracle, Salesforce)
- Custom patterns

## Customization

- **Adjust Weights**: Use sidebar sliders to prioritize different factors
- **Keyword Synonyms**: Toggle synonym grouping on/off
- **Keyword Count**: Adjust number of keywords extracted (5-30)

## 🛠️ Installation Notes

- The app attempts to lazily download `en_core_web_sm` if missing.
- For PDFs, it tries `pdfplumber` first then falls back to `PyPDF2`.
- Embeddings use `sentence-transformers/all-MiniLM-L6-v2` (downloads on first run).
- **Windows users**: Use CPU-only PyTorch to avoid DLL issues:
  ```bash
  pip install --index-url https://download.pytorch.org/whl/cpu torch==2.2.2+cpu
  ```

## 📦 Tech Stack

- **Python 3.10+**
- **Streamlit** - Web UI framework
- **spaCy** - NLP and keyword extraction
- **Sentence-Transformers** - Semantic embeddings
- **PyTorch** - Deep learning backend
- **pandas** - Data processing
- **pdfplumber/PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 👤 Author

ARPIT PANDEY 
https://github.com/arpitpandey454507

---

**⭐ Star this repo if you find it useful!**


