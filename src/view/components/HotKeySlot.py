
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
        
        self.label = QtWidgets.QLabel('None', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyLabel")
        self.layout.addWidget(self.label)
        

        
    def setStyleFromState(self, active: bool):
        self.label.setObjectName("HotKeyLabelActive" if active else "HotKeyLabel")
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        
        self.setObjectName("HotKeySlotActive" if active else "HotKeySlot")
        self.style().unpolish(self)
        self.style().polish(self)
        
        self.icon.setObjectName("HotKeyIconActive" if active else "HotKeyIcon")
        self.icon.style().unpolish(self.icon)
        self.icon.style().polish(self.icon)
        
    def on_state_changed(self):
        self.label.setText(self.store_.state['hotkey_folders'][self.key])
        is_active = self.store_.state['hotkey_folders'][self.key] == self.store_.state['current_folder_name']
        self.setStyleFromState(is_active)