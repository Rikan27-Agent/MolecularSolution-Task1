import os
import time

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

from src.preprocessing.text_cleaner import preprocess_pages


def extract_with_pdfminer(pdf_path):
    """Extract PDF text page-by-page using pdfminer.six."""
    pages = []
    for page_number, page_layout in enumerate(extract_pages(pdf_path),start=1):
        text_parts = []
        
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text_parts.append(element.get_text())

        pages.append({
            "page_number": page_number,
            "text": "".join(text_parts)
        })

    return pages


def process_with_pdfminer(pdf_path):
    """Extract, preprocess and benchmark a PDF using pdfminer.six."""

    start_time = time.perf_counter()

    # 1. Extract
    raw_pages = extract_with_pdfminer(pdf_path)

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
        "library": "pdfminer.six",
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