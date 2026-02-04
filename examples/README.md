# Verba SDK Examples

This directory contains example scripts demonstrating how to use the Verba Python SDK with Weaviate running in Docker.

## Prerequisites

### 1. Weaviate Running in Docker

Make sure you have Weaviate running in Docker. Check with:

```bash
docker ps | grep weaviate
```

If Weaviate is not running, start it:

```bash
# Option 1: Using docker-compose (if you have docker-compose.yml)
docker compose up -d weaviate

# Option 2: Run Weaviate directly
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  semitechnologies/weaviate:1.25.10 \
  --host 0.0.0.0 \
  --port 8080 \
  --scheme http \
  --env AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
```

Verify it's running:
```bash
curl http://localhost:8080/v1/.well-known/ready
```

### 2. Install Verba

```bash
pip install goldenverba
```

### 3. API Keys (Required for Embeddings/Generation)

**For OpenAI Embeddings (Recommended):**
```bash
export OPENAI_API_KEY='your-openai-api-key'
```

**For Other Providers:**
- Cohere: `export COHERE_API_KEY='your-key'`
- Anthropic: `export ANTHROPIC_API_KEY='your-key'`
- VoyageAI: `export VOYAGE_API_KEY='your-key'`

**Note:** If you don't have API keys, you can use Ollama (local) by running:
```bash
docker run -d -p 11434:11434 ollama/ollama
```

Then configure Verba to use Ollama embedder instead of OpenAI.

## Connection Details

All examples use **Custom deployment** to connect to Weaviate in Docker:

```python
verba = Verba(
    deployment="Custom",
    weaviate_url="localhost",  # Change if Weaviate is on different host
    port="8080"                # Change if Weaviate uses different port
)
```

### If Your Weaviate is on a Different Host/Port

If your Weaviate Docker container is accessible at a different address:

```python
# Different host
verba = Verba(deployment="Custom", weaviate_url="192.168.1.100", port="8080")

# Different port
verba = Verba(deployment="Custom", weaviate_url="localhost", port="8090")

# With authentication (if enabled)
verba = Verba(
    deployment="Custom",
    weaviate_url="localhost",
    port="8080",
    weaviate_key="your-api-key"
)
```

## Deployment Options Reference

1. **Custom (Examples)** - `Verba(deployment="Custom", weaviate_url="localhost", port="8080")`
   - Connect to Weaviate running in Docker or any Weaviate instance
   - **This is what all examples use**

2. **Local (Embedded)** - `Verba(deployment="Local")`
   - Runs Weaviate inside Python process (no Docker needed)
   - Not supported on Windows
   - Data stored in `~/.local/share/weaviate`

3. **Docker** - `Verba(deployment="Docker")`
   - Connects to Weaviate service named "weaviate" in Docker network
   - Only works when Verba itself is running in Docker

4. **Weaviate Cloud** - `Verba(deployment="Weaviate", weaviate_url="...", weaviate_key="...")`
   - Connect to cloud-hosted Weaviate instance

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

- All examples connect to Weaviate running in Docker on `localhost:8080`
- If your Weaviate is on a different host/port, modify the `Verba()` call in each script
- Examples create data that persists in Weaviate Docker volume
- To reset data, restart the Weaviate container or use: `verba reset` CLI command

## Troubleshooting

### Connection Issues

1. **Verify Weaviate is running:**
   ```bash
   docker ps | grep weaviate
   curl http://localhost:8080/v1/.well-known/ready
   ```

2. **Check Weaviate logs:**
   ```bash
   docker logs weaviate
   ```

3. **If Weaviate is on different host/port:**
   - Update `weaviate_url` and `port` in the `Verba()` call
   - Example: `Verba(deployment="Custom", weaviate_url="192.168.1.100", port="8080")`

4. **If authentication is enabled:**
   - Add `weaviate_key="your-api-key"` to the `Verba()` call

5. **Check firewall/network:**
   - Ensure port 8080 is accessible
   - If using Docker network, ensure proper network configuration
