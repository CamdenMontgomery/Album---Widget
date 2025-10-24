from PySide6 import QtWidgets, QtGui
from utils.Store import store

class ToolbarButton(QtWidgets.QPushButton): 
    def __init__(self, icon, action_type):
        super().__init__("", None)
        self.setIcon(QtGui.QIcon(icon))
        self.setStatusTip("Toolbar Button")
        self.clicked.connect(lambda: store.dispatch(action_type, None))