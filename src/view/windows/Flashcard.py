# --- Standard Library ---
import os
from os import path

# --- PySide6 ---
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSize

# --- Project Imports ---
from utils.cleaning import cleanFlashcardContent
from view.components.GrabHandle import GrabHandle
from utils.basepath import BASE_PATH


# --- Constants ---
CLOSE_ICON = path.join(BASE_PATH, "public", "icons", "close.svg")
CONFIRM_ICON = path.join(BASE_PATH, "public", "icons", "check.svg")


class Flashcard(QtWidgets.QWidget):
    """A widget for creating and saving flashcards, with a question and answer."""

    def __init__(self, path: str):
        """
        Initialize the Flashcard widget.

        Args:
            path (str): Directory where flashcards will be saved.
        """
        super().__init__()
        self.save_path = path

        # --- Window Setup ---
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )
        self.setObjectName("FlashcardWindow")

        # Root layout
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)

        # --- Header Section ---
        self.header = QtWidgets.QWidget()
        self.header.setObjectName("FlashcardHeader")

        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(20, 20, 20, 20)

        # Flashcard label
        self.new_flashcard_label = QtWidgets.QLabel("New Flashcard")
        self.new_flashcard_label.setObjectName("FlashcardLabel")
        self.header_layout.addWidget(self.new_flashcard_label)

        # Confirm button (saves flashcard)
        self.confirm_button = QtWidgets.QPushButton()
        self.confirm_button.setIcon(QtGui.QIcon(CONFIRM_ICON))
        self.confirm_button.setIconSize(QSize(24, 24))
        self.confirm_button.setObjectName("FlashcardConfirmButton")
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(self.saveFlashcard)
        self.header_layout.addWidget(self.confirm_button)

        # Close button (discards flashcard)
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setObjectName("FlashcardCloseButton")
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close)
        self.header_layout.addWidget(self.close_button)

        # Grab handle (for dragging the flashcard)
        self.grab_handle = GrabHandle(self)
        self.header_layout.addWidget(self.grab_handle)

        # Add header to layout
        self.window_layout.addWidget(self.header)

        # --- Body Section ---
        self.body = QtWidgets.QWidget()
        self.body.setObjectName("FlashcardBody")

        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(20, 20, 20, 20)
        self.body_layout.setSpacing(20)

        # Question text area
        self.question_text = QtWidgets.QTextEdit()
        self.question_text.setPlaceholderText("Question...")
        self.question_text.setObjectName("FlashcardTextArea")
        self.body_layout.addWidget(self.question_text)

        # Answer text area
        self.answer_text = QtWidgets.QTextEdit()
        self.answer_text.setPlaceholderText("Answer...")
        self.answer_text.setObjectName("FlashcardTextArea")
        self.body_layout.addWidget(self.answer_text)

        # Add body to main layout
        self.window_layout.addWidget(self.body)

    def saveFlashcard(self):
        """
        Save the question and answer of the flashcard to a text file.

        The flashcard is appended to a file named 'export.quizlet.txt' in the provided save path.
        Each flashcard is saved with the question followed by the answer, separated by a tab.
        """
        question = cleanFlashcardContent(self.question_text.toPlainText()).strip()
        answer = cleanFlashcardContent(self.answer_text.toPlainText()).strip()

        if not question or not answer:
            self.close()
            return  # Don't save if either question or answer is empty

        # Filepath to save flashcards
        file_name = "export.quizlet.txt"
        file_path = os.path.join(self.save_path, file_name)

        # Append the flashcard to the file
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"\n{question}\t{answer}")

        # Close the flashcard window
        self.close()
