import json
from pathlib import Path


def save_json(result: dict, output_dir: str) -> str:
    """
    Save the processed PDF result as a JSON file.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    library = result["library"].lower()
    filename = library.replace(".", "_").replace(" ", "_")

    output_path = (
        output_dir / f"extracted_output_{filename}.json"
    )

    output_data = {
        "library": result["library"],
        "source_file": result["source_file"],
        "execution_time_seconds": result["execution_time_seconds"],
        "total_pages": result["pages"],
        "total_words": result["words"],
        "total_characters": result["characters"],

        "removed_headers": result["removed_headers"],
        "removed_footers": result["removed_footers"],
        "removed_page_numbers": result["removed_page_numbers"],

        "preprocessing_stats": result["preprocessing_stats"],

        "pages": result["pages_data"]
    }

    with open(output_path,"w",encoding="utf-8") as file:
        json.dump(output_data,file,ensure_ascii=False,indent=2)
    return str(output_path)