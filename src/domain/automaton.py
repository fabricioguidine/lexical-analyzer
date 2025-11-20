"""
Finite Automaton implementation for regular expression matching.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

from typing import Set, Dict, Optional, List
from collections import defaultdict


class State:
    """Represents a state in a finite automaton."""
    
    def __init__(self, state_id: int):
        self.id = state_id
        self.is_final = False
        self.transitions: Dict[str, Set['State']] = defaultdict(set)
        self.epsilon_transitions: Set['State'] = set()
    
    def add_transition(self, symbol: str, target: 'State'):
        """Add a transition on a symbol."""
        self.transitions[symbol].add(target)
    
    def add_epsilon_transition(self, target: 'State'):
        """Add an epsilon transition."""
        self.epsilon_transitions.add(target)
    
    def __repr__(self):
        return f"State({self.id}, final={self.is_final})"


class FiniteAutomaton:
    """Finite Automaton (NFA) for pattern matching."""
    
    def __init__(self):
        self.start_state: Optional[State] = None
        self.states: List[State] = []
        self.state_counter = 0
    
    def create_state(self) -> State:
        """Create a new state."""
        state = State(self.state_counter)
        self.state_counter += 1
        self.states.append(state)
        return state
    
    def epsilon_closure(self, states: Set[State]) -> Set[State]:
        """Compute epsilon closure of a set of states."""
        closure = set(states)
        stack = list(states)
        
        while stack:
            state = stack.pop()
            for target in state.epsilon_transitions:
                if target not in closure:
                    closure.add(target)
                    stack.append(target)
        
        return closure
    
    def match(self, text: str, start_pos: int = 0) -> Optional[int]:
        """
        Match the automaton against text starting at start_pos.
        Returns the end position if match succeeds, None otherwise.
        Uses longest match strategy.
        """
        if not self.start_state:
            return None
        
        current_states = self.epsilon_closure({self.start_state})
        longest_match = None
        
        # Check if we can accept empty string
        if any(state.is_final for state in current_states):
            longest_match = start_pos
        
        pos = start_pos
        while pos < len(text):
            symbol = text[pos]
            next_states = set()
            
            for state in current_states:
                # Check transitions on this symbol
                if symbol in state.transitions:
                    next_states.update(state.transitions[symbol])
                # Check transitions on any character (.)
                if '.' in state.transitions:
                    next_states.update(state.transitions['.'])
            
            if not next_states:
                break
            
            current_states = self.epsilon_closure(next_states)
            pos += 1
            
            # Check if we have a final state
            if any(state.is_final for state in current_states):
                longest_match = pos
        
        return longest_match
    
    def get_formal_definition(self) -> str:
        """Get formal definition of the automaton."""
        if not self.start_state:
            return "Empty automaton"
        
        lines = []
        lines.append(f"States: {[s.id for s in self.states]}")
        lines.append(f"Start state: {self.start_state.id}")
        final_states = [s.id for s in self.states if s.is_final]
        lines.append(f"Final states: {final_states}")
        lines.append("Transitions:")
        
        for state in self.states:
            for symbol, targets in state.transitions.items():
                for target in targets:
                    lines.append(f"  δ({state.id}, '{symbol}') = {target.id}")
            for target in state.epsilon_transitions:
                lines.append(f"  δ({state.id}, ε) = {target.id}")
        
        return "\n".join(lines)

