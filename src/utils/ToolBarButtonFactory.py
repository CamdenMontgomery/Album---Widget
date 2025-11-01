from enums.EActionTypes import EActionTypes
from view.components.ToolbarButton import ToolbarButton
from utils.basepath import BASE_PATH
from os import path

class ToolBarButtonFactory:
    """
    Factory class to create different toolbar buttons with associated icons and actions.
    """

    def __init__(self, prefix_path: str = path.join(BASE_PATH, 'public', 'icons')):
        """
        Initialize the factory with a given prefix path for icons.

        Args:
            prefix_path (str): The base directory where icons are stored. Defaults to BASE_PATH.
        """
        self.prefix_path = prefix_path

    def _create_button(self, icon_name: str, action_type: EActionTypes, tooltip: str) -> ToolbarButton:
        """
        Helper function to create a toolbar button with the provided parameters.

        Args:
            icon_name (str): The name of the icon file (without path).
            action_type (EActionTypes): The action type to associate with the button.
            tooltip (str): The tooltip to display on hover.

        Returns:
            ToolbarButton: The created toolbar button.
        """
        icon_path = path.join(self.prefix_path, icon_name)
        return ToolbarButton(icon_path, action_type, tooltip)

    def createAddFolderButton(self) -> ToolbarButton:
        """Create a toolbar button for adding a folder."""
        return self._create_button("add_folder.svg", EActionTypes.ADD_FOLDER, "Add Folder To Workspace")

    def createRemoveFolderButton(self) -> ToolbarButton:
        """Create a toolbar button for removing a folder."""
        return self._create_button("remove_folder.svg", EActionTypes.REMOVE_FOLDER, "Remove Folder From Workspace")

    def createSnapshotButton(self) -> ToolbarButton:
        """Create a toolbar button for taking a screenshot."""
        return self._create_button("take_snapshot.svg", EActionTypes.BEGIN_SNAPSHOT, "Snip Screen (Alt + Z)")

    def createNoteButton(self) -> ToolbarButton:
        """Create a toolbar button for opening notes."""
        return self._create_button("open_note.svg", EActionTypes.OPEN_NOTES, "Create Note (Alt + X)")

    def createFlashcardButton(self) -> ToolbarButton:
        """Create a toolbar button for creating a flashcard."""
        return self._create_button("make_flashcard.svg", EActionTypes.NEW_FLASHCARD, "Create Flashcard (Alt + C)")
