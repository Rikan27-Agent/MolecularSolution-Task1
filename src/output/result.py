def display_result(result):
    """Display processing result for any PDF library."""

    print("=" * 70)
    print(f"{result['library']} RESULT")
    print("=" * 70)

    print(f"Library        : {result['library']}")
    print(
        f"Execution Time : "
        f"{result['execution_time_seconds']:.6f} s"
    )
    print(f"Pages          : {result['pages']}")
    print(f"Words          : {result['words']}")
    print(f"Characters     : {result['characters']}")

    print("=" * 70)


def detail_analysis(result, page_number):
    """Display before/after cleaning and preprocessing details."""

    page = next(
        (
            page for page in result["pages_data"]
            if page["page_number"] == page_number
        ),
        None
    )

    if page is None:
        print(f"Page {page_number} not found.")
        return

    print("\n" + "=" * 70)
    print("BEFORE / AFTER CLEANING")
    print("=" * 70)

    print(f"\nPAGE {page_number} - BEFORE CLEANING")
    print("-" * 70)
    print(page["raw_text"][:1500])

    print(f"\nPAGE {page_number} - AFTER CLEANING")
    print("-" * 70)
    print(page["cleaned_text"][:1500])

    print("\nREMOVED HEADERS")
    print("-" * 70)

    if result["removed_headers"]:
        for header in result["removed_headers"]:
            print(f"- {header}")
    else:
        print("No repeated headers detected.")

    print("\nREMOVED FOOTERS")
    print("-" * 70)

    if result["removed_footers"]:
        for footer in result["removed_footers"]:
            print(f"- {footer}")
    else:
        print("No repeated footers detected.")

    print("\nREMOVED PAGE NUMBERS")
    print("-" * 70)

    if result["removed_page_numbers"]:
        for number in result["removed_page_numbers"]:
            print(f"- {number}")
    else:
        print("No page numbers detected.")


def display_preprocessing_stats(result):
    """Display before and after preprocessing statistics."""

    stats = result["preprocessing_stats"]

    print("\n" + "=" * 70)
    print("TEXT PREPROCESSING COMPARISON")
    print("=" * 70)

    print(
        f"{'Metric':<25}"
        f"{'Before':<12}"
        f"{'After':<12}"
    )

    print("-" * 50)

    for metric in stats["before"]:
        print(
            f"{metric:<25}"
            f"{stats['before'][metric]:<12}"
            f"{stats['after'][metric]:<12}"
        )

    print("=" * 70)