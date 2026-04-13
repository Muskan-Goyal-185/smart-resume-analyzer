"""
app.py
------
Main Streamlit application for the Smart Resume Analyzer.
Run with: streamlit run app.py

UI Flow:
  1. User uploads a resume (PDF or TXT)
  2. User pastes a job description
  3. Click "Analyze" → displays match score, skills, gaps, suggestions
"""

import streamlit as st
from resume_parser import parse_resume
from skill_extractor import extract_skills, get_skill_gap
from similarity import compute_match_score, get_score_label, generate_suggestions


# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS Styling ────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background and font */
    .main { background-color: #0f1117; }

    /* Header styling */
    .app-header {
        background: linear-gradient(135deg, #1a1f36 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .app-header h1 {
        color: #58a6ff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .app-header p {
        color: #8b949e;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #161b22, #1c2128);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-number {
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1;
    }

    /* Skill badge styling */
    .skill-badge {
        display: inline-block;
        background-color: #1f6feb22;
        border: 1px solid #1f6feb;
        color: #58a6ff;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .missing-badge {
        display: inline-block;
        background-color: #f8514922;
        border: 1px solid #f85149;
        color: #ff7b72;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .found-badge {
        display: inline-block;
        background-color: #2ea04322;
        border: 1px solid #2ea043;
        color: #3fb950;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.82rem;
        font-weight: 500;
    }

    /* Section cards */
    .section-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .section-title {
        color: #e6edf3;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
    }

    /* Suggestion item */
    .suggestion-item {
        background: #1c2128;
        border-left: 3px solid #58a6ff;
        border-radius: 0 6px 6px 0;
        padding: 0.7rem 1rem;
        margin-bottom: 0.6rem;
        color: #c9d1d9;
        font-size: 0.9rem;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f6feb, #388bfd);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #388bfd, #58a6ff);
        transform: translateY(-1px);
    }

    /* Metric styling */
    .stat-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 700; color: #58a6ff; }
    .stat-label  { font-size: 0.8rem; color: #8b949e; margin-top: 0.2rem; }

    /* Divider */
    hr { border-color: #30363d; }
</style>
""", unsafe_allow_html=True)


# ── App Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>📄 Smart Resume Analyzer</h1>
    <p>Upload your resume · Paste a job description · Get instant AI-powered insights</p>
</div>
""", unsafe_allow_html=True)


# ── Input Section ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📎 Upload Resume")
    uploaded_file = st.file_uploader(
        "Supported formats: PDF, TXT",
        type=["pdf", "txt"],
        help="Upload your resume in PDF or plain text format.",
    )

with col2:
    st.markdown("### 📋 Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=220,
        placeholder="e.g., We are looking for a Data Scientist with experience in Python, "
                    "machine learning, TensorFlow, SQL, and data visualization...",
    )

st.markdown("---")

# ── Analyze Button ────────────────────────────────────────────────────────────
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    analyze_clicked = st.button("🔍 Analyze Now")


# ── Analysis Logic & Results ──────────────────────────────────────────────────
if analyze_clicked:

    # ── Validation ────────────────────────────────────────────────────────────
    if not uploaded_file:
        st.error("⚠️ Please upload a resume file (PDF or TXT).")
        st.stop()
    if not job_description.strip():
        st.error("⚠️ Please paste a job description.")
        st.stop()

    # ── Processing ────────────────────────────────────────────────────────────
    with st.spinner("🔄 Analyzing your resume..."):

        # 1. Parse resume text
        resume_text = parse_resume(uploaded_file)

        if not resume_text:
            st.error("❌ Could not extract text from the resume. "
                     "Ensure the PDF is not scanned/image-only.")
            st.stop()

        # 2. Compute match score
        match_score = compute_match_score(resume_text, job_description)
        score_label, score_color = get_score_label(match_score)

        # 3. Extract skills
        resume_skills = extract_skills(resume_text)
        jd_skills     = extract_skills(job_description)

        # 4. Find skill gap
        missing_skills = get_skill_gap(resume_skills, jd_skills)

        # 5. Generate suggestions
        suggestions = generate_suggestions(missing_skills, match_score)

    st.success("✅ Analysis complete!")
    st.markdown("---")

    # ─────────────────────────────────────────────────────────────────────────
    # RESULTS SECTION
    # ─────────────────────────────────────────────────────────────────────────

    # ── Row 1: Score + Quick Stats ────────────────────────────────────────────
    st.markdown("## 📊 Analysis Results")
    r1col1, r1col2, r1col3, r1col4 = st.columns([2, 1, 1, 1])

    with r1col1:
        st.markdown(f"""
        <div class="score-card">
            <div style="color:#8b949e; font-size:0.9rem; margin-bottom:0.5rem;">
                OVERALL MATCH SCORE
            </div>
            <div class="score-number" style="color:{score_color}">
                {match_score}%
            </div>
            <div style="color:{score_color}; font-size:1rem; margin-top:0.5rem;">
                {score_label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Progress bar (native Streamlit)
        st.progress(int(match_score))

    with r1col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(resume_skills)}</div>
            <div class="stat-label">Skills in Resume</div>
        </div>""", unsafe_allow_html=True)

    with r1col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{len(jd_skills)}</div>
            <div class="stat-label">Skills in JD</div>
        </div>""", unsafe_allow_html=True)

    with r1col4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-number" style="color:#ff7b72">{len(missing_skills)}</div>
            <div class="stat-label">Missing Skills</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Skills Columns ─────────────────────────────────────────────────
    r2col1, r2col2 = st.columns(2, gap="large")

    with r2col1:
        st.markdown('<div class="section-card">'
                    '<div class="section-title">✅ Skills Found in Resume</div>',
                    unsafe_allow_html=True)
        if resume_skills:
            badges = "".join(
                f'<span class="found-badge">{s}</span>'
                for s in resume_skills
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No recognizable skills found in resume.")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2col2:
        st.markdown('<div class="section-card">'
                    '<div class="section-title">🎯 Skills Required by Job</div>',
                    unsafe_allow_html=True)
        if jd_skills:
            badges = "".join(
                f'<span class="skill-badge">{s}</span>'
                for s in jd_skills
            )
            st.markdown(badges, unsafe_allow_html=True)
        else:
            st.info("No recognizable skills found in job description.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 3: Missing Skills ──────────────────────────────────────────────────
    st.markdown('<div class="section-card">'
                '<div class="section-title">⚠️ Missing Skills — Skill Gap Analysis</div>',
                unsafe_allow_html=True)
    if missing_skills:
        badges = "".join(
            f'<span class="missing-badge">⛔ {s}</span>'
            for s in missing_skills
        )
        st.markdown(badges, unsafe_allow_html=True)
    else:
        st.markdown(
            '<span style="color:#3fb950">🎉 Great news! Your resume covers '
            'all skills mentioned in the job description.</span>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Row 4: Suggestions ─────────────────────────────────────────────────────
    st.markdown("### 💡 Personalized Suggestions to Improve Your Resume")
    for suggestion in suggestions:
        st.markdown(
            f'<div class="suggestion-item">{suggestion}</div>',
            unsafe_allow_html=True,
        )

    # ── Row 5: Extracted Resume Text (optional expander) ─────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📃 View Extracted Resume Text"):
        st.text_area("Resume Content", resume_text, height=250, disabled=True)


# ── Footer ────────────────────────────────────────────────────────────────────
else:
    # Show instructions when no analysis has been run yet
    st.markdown("""
    <div style="text-align:center; color:#8b949e; padding:2rem">
        <div style="font-size:3rem">🚀</div>
        <div style="font-size:1rem; margin-top:1rem">
            Upload your resume and paste a job description above,<br>
            then click <strong style="color:#58a6ff">Analyze Now</strong> to get your results.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<hr>
<div style="text-align:center; color:#8b949e; font-size:0.8rem; padding:1rem 0">
    Smart Resume Analyzer · Built with Python, NLP & Streamlit ·
    TF-IDF + Cosine Similarity
</div>
""", unsafe_allow_html=True)
