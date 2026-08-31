# Task 1 — PDF Document Processing

## 1. Objective

Build a PDF text-processing pipeline that extracts text page-by-page,
cleans the extracted content, stores the result in structured JSON,
and compares five PDF libraries based on execution performance and
extraction output.

Libraries used:

- PyMuPDF
- pdfplumber
- pypdf
- pypdfium2
- pdfminer.six


PyMuPDF: -
•	PyMuPDF is a fast Python library for reading, extracting, rendering, and manipulating PDF documents.
•	It is commonly used for fast text extraction, page-level processing, metadata extraction, PDF       rendering, and document preprocessing.
Pdfplumber: - 
•	pdfplumber is a Python library for extracting text and layout information from PDFs, with particularly useful support for tables and positioned text.
•	It is useful when document layout, text positioning, and table extraction are important.
Pypdf: -
•	pypdf is a pure-Python library used for reading, extracting, and manipulating PDF documents.
•	It is useful for basic text extraction and general PDF operations without focusing heavily on layout analysis.
Pypdfium2: -
•	pypdfium2 is a Python binding for the PDFium library, used for rendering PDF pages and extracting PDF content.
•	It is useful when you need PDF rendering capabilities along with page-level document processing.
Pdfminer.six: -
•	pdfminer.six is a Python library focused on detailed PDF text extraction and layout analysis.
•	It is useful when we need fine-grained control over extracted text and its layout structure.

---

## 2. Project Workflow

```text
                         ┌─────────────────────┐
                         │         PDF         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                  ┌───────────────────────────────┐
                  │        PDF EXTRACTORS         │
                  ├───────────────────────────────┤
                  │ 1. PyMuPDF                    │
                  │ 2. pdfplumber                 │
                  │ 3. pypdf                      │
                  │ 4. pypdfium2                  │
                  │ 5. pdfminer.six               │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │   RAW PAGE-WISE TEXT    │
                    ├─────────────────────────┤
                    │ page_number             │
                    │ raw_text                │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌────────────────────────────────────┐
              │      TEXT CLEANING & PREPROCESSING │
              ├────────────────────────────────────┤
              │ 1. Unicode Normalization           │
              │ 2. Remove Unwanted Characters      │
              │ 3. Fix Broken Lines                │
              │ 4. Detect Repeated Headers         │
              │ 5. Detect Repeated Footers         │
              │ 6. Remove Page Numbers             │
              │ 7. Remove Extra Spaces             │
              │ 8. Remove Blank Lines              │
              └────────────────┬───────────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   CLEANED PAGE-WISE     │
                    ├─────────────────────────┤
                    │ page_number             │
                    │ raw_text                │
                    │ cleaned_text            │
                    └────────────┬────────────┘
                                 │
                ┌────────────────┴─────────────────┐
                │                                  │
                ▼                                  ▼
     ┌─────────────────────────┐      ┌──────────────────────────┐
     │ PREPROCESSING ANALYSIS  │      │   STRUCTURED JSON OUTPUT │
     ├─────────────────────────┤      ├──────────────────────────┤
     │ Before vs After         │      │ library                  │
     │ Words                   │      │ source_file              │
     │ Characters              │      │ page_number              │
     │ Headers                 │      │ raw_text                 │
     │ Footers                 │      │ cleaned_text             │
     │ Page Numbers            │      │ preprocessing statistics │
     │ Blank Lines             │      │ removed headers/footers  │
     │ Extra Spaces            │      └─────────────┬────────────┘
     │ Unwanted Characters     │                    │
     │ Broken Lines            │                    ▼
     └────────────┬────────────┘          ┌───────────────────────┐
                  │                       │      JSON FILE        │
                  │                       └───────────────────────┘
                  │
                  ▼
          ┌───────────────────────────┐
          │ FINAL COMPARISON          │
          ├───────────────────────────┤
          │ • Execution Time          │
          │ • Pages                   │
          │ • Words                   │
          │ • Characters              │
          └───────────────────────────┘

---
### 3. Project Structure

---

Task1/
│
├── data/
│   ├── input/
│   │   ├── document1.pdf
│   │   ├── document2.pdf
│   │   └── document3.pdf
│   │
│   └── output/
│       ├── pymupdf/
│       ├── pdfplumber/
│       ├── pypdf/
│       ├── pypdfium2/
│       └── pdfminer/
│
├── src/
│   │
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pymupdf_extractor.py
│   │   ├── pdfplumber_extractor.py
│   │   ├── pypdf_extractor.py
│   │   ├── pypdfium2_extractor.py
│   │   └── pdfminer_extractor.py
│   │
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   └── text_cleaner.py
│   │
│   ├── output/
│   │   ├── __init__.py
│   │   └── json_writer.py
│   │
│   ├── comparison/
│   │   ├── __init__.py
│   │   └── comparison.py
│   │
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore


## 4. Implementation

### 4.1 PDF Extraction

Each PDF is processed independently using the five selected PDF libraries.

- Opens the PDF file and reads it page-by-page.
- Extracts text from each page.
- Assigns a page number to every extracted page.
- Stores the extracted content in a page-wise structure.
- Keeps the extraction logic separate for each library.
- Uses the same output structure for all five libraries so that their results can be compared consistently.

---

#### 4.2 Text Cleaning & Preprocessing

A common preprocessing pipeline is applied to the extracted text from all five libraries.

##### 4.2.1 Text Normalization

- Normalizes Unicode characters.
- Standardizes different representations of the same character.
- Helps maintain consistency in the extracted text.

##### 4.2.2 Unwanted Character Cleaning

- Removes unwanted control and non-printable characters.
- Preserves required characters such as newlines and tabs.
- Reduces noise from the extracted text.

##### 4.2.3 Broken-Line Handling

- Detects words broken across lines using hyphens.
- Joins the separated parts into a complete word.
- Example: `imple-` + `mentation` → `implementation`.

##### 4.2.4 Repeated Header Detection

- Examines repeated text appearing across multiple pages.
- Checks the top section of each page for repeated content.
- Identifies repeated lines as possible document headers.
- Removes only the detected header content.

##### 4.2.5 Repeated Footer Detection

- Examines the bottom section of each page.
- Detects repeated footer information across pages.
- Removes repeated footer content while keeping the main document content.

##### 4.2.6 Page Number Removal

- Detects common page-number formats such as `Page 4`, `Page 4 of 16`, and `4 / 16`.
- Removes page numbers from the cleaned text.
- Keeps normal numeric content inside the document.

##### 4.2.7 Space Cleaning

- Removes unnecessary spaces and tabs.
- Reduces multiple consecutive spaces to a single space.
- Removes leading and trailing spaces from lines.

##### 4.2.8 Blank-Line Removal

- Removes empty lines that are not required.
- Produces cleaner and more compact extracted text.

---

#### 4.3 Raw and Cleaned Content

- Preserves the original extracted content as `raw_text`.
- Stores the processed content as `cleaned_text`.
- Maintains the page number for both versions.
- Allows direct Before/After comparison of the preprocessing results.

---

#### 4.4 Preprocessing Analysis

The system calculates preprocessing statistics before and after cleaning.

The following metrics are recorded:

- Number of pages
- Number of words
- Number of characters
- Number of detected headers
- Number of detected footers
- Number of page numbers
- Number of blank lines
- Number of extra spaces
- Number of unwanted characters
- Number of broken lines

This allows the effect of the preprocessing stage to be measured.

---

#### 4.5 Structured JSON Generation

The processed result is converted into a structured JSON format.

The JSON contains:

- Library name
- Source PDF file
- Execution time
- Total pages
- Total words
- Total characters
- Removed headers
- Removed footers
- Removed page numbers
- Preprocessing statistics
- Page-wise extracted content
- Original text (`raw_text`)
- Cleaned text (`cleaned_text`)

This provides a consistent machine-readable representation of the processed PDF.

---

#### 4.6 Result Handling

- Displays the result of each PDF library separately.
- Shows execution time, pages, words, and characters.
- Displays Before/After text for a user-selected page.
- Displays detected headers, footers, and page numbers.
- Displays Before/After preprocessing statistics.

---

#### 4.7 Final Comparison

Each library is processed using the same workflow.

The benchmark records:

- Execution time
- Number of pages processed
- Extracted word count
- Extracted character count
- Generated JSON output file

Using the same preprocessing and measurement process allows the five libraries to be compared consistently.

---
### 5. How to Run

pip install -r requirements.txt
python -m src.main

## 6. Observations

- All five libraries successfully processed the tested PDF documents page-by-page.
- Execution time varied across the libraries, showing differences in processing efficiency.
- Word and character counts varied across some documents, indicating differences in extracted text volume.
- The common preprocessing pipeline reduced unwanted content such as repeated headers, footers, page numbers, extra spaces, unwanted characters, and broken-line artifacts.
- Table content was preserved during preprocessing instead of being removed as repeated document content.
- The generated JSON provides both `raw_text` and `cleaned_text`, allowing the extraction and preprocessing results to be inspected directly.
- Different PDF structures, such as tables, multi-column layouts, and visual elements, can produce different extraction results across libraries.


#### Sample Observation 1 :- 
======================================================================
PyMuPDF RESULT
======================================================================
Library        : PyMuPDF
Execution Time : 0.025629 s
Pages          : 16
Words          : 2635
Characters     : 18976
======================================================================
======================================================================
pdfplumber RESULT
======================================================================
Library        : pdfplumber
Execution Time : 0.454614 s
Pages          : 16
Words          : 2643
Characters     : 19728
======================================================================
======================================================================
pypdf RESULT
======================================================================
Library        : pypdf
Execution Time : 0.178856 s
Pages          : 16
Words          : 2630
Characters     : 18977
======================================================================
======================================================================
pypdfium2 RESULT
======================================================================
Library        : pypdfium2
Execution Time : 0.041884 s
Pages          : 16
Words          : 2780
Characters     : 19825
======================================================================
======================================================================
pdfminer.six RESULT
======================================================================
Library        : pdfminer.six
Execution Time : 0.951684 s
Pages          : 16
Words          : 2714
Characters     : 19183
======================================================================

Enter page number (1-16): 9

======================================================================
BEFORE / AFTER CLEANING
======================================================================

PAGE 9 - BEFORE CLEANING
----------------------------------------------------------------------
CONFIDENTIAL — DOCUMENT EXTRACTION TEST
SECTION 09 — EXTRACTION CHECKLIST
REV. 3.7
4. Table Extraction Complexity
The next table intentionally spans multiple pages. Its header repeats after page breaks. It contains null cells,
N/A markers, negative values, percentages, dates, and mixed alignment.
Item
Description
Category
Qty
Unit Price
Discount
Tax
Net
Status
Review Date
ITM-001
ITM-002
ITM-003
ITM-004
ITM-005
ITM-006
ITM-007
ITM-008
ITM-009
ITM-010
ITM-011
ITM-012
ITM-013
ITM-014
ITM-015
ITM-016
ITM-017
ITM-018
ITM-019
ITM-020
ITM-021
ITM-022
ITM-023
ITM-024
ITM-025
ITM-026
ITM-027
ITM-028
ITM-029
ITM-030
ITM-031
ITM-032
ITM-033
ITM-034
ITM-035
ITM-036
ITM-037
ITM-038
ITM-039
ITM-040
ITM-041
ITM-042
ITM-043
ITM-044
ITM-045
Audit
Synthetic transaction record 01 with intentionally long descriptive text for row-boundary testing.
137.25
8
Synthetic transaction record 02 with intentionally long descriptive text for row-boundary testing.
Support
274.50
15
Risk
Synthetic transaction record 03 with intentionally long descriptive text for row-boundary testing.
411.75
3
Core
Synthetic transaction record 04 with intentionally long descriptive text for row-boundary testing.
549.00
10
Audit
Synthetic transaction record 05 with intentionally long descriptive text for row-boundary testing.
686.25
17
Synthetic transaction record 06 with intentionally long descriptive text for row-boundary testing.
Support
823.50
5
Risk
Synthetic transaction record 07 with intentionally long descriptive tex

PAGE 9 - AFTER CLEANING
----------------------------------------------------------------------
4. Table Extraction Complexity
The next table intentionally spans multiple pages. Its header repeats after page breaks. It contains null cells,
N/A markers, negative values, percentages, dates, and mixed alignment.
Item
Description
Category
Qty
Unit Price
Discount
Tax
Net
Status
Review Date
ITM-001
ITM-002
ITM-003
ITM-004
ITM-005
ITM-006
ITM-007
ITM-008
ITM-009
ITM-010
ITM-011
ITM-012
ITM-013
ITM-014
ITM-015
ITM-016
ITM-017
ITM-018
ITM-019
ITM-020
ITM-021
ITM-022
ITM-023
ITM-024
ITM-025
ITM-026
ITM-027
ITM-028
ITM-029
ITM-030
ITM-031
ITM-032
ITM-033
ITM-034
ITM-035
ITM-036
ITM-037
ITM-038
ITM-039
ITM-040
ITM-041
ITM-042
ITM-043
ITM-044
ITM-045
Audit
Synthetic transaction record 01 with intentionally long descriptive text for row-boundary testing.
137.25
8
Synthetic transaction record 02 with intentionally long descriptive text for row-boundary testing.
Support
274.50
15
Risk
Synthetic transaction record 03 with intentionally long descriptive text for row-boundary testing.
411.75
3
Core
Synthetic transaction record 04 with intentionally long descriptive text for row-boundary testing.
549.00
10
Audit
Synthetic transaction record 05 with intentionally long descriptive text for row-boundary testing.
686.25
17
Synthetic transaction record 06 with intentionally long descriptive text for row-boundary testing.
Support
823.50
5
Risk
Synthetic transaction record 07 with intentionally long descriptive text for row-boundary testing.
960.75
12
Core
Synthetic transaction record 08 with int

REMOVED HEADERS
----------------------------------------------------------------------
- CONFIDENTIAL — DOCUMENT EXTRACTION TEST
- REV. 3.7
- SECTION 09 — EXTRACTION CHECKLIST

REMOVED FOOTERS
----------------------------------------------------------------------
- CONFIDENTIAL — SYNTHETIC TEST DOCUMENT

REMOVED PAGE NUMBERS
----------------------------------------------------------------------
- Page 16 of 16
- Page 1 of 16
- Page 11 of 16
- Page 13 of 16
- Page 6 of 16
- Page 4 of 16
- Page 9 of 16
- Page 10 of 16
- Page 14 of 16
- Page 12 of 16
- Page 8 of 16
- Page 7 of 16
- Page 3 of 16
- Page 15 of 16
- Page 2 of 16

======================================================================
TEXT PREPROCESSING COMPARISON
======================================================================
Metric                   Before      After       
--------------------------------------------------
pages                    16          16          
words                    3040        2714        
characters               21326       19183       
headers                  3           0           
footers                  1           0           
page_numbers             15          0           
blank_lines              10          0           
extra_spaces             11          0           
unwanted_characters      3           0           
broken_lines             4           0           
======================================================================
====================================================================================================
FINAL COMPARISON SUMMARY
====================================================================================================
Library         | Time (s)   | Pages   | Words    | Chars   
----------------------------------------------------------------------------------------------------
PyMuPDF         | 0.0256     | 16      | 2635     | 18976   
pdfplumber      | 0.4546     | 16      | 2643     | 19728   
pypdf           | 0.1789     | 16      | 2630     | 18977   
pypdfium2       | 0.0419     | 16      | 2780     | 19825   
pdfminer.six    | 0.9517     | 16      | 2714     | 19183   
====================================================================================================
---
### 7. Conclusion

- The task successfully implements PDF extraction, text cleaning, structured JSON generation.
- The five libraries showed different processing times and extraction outputs.
- Execution time alone is not sufficient to determine extraction quality.
- The actual extracted content and document structure must also be considered.
- The appropriate library depends on the PDF structure and application requirements.
