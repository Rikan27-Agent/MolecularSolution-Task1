import os
import time
import pdfplumber

from src.preprocessing.text_cleaner import preprocess_pages


def extract_with_pdfplumber(pdf_path):
    """Extract PDF text page-by-page using pdfplumber."""
    pages = []

    with pdfplumber.open(pdf_path) as document:

        for page_number, page in enumerate(document.pages,start=1):
            text = page.extract_text() or ""
            pages.append({
                "page_number": page_number,
                "text": text
            })

    return pages


def process_with_pdfplumber(pdf_path):
    """Extract, preprocess and benchmark a PDF using pdfplumber."""

    start_time = time.perf_counter()

    # 1. Extract
    raw_pages = extract_with_pdfplumber(pdf_path)

    # 2. Preprocess
    processed_pages, removed_headers, removed_footers, removed_page_numbers, preprocessing_stats = preprocess_pages(raw_pages)

    # 3. Statistics
    total_pages = len(processed_pages)

    total_words = sum(
        len(page["cleaned_text"].split())
        for page in processed_pages
    )

    total_characters = sum(
        len(page["cleaned_text"])
        for page in processed_pages
    )

    # 4. Execution time
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return {
        "library": "pdfplumber",
        "source_file": os.path.basename(pdf_path),
        "execution_time_seconds": execution_time,
        "pages": total_pages,
        "words": total_words,
        "characters": total_characters,
        "pages_data": processed_pages,
        "removed_headers": list(removed_headers),
        "removed_footers": list(removed_footers),
        "removed_page_numbers": list(removed_page_numbers),
        "preprocessing_stats": preprocessing_stats
    }