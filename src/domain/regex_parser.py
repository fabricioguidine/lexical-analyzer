"""
Regular Expression Parser for Reverse Polish Notation.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from typing import List, Optional
from .automaton import FiniteAutomaton, State


class RegexParser:
    """Parser for regular expressions in reverse Polish notation."""
    
    # Escape sequences mapping
    ESCAPE_SEQUENCES = {
        'n': '\n',
        '\\': '\\',
        '*': '*',
        '.': '.',
        '+': '+',
        'l': ''  # lambda (empty string)
    }
    
    def __init__(self):
        self.alphabet = set(chr(i) for i in range(32, 127))  # ASCII 32-126
    
    def parse_escape_sequence(self, expr: str, pos: int) -> tuple[str, int]:
        """
        Parse an escape sequence starting at pos.
        Returns (parsed_char, new_position).
        """
        if pos >= len(expr) - 1:
            raise ValueError("Incomplete escape sequence")
        
        esc_char = expr[pos + 1]
        if esc_char in self.ESCAPE_SEQUENCES:
            return self.ESCAPE_SEQUENCES[esc_char], pos + 2
        else:
            # Unknown escape, treat as literal backslash + char
            return expr[pos], pos + 1
    
    def parse_character(self, expr: str, pos: int) -> tuple[str, int]:
        """
        Parse a single character (possibly escaped).
        Returns (char, new_position).
        """
        if pos >= len(expr):
            raise ValueError("Unexpected end of expression")
        
        if expr[pos] == '\\':
            return self.parse_escape_sequence(expr, pos)
        else:
            return expr[pos], pos + 1
    
    def build_automaton(self, expr: str) -> FiniteAutomaton:
        """
        Build a finite automaton from a regular expression in RPN.
        
        Operators:
        - + : union (e1 + e2)
        - . : concatenation (e1 . e2)
        - * : Kleene star (e*)
        - a : character (a ∈ Σ)
        - λ : empty string
        - ∅ : empty language
        """
        if not expr:
            # Empty expression = empty language
            return self._empty_language()
        
        stack: List[FiniteAutomaton] = []
        pos = 0
        
        while pos < len(expr):
            char, pos = self.parse_character(expr, pos)
            
            if char == '+':  # Union
                if len(stack) < 2:
                    raise ValueError("Not enough operands for union operator")
                b = stack.pop()
                a = stack.pop()
                result = self._union(a, b)
                stack.append(result)
            
            elif char == '.':  # Concatenation
                if len(stack) < 2:
                    raise ValueError("Not enough operands for concatenation operator")
                b = stack.pop()
                a = stack.pop()
                result = self._concatenation(a, b)
                stack.append(result)
            
            elif char == '*':  # Kleene star
                if len(stack) < 1:
                    raise ValueError("Not enough operands for Kleene star operator")
                a = stack.pop()
                result = self._kleene_star(a)
                stack.append(result)
            
            elif char == '':  # Lambda (empty string)
                stack.append(self._empty_string())
            
            else:  # Character
                stack.append(self._single_character(char))
        
        if len(stack) != 1:
            raise ValueError(f"Invalid expression: {len(stack)} automata left on stack")
        
        return stack[0]
    
    def _single_character(self, char: str) -> FiniteAutomaton:
        """Create automaton for a single character."""
        automaton = FiniteAutomaton()
        start = automaton.create_state()
        final = automaton.create_state()
        final.is_final = True
        
        automaton.start_state = start
        start.add_transition(char, final)
        
        return automaton
    
    def _empty_string(self) -> FiniteAutomaton:
        """Create automaton for empty string (lambda)."""
        automaton = FiniteAutomaton()
        state = automaton.create_state()
        state.is_final = True
        automaton.start_state = state
        return automaton
    
    def _empty_language(self) -> FiniteAutomaton:
        """Create automaton for empty language."""
        automaton = FiniteAutomaton()
        state = automaton.create_state()
        automaton.start_state = state
        # No final states = empty language
        return automaton
    
    def _union(self, a: FiniteAutomaton, b: FiniteAutomaton) -> FiniteAutomaton:
        """Create automaton for union (a + b)."""
        automaton = FiniteAutomaton()
        new_start = automaton.create_state()
        
        # Copy automaton a
        a_state_map = {}
        for old_state in a.states:
            new_state = automaton.create_state()
            new_state.is_final = old_state.is_final
            a_state_map[old_state] = new_state
        
        # Copy automaton b
        b_state_map = {}
        for old_state in b.states:
            new_state = automaton.create_state()
            new_state.is_final = old_state.is_final
            b_state_map[old_state] = new_state
        
        # Copy transitions from a
        for old_state, new_state in a_state_map.items():
            for symbol, targets in old_state.transitions.items():
                for target in targets:
                    new_state.add_transition(symbol, a_state_map[target])
            for target in old_state.epsilon_transitions:
                new_state.add_epsilon_transition(a_state_map[target])
        
        # Copy transitions from b
        for old_state, new_state in b_state_map.items():
            for symbol, targets in old_state.transitions.items():
                for target in targets:
                    new_state.add_transition(symbol, b_state_map[target])
            for target in old_state.epsilon_transitions:
                new_state.add_epsilon_transition(b_state_map[target])
        
        # Add epsilon transitions from new start to both old starts
        automaton.start_state = new_start
        new_start.add_epsilon_transition(a_state_map[a.start_state])
        new_start.add_epsilon_transition(b_state_map[b.start_state])
        
        return automaton
    
    def _concatenation(self, a: FiniteAutomaton, b: FiniteAutomaton) -> FiniteAutomaton:
        """Create automaton for concatenation (a . b)."""
        automaton = FiniteAutomaton()
        
        # Copy automaton a
        a_state_map = {}
        for old_state in a.states:
            new_state = automaton.create_state()
            new_state.is_final = False  # Will be set later
            a_state_map[old_state] = new_state
        
        # Copy automaton b
        b_state_map = {}
        for old_state in b.states:
            new_state = automaton.create_state()
            new_state.is_final = old_state.is_final
            b_state_map[old_state] = new_state
        
        # Copy transitions from a
        for old_state, new_state in a_state_map.items():
            for symbol, targets in old_state.transitions.items():
                for target in targets:
                    new_state.add_transition(symbol, a_state_map[target])
            for target in old_state.epsilon_transitions:
                new_state.add_epsilon_transition(a_state_map[target])
        
        # Copy transitions from b
        for old_state, new_state in b_state_map.items():
            for symbol, targets in old_state.transitions.items():
                for target in targets:
                    new_state.add_transition(symbol, b_state_map[target])
            for target in old_state.epsilon_transitions:
                new_state.add_epsilon_transition(b_state_map[target])
        
        # Connect final states of a to start of b
        for old_state in a.states:
            if old_state.is_final:
                a_state_map[old_state].add_epsilon_transition(b_state_map[b.start_state])
        
        automaton.start_state = a_state_map[a.start_state]
        
        return automaton
    
    def _kleene_star(self, a: FiniteAutomaton) -> FiniteAutomaton:
        """Create automaton for Kleene star (a*)."""
        automaton = FiniteAutomaton()
        new_start = automaton.create_state()
        new_final = automaton.create_state()
        new_final.is_final = True
        
        # Copy automaton a
        a_state_map = {}
        for old_state in a.states:
            new_state = automaton.create_state()
            new_state.is_final = False
            a_state_map[old_state] = new_state
        
        # Copy transitions from a
        for old_state, new_state in a_state_map.items():
            for symbol, targets in old_state.transitions.items():
                for target in targets:
                    new_state.add_transition(symbol, a_state_map[target])
            for target in old_state.epsilon_transitions:
                new_state.add_epsilon_transition(a_state_map[target])
        
        # Epsilon from new start to a's start and to new final
        new_start.add_epsilon_transition(a_state_map[a.start_state])
        new_start.add_epsilon_transition(new_final)
        
        # Epsilon from a's final states to a's start and to new final
        for old_state in a.states:
            if old_state.is_final:
                a_state_map[old_state].add_epsilon_transition(a_state_map[a.start_state])
                a_state_map[old_state].add_epsilon_transition(new_final)
        
        automaton.start_state = new_start
        
        return automaton

