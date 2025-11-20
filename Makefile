# Makefile for Lexical Analyzer
# Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez

.PHONY: run test clean install

# Default target
all: test

# Run the program
run:
	python main.py

# Run tests
test:
	python -m pytest test/ -v
	python -m unittest discover -s test -p "test_*.py" -v

# Install (no dependencies needed)
install:
	@echo "No external dependencies required"

# Clean generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f *.txt *.log

# Format code (optional, requires black)
format:
	@echo "Formatting code..."
	@if command -v black > /dev/null; then black src/ test/; else echo "black not installed"; fi

# Lint code (optional, requires pylint)
lint:
	@echo "Linting code..."
	@if command -v pylint > /dev/null; then pylint src/; else echo "pylint not installed"; fi

