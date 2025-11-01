# --- Standard Library ---
from PySide6.QtCore import QSize, QPoint, Qt

# --- Third-Party Imports ---
from PySide6 import QtWidgets, QtGui
from pyqttooltip import Tooltip, TooltipPlacement

# --- Project Imports ---
from utils.Store import store


class ToolbarButton(QtWidgets.QPushButton):
    """A button widget for the toolbar with an icon, action, and tooltip."""

    def __init__(self, icon: str, action_type: int, tooltip: str):
        """
        Initialize the ToolbarButton.

        Args:
            icon (str): The path to the icon image for the button.
            action_type (int): The action type (integer) to dispatch when the button is clicked.
            tooltip (str): The tooltip text to display on hover.
        """
        super().__init__("", None)
        self.setObjectName("ToolBarButton")

        # Set button icon and size
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)

        # Tooltip setup
        self.tooltip = Tooltip(self, tooltip)
        self.tooltip.setPlacement(TooltipPlacement.TOP)
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(20, 20))

        # Connect button click to dispatch action
        self.clicked.connect(lambda: self.trigger_action(action_type))

    def trigger_action(self, action_type: int):
        """
        Dispatch an action to the store when the button is clicked.

        Args:
            action_type (int): The action (integer) to dispatch to the store.
        """
        store.dispatch(action_type, None)
