"""
resume_parser.py
----------------
Handles extraction of raw text from uploaded resume files.
Supports both PDF and plain text (.txt) formats.
"""

import pdfplumber  # For PDF text extraction
import re


def extract_text_from_pdf(file) -> str:
    """
    Extract all text from a PDF file object (e.g., from Streamlit uploader).

    Args:
        file: A file-like object (BytesIO) from Streamlit's file_uploader.

    Returns:
        A single string containing all extracted text from the PDF.
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Some pages may be blank or image-only
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Failed to read PDF: {e}")
    return text.strip()


def extract_text_from_txt(file) -> str:
    """
    Extract text from a plain .txt file object.

    Args:
        file: A file-like object from Streamlit's file_uploader.

    Returns:
        A decoded string of the file's contents.
    """
    try:
        return file.read().decode("utf-8").strip()
    except Exception as e:
        raise ValueError(f"Failed to read text file: {e}")


def clean_text(text: str) -> str:
    """
    Clean extracted text by removing special characters and extra whitespace.
    Keeps letters, numbers, and basic punctuation.

    Args:
        text: Raw text string.

    Returns:
        Cleaned, normalized text string.
    """
    # Replace multiple newlines/spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove non-ASCII characters (e.g., weird PDF encoding artifacts)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()


def parse_resume(file) -> str:
    """
    Main entry point for resume parsing.
    Detects file type and routes to the appropriate extractor.

    Args:
        file: Streamlit UploadedFile object.

    Returns:
        Cleaned text string from the resume.
    """
    filename = file.name.lower()

    if filename.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file)
    elif filename.endswith(".txt"):
        raw_text = extract_text_from_txt(file)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")

    return clean_text(raw_text)
