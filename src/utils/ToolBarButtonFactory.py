from enums.EActionTypes import EActionTypes
from view.components.ToolbarButton import ToolbarButton


class ToolBarButtonFactory:
    def __init__(self, prefix_path="public/icons/"):
        self.prefix_path = prefix_path
        
    def createAddFolderButton(self):
        return ToolbarButton(self.prefix_path + "add_folder.svg", EActionTypes.ADD_FOLDER)
    
    def createRemoveFolderButton(self):
        return ToolbarButton(self.prefix_path + "remove_folder.svg", EActionTypes.REMOVE_FOLDER)
    
    
    def createSnapshotButton(self):
        return ToolbarButton(self.prefix_path + "take_snapshot.svg", EActionTypes.BEGIN_SNAPSHOT)
    
    def createNoteButton(self):
        return ToolbarButton(self.prefix_path + "open_note.svg", EActionTypes.OPEN_NOTES)
    
    def createFlashcardButton(self):
        return ToolbarButton(self.prefix_path + "make_flashcard.svg", EActionTypes.NEW_FLASHCARD)
    