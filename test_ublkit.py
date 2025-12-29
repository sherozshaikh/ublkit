"""
Test script for ublkit configuration changes.

Tests all combinations of namespace prefix and JSON flattening options.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ublkit import convert_file


def test_configuration(test_name: str, xml_path: str, config_path: str):
    """Test a specific configuration."""
    print(f"\n{'=' * 60}")
    print(f"Test: {test_name}")
    print(f"{'=' * 60}")

    try:
        result = convert_file(
            xml_path=xml_path,
            output_format="json",
            config_path=config_path,
        )

        if result["success"]:
            print(f"✓ Success")
            print(f"  Document type: {result['ubl_document_type']}")
            print(f"  Processing time: {result['processing_time_seconds']:.4f}s")

            # Show first few keys
            content = result["content"]
            if isinstance(content, dict):
                keys = list(content.keys())[:5]
                print(f"  Sample keys: {keys}")

            return True
        else:
            print(f"✗ Failed: {result['error_message']}")
            return False

    except Exception as e:
        print(f"✗ Exception: {type(e).__name__}: {e}")
        return False


def main():
    """Run all tests."""
    fixtures_dir = Path("tests/fixtures")
    xml_file = fixtures_dir / "sample_invoice.xml"

    if not Path(xml_file).exists():
        print(f"Error: {xml_file} not found")
        return

    tests = [
        ("Default (no prefix, nested)", fixtures_dir / "ublkit_test_1.yaml"),
        ("With prefix, nested", fixtures_dir / "ublkit_test_2.yaml"),
        ("With prefix, flattened", fixtures_dir / "ublkit_test_3.yaml"),
        ("No prefix, flattened", fixtures_dir / "ublkit_test_4.yaml"),
    ]

    results = []
    for test_name, config in tests:
        if not Path(config).exists():
            print(f"\nSkipping: {test_name} (config not found: {config})")
            continue
        results.append(test_configuration(test_name, xml_file, config))

    print(f"\n{'=' * 60}")
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
