from setuptools import find_packages, setup

# =============================================================================
# Dependency Groups
# =============================================================================

# Core SDK dependencies - minimal set for programmatic usage
# These are always installed
CORE_DEPS = [
    "weaviate-client==4.9.6",
    "python-dotenv==1.0.0",
    "wasabi==1.1.2",
    "asyncio==3.4.3",
    "tiktoken==0.6.0",
    "requests==2.31.0",
    "aiohttp==3.9.5",
    "numpy<2.0",  # Pin numpy < 2.0 for spacy 3.7.5 compatibility
    "scikit-learn==1.5.1",  # For PCA on embeddings
]

# Document processing dependencies
DOCUMENT_DEPS = [
    "openpyxl==3.1.5",  # Excel files
    "xlrd==2.0.2",  # Excel files
    "pypdf==4.3.1",  # PDF files
    "python-docx==1.1.2",  # Word docs
    "markdownify==0.13.1",  # Markdown conversion
    "aiofiles==24.1.0",  # Async file operations
    "beautifulsoup4==4.12.3",  # HTML parsing
    "langdetect==1.0.9",  # Language detection
]

# Chunking dependencies (spacy, langchain)
CHUNKING_DEPS = [
    "langchain-text-splitters==0.2.2",
    "spacy==3.7.5",
]

# Web server dependencies (FastAPI, CLI, etc.)
SERVER_DEPS = [
    "fastapi==0.111.1",
    "uvicorn[standard]==0.29.0",
    "gunicorn==22.0.0",
    "click==8.1.7",
]

# Audio transcription via AssemblyAI
ASSEMBLYAI_DEPS = [
    "assemblyai==0.33.0",
]

# All non-core dependencies combined
ALL_EXTRAS = DOCUMENT_DEPS + CHUNKING_DEPS + SERVER_DEPS + ASSEMBLYAI_DEPS

# =============================================================================
# Setup Configuration
# =============================================================================

setup(
    name="goldenverba",
    version="2.1.3",
    packages=find_packages(),
    python_requires=">=3.10.0,<3.13.0",
    entry_points={
        "console_scripts": [
            "verba=goldenverba.server.cli:cli",
        ],
    },
    author="Weaviate",
    author_email="edward@weaviate.io",
    description="Welcome to Verba: The Golden RAGtriever, an open-source initiative designed to offer a streamlined, user-friendly interface for Retrieval-Augmented Generation (RAG) applications. In just a few easy steps, dive into your data and make meaningful interactions!",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/weaviate/Verba",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    include_package_data=True,
    # Base install = Core SDK only (lightweight)
    # Use extras for additional features
    install_requires=CORE_DEPS,
    extras_require={
        # SDK with document processing (PDF, Word, Excel, etc.)
        "documents": DOCUMENT_DEPS,
        # Advanced chunking (spacy, langchain)
        "chunking": CHUNKING_DEPS,
        # Web server (FastAPI, uvicorn, gunicorn, CLI)
        "server": SERVER_DEPS,
        # Audio transcription via AssemblyAI
        "assemblyai": ASSEMBLYAI_DEPS,
        # Full installation - everything included
        # This is recommended for the web UI experience
        "full": ALL_EXTRAS,
        # Alias for full (backward compatibility)
        "all": ALL_EXTRAS,
        # Development dependencies
        "dev": ["pytest", "wheel", "twine", "black>=23.7.0", "setuptools"],
        # Google Cloud / Vertex AI
        "google": ["vertexai==1.46.0"],
        # HuggingFace embedding models
        "huggingface": ["sentence-transformers==3.0.1"],
    },
)
