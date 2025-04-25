"""
End-to-end tests for Markdown Inspector.
Tests the entire application flow from CLI to validation.
"""

import os
import tempfile
import json
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

from markdown_inspector.cli import main


class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the Markdown Inspector application."""

    def setUp(self):
        """Set up test environment with temporary files."""
        # Create a temporary config file
        self.config_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        self.config = {
            "headings": [
                {"title": "Test Document", "level": 1},
                {"title": "Section One", "level": 2},
                {"title": "Section Two", "level": 2},
                {"title": "Conclusion", "level": 2},
            ]
        }
        json.dump(self.config, self.config_file)
        self.config_file.close()

        # Create temporary markdown files for testing
        self.valid_md = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        )
        self.valid_md.write(
            "# Test Document\n\nContent here\n\n## Section One\n\nMore content\n\n## Section Two\n\nEven more content\n\n## Conclusion\n\nFinal content"
        )
        self.valid_md.close()

        self.invalid_md = tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        )
        self.invalid_md.write(
            "# Test Document\n\nContent here\n\n## Section Two\n\nWrong order\n\n## Section One\n\nOut of order\n\n# Conclusion\n\nWrong level"
        )
        self.invalid_md.close()

    def tearDown(self):
        """Clean up temporary files."""
        os.unlink(self.config_file.name)
        os.unlink(self.valid_md.name)
        os.unlink(self.invalid_md.name)

    @patch("sys.argv")
    def test_valid_document(self, mock_argv):
        """Test CLI with a valid markdown document."""
        # Set up CLI arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "markdowninspector",
            "--config",
            self.config_file.name,
            "--target",
            self.valid_md.name,
        ][i]

        # Run CLI and capture exit code
        with patch("sys.stdout"):  # Suppress output during test
            exit_code = main()

        # Verify success
        self.assertEqual(exit_code, 0)

    @patch("sys.argv")
    def test_invalid_document(self, mock_argv):
        """Test CLI with an invalid markdown document."""
        # Set up CLI arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "markdowninspector",
            "--config",
            self.config_file.name,
            "--target",
            self.invalid_md.name,
        ][i]

        # Run CLI and capture exit code
        with patch("sys.stdout"):  # Suppress output during test
            exit_code = main()

        # Verify failure
        self.assertEqual(exit_code, 1)

    @patch("sys.argv")
    def test_json_output(self, mock_argv):
        """Test CLI with JSON output format."""
        # Set up CLI arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "markdowninspector",
            "--config",
            self.config_file.name,
            "--target",
            self.valid_md.name,
            "--output-format",
            "json",
        ][i]

        # Run CLI and capture output
        with patch("sys.stdout") as mock_stdout:
            exit_code = main()

        # Verify JSON output was requested
        self.assertTrue(mock_stdout.write.called)

    @patch("sys.argv")
    def test_nonexistent_file(self, mock_argv):
        """Test CLI with a non-existent target file."""
        # Set up CLI arguments
        mock_argv.__getitem__.side_effect = lambda i: [
            "markdowninspector",
            "--config",
            self.config_file.name,
            "--target",
            "/path/to/nonexistent/file.md",
        ][i]

        # Run CLI and capture exit code
        with patch("sys.stdout"), patch("sys.stderr"):  # Suppress output during test
            exit_code = main()

        # Verify failure - actual implementation returns exit code 1 for non-existent files
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
