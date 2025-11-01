from utils.UseStore import UseStore
from PySide6.QtCore import Qt
from PySide6 import QtWidgets, QtCore

class HotKeyDisplay(QtWidgets.QWidget, UseStore):
    """
    A widget that displays the current hotkey for the active folder and updates
    its appearance based on the current folder's status.
    """
    def __init__(self, parent=None):
        """
        Initializes the HotKeyDisplay widget.

        Args:
            parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setObjectName("HotKeyDisplay")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # Layout setup
        self.layout = QtWidgets.QHBoxLayout(self)
        
        # Label to display the hotkey
        self.label = QtWidgets.QLabel('', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyDisplayLabel")
        self.layout.addWidget(self.label)

    def setStyleFromState(self, active: bool):
        """
        Updates the style of the widget based on whether it is active or not.

        Args:
            active (bool): True if the widget should be styled as active, False otherwise.
        """
        # Update the label's style based on active state
        self.label.setObjectName("HotKeyDisplayLabelActive" if active else "HotKeyDisplayLabel")
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        
        # Update the widget's style based on active state
        self.setObjectName("HotKeyDisplayActive" if active else "HotKeyDisplay")
        self.style().unpolish(self)
        self.style().polish(self)

    def on_state_changed(self):
        """
        Updates the displayed hotkey based on the current folder state and whether
        the folder is assigned to a hotkey.
        """
        hotkey_folders = self.store_.state['hotkey_folders']
        current_folder = self.store_.state['current_folder_name']
        
        # Check if the current folder is in the hotkey folders
        folders = list(hotkey_folders.values())
        
        if current_folder in folders:
            # Find the index of the current folder in the hotkey list
            index = folders.index(current_folder)
            self.label.setText(f'Alt + {index + 1}')
            self.setStyleFromState(True)  # Mark the widget as active
        else:
            self.label.setText('...')  # Indicate no hotkey assigned
            self.setStyleFromState(False)  # Mark the widget as inactive
