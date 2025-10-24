import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from utils.styleloader import loadStylesheetsFromFolder
from view.windows.Widget import Widget

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Widget()
    widget.show()
    
    style = loadStylesheetsFromFolder("public/styles")
    app.setStyleSheet(style)

    sys.exit(app.exec())