from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog
from enums.EActionTypes import EActionTypes


MODEL = {
    "workspace_dir": None,
    "workspace_folders": [],
    "current_folder_name": None,
    "hotkey_folders": {1: None, 2: None, 3: None, 4: None, 5: None},
}



class Store():
    
    def __init__(self):
        self.state = MODEL.copy()
        
    def dispatch(self, action_type, payload):
        self._controller(action_type, payload)
        
        
    def _controller(self, action_type, payload):
        match action_type:
            case EActionTypes.OPEN_WORKSPACE_SELECTOR: 
                folder_path = QFileDialog.getExistingDirectory(None, "Select Directory", "")
                if folder_path: 
                    copy = self.state.copy()
                    copy["workspace_dir"] = folder_path
                    self.state = copy
                    print(folder_path)
                

        
    