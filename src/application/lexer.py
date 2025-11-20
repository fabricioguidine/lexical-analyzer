"""
Lexical Analyzer - main component for tokenizing input.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from typing import List, Optional, Tuple
from ..domain.tag import Tag


class LexicalAnalyzer:
    """Main lexical analyzer that tokenizes input using defined tags."""
    
    def __init__(self, tags: List[Tag]):
        self.tags = tags
        self.tag_order = {tag.name: i for i, tag in enumerate(tags)}
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into tags.
        Uses longest match strategy, then priority by definition order.
        Returns list of tag names.
        Raises ValueError if text cannot be fully tokenized.
        """
        tokens = []
        pos = 0
        
        while pos < len(text):
            best_match: Optional[Tuple[Tag, int]] = None
            
            # Try all tags and find the longest match
            for tag in self.tags:
                end_pos = tag.match(text, pos)
                if end_pos is not None:
                    length = end_pos - pos
                    if best_match is None or length > (best_match[1] - pos):
                        best_match = (tag, end_pos)
                    elif length == (best_match[1] - pos):
                        # Same length: prefer earlier defined tag
                        if self.tag_order[tag.name] < self.tag_order[best_match[0].name]:
                            best_match = (tag, end_pos)
            
            if best_match is None:
                raise ValueError(f"Cannot tokenize character at position {pos}: '{text[pos]}'")
            
            tag, end_pos = best_match
            tokens.append(tag.name)
            pos = end_pos
        
        return tokens
    
    def check_overlaps(self) -> List[Tuple[str, str]]:
        """
        Check for overlapping tag definitions.
        Returns list of (tag1, tag2) pairs that overlap.
        """
        overlaps = []
        
        for i, tag1 in enumerate(self.tags):
            for tag2 in self.tags[i + 1:]:
                # Simple overlap detection: check if they can match same strings
                # This is a simplified check - full overlap detection would require
                # checking language intersection
                if self._tags_overlap(tag1, tag2):
                    overlaps.append((tag1.name, tag2.name))
        
        return overlaps
    
    def _tags_overlap(self, tag1: Tag, tag2: Tag) -> bool:
        """
        Check if two tags might overlap.
        This is a simplified check - a full implementation would check
        if L(tag1) ∩ L(tag2) ≠ ∅
        """
        # For now, we'll do a simple heuristic: if both can match common patterns
        # This is not complete but works for common cases
        test_strings = [
            "a", "b", "0", "1", "aa", "ab", "01", "10",
            "a0", "0a", " ", "  ", "=", "=="
        ]
        
        for test_str in test_strings:
            match1 = tag1.match(test_str, 0)
            match2 = tag2.match(test_str, 0)
            if match1 is not None and match2 is not None:
                return True
        
        return False

