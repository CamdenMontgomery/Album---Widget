import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from view.components.actions.ANewFolder import ANewFolder

class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Album")
        toolbar = QtWidgets.QToolBar("Tools")
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        self.folder_add_button = ANewFolder()
        toolbar.addAction(self.folder_add_button)
