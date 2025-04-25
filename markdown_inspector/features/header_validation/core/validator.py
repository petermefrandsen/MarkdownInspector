"""
Header validation module for Markdown Inspector.
Handles parsing markdown headers and validating against configuration requirements.
"""

import re
from typing import Dict, List, Tuple, Any


class HeaderValidator:
    """Validates markdown headers against configuration requirements."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the validator with configuration.

        Args:
            config: Dictionary containing the validation configuration
        """
        self.config = config

    def parse_markdown_headers(self, markdown_content: str) -> List[Dict[str, Any]]:
        """
        Parse headers from markdown content.

        Args:
            markdown_content: The content of the markdown file

        Returns:
            List of dictionaries with header info (title, level)
        """
        # Regular expression to match markdown headers (# Header, ## Header, etc.)
        header_pattern = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+)?$", re.MULTILINE)

        headers = []
        for match in header_pattern.finditer(markdown_content):
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append({"title": title, "level": level})

        return headers

    def validate_headers(
        self, actual_headers: List[Dict[str, Any]]
    ) -> Tuple[bool, List[str]]:
        """
        Validate parsed headers against configuration requirements.
        
        This validation supports documents that have additional headers between the
        required headers - only the headers specified in the configuration are checked
        for existence, correct order, and proper level.

        Args:
            actual_headers: List of dictionaries with header info

        Returns:
            Tuple of (success_flag, list_of_validation_messages)
        """
        if "headings" not in self.config:
            return False, ["Configuration file does not contain 'headings' key"]

        expected_headers = self.config["headings"]
        messages = []
        success = True

        # Check if all required headers exist
        actual_titles = [h["title"] for h in actual_headers]
        for expected in expected_headers:
            if expected["title"] not in actual_titles:
                messages.append(f"Missing header: '{expected['title']}'")
                success = False

        # Extract only the required headers from the document, preserving their order
        # This allows for additional headers to exist between required headers
        filtered_actual_headers = [h for h in actual_headers if h["title"] in [eh["title"] for eh in expected_headers]]
        actual_titles_ordered = [h["title"] for h in filtered_actual_headers]

        # Create a map of titles that appear in both lists
        title_positions_expected = {title["title"]: i for i, title in enumerate(expected_headers)}

        # Check if the relative order of required headers matches the expected order
        previous_position = -1
        for title in actual_titles_ordered:
            if title in title_positions_expected:
                current_position = title_positions_expected[title]
                if current_position < previous_position:
                    messages.append(f"Header '{title}' is out of order")
                    success = False
                previous_position = current_position

        # Check header levels
        for actual in actual_headers:
            for expected in expected_headers:
                if (
                    actual["title"] == expected["title"]
                    and actual["level"] != expected["level"]
                ):
                    messages.append(
                        f"Header level mismatch for '{actual['title']}': "
                        f"expected level {expected['level']}, got level {actual['level']}"
                    )
                    success = False

        if success:
            messages.append("All headers validated successfully")

        return success, messages
