#!/usr/bin/env python3
"""
Quick Start - Minimal Example

This is the simplest possible example showing that you DON'T need to start
a separate Weaviate server. Weaviate Embedded runs automatically!
"""

from goldenverba import Verba

# That's it! No server setup needed.
# Weaviate Embedded starts automatically when you create Verba()
verba = Verba(deployment="Local")

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

print("\n✅ Done! No Weaviate server was needed - it ran embedded in Python.")
