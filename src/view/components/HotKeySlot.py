
from utils.UseStore import UseStore
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore

class HotKeySlot(QtWidgets.QWidget, UseStore):
    def __init__(self, key='1', parent=None):
        super().__init__(parent)
        self.setObjectName("HotKeySlot")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.key = key
        self.layout = QtWidgets.QHBoxLayout(self)
        
        self.icon = QtWidgets.QLabel(key, self)
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon.setObjectName("HotKeyIcon")
        self.layout.addWidget(self.icon)
        
        self.label = QtWidgets.QLabel('Empty', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyLabel")
        self.layout.addWidget(self.label)
        
        self.store_.state_changed.connect(self.on_state_changed)
        
    def on_state_changed(self):
        self.label.setText(self.store_.state['hotkey_folders'][self.key])