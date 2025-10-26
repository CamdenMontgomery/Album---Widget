from abc import abstractmethod
from utils.Store import store
class UseStore:
    def __init__(self):
        self.store_= store
        store.state_changed.connect(self.on_state_changed)
        
    @abstractmethod
    def on_state_changed(self):
        pass