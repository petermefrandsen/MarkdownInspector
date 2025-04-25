"""
Analyzer module for Markdown Inspector.
Handles analyzing markdown files based on configuration requirements.
"""

from typing import Dict, List, Tuple, Any
from markdown_inspector.features.header_validation.core.config_loader import (
    ConfigLoader,
)
from markdown_inspector.features.header_validation.core.validator import HeaderValidator


class MarkdownAnalyzer:
    """Analyzes markdown files against configuration requirements."""

    def __init__(self, config_path: str):
        """
        Initialize the analyzer with a configuration file.

        Args:
            config_path: Path to the JSON configuration file
        """
        self.config = ConfigLoader.load_config(config_path)
        self.header_validator = HeaderValidator(self.config)

    def analyze_file(self, markdown_path: str) -> Tuple[bool, List[str]]:
        """
        Analyze a markdown file against the configuration requirements.

        Args:
            markdown_path: Path to the markdown file

        Returns:
            Tuple of (success_flag, list_of_validation_messages)
        """
        try:
            with open(markdown_path, "r") as md_file:
                content = md_file.read()
        except FileNotFoundError:
            return False, [f"Markdown file not found: {markdown_path}"]

        # Parse the headers from the markdown file
        actual_headers = self.header_validator.parse_markdown_headers(content)

        # Validate headers against configuration
        return self.header_validator.validate_headers(actual_headers)
