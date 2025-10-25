import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from utils.styleloader import loadStylesheetsFromFolder
from view.windows.Widget import Widget
from PySide6.QtGui import QFontDatabase, QFont
from utils.summon import HoverStateManager


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    #enable hover state show/hide tracking
    manager = HoverStateManager()

    #load fonts
    QFontDatabase.addApplicationFont("public/fonts/Nunito-VariableFont_wght.ttf")
    
    #load styles
    style = loadStylesheetsFromFolder("public/styles")
    app.setStyleSheet(style)
    
    #activate main window
    widget = Widget()
    widget.show()


    sys.exit(app.exec())