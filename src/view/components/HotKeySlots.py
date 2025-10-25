from PySide6 import QtWidgets
from view.components.HotKeySlot import HotKeySlot

class HotKeySlots(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HotKeySlots")
        
        self.layout = QtWidgets.QHBoxLayout(self)
        
        self.slot1 = HotKeySlot('1', self)
        self.layout.addWidget(self.slot1)
        
        self.slot2 = HotKeySlot('2', self)
        self.layout.addWidget(self.slot2)
        
        self.slot3 = HotKeySlot('3', self)
        self.layout.addWidget(self.slot3)
        
        self.slot4 = HotKeySlot('4', self)
        self.layout.addWidget(self.slot4)
        
        self.slot5 = HotKeySlot('5', self)
        self.layout.addWidget(self.slot5)
            

        

