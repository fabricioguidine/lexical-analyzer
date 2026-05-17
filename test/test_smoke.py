"""Smoke tests: verify core units import and basic tokenization works end-to-end."""

from __future__ import annotations

import pytest

from src.application.lexer import LexicalAnalyzer
from src.domain.regex_parser import RegexParser
from src.domain.tag import Tag, TagDefinitionParser


def test_imports_core_modules() -> None:
    """All core modules import and exported classes are usable."""
    assert LexicalAnalyzer is not None
    assert Tag is not None
    assert TagDefinitionParser is not None
    assert RegexParser is not None


def test_tag_instantiation_builds_automaton() -> None:
    """Instantiating a Tag with a valid RPN expression builds an automaton."""
    tag = Tag("EQUALS", "=")
    assert tag.name == "EQUALS"
    assert tag.expression == "="
    assert tag.automaton is not None


def test_lexer_tokenizes_single_char_tag() -> None:
    """Lexer tokenizes a string of equals signs into successive EQUALS tokens."""
    lexer = LexicalAnalyzer([Tag("EQUALS", "=")])
    tokens = lexer.tokenize("===")
    assert tokens == ["EQUALS", "EQUALS", "EQUALS"]


def test_lexer_rejects_unrecognized_input() -> None:
    """Lexer raises ValueError when input contains no matching tag."""
    lexer = LexicalAnalyzer([Tag("EQUALS", "=")])
    with pytest.raises(ValueError):
        lexer.tokenize("=x=")


def test_tag_definition_parser_round_trip() -> None:
    """Parser accepts well-formed 'NAME: EXPR' lines and rejects malformed ones."""
    good = TagDefinitionParser.parse("EQUALS: =")
    assert good is not None
    assert good.name == "EQUALS"
    assert good.expression == "="

    # Missing space after colon -> rejected
    assert TagDefinitionParser.parse("EQUALS:=") is None
    # Space before colon -> rejected
    assert TagDefinitionParser.parse("EQUALS : =") is None
    # Empty line -> rejected
    assert TagDefinitionParser.parse("") is None


def test_lexer_longest_match_priority() -> None:
    """Lexer prefers the longest match across competing tags."""
    short_tag = Tag("SHORT", "a")
    long_tag = Tag("LONG", "aa.")  # RPN for 'aa'
    lexer = LexicalAnalyzer([short_tag, long_tag])
    assert lexer.tokenize("aa") == ["LONG"]
