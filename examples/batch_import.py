#!/usr/bin/env python3
"""
Batch Import Example

This script demonstrates batch importing multiple documents at once.
"""

from goldenverba import Verba


def main():
    print("🚀 Verba SDK - Batch Import Example\n")

    # Initialize Verba
    print("1. Initializing Verba...")
    verba = Verba(deployment="Local")
    print("   ✓ Connected\n")

    # Prepare batch of documents
    print("2. Preparing batch of documents...")
    documents = [
        {
            "content": """
            Machine Learning is a subset of artificial intelligence that enables
            systems to learn and improve from experience without being explicitly
            programmed. It uses algorithms to analyze data and make predictions.
            """,
            "title": "Machine Learning Basics",
            "labels": ["ai", "ml", "technology"],
        },
        {
            "content": """
            Natural Language Processing (NLP) is a branch of AI that helps computers
            understand, interpret, and manipulate human language. NLP combines
            computational linguistics with machine learning and deep learning.
            """,
            "title": "Natural Language Processing",
            "labels": ["ai", "nlp", "technology"],
        },
        {
            "content": """
            Vector databases are specialized databases designed to store and query
            high-dimensional vectors efficiently. They are essential for semantic
            search, recommendation systems, and RAG applications.
            """,
            "title": "Vector Databases",
            "labels": ["database", "vectors", "search"],
        },
        {
            "content": """
            Retrieval Augmented Generation (RAG) combines information retrieval
            with language generation. It retrieves relevant context from a knowledge
            base and uses it to generate more accurate and contextual responses.
            """,
            "title": "RAG Overview",
            "labels": ["rag", "ai", "nlp"],
        },
    ]
    print(f"   ✓ Prepared {len(documents)} documents\n")

    # Batch import
    print("3. Batch importing documents...")
    imported_docs = verba.add_documents(documents)
    print(f"   ✓ Successfully imported {len(imported_docs)} documents:\n")
    for doc in imported_docs:
        print(f"   - {doc.title} ({doc.chunk_count} chunks)")

    # Query across all documents
    print("\n4. Querying across all documents...")
    results = verba.query("What is RAG and how does it work?", limit=5)
    print(f"   Found {len(results.chunks)} relevant chunks from multiple documents\n")

    # Group by document
    from collections import defaultdict
    by_document = defaultdict(list)
    for chunk in results.chunks:
        by_document[chunk.document_title].append(chunk)

    for doc_title, chunks in by_document.items():
        print(f"   From '{doc_title}':")
        for chunk in chunks[:2]:  # Show first 2 chunks per document
            print(f"     - {chunk.content[:80]}...")

    # Clean up
    print("\n5. Cleaning up...")
    verba.close()
    print("   ✓ Connection closed\n")

    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
