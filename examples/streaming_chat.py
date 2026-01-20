#!/usr/bin/env python3
"""
Streaming Chat Example

This script demonstrates streaming chat responses with the Verba SDK.
"""

from goldenverba import Verba
import sys


def main():
    print("🚀 Verba SDK - Streaming Chat Example\n")

    # Initialize Verba
    print("Initializing Verba...")
    verba = Verba(deployment="Local")
    print("✓ Connected\n")

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
