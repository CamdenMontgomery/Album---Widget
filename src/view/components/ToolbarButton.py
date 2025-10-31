from PySide6 import QtWidgets, QtGui
from utils.Store import store
from PySide6.QtCore import QSize, QPoint
from PySide6.QtCore import Qt
from pyqttooltip import Tooltip, TooltipPlacement

class ToolbarButton(QtWidgets.QPushButton): 
    def __init__(self, icon, action_type, tooltip):
        super().__init__("", None)
        self.setObjectName("ToolBarButton")
        
        self.setIcon(QtGui.QIcon(icon))
        self.setIconSize(QSize(24, 24))
        self.setStatusTip("Toolbar Button")
        self.setCursor(Qt.PointingHandCursor)
        
        self.tooltip = Tooltip(self, tooltip)
        self.tooltip.setPlacement(TooltipPlacement.TOP) 
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(20, 20))
        
        self.clicked.connect(lambda: store.dispatch(action_type, None))