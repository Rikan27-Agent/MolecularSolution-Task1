def compare_results(results, observations=None):
    """Display the comparison."""

    print("=" * 100)
    print("FINAL COMPARISON SUMMARY")
    print("=" * 100)

    print(
        f"{'Library':<15} | "
        f"{'Time (s)':<10} | "
        f"{'Pages':<7} | "
        f"{'Words':<8} | "
        f"{'Chars':<8}"
    )

    print("-" * 100)

    for result in results:

        print(
            f"{result['library']:<15} | "
            f"{result['execution_time_seconds']:<10.4f} | "
            f"{result['pages']:<7} | "
            f"{result['words']:<8} | "
            f"{result['characters']:<8}"
        )

    print("=" * 100)
