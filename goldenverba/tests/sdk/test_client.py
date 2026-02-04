"""Tests for Verba client class."""

import pytest
from goldenverba import Verba
from goldenverba.sdk.exceptions import ConnectionError, VerbaError


def test_verba_initialization():
    """Test Verba initialization."""
    verba = Verba(deployment="Local", auto_connect=False)
    assert verba._manager is not None
    assert verba._client is None
    assert verba._credentials.deployment == "Local"
    verba.close()


def test_verba_context_manager():
    """Test Verba as context manager."""
    with Verba(deployment="Local", auto_connect=False) as verba:
        assert verba._manager is not None
    # Should be closed after context exit
    assert verba._client is None


def test_verba_properties():
    """Test Verba component properties."""
    verba = Verba(deployment="Local", auto_connect=False)
    # These should return lists even when not connected
    assert isinstance(verba.readers, list)
    assert isinstance(verba.chunkers, list)
    assert isinstance(verba.embedders, list)
    assert isinstance(verba.retrievers, list)
    assert isinstance(verba.generators, list)
    verba.close()


def test_verba_not_connected_error():
    """Test that operations fail when not connected."""
    verba = Verba(deployment="Local", auto_connect=False)

    with pytest.raises(ConnectionError):
        verba.add_document(content="test", title="Test")

    with pytest.raises(ConnectionError):
        verba.query("test")

    with pytest.raises(ConnectionError):
        verba.chat("test")

    verba.close()


def test_verba_add_document_validation():
    """Test add_document input validation."""
    verba = Verba(deployment="Local", auto_connect=False)
    verba.connect()

    # Should fail if multiple inputs provided
    with pytest.raises(ValueError):
        verba.add_document(content="test", file_path="test.txt")

    # Should fail if no inputs provided
    with pytest.raises(ValueError):
        verba.add_document()

    verba.close()


def test_verba_config_property():
    """Test config property."""
    verba = Verba(deployment="Local", auto_connect=False)
    verba.connect()

    config = verba.config
    assert isinstance(config, dict)
    assert "Reader" in config or config == {}  # May be empty if not fully initialized

    verba.close()
