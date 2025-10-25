from pynput import mouse
from PySide6.QtCore import QObject, Signal, QThread
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import  Qt
from PySide6.QtCore import QObject, QTimer, Signal, QPoint
from PySide6.QtCore import QTimer, QPoint
from PySide6.QtGui import QCursor, QGuiApplication

       
        
REVEAL_THRESHOLD = 10
HIDE_THRESHOLD = 800
        
        
class HoverStateManager(QObject, UseStore):
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_cursor)
        self.timer.start(16)  # ~60 Hz

    def check_cursor(self):
        pos: QPoint = QCursor.pos()
        y = pos.y()
        screen_height = QGuiApplication.primaryScreen().size().height()


        if not self.store_.state["show_widget"] and y >= screen_height - REVEAL_THRESHOLD:
            self.store_.dispatch(EActionTypes.SHOW_WIDGET, None)

        elif self.store_.state["show_widget"] and y < screen_height - HIDE_THRESHOLD:
            self.store_.dispatch(EActionTypes.HIDE_WIDGET, None)
