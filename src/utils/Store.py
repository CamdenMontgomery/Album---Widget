from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QFileDialog, QDialog
from enums.EActionTypes import EActionTypes
import os

from utils.persist import getGlobalConfigsRef, getLocalConfigsRef, getStateFromConfigs
from view.windows.Flashcard import Flashcard
from view.windows.Note import Note
from view.windows.Snipping import SnippingOverlay
from view.components.Dialog import Dialog, DIALOG_TYPES



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
        self.state = getStateFromConfigs()
        print(self.state)
        
        #store references to global and local persistence files
        self.global_configs = getGlobalConfigsRef()
        self.local_configs = getLocalConfigsRef()
        
        self.state_changed.emit()
            
    def dispatch(self, action_type, payload):
        self._controller(action_type, payload)
        
        
    def _controller(self, action_type, payload):
        

        
        match action_type:
            case EActionTypes.OPEN_WORKSPACE_SELECTOR: 
                
                #prepare for mutation
                copy = self.state.copy()
                
                #open file dialog to select folder
                folder_path = QFileDialog.getExistingDirectory(None, "Select Directory", copy["workspace_dir"] or "")
                
                if not folder_path:
                    return
                  
                
                copy["workspace_dir"] = folder_path
                
                
                #get workspace folders
                contents = os.listdir(folder_path)
                folders = [name for name in contents if os.path.isdir(os.path.join(folder_path, name))]
                copy["workspace_folders"] = folders
                
                
                
                #finalize mutation
                self.state = copy
                self.global_configs.setValue("workspace_dir",folder_path)
                self.global_configs.setValue("workspace_folders",folders)
                self.state_changed.emit()
                
            case EActionTypes.FOLDER_CHANGED:
                #Once a folder is selected the user can start working
                copy = self.state.copy()
                copy['current_folder_name'] = payload
                copy['ready'] = True
                self.state = copy  
                
                self.state_changed.emit()
                self.global_configs.setValue("current_folder_name",payload)
            
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
                self.local_configs.setValue("hotkey_folders",self.state['hotkey_folders'])
                    
                    
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
                    
            
                    
            case EActionTypes.REMOVE_FOLDER:
                
                title = "Delete This Folder?"
                message = f"""Doing this will permanently delete the '{self.state['current_folder_name']}' folder from this workspace and from this computer. This is irreversable. Are you sure you want to remove '{ self.state['current_folder_name'] }'?"""
                confirm_text = "Yes, Delete It"
                reject_text = "No, Keep It"
                
                warning = Dialog(title, message, confirm_text, reject_text, DIALOG_TYPES.WARNING)
                result = warning.exec()
                
                if result == QDialog.DialogCode.Accepted:
                    
                    workspace_dir = self.state['workspace_dir']
                    folder_name = self.state['current_folder_name']
                    full_path = os.path.join(workspace_dir,folder_name)
                    
                    try:
                        if not os.path.exists(full_path): raise FileNotFoundError
                        
                        os.rmdir(full_path)
                        print(f"Directory '{full_path}' removed successfully.")
                        
                        #reload folders, hotkeys and current workspace
                        copy = self.state.copy()
                        
                        contents = os.listdir(workspace_dir)
                        folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
                        copy["workspace_folders"] = folders     
                        
                        hotkey_folders = self.state['hotkey_folders']
                        current_folder = self.state['current_folder_name']
                        folders = list(hotkey_folders.values())
                        
                        #If hotkey exists, remove it
                        if current_folder in folders:
                            index = folders.index(current_folder)
                            copy['hotkey_folders'][str(index + 1)] = ""
                        
                        copy['current_folder_name'] = folders[0] or ''
                
                        #finalize mutation
                        self.state = copy
                        self.global_configs.setValue("workspace_folders",folders)
                        self.state_changed.emit()
                        
                        
                    except FileExistsError:
                        print(f"Directory '{full_path}' doesn't exists.")
                    except OSError as e:
                        print(f"Error removing directory: {e}")
                    
                else:
                    print("Dont do it")
                    
                    
            case EActionTypes.ADD_FOLDER:
                
                title = "New Folder"
                message = "What is the name of this folder? It should be named relative to the topic you are studying."
                confirm_text = "Create"
                reject_text = "Cancel"
                
                input = Dialog(title, message, confirm_text, reject_text, DIALOG_TYPES.INPUT)
                result = input.exec()
                
                if result == QDialog.DialogCode.Accepted:
                    
                    workspace_dir = self.state['workspace_dir']
                    folder_name = input.getResultingText().replace('.','')#Break any extensions the user tries to force
                    full_path = os.path.join(workspace_dir,folder_name)
                    
                    try:
                        os.mkdir(full_path)
                        print(f"Directory '{full_path}' created successfully.")
                        
                        #reload folders and current workspace
                        copy = self.state.copy()
                        
                        contents = os.listdir(workspace_dir)
                        folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
                        copy["workspace_folders"] = folders     
                        copy['current_folder_name'] = folder_name
                
                        #finalize mutation
                        self.state = copy
                        self.global_configs.setValue("workspace_folders",folders)
                        self.state_changed.emit()
                        
                        
                    except FileExistsError:
                        print(f"Directory '{full_path}' already exists.")
                    except OSError as e:
                        print(f"Error creating directory: {e}")
                    
                    
                else:
                    print("Dont do it")
                 
#Globally accessible store instance
store = Store()
store.setParent(QApplication.instance()) #Avoid garbage collection
    