"""
skill_extractor.py
------------------
Extracts skills from text (resume or job description) by matching
against a curated skills database using keyword matching.

Uses lowercase + multi-word phrase matching for accuracy.
"""

from skills_data import SKILLS_DB


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from a given text by matching against SKILLS_DB.

    Strategy:
    - Normalize text to lowercase for case-insensitive matching.
    - Use word-boundary-aware phrase matching to avoid false positives
      (e.g., "r" should not match inside "framework").
    - Multi-word skills (e.g., "machine learning") are checked as substrings.

    Args:
        text: Cleaned text string from resume or job description.

    Returns:
        Sorted list of unique skills found in the text.
    """
    import re
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILLS_DB:
        skill_lower = skill.lower()

        if " " in skill_lower:
            # Multi-word skill: check as a phrase (e.g., "machine learning")
            if skill_lower in text_lower:
                found_skills.add(skill.title())
        else:
            # Single-word skill: use word boundaries to avoid partial matches
            # e.g., "r" won't match inside "programming"
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill.title())

    return sorted(found_skills)


def get_skill_gap(resume_skills: list[str], jd_skills: list[str]) -> list[str]:
    """
    Identify skills required by the job but missing from the resume.

    Args:
        resume_skills: List of skills extracted from resume.
        jd_skills:     List of skills extracted from job description.

    Returns:
        List of missing skills (case-insensitive comparison).
    """
    # Normalize to lowercase sets for fair comparison
    resume_set = {s.lower() for s in resume_skills}
    jd_set = {s.lower() for s in jd_skills}

    # Skills in JD but NOT in resume
    missing = jd_set - resume_set

    # Return original-cased versions from jd_skills
    missing_display = [s for s in jd_skills if s.lower() in missing]
    return sorted(missing_display)
