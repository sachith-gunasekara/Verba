"""Configuration management helpers for RAG pipeline."""

from typing import Dict, Any, Optional


class ConfigManager:
    """Manages RAG configuration for the SDK."""

    def __init__(self, rag_config: Dict[str, Any]):
        """Initialize with RAG config from VerbaManager."""
        self._rag_config = rag_config

    def update_component(
        self,
        component_type: str,
        component_name: str,
        config_overrides: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Update a component in the RAG config.

        Args:
            component_type: One of "Reader", "Chunker", "Embedder", "Retriever", "Generator"
            component_name: Name of the component to select
            config_overrides: Optional dict of config key-value pairs to override
        """
        if component_type not in self._rag_config:
            raise ValueError(f"Invalid component type: {component_type}")

        component_class = self._rag_config[component_type]

        # Check if component exists
        if component_name not in component_class["components"]:
            available = list(component_class["components"].keys())
            raise ValueError(
                f"Component '{component_name}' not found. Available: {available}"
            )

        # Update selected component
        component_class["selected"] = component_name

        # Apply config overrides if provided
        if config_overrides:
            component = component_class["components"][component_name]
            for key, value in config_overrides.items():
                if key in component["config"]:
                    component["config"][key]["value"] = value
                else:
                    raise ValueError(
                        f"Config key '{key}' not found in component '{component_name}'"
                    )

    def get_component_config(self, component_type: str) -> Dict[str, Any]:
        """Get current configuration for a component type."""
        if component_type not in self._rag_config:
            raise ValueError(f"Invalid component type: {component_type}")

        component_class = self._rag_config[component_type]
        selected = component_class["selected"]
        return component_class["components"][selected]

    def get_rag_config(self) -> Dict[str, Any]:
        """Get the full RAG configuration."""
        return self._rag_config.copy()

    def get_selected_components(self) -> Dict[str, str]:
        """Get currently selected components."""
        return {
            "Reader": self._rag_config["Reader"]["selected"],
            "Chunker": self._rag_config["Chunker"]["selected"],
            "Embedder": self._rag_config["Embedder"]["selected"],
            "Retriever": self._rag_config["Retriever"]["selected"],
            "Generator": self._rag_config["Generator"]["selected"],
        }
