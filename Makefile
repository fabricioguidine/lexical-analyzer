# Makefile for Lexical Analyzer
# Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez

.PHONY: help run test clean install format lint

# Default target
.DEFAULT_GOAL := help

# Python interpreter
PYTHON := python
PYTEST := pytest

# Directories
SRC_DIR := src
TEST_DIR := test
DOCS_DIR := docs

##@ General

help: ## Display this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

##@ Development

run: ## Run the lexical analyzer program
	$(PYTHON) main.py

test: ## Run the test suite
	@echo "Running tests..."
	@if command -v $(PYTEST) > /dev/null 2>&1; then \
		$(PYTEST) $(TEST_DIR)/ -v; \
	else \
		$(PYTHON) -m unittest discover -s $(TEST_DIR) -p "test_*.py" -v; \
	fi

install: ## Install the package (no external dependencies required)
	@echo "Installing lexical-analyzer..."
	$(PYTHON) setup.py install
	@echo "Installation complete. No external dependencies required."

##@ Code Quality

format: ## Format code using black (optional)
	@echo "Formatting code..."
	@if command -v black > /dev/null 2>&1; then \
		black $(SRC_DIR)/ $(TEST_DIR)/; \
		echo "Code formatted successfully."; \
	else \
		echo "black not installed. Install with: pip install black"; \
	fi

lint: ## Lint code using pylint (optional)
	@echo "Linting code..."
	@if command -v pylint > /dev/null 2>&1; then \
		pylint $(SRC_DIR)/; \
	else \
		echo "pylint not installed. Install with: pip install pylint"; \
	fi

##@ Maintenance

clean: ## Clean generated files and caches
	@echo "Cleaning generated files..."
	@if command -v find > /dev/null 2>&1; then \
		find . -type f -name "*.pyc" -delete; \
		find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true; \
		find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true; \
		find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true; \
		find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true; \
	fi
	@if exist __pycache__ rmdir /s /q __pycache__ 2>nul || true
	@if exist *.egg-info rmdir /s /q *.egg-info 2>nul || true
	@if exist .pytest_cache rmdir /s /q .pytest_cache 2>nul || true
	@if exist .mypy_cache rmdir /s /q .mypy_cache 2>nul || true
	@echo "Clean complete."

##@ Documentation

docs: ## Open project documentation
	@if exist $(DOCS_DIR)\project-specification.pdf ( \
		echo "Opening project specification..."; \
		start $(DOCS_DIR)\project-specification.pdf \
	) else ( \
		echo "Documentation not found in $(DOCS_DIR)/" \
	)
