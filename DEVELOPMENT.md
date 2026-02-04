# Development Setup Guide

This guide will help you set up the Verba project for local development.

## Prerequisites

- **Python**: >= 3.10.0 and < 3.13.0 (check with `python3 --version`)
- **pip**: Python package manager (comes with Python 3.4+)
- **Git**: For cloning and version control
- **Docker** (optional): If you want to run Weaviate in Docker

## Step 1: Clone the Repository

If you haven't already cloned the repository:

```bash
git clone https://github.com/weaviate/Verba.git
cd Verba
```

## Step 2: Create a Virtual Environment

It's highly recommended to use a virtual environment to avoid conflicts with other projects:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

## Step 3: Install Dependencies

### Install in Editable Mode with Dev Dependencies

Install the package in editable mode (so changes to code are immediately reflected) along with development dependencies:

```bash
pip install -e ".[dev]"
```

This will install:
- All production dependencies from `setup.py`
- Development tools: `pytest`, `wheel`, `twine`, `black`, `setuptools`

### Optional: Install Additional Extras

If you need Google Vertex AI support:

```bash
pip install -e ".[dev,google]"
```

If you need HuggingFace support:

```bash
pip install -e ".[dev,huggingface]"
```

Or install all extras:

```bash
pip install -e ".[dev,google,huggingface]"
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the project root for API keys and configuration:

```bash
# Copy example if available, or create new
touch .env
```

Add your API keys to `.env` (as needed):

```env
# Weaviate (if using cloud)
WEAVIATE_URL_VERBA=https://your-cluster.weaviate.network
WEAVIATE_API_KEY=your-api-key

# OpenAI
OPENAI_API_KEY=your-openai-key

# Anthropic
ANTHROPIC_API_KEY=your-anthropic-key

# Cohere
COHERE_API_KEY=your-cohere-key

# Ollama (if using local Ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
OLLAMA_EMBED_MODEL=nomic-embed-text

# Unstructured (for document processing)
UNSTRUCTURED_API_KEY=your-unstructured-key
UNSTRUCTURED_API_URL=https://api.unstructured.io

# AssemblyAI (for audio transcription)
ASSEMBLYAI_API_KEY=your-assemblyai-key

# GitHub (for importing from GitHub)
GITHUB_TOKEN=your-github-token
```

> **Note**: Not all API keys are required. Only add the ones you need for your development work.

## Step 5: Set Up Weaviate

You have several options for Weaviate:

### Option A: Docker (Recommended for Development)

```bash
# Start Weaviate in Docker
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -p 50051:50051 \
  semitechnologies/weaviate:1.25.10 \
  --host 0.0.0.0 \
  --port 8080 \
  --scheme http \
  --env AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true

# Verify it's running
curl http://localhost:8080/v1/.well-known/ready
```

### Option B: Weaviate Embedded (Local)

Weaviate Embedded runs automatically when using `deployment="Local"` in the SDK. No separate setup needed, but not supported on Windows.

### Option C: Weaviate Cloud

Use your Weaviate Cloud instance URL and API key in the `.env` file.

## Step 6: Verify Installation

Test that everything is installed correctly:

```bash
# Check Verba CLI is available
verba --help

# Run tests (if you have Weaviate running)
pytest goldenverba/tests

# Try running an example
python examples/quick_start.py
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest goldenverba/tests

# Run specific test file
pytest goldenverba/tests/sdk/test_client.py

# Run with verbose output
pytest -v goldenverba/tests

# Run with coverage
pytest --cov=goldenverba goldenverba/tests
```

### Code Formatting

Format your code with Black before committing:

```bash
# Format all Python files
black goldenverba/

# Check formatting without making changes
black --check goldenverba/

# Format specific file
black goldenverba/sdk/client.py
```

### Type Checking (Optional)

The project uses type hints. You can check types with mypy (if installed):

```bash
pip install mypy
mypy goldenverba/
```

### Running the Development Server

Start the FastAPI server for UI development:

```bash
verba start

# Or with custom host/port
verba start --host 0.0.0.0 --port 8000
```

Then visit `http://localhost:8000` in your browser.

### SDK Development

When developing the SDK, test your changes:

```bash
# Test SDK examples
python examples/basic_usage.py
python examples/streaming_chat.py
python examples/file_import.py
```

## Project Structure

```
Verba/
├── goldenverba/          # Main package
│   ├── sdk/             # Python SDK
│   ├── components/      # RAG components
│   ├── server/          # FastAPI server
│   └── tests/           # Test suite
├── examples/            # SDK usage examples
├── frontend/            # React frontend
├── setup.py            # Package configuration
└── README.md           # Project documentation
```

## Common Development Tasks

### Adding a New Dependency

1. Add to `install_requires` in `setup.py` for production dependencies
2. Add to `extras_require["dev"]` in `setup.py` for dev-only dependencies
3. Reinstall: `pip install -e ".[dev]"`

### Running SDK Examples

All examples in `examples/` connect to Docker Weaviate by default:

```bash
# Make sure Weaviate is running
docker ps | grep weaviate

# Run examples
python examples/quick_start.py
python examples/basic_usage.py
```

### Debugging

- Use `print()` statements or Python debugger (`pdb`)
- Check logs in the terminal when running `verba start`
- For SDK issues, add debug prints in `goldenverba/sdk/client.py`

## Troubleshooting

### Import Errors

If you get import errors after installing:

```bash
# Reinstall in editable mode
pip install -e ".[dev]" --force-reinstall
```

### Weaviate Connection Issues

```bash
# Check if Weaviate is running
docker ps | grep weaviate
curl http://localhost:8080/v1/.well-known/ready

# Check Weaviate logs
docker logs weaviate
```

### Virtual Environment Issues

If you're having issues with the virtual environment:

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv

# Create fresh environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
verba start --port 8001
```

## Next Steps

- Read [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check [TECHNICAL.md](TECHNICAL.md) for technical documentation
- Review [README.md](README.md) for project overview
- Explore `examples/` directory for SDK usage examples

## Getting Help

- Check existing [GitHub Issues](https://github.com/weaviate/Verba/issues)
- Ask questions in [GitHub Discussions](https://github.com/weaviate/Verba/discussions)
- Visit [Weaviate Support Page](https://forum.weaviate.io/)

Happy coding! 🚀
