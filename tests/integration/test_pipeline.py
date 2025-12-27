"""
Integration tests for complete pipeline with various UBL document types.

Tests processing of Invoice, CreditNote, Order, and DespatchAdvice documents.
"""

import pytest
from pathlib import Path

from ublkit import convert_file, convert_batch


class TestSingleFileConversion:
    """Test single file conversion with different UBL document types."""

    def test_simple_invoice(self, fixtures_dir, sample_config_path):
        """Test conversion of simple invoice to JSON."""
        xml_file = fixtures_dir / "sample_invoice.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["error_message"] == ""
        assert result["ubl_document_type"] == "Invoice"
        assert result["output_format"] == "json"
        assert result["content"] is not None
        assert "Invoice" in result["content"]

    def test_invoice_multi_tax(self, fixtures_dir, sample_config_path):
        """Test conversion of Canadian invoice with multiple tax schemes."""
        xml_file = fixtures_dir / "sample_invoice_multi_tax.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["ubl_document_type"] == "Invoice"
        assert "Invoice" in result["content"]

        # Verify tax schemes are present
        content = result["content"]["Invoice"]
        assert "TaxTotal" in content

    def test_invoice_with_order_reference(self, fixtures_dir, sample_config_path):
        """Test conversion of invoice with order reference."""
        xml_file = fixtures_dir / "sample_invoice_with_order.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["ubl_document_type"] == "Invoice"

        # Verify order reference is present
        content = result["content"]["Invoice"]
        assert "OrderReference" in content

    def test_creditnote(self, fixtures_dir, sample_config_path):
        """Test conversion of CreditNote document."""
        xml_file = fixtures_dir / "sample_creditnote.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["ubl_document_type"] == "CreditNote"
        assert "CreditNote" in result["content"]

        # Verify credit note specific fields
        content = result["content"]["CreditNote"]
        assert "CreditNoteLine" in content

    def test_order(self, fixtures_dir, sample_config_path):
        """Test conversion of Order document."""
        xml_file = fixtures_dir / "sample_order.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["ubl_document_type"] == "Order"
        assert "Order" in result["content"]

        # Verify order specific fields
        content = result["content"]["Order"]
        assert "OrderLine" in content

    def test_despatchadvice(self, fixtures_dir, sample_config_path):
        """Test conversion of DespatchAdvice document."""
        xml_file = fixtures_dir / "sample_despatchadvice.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["ubl_document_type"] == "DespatchAdvice"
        assert "DespatchAdvice" in result["content"]

        # Verify despatch advice specific fields
        content = result["content"]["DespatchAdvice"]
        assert "DespatchLine" in content
        assert "Shipment" in content


class TestCSVConversion:
    """Test CSV conversion with flattened key-value pairs."""

    def test_invoice_to_csv(self, fixtures_dir, sample_config_path):
        """Test conversion of invoice to CSV format."""
        xml_file = fixtures_dir / "sample_invoice.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="csv",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert result["output_format"] == "csv"
        assert isinstance(result["content"], list)
        assert len(result["content"]) > 0

        # Verify CSV structure
        first_pair = result["content"][0]
        assert "key" in first_pair
        assert "value" in first_pair
        assert "source_file" in first_pair

    def test_creditnote_to_csv(self, fixtures_dir, sample_config_path):
        """Test conversion of CreditNote to CSV format."""
        xml_file = fixtures_dir / "sample_creditnote.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="csv",
            config_path=str(sample_config_path),
        )

        assert result["success"] is True
        assert isinstance(result["content"], list)
        assert len(result["content"]) > 0


class TestBatchProcessing:
    """Test batch processing of multiple files."""

    def test_batch_conversion_json(
        self, fixtures_dir, sample_config_path, temp_output_dir
    ):
        """Test batch conversion to JSON format."""
        summary = convert_batch(
            input_dir=str(fixtures_dir),
            output_dir=str(temp_output_dir),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert summary.total_files > 0
        assert summary.successful > 0
        assert summary.output_format == "json"

        # Verify output files were created
        output_files = list(temp_output_dir.glob("*.json"))
        assert len(output_files) > 0

    def test_batch_conversion_csv(
        self, fixtures_dir, sample_config_path, temp_output_dir
    ):
        """Test batch conversion to CSV format."""
        summary = convert_batch(
            input_dir=str(fixtures_dir),
            output_dir=str(temp_output_dir),
            output_format="csv",
            config_path=str(sample_config_path),
        )

        assert summary.total_files > 0
        assert summary.successful > 0
        assert summary.output_format == "csv"

        # Verify output files were created
        output_files = list(temp_output_dir.glob("*.csv"))
        assert len(output_files) > 0


class TestErrorHandling:
    """Test error handling for malformed files."""

    def test_nonexistent_file(self, sample_config_path):
        """Test handling of non-existent file."""
        result = convert_file(
            xml_path="nonexistent.xml",
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["success"] is False
        assert result["error_message"] != ""

    def test_invalid_format(self, fixtures_dir, sample_config_path):
        """Test handling of invalid output format."""
        xml_file = fixtures_dir / "sample_invoice.xml"

        with pytest.raises(ValueError):
            convert_file(
                xml_path=str(xml_file),
                output_format="invalid",
                config_path=str(sample_config_path),
            )


class TestProcessingMetrics:
    """Test that processing metrics are captured correctly."""

    def test_processing_time_captured(self, fixtures_dir, sample_config_path):
        """Test that processing time is captured."""
        xml_file = fixtures_dir / "sample_invoice.xml"

        result = convert_file(
            xml_path=str(xml_file),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert result["processing_time_seconds"] > 0
        assert result["file_size_bytes"] > 0

    def test_batch_summary_completeness(
        self, fixtures_dir, sample_config_path, temp_output_dir
    ):
        """Test that batch summary contains all required fields."""
        summary = convert_batch(
            input_dir=str(fixtures_dir),
            output_dir=str(temp_output_dir),
            output_format="json",
            config_path=str(sample_config_path),
        )

        assert summary.start_time is not None
        assert summary.end_time is not None
        assert summary.total_files == len(summary.results)
        assert summary.successful + summary.failed == summary.total_files
