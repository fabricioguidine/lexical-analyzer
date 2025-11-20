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
        self.assertIsNotNone(self.handler.lexer)
    
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
        self.assertEqual(tag.expression, "a*")
    
    def test_parse_invalid_tag_line(self):
        """Test parsing invalid tag line."""
        tag = self.handler.parse_tag_line("INVALID")
        self.assertIsNone(tag)
    
    def test_save_and_load_tags(self):
        """Test saving and loading tags."""
        tag1 = Tag("VAR", "a*")
        tag2 = Tag("INT", "01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.")
        self.handler.add_tag(tag1)
        self.handler.add_tag(tag2)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            self.handler.save_tags_to_file(filepath)
            
            # Create new handler and load
            new_handler = CommandHandler()
            valid_tags, invalid = new_handler.load_tags_from_file(filepath)
            self.assertEqual(len(valid_tags), 2)
            self.assertEqual(valid_tags[0].name, "VAR")
            self.assertEqual(valid_tags[1].name, "INT")
        finally:
            os.unlink(filepath)
    
    def test_process_input(self):
        """Test processing input."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        result = self.handler.process_input("aaa")
        self.assertEqual(result, "VAR")
    
    def test_process_input_multiple_tokens(self):
        """Test processing input with multiple tokens."""
        var_tag = Tag("VAR", "a*")
        space_tag = Tag("SPACE", " *")
        self.handler.add_tag(var_tag)
        self.handler.add_tag(space_tag)
        result = self.handler.process_input("aaa   ")
        self.assertEqual(result, "VAR SPACE")
    
    def test_process_input_no_tags(self):
        """Test processing input without tags."""
        with self.assertRaises(ValueError):
            self.handler.process_input("test")
    
    def test_list_tags(self):
        """Test listing tags."""
        tag1 = Tag("VAR", "a*")
        tag2 = Tag("INT", "01+2+3+4+5+6+7+8+9+01+2+3+4+5+6+7+8+9+*.")
        self.handler.add_tag(tag1)
        self.handler.add_tag(tag2)
        tags = self.handler.list_tags()
        self.assertEqual(len(tags), 2)
        self.assertIn("VAR: a*", tags)
        self.assertIn("INT:", tags[1])
    
    def test_list_automata(self):
        """Test listing automata."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        automata = self.handler.list_automata()
        self.assertEqual(len(automata), 1)
        self.assertIn("VAR", automata[0])
    
    def test_set_output_file(self):
        """Test setting output file."""
        self.handler.set_output_file("output.txt")
        self.assertEqual(self.handler.output_file, "output.txt")
    
    def test_write_output(self):
        """Test writing output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            filepath = f.name
        
        try:
            self.handler.set_output_file(filepath)
            self.handler.write_output("test output")
            
            with open(filepath, 'r') as f:
                content = f.read()
            self.assertIn("test output", content)
        finally:
            os.unlink(filepath)
    
    def test_check_overlaps(self):
        """Test checking overlaps."""
        tag1 = Tag("TAG1", "a*")
        tag2 = Tag("TAG2", "a*")
        self.handler.add_tag(tag1)
        self.handler.add_tag(tag2)
        overlaps = self.handler.check_overlaps()
        # Should return list of tuples
        self.assertIsInstance(overlaps, list)
    
    def test_load_tags_from_nonexistent_file(self):
        """Test loading tags from nonexistent file."""
        with self.assertRaises(FileNotFoundError):
            self.handler.load_tags_from_file("nonexistent.txt")
    
    def test_process_file(self):
        """Test processing a file."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("aaa")
            filepath = f.name
        
        try:
            result = self.handler.process_file(filepath)
            self.assertEqual(result, "VAR")
        finally:
            os.unlink(filepath)
    
    def test_process_file_nonexistent(self):
        """Test processing nonexistent file."""
        tag = Tag("VAR", "a*")
        self.handler.add_tag(tag)
        
        with self.assertRaises(FileNotFoundError):
            self.handler.process_file("nonexistent.txt")


if __name__ == "__main__":
    unittest.main()
