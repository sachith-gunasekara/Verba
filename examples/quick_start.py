#!/usr/bin/env python3
"""
Quick Start - Minimal Example with Docker Weaviate

This example connects to Weaviate running in Docker.
Make sure Weaviate is running: docker ps | grep weaviate
"""

from goldenverba import Verba

# Connect to Weaviate running in Docker on localhost:8080
# If your Weaviate is on a different host/port, use Custom deployment instead
verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")

# Add a document
verba.add_document(
    content="Python is a programming language. It's easy to learn and powerful.",
    title="Python Intro"
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
