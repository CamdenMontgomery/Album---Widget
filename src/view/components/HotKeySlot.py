from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore
from PySide6.QtCore import Qt, QPoint
from PySide6 import QtWidgets, QtCore
from pyqttooltip import Tooltip, TooltipPlacement


class HotKeySlot(QtWidgets.QPushButton, UseStore):
    """
    A button representing a hotkey slot, displaying the hotkey label and the corresponding folder.
    Allows the user to trigger folder changes based on hotkey actions.
    """
    
    def __init__(self, key='1', parent=None):
        """
        Initializes the HotKeySlot widget with a specific hotkey and parent.

        Args:
            key (str): The hotkey (e.g., '1', '2', etc.) associated with this slot.
            parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setObjectName("HotKeySlot")
        self.setAttribute(Qt.WA_StyledBackground, True)

        # Connect the button click to the onClick method
        self.clicked.connect(self.onClick)

        self.key = key  # Store the key value for the hotkey
        self.layout = QtWidgets.QHBoxLayout(self)
        
        # Icon (displays the hotkey key)
        self.icon = QtWidgets.QLabel(key, self)
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon.setObjectName("HotKeyIcon")
        self.layout.addWidget(self.icon)
        
        # Label (displays the folder name bound to the hotkey)
        self.label = QtWidgets.QLabel('', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyLabel")
        self.layout.addWidget(self.label)
        
        # Tooltip for additional information
        self.tooltip = Tooltip(self, "hi")
        self.tooltip.setPlacement(TooltipPlacement.TOP) 
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(900, 20))
        
    def onClick(self):
        """
        Dispatches an action when the hotkey slot is clicked, triggering the corresponding folder change.
        """
        self.store_.dispatch(EActionTypes.FOLDER_HOTKEY, self.key)

    def setStyleFromState(self, active: bool):
        """
        Updates the style of the widget based on its active state.

        Args:
            active (bool): Whether the hotkey slot is active (selected) or not.
        """
        # Update label style based on whether the slot is active
        self.label.setObjectName("HotKeyLabelActive" if active else "HotKeyLabel")
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        
        # Update button style
        self.setObjectName("HotKeySlotActive" if active else "HotKeySlot")
        self.style().unpolish(self)
        self.style().polish(self)
        
        # Update icon style
        self.icon.setObjectName("HotKeyIconActive" if active else "HotKeyIcon")
        self.icon.style().unpolish(self.icon)
        self.icon.style().polish(self.icon)

    def on_state_changed(self):
        """
        Updates the displayed folder name and active state based on the current hotkey state.
        Also updates the tooltip and cursor based on whether the hotkey is bound to a folder.
        """
        # Set the folder name bound to this hotkey (formatted)
        self.label.setText(self.store_.state['hotkey_folders'][self.key].capitalize())
        
        # Determine if this hotkey is the current active folder
        is_active = self.store_.state['hotkey_folders'][self.key] == self.store_.state['current_folder_name']
        self.setStyleFromState(is_active)  # Update style based on active state
        
        # Check if the hotkey is bound to a folder
        is_bound = self.store_.state['hotkey_folders'][self.key] != ''
        
        # Update the tooltip text based on whether the hotkey is bound
        self.tooltip.setText(f"Jump To Topic '{self.label.text()}' (Alt + {self.key})" if is_bound else "Unbound Hotkey")
        
        # Update the cursor style based on whether the hotkey is bound to a folder
        self.setCursor(Qt.CursorShape.PointingHandCursor if is_bound else Qt.CursorShape.ArrowCursor)
