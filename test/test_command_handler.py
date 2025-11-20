"""
Tests for command handler.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

import unittest
import tempfile
import os
from src.application.command_handler import CommandHandler
from src.domain.tag import Tag


class TestCommandHandler(unittest.TestCase):
    """Test cases for CommandHandler."""
    
    def setUp(self):
        self.handler = CommandHandler()
    
    def test_add_tag(self):
        """Test adding a tag."""
        tag = Tag("VAR", "a*")
        result = self.handler.add_tag(tag)
        self.assertTrue(result)
        self.assertEqual(len(self.handler.tags), 1)
    
    def test_duplicate_tag(self):
        """Test adding duplicate tag."""
        tag1 = Tag("VAR", "a*")
        tag2 = Tag("VAR", "b*")
        self.handler.add_tag(tag1)
        result = self.handler.add_tag(tag2)
        self.assertFalse(result)
        self.assertEqual(len(self.handler.tags), 1)
    
    def test_parse_tag_line(self):
        """Test parsing tag line."""
        tag = self.handler.parse_tag_line("VAR: a*")
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "VAR")
    
    def test_save_and_load_tags(self):
        """Test saving and loading tags."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            self.handler.save_tags_to_file(filepath)
            
            # Create new handler and load
            new_handler = CommandHandler()
            valid_tags, invalid = new_handler.load_tags_from_file(filepath)
            self.assertEqual(len(valid_tags), 1)
            self.assertEqual(valid_tags[0].name, "VAR")
        finally:
            os.unlink(filepath)
    
    def test_process_input(self):
        """Test processing input."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        result = self.handler.process_input("aaa")
        self.assertEqual(result, "VAR")
    
    def test_list_tags(self):
        """Test listing tags."""
        tag1 = Tag("VAR", "a*")
        tag2 = Tag("INT", "01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.")
        self.handler.add_tag(tag1)
        self.handler.add_tag(tag2)
        tags = self.handler.list_tags()
        self.assertEqual(len(tags), 2)


if __name__ == "__main__":
    unittest.main()

