"""
Tests for regular expression parser.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

import unittest
from src.domain.regex_parser import RegexParser
from src.domain.automaton import FiniteAutomaton


class TestRegexParser(unittest.TestCase):
    """Test cases for RegexParser."""
    
    def setUp(self):
        self.parser = RegexParser()
    
    def test_single_character(self):
        """Test parsing a single character."""
        automaton = self.parser.build_automaton("a")
        self.assertIsNotNone(automaton.start_state)
        result = automaton.match("a", 0)
        self.assertEqual(result, 1)
        result = automaton.match("b", 0)
        self.assertIsNone(result)
    
    def test_union(self):
        """Test union operator."""
        # a + b should match 'a' or 'b'
        automaton = self.parser.build_automaton("ab+")
        self.assertEqual(automaton.match("a", 0), 1)
        self.assertEqual(automaton.match("b", 0), 1)
        self.assertIsNone(automaton.match("c", 0))
    
    def test_concatenation(self):
        """Test concatenation operator."""
        # ab should match 'ab'
        automaton = self.parser.build_automaton("ab.")
        self.assertEqual(automaton.match("ab", 0), 2)
        self.assertIsNone(automaton.match("a", 0))
        self.assertIsNone(automaton.match("b", 0))
        self.assertIsNone(automaton.match("ba", 0))
    
    def test_kleene_star(self):
        """Test Kleene star operator."""
        # a* should match '', 'a', 'aa', 'aaa', ...
        automaton = self.parser.build_automaton("a*")
        self.assertEqual(automaton.match("", 0), 0)  # Empty string
        self.assertEqual(automaton.match("a", 0), 1)
        self.assertEqual(automaton.match("aa", 0), 2)
        self.assertEqual(automaton.match("aaa", 0), 3)
        self.assertEqual(automaton.match("aaaa", 0), 4)
    
    def test_complex_expression(self):
        """Test complex expression."""
        # (ab + ba)*
        automaton = self.parser.build_automaton("ab.ba.+*")
        self.assertEqual(automaton.match("ab", 0), 2)
        self.assertEqual(automaton.match("ba", 0), 2)
        self.assertEqual(automaton.match("abba", 0), 4)
        self.assertEqual(automaton.match("", 0), 0)
        self.assertEqual(automaton.match("abab", 0), 4)
    
    def test_escape_sequences(self):
        """Test escape sequences."""
        # Test \n
        automaton = self.parser.build_automaton("\\n")
        self.assertEqual(automaton.match("\n", 0), 1)
        
        # Test \\
        automaton = self.parser.build_automaton("\\\\")
        self.assertEqual(automaton.match("\\", 0), 1)
        
        # Test \*
        automaton = self.parser.build_automaton("\\*")
        self.assertEqual(automaton.match("*", 0), 1)
        
        # Test \.
        automaton = self.parser.build_automaton("\\.")
        self.assertEqual(automaton.match(".", 0), 1)
        
        # Test \+
        automaton = self.parser.build_automaton("\\+")
        self.assertEqual(automaton.match("+", 0), 1)
    
    def test_lambda(self):
        """Test lambda (empty string)."""
        automaton = self.parser.build_automaton("\\l")
        self.assertEqual(automaton.match("", 0), 0)
        self.assertEqual(automaton.match("a", 0), 0)  # Matches empty prefix
    
    def test_empty_expression(self):
        """Test empty expression (empty language)."""
        automaton = self.parser.build_automaton("")
        self.assertIsNotNone(automaton.start_state)
        # Empty language should not match anything
        self.assertIsNone(automaton.match("a", 0))
        self.assertIsNone(automaton.match("", 0))
    
    def test_int_tag_example(self):
        """Test INT tag from specification."""
        # INT: 01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.
        # This represents: (0+1+2+...+9)(0+1+2+...+9)*
        digits = "01+2+3+4+5+6+7+8+9+"
        automaton = self.parser.build_automaton(f"{digits}{digits}*.")
        self.assertEqual(automaton.match("0", 0), 1)
        self.assertEqual(automaton.match("123", 0), 3)
        self.assertEqual(automaton.match("1000", 0), 4)
        self.assertEqual(automaton.match("999", 0), 3)
        self.assertIsNone(automaton.match("a", 0))
        self.assertIsNone(automaton.match("", 0))  # Must have at least one digit
    
    def test_nested_expressions(self):
        """Test nested expressions."""
        # (a(b+c))* = a(b+c) then *
        automaton = self.parser.build_automaton("abc+.+*")
        self.assertEqual(automaton.match("", 0), 0)
        self.assertEqual(automaton.match("ab", 0), 2)
        self.assertEqual(automaton.match("ac", 0), 2)
        self.assertEqual(automaton.match("abab", 0), 4)
    
    def test_invalid_expressions(self):
        """Test invalid expressions raise errors."""
        # Not enough operands
        with self.assertRaises(ValueError):
            self.parser.build_automaton("+")
        
        with self.assertRaises(ValueError):
            self.parser.build_automaton("a+")
        
        with self.assertRaises(ValueError):
            self.parser.build_automaton(".")
        
        with self.assertRaises(ValueError):
            self.parser.build_automaton("*")
        
        # Too many operands
        with self.assertRaises(ValueError):
            self.parser.build_automaton("aaa")


if __name__ == "__main__":
    unittest.main()
