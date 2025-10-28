
from utils.UseStore import UseStore
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore

class HotKeyDisplay(QtWidgets.QWidget, UseStore):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HotKeyDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        
        
        self.label = QtWidgets.QLabel('No Hotkey', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyDisplayLabel")
        self.layout.addWidget(self.label)
        
        
        

        
    def setStyleFromState(self, active: bool):
        self.label.setObjectName("HotKeyDisplayLabelActive" if active else "HotKeyDisplayLabel")
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        
        self.setObjectName("HotKeyDisplayActive" if active else "HotKeyDisplay")
        self.style().unpolish(self)
        self.style().polish(self)
        
        
    def on_state_changed(self):
        hotkey_folders = self.store_.state['hotkey_folders']
        current_folder = self.store_.state['current_folder_name']
        folders = list(hotkey_folders.values())
        
        if current_folder in folders:
            index = folders.index(current_folder)
            self.label.setText('Alt + ' + str(index + 1) )
            self.setStyleFromState(True)
            
                
        else:
            self.label.setText('No Hotkey')
            self.setStyleFromState(False)