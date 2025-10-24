import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from utils.styleloader import loadStylesheets
from view.components.actions.ANewFolder import ANewFolder

class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Album")
        self.resize(800, 24)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("MainWindow")
        
        toolbar = QtWidgets.QToolBar("Tools")
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        self.folder_add_button = ANewFolder()
        toolbar.addAction(self.folder_add_button)
        

