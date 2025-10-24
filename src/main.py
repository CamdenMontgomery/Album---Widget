import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from view.windows.Widget import Widget

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Widget()
    widget.resize(800, 24)
    widget.show()

    sys.exit(app.exec())