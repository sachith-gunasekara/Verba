# Verba SDK Examples

This directory contains example scripts demonstrating how to use the Verba Python SDK with local Weaviate.

## How Weaviate Works with the SDK

### No Separate Server Needed for Local Deployment! 🎉

When you use `deployment="Local"` in the SDK, Verba uses **Weaviate Embedded**, which means:

- ✅ **No separate Weaviate server to start** - it runs inside your Python process
- ✅ **Automatic setup** - Verba handles everything when you call `Verba()`
- ✅ **Data persists** - stored in `~/.local/share/weaviate` on your machine
- ⚠️ **Not supported on Windows** - use Docker deployment instead

### Deployment Options

1. **Local (Embedded)** - `Verba(deployment="Local")`
   - Runs Weaviate inside Python process
   - No setup required
   - Best for development and testing
   - **This is what all examples use**

2. **Docker** - `Verba(deployment="Docker")`
   - Requires Weaviate running in Docker
   - Use if you already have docker-compose setup
   - Works on all platforms including Windows

3. **Weaviate Cloud** - `Verba(deployment="Weaviate", weaviate_url="...", weaviate_key="...")`
   - Connect to cloud-hosted Weaviate instance
   - Requires Weaviate Cloud account

4. **Custom** - `Verba(deployment="Custom", weaviate_url="...", port="8080")`
   - Connect to your own Weaviate server
   - Requires separate Weaviate instance running

## Prerequisites

1. Install Verba:
   ```bash
   pip install goldenverba
   ```

2. Ensure you have the required dependencies for your chosen components (e.g., OpenAI API key if using OpenAI embedder/generator)

3. **For Local deployment (examples)**: Nothing else needed! Just run the scripts.

## Example Scripts

### 0. `quick_start.py` ⚡
**Start here!** Minimal example showing that no Weaviate server is needed:
- Shows Weaviate Embedded running automatically
- Simplest possible usage
- Perfect for understanding how it works

**Run:**
```bash
python examples/quick_start.py
```

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
