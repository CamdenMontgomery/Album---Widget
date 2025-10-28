from abc import abstractmethod
from utils.Store import store
from PySide6.QtCore import QTimer
class UseStore:
    def __init__(self):
        self.store_= store
        store.state_changed.connect(self.on_state_changed)
        QTimer.singleShot(0, self.on_state_changed)#defer till after QT internals initialize in subclass | loads initial data
        
    @abstractmethod
    def on_state_changed(self):
        pass