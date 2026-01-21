#!/usr/bin/env python3
"""
Quick Start - Minimal Example with Docker Weaviate

This example connects to Weaviate running in Docker and uses Azure OpenAI for embeddings.
Make sure Weaviate is running: docker ps | grep weaviate
Set OPENAI_API_KEY and OPENAI_EMBED_BASE_URL environment variables before running.
"""

import os
from goldenverba import Verba

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

# Connect to Weaviate running in Docker on localhost:8080
# HTTP port is 8080, gRPC port is 50051 (default)
verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")

# Configure to use Azure OpenAI for embeddings and generation
# The base URL should be set via OPENAI_EMBED_BASE_URL environment variable
# Format: https://<resource-name>.openai.azure.com/openai/deployments/<deployment-name>
# API version can be set via OPENAI_API_VERSION (default: 2024-02-15-preview)
verba.configure(
    embedder="OpenAI",
    generator="OpenAI",  # Use OpenAI for chat as well
    embedder_config={
        "URL": os.getenv("OPENAI_EMBED_BASE_URL", ""),
        "Model": "text-embedding-3-small",  # Use small embedding model
        "API Version": os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
    },
)

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
