from PySide6 import QtWidgets, QtGui
from utils.Store import store
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore


class PinButton(QtWidgets.QPushButton, UseStore):
    def __init__(self):
        super().__init__("", None)
        self.setObjectName("ToolBarButton")
        
        self.setIcon(QtGui.QIcon("public/icons/pin_folder.svg"))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)
        
        self.clicked.connect(lambda: store.dispatch( EActionTypes.TOGGLE_PIN, None))
        
        
    
    def on_state_changed(self):
    
        #Check if current folder is pinned
        hotkey_folders = self.store_.state['hotkey_folders']
        current_folder = self.store_.state['current_folder_name']
        folders = list(hotkey_folders.values())
        
        #If pinned show unpin button
        if current_folder in folders:
            print("Show Unpin")
            self.setIcon(QtGui.QIcon("public/icons/unpin_folder.svg"))
            self.update()
        else:
            print("Show pin")
            self.setIcon(QtGui.QIcon("public/icons/pin_folder.svg"))
            self.update()