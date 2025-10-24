from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog
from enums.EActionTypes import EActionTypes
import os

MODEL = {
    "workspace_dir": None,
    "workspace_folders": [],
    "current_folder_name": None,
    "hotkey_folders": {1: None, 2: None, 3: None, 4: None, 5: None},
}


class Store(QObject):
    
    state_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.state = MODEL.copy()
            
    def dispatch(self, action_type, payload):
        self._controller(action_type, payload)
        
        
    def _controller(self, action_type, payload):
        match action_type:
            case EActionTypes.OPEN_WORKSPACE_SELECTOR: 
                
                #prepare for mutation
                copy = self.state.copy()
                
                #open file dialog to select folder
                folder_path = QFileDialog.getExistingDirectory(None, "Select Directory", "")
                
                if not folder_path:
                    return
                  
                
                copy["workspace_dir"] = folder_path
                
                
                #get workspace folders
                contents = os.listdir(folder_path)
                folders = [name for name in contents if os.path.isdir(os.path.join(folder_path, name))]
                copy["workspace_folders"] = folders
                
                
                
                #finalize mutation
                self.state = copy
                self.state_changed.emit()
                print(self.state)
                
                
                 
#Globally accessible store instance
store = Store()
store.setParent(QApplication.instance()) #Avoid garbage collection
    