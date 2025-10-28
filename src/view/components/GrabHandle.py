from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QSize, QPoint, Qt
from utils.basepath import BASE_PATH
from os import path

ICON_PATH = path.join(BASE_PATH,"public","icons","grab_handle.svg")

class GrabHandle(QtWidgets.QPushButton):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__()
        self.grabbing = False
        self.offset = QPoint(0,0)
        self.parent_widget = parent

        self.setObjectName("GrabHandle")
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setIcon(QtGui.QIcon(ICON_PATH))
        self.setIconSize(QSize(24, 24))
        
        
    def mouseMoveEvent(self, event):
        if self.grabbing:
            cursor_pos = QtGui.QCursor.pos() #get it relative to the entire screen
            self.parent_widget.move(cursor_pos - self.offset)
            
    def mousePressEvent(self, event):
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        grabbed_at = event.pos()
        self.offset = grabbed_at + self.pos()
        self.grabbing = True
        
    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.grabbing = False
            