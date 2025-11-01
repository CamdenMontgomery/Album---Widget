# --- Standard Library ---
from os import path

# --- PySide6 ---
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize, Qt

# --- Project Imports ---
from enums.EActionTypes import EActionTypes
from utils.Store import store
from utils.basepath import BASE_PATH
from utils.UseStore import UseStore


# --- Constants ---
ICON_PATH = path.join(BASE_PATH, "public", "icons", "workspace.svg")


class WorkspaceButton(QtWidgets.QPushButton, UseStore):
    """A button widget that opens the workspace selector or displays the current workspace."""

    def __init__(self):
        """
        Initialize the WorkspaceButton.

        Sets the button's icon, text, and behavior when clicked.
        """
        super().__init__("", None)
        self.setObjectName("WorkspaceButton")

        # Set button icon and text
        self.setIcon(QtGui.QIcon(ICON_PATH))
        self.setIconSize(QSize(24, 24))
        self.setText("   Open Workspace")
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)

        # Connect button click to the trigger method
        self.clicked.connect(self.trigger)

    def trigger(self):
        """
        Dispatch an action to open the workspace selector when the button is clicked.
        """
        store.dispatch(EActionTypes.OPEN_WORKSPACE_SELECTOR, None)

    def on_state_changed(self):
        """
        Update the button's text based on the current workspace directory state.

        If a workspace is set, display the workspace name. If no workspace is set,
        display "Open Workspace."
        """
        current_workspace = self.store_.state.get('workspace_dir')

        # Update the button text based on whether a workspace is set
        if current_workspace:
            workspace_name = current_workspace.split('/')[-1].capitalize()
            self.setText(f"   Workspace: {workspace_name}")
        else:
            self.setText("   Open Workspace")
