# --- PySide6 Imports ---
from PySide6 import QtWidgets
from PySide6.QtGui import Qt

class Separator(QtWidgets.QWidget):
    """A simple separator widget with a styled background."""

    def __init__(self):
        """
        Initialize the Separator widget.
        
        Sets the object name for styling and enables the widget to 
        have a styled background.
        """
        super().__init__()

        # Set object name for styling
        self.setObjectName("Separator")

        # Enable background styling
        self.setAttribute(Qt.WA_StyledBackground, True)
