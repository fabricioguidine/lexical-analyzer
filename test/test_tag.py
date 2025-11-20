"""
Tests for tag definitions.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

import unittest
from src.domain.tag import Tag, TagDefinitionParser


class TestTag(unittest.TestCase):
    """Test cases for Tag."""
    
    def test_tag_creation(self):
        """Test creating a tag."""
        tag = Tag("VAR", "a*")
        self.assertEqual(tag.name, "VAR")
        self.assertEqual(tag.expression, "a*")
        self.assertIsNotNone(tag.automaton)
    
    def test_tag_matching(self):
        """Test tag matching."""
        tag = Tag("VAR", "a*")
        self.assertEqual(tag.match("aaa", 0), 3)
        self.assertEqual(tag.match("a", 0), 1)
        self.assertEqual(tag.match("", 0), 0)


class TestTagDefinitionParser(unittest.TestCase):
    """Test cases for TagDefinitionParser."""
    
    def test_valid_tag_definition(self):
        """Test parsing valid tag definition."""
        tag = TagDefinitionParser.parse("VAR: a*")
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "VAR")
        self.assertEqual(tag.expression, "a*")
    
    def test_invalid_no_colon(self):
        """Test parsing tag without colon."""
        tag = TagDefinitionParser.parse("VAR a*")
        self.assertIsNone(tag)
    
    def test_invalid_no_space_after_colon(self):
        """Test parsing tag without space after colon."""
        tag = TagDefinitionParser.parse("VAR:a*")
        self.assertIsNone(tag)
    
    def test_invalid_space_before_colon(self):
        """Test parsing tag with space before colon."""
        tag = TagDefinitionParser.parse("VAR : a*")
        self.assertIsNone(tag)
    
    def test_empty_line(self):
        """Test parsing empty line."""
        tag = TagDefinitionParser.parse("")
        self.assertIsNone(tag)
    
    def test_example_tags(self):
        """Test example tags from specification."""
        # INT tag
        tag = TagDefinitionParser.parse("INT: 01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.")
        self.assertIsNotNone(tag)
        
        # VAR tag (simplified)
        tag = TagDefinitionParser.parse("VAR: ab.ba.+*")
        self.assertIsNotNone(tag)


if __name__ == "__main__":
    unittest.main()

