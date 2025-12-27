"""
PyTest configuration and shared fixtures for ublkit tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_config_path(fixtures_dir: Path) -> Path:
    """Return path to sample configuration file."""
    return fixtures_dir / "ublkit.yaml"


@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Return path to temporary output directory for tests."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir
