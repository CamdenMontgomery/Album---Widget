from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QSize
from enum import Enum, unique
from utils.basepath import BASE_PATH
from os import path

# Path for the close icon
CLOSE_ICON = path.join(BASE_PATH, "public", "icons", "close.svg")

# Enum for dialog types to ensure type safety and clarity
@unique
class DIALOG_TYPES(Enum):
    WARNING = 1  # For warning dialogs
    MESSAGE = 2  # For general informational message dialogs
    INPUT = 3  # For input dialog with text field


class Dialog(QtWidgets.QDialog):
    """
    A customizable dialog class that can display different types of dialogs like
    messages, warnings, and inputs. It includes a confirm and reject button.
    """

    def __init__(self, title: str, message: str, confirmText: str = "OK", rejectText: str = "Cancel", type: int = DIALOG_TYPES.MESSAGE):
        """
        Initializes the dialog with the given parameters.

        Args:
            title (str): The title of the dialog window.
            message (str): The message content to be displayed in the dialog.
            confirmText (str): The text for the confirm button (default is "OK").
            rejectText (str): The text for the reject button (default is "Cancel").
            type (int): The type of the dialog (uses DIALOG_TYPES enum, default is MESSAGE).
        """
        super().__init__()

        # Set window attributes and layout
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("DialogWindow")
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)

        # Background container for the dialog
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("DialogContainer")
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(30, 30, 30, 30)
        self.container_layout.setSpacing(30)
        self.window_layout.addWidget(self.container)

        # Title container
        self._title_widget = QtWidgets.QWidget()
        self._title_layout = QtWidgets.QHBoxLayout(self._title_widget)
        self._title_layout.setContentsMargins(0, 0, 0, 0)
        self._title_layout.setSpacing(8)

        # Title display
        self.title_display = QtWidgets.QLabel()
        self.title_display.setObjectName("DialogTitleDisplay")
        self.title_display.setText(title)
        self._title_layout.addWidget(self.title_display)

        # Spacer to push close button to the right
        self._title_layout.addStretch()

        # Close button
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setObjectName("DialogCloseButton")
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.reject)
        self._title_layout.addWidget(self.close_button)

        self.container_layout.addWidget(self._title_widget)

        # Message display (can be any type of message, warning, etc.)
        self.message_display = QtWidgets.QLabel()
        self.message_display.setObjectName("DialogMessageDisplay")
        self.message_display.setWordWrap(True)
        self.message_display.setText(message)
        self.message_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.container_layout.addWidget(self.message_display)

        # Text input field (only for INPUT type dialogs)
        if type == DIALOG_TYPES.INPUT:
            self.text_input = QtWidgets.QLineEdit()
            self.text_input.setObjectName("DialogTextInput")
            self.text_input.setPlaceholderText("Enter your input...")
            self.container_layout.addWidget(self.text_input)

        # Buttons container (Confirm and Reject)
        self._buttons_widget = QtWidgets.QWidget()
        self._buttons_layout = QtWidgets.QHBoxLayout(self._buttons_widget)
        self._buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._buttons_layout.setSpacing(8)

        # Spacer to align buttons to the right
        self._buttons_layout.addStretch()

        # Confirm button
        self.confirm_button = QtWidgets.QPushButton(confirmText)
        self.confirm_button.setObjectName("DialogConfirmButton")
        self.confirm_button.clicked.connect(self.onConfirm)
        self._buttons_layout.addWidget(self.confirm_button)

        # Reject button
        self.reject_button = QtWidgets.QPushButton(rejectText)
        self.reject_button.setObjectName("DialogRejectButton")
        self.reject_button.clicked.connect(self.onReject)
        self._buttons_layout.addWidget(self.reject_button)

        self.container_layout.addWidget(self._buttons_widget)

        # Window flags and basic sizing
        self.setModal(True)
        self.resize(400, 120)

    def onConfirm(self):
        """
        Handle the confirm button click.
        For INPUT dialogs, store the text entered by the user on accept().
        """
        if hasattr(self, "text_input"):
            self._result_text = self.text_input.text()
        self.accept()

    def onReject(self):
        """Handle reject/close actions."""
        self._result_text = None
        self.reject()

    def getResultingText(self) -> str | None:
        """
        Return the text entered by the user (if any) after closing the dialog.

        Returns:
            str or None: The text inputted by the user, or None if none was entered.
        """
        return getattr(self, "_result_text", None)
