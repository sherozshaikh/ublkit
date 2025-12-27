"""
Example: Batch Processing

This example demonstrates converting multiple UBL XML files in a directory
to JSON or CSV format using ublkit. Files are written to disk and a summary
is generated.
"""

from ublkit import convert_batch


def main():
    # Convert all XML files in directory to CSV
    summary = convert_batch(
        input_dir="./xml_files",
        output_dir="./output",
        output_format="csv",  # or "json"
        config_path="ublkit.yaml",
    )

    # Print summary
    print(f"{'=' * 60}")
    print("Batch Conversion Summary")
    print(f"{'=' * 60}")
    print(f"Total files: {summary.total_files}")
    print(f"Successful: {summary.successful}")
    print(f"Failed: {summary.failed}")
    print(f"Output format: {summary.output_format}")

    # Calculate duration
    if summary.start_time and summary.end_time:
        duration = (summary.end_time - summary.start_time).total_seconds()
        print(f"Duration: {duration:.2f}s")

    # Show failed files if any
    if summary.failed > 0:
        print(f"\n⚠ Failed files:")
        for result in summary.results:
            if not result.success:
                print(f"  - {result.file_path.name}: {result.error_message}")

    # Show successful files
    print(f"\n✓ Successfully processed {summary.successful} files")
    for result in summary.results:
        if result.success:
            print(
                f"  - {result.file_path.name} -> {result.output_path.name if result.output_path else 'N/A'}"
            )
            print(
                f"    Type: {result.ubl_document_type}, Time: {result.processing_time_seconds:.3f}s"
            )

    # Summary file location
    print(f"\nDetailed summary saved to: ./summaries/")


if __name__ == "__main__":
    main()
