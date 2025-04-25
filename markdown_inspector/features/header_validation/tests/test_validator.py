"""
Tests for the header validator module.
"""

import os
import unittest
from pathlib import Path

from markdown_inspector.features.header_validation.core.validator import HeaderValidator


class TestHeaderValidator(unittest.TestCase):
    """Test cases for the HeaderValidator."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent / "test-files"
        self.config = {
            "headings": [
                {"title": "Header abc", "level": 1},
                {"title": "Header 1", "level": 2},
                {"title": "Header 2", "level": 2},
                {"title": "Header 3", "level": 2},
                {"title": "Header 4", "level": 2},
                {"title": "Header 5", "level": 2},
                {"title": "Header 6", "level": 2},
            ]
        }
        self.validator = HeaderValidator(self.config)

    def _read_test_file(self, filename):
        """Helper to read test files."""
        file_path = self.test_dir / filename
        with open(file_path, "r") as file:
            return file.read()

    def test_parse_markdown_headers(self):
        """Test parsing headers from markdown content."""
        content = "# Header 1\n\nSome content\n\n## Header 2\n\nMore content"
        headers = self.validator.parse_markdown_headers(content)

        self.assertEqual(len(headers), 2)
        self.assertEqual(headers[0]["title"], "Header 1")
        self.assertEqual(headers[0]["level"], 1)
        self.assertEqual(headers[1]["title"], "Header 2")
        self.assertEqual(headers[1]["level"], 2)

    def test_valid_headers(self):
        """Test validating headers that match the configuration."""
        content = self._read_test_file("testfile_headers_exist.md")
        headers = self.validator.parse_markdown_headers(content)
        success, messages = self.validator.validate_headers(headers)

        self.assertTrue(success)
        self.assertIn("All headers validated successfully", messages)

    def test_missing_headers(self):
        """Test validating headers with missing required headers."""
        content = self._read_test_file("testfile_headers_missing.md")
        headers = self.validator.parse_markdown_headers(content)
        success, messages = self.validator.validate_headers(headers)

        self.assertFalse(success)
        self.assertIn("Missing header: 'Header 3'", messages)

    def test_wrong_level_headers(self):
        """Test validating headers with incorrect levels."""
        content = self._read_test_file("testfile_headers_wrong_level.md")
        headers = self.validator.parse_markdown_headers(content)
        success, messages = self.validator.validate_headers(headers)

        self.assertFalse(success)
        self.assertTrue(any("level mismatch" in msg for msg in messages))

    def test_additional_headers_between_required(self):
        """Test validating a document with additional headers between required headers."""
        # Create a document with additional headers between required ones
        content = """# Header abc

## Extra header at the beginning

## Header 1

### Some subsection

## Another extra header

## Header 2

## Header 3

#### Deep subsection

## Header 4

## Yet another extra header

## Header 5

## Header 6

## Conclusion header not in requirements
"""
        headers = self.validator.parse_markdown_headers(content)
        success, messages = self.validator.validate_headers(headers)

        # Should pass because all required headers are present in the correct order
        self.assertTrue(success, "Should pass with additional headers between required headers")
        self.assertIn("All headers validated successfully", messages)


if __name__ == "__main__":
    unittest.main()
