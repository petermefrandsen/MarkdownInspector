#!/usr/bin/env python3
"""
Example script demonstrating how to use Markdown Inspector programmatically.
"""

import sys
import json
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from markdown_inspector import MarkdownAnalyzer


def main():
    # Use sample config files from our config directory
    config_file = Path(__file__).parent.parent / "config" / "architecture-docs-req.json"
    
    # Create an example markdown file programmatically
    markdown_content = """# Architecture Document

## Introduction

This document describes the architecture of our system.

## Architecture Overview

Here is an overview of our architecture.

## Components

These are the main components of our system.

## Deployment

This is how the system is deployed.

## Security Considerations

These are the security considerations for our system.
"""
    
    # Write to a temporary file
    temp_file = Path(__file__).parent / "temp_architecture.md"
    with open(temp_file, "w") as f:
        f.write(markdown_content)
    
    try:
        # Create analyzer and check the file
        analyzer = MarkdownAnalyzer(str(config_file))
        success, messages = analyzer.analyze_file(str(temp_file))
        
        # Output results
        print(f"Analysis {'succeeded' if success else 'failed'}")
        for message in messages:
            print(f"- {message}")
            
        # Also demonstrate JSON output
        result = {
            "success": success,
            "messages": messages
        }
        print("\nJSON output:")
        print(json.dumps(result, indent=2))
        
        # Return appropriate exit code
        return 0 if success else 1
        
    finally:
        # Clean up the temporary file
        if temp_file.exists():
            temp_file.unlink()


if __name__ == "__main__":
    sys.exit(main())