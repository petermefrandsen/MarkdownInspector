.PHONY: setup test lint clean venv install run

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest

venv:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip

install: venv
	$(PIP) install -e .
	$(PIP) install -r requirements.txt

setup: install

test:
	$(PYTEST) -v

lint:
	$(VENV)/bin/flake8 markdown_inspector
	$(VENV)/bin/black --check markdown_inspector

format:
	$(VENV)/bin/black markdown_inspector

clean:
	rm -rf $(VENV)
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	$(PYTHON) -m markdown_inspector.cli --help