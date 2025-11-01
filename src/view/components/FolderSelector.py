from PySide6 import QtWidgets
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore


class FolderSelector(QtWidgets.QComboBox, UseStore):
    """
    FolderSelector is a custom combo box that displays the list of folders in the workspace.
    It tracks the selected folder and notifies the store of changes.
    The combo box allows for the selection of folders within the workspace.
    """
    
    def __init__(self, parent=None):
        """
        Initializes the FolderSelector widget.

        Args:
            parent: The parent widget (optional).
        """
        super().__init__(parent)

        # List to track the original folder names
        self.items = []

        self.setObjectName("FolderSelector")
        
        # Configure the combo box
        self.setPlaceholderText('Select Folder...')
        self.setStatusTip("Select a folder")
        self.setEditable(False)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

        # Connect the index change event to the handler
        self.currentIndexChanged.connect(self.on_folder_changed)

    def on_folder_changed(self, index):
        """
        Handler for when the folder selection changes.
        Dispatches the selected folder to the store.

        Args:
            index (int): The index of the selected item in the combo box.
        """
        folder = self.items[index]
        self.store_.dispatch(EActionTypes.FOLDER_CHANGED, folder)

    def on_state_changed(self):
        """
        Updates the combo box when the state of the store changes.
        - Refreshes the list of folders.
        - Updates the current selection based on the current folder in the store.
        """
        # Helper function to format folder text for display
        def format(text):
            return './' + text.capitalize()

        # Only update the combo box if the folder list has changed
        if self.items != self.store_.state['workspace_folders']:
            self.items = []  # Reset the list of folders
            self.clear()  # Clear the current items in the combo box

            # Add the updated list of folders to the combo box
            for folder in self.store_.state["workspace_folders"]:
                self.items.append(folder)
                self.addItem(format(folder))

        # Update the selection if the current folder has changed
        current_folder = self.store_.state["current_folder_name"]
        if current_folder is not None and self.currentText() != format(current_folder):    
            # Find the index of the current folder and select it
            try:
                index = self.items.index(current_folder)
                if index > -1:
                    self.setCurrentIndex(index)
            except ValueError:
                pass  # If the folder is not found, we do nothing

