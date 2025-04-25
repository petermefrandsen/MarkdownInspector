# Markdown Inspector

A command-line tool to analyze markdown files based on configuration requirements.

## Overview

Markdown Inspector validates markdown files against structural requirements defined in JSON configuration files. The initial version focuses on validating heading structures (existence, order, and hierarchy).

## Installation

### Using a Virtual Environment (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd MarkdownInspector

# Set up using Makefile (recommended)
make setup

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Using pip

You can install the package directly using pip:

```bash
# Install from PyPI (if published)
pip install markdown-inspector

# Or install from the local directory
pip install -e .
```

### Verifying Installation

After installation, you should be able to run the CLI tool:

```bash
# Check if the command is available
markdowninspector --help
# Or use the shorter alias
mkinspec --help
```

If you get a "command not found" error, make sure:

1. The virtual environment is activated (if using one)
2. The installation completed successfully
3. The directory containing the installed scripts is in your PATH

### Manual Installation

If you prefer not to use the Makefile:

```bash
# Clone the repository
git clone <repository-url>
cd MarkdownInspector

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# Install development dependencies (optional)
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
markdowninspector --config <config_file.json> --target <markdown_file.md>
```

Or use the shorter alias:

```bash
mkinspec --config <config_file.json> --target <markdown_file.md>
```

### Options

- `--config`: Path to the JSON configuration file (required)
- `--target`: Path to the markdown file to analyze (required)
- `--verbose`: Display detailed output
- `--output-format`: Format for output (text, json)

### Example

```bash
markdowninspector --config config/architecture-docs-req.json --target docs/architecture.md
```

### Configuration File Format

JSON files defining required document structure:

```json
{
  "headings": [
    {
      "title": "Document Title",
      "level": 1
    },
    {
      "title": "Section Header",
      "level": 2
    }
  ]
}
```

## Development

### Project Structure

```
MarkdownInspector/
├── markdown_inspector/               # Main package
│   ├── __init__.py                   # Package initialization
│   ├── analyzer.py                   # Main analyzer interface
│   ├── cli.py                        # Command-line interface
│   └── features/                     # Feature-based modules
│       ├── __init__.py
│       └── header_validation/        # Header validation feature
│           ├── __init__.py
│           ├── core/                 # Core functionality
│           │   ├── __init__.py
│           │   ├── config_loader.py  # Configuration loading
│           │   └── validator.py      # Header validation logic
│           └── tests/                # Feature-specific tests
├── config/                           # Sample configuration files
├── tests/                            # Integration tests
└── setup.py                          # Package setup script
```

### Using the Makefile

The project includes a Makefile to simplify common tasks:

```bash
make setup      # Set up virtual environment and install dependencies
make test       # Run tests
make lint       # Run linters (flake8, black)
make format     # Format code using black
make clean      # Clean up temporary files and virtual environment
make run        # Run the CLI with help output
```

## Running Tests

### Using the Makefile (recommended)

```bash
make test       # Run all tests
```

### Using pytest directly

First, activate the virtual environment:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Then run the tests:

```bash
pytest                  # Run all tests
pytest -v               # Run with verbose output
pytest --cov            # Run with coverage report
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
