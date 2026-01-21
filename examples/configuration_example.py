#!/usr/bin/env python3
"""
Configuration Example

This script demonstrates how to configure the RAG pipeline components with Azure OpenAI.
"""

import os
from goldenverba import Verba


def main():
    print("🚀 Verba SDK - Configuration Example\n")

    # Check for Azure OpenAI configuration
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Set it with:")
        print("   export OPENAI_API_KEY='your-azure-openai-api-key'")
        print()
    if not os.getenv("OPENAI_EMBED_BASE_URL"):
        print("⚠️  Warning: OPENAI_EMBED_BASE_URL not set. Set it with:")
        print(
            "   export OPENAI_EMBED_BASE_URL='https://<resource>.openai.azure.com/openai/deployments/<deployment>'"
        )
        print()

    # Initialize Verba with Docker Weaviate
    print("1. Initializing Verba...")
    verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")
    print("   ✓ Connected to Weaviate in Docker\n")

    # Configure to use Azure OpenAI embedder
    verba.configure(
        embedder="OpenAI",
        embedder_config={
            "URL": os.getenv("OPENAI_EMBED_BASE_URL", ""),
            "Model": "text-embedding-3-small",
            "API Version": os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
        },
    )

    # Show available components
    print("2. Available components:")
    print(f"   Readers: {', '.join(verba.readers[:3])}...")
    print(f"   Chunkers: {', '.join(verba.chunkers[:3])}...")
    print(f"   Embedders: {', '.join(verba.embedders[:3])}...")
    print(f"   Retrievers: {', '.join(verba.retrievers)}")
    print(f"   Generators: {', '.join(verba.generators[:3])}...\n")

    # Show current configuration
    print("3. Current RAG configuration:")
    config = verba.config
    if config:
        selected = {
            "Reader": config.get("Reader", {}).get("selected", "N/A"),
            "Chunker": config.get("Chunker", {}).get("selected", "N/A"),
            "Embedder": config.get("Embedder", {}).get("selected", "N/A"),
            "Retriever": config.get("Retriever", {}).get("selected", "N/A"),
            "Generator": config.get("Generator", {}).get("selected", "N/A"),
        }
        for component, name in selected.items():
            print(f"   {component}: {name}")
    print()

    # Configure pipeline (example - adjust based on available components)
    print("4. Configuring RAG pipeline...")
    try:
        # Get first available components
        reader = verba.readers[0] if verba.readers else None
        chunker = verba.chunkers[0] if verba.chunkers else None
        embedder = verba.embedders[0] if verba.embedders else None
        retriever = verba.retrievers[0] if verba.retrievers else None
        generator = verba.generators[0] if verba.generators else None

        if all([reader, chunker, embedder, retriever, generator]):
            verba.configure(
                reader=reader,
                chunker=chunker,
                embedder="OpenAI",  # Use OpenAI embedder
                retriever=retriever,
                generator=generator,
                embedder_config={
                    "URL": os.getenv("OPENAI_EMBED_BASE_URL", ""),
                    "Model": "text-embedding-3-small",
                    "API Version": os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
                },
            )
            print("   ✓ Configuration updated\n")
        else:
            print("   ⚠ Some components not available, using defaults\n")
    except Exception as e:
        print(f"   ⚠ Configuration update skipped: {e}\n")

    # Add a document with custom configuration
    print("5. Adding document with custom chunker settings...")
    try:
        doc = verba.add_document(
            content="""
            This is a test document to demonstrate per-document configuration.
            You can override the default chunker settings for individual documents.
            This allows fine-grained control over how each document is processed.
            """,
            title="Configuration Test",
            labels=["demo", "config"],
            # Note: Per-document config overrides would go here
            # chunker_config={"Units": 50, "Overlap": 10}
        )
        print(f"   ✓ Document added: {doc.title}\n")
    except Exception as e:
        print(f"   ⚠ Document addition: {e}\n")

    # Query with the configured pipeline
    print("6. Testing query with configured pipeline...")
    try:
        results = verba.query("What is this document about?", limit=2)
        print(f"   Found {len(results.chunks)} chunks\n")
    except Exception as e:
        print(f"   ⚠ Query failed: {e}\n")

    # Clean up
    print("7. Cleaning up...")
    verba.close()
    print("   ✓ Connection closed\n")

    print("✅ Demo completed!")


if __name__ == "__main__":
    main()
