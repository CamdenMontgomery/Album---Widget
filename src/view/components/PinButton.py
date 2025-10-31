from PySide6 import QtWidgets, QtGui
from utils.Store import store
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

from utils.basepath import BASE_PATH
from os import path

from PySide6.QtCore import QSize, QPoint
from PySide6.QtCore import Qt
from pyqttooltip import Tooltip, TooltipPlacement

PIN_PATH = path.join(BASE_PATH,"public","icons","pin_folder.svg")
UNPIN_PATH = path.join(BASE_PATH,"public","icons","unpin_folder.svg")

PIN_TOOLTIP = "Add Folder To Hotkeys"
UNPIN_TOOLTIP = "Remove Folder From Hotkeys"

class PinButton(QtWidgets.QPushButton, UseStore):
    def __init__(self):
        super().__init__("", None)
        self.setObjectName("ToolBarButton")
        
        self.setIcon(QtGui.QIcon(PIN_PATH))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)
        
        self.tooltip = Tooltip(self, PIN_TOOLTIP)
        self.tooltip.setPlacement(TooltipPlacement.TOP) 
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(20, 20))
        
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
            self.tooltip.setText(UNPIN_TOOLTIP)
            self.update()
        else:
            print("Show pin")
            self.setIcon(QtGui.QIcon(PIN_PATH))
            self.tooltip.setText(PIN_TOOLTIP)
            self.update()