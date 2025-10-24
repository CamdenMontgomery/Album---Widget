from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from global_store import store
from enums.EActionTypes import EActionTypes

class WorkspaceChangeButton(QtWidgets.QPushButton):
    

    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setShortcut("Ctrl+W")
        self.setStatusTip("Select a new workspace")
        self.clicked.connect(self.trigger)
        
    def trigger(self):
        store.dispatch(EActionTypes.OPEN_WORKSPACE_SELECTOR, None)