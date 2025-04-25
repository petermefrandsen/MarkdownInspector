"""
Setup script for Markdown Inspector.
"""

from setuptools import setup, find_packages
from markdown_inspector import __version__

setup(
    name="markdown-inspector",
    version=__version__,
    description="A tool to analyze markdown files based on configuration requirements",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/markdown-inspector",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "markdowninspector=markdown_inspector.cli:main",
            "mkinspec=markdown_inspector.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)