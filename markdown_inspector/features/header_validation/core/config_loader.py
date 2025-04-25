"""
Configuration loader for Markdown Inspector.
Handles loading and validating configuration files.
"""

import json
from typing import Dict, Any


class ConfigLoader:
    """Loads and validates configuration files."""

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Load and parse the JSON configuration file.

        Args:
            config_path: Path to the configuration file

        Returns:
            Dict containing the parsed configuration

        Raises:
            ValueError: If the configuration file contains invalid JSON
            FileNotFoundError: If the configuration file doesn't exist
        """
        try:
            with open(config_path, "r") as config_file:
                return json.load(config_file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in configuration file: {config_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """
        Validate that the configuration has the required structure.

        Args:
            config: The configuration dictionary to validate

        Returns:
            True if the configuration is valid, False otherwise
        """
        return "headings" in config and isinstance(config["headings"], list)
