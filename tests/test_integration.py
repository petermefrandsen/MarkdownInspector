"""
Integration tests for Markdown Inspector.

These tests verify the behavior of the entire system working together.
"""

import os
import unittest
from pathlib import Path
import sys

# Add parent directory to path to allow importing the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from markdown_inspector.analyzer import MarkdownAnalyzer


class TestMarkdownInspectorIntegration(unittest.TestCase):
    """Integration tests for Markdown Inspector."""
    
    def setUp(self):
        """Set up test environment with paths to test files."""
        self.test_dir = Path(__file__).parent
        self.config_file = os.path.join(
            str(Path(__file__).parent.parent),
            "markdown_inspector/features/header_validation/tests/test-files/test-config-file.json"
        )
        # Ensure the test config exists
        self.assertTrue(os.path.exists(self.config_file), f"Test config not found: {self.config_file}")
        
        # Set test file paths
        self.valid_file = os.path.join(self.test_dir, "testfile_headers_exist.md")
        self.missing_headers_file = os.path.join(self.test_dir, "testfile_headers_missing.md")
        self.wrong_order_file = os.path.join(self.test_dir, "testfile_headers_exist_but_wrong_order.md")
        self.additional_headers_file = os.path.join(self.test_dir, "testfile_headers_with_additional.md")
        
        # Set up analyzer
        self.analyzer = MarkdownAnalyzer(self.config_file)

    def test_valid_headers(self):
        """Test integration with a file containing all required headers."""
        success, messages = self.analyzer.analyze_file(self.valid_file)
        self.assertTrue(success)
        self.assertIn("All headers validated successfully", messages)

    def test_missing_headers(self):
        """Test integration with a file missing required headers."""
        success, messages = self.analyzer.analyze_file(self.missing_headers_file)
        self.assertFalse(success)
        # The exact error message will depend on which headers are missing in the test file
        self.assertTrue(any("Missing header:" in msg for msg in messages))

    def test_wrong_order_headers(self):
        """Test integration with a file having headers in the wrong order."""
        success, messages = self.analyzer.analyze_file(self.wrong_order_file)
        self.assertFalse(success)
        self.assertTrue(any("out of order" in msg for msg in messages))

    def test_additional_headers(self):
        """Test integration with a file containing additional headers between required ones.
        
        This test verifies that the tool correctly validates documents that have all required
        headers in the correct order but also contain additional headers in between.
        
        This reflects a common real-world scenario where documentation includes all required
        sections but also has additional sections not specified in the template.
        """
        success, messages = self.analyzer.analyze_file(self.additional_headers_file)
        self.assertTrue(success)
        self.assertIn("All headers validated successfully", messages)

    def test_prd_document(self):
        """Test the PRD document against a custom validation config.
        
        This test verifies that the tool can validate the PRD markdown file
        against a configuration that requires specific sections in a specific order.
        """
        # Create a temp config file for PRD validation
        import tempfile
        import json
        
        prd_path = os.path.join(str(Path(__file__).parent.parent), "prd.md")
        self.assertTrue(os.path.exists(prd_path), f"PRD file not found: {prd_path}")
        
        prd_config = {
            "headings": [
                {"title": "Markdown Inspector - Product Requirements Document", "level": 1},
                {"title": "Overview", "level": 2},
                {"title": "Problem Statement", "level": 2},
                {"title": "Target Users", "level": 2},
                {"title": "Key Features", "level": 2},
                {"title": "Technical Requirements", "level": 2},
                {"title": "Implementation Plan", "level": 2},
                {"title": "Testing", "level": 2},
                {"title": "Success Metrics", "level": 2}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp:
            json.dump(prd_config, temp)
            temp_config_path = temp.name
        
        try:
            # Create a new analyzer with the PRD config
            prd_analyzer = MarkdownAnalyzer(temp_config_path)
            success, messages = prd_analyzer.analyze_file(prd_path)
            
            # The PRD should pass validation
            self.assertTrue(success)
            self.assertIn("All headers validated successfully", messages)
        finally:
            # Clean up temp file
            if os.path.exists(temp_config_path):
                os.unlink(temp_config_path)


if __name__ == "__main__":
    unittest.main()