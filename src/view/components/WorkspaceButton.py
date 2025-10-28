from PySide6 import QtWidgets, QtGui
from enums.EActionTypes import EActionTypes
from utils.Store import store
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt

from utils.UseStore import UseStore


class WorkspaceButton(QtWidgets.QPushButton, UseStore): 
    def __init__(self):
        super().__init__("", None)
        self.setObjectName("WorkspaceButton")
        
        self.setIcon(QtGui.QIcon("public/icons/workspace.svg"))
        self.setIconSize(QSize(24, 24))
        self.setText("Select Workspace")
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)
        

        
        self.clicked.connect(self.trigger)
        
    def trigger(self):
        store.dispatch(EActionTypes.OPEN_WORKSPACE_SELECTOR, None)
        
   
    def on_state_changed(self):
        current_workspace = self.store_.state['workspace_dir']
        if current_workspace:
            workspace_name = current_workspace.split('/')[-1]
            self.setText('Workspace: ' + workspace_name.capitalize())
        else:
            self.setText("Select Workspace")
        