"""Shared test fixtures for cluefin-xbrl tests."""

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def sample_xbrl_path():
    return FIXTURES_DIR / "sample.xbrl"


@pytest.fixture
def sample_xbrl_dir():
    return FIXTURES_DIR
