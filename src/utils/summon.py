from PySide6.QtCore import QObject, QTimer, QPoint
from PySide6.QtGui import QCursor, QGuiApplication
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

# Threshold constants for detecting hover behavior
REVEAL_THRESHOLD = 10
HIDE_THRESHOLD = 800

class HoverStateManager(QObject, UseStore):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_cursor)
        self.timer.start(16)  # ~60 Hz

    def check_cursor(self):
        """Check the cursor position and dispatch actions based on hover state."""
        pos: QPoint = QCursor.pos()
        y = pos.y()  # Cursor Y position
        screen_height = QGuiApplication.primaryScreen().size().height()

        # Get the current state of the widget visibility from the store
        show_widget = self.store_.state["show_widget"]



        # If the widget is hidden and cursor is near the bottom, show the widget
        if not show_widget and y >= screen_height - REVEAL_THRESHOLD:
            self.store_.dispatch(EActionTypes.SHOW_WIDGET, None)

        # If the widget is visible and cursor is not near the bottom, hide the widget
        elif show_widget and y < screen_height - HIDE_THRESHOLD:
            self.store_.dispatch(EActionTypes.HIDE_WIDGET, None)
