"""
Unit tests for configuration loading and validation.
"""

import pytest
from pathlib import Path

from ublkit.config import UBLKitConfig


def test_load_valid_config(sample_config_path):
    """Test loading a valid configuration file."""
    config = UBLKitConfig.from_yaml(str(sample_config_path))

    assert config is not None
    assert config.logging.level == "DEBUG"
    assert config.processing.max_workers == 2
    assert config.csv.preservation_method == "apostrophe"


def test_load_nonexistent_config():
    """Test loading a non-existent configuration file."""
    with pytest.raises(FileNotFoundError):
        UBLKitConfig.from_yaml("nonexistent.yaml")


def test_config_validation_invalid_workers():
    """Test configuration validation with invalid max_workers."""
    # This test would require creating a temporary invalid config
    # For now, it's a placeholder showing test structure
    pass


def test_config_to_dict(sample_config_path):
    """Test converting config to dictionary."""
    config = UBLKitConfig.from_yaml(str(sample_config_path))
    config_dict = config.to_dict()

    assert isinstance(config_dict, dict)
    assert "logging" in config_dict
    assert "processing" in config_dict
    assert "csv" in config_dict
    assert config_dict["csv"]["preservation_method"] == "apostrophe"
