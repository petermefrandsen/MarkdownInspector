"""
Command-line interface for Markdown Inspector.
"""

import sys
import argparse
import json
from typing import List, Optional
from markdown_inspector.analyzer import MarkdownAnalyzer


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        description="Analyze markdown files against configuration requirements"
    )

    parser.add_argument(
        "--config", required=True, help="Path to the JSON configuration file"
    )

    parser.add_argument(
        "--target", required=True, help="Path to the markdown file to analyze"
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Display detailed output"
    )

    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Format for the output (default: text)",
    )

    return parser.parse_args(args)


def format_output(
    success: bool, messages: List[str], output_format: str, verbose: bool = False
) -> str:
    """
    Format the analysis output based on the specified format.

    Args:
        success: Whether the analysis succeeded
        messages: List of validation messages
        output_format: The output format (text or json)
        verbose: Whether to include verbose output

    Returns:
        Formatted output string
    """
    if output_format == "json":
        result = {"success": success, "messages": messages}

        return json.dumps(result, indent=2)
    else:
        # Text output
        result = [f"Analysis {'succeeded' if success else 'failed'}"]

        # Only show detailed messages if verbose or analysis failed
        if verbose or not success:
            for message in messages:
                result.append(f"- {message}")

        return "\n".join(result)


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        args: Command line arguments (uses sys.argv if None)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    parsed_args = parse_args(args)

    try:
        analyzer = MarkdownAnalyzer(parsed_args.config)
        success, messages = analyzer.analyze_file(parsed_args.target)

        # Format and print output
        output = format_output(
            success, messages, parsed_args.output_format, parsed_args.verbose
        )
        print(output)

        # Return appropriate exit code
        return 0 if success else 1

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
