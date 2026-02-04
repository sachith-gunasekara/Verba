"""Tests for SDK models."""

from goldenverba.sdk.models import (
    Document,
    Chunk,
    QueryResult,
    ChatResponse,
    DocumentList,
)


def test_document_from_dict():
    """Test Document creation from dictionary."""
    data = {
        "uuid": "test-uuid",
        "title": "Test Document",
        "content": "Test content",
        "extension": "txt",
        "labels": ["test"],
        "source": "test_source",
        "fileSize": 100,
        "metadata": "test metadata",
    }
    doc = Document.from_dict(data, chunk_count=5)
    assert doc.uuid == "test-uuid"
    assert doc.title == "Test Document"
    assert doc.chunk_count == 5


def test_chunk_from_dict():
    """Test Chunk creation from dictionary."""
    data = {
        "uuid": "chunk-uuid",
        "content": "Chunk content",
        "chunk_id": 1,
        "doc_uuid": "doc-uuid",
        "title": "Document Title",
    }
    chunk = Chunk.from_dict(data, score=0.95)
    assert chunk.uuid == "chunk-uuid"
    assert chunk.score == 0.95
    assert chunk.document_uuid == "doc-uuid"


def test_query_result_from_retrieval():
    """Test QueryResult creation from retrieval."""
    documents = [
        {
            "uuid": "chunk-1",
            "content": "Content 1",
            "chunk_id": 1,
            "doc_uuid": "doc-1",
            "title": "Doc 1",
            "score": 0.9,
        },
        {
            "uuid": "chunk-2",
            "content": "Content 2",
            "chunk_id": 2,
            "doc_uuid": "doc-2",
            "title": "Doc 2",
            "score": 0.8,
        },
    ]
    result = QueryResult.from_retrieval("test query", documents, "Context")
    assert result.query == "test query"
    assert len(result.chunks) == 2
    assert result.context == "Context"
    assert result.total_results == 2


def test_chat_response_from_query_result():
    """Test ChatResponse creation from QueryResult."""
    query_result = QueryResult(
        query="test",
        chunks=[],
        context="Context",
        total_results=0,
    )
    response = ChatResponse.from_query_result("test", query_result, "Answer")
    assert response.answer == "Answer"
    assert response.query == "test"
    assert response.context == "Context"


def test_document_list():
    """Test DocumentList creation."""
    docs = [
        Document(
            uuid="1",
            title="Doc 1",
            content="",
            extension="txt",
            labels=[],
            source="",
            file_size=100,
            chunk_count=5,
            metadata="",
        )
    ]
    doc_list = DocumentList(documents=docs, total_count=1, page=1, page_size=10)
    assert len(doc_list.documents) == 1
    assert doc_list.total_count == 1
