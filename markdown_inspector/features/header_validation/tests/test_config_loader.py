"""
Tests for the configuration loader module.
"""

import os
import json
import unittest
import tempfile
from pathlib import Path

from markdown_inspector.features.header_validation.core.config_loader import (
    ConfigLoader,
)


class TestConfigLoader(unittest.TestCase):
    """Test cases for the ConfigLoader."""

    def test_load_valid_config(self):
        """Test loading a valid configuration file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            config = {
                "headings": [
                    {"title": "Test Header", "level": 1},
                    {"title": "Another Header", "level": 2},
                ]
            }
            json.dump(config, temp_file)
            temp_file_path = temp_file.name

        try:
            loaded_config = ConfigLoader.load_config(temp_file_path)
            self.assertEqual(loaded_config, config)
            self.assertTrue(ConfigLoader.validate_config(loaded_config))
        finally:
            os.unlink(temp_file_path)

    def test_load_invalid_json(self):
        """Test loading an invalid JSON file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            temp_file.write("{invalid json}")
            temp_file_path = temp_file.name

        try:
            with self.assertRaises(ValueError):
                ConfigLoader.load_config(temp_file_path)
        finally:
            os.unlink(temp_file_path)

    def test_load_nonexistent_file(self):
        """Test loading a non-existent file."""
        non_existent_path = "/tmp/this_file_does_not_exist_12345.json"

        # Ensure the file doesn't exist
        if os.path.exists(non_existent_path):
            os.unlink(non_existent_path)

        with self.assertRaises(FileNotFoundError):
            ConfigLoader.load_config(non_existent_path)

    def test_validate_config(self):
        """Test validating configuration structure."""
        # Valid config
        valid_config = {"headings": [{"title": "Test", "level": 1}]}
        self.assertTrue(ConfigLoader.validate_config(valid_config))

        # Invalid configs
        self.assertFalse(ConfigLoader.validate_config({}))
        self.assertFalse(ConfigLoader.validate_config({"headings": "not a list"}))
        self.assertFalse(ConfigLoader.validate_config({"wrong_key": []}))


if __name__ == "__main__":
    unittest.main()
