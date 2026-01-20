#!/usr/bin/env python3
"""
File Import Example

This script demonstrates importing documents from files using the Verba SDK.
"""

from goldenverba import Verba
from pathlib import Path
import tempfile
import os


def create_sample_files():
    """Create sample text files for demonstration."""
    temp_dir = Path(tempfile.mkdtemp())
    
    # Create sample markdown file
    md_file = temp_dir / "sample.md"
    md_file.write_text("""# Sample Markdown Document

This is a sample markdown file for testing Verba SDK.

## Features

- Document ingestion
- Vector search
- RAG capabilities

## Usage

You can import this file and query it using natural language.
""")

    # Create sample text file
    txt_file = temp_dir / "sample.txt"
    txt_file.write_text("""Verba SDK File Import Example

This is a plain text file that demonstrates file import functionality.
The SDK can handle various file formats including PDF, Markdown, and plain text.
""")

    return temp_dir, [md_file, txt_file]


def main():
    print("🚀 Verba SDK - File Import Example\n")

    # Initialize Verba
    print("1. Initializing Verba...")
    verba = Verba(deployment="Local")
    print("   ✓ Connected\n")

    # Create sample files
    print("2. Creating sample files...")
    temp_dir, files = create_sample_files()
    print(f"   ✓ Created {len(files)} sample files in {temp_dir}\n")

    # Import files
    print("3. Importing files...")
    imported_docs = []
    for file_path in files:
        print(f"   Importing {file_path.name}...")
        doc = verba.add_document(
            file_path=str(file_path),
            labels=["demo", "sample"],
            metadata=f"Imported from {file_path.name}",
        )
        imported_docs.append(doc)
        print(f"   ✓ Imported: {doc.title} ({doc.chunk_count} chunks)")

    print(f"\n   ✓ Total documents imported: {len(imported_docs)}\n")

    # Query imported documents
    print("4. Querying imported documents...")
    results = verba.query("What features does Verba have?", limit=5)
    print(f"   Found {len(results.chunks)} relevant chunks:\n")
    for i, chunk in enumerate(results.chunks, 1):
        print(f"   [{i}] {chunk.document_title}")
        print(f"       {chunk.content[:100]}...\n")

    # List all documents
    print("5. Listing all documents...")
    doc_list = verba.list_documents()
    print(f"   Total documents: {doc_list.total_count}\n")

    # Clean up
    print("6. Cleaning up...")
    verba.close()
    # Optionally remove temp files
    import shutil
    shutil.rmtree(temp_dir)
    print("   ✓ Connection closed and temp files removed\n")

    print("✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
