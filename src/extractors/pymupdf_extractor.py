import os
import time
import pymupdf

from src.preprocessing.text_cleaner import preprocess_pages


def extract_with_pymupdf(pdf_path):
    """Extract PDF text page-by-page using PyMuPDF."""
    pages = []
    document = pymupdf.open(pdf_path)
    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text")
            pages.append({
                "page_number": page_number,
                "text": text
            })
    finally:
        document.close()
    return pages


def process_with_pymupdf(pdf_path):
    start_time = time.perf_counter()

    # 1. Extract
    raw_pages = extract_with_pymupdf(pdf_path)

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

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return {
        "library": "PyMuPDF",
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