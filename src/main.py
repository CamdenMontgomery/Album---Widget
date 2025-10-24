import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from utils.styleloader import loadStylesheetsFromFolder
from view.windows.Widget import Widget
from PySide6.QtGui import QFontDatabase, QFont


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    QFontDatabase.addApplicationFont("public/fonts/Nunito-VariableFont_wght.ttf")
    style = loadStylesheetsFromFolder("public/styles")
    app.setStyleSheet(style)
    
    widget = Widget()
    widget.show()

    sys.exit(app.exec())