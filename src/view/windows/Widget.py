import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from utils.ToolBarButtonFactory import ToolBarButtonFactory
from view.components.FolderSelector import FolderSelector
from view.components.PinButton import PinButton
from view.components.WorkspaceChangeButton import WorkspaceChangeButton

from view.components.WorkspaceLabel import WorkspaceLabel
from view.components.actions.ANewFolder import ANewFolder
from utils.Store import store
from view.components.HotKeySlots import HotKeySlots
from PySide6.QtWidgets import QApplication
from utils.UseStore import UseStore


from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QPoint, QParallelAnimationGroup

class Widget(QtWidgets.QMainWindow, UseStore):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Album")
        
        self.resize(1290, 24)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() * 0.5 - self.width() * 0.5, screen.height() * 0.8 - self.height() * 0.5)
        
        
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
        self.folder_pin_button = PinButton()
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
        
        #--Hotkey Slots
        self.hotkey_slots = HotKeySlots()
        toolbar.addWidget(self.hotkey_slots)
        
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
        
        
        
        self.store_.hide_widget.connect(self.slide_out)
        self.store_.show_widget.connect(self.slide_in)
        

        
    def slide_out(self):

        #Store animation in self to avoid garbage collection
        screen = QApplication.primaryScreen().geometry()
        
        start_pos = self.pos()
        end_pos = QPoint(screen.width() * 0.5 - self.width() * 0.5, screen.height() * 1.2 - self.height() * 0.5)

        self.move_anim = QPropertyAnimation(self, b"pos")
        self.move_anim.setDuration(300)                  
        self.move_anim.setStartValue(start_pos)       
        self.move_anim.setEndValue(end_pos)
        self.move_anim.setEasingCurve(QEasingCurve.Type.Linear)
   
        
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.Linear)
        
        
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.move_anim)
        self.anim_group.addAnimation(self.fade_anim)
        self.anim_group.start()

        
    def slide_in(self):
        
        
        #Store animation in self to avoid garbage collection
        screen = QApplication.primaryScreen().geometry()
        
        start_pos = self.pos()
        end_pos = QPoint(screen.width() * 0.5 - self.width() * 0.5, screen.height() * 0.8 - self.height() * 0.5)

        self.move_anim = QPropertyAnimation(self, b"pos")
        self.move_anim.setDuration(300)                  
        self.move_anim.setStartValue(start_pos)       
        self.move_anim.setEndValue(end_pos)
        self.move_anim.setEasingCurve(QEasingCurve.Type.Linear)
   
        
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.Linear)
        
        
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.move_anim)
        self.anim_group.addAnimation(self.fade_anim)
        self.anim_group.start()

