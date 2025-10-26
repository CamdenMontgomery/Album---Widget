from pynput import keyboard
from PySide6.QtCore import QObject, Signal, QThread
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import  Qt
from PySide6.QtCore import QObject, QTimer, Signal, QPoint
from PySide6.QtCore import QTimer, QPoint
from PySide6.QtGui import QCursor, QGuiApplication

class HotKeyManager(QObject, UseStore):

    def __init__(self):
        super().__init__()
        
        #Define Hotkeys and bindings
        self.hotkeys = keyboard.GlobalHotKeys({
         '<alt>+1': lambda: self.store_.dispatch(EActionTypes.HOTKEY_INPUT, 1),
         '<alt>+2': lambda: self.store_.dispatch(EActionTypes.HOTKEY_INPUT, 2),
         '<alt>+3': lambda: self.store_.dispatch(EActionTypes.HOTKEY_INPUT, 3),
         '<alt>+4': lambda: self.store_.dispatch(EActionTypes.HOTKEY_INPUT, 4),
         '<alt>+5': lambda: self.store_.dispatch(EActionTypes.HOTKEY_INPUT, 5),
        })
        
        self.hotkeys.start()

    def on_state_changed(self):
        pass
    