#!/usr/bin/env python3
"""
PyEdit - A simple terminal-based text editor written in Python

This editor implements Vim-like modes, cursor movement, and file operations
using the curses library for terminal handling.
"""

import curses
import os
import sys
import time
from enum import Enum, auto


class Mode(Enum):
    """Editor modes"""
    NORMAL = auto()
    INSERT = auto()
    COMMAND = auto()


class Editor:
    """Main editor class"""

    def __init__(self, filename=None):
        """Initialize the editor"""
        self.filename = filename
        self.lines = ['']
        self.cursor_x = 0
        self.cursor_y = 0
        self.offset_y = 0  # For scrolling
        self.offset_x = 0  # For horizontal scrolling
        self.mode = Mode.NORMAL
        self.status_message = ''
        self.status_time = 0
        self.command_buffer = ''
        self.dirty = False
        self.quit_times = 2  # Number of times to press q to quit

        # Load file if specified
        if filename and os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.lines = [line.rstrip('\n') for line in f.readlines()]
                if not self.lines:  # Handle empty files
                    self.lines = ['']
            except Exception as e:
                self.set_status_message(f"Error opening file: {e}")
        elif filename:
            self.set_status_message(f"New file: {filename}")

    def set_status_message(self, message):
        """Set a status message to be displayed on the status bar"""
        self.status_message = message
        self.status_time = time.time()

    def get_current_line(self):
        """Get the line at the current cursor position"""
        if 0 <= self.cursor_y < len(self.lines):
            return self.lines[self.cursor_y]
        return ''

    def save_file(self):
        """Save the current buffer to a file"""
        if not self.filename:
            self.filename = 'untitled.txt'
            self.set_status_message(f"Saving as {self.filename}")

        try:
            with open(self.filename, 'w') as f:
                f.write('\n'.join(self.lines))
            self.dirty = False
            self.set_status_message(f"Saved {len(self.lines)} lines to {self.filename}")
            return True
        except Exception as e:
            self.set_status_message(f"Error saving file: {e}")
            return False

    def insert_char(self, char):
        """Insert a character at the current cursor position"""
        current_line = self.get_current_line()
        new_line = current_line[:self.cursor_x] + char + current_line[self.cursor_x:]
        self.lines[self.cursor_y] = new_line
        self.cursor_x += 1
        self.dirty = True

    def insert_newline(self):
        """Insert a new line at the current cursor position"""
        current_line = self.get_current_line()
        
        # Split the line at the cursor
        left_part = current_line[:self.cursor_x]
        right_part = current_line[self.cursor_x:]
        
        # Update the current line and insert the new one
        self.lines[self.cursor_y] = left_part
        self.lines.insert(self.cursor_y + 1, right_part)
        
        # Move cursor to the beginning of the new line
        self.cursor_y += 1
        self.cursor_x = 0
        self.dirty = True

    def delete_char(self):
        """Delete the character at the current cursor position"""
        if self.cursor_y >= len(self.lines):
            return
            
        current_line = self.get_current_line()
        
        if self.cursor_x > 0:
            # Delete character before cursor
            new_line = current_line[:self.cursor_x-1] + current_line[self.cursor_x:]
            self.lines[self.cursor_y] = new_line
            self.cursor_x -= 1
            self.dirty = True
        elif self.cursor_y > 0:
            # At the beginning of a line, join with the previous line
            previous_line = self.lines[self.cursor_y - 1]
            self.cursor_x = len(previous_line)
            self.lines[self.cursor_y - 1] = previous_line + current_line
            self.lines.pop(self.cursor_y)
            self.cursor_y -= 1
            self.dirty = True

    def move_cursor(self, key):
        """Move the cursor based on key press"""
        if key == curses.KEY_UP or key == ord('k'):
            if self.cursor_y > 0:
                self.cursor_y -= 1
        elif key == curses.KEY_DOWN or key == ord('j'):
            if self.cursor_y < len(self.lines) - 1:
                self.cursor_y += 1
        elif key == curses.KEY_LEFT or key == ord('h'):
            if self.cursor_x > 0:
                self.cursor_x -= 1
            elif self.cursor_y > 0:
                # Move to end of previous line
                self.cursor_y -= 1
                self.cursor_x = len(self.lines[self.cursor_y])
        elif key == curses.KEY_RIGHT or key == ord('l'):
            current_line = self.get_current_line()
            if self.cursor_x < len(current_line):
                self.cursor_x += 1
            elif self.cursor_y < len(self.lines) - 1:
                # Move to beginning of next line
                self.cursor_y += 1
                self.cursor_x = 0

        # Make sure cursor_x is within the bounds of the current line
        current_line = self.get_current_line()
        if self.cursor_x > len(current_line):
            self.cursor_x = len(current_line)

    def process_keypress(self, key):
        """Process a keypress based on the current mode"""
        if self.mode == Mode.NORMAL:
            return self.process_normal_mode(key)
        elif self.mode == Mode.INSERT:
            return self.process_insert_mode(key)
        elif self.mode == Mode.COMMAND:
            return self.process_command_mode(key)
        return False

    def process_normal_mode(self, key):
        """Process a keypress in normal mode"""
        if key == ord('q'):
            if self.dirty and self.quit_times > 0:
                self.set_status_message(
                    f"WARNING! File has unsaved changes. "
                    f"Press q {self.quit_times} more time{'s' if self.quit_times > 1 else ''} to quit."
                )
                self.quit_times -= 1
                return False
            return True  # Quit
        elif key == ord('i'):
            self.mode = Mode.INSERT
            self.set_status_message("-- INSERT --")
        elif key == ord(':'):
            self.mode = Mode.COMMAND
            self.command_buffer = ''
            self.set_status_message(":")
        elif key == ord('x'):
            # Delete character under cursor
            current_line = self.get_current_line()
            if self.cursor_x < len(current_line):
                new_line = current_line[:self.cursor_x] + current_line[self.cursor_x+1:]
                self.lines[self.cursor_y] = new_line
                self.dirty = True
        else:
            self.move_cursor(key)
        
        self.quit_times = 2  # Reset quit counter
        return False

    def process_insert_mode(self, key):
        """Process a keypress in insert mode"""
        if key == 27:  # ESC key
            self.mode = Mode.NORMAL
            # Move cursor back one if at end of line
            if self.cursor_x > 0 and self.cursor_x == len(self.get_current_line()):
                self.cursor_x -= 1
            self.set_status_message("")
        elif key == curses.KEY_BACKSPACE or key == 127:
            self.delete_char()
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            self.insert_newline()
        elif key == curses.KEY_UP or key == curses.KEY_DOWN or \
             key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            self.move_cursor(key)
        elif 32 <= key <= 126:  # Printable ASCII
            self.insert_char(chr(key))
        return False

    def process_command_mode(self, key):
        """Process a keypress in command mode"""
        if key == 27:  # ESC key
            self.mode = Mode.NORMAL
            self.set_status_message("")
        elif key == curses.KEY_BACKSPACE or key == 127:
            if self.command_buffer:
                self.command_buffer = self.command_buffer[:-1]
                self.set_status_message(f":{self.command_buffer}")
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            # Process the command
            if self.command_buffer == 'w':
                self.save_file()
                self.mode = Mode.NORMAL
            elif self.command_buffer == 'q':
                if self.dirty:
                    self.set_status_message("File has unsaved changes. Use :q! to force quit.")
                    self.mode = Mode.NORMAL
                else:
                    return True  # Quit
            elif self.command_buffer == 'q!':
                return True  # Force quit
            elif self.command_buffer == 'wq':
                if self.save_file():
                    return True  # Save and quit
            else:
                self.set_status_message(f"Unknown command: {self.command_buffer}")
                
            self.mode = Mode.NORMAL
        elif 32 <= key <= 126:  # Printable ASCII
            self.command_buffer += chr(key)
            self.set_status_message(f":{self.command_buffer}")
        return False

    def scroll_if_needed(self, screen_height, screen_width):
        """Adjust scroll offsets if the cursor would be off-screen"""
        # Vertical scrolling
        if self.cursor_y < self.offset_y:
            self.offset_y = self.cursor_y
        if self.cursor_y >= self.offset_y + screen_height - 2:  # -2 for status lines
            self.offset_y = self.cursor_y - screen_height + 3

        # Horizontal scrolling
        if self.cursor_x < self.offset_x:
            self.offset_x = self.cursor_x
        if self.cursor_x >= self.offset_x + screen_width - 1:
            self.offset_x = self.cursor_x - screen_width + 2

    def draw_rows(self, screen, screen_height, screen_width):
        """Draw the editor rows"""
        for y in range(screen_height - 2):  # -2 for status lines
            file_row = y + self.offset_y
            
            if file_row >= len(self.lines):
                # Display tilde for empty lines past the end of the file
                if len(self.lines) == 0 and y == screen_height // 3:
                    welcome = f"PyEdit -- version 1.0"
                    padding = (screen_width - len(welcome)) // 2
                    if padding > 0:
                        screen.addstr(y, 0, "~")
                        screen.addstr(y, padding, welcome)
                    else:
                        screen.addstr(y, 0, welcome[:screen_width])
                else:
                    screen.addstr(y, 0, "~")
            else:
                # Draw content from the buffer
                line = self.lines[file_row]
                offset = self.offset_x
                
                if offset < len(line):
                    # Draw the visible part of the line
                    display = line[offset:offset + screen_width]
                    screen.addstr(y, 0, display)

    def draw_status_bar(self, screen, screen_height, screen_width):
        """Draw the status bar"""
        screen.attron(curses.A_REVERSE)
        
        status = f" {self.filename or '[No Name]'} - {len(self.lines)} lines "
        status += f"{'[modified]' if self.dirty else ''}"
        
        mode_str = ""
        if self.mode == Mode.INSERT:
            mode_str = "INSERT"
        elif self.mode == Mode.NORMAL:
            mode_str = "NORMAL"
        elif self.mode == Mode.COMMAND:
            mode_str = "COMMAND"
            
        position = f" {mode_str} | {self.cursor_y + 1}:{self.cursor_x + 1} "
        
        # Fill with spaces
        status = status + ' ' * (screen_width - len(status) - len(position)) + position
        
        # Truncate if necessary
        if len(status) > screen_width:
            status = status[:screen_width]
            
        screen.addstr(screen_height - 2, 0, status)
        screen.attroff(curses.A_REVERSE)

    def draw_message_bar(self, screen, screen_height, screen_width):
        """Draw the message bar"""
        screen.move(screen_height - 1, 0)
        screen.clrtoeol()
        
        if self.status_message and time.time() - self.status_time < 5:
            message = self.status_message
            if len(message) > screen_width:
                message = message[:screen_width]
            screen.addstr(screen_height - 1, 0, message)
        
        # For command mode, also show the command being typed
        if self.mode == Mode.COMMAND:
            screen.addstr(screen_height - 1, 0, f":{self.command_buffer}")

    def refresh_screen(self, screen):
        """Refresh the screen with the current state"""
        # Get screen dimensions
        screen_height, screen_width = screen.getmaxyx()
        
        # Adjust scroll if needed
        self.scroll_if_needed(screen_height, screen_width)
        
        # Hide cursor during refresh
        curses.curs_set(0)
        
        # Clear screen
        screen.clear()
        
        # Draw rows
        self.draw_rows(screen, screen_height, screen_width)
        
        # Draw status bar
        self.draw_status_bar(screen, screen_height, screen_width)
        
        # Draw message bar
        self.draw_message_bar(screen, screen_height, screen_width)
        
        # Position cursor
        cursor_y = self.cursor_y - self.offset_y
        cursor_x = self.cursor_x - self.offset_x
        
        # Make sure cursor is within bounds
        if 0 <= cursor_y < screen_height - 2 and 0 <= cursor_x < screen_width:
            screen.move(cursor_y, cursor_x)
        
        # Show cursor
        curses.curs_set(1)
        
        # Refresh
        screen.refresh()


def main(stdscr, filename=None):
    """Main function"""
    # Setup curses
    curses.raw()  # Raw mode
    curses.noecho()  # Don't echo keys
    stdscr.keypad(True)  # Enable keypad mode (for arrow keys)
    curses.start_color()  # Enable colors
    
    # Initialize the editor
    editor = Editor(filename)
    editor.set_status_message(
        "HELP: ESC = normal mode | i = insert mode | :w = save | :q = quit | :wq = save and quit"
    )
    
    # Main loop
    while True:
        editor.refresh_screen(stdscr)
        
        # Get user input
        key = stdscr.getch()
        
        # Process the key
        if editor.process_keypress(key):
            break  # Exit if process_keypress returns True


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        curses.wrapper(main, filename)
    except KeyboardInterrupt:
        sys.exit(0)