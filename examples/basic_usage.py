#!/usr/bin/env python3
"""
Basic Verba SDK Usage Example

This script demonstrates basic usage of the Verba SDK with local Weaviate Embedded.
It shows how to:
- Initialize Verba
- Add documents
- Query documents
- Chat with RAG
"""

from goldenverba import Verba


def main():
    print("🚀 Verba SDK - Basic Usage Example\n")

    # Initialize Verba with Weaviate running in Docker
    print("1. Initializing Verba with Docker Weaviate...")
    verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")
    print("   ✓ Connected to Weaviate in Docker\n")

    # Add a document
    print("2. Adding a document...")
    doc = verba.add_document(
        content="""
        Verba is an open-source RAG (Retrieval Augmented Generation) application.
        It provides an end-to-end interface for working with your documents using
        state-of-the-art RAG techniques. Verba combines Weaviate's vector database
        with various LLM providers like OpenAI, Anthropic, and Cohere.
        
        Key features of Verba:
        - Document ingestion from multiple sources (files, URLs, text)
        - Multiple chunking strategies (token, sentence, semantic, recursive)
        - Hybrid search combining semantic and keyword search
        - Support for various embedding models
        - Integration with multiple LLM providers
        - Streaming chat responses
        """,
        title="About Verba",
        labels=["documentation", "introduction"],
        metadata="Introduction to Verba RAG platform",
    )
    print(f"   ✓ Document added: {doc.title} (UUID: {doc.uuid[:8]}...)\n")

    # Query documents
    print("3. Querying documents...")
    results = verba.query("What is Verba?", limit=3)
    print(f"   Found {len(results.chunks)} relevant chunks:\n")
    for i, chunk in enumerate(results.chunks, 1):
        print(f"   Chunk {i} (score: {chunk.score:.3f}):")
        print(f"   {chunk.content[:150]}...\n")

    # Chat with RAG
    print("4. Chatting with RAG...")
    response = verba.chat("Explain what Verba does in simple terms")
    print(f"   Question: Explain what Verba does in simple terms")
    print(f"   Answer: {response.answer}\n")
    print(f"   Sources: {len(response.sources)} chunks used\n")

    # List documents
    print("5. Listing all documents...")
    doc_list = verba.list_documents()
    print(f"   Total documents: {doc_list.total_count}")
    for doc in doc_list.documents:
        print(f"   - {doc.title} ({doc.chunk_count} chunks)")

    # Clean up
    print("\n6. Cleaning up...")
    verba.close()
    print("   ✓ Connection closed\n")

    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
