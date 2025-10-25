from PySide6 import QtWidgets, QtGui
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

class FolderSelector(QtWidgets.QComboBox, UseStore):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FolderSelector")

        #configuration
        self.setStatusTip("Select a folder")
        self.setEditable(False)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        
        #outgoing changes
        self.currentIndexChanged.connect(self.on_folder_changed)
        
        #incoming changes
        self.store_.state_changed.connect(self.on_state_changed)


    def on_folder_changed(self, index):
        folder_path = self.itemText(index)
        self.store_.dispatch(EActionTypes.FOLDER_CHANGED, folder_path)
        
        
    def on_state_changed(self):
        self.clear()
        for folder in self.store_.state["workspace_folders"]:
            self.addItem(folder)
        
    