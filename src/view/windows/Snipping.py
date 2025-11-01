from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime


# Constants for overlay and selection colors
OVERLAY_COLOR = QColor(255, 255, 255, 100)  # Semi-transparent white overlay
SELECTION_COLOR = QColor(255, 127, 80, 100)  # Coral-colored selection area


class SnippingOverlay(QtWidgets.QWidget):

    def __init__(self, path: str):
        super().__init__()

        # Path to save the screenshot to
        self.save_path = path

        # Coordinates for the selection rectangle
        self.snip_top_left = QPoint(0, 0)
        self.snip_bottom_right = QPoint(0, 0)

        # Window setup: frameless, transparent, and always on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)

        # Capture the current screen as a static background
        screen = QApplication.instance().primaryScreen()
        self.freeze_screen = screen.grabWindow(0)

    def paintEvent(self, event: QtGui.QPaintEvent):
        """Draw the frozen background, transparent overlay, and selection rectangle."""
        painter = QPainter(self)

        # Draw the frozen screen (static background)
        painter.drawPixmap(0, 0, self.freeze_screen)
        painter.fillRect(self.rect(), OVERLAY_COLOR)  # Apply the semi-transparent overlay

        # Create and draw the selection rectangle (if any)
        selection_rect = QRect(self.snip_top_left, self.snip_bottom_right)

        # Set up the selection box (coral-colored dashed line)
        pen = QPen(SELECTION_COLOR)
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)

        # Draw the selection area with filled color and an outline
        painter.fillRect(selection_rect, SELECTION_COLOR)
        painter.drawRect(selection_rect.normalized())  # Draw the rectangle outline

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        """Start the selection process: Store the initial position."""
        self.snip_top_left = event.pos()  # The point where the mouse was pressed

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        """Update the selection rectangle as the mouse moves."""
        if self.snip_top_left != QPoint(0, 0):  # Ensure a start point is defined
            self.snip_bottom_right = event.pos()  # Update the bottom-right corner
            self.update()  # Redraw the widget to show the updated selection

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Finalize the selection and save the screenshot."""
        self.snip_bottom_right = event.pos()  # Finalize the selection
        self.save_snip()  # Save the screenshot
        self.close()  # Close the snipping overlay after selection

    def save_snip(self):
        """Crop the screen to the selected area and save it as a PNG."""
        # Normalize the selection rectangle to ensure valid dimensions
        selection_rect = QRect(self.snip_top_left, self.snip_bottom_right).normalized()

        # Crop the selected region from the screen
        snippet = self.freeze_screen.copy(selection_rect)

        # Generate a timestamped filename for the saved image
        now = datetime.now()
        timestamp = now.strftime("%H-%M-%S_%Y-%m-%d")
        filename = f"{timestamp}.png"

        # Ensure the 'Snapshots' directory exists
        subdirectory = os.path.join(self.save_path, 'Snapshots')
        os.makedirs(subdirectory, exist_ok=True)

        # Full file path where the snippet will be saved
        file_path = os.path.join(subdirectory, filename)

        # Save the cropped screenshot as a PNG file
        snippet.save(file_path, 'PNG')
        print(f"Snip saved to: {file_path}")
