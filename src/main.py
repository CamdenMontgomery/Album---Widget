import sys
from os import path
from PySide6 import QtWidgets
from PySide6.QtGui import QFontDatabase

# Utility imports
from utils.summon import HoverStateManager
from utils.hotkeys import HotKeyManager
from utils.basepath import BASE_PATH
from utils.styleloader import loadStylesheetsFromFolder

# View imports
from view.windows.Widget import Widget

def main():
    """
    Initializes the application, sets up necessary utilities, 
    loads fonts and styles, and launches the main window.
    """
    # Create the Qt application
    app = QtWidgets.QApplication([])

    # Enable hover state tracking (for hover-based UI features)
    hover = HoverStateManager()
    
    # Enable global hotkey functionality
    hotkeys = HotKeyManager()

    # Load custom font
    font_path = path.join(BASE_PATH, "public", "fonts", "Nunito-VariableFont_wght.ttf")
    QFontDatabase.addApplicationFont(font_path)
    
    # Load and apply stylesheets from the styles folder
    style_path = path.join(BASE_PATH, "public", "styles")
    style = loadStylesheetsFromFolder(style_path)
    app.setStyleSheet(style)
    
    # Create and show the main application window
    widget = Widget()
    widget.show()

    # Start the application's event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
