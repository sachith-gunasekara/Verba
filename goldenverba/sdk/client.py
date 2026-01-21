"""Main Verba SDK client class."""

import base64
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, Iterator, Callable, Literal

from goldenverba.verba_manager import VerbaManager
from goldenverba.server.types import (
    Credentials,
    FileConfig,
    FileStatus,
    DocumentFilter,
)
from goldenverba.server.helpers import LoggerManager
from goldenverba.sdk.models import (
    Document,
    QueryResult,
    ChatResponse,
    DocumentList,
)
from goldenverba.sdk.exceptions import (
    VerbaError,
    ConnectionError,
    DocumentNotFoundError,
    ImportError,
    QueryError,
    GenerationError,
)
from goldenverba.sdk.sync import run_sync, AsyncToSyncIterator
from goldenverba.sdk.config import ConfigManager


class CallbackLogger(LoggerManager):
    """Logger that calls a callback function instead of using WebSocket."""

    def __init__(self, callback: Optional[Callable[[str, str, float], None]] = None):
        # type: ignore - LoggerManager accepts Optional[WebSocket] but type checker doesn't recognize it
        super().__init__(socket=None)  # type: ignore[arg-type]
        self.callback = callback

    async def send_report(
        self, file_Id: str, status: FileStatus, message: str, took: float
    ):
        """Send report via callback if provided."""
        await super().send_report(file_Id, status, message, took)
        if self.callback:
            try:
                self.callback(status, message, took)
            except Exception:
                pass  # Ignore callback errors


class Verba:
    """
    Main SDK client for Verba - The Golden RAGtriever.

    Example:
        >>> from goldenverba import Verba
        >>> verba = Verba()
        >>> verba.add_document(content="Hello world", title="Test")
        >>> results = verba.query("What is hello?")
    """

    def __init__(
        self,
        deployment: Literal["Weaviate", "Docker", "Local", "Custom"] = "Local",
        weaviate_url: Optional[str] = None,
        weaviate_key: Optional[str] = None,
        port: str = "8080",
        grpc_port: Optional[str] = None,
        auto_connect: bool = True,
    ):
        """
        Initialize Verba SDK.

        Args:
            deployment: Deployment type - "Local", "Weaviate", "Docker", or "Custom"
            weaviate_url: Weaviate URL (required for Weaviate/Custom deployments)
            weaviate_key: Weaviate API key (required for Weaviate/Custom deployments)
            port: HTTP port for Custom deployment (default: "8080")
            grpc_port: gRPC port for Custom deployment (default: "50051" if not specified)
            auto_connect: Automatically connect on initialization (default: True)
        """
        self._manager = VerbaManager()
        self._client = None
        self._credentials = Credentials(
            deployment=deployment,
            url=weaviate_url or "",
            key=weaviate_key or "",
        )
        self._port = port
        self._grpc_port = grpc_port
        self._rag_config = None
        self._config_manager = None

        if auto_connect:
            self.connect()

    def connect(self) -> None:
        """Explicitly connect to Weaviate and load configuration."""
        try:
            self._client = run_sync(
                self._manager.connect(self._credentials, self._port, self._grpc_port)
            )
            if not self._client:
                raise ConnectionError("Failed to connect to Weaviate")

            self._rag_config = run_sync(self._manager.load_rag_config(self._client))
            self._config_manager = ConfigManager(self._rag_config)
        except Exception as e:
            if isinstance(e, ConnectionError):
                raise
            raise ConnectionError(f"Failed to connect to Weaviate: {str(e)}")

    def close(self) -> None:
        """Close the connection to Weaviate and clean up resources."""
        if self._client:
            run_sync(self._manager.disconnect(self._client))
            self._client = None
            self._rag_config = None
            self._config_manager = None

    def __enter__(self) -> "Verba":
        """Context manager entry."""
        if not self._client:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.close()

    # Document Operations

    def add_document(
        self,
        content: Optional[str] = None,
        file_path: Optional[str] = None,
        url: Optional[str] = None,
        title: Optional[str] = None,
        labels: Optional[List[str]] = None,
        metadata: str = "",
        overwrite: bool = False,
        reader: Optional[str] = None,
        chunker: Optional[str] = None,
        embedder: Optional[str] = None,
        on_progress: Optional[Callable[[str, str, float], None]] = None,
        **config_overrides,
    ) -> Document:
        """
        Add a document to Verba.

        Args:
            content: Document content as string
            file_path: Path to file to import
            url: URL to import from
            title: Document title (auto-generated if not provided)
            labels: List of labels for filtering
            metadata: Additional metadata string
            overwrite: Overwrite if document exists
            reader: Reader component name (overrides default)
            chunker: Chunker component name (overrides default)
            embedder: Embedder component name (overrides default)
            on_progress: Optional callback for progress updates (status, message, took)
            **config_overrides: Additional config overrides (e.g., chunker_config={"Units": 100})

        Returns:
            Document object with UUID and metadata

        Raises:
            ImportError: If import fails
            ValueError: If invalid arguments provided
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        # Validate input
        input_count = sum([content is not None, file_path is not None, url is not None])
        if input_count != 1:
            raise ValueError(
                "Exactly one of 'content', 'file_path', or 'url' must be provided"
            )

        # Prepare FileConfig
        file_id = str(uuid.uuid4())

        if file_path:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            filename = title or path.name
            extension = path.suffix.lstrip(".")

            # Read and encode file
            with open(path, "rb") as f:
                file_bytes = f.read()
                encoded_content = base64.b64encode(file_bytes).decode("utf-8")

            file_size = len(file_bytes)
            is_url = False
            source = str(path.absolute())
            content_str = encoded_content

        elif url:
            filename = title or url.split("/")[-1] or "url_document"
            extension = ""
            file_size = 0
            is_url = True
            source = url
            content_str = url

        else:  # content
            if content is None:
                raise ValueError("Content cannot be None")
            filename = title or "text_document"
            extension = ""
            file_size = len(content.encode("utf-8"))
            is_url = False
            source = ""
            content_str = content

        # Get RAG config (with overrides)
        rag_config = self._get_rag_config_with_overrides(
            reader=reader,
            chunker=chunker,
            embedder=embedder,
            **config_overrides,
        )

        # Create FileConfig
        file_config = FileConfig(
            fileID=file_id,
            filename=filename,
            isURL=is_url,
            overwrite=overwrite,
            extension=extension,
            source=source,
            content=content_str,
            labels=labels or [],
            rag_config=rag_config,
            file_size=file_size,
            status=FileStatus.READY,
            metadata=metadata,
            status_report={},
        )

        # Import document
        logger = CallbackLogger(on_progress) if on_progress else LoggerManager()

        try:
            run_sync(self._manager.import_document(self._client, file_config, logger))
        except Exception as e:
            raise ImportError(f"Failed to import document: {str(e)}") from e

        # Get imported document
        try:
            doc_uuid = run_sync(
                self._manager.weaviate_manager.exist_document_name(
                    self._client, filename
                )
            )
            if not doc_uuid:
                raise DocumentNotFoundError("Document imported but UUID not found")

            doc_data = run_sync(
                self._manager.weaviate_manager.get_document(
                    self._client,
                    doc_uuid,
                    properties=[
                        "title",
                        "extension",
                        "fileSize",
                        "labels",
                        "source",
                        "meta",
                        "metadata",
                    ],
                )
            )

            if not doc_data or not isinstance(doc_data, dict):
                raise DocumentNotFoundError("Document imported but data not found")

            # Get chunk count
            # RAG config structure: rag_config["Embedder"]["components"][embedder_name]["config"]
            embedder_name = rag_config["Embedder"]["selected"]
            embedder_config = rag_config["Embedder"]["components"][embedder_name]["config"]
            embedder_model = embedder_config["Model"]["value"]
            chunk_count = run_sync(
                self._manager.weaviate_manager.get_chunk_count(
                    self._client, embedder_model, doc_uuid
                )
            )

            return Document.from_dict(doc_data, chunk_count=chunk_count)
        except Exception as e:
            raise ImportError(
                f"Document imported but failed to retrieve: {str(e)}"
            ) from e

    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        **kwargs,
    ) -> List[Document]:
        """
        Batch add multiple documents.

        Args:
            documents: List of document dicts, each with 'content', 'file_path', or 'url'
            **kwargs: Common arguments applied to all documents

        Returns:
            List of Document objects
        """
        results = []
        for doc in documents:
            # Merge document-specific args with common kwargs
            doc_kwargs = {**kwargs, **doc}
            result = self.add_document(**doc_kwargs)
            results.append(result)
        return results

    def list_documents(
        self,
        query: str = "",
        page: int = 1,
        page_size: int = 10,
        labels: Optional[List[str]] = None,
    ) -> DocumentList:
        """
        List documents with pagination.

        Args:
            query: Search query (empty for all documents)
            page: Page number (1-indexed)
            page_size: Number of documents per page
            labels: Filter by labels

        Returns:
            DocumentList with documents and pagination info
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        try:
            result = run_sync(
                self._manager.weaviate_manager.get_documents(
                    self._client,
                    query,
                    page_size,
                    page,
                    labels or [],
                    properties=[
                        "title",
                        "extension",
                        "fileSize",
                        "labels",
                        "source",
                        "meta",
                    ],
                )
            )
            documents, total_count = result
            if not isinstance(total_count, int):
                total_count = 0

            # Convert to Document objects
            doc_objects = []
            for doc in documents:
                if not isinstance(doc, dict):
                    continue
                # Get chunk count
                try:
                    meta = doc.get("meta", {})
                    if isinstance(meta, str):
                        import json

                        meta = json.loads(meta)
                    embedder_model = (
                        meta.get("Embedder", {})
                        .get("config", {})
                        .get("Model", {})
                        .get("value", "")
                    )
                    if embedder_model:
                        chunk_count = run_sync(
                            self._manager.weaviate_manager.get_chunk_count(
                                self._client, embedder_model, doc["uuid"]
                            )
                        )
                    else:
                        chunk_count = 0
                except Exception:
                    chunk_count = 0

                doc_obj = Document(
                    uuid=doc["uuid"],
                    title=doc["title"],
                    content="",  # Not included in list view
                    extension=doc.get("extension", ""),
                    labels=doc.get("labels", []),
                    source=doc.get("source", ""),
                    file_size=doc.get("fileSize", 0),
                    chunk_count=chunk_count,
                    metadata="",
                )
                doc_objects.append(doc_obj)

            return DocumentList(
                documents=doc_objects,
                total_count=total_count,
                page=page,
                page_size=page_size,
            )
        except Exception as e:
            raise QueryError(f"Failed to list documents: {str(e)}") from e

    def get_document(self, uuid: str) -> Document:
        """
        Get document by UUID.

        Args:
            uuid: Document UUID

        Returns:
            Document object

        Raises:
            DocumentNotFoundError: If document not found
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        try:
            doc_data = run_sync(
                self._manager.weaviate_manager.get_document(
                    self._client,
                    uuid,
                    properties=[
                        "title",
                        "extension",
                        "fileSize",
                        "labels",
                        "source",
                        "meta",
                        "metadata",
                    ],
                )
            )

            if not doc_data or not isinstance(doc_data, dict):
                raise DocumentNotFoundError(f"Document with UUID '{uuid}' not found")

            # Get chunk count
            try:
                meta = doc_data.get("meta", {})
                if isinstance(meta, str):
                    import json

                    meta = json.loads(meta)
                embedder_model = (
                    meta.get("Embedder", {})
                    .get("config", {})
                    .get("Model", {})
                    .get("value", "")
                )
                if embedder_model:
                    chunk_count = run_sync(
                        self._manager.weaviate_manager.get_chunk_count(
                            self._client, embedder_model, uuid
                        )
                    )
                else:
                    chunk_count = 0
            except Exception:
                chunk_count = 0

            return Document.from_dict(doc_data, chunk_count=chunk_count)
        except DocumentNotFoundError:
            raise
        except Exception as e:
            raise DocumentNotFoundError(f"Failed to get document: {str(e)}") from e

    def delete_document(self, uuid: str) -> bool:
        """
        Delete document by UUID.

        Args:
            uuid: Document UUID

        Returns:
            True if deleted successfully
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        try:
            run_sync(self._manager.weaviate_manager.delete_document(self._client, uuid))
            return True
        except Exception as e:
            raise VerbaError(f"Failed to delete document: {str(e)}") from e

    # Query Operations

    def query(
        self,
        query: str,
        limit: int = 5,
        labels: Optional[List[str]] = None,
        document_ids: Optional[List[str]] = None,
        retriever: Optional[str] = None,
        embedder: Optional[str] = None,
    ) -> QueryResult:
        """
        Query documents and retrieve relevant chunks.

        Args:
            query: Search query
            limit: Maximum number of results
            labels: Filter by labels
            document_ids: Filter by document UUIDs
            retriever: Retriever component name (overrides default)
            embedder: Embedder component name (overrides default)

        Returns:
            QueryResult with chunks and context
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        # Get RAG config with overrides
        rag_config = self._get_rag_config_with_overrides(
            retriever=retriever, embedder=embedder
        )

        try:
            # Convert document_ids to DocumentFilter format
            document_filters = []
            if document_ids:
                for doc_id in document_ids:
                    # Get document title for filter
                    try:
                        doc = run_sync(
                            self._manager.weaviate_manager.get_document(
                                self._client, doc_id, properties=["title"]
                            )
                        )
                        title = (
                            doc.get("title", "")
                            if doc and isinstance(doc, dict)
                            else ""
                        )
                    except Exception:
                        title = ""
                    document_filters.append(DocumentFilter(uuid=doc_id, title=title))

            documents, context = run_sync(
                self._manager.retrieve_chunks(
                    self._client,
                    query,
                    rag_config,
                    labels or [],
                    document_ids or [],
                )
            )

            # Flatten documents structure: documents is list[dict] where each dict has "chunks" list
            # We need to extract all chunks and add document metadata
            flattened_chunks = []
            for doc in documents:
                if isinstance(doc, dict) and "chunks" in doc:
                    for chunk in doc["chunks"]:
                        # Add document metadata to chunk
                        chunk_with_doc = chunk.copy()
                        chunk_with_doc["doc_uuid"] = doc.get("uuid", "")
                        chunk_with_doc["title"] = doc.get("title", "")
                        # Get content if available
                        if "content" not in chunk_with_doc:
                            # Try to get from context_chunks or fetch it
                            chunk_with_doc["content"] = ""
                        flattened_chunks.append(chunk_with_doc)
                else:
                    # If it's already a flat chunk dict, use it as-is
                    flattened_chunks.append(doc)

            return QueryResult.from_retrieval(query, flattened_chunks, context)
        except Exception as e:
            raise QueryError(f"Query failed: {str(e)}") from e

    # Chat Operations

    def chat(
        self,
        message: str,
        conversation: Optional[List[Dict[str, str]]] = None,
        stream: bool = False,
        labels: Optional[List[str]] = None,
        document_ids: Optional[List[str]] = None,
        generator: Optional[str] = None,
        retriever: Optional[str] = None,
        embedder: Optional[str] = None,
    ) -> ChatResponse | Iterator[str]:
        """
        Chat with RAG - retrieves context and generates response.

        Args:
            message: User message
            conversation: Previous conversation messages [{"type": "user|assistant", "content": "..."}]
            stream: Return streaming iterator instead of complete response
            labels: Filter by labels
            document_ids: Filter by document UUIDs
            generator: Generator component name (overrides default)
            retriever: Retriever component name (overrides default)
            embedder: Embedder component name (overrides default)

        Returns:
            ChatResponse if stream=False, Iterator[str] if stream=True
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        # Get RAG config with overrides
        rag_config = self._get_rag_config_with_overrides(
            generator=generator, retriever=retriever, embedder=embedder
        )

        try:
            # First, retrieve relevant chunks
            query_result = self.query(
                message,
                limit=5,  # Default limit for chat
                labels=labels,
                document_ids=document_ids,
                retriever=retriever,
                embedder=embedder,
            )

            # Convert conversation format to list[dict] for generate_stream_answer
            conversation_dicts: List[Dict[str, str]] = []
            if conversation:
                for msg in conversation:
                    conversation_dicts.append(
                        {
                            "type": msg.get("type", "user"),
                            "content": msg.get("content", ""),
                        }
                    )

            if stream:
                return self._chat_stream(
                    message, query_result.context, conversation_dicts, rag_config
                )
            else:
                # Generate complete response
                full_answer = ""
                async_gen = self._manager.generate_stream_answer(
                    rag_config,
                    message,
                    query_result.context,
                    conversation_dicts,
                )

                # Collect all chunks
                async def collect():
                    nonlocal full_answer
                    async for chunk in async_gen:
                        full_answer += chunk["message"]
                    return full_answer

                full_answer = run_sync(collect())

                return ChatResponse.from_query_result(
                    message, query_result, full_answer
                )
        except Exception as e:
            raise GenerationError(f"Chat failed: {str(e)}") from e

    def _chat_stream(
        self,
        message: str,
        context: str,
        conversation: List[Dict[str, str]],
        rag_config: Dict[str, Any],
    ) -> Iterator[str]:
        """Internal method for streaming chat responses."""

        async def async_stream():
            async for chunk in self._manager.generate_stream_answer(
                rag_config, message, context, conversation
            ):
                yield chunk["message"]

        # type: ignore - AsyncToSyncIterator implements Iterator protocol but type checker doesn't recognize it
        return AsyncToSyncIterator(async_stream())  # type: ignore[return-value]

    # Configuration

    def configure(
        self,
        reader: Optional[str] = None,
        chunker: Optional[str] = None,
        embedder: Optional[str] = None,
        retriever: Optional[str] = None,
        generator: Optional[str] = None,
        **component_configs,
    ) -> None:
        """
        Configure the RAG pipeline.

        Args:
            reader: Reader component name
            chunker: Chunker component name
            embedder: Embedder component name
            retriever: Retriever component name
            generator: Generator component name
            **component_configs: Config overrides like chunker_config={"Units": 100}
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        if not self._config_manager:
            if not self._rag_config:
                raise ConnectionError("Not connected. Call connect() first.")
            self._config_manager = ConfigManager(self._rag_config)

        # Update components
        if reader and self._config_manager:
            self._config_manager.update_component("Reader", reader)
        if chunker and self._config_manager:
            chunker_config = component_configs.get("chunker_config", {})
            self._config_manager.update_component("Chunker", chunker, chunker_config)
        if embedder and self._config_manager:
            embedder_config = component_configs.get("embedder_config", {})
            self._config_manager.update_component("Embedder", embedder, embedder_config)
        if retriever and self._config_manager:
            self._config_manager.update_component("Retriever", retriever)
        if generator and self._config_manager:
            generator_config = component_configs.get("generator_config", {})
            self._config_manager.update_component(
                "Generator", generator, generator_config
            )

        # Save updated config
        if not self._config_manager:
            raise ConnectionError("Configuration manager not initialized")
        updated_config = self._config_manager.get_rag_config()
        run_sync(self._manager.set_rag_config(self._client, updated_config))
        self._rag_config = updated_config

    @property
    def readers(self) -> List[str]:
        """Available readers."""
        return list(self._manager.reader_manager.readers.keys())

    @property
    def chunkers(self) -> List[str]:
        """Available chunkers."""
        return list(self._manager.chunker_manager.chunkers.keys())

    @property
    def embedders(self) -> List[str]:
        """Available embedders."""
        return list(self._manager.embedder_manager.embedders.keys())

    @property
    def retrievers(self) -> List[str]:
        """Available retrievers."""
        return list(self._manager.retriever_manager.retrievers.keys())

    @property
    def generators(self) -> List[str]:
        """Available generators."""
        return list(self._manager.generator_manager.generators.keys())

    @property
    def config(self) -> Dict[str, Any]:
        """Current RAG configuration."""
        if not self._rag_config:
            return {}
        return (
            self._config_manager.get_rag_config()
            if self._config_manager
            else self._rag_config
        )

    # Helper methods

    def _get_rag_config_with_overrides(
        self,
        reader: Optional[str] = None,
        chunker: Optional[str] = None,
        embedder: Optional[str] = None,
        retriever: Optional[str] = None,
        generator: Optional[str] = None,
        **config_overrides,
    ) -> Dict[str, Any]:
        """Get RAG config with temporary overrides (doesn't save to DB)."""
        if not self._rag_config:
            raise ConnectionError("Not connected. Call connect() first.")

        # Deep copy to avoid modifying original
        import copy

        rag_config = copy.deepcopy(self._rag_config)

        # Apply component overrides
        if reader and reader in rag_config["Reader"]["components"]:
            rag_config["Reader"]["selected"] = reader
        if chunker and chunker in rag_config["Chunker"]["components"]:
            rag_config["Chunker"]["selected"] = chunker
            # Apply chunker config overrides
            if "chunker_config" in config_overrides:
                chunker_comp = rag_config["Chunker"]["components"][chunker]
                for key, value in config_overrides["chunker_config"].items():
                    if key in chunker_comp["config"]:
                        chunker_comp["config"][key]["value"] = value
        if embedder and embedder in rag_config["Embedder"]["components"]:
            rag_config["Embedder"]["selected"] = embedder
            # Apply embedder config overrides
            if "embedder_config" in config_overrides:
                embedder_comp = rag_config["Embedder"]["components"][embedder]
                for key, value in config_overrides["embedder_config"].items():
                    if key in embedder_comp["config"]:
                        embedder_comp["config"][key]["value"] = value
        if retriever and retriever in rag_config["Retriever"]["components"]:
            rag_config["Retriever"]["selected"] = retriever
        if generator and generator in rag_config["Generator"]["components"]:
            rag_config["Generator"]["selected"] = generator
            # Apply generator config overrides
            if "generator_config" in config_overrides:
                generator_comp = rag_config["Generator"]["components"][generator]
                for key, value in config_overrides["generator_config"].items():
                    if key in generator_comp["config"]:
                        generator_comp["config"][key]["value"] = value

        return rag_config
