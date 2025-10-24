import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from utils.ToolBarButtonFactory import ToolBarButtonFactory
from view.components.WorkspaceChangeButton import WorkspaceChangeButton

from view.components.actions.ANewFolder import ANewFolder

class Widget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Album")
        self.resize(800, 24)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("MainWindow")
        
        #Top Half
        toolbar = QtWidgets.QToolBar("Tools")
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.setMovable(False)
        toolbar.setObjectName('Toolbar')
        self.addToolBar(toolbar)
        
        factory = ToolBarButtonFactory()
        self.folder_add_button = factory.createAddFolderButton()
        toolbar.addWidget(self.folder_add_button)
        
        self.folder_remove_button = factory.createRemoveFolderButton()
        toolbar.addWidget(self.folder_remove_button)
        
        #Bottom Half
        self.workspace_container = QtWidgets.QWidget()
        self.workspace_layout = QtWidgets.QHBoxLayout(self.workspace_container)
        
        self.workspace_label = QtWidgets.QLabel("Workspace: None")
        self.workspace_layout.addWidget(self.workspace_label)
        
        self.workspace_change_button = WorkspaceChangeButton()
        self.workspace_layout.addWidget(self.workspace_change_button)
        
        self.workspace_new_button = QtWidgets.QPushButton("new")
        self.workspace_layout.addWidget(self.workspace_new_button)
        
        self.setCentralWidget(self.workspace_container)
        

        

