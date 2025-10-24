from PySide6 import QtWidgets
from utils.Store import store

class WorkspaceLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Workspace: Select a new workspace")
        self.setStatusTip("Current Workspace")
        store.state_changed.connect(self.on_state_changed)
        
    def on_state_changed(self):
        # Update label text based on the current workspace in the store
        current_workspace = store.state['workspace_dir'] or "Select a new workspace"
        self.setText(f"Workspace: {current_workspace}")