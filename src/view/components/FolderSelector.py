from PySide6 import QtWidgets, QtGui
from PySide6.QtGui import Qt
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore


#Notes
# uses internal items array to track the actual names of the folders in the list so it can display formatted text in the combobox and dropdown
class FolderSelector(QtWidgets.QComboBox, UseStore):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.items = [] #Track the original values of the items 
        
        self.setObjectName("FolderSelector")

        #configuration
        self.setPlaceholderText('Select Folder...')
        self.setStatusTip("Select a folder")
        self.setEditable(False)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        
        #outgoing changes
        self.currentIndexChanged.connect(self.on_folder_changed)
        



    def on_folder_changed(self, index):
        folder = self.items[index]
        self.store_.dispatch(EActionTypes.FOLDER_CHANGED, folder)
        print('folder',folder)
        print('chg',self.store_.state)
        
        
    def on_state_changed(self):
        
        #Text in the selector will be in this format so to compare the text in th selector we must format what were comparing it to
        def format(text): return './' + text.capitalize()
        
        #Only update if folder list changed to avoid self.clear calling on_folder_changed and resetting the selection for every update to the state
        if self.items != self.store_.state['workspace_folders']:
            #Populate selector with workspace folders
            self.items = []
            self.clear()
            for folder in self.store_.state["workspace_folders"]:
                self.items.append(folder)
                self.addItem(format(folder))
        

        
        #Update selection if current folder changed
        current_folder = self.store_.state["current_folder_name"]
        
        if current_folder != None and  self.currentText() != format(current_folder):    
            index = self.items.index(current_folder)
            if index > -1: self.setCurrentIndex(index)
        

        

           
        
    