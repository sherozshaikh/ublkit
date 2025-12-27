"""
Unit tests for XML processing.
"""

import pytest
from pathlib import Path

from ublkit.processors.xml_processor import (
    XMLValidator,
    XMLReader,
    NamespaceExtractor,
    XMLProcessor,
)


def test_xml_validator_valid_xml():
    """Test XML validator with valid XML."""
    validator = XMLValidator()
    xml_content = b'<?xml version="1.0"?><root><item>test</item></root>'

    is_valid, error = validator.validate_well_formedness(xml_content)

    assert is_valid is True
    assert error is None


def test_xml_validator_invalid_xml():
    """Test XML validator with malformed XML."""
    validator = XMLValidator()
    xml_content = b'<?xml version="1.0"?><root><item>test</root>'  # Mismatched tags

    is_valid, error = validator.validate_well_formedness(xml_content)

    assert is_valid is False
    assert error is not None
    assert "XML syntax error" in error


def test_xml_processor_sample_invoice(fixtures_dir):
    """Test XML processor with sample invoice."""
    invoice_path = fixtures_dir / "sample_invoice.xml"

    if not invoice_path.exists():
        pytest.skip("Sample invoice not found")

    processor = XMLProcessor(encoding_priority=["utf-8"])
    json_data, doc_type, encoding = processor.process_file(invoice_path)

    assert json_data is not None
    assert isinstance(json_data, dict)
    assert doc_type == "Invoice"
    assert encoding == "utf-8"
    assert "Invoice" in json_data
