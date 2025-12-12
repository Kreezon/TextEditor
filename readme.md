# 📝 PyEdit — A Terminal-Based Text Editor in Python

PyEdit is a lightweight, Vim-style text editor written entirely in Python using the `curses` library.  
It supports basic editing features such as insert mode, navigation, saving files, and command mode.

---

## 🚀 Features

- ✔️ **Vim-like modes**
  - NORMAL mode
  - INSERT mode
  - COMMAND mode (`:w`, `:q`, `:wq`, `:q!`)
- ✔️ Supports opening & editing existing files
- ✔️ Simple UI with a status bar
- ✔️ Cursor-based navigation
- ✔️ Save files directly from inside the editor
- ✔️ Lightweight — only uses Python + curses

---

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
ENTER	New line
Backspace	Delete character
COMMAND Mode (:)
Command	Action
:w	Save file
:q	Quit if no unsaved changes
:q!	Force quit without saving
:wq	Save & quit


