from PySide6 import QtGui

class ANewFolder(QtGui.QAction):
    def __init__(self, parent=None):
        super().__init__("New Folder", parent)
        self.setShortcut("Ctrl+N")
        self.setStatusTip("Create a new folder")
        self.triggered.connect(self.trigger)
        
    def trigger():
        print("New Folder action triggered")