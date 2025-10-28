import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from utils.hotkeys import HotKeyManager
from utils.styleloader import loadStylesheetsFromFolder
from view.windows.Widget import Widget
from PySide6.QtGui import QFontDatabase, QFont
from utils.summon import HoverStateManager
from utils.basepath import BASE_PATH
from os import path

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    


    #enable hover state show/hide tracking
    hover = HoverStateManager()
    
    #enable hotkeys
    hotkeys = HotKeyManager()

    #load fonts
    font_path = path.join(BASE_PATH,"public","fonts","Nunito-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(font_path)
    
    #load styles
    style_path = path.join(BASE_PATH,"public","styles")
    style = loadStylesheetsFromFolder(style_path)
    app.setStyleSheet(style)
    
    #activate main window
    widget = Widget()
    widget.show()


    sys.exit(app.exec())