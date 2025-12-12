📝 PyEdit — A Terminal-Based Text Editor in Python

PyEdit is a lightweight, Vim-inspired terminal text editor written in Python using the curses library.
It supports multiple editing modes, cursor movement, file saving, and command-based controls — all inside your terminal window.

🚀 Features

✔️ Vim-like modes: Normal, Insert, Command

✔️ Open & edit existing files

✔️ Cursor navigation (arrows or HJKL)

✔️ Save, quit, force quit—just like Vim

✔️ Lightweight & terminal-native

✔️ Cross-platform support (with windows-curses on Windows)

📂 Project Structure
main.py              # Core text editor  
requirements.txt     # Dependencies  
README.md            # Documentation

🔧 Installation
🖥 Windows Users

Windows does NOT include curses by default, so install this first:

pip install windows-curses

🐧 Linux / macOS

No setup required — curses is already included with Python.

▶️ Running the Editor
Start the editor:
python main.py

Open a specific file:
python main.py notes.txt

⌨️ Keybindings
NORMAL Mode
Key	Action
i	Enter INSERT mode
x	Delete character under cursor
:	Enter COMMAND mode
q	Quit (press twice if unsaved changes)
Arrow keys / h j k l	Move cursor
INSERT Mode
Key	Action
ESC	Return to NORMAL mode
ENTER	Insert a new line
Backspace	Delete character
COMMAND Mode (:)
Command	Action
:w	Save file
:q	Quit if no unsaved changes
:q!	Force quit without saving
:wq	Save & quit
⚠️ Common Errors & Fixes
❌ ModuleNotFoundError: No module named '_curses'

This happens on Windows.
✔️ Fix:

pip install windows-curses

🤝 Contributing

Enhancements welcome! Ideas include:

Syntax highlighting

Undo/redo system

Search (/) functionality

File explorer sidebar
