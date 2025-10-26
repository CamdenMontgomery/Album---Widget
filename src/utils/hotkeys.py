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

    _cross_thread = Signal(int, str)

    def __init__(self):
        super().__init__()
        
        #Define Hotkeys and bindings
        self.hotkeys = keyboard.GlobalHotKeys({
            
            #Folder Switching
            '<alt>+1': lambda: self._cross_thread.emit(EActionTypes.FOLDER_HOTKEY, '1'),
            '<alt>+2': lambda: self._cross_thread.emit(EActionTypes.FOLDER_HOTKEY, '2'),
            '<alt>+3': lambda: self._cross_thread.emit(EActionTypes.FOLDER_HOTKEY, '3'),
            '<alt>+4': lambda: self._cross_thread.emit(EActionTypes.FOLDER_HOTKEY, '4'),
            '<alt>+5': lambda: self._cross_thread.emit(EActionTypes.FOLDER_HOTKEY, '5'),
            
            #Tools
            '<alt>+z': lambda: self._cross_thread.emit(EActionTypes.TOOL_HOTKEY, 'z'),
            '<alt>+x': lambda: self._cross_thread.emit(EActionTypes.TOOL_HOTKEY, 'x'),
            '<alt>+c': lambda: self._cross_thread.emit(EActionTypes.TOOL_HOTKEY, 'c'),
            
        })
        
        self._cross_thread.connect(self.qtThread)
        self.hotkeys.start()
        
    #Use signals to jump from pynput thread to qtthread to aviod issues
    def qtThread(self, type, key):
        self.store_.dispatch(type,key)

    def on_state_changed(self):
        pass
    