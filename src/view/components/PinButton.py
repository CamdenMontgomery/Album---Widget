# --- Standard Library ---
from os import path

# --- PySide6 Imports ---
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize, Qt, QPoint

# --- Third-Party Imports ---
from pyqttooltip import Tooltip, TooltipPlacement

# --- Project Imports ---
from utils.Store import store
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore
from utils.basepath import BASE_PATH


# --- Constants ---
PIN_PATH = path.join(BASE_PATH, "public", "icons", "pin_folder.svg")
UNPIN_PATH = path.join(BASE_PATH, "public", "icons", "unpin_folder.svg")
PIN_TOOLTIP = "Add Folder To Hotkeys"
UNPIN_TOOLTIP = "Remove Folder From Hotkeys"


class PinButton(QtWidgets.QPushButton, UseStore):
    """A button that toggles pinning a folder to hotkeys, with appropriate tooltip and icon."""

    def __init__(self):
        """
        Initialize the PinButton.

        Sets the button's icon, tooltip, and behavior when clicked. 
        Initially shows the "pin" icon and tooltip.
        """
        super().__init__("", None)
        self.setObjectName("ToolBarButton")

        # Set the initial icon and size
        self.setIcon(QtGui.QIcon(PIN_PATH))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)

        # Set up the tooltip
        self.tooltip = Tooltip(self, PIN_TOOLTIP)
        self.tooltip.setPlacement(TooltipPlacement.TOP)
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(20, 20))

        # Connect the button's click to toggle pin action
        self.clicked.connect(self.toggle_pin)

    def toggle_pin(self):
        """
        Dispatch an action to toggle the pin state of the current folder.
        """
        store.dispatch(EActionTypes.TOGGLE_PIN, None)

    def on_state_changed(self):
        """
        Update the button's icon and tooltip based on whether the current folder is pinned.

        If the current folder is in the 'hotkey_folders', it shows the "unpin" icon and tooltip.
        Otherwise, it shows the "pin" icon and tooltip.
        """
        hotkey_folders = self.store_.state.get('hotkey_folders', {})
        current_folder = self.store_.state.get('current_folder_name', '')
        folders = list(hotkey_folders.values())
        
        # Check if the current folder is pinned
        if current_folder in folders:
            self.setIcon(QtGui.QIcon(UNPIN_PATH))
            self.tooltip.setText(UNPIN_TOOLTIP)
        else:
            self.setIcon(QtGui.QIcon(PIN_PATH))
            self.tooltip.setText(PIN_TOOLTIP)

        self.update()  # Ensure the button is updated with the new icon and tooltip text
