"""
Tag definition and management.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from typing import Optional
from .automaton import FiniteAutomaton
from .regex_parser import RegexParser


class Tag:
    """Represents a tag definition with its automaton."""
    
    def __init__(self, name: str, expression: str):
        self.name = name
        self.expression = expression
        self.automaton: Optional[FiniteAutomaton] = None
        self._parser = RegexParser()
        self._build_automaton()
    
    def _build_automaton(self):
        """Build the automaton from the regular expression."""
        try:
            self.automaton = self._parser.build_automaton(self.expression)
        except Exception as e:
            raise ValueError(f"Invalid regular expression: {e}")
    
    def match(self, text: str, start_pos: int = 0) -> Optional[int]:
        """Match the tag against text starting at start_pos. Returns end position or None."""
        if not self.automaton:
            return None
        return self.automaton.match(text, start_pos)
    
    def get_formal_definition(self) -> str:
        """Get formal definition of the tag's automaton."""
        if not self.automaton:
            return f"Tag {self.name}: Invalid automaton"
        return f"Tag: {self.name}\nExpression: {self.expression}\n{self.automaton.get_formal_definition()}"
    
    def __repr__(self):
        return f"Tag(name='{self.name}', expression='{self.expression}')"


class TagDefinitionParser:
    """Parser for tag definitions."""
    
    @staticmethod
    def parse(line: str) -> Optional[Tag]:
        """
        Parse a tag definition line.
        Format: TAGNAME: EXPRESSION
        Returns Tag if valid, None if invalid.
        """
        line = line.strip()
        if not line:
            return None
        
        # Check for colon
        if ':' not in line:
            return None
        
        colon_pos = line.find(':')
        
        # Validation rules:
        # 1. Name must be unique (checked elsewhere)
        # 2. No space between name and colon
        if colon_pos > 0 and line[colon_pos - 1] == ' ':
            return None
        
        # 3. Exactly one space after colon
        if colon_pos + 1 >= len(line) or line[colon_pos + 1] != ' ':
            return None
        
        name = line[:colon_pos].strip()
        expression = line[colon_pos + 1:].strip()
        
        if not name:
            return None
        
        if not expression:
            return None
        
        try:
            return Tag(name, expression)
        except ValueError:
            return None

