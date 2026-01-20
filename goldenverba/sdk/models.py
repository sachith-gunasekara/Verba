"""Response models for Verba SDK."""

from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    """Represents a document in Verba."""

    uuid: str
    title: str
    content: str
    extension: str
    labels: List[str]
    source: str
    file_size: int
    chunk_count: int
    metadata: str

    @classmethod
    def from_dict(cls, data: dict, chunk_count: int = 0) -> "Document":
        """Create Document from dictionary (from Weaviate response)."""
        return cls(
            uuid=data.get("uuid", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            extension=data.get("extension", ""),
            labels=data.get("labels", []),
            source=data.get("source", ""),
            file_size=data.get("fileSize", 0),
            chunk_count=chunk_count,
            metadata=data.get("metadata", ""),
        )


@dataclass
class Chunk:
    """Represents a chunk from a document."""

    uuid: str
    content: str
    chunk_id: int
    score: float
    document_uuid: str
    document_title: str

    @classmethod
    def from_dict(cls, data: dict, score: float = 0.0) -> "Chunk":
        """Create Chunk from dictionary."""
        return cls(
            uuid=data.get("uuid", ""),
            content=data.get("content", ""),
            chunk_id=data.get("chunk_id", 0),
            score=score,
            document_uuid=data.get("doc_uuid", ""),
            document_title=data.get("title", ""),
        )


@dataclass
class QueryResult:
    """Result from a query operation."""

    query: str
    chunks: List[Chunk]
    context: str  # Concatenated context for generation
    total_results: int

    @classmethod
    def from_retrieval(
        cls, query: str, documents: List[dict], context: str
    ) -> "QueryResult":
        """Create QueryResult from retrieval response."""
        chunks = []
        for doc in documents:
            chunk = Chunk.from_dict(doc, score=doc.get("score", 0.0))
            chunks.append(chunk)

        return cls(
            query=query,
            chunks=chunks,
            context=context,
            total_results=len(chunks),
        )


@dataclass
class ChatResponse:
    """Response from a chat operation."""

    answer: str
    query: str
    sources: List[Chunk]
    context: str

    @classmethod
    def from_query_result(
        cls, query: str, query_result: QueryResult, answer: str
    ) -> "ChatResponse":
        """Create ChatResponse from QueryResult and generated answer."""
        return cls(
            answer=answer,
            query=query,
            sources=query_result.chunks,
            context=query_result.context,
        )


@dataclass
class DocumentList:
    """Paginated list of documents."""

    documents: List[Document]
    total_count: int
    page: int
    page_size: int
