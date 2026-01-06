"""
Example: Single File Conversion to JSON

This example demonstrates converting a single UBL XML file to JSON format
using ublkit. The conversion happens in-memory and returns the result.
"""

from ublkit import convert_file


def main():
    result = convert_file(
        xml_path="invoice.xml", output_format="json", config_path="ublkit.yaml"
    )

    if result["success"]:
        print("✓ Conversion successful!")
        print(f"  Document type: {result['ubl_document_type']}")
        print(f"  File size: {result['file_size_bytes']:,} bytes")
        print(f"  Processing time: {result['processing_time_seconds']:.3f}s")
        print(f"  Format: {result['output_format']}")

        data = result["content"]
        print(f"\n  Data keys: {list(data.keys())}")

    else:
        print("✗ Conversion failed!")
        print(f"  Error: {result['error_message']}")


if __name__ == "__main__":
    main()
