"""
Command-line interface for the lexical analyzer.

Authors: Fabrício de Sousa Guidine, Débora Izabel Duarte, Guilherme, Juarez
"""

import sys
from ..application.command_handler import CommandHandler


class CLI:
    """Interactive command-line interface."""
    
    def __init__(self):
        self.handler = CommandHandler()
        self.running = True
    
    def run(self):
        """Start the interactive interpreter."""
        while self.running:
            try:
                line = input().strip()
                if not line:
                    continue
                
                self.process_line(line)
            except EOFError:
                self.running = False
            except KeyboardInterrupt:
                print("\n[INFO] Program interrupted by user")
                self.running = False
    
    def process_line(self, line: str):
        """Process a single line of input."""
        # Check if it's a command (starts with :)
        if line.startswith(':'):
            self.handle_command(line)
        else:
            # Try to parse as tag definition
            self.handle_tag_definition(line)
    
    def handle_command(self, line: str):
        """Handle a command."""
        parts = line.split(None, 1)
        command = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        
        if command == ':q':
            self.running = False
            print("[INFO] Exiting program")
        
        elif command == ':p':
            if not arg:
                print("[ERROR] Command :p requires an argument")
                return
            try:
                result = self.handler.process_input(arg)
                self.handler.write_output(result)
            except ValueError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        elif command == ':d':
            if not arg:
                print("[ERROR] Command :d requires a file path")
                return
            try:
                result = self.handler.process_file(arg)
                self.handler.write_output(result)
            except FileNotFoundError as e:
                print(f"[ERROR] {e}")
            except ValueError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        elif command == ':c':
            if not arg:
                print("[ERROR] Command :c requires a file path")
                return
            try:
                valid_tags, invalid_lines = self.handler.load_tags_from_file(arg)
                print(f"[INFO] Loaded {len(valid_tags)} valid tag(s)")
                for tag in valid_tags:
                    print(f"[INFO] Tag '{tag.name}' loaded successfully")
                if invalid_lines:
                    for line in invalid_lines:
                        print(f"[WARNING] {line}")
            except FileNotFoundError as e:
                print(f"[ERROR] {e}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        elif command == ':o':
            if not arg:
                print("[ERROR] Command :o requires a file path")
                return
            try:
                self.handler.set_output_file(arg)
                print(f"[INFO] Output file set to: {arg}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        elif command == ':l':
            tags = self.handler.list_tags()
            if tags:
                print("[INFO] Tag definitions:")
                for tag_def in tags:
                    print(f"  {tag_def}")
            else:
                print("[INFO] No tags defined")
        
        elif command == ':a':
            automata = self.handler.list_automata()
            if automata:
                print("[INFO] Automata definitions:")
                for i, automaton_def in enumerate(automata):
                    if i > 0:
                        print()
                    print(automaton_def)
            else:
                print("[INFO] No automata defined")
        
        elif command == ':s':
            if not arg:
                print("[ERROR] Command :s requires a file path")
                return
            try:
                self.handler.save_tags_to_file(arg)
                print(f"[INFO] Tags saved to: {arg}")
            except Exception as e:
                print(f"[ERROR] {e}")
        
        else:
            print(f"[ERROR] Unknown command: {command}")
    
    def handle_tag_definition(self, line: str):
        """Handle a tag definition line."""
        tag = self.handler.parse_tag_line(line)
        if tag:
            if self.handler.add_tag(tag):
                print(f"[INFO] Tag '{tag.name}' defined successfully")
                # Check for overlaps
                overlaps = self.handler.check_overlaps()
                for tag1, tag2 in overlaps:
                    print(f"[WARNING] Overlap in tag definitions: {tag1} and {tag2}")
            else:
                print(f"[ERROR] Tag name '{tag.name}' already exists")
        else:
            print(f"[ERROR] Invalid tag definition: {line}")


def main():
    """Main entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()

