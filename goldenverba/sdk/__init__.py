"""Verba Python SDK - Programmatic access to Verba RAG capabilities."""

from goldenverba.sdk.client import Verba
from goldenverba.sdk.models import (
    Document,
    Chunk,
    QueryResult,
    ChatResponse,
    DocumentList,
)
from goldenverba.sdk.exceptions import (
    VerbaError,
    ConnectionError,
    DocumentNotFoundError,
    ConfigurationError,
    ImportError,
    QueryError,
    GenerationError,
)

__all__ = [
    "Verba",
    "Document",
    "Chunk",
    "QueryResult",
    "ChatResponse",
    "DocumentList",
    "VerbaError",
    "ConnectionError",
    "DocumentNotFoundError",
    "ConfigurationError",
    "ImportError",
    "QueryError",
    "GenerationError",
]
