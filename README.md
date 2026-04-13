# 📄 Smart Resume Analyzer

> An NLP-powered web app that compares your resume against a job description
> and gives you a match score, skill gap analysis, and improvement suggestions.

---

## Quick Start

```bash
# 1. Clone / download the project
cd smart_resume_analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Project Structure

```
smart_resume_analyzer/
│
├── app.py               ← Streamlit UI (main entry point)
├── resume_parser.py     ← PDF/TXT text extraction
├── skill_extractor.py   ← Keyword-based skill matching
├── similarity.py        ← TF-IDF + Cosine Similarity engine
├── skills_data.py       ← Master skills database (150+ skills)
├── requirements.txt     ← Python dependencies
└── README.md            ← This file
```

---

##  How It Works

### 1. Resume Parsing
- PDF files are read using `pdfplumber`
- Text files are decoded directly
- Text is cleaned (whitespace, encoding artifacts removed)

### 2. Skill Extraction
- Text is matched against a 150+ skill database (`skills_data.py`)
- Multi-word skills (e.g., "machine learning") use phrase matching
- Single-word skills use regex word boundaries to avoid false positives

### 3. Match Scoring (TF-IDF + Cosine Similarity)
- Both texts are converted to TF-IDF vectors
- Cosine similarity measures how "close" the two vectors are
- Score is converted to a 0–100% percentage

### 4. Skill Gap Analysis
- Compares resume skills vs JD skills (set difference)
- Missing skills are clearly highlighted

### 5. Suggestions
- Personalized advice based on score range and missing skills

---

## Output Example

```
Match Score:       72.4%  →  Good Match 👍
Resume Skills:     Python, SQL, Pandas, Scikit-Learn, Git
JD Skills:         Python, SQL, TensorFlow, AWS, Docker, Pandas
Missing Skills:    TensorFlow, AWS, Docker

Suggestions:
  Learn: TensorFlow, AWS, Docker
  Add missing skills to your resume if you have experience
  Strengthen project descriptions with role-specific terms
```

---

## Future Enhancements

- [ ] Named Entity Recognition (NER) for smarter skill extraction
- [ ] BERT/Sentence-Transformers for semantic (not just keyword) similarity
- [ ] Export report as PDF
- [ ] Resume scoring rubric (ATS compatibility check)
- [ ] Multi-resume batch comparison
- [ ] Job description scraper from LinkedIn/Indeed URLs
