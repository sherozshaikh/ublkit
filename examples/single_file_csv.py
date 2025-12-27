"""
Example: Single File Conversion to CSV

This example demonstrates converting a single UBL XML file to CSV format
using ublkit. The conversion happens in-memory and returns flattened key-value pairs.
"""

from ublkit import convert_file
import json


def main():
    # Convert single XML file to CSV
    result = convert_file(
        xml_path="invoice.xml", output_format="csv", config_path="ublkit.yaml"
    )

    # Check if conversion was successful
    if result["success"]:
        print(f"✓ Conversion successful!")
        print(f"  Document type: {result['ubl_document_type']}")
        print(f"  File size: {result['file_size_bytes']:,} bytes")
        print(f"  Processing time: {result['processing_time_seconds']:.3f}s")
        print(f"  Format: {result['output_format']}")

        # Access the converted data (list of key-value pairs)
        data = result["content"]
        print(f"\n  Total key-value pairs: {len(data)}")

        # Preview first few pairs
        print("\n  First 5 pairs:")
        for pair in data[:5]:
            print(f"    {pair['key']}: {pair['value']}")

        # You can save to CSV file:
        # import polars as pl
        # df = pl.DataFrame(data)
        # df.write_csv("output.csv")
    else:
        print(f"✗ Conversion failed!")
        print(f"  Error: {result['error_message']}")


if __name__ == "__main__":
    main()
