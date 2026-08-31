import re
import unicodedata
from collections import Counter

def normalize_text(text):
    return unicodedata.normalize("NFKC", text)


def clean_unwanted_characters(text):
    cleaned = []
    for char in text:
        if char == "\n" or char == "\t" or char.isprintable():
            cleaned.append(char)
    return "".join(cleaned)


def fix_hyphenated_line_breaks(text):
    return re.sub(r"(\w+)-\s*\n\s*(\w+)", r"\1\2", text)


def remove_headers_footers(pages, threshold=0.7):
    """Remove repeated headers, footers, and page numbers."""

    # -------------------------------------------------
    # Find repeated lines across pages
    # -------------------------------------------------

    page_line_sets = []

    for page in pages:

        lines = [
            line.strip()
            for line in page["text"].splitlines()
            if line.strip()
        ]

        page_line_sets.append(set(lines))

    counts = Counter()

    # Count each line once per page
    for lines in page_line_sets:
        for line in lines:
            counts[line] += 1

    min_pages = max(
        2,
        int(len(pages) * threshold)
    )

    repeated_lines = {
        line
        for line, count in counts.items()
        if count >= min_pages
    }

    # -------------------------------------------------
    # Identify header/footer candidates
    # Only from page margins
    # -------------------------------------------------

    headers = set()
    footers = set()

    for page in pages:

        lines = [
            line.strip()
            for line in page["text"].splitlines()
            if line.strip()
        ]

        # Top 3 lines
        for line in lines[:3]:
            if line in repeated_lines:
                headers.add(line)

        # Bottom 3 lines
        for line in lines[-3:]:
            if line in repeated_lines:
                footers.add(line)

    # -------------------------------------------------
    # Page number pattern
    # -------------------------------------------------

    page_number_pattern = re.compile(
        r"(Page\s+\d+(\s+of\s+\d+)?|\d+\s*/\s*\d+)",
        re.IGNORECASE
    )

    cleaned_pages = []

    removed_headers = set()
    removed_footers = set()
    removed_page_numbers = set()

    # -------------------------------------------------
    # Remove only from actual margin positions
    # -------------------------------------------------

    for page in pages:

        raw_lines = page["text"].splitlines()

        # Find non-empty line indexes
        non_empty_indexes = [
            i
            for i, line in enumerate(raw_lines)
            if line.strip()
        ]

        header_indexes = set(
            non_empty_indexes[:3]
        )

        footer_indexes = set(
            non_empty_indexes[-3:]
        )

        cleaned_lines = []

        for index, line in enumerate(raw_lines):

            stripped = line.strip()

            # Empty line
            if not stripped:
                cleaned_lines.append(line)
                continue

            # Remove header ONLY from top margin
            if (
                index in header_indexes
                and stripped in headers
            ):
                removed_headers.add(stripped)
                continue

            # Remove footer ONLY from bottom margin
            if (
                index in footer_indexes
                and stripped in footers
            ):
                removed_footers.add(stripped)
                continue

            # Remove page number ONLY when it matches
            if (
                index in footer_indexes
                and page_number_pattern.fullmatch(stripped)
            ):
                removed_page_numbers.add(stripped)
                continue

            # Keep everything else
            cleaned_lines.append(line)

        cleaned_pages.append({
            "page_number": page["page_number"],
            "raw_text": page["raw_text"],
            "text": "\n".join(cleaned_lines)
        })

    return (
        cleaned_pages,
        removed_headers,
        removed_footers,
        removed_page_numbers
    )


def remove_spaces_and_blank_lines(text):
    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

def count_blank_lines(text):
    return sum(
        1
        for line in text.splitlines()
        if not line.strip()
    )


def count_extra_spaces(text):
    return len(
        re.findall(r"[ \t]{2,}", text)
    )


def count_unwanted_characters(text):
    return sum(
        1
        for char in text
        if not (char == "\n" or char == "\t" or char.isprintable())
    )


def count_broken_lines(text):
    return len(
        re.findall(
            r"(\w+)-\s*\n\s*(\w+)",
            text
        )
    )


def preprocess_pages(pages):
    """
    Complete text cleaning and preprocessing pipeline.

    Keeps raw text separate from cleaned text.
    """

    # BEFORE PREPROCESSING
    before_words = sum(
        len(page["text"].split())
        for page in pages
    )

    before_characters = sum(
        len(page["text"])
        for page in pages
    )

    before_blank_lines = sum(
        count_blank_lines(page["text"])
        for page in pages
    )

    before_extra_spaces = sum(
        count_extra_spaces(page["text"])
        for page in pages
    )

    before_unwanted_characters = sum(
        count_unwanted_characters(page["text"])
        for page in pages
    )

    before_broken_lines = sum(
        count_broken_lines(page["text"])
        for page in pages
    )

    # Create a copy so original extraction remains unchanged
    processed_pages = []

    for page in pages:
        processed_pages.append({
            "page_number": page["page_number"],
            "raw_text": page["text"]
        })

    # 1. Normalize
    for page in processed_pages:
        page["text"] = normalize_text(page["raw_text"])

    # 2. Remove unwanted characters
    for page in processed_pages:
        page["text"] = clean_unwanted_characters(page["text"])

    # 3. Fix broken lines
    for page in processed_pages:
        page["text"] = fix_hyphenated_line_breaks(page["text"])

    # 4. Remove headers and footers
    (
        cleaned_pages,
        removed_headers,
        removed_footers,
        removed_page_numbers
    ) = remove_headers_footers(processed_pages)

    # 5. Remove spaces and blank lines
    final_pages = []

    for page in cleaned_pages:

        cleaned_text = remove_spaces_and_blank_lines(
            page["text"]
        )

        final_pages.append({
            "page_number": page["page_number"],
            "raw_text": page["raw_text"],
            "cleaned_text": cleaned_text
        })

    # AFTER PREPROCESSING
    after_words = sum(
        len(page["cleaned_text"].split())
        for page in final_pages
    )

    after_characters = sum(
        len(page["cleaned_text"])
        for page in final_pages
    )

    after_blank_lines = sum(
        count_blank_lines(page["cleaned_text"])
        for page in final_pages
    )

    after_extra_spaces = sum(
        count_extra_spaces(page["cleaned_text"])
        for page in final_pages
    )

    after_unwanted_characters = sum(
        count_unwanted_characters(page["cleaned_text"])
        for page in final_pages
    )

    after_broken_lines = sum(
        count_broken_lines(page["cleaned_text"])
        for page in final_pages
    )

    # Preprocessing statistics
    preprocessing_stats = {
        "before": {
            "pages": len(pages),
            "words": before_words,
            "characters": before_characters,
            "headers": len(removed_headers),
            "footers": len(removed_footers),
            "page_numbers": len(removed_page_numbers),
            "blank_lines": before_blank_lines,
            "extra_spaces": before_extra_spaces,
            "unwanted_characters": before_unwanted_characters,
            "broken_lines": before_broken_lines
        },

        "after": {
            "pages": len(final_pages),
            "words": after_words,
            "characters": after_characters,
            "headers": 0,
            "footers": 0,
            "page_numbers": 0,
            "blank_lines": after_blank_lines,
            "extra_spaces": after_extra_spaces,
            "unwanted_characters": after_unwanted_characters,
            "broken_lines": after_broken_lines
        }
    }

    return (
        final_pages,
        removed_headers,
        removed_footers,
        removed_page_numbers,
        preprocessing_stats
    )