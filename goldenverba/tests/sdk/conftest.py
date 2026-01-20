"""Pytest fixtures for SDK tests."""

import pytest
from goldenverba import Verba


@pytest.fixture
def verba_local():
    """Create a Verba instance with Local deployment."""
    verba = Verba(deployment="Local", auto_connect=False)
    yield verba
    verba.close()


@pytest.fixture
def verba_connected(verba_local):
    """Create and connect a Verba instance."""
    verba_local.connect()
    yield verba_local
    verba_local.close()
