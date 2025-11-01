from PySide6 import QtWidgets
from view.components.HotKeySlot import HotKeySlot

class HotKeySlots(QtWidgets.QWidget):
    """
    A widget that holds multiple hotkey slots (buttons) to trigger folder changes.
    It dynamically creates a set of HotKeySlot widgets and displays them in a horizontal layout.
    """
    
    def __init__(self, parent=None):
        """
        Initializes the HotKeySlots widget, creating five HotKeySlot buttons by default.
        
        Args:
            parent (QtWidgets.QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        
        self.setObjectName("HotKeySlots")
        
        # Create a horizontal layout to hold the hotkey slots
        self.layout = QtWidgets.QHBoxLayout(self)
        
        # List of keys (hotkeys) to generate slots for
        keys = ['1', '2', '3', '4', '5']
        
        # Dynamically create HotKeySlot widgets for each key
        for key in keys:
            slot = HotKeySlot(key, self)
            self.layout.addWidget(slot)
        
        # Set layout properties for spacing and margins
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
