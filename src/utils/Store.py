from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog
from enums.EActionTypes import EActionTypes
import os

from view.windows.Flashcard import Flashcard
from view.windows.Note import Note
from view.windows.Snipping import SnippingOverlay

MODEL = {
    "ready" : False,
    "workspace_dir": None,
    "workspace_folders": [],
    "current_folder_name": None,
    "hotkey_folders": {'1': '', '2': '', '3': '', '4': '', '5': ''},
    "show_widget": True
}


class Store(QObject):
    
    show_widget = Signal()
    hide_widget = Signal()
    
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
                
            case EActionTypes.FOLDER_CHANGED:
                #Once a folder is selected the user can start working
                copy = self.state.copy()
                copy['current_folder_name'] = payload
                copy['ready'] = True
                self.state = copy  
                self.state_changed.emit()
            
            case EActionTypes.HIDE_WIDGET:
                copy = self.state.copy()
                copy['show_widget'] = False
                self.hide_widget.emit()
                self.state = copy                
                
                
            case EActionTypes.SHOW_WIDGET:
                copy = self.state.copy()
                copy['show_widget'] = True
                self.show_widget.emit()
                self.state = copy  
                
            case EActionTypes.BEGIN_SNAPSHOT:
                if not self.state['ready']: return
                save_path = os.path.join(self.state['workspace_dir'],self.state['current_folder_name'])
                self.snipping_overlay = SnippingOverlay(path=save_path)
                self.snipping_overlay.show()
                
                
            case EActionTypes.OPEN_NOTES:
                if not self.state['ready']: return
                save_path = os.path.join(self.state['workspace_dir'],self.state['current_folder_name'])
                self.note = Note(path=save_path)
                self.note.show()
                
            case EActionTypes.NEW_FLASHCARD:
                if not self.state['ready']: return
                save_path = os.path.join(self.state['workspace_dir'],self.state['current_folder_name'])
                print('new flashy')
                self.flashcard = Flashcard(path=save_path)
                print('fl',self.flashcard)
                self.flashcard.show()
                print('n flashy')
                
            #Toggle whether current folder is in the hotkeys or not
            case EActionTypes.TOGGLE_PIN:
                hotkey_folders = self.state['hotkey_folders']
                current_folder = self.state['current_folder_name']
                folders = list(hotkey_folders.values())
                
                #If hotkey exists, remove it
                if current_folder in folders:
                    index = folders.index(current_folder)
                    copy = self.state.copy()
                    copy['hotkey_folders'][str(index + 1)] = ""
                    self.state = copy   
                     
                else:
                    index = folders.index("")
                    copy = self.state.copy()
                    copy['hotkey_folders'][str(index + 1)] = current_folder
                    self.state = copy   
                    
                self.state_changed.emit()
                    
                    
            case EActionTypes.FOLDER_HOTKEY:
                hotkey_folders = self.state['hotkey_folders']
                go_to_folder = hotkey_folders[str(payload)]
                if go_to_folder != '':
                    self.dispatch(EActionTypes.FOLDER_CHANGED,go_to_folder)
                    
            case EActionTypes.TOOL_HOTKEY:
                match (payload):
                    case 'z': self.dispatch(EActionTypes.BEGIN_SNAPSHOT, None)
                    case 'x': self.dispatch(EActionTypes.OPEN_NOTES, None)
                    case 'c': self.dispatch(EActionTypes.NEW_FLASHCARD, None)
                
                 
#Globally accessible store instance
store = Store()
store.setParent(QApplication.instance()) #Avoid garbage collection
    