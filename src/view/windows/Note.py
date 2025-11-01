# --- Standard Library ---
import os
from os import path

# --- PySide6 ---
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize

# --- Project Imports ---
from view.components.GrabHandle import GrabHandle
from utils.basepath import BASE_PATH


# --- Constants ---
CLOSE_ICON = path.join(BASE_PATH, "public", "icons", "close.svg")
CONFIRM_ICON = path.join(BASE_PATH, "public", "icons", "check.svg")


class Note(QtWidgets.QWidget):
    """A floating sticky note widget that allows the user to write,
    save, and close notes directly from the desktop interface."""

    def __init__(self, path: str):
        """
        Initialize the Note widget.

        Args:
            path (str): Directory where sticky notes will be saved.
        """
        super().__init__()
        self.save_path = path

        # --- Window setup ---
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setObjectName("NoteWindow")

        # Root layout
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)

        # --- Header Section ---
        self.header = QtWidgets.QWidget()
        self.header.setObjectName("NoteHeader")

        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(20, 20, 20, 20)

        # Label
        self.new_note_label = QtWidgets.QLabel("New Note")
        self.new_note_label.setObjectName("NoteLabel")
        self.header_layout.addWidget(self.new_note_label)

        # Confirm button (saves note)
        self.confirm_button = QtWidgets.QPushButton()
        self.confirm_button.setIcon(QtGui.QIcon(CONFIRM_ICON))
        self.confirm_button.setIconSize(QSize(24, 24))
        self.confirm_button.setObjectName("NoteConfirmButton")
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(self.saveNote)
        self.header_layout.addWidget(self.confirm_button)

        # Close button (discards note)
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setObjectName("NoteCloseButton")
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close)
        self.header_layout.addWidget(self.close_button)

        # Grab handle (for dragging the note around)
        self.grab_handle = GrabHandle(self)
        self.header_layout.addWidget(self.grab_handle)

        # Add header to layout
        self.window_layout.addWidget(self.header)

        # --- Body Section ---
        self.body = QtWidgets.QWidget()
        self.body.setObjectName("NoteBody")

        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(20, 20, 20, 20)

        # Text area for note content
        self.text_area = QtWidgets.QPlainTextEdit()
        self.text_area.setPlaceholderText("Content...")
        self.text_area.setObjectName("NoteTextArea")
        self.body_layout.addWidget(self.text_area)

        # Add body to main layout
        self.window_layout.addWidget(self.body)

    def saveNote(self):
        """
        Save the contents of the note to a text file.

        The note is saved in the 'Sticky Notes' subdirectory of the provided save path.
        The filename is derived from the first few characters of the note content.
        """
        contents = self.text_area.toPlainText().strip()
        if not contents:
            self.close()
            return  # Don't save empty notes

        # Generate a short filename from the first 10 characters
        snippet = contents[:10].replace("\n", " ").strip()
        filename = f"{snippet or 'Untitled'}.sticky.txt"

        # Ensure 'Sticky Notes' directory exists
        notes_dir = os.path.join(self.save_path, "Sticky Notes")
        os.makedirs(notes_dir, exist_ok=True)

        # Full file path
        file_path = os.path.join(notes_dir, filename)

        # Save content to text file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(contents)

        # Close the note window
        self.close()
