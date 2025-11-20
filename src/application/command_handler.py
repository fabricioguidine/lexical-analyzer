"""
Command handler for the interactive interpreter.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from typing import List, Optional, Tuple
from ..domain.tag import Tag, TagDefinitionParser
from .lexer import LexicalAnalyzer


class CommandHandler:
    """Handles all commands for the lexical analyzer."""
    
    def __init__(self):
        self.tags: List[Tag] = []
        self.output_file: Optional[str] = None
        self.lexer: Optional[LexicalAnalyzer] = None
    
    def add_tag(self, tag: Tag) -> bool:
        """
        Add a tag definition.
        Returns True if added, False if duplicate name.
        """
        # Check for duplicate names
        if any(t.name == tag.name for t in self.tags):
            return False
        
        self.tags.append(tag)
        self.lexer = LexicalAnalyzer(self.tags)
        return True
    
    def parse_tag_line(self, line: str) -> Optional[Tag]:
        """Parse a tag definition line."""
        return TagDefinitionParser.parse(line)
    
    def load_tags_from_file(self, filepath: str) -> tuple[List[Tag], List[str]]:
        """
        Load tags from a file.
        Returns (valid_tags, invalid_lines).
        """
        valid_tags = []
        invalid_lines = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    tag = self.parse_tag_line(line)
                    if tag:
                        if self.add_tag(tag):
                            valid_tags.append(tag)
                        else:
                            invalid_lines.append(f"Line {line_num}: Duplicate tag name '{tag.name}'")
                    else:
                        invalid_lines.append(f"Line {line_num}: Invalid tag definition")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
        
        return valid_tags, invalid_lines
    
    def save_tags_to_file(self, filepath: str):
        """Save current tags to a file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for tag in self.tags:
                    f.write(f"{tag.name}: {tag.expression}\n")
        except Exception as e:
            raise Exception(f"Error writing file: {e}")
    
    def set_output_file(self, filepath: str):
        """Set the output file for results."""
        self.output_file = filepath
    
    def process_input(self, text: str) -> str:
        """
        Process input text and return tokenized result.
        Returns space-separated tag names.
        """
        if not self.lexer:
            raise ValueError("No tags defined")
        
        tokens = self.lexer.tokenize(text)
        return " ".join(tokens)
    
    def process_file(self, filepath: str) -> str:
        """
        Process a file and return tokenized result.
        Returns space-separated tag names.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.process_input(text)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    
    def list_tags(self) -> List[str]:
        """List all tag definitions."""
        return [f"{tag.name}: {tag.expression}" for tag in self.tags]
    
    def list_automata(self) -> List[str]:
        """List formal definitions of all automata."""
        return [tag.get_formal_definition() for tag in self.tags]
    
    def check_overlaps(self) -> List[Tuple[str, str]]:
        """Check for overlapping tag definitions."""
        if not self.lexer:
            return []
        return self.lexer.check_overlaps()
    
    def write_output(self, content: str):
        """Write output to file or stdout."""
        if self.output_file:
            try:
                with open(self.output_file, 'a', encoding='utf-8') as f:
                    f.write(content + "\n")
            except Exception as e:
                raise Exception(f"Error writing to output file: {e}")
        else:
            print(content)

