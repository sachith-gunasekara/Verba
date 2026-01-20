# Verba SDK Examples

This directory contains example scripts demonstrating how to use the Verba Python SDK with local Weaviate.

## Prerequisites

1. Install Verba:
   ```bash
   pip install goldenverba
   ```

2. Ensure you have the required dependencies for your chosen components (e.g., OpenAI API key if using OpenAI embedder/generator)

## Example Scripts

### 1. `basic_usage.py`
Basic example showing:
- Initializing Verba with local Weaviate
- Adding documents
- Querying documents
- Chatting with RAG
- Listing documents

**Run:**
```bash
python examples/basic_usage.py
```

### 2. `streaming_chat.py`
Demonstrates streaming chat responses:
- Adding multiple documents
- Streaming chat responses token by token
- Real-time output

**Run:**
```bash
python examples/streaming_chat.py
```

### 3. `file_import.py`
Shows how to import documents from files:
- Creating sample files
- Importing from file paths
- Querying imported documents

**Run:**
```bash
python examples/file_import.py
```

### 4. `batch_import.py`
Demonstrates batch importing multiple documents:
- Preparing multiple documents
- Batch import operation
- Querying across multiple documents

**Run:**
```bash
python examples/batch_import.py
```

### 5. `configuration_example.py`
Shows how to configure the RAG pipeline:
- Viewing available components
- Configuring pipeline components
- Per-document configuration

**Run:**
```bash
python examples/configuration_example.py
```

## Environment Variables

For components that require API keys, set them as environment variables:

```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
# etc.
```

Or create a `.env` file in the project root (see `goldenverba/.env.example`).

## Notes

- All examples use `deployment="Local"` which uses Weaviate Embedded
- Weaviate Embedded is not supported on Windows - use Docker deployment instead
- Examples create temporary data that persists in Weaviate until you reset it
- To reset data, you can use: `verba reset` CLI command

## Troubleshooting

If you encounter connection issues:
1. Ensure you have sufficient system resources (Weaviate Embedded requires memory)
2. Check that no other Weaviate instance is running on the default port
3. On Windows, use Docker deployment instead of Local
