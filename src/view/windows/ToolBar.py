import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class ToolBar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.folder_add_button = QtWidgets.QPushButton("New Folder")
        
        self.folder_delete_button = QtWidgets.QPushButton("Delete")
        self.folder_pin_button = QtWidgets.QPushButton("Pin")
        self.folder_select = QtWidgets.QComboBox()


        self.layout.addWidget()
