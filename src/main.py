import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from view.Widget import Widget

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Widget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())