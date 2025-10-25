import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from utils.ToolBarButtonFactory import ToolBarButtonFactory
from view.components.FolderSelector import FolderSelector
from view.components.WorkspaceChangeButton import WorkspaceChangeButton

from view.components.WorkspaceLabel import WorkspaceLabel
from view.components.actions.ANewFolder import ANewFolder
from utils.Store import store

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
        
        #--New Folder Button
        factory = ToolBarButtonFactory()
        self.folder_add_button = factory.createAddFolderButton()
        toolbar.addWidget(self.folder_add_button)
        
        #--Separator Bar
        toolbar.addSeparator()

        #--Folder Selector
        self.folder_select = FolderSelector()
        toolbar.addWidget(self.folder_select)
        
        #--Remove Folder Button
        self.folder_remove_button = factory.createRemoveFolderButton()
        toolbar.addWidget(self.folder_remove_button)
        
        #--Pin Folder Button
        self.folder_pin_button = factory.createPinFolderButton()
        toolbar.addWidget(self.folder_pin_button)
        
        #--Separator Bar
        toolbar.addSeparator()
        
        #--Snapshot Button
        self.snapshot_button = factory.createSnapshotButton()
        toolbar.addWidget(self.snapshot_button)
        
        #--Note Button
        self.note_button = factory.createNoteButton()
        toolbar.addWidget(self.note_button)
        
        #--Flashcard Button
        self.flashcard_button = factory.createFlashcardButton()
        toolbar.addWidget(self.flashcard_button)
        
        #--Separator Bar
        toolbar.addSeparator()
        
        #Bottom Half
        self.workspace_container = QtWidgets.QWidget()
        self.workspace_container.setObjectName("WorkspaceContainer")
        self.workspace_layout = QtWidgets.QHBoxLayout(self.workspace_container)
        
        self.workspace_label = WorkspaceLabel()
        self.workspace_layout.addWidget(self.workspace_label)
        
        self.workspace_layout.addStretch()
        
        self.workspace_change_button = WorkspaceChangeButton()
        self.workspace_layout.addWidget(self.workspace_change_button)
        

        
        self.setCentralWidget(self.workspace_container)
        

        

