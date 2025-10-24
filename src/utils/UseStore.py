from abc import abstractmethod
from utils.Store import store
class UseStore:
    def __init__(self):
        self.store_= store
        
    @abstractmethod
    def on_state_changed(self):
        pass