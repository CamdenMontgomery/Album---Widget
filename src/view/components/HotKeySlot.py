
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore
from PySide6.QtCore import Qt, QPoint
from PySide6 import QtWidgets, QtCore
from pyqttooltip import Tooltip, TooltipPlacement


class HotKeySlot(QtWidgets.QPushButton, UseStore):
    def __init__(self, key='1', parent=None):
        super().__init__(parent)
        self.setObjectName("HotKeySlot")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.clicked.connect(self.onClick)
        
        self.key = key
        self.layout = QtWidgets.QHBoxLayout(self)
        
        
        self.icon = QtWidgets.QLabel(key, self)
        self.icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.icon.setObjectName("HotKeyIcon")
        self.layout.addWidget(self.icon)
        
        self.label = QtWidgets.QLabel('', self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("HotKeyLabel")
        self.layout.addWidget(self.label)
        
        
        
        
        self.tooltip = Tooltip(self, "hi")
        self.tooltip.setPlacement(TooltipPlacement.TOP) 
        self.tooltip.setOffsetByPlacement(TooltipPlacement.TOP, QPoint(900, 20))
        
        
    def onClick(self):
        self.store_.dispatch(EActionTypes.FOLDER_HOTKEY, self.key)

        
    def setStyleFromState(self, active: bool):
        self.label.setObjectName("HotKeyLabelActive" if active else "HotKeyLabel")
        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)
        
        self.setObjectName("HotKeySlotActive" if active else "HotKeySlot")
        self.style().unpolish(self)
        self.style().polish(self)
        
        self.icon.setObjectName("HotKeyIconActive" if active else "HotKeyIcon")
        self.icon.style().unpolish(self.icon)
        self.icon.style().polish(self.icon)
        

       
        
    def on_state_changed(self):
        self.label.setText(self.store_.state['hotkey_folders'][self.key].capitalize())
        is_active = self.store_.state['hotkey_folders'][self.key] == self.store_.state['current_folder_name']
        self.setStyleFromState(is_active)  
        
        #If the hotkey has a folder it is bound to, add extra styling
        is_bound = self.store_.state['hotkey_folders'][self.key] != ''
        
        #Update Tooltip
        self.tooltip.setText(f"Jump To Topic '{self.label.text()}' (Alt + {self.key})" if is_bound else "Unbound Hotkey")
        
        #Update Cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor if is_bound else Qt.CursorShape.ArrowCursor)
        

            