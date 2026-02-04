#!/usr/bin/env python3
"""
Streaming Chat Example

This script demonstrates streaming chat responses with the Verba SDK using Azure OpenAI.
"""

import os
from goldenverba import Verba
import sys


def main():
    print("🚀 Verba SDK - Streaming Chat Example\n")

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
    print("Initializing Verba...")
    verba = Verba(deployment="Custom", weaviate_url="localhost", port="8080")
    print("✓ Connected to Weaviate in Docker\n")

    # Configure to use Azure OpenAI embedder
    verba.configure(
        embedder="OpenAI",
        embedder_config={
            "URL": os.getenv("OPENAI_EMBED_BASE_URL", ""),
            "Model": "text-embedding-3-small",
            "API Version": os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
        },
    )

    # Add some documents
    print("Adding documents...")
    verba.add_document(
        content="""
        Python is a high-level programming language known for its simplicity and readability.
        It supports multiple programming paradigms including procedural, object-oriented,
        and functional programming. Python has a large standard library and active community.
        """,
        title="Python Programming",
        labels=["programming", "python"],
    )

    verba.add_document(
        content="""
        FastAPI is a modern web framework for building APIs with Python. It's based on
        standard Python type hints and provides automatic API documentation. FastAPI is
        built on top of Starlette and Pydantic, making it fast and easy to use.
        """,
        title="FastAPI Framework",
        labels=["programming", "web", "api"],
    )
    print("✓ Documents added\n")

    # Stream chat response
    print("Chatting with streaming response...\n")
    print("You: What is Python and FastAPI?")
    print("Verba: ", end="", flush=True)

    for chunk in verba.chat("What is Python and FastAPI?", stream=True):
        print(chunk, end="", flush=True)
        sys.stdout.flush()

    print("\n\n✓ Streaming complete\n")

    # Clean up
    verba.close()
    print("✅ Demo completed!")


if __name__ == "__main__":
    main()
