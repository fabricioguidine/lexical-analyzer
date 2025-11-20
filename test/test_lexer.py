"""
Tests for lexical analyzer.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

import unittest
from src.domain.tag import Tag
from src.application.lexer import LexicalAnalyzer


class TestLexicalAnalyzer(unittest.TestCase):
    """Test cases for LexicalAnalyzer."""
    
    def setUp(self):
        # Create simple tags for testing
        self.var_tag = Tag("VAR", "ab.ba.+*")  # (ab + ba)*
        self.int_tag = Tag("INT", "01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.")
        # SPACE: one or more spaces
        # Using reverse Polish: space character followed by Kleene star
        self.space_tag = Tag("SPACE", " *")  # Space(s) - ' ' followed by *
        self.equals_tag = Tag("EQUALS", "=")
    
    def test_simple_tokenization(self):
        """Test simple tokenization."""
        tags = [self.var_tag, self.space_tag, self.equals_tag]
        lexer = LexicalAnalyzer(tags)
        tokens = lexer.tokenize("ab =")
        self.assertEqual(tokens, ["VAR", "SPACE", "EQUALS"])
    
    def test_longest_match(self):
        """Test longest match priority."""
        # Tag that matches "a" and tag that matches "aa"
        short_tag = Tag("SHORT", "a")
        long_tag = Tag("LONG", "aa.")
        tags = [short_tag, long_tag]
        lexer = LexicalAnalyzer(tags)
        tokens = lexer.tokenize("aa")
        # Should prefer longest match
        self.assertEqual(tokens, ["LONG"])
    
    def test_priority_order(self):
        """Test priority by definition order."""
        # Two tags that match same length
        tag1 = Tag("FIRST", "a*")
        tag2 = Tag("SECOND", "a*")
        tags = [tag1, tag2]
        lexer = LexicalAnalyzer(tags)
        tokens = lexer.tokenize("aaa")
        # Should prefer first defined
        self.assertEqual(tokens, ["FIRST"])
    
    def test_incomplete_tokenization(self):
        """Test error on incomplete tokenization."""
        tags = [self.var_tag]
        lexer = LexicalAnalyzer(tags)
        with self.assertRaises(ValueError):
            lexer.tokenize("xyz")  # Cannot be tokenized


if __name__ == "__main__":
    unittest.main()

