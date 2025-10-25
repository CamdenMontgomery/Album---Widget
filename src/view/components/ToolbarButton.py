from PySide6 import QtWidgets, QtGui
from utils.Store import store
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt

class ToolbarButton(QtWidgets.QPushButton): 
    def __init__(self, icon, action_type):
        super().__init__("", None)
        self.setObjectName("ToolBarButton")
        
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)
        
        self.clicked.connect(lambda: store.dispatch(action_type, None))