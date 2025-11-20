# Lexical Analyzer

A lexical analyzer implementation that divides input strings into sequences of subwords (tokens) based on user-defined tags specified using regular expressions in reverse Polish notation.

## Overview

This project implements a lexical analyzer (lexer) that tokenizes input text according to user-defined tags. Each tag is specified using a regular expression in reverse Polish notation (RPN), and the system builds finite automata to recognize patterns defined by these expressions.

### Key Features

- **Regular Expression Parsing**: Supports regular expressions in reverse Polish notation with union (+), concatenation (.), and Kleene star (*) operators
- **Finite Automata Construction**: Automatically builds non-deterministic finite automata (NFA) from regular expressions
- **Longest Match Strategy**: Prioritizes the longest matching prefix when multiple tags could match
- **Priority Resolution**: When multiple tags match the same length, uses the order of definition as a tiebreaker
- **Interactive Command Interface**: Full-featured CLI with commands for tag management, file processing, and automata inspection
- **Overlap Detection**: Warns users when tag definitions overlap
- **Clean Architecture**: Modular design with separation of concerns (domain, application, infrastructure layers)

## Project Structure

```
.
├── src/
│   ├── domain/           # Core business logic
│   │   ├── automaton.py  # Finite automaton implementation
│   │   ├── regex_parser.py  # Regular expression parser (RPN)
│   │   └── tag.py        # Tag definition and parsing
│   ├── application/      # Use cases and application logic
│   │   ├── lexer.py      # Main lexical analyzer
│   │   └── command_handler.py  # Command processing
│   └── infrastructure/   # External interfaces
│       └── cli.py        # Command-line interface
├── test/                 # Test suite
│   ├── test_regex_parser.py
│   ├── test_tag.py
│   ├── test_lexer.py
│   └── test_command_handler.py
├── main.py               # Entry point
├── Makefile              # Build system
├── setup.py              # Python package setup
└── requirements.txt       # Dependencies (none required)
```

## Architecture

The project follows **Clean Architecture** principles with three main layers:

1. **Domain Layer** (`src/domain/`): Contains core business logic
   - `FiniteAutomaton`: NFA implementation for pattern matching
   - `RegexParser`: Parses RPN regular expressions and builds automata
   - `Tag`: Represents a tag definition with its automaton

2. **Application Layer** (`src/application/`): Contains use cases
   - `LexicalAnalyzer`: Main tokenization logic with longest match and priority
   - `CommandHandler`: Processes commands and manages tag definitions

3. **Infrastructure Layer** (`src/infrastructure/`): External interfaces
   - `CLI`: Interactive command-line interface

## Installation

### Prerequisites

- Python 3.8 or higher
- Unix/Linux environment (or Windows with compatible tools)

### Setup

No external dependencies are required. The project uses only Python standard library.

```bash
# Clone the repository
git clone <repository-url>
cd lexical-analyzer

# Install (optional, for development)
python setup.py install

# Or simply run directly
python main.py
```

## Usage

### Running the Program

```bash
# Using Python directly
python main.py

# Or using Make
make run
```

### Interactive Commands

The program runs in interactive mode. You can define tags and execute commands:

#### Defining Tags

Tags are defined using the format: `TAGNAME: EXPRESSION`

Where `EXPRESSION` is a regular expression in reverse Polish notation.

**Example:**
```
INT: 01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.
VAR: ab.ba.+*
SPACE:  *
EQUALS: =
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `:p <text>` | Process and tokenize the input text | `:p x=1037` |
| `:d <file>` | Process and tokenize a file | `:d input.txt` |
| `:c <file>` | Load tag definitions from a file | `:c tags.lex` |
| `:o <file>` | Set output file for results | `:o output.txt` |
| `:l` | List all defined tags | `:l` |
| `:a` | List formal definitions of all automata | `:a` |
| `:s <file>` | Save current tags to a file | `:s tags.lex` |
| `:q` | Quit the program | `:q` |

### Example Session

```
INT: 01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.
[INFO] Tag 'INT' defined successfully
VAR: ab.ba.+*
[INFO] Tag 'VAR' defined successfully
SPACE:  *
[INFO] Tag 'SPACE' defined successfully
EQUALS: =
[INFO] Tag 'EQUALS' defined successfully
:p x=1037
VAR EQUALS INT
:l
[INFO] Tag definitions:
  INT: 01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.
  VAR: ab.ba.+*
  SPACE:  *
  EQUALS: =
:q
[INFO] Exiting program
```

## Regular Expression Syntax

### Operators

- **Character**: Any ASCII character (codes 32-126) represents itself
- **Union (`+`)**: `e1e2+` represents `L(e1) ∪ L(e2)`
- **Concatenation (`.`)**: `e1e2.` represents `L(e1) · L(e2)`
- **Kleene Star (`*`)**: `e*` represents `L(e)*`
- **Lambda (`\l`)**: Represents the empty string `{λ}`
- **Empty Language**: Empty expression represents `∅`

### Escape Sequences

| Escape | Character | ASCII Code |
|--------|-----------|------------|
| `\n` | Newline | 10 |
| `\\` | Backslash | 92 |
| `\*` | Asterisk | 42 |
| `\.` | Period | 46 |
| `\+` | Plus sign | 43 |
| `\l` | Lambda (empty string) | - |

### Examples

- `ab.ba.+*` → `(ab + ba)*`
- `01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.` → `(0+1+2+...+9)(0+1+2+...+9)*` (integers)

## Testing

Run the test suite:

```bash
# Using Make
make test

# Or directly with unittest
python -m unittest discover -s test -p "test_*.py" -v

# Or with pytest (if installed)
pytest test/ -v
```

### Test Coverage

The test suite includes:
- Regular expression parser tests
- Tag definition parsing tests
- Lexical analyzer tokenization tests
- Command handler tests

## Building

The project includes a `Makefile` for common operations:

```bash
make test      # Run tests
make run       # Run the program
make clean     # Clean generated files
make install   # Install (no-op, no dependencies)
```

## Error Handling

The program provides three types of messages:

- **[INFO]**: Informational messages (successful operations)
- **[WARNING]**: Warnings (overlaps, invalid but recoverable situations)
- **[ERROR]**: Errors (invalid input, file not found, tokenization failures)

### Common Error Scenarios

1. **Invalid Tag Definition**: Missing colon, incorrect spacing, invalid regex
2. **Duplicate Tag Name**: Attempting to define a tag with an existing name
3. **Tokenization Failure**: Input cannot be fully tokenized with available tags
4. **File Errors**: File not found, permission errors, etc.

## Algorithm Details

### Longest Match Strategy

When tokenizing input, the analyzer:
1. Tries all tags at the current position
2. Selects the tag that matches the longest prefix
3. If multiple tags match the same length, selects the first defined tag
4. Advances the position and repeats

### Overlap Detection

The system detects when two tags can match the same strings and warns the user. During tokenization, priority is given to the first defined tag when overlaps occur.

## Project Specification Document

The complete project specification is available in the repository:

**Document**: [`ACFrOgALQLndU88srjBOsX865RxEumVtgl9fVsOwSczo0R0SkJX8Q8V80tGylKszPlCl-7lHNAzfa4LRcX_pN-aPlhfBvnRcoeU9Ejke3knp3VOX5uth6qbdhLb5HZ4ReSE5vwZs4oFiVLAgHWs9.pdf`](ACFrOgALQLndU88srjBOsX865RxEumVtgl9fVsOwSczo0R0SkJX8Q8V80tGylKszPlCl-7lHNAzfa4LRcX_pN-aPlhfBvnRcoeU9Ejke3knp3VOX5uth6qbdhLb5HZ4ReSE5vwZs4oFiVLAgHWs9.pdf)

This document contains:
- Complete technical specification
- Tag definition language syntax
- Command reference
- Examples and use cases
- Evaluation criteria

## Authors

- **Fabrício de Sousa Guidine**
- **Débora Izabel Duarte**
- **Guilherme**
- **Juarez**

## Course Information

**Course**: Aspectos Teóricos da Computação (DCC146)  
**Institution**: Departamento de Ciência da Computação - UFJF  
**Professor**: Prof. Dr. Gleiph Ghiotto Lima de Menezes  
**Semester**: 2021-1 (ERE - Ensino Remoto Emergencial)

## License

See [LICENSE](LICENSE) file for details.

## Contributing

This is an academic project. For questions or issues, please contact the authors.

## Acknowledgments

Special thanks to Prof. Dr. Gleiph Ghiotto Lima de Menezes for the project specification and guidance.
