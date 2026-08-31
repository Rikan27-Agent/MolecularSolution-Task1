from src.extractors.pymupdf_extractor import process_with_pymupdf
from src.extractors.pdfplumber_extractor import process_with_pdfplumber
from src.extractors.pypdf_extractor import process_with_pypdf
from src.extractors.pypdfium2_extractor import process_with_pypdfium2
from src.extractors.pdfminer_extractor import process_with_pdfminer

from src.output.result import (
    detail_analysis,
    display_result,
    display_preprocessing_stats
)

from src.output.json_writer import save_json

from src.comparison.comparison import compare_results


def main():

    pdf_path = "data/input/new_table1.pdf"

    # Output directory
    output_dir = "data/output"

    results = []

    processors = [
        process_with_pymupdf,
        process_with_pdfplumber,
        process_with_pypdf,
        process_with_pypdfium2,
        process_with_pdfminer
    ]   

    for process in processors:

        result = process(pdf_path)
        
        display_result(result)# Display individual library result

        # Save JSON output
        output_path = save_json(
            result,
            output_dir
        )

        result["output_file"] = output_path

        results.append(result)# Store result


    page_number = int(input(f"\nEnter page number "f"(1-{results[0]['pages']}): "))

    # Show analysis for the last processed library
    detail_analysis(results[-1],page_number)

    # Show preprocessing statistics
    display_preprocessing_stats(results[-1])

    compare_results(results,)


if __name__ == "__main__":
    main()