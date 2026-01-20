"""SDK-specific exceptions."""


class VerbaError(Exception):
    """Base exception for Verba SDK."""

    pass


class ConnectionError(VerbaError):
    """Failed to connect to Weaviate."""

    pass


class DocumentNotFoundError(VerbaError):
    """Document not found."""

    pass


class ConfigurationError(VerbaError):
    """Invalid configuration."""

    pass


class ImportError(VerbaError):
    """Document import failed."""

    pass


class QueryError(VerbaError):
    """Query execution failed."""

    pass


class GenerationError(VerbaError):
    """LLM generation failed."""

    pass
