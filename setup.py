"""
Setup script for Lexical Analyzer.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from setuptools import setup, find_packages

setup(
    name="lexical-analyzer",
    version="1.0.0",
    description="A lexical analyzer for tokenizing input using user-defined tags with regular expressions",
    author="Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "lexer=src.infrastructure.cli:main",
        ],
    },
)

