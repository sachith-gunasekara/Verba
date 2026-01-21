#!/usr/bin/env python3
"""
Quick Start - Minimal Example with Docker Weaviate

This example connects to Weaviate running in Docker and uses OpenAI for embeddings.
Make sure Weaviate is running: docker ps | grep weaviate
Set OPENAI_API_KEY environment variable before running.
"""

import os
from goldenverba import Verba

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Warning: OPENAI_API_KEY not set. Set it with:")
    print("   export OPENAI_API_KEY='your-api-key'")
    print()

# Connect to Weaviate running in Docker on localhost:8080
# HTTP port is 8080, gRPC port is 50051 (default)
verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")

# Configure to use OpenAI embedder (instead of default Ollama)
verba.configure(embedder="OpenAI")

# Add a document
verba.add_document(
    content="Python is a programming language. It's easy to learn and powerful.",
    title="Python Intro",
)

# Query it
results = verba.query("What is Python?")
print(f"Found {len(results.chunks)} chunks")
print(f"First result: {results.chunks[0].content[:100]}...")

# Chat with it
response = verba.chat("Tell me about Python")
print(f"\nChat response: {response.answer}")

# Clean up
verba.close()

print("\n✅ Done! Connected to Weaviate running in Docker.")
