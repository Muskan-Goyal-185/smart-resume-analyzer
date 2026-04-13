"""
similarity.py
-------------
Computes the semantic similarity between a resume and a job description
using TF-IDF vectorization and Cosine Similarity.

How It Works:
─────────────
1. TF-IDF (Term Frequency–Inverse Document Frequency):
   - TF: How often a word appears in a document.
   - IDF: How rare the word is across all documents.
   - Together, they give higher weight to meaningful, unique words
     and down-weight common words like "the", "is", "and".

2. Cosine Similarity:
   - Represents each document as a vector of TF-IDF scores.
   - Measures the cosine of the angle between two vectors.
   - Score of 1.0 = identical, 0.0 = completely different.
   - Perfect for comparing documents regardless of length.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_match_score(resume_text: str, jd_text: str) -> float:
    """
    Compute how well a resume matches a job description.

    Args:
        resume_text: Cleaned text from the resume.
        jd_text:     Cleaned text from the job description.

    Returns:
        Match score as a float between 0.0 and 100.0 (percentage).
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    # Step 1: Create TF-IDF vectors for both documents
    # stop_words='english' removes common words like "the", "a", "is"
    vectorizer = TfidfVectorizer(stop_words='english')

    # Fit and transform both texts together so the vocabulary is shared
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])

    # Step 2: Compute cosine similarity between the two vectors
    # tfidf_matrix[0] = resume vector, tfidf_matrix[1] = JD vector
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # Step 3: Convert to percentage and round to 2 decimal places
    return round(score * 100, 2)


def get_score_label(score: float) -> tuple[str, str]:
    """
    Return a human-readable label and color for the match score.

    Args:
        score: Match percentage (0–100).

    Returns:
        Tuple of (label, color_hex) for UI display.
    """
    if score >= 75:
        return "Excellent Match 🎯", "#2ecc71"   # Green
    elif score >= 50:
        return "Good Match 👍", "#f39c12"         # Orange
    elif score >= 30:
        return "Moderate Match ⚠️", "#e67e22"     # Dark Orange
    else:
        return "Low Match ❌", "#e74c3c"           # Red


def generate_suggestions(missing_skills: list[str], score: float) -> list[str]:
    """
    Generate actionable improvement suggestions based on analysis results.

    Args:
        missing_skills: Skills found in JD but absent from resume.
        score:          Overall match score percentage.

    Returns:
        List of suggestion strings to display in the UI.
    """
    suggestions = []

    # Skill-based suggestions
    if missing_skills:
        top_missing = missing_skills[:5]  # Highlight top 5
        suggestions.append(
            f"📚 **Learn these in-demand skills**: {', '.join(top_missing)}"
        )
        suggestions.append(
            "✏️ **Add missing skills** to your resume's Skills section "
            "if you already have experience with them."
        )

    # Score-based suggestions
    if score < 30:
        suggestions.append(
            "🔍 **Significantly tailor your resume** — use keywords "
            "from the job description throughout your resume."
        )
    elif score < 50:
        suggestions.append(
            "🔧 **Improve keyword alignment** — mirror the exact phrasing "
            "from the job description in your experience bullets."
        )
    elif score < 75:
        suggestions.append(
            "✅ **You're close!** Strengthen your project descriptions "
            "with more role-specific terminology."
        )

    # General best-practice suggestions
    suggestions.extend([
        "📊 **Quantify achievements**: e.g., 'Improved model accuracy by 12%' "
        "instead of 'Improved model accuracy'.",
        "🎯 **Add a tailored Summary/Objective** section that mirrors the job role.",
        "🔗 **Include links** to GitHub, portfolio, or relevant certifications.",
        "📝 **Use action verbs**: Built, Designed, Optimized, Led, Deployed, Automated.",
    ])

    return suggestions
