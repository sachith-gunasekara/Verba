"""Dependency checking for SDK optional features."""

import importlib
from typing import Dict, List, Tuple
from wasabi import msg


def check_dependency(module_name: str) -> bool:
    """Check if a module is available."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


# Map of features to their required dependencies
FEATURE_DEPENDENCIES: Dict[str, List[Tuple[str, str]]] = {
    "pdf_import": [("pypdf", "pypdf")],
    "word_import": [("docx", "python-docx")],
    "excel_import": [("openpyxl", "openpyxl"), ("xlrd", "xlrd")],
    "sentence_chunking": [("spacy", "spacy")],
    "semantic_chunking": [("spacy", "spacy")],
    "recursive_chunking": [("langchain_text_splitters", "langchain-text-splitters")],
    "html_chunking": [("langchain_text_splitters", "langchain-text-splitters")],
    "markdown_chunking": [("langchain_text_splitters", "langchain-text-splitters")],
    "audio_import": [("assemblyai", "assemblyai")],
    "huggingface_embeddings": [("sentence_transformers", "sentence-transformers")],
    "web_server": [("fastapi", "fastapi"), ("uvicorn", "uvicorn")],
}


def check_feature(feature: str) -> Tuple[bool, List[str]]:
    """
    Check if a feature's dependencies are available.
    
    Returns:
        Tuple of (is_available, list_of_missing_packages)
    """
    if feature not in FEATURE_DEPENDENCIES:
        return True, []
    
    missing = []
    for module_name, package_name in FEATURE_DEPENDENCIES[feature]:
        if not check_dependency(module_name):
            missing.append(package_name)
    
    return len(missing) == 0, missing


def get_available_features() -> Dict[str, bool]:
    """Get a dictionary of features and their availability."""
    return {feature: check_feature(feature)[0] for feature in FEATURE_DEPENDENCIES}


def warn_missing_dependencies(verbose: bool = False) -> None:
    """Print warnings for missing optional dependencies."""
    if not verbose:
        return
        
    for feature, deps in FEATURE_DEPENDENCIES.items():
        available, missing = check_feature(feature)
        if not available:
            msg.warn(
                f"Feature '{feature}' unavailable. Install: pip install {' '.join(missing)}"
            )


def require_feature(feature: str, action: str = "use this feature") -> None:
    """
    Raise an error if a feature's dependencies are not available.
    
    Args:
        feature: The feature name to check
        action: Description of what the user was trying to do
    
    Raises:
        ImportError: If dependencies are missing
    """
    available, missing = check_feature(feature)
    if not available:
        raise ImportError(
            f"Cannot {action}. Missing dependencies: {', '.join(missing)}. "
            f"Install with: pip install {' '.join(missing)}"
        )


# Quick checks for common dependencies
HAS_SPACY = check_dependency("spacy")
HAS_LANGCHAIN = check_dependency("langchain_text_splitters")
HAS_PYPDF = check_dependency("pypdf")
HAS_DOCX = check_dependency("docx")
HAS_FASTAPI = check_dependency("fastapi")
HAS_ASSEMBLYAI = check_dependency("assemblyai")
HAS_HUGGINGFACE = check_dependency("sentence_transformers")
