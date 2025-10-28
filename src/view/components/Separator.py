from PySide6 import QtWidgets
from PySide6.QtGui import Qt
class Separator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Separator")
        self.setAttribute(Qt.WA_StyledBackground, True)
            