from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize, QPoint, Qt
from utils.basepath import BASE_PATH
from os import path

# Define the path to the grab handle icon
ICON_PATH = path.join(BASE_PATH, "public", "icons", "grab_handle.svg")

class GrabHandle(QtWidgets.QPushButton):
    """
    A custom QPushButton used as a grab handle to allow the user to drag the parent widget.
    """
    def __init__(self, parent: QtWidgets.QWidget):
        """
        Initializes the GrabHandle button and sets up its properties.

        Args:
            parent (QtWidgets.QWidget): The parent widget that will be moved when dragged.
        """
        super().__init__()

        self.grabbing = False  # Indicates whether the user is currently dragging the widget
        self.offset = QPoint(0, 0)  # The offset between the cursor and the widget's position
        self.parent_widget = parent  # The parent widget to be dragged

        self.setObjectName("GrabHandle")
        self.setCursor(Qt.CursorShape.OpenHandCursor)  # Set the cursor to an open hand (indicating draggable)
        self.setIcon(QtGui.QIcon(ICON_PATH))  # Set the icon of the button
        self.setIconSize(QSize(24, 24))  # Set the icon size to 24x24 pixels

    def mouseMoveEvent(self, event):
        """
        Moves the parent widget when the user drags the grab handle.

        Args:
            event (QMouseEvent): The mouse event triggered during dragging.
        """
        if self.grabbing:
            # Get the current position of the cursor on the screen
            cursor_pos = QtGui.QCursor.pos()
            # Move the parent widget by the offset calculated during mousePressEvent
            self.parent_widget.move(cursor_pos - self.offset)

    def mousePressEvent(self, event):
        """
        Initiates the dragging action when the user presses the mouse button on the grab handle.

        Args:
            event (QMouseEvent): The mouse event triggered during mouse press.
        """
        # Change the cursor to a closed hand (indicating dragging is active)
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        # Calculate the offset between the cursor and the button's position
        grabbed_at = event.pos()
        self.offset = grabbed_at + self.pos()
        self.grabbing = True  # Set grabbing flag to True

    def mouseReleaseEvent(self, event):
        """
        Stops the dragging action when the user releases the mouse button.

        Args:
            event (QMouseEvent): The mouse event triggered during mouse release.
        """
        # Change the cursor back to the open hand (indicating drag is no longer active)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.grabbing = False  # Set grabbing flag to False
