from enums.EActionTypes import EActionTypes
from view.components.ToolbarButton import ToolbarButton


class ToolBarButtonFactory:
    def __init__(self, prefix_path="public/icons/"):
        self.prefix_path = prefix_path
        
    def createAddFolderButton(self):
        return ToolbarButton(self.prefix_path + "add_folder.svg", EActionTypes.ADD_FOLDER)
    
    def createRemoveFolderButton(self):
        return ToolbarButton(self.prefix_path + "remove_folder.svg", EActionTypes.REMOVE_FOLDER)
    