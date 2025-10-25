from PySide6 import QtWidgets
from utils.UseStore import UseStore

class HotKeySlot(QtWidgets.QWidget, UseStore):
    def __init__(self, key='1', parent=None):
        super().__init__(parent)
        self.setObjectName("HotKeySlot")
        self.key = key
        
        self.layout = QtWidgets.QHBoxLayout(self)
        
        self.icon = QtWidgets.QLabel(key, self)
        self.icon.setObjectName("hotKeyIcon")
        self.layout.addWidget(self.icon)
        
        self.label = QtWidgets.QLabel('', self)
        self.label.setObjectName("hotKeyLabel")
        self.layout.addWidget(self.label)
        
        self.store_.state_changed.connect(self.on_state_changed)
        
    def on_state_changed(self):
        self.label.setText(self.store_.state['hotkey_folders'][self.key])