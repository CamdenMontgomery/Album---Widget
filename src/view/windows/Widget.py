import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

from utils.ToolBarButtonFactory import ToolBarButtonFactory
from view.components.WorkspaceButton import WorkspaceButton
from view.components.FolderSelector import FolderSelector
from view.components.HotkeyDisplay import HotKeyDisplay
from view.components.PinButton import PinButton
from view.components.Separator import Separator
from view.components.WorkspaceChangeButton import WorkspaceChangeButton

from view.components.WorkspaceLabel import WorkspaceLabel
from view.components.actions.ANewFolder import ANewFolder
from utils.Store import store
from view.components.HotKeySlots import HotKeySlots
from PySide6.QtWidgets import QApplication
from utils.UseStore import UseStore
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect



from PySide6.QtCore import QPropertyAnimation, QRect, QEasingCurve, QPoint, QParallelAnimationGroup

class Widget(QtWidgets.QMainWindow, UseStore):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Album")
        
        #self.resize(1290, 24)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() * 0.5 - self.width() * 0.5, screen.height() * 0.8 - self.height() * 0.5)
        
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("MainWindow")
        
        
        #Content Container
        self.container = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(20, 20, 20, 20) #For Catching Shadows
        
        
        
        #Top Half
        self.toolbar = QtWidgets.QWidget()
        self.toolbar.setObjectName('Toolbar')
        self.toolbar_layout = QtWidgets.QHBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(10, 10, 10, 10)
        self.toolbar_layout.setSpacing(10)
        self.container_layout.addWidget(self.toolbar)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)  # Adjust the blur radius as needed
        self.shadow.setXOffset(0)      # Adjust the X offset as needed
        self.shadow.setYOffset(5)      # Adjust the Y offset as needed
        self.shadow.setColor(QColor(150, 150, 150, 100))


        self.toolbar.setGraphicsEffect(self.shadow)
        
        
        
        #--Workspace Button
        self.workspace_button = WorkspaceButton()
        self.toolbar_layout.addWidget(self.workspace_button)

        #--Separator Bar
        self.toolbar_layout.addWidget(Separator())
        

        


        #--Folder Selector
        self.folder_select = FolderSelector()
        self.toolbar_layout.addWidget(self.folder_select)
        
        #--New Folder Button
        factory = ToolBarButtonFactory()
        self.folder_add_button = factory.createAddFolderButton()
        self.toolbar_layout.addWidget(self.folder_add_button)
        
        #--Remove Folder Button
        self.folder_remove_button = factory.createRemoveFolderButton()
        self.toolbar_layout.addWidget(self.folder_remove_button)
        
        #--Pin Folder Button
        self.folder_pin_button = PinButton()
        self.toolbar_layout.addWidget(self.folder_pin_button)
        
        #--Hotkey Display
        self.hotkey_display = HotKeyDisplay()
        self.toolbar_layout.addWidget(self.hotkey_display)
        
        #--Separator Bar
        self.toolbar_layout.addWidget(Separator())
        
        #--Snapshot Button
        self.snapshot_button = factory.createSnapshotButton()
        self.toolbar_layout.addWidget(self.snapshot_button)
        
        #--Note Button
        self.note_button = factory.createNoteButton()
        self.toolbar_layout.addWidget(self.note_button)
        
        #--Flashcard Button
        self.flashcard_button = factory.createFlashcardButton()
        self.toolbar_layout.addWidget(self.flashcard_button)
        
        #--Separator Bar
        self.toolbar_layout.addWidget(Separator())
        
        #--Hotkey Slots
        self.hotkey_slots = HotKeySlots()
        self.toolbar_layout.addWidget(self.hotkey_slots)
        
        self.container_layout.addWidget(self.toolbar)
        
        #Bottom Half
        self.workspace_container = QtWidgets.QWidget()
        self.workspace_container.setObjectName("WorkspaceContainer")
        self.workspace_layout = QtWidgets.QHBoxLayout(self.workspace_container)
        
        self.workspace_label = WorkspaceLabel()
        self.workspace_layout.addWidget(self.workspace_label)
        
        self.workspace_layout.addStretch()
        
        self.workspace_change_button = WorkspaceChangeButton()
        self.workspace_layout.addWidget(self.workspace_change_button)
    
    
        #self.container_layout.addWidget(self.workspace_container)
        
        self.setCentralWidget(self.container)
        
        
        
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

