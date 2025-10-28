from PySide6 import QtWidgets, QtGui
from utils.Store import store
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

from utils.basepath import BASE_PATH
from os import path

PIN_PATH = path.join(BASE_PATH,"public","icons","pin_folder.svg")
UNPIN_PATH = path.join(BASE_PATH,"public","icons","unpin_folder.svg")

class PinButton(QtWidgets.QPushButton, UseStore):
    def __init__(self):
        super().__init__("", None)
        self.setObjectName("ToolBarButton")
        
        self.setIcon(QtGui.QIcon(PIN_PATH))
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
            self.setIcon(QtGui.QIcon(UNPIN_PATH))
            self.update()
        else:
            print("Show pin")
            self.setIcon(QtGui.QIcon(PIN_PATH))
            self.update()