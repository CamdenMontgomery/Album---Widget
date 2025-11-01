from pathlib import Path
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QDialog, QApplication
from enums.EActionTypes import EActionTypes
import os

from utils.persist import getGlobalConfigsRef, getLocalConfigsRef, getStateFromConfigs
from view.windows.Flashcard import Flashcard
from view.windows.Note import Note
from view.windows.Snipping import SnippingOverlay
from view.components.Dialog import Dialog, DIALOG_TYPES

# Initial state model
MODEL = {
    "ready": False,
    "workspace_dir": None,
    "workspace_folders": [],
    "current_folder_name": None,
    "hotkey_folders": {'1': '', '2': '', '3': '', '4': '', '5': ''},
    "show_widget": True
}


class Store(QObject):
    """
    This class manages the state of the application and handles the dispatch of actions
    to mutate the state based on various events, such as selecting folders, starting snapshots, 
    opening notes, and managing hotkeys and folders.
    """
    
    show_widget = Signal()
    hide_widget = Signal()
    state_changed = Signal()

    def __init__(self):
        """
        Initializes the Store class by loading configuration files and setting up the initial state.
        """
        super().__init__()
        self.state = getStateFromConfigs()  # Load persisted state
        self.global_configs = getGlobalConfigsRef()
        self.local_configs = getLocalConfigsRef()
        self.state_changed.emit()

    def dispatch(self, action_type, payload):
        """
        Dispatches an action to be processed by the controller.
        
        Args:
            action_type (str): The type of action to process.
            payload (any): The data associated with the action.
        """
        self._controller(action_type, payload)

    def _controller(self, action_type, payload):
        """
        Processes actions to mutate the state based on action types.
        
        Args:
            action_type (str): The action type to process.
            payload (any): The data associated with the action.
        """
        match action_type:
            case EActionTypes.OPEN_WORKSPACE_SELECTOR: 
                # Prepare for mutation
                copy = self.state.copy()

                # Open file dialog to select a folder
                folder_path = QFileDialog.getExistingDirectory(None, "Select Directory", copy["workspace_dir"] or "")
                if not folder_path:
                    return

                copy["workspace_dir"] = folder_path

                # Get workspace folders
                contents = os.listdir(folder_path)
                folders = [name for name in contents if os.path.isdir(os.path.join(folder_path, name))]
                copy["workspace_folders"] = folders

                # Update global configs to reflect the new workspace
                self.global_configs.setValue("workspace_dir", folder_path)
                self.global_configs.setValue("workspace_folders", folders)

                # Reload local configs for the new workspace
                self.local_configs = getLocalConfigsRef()

                # Get and update hotkeys
                copy['hotkey_folders'] = self.local_configs.value('hotkey_folders') or MODEL['hotkey_folders']
                self.local_configs.setValue('hotkey_folders', copy['hotkey_folders'])

                # Finalize mutation
                self.state = copy
                self.state_changed.emit()

            case EActionTypes.FOLDER_CHANGED:
                # Update current folder and mark workspace as ready
                copy = self.state.copy()
                copy['current_folder_name'] = payload
                copy['ready'] = True
                self.state = copy  
                self.state_changed.emit()
                self.global_configs.setValue("current_folder_name", payload)

            case EActionTypes.HIDE_WIDGET:
                # Hide the widget
                copy = self.state.copy()
                copy['show_widget'] = False
                self.hide_widget.emit()
                self.state = copy                

            case EActionTypes.SHOW_WIDGET:
                # Show the widget
                copy = self.state.copy()
                copy['show_widget'] = True
                self.show_widget.emit()
                self.state = copy  

            case EActionTypes.BEGIN_SNAPSHOT:
                # Begin a screenshot session if the workspace is ready
                if not self.state['ready']:
                    return

                save_path = os.path.join(self.state['workspace_dir'], self.state['current_folder_name'])
                self.snipping_overlay = SnippingOverlay(path=save_path)
                self.snipping_overlay.show()

            case EActionTypes.OPEN_NOTES:
                # Open the notes window for the current folder
                if not self.state['ready']:
                    return

                save_path = os.path.join(self.state['workspace_dir'], self.state['current_folder_name'])
                self.note = Note(path=save_path)
                self.note.show()

            case EActionTypes.NEW_FLASHCARD:
                # Open the flashcard window for the current folder
                if not self.state['ready']:
                    return

                save_path = os.path.join(self.state['workspace_dir'], self.state['current_folder_name'])
                self.flashcard = Flashcard(path=save_path)
                self.flashcard.show()

            case EActionTypes.TOGGLE_PIN:
                # Toggle whether the current folder is pinned in hotkeys
                hotkey_folders = self.state['hotkey_folders']
                current_folder = self.state['current_folder_name']
                folders = list(hotkey_folders.values())

                if current_folder in folders:
                    # If the folder is pinned, unpin it
                    index = folders.index(current_folder)
                    copy = self.state.copy()
                    copy['hotkey_folders'][str(index + 1)] = ""
                    self.state = copy   
                else:
                    # If the folder is not pinned, pin it
                    index = folders.index("")
                    copy = self.state.copy()
                    copy['hotkey_folders'][str(index + 1)] = current_folder
                    self.state = copy   

                self.state_changed.emit()
                self.local_configs.setValue("hotkey_folders", self.state['hotkey_folders'])

            case EActionTypes.FOLDER_HOTKEY:
                # Handle folder hotkey by switching to the folder associated with the hotkey
                hotkey_folders = self.state['hotkey_folders']
                go_to_folder = hotkey_folders[str(payload)]
                if go_to_folder != '':
                    self.dispatch(EActionTypes.FOLDER_CHANGED, go_to_folder)

            case EActionTypes.TOOL_HOTKEY:
                # Handle tool-specific hotkey actions (snapshot, notes, flashcards)
                match payload:
                    case 'z': 
                        self.dispatch(EActionTypes.BEGIN_SNAPSHOT, None)
                    case 'x': 
                        self.dispatch(EActionTypes.OPEN_NOTES, None)
                    case 'c': 
                        self.dispatch(EActionTypes.NEW_FLASHCARD, None)

            case EActionTypes.REMOVE_FOLDER:
                # Prompt the user to confirm folder removal and delete it
                title = "Delete This Folder?"
                message = f"""Deleting '{self.state['current_folder_name']}' will permanently remove it from this workspace and your computer. This action cannot be undone. Are you sure you want to proceed?"""
                confirm_text = "Yes, Delete It"
                reject_text = "No, Keep It"

                warning = Dialog(title, message, confirm_text, reject_text, DIALOG_TYPES.WARNING)
                result = warning.exec()

                if result == QDialog.DialogCode.Accepted:
                    workspace_dir = self.state['workspace_dir']
                    folder_name = self.state['current_folder_name']
                    full_path = os.path.join(workspace_dir, folder_name)

                    try:
                        if not os.path.exists(full_path):
                            raise FileNotFoundError

                        os.rmdir(full_path)

                        # Reload workspace folders after deletion
                        copy = self.state.copy()
                        contents = os.listdir(workspace_dir)
                        folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
                        copy["workspace_folders"] = folders

                        # Update hotkeys if the deleted folder was pinned
                        hotkey_folders = self.state['hotkey_folders']
                        if folder_name in list(hotkey_folders.values()):
                            index = list(hotkey_folders.values()).index(folder_name)
                            copy['hotkey_folders'][str(index + 1)] = ""
                        
                        copy['current_folder_name'] = folders[0] or ''
                        self.state = copy

                        # Update global configs
                        self.global_configs.setValue("workspace_folders", folders)
                        self.state_changed.emit()

                    except FileExistsError:
                        print(f"Directory '{full_path}' does not exist.")
                    except OSError as e:
                        print(f"Error removing directory: {e}")

            case EActionTypes.ADD_FOLDER:
                # Prompt the user to create a new folder and add it to the workspace
                title = "New Folder"
                message = "What is the name of this folder? It should be named relative to the topic you are studying."
                confirm_text = "Create"
                reject_text = "Cancel"

                input = Dialog(title, message, confirm_text, reject_text, DIALOG_TYPES.INPUT)
                result = input.exec()

                if result == QDialog.DialogCode.Accepted:
                    workspace_dir = self.state['workspace_dir']
                    folder_name = input.getResultingText().replace('.', '')  # Remove extensions
                    full_path = os.path.join(workspace_dir, folder_name)

                    try:
                        os.mkdir(full_path)

                        # Reload workspace folders and update current folder
                        copy = self.state.copy()
                        contents = os.listdir(workspace_dir)
                        folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
                        copy["workspace_folders"] = folders

                        copy["current_folder_name"] = folder_name
                        self.state = copy

                        # Update global configs
                        self.global_configs.setValue("workspace_folders", folders)
                        self.state_changed.emit()

                    except FileExistsError:
                        print(f"Folder '{full_path}' already exists.")
                    except OSError as e:
                        print(f"Error creating folder: {e}")

#Globally accessible store instance
store = Store()
store.setParent(QApplication.instance()) #Avoid garbage collection
    