from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import Qt
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

class FolderSelector(QtWidgets.QComboBox, UseStore):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #track workspace to only update upon change
        self.workspace = None
        
        self.setObjectName("FolderSelector")

        #configuration
        self.setPlaceholderText('Select Folder...')
        self.setStatusTip("Select a folder")
        self.setEditable(False)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        
        #outgoing changes
        self.currentIndexChanged.connect(self.on_folder_changed)
        



    def on_folder_changed(self, index):
        folder = self.itemText(index)
        self.store_.dispatch(EActionTypes.FOLDER_CHANGED, folder)
        print('folder',folder)
        print('chg',self.store_.state)
        
        
    def on_state_changed(self):
        
        #Only update if workspace changed to avoid self.clear calling on_folder_changed and resetting the selection for every update to the state
        if self.workspace == self.store_.state["workspace_dir"]: return
        self.workspace = self.store_.state["workspace_dir"]
        
        #Populate selector with workspace folders
        self.clear()
        for folder in self.store_.state["workspace_folders"]:
            self.addItem(folder)
           
        
    