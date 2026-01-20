"""Tests for SDK exceptions."""

from goldenverba.sdk.exceptions import (
    VerbaError,
    ConnectionError,
    DocumentNotFoundError,
    ConfigurationError,
    ImportError,
    QueryError,
    GenerationError,
)


def test_exception_hierarchy():
    """Test that all exceptions inherit from VerbaError."""
    assert issubclass(ConnectionError, VerbaError)
    assert issubclass(DocumentNotFoundError, VerbaError)
    assert issubclass(ConfigurationError, VerbaError)
    assert issubclass(ImportError, VerbaError)
    assert issubclass(QueryError, VerbaError)
    assert issubclass(GenerationError, VerbaError)


def test_exception_creation():
    """Test exception creation with messages."""
    error = ConnectionError("Test error")
    assert str(error) == "Test error"

    error = DocumentNotFoundError("Document not found")
    assert str(error) == "Document not found"
