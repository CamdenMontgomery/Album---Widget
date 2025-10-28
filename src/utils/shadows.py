from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
      
        
class MidshadeShadow(QGraphicsDropShadowEffect):
    def __init__(self):
        super().__init__()
        self.setBlurRadius(50)  # Adjust the blur radius as needed
        self.setXOffset(0)      # Adjust the X offset as needed
        self.setYOffset(5)      # Adjust the Y offset as needed
        self.setColor(QColor(150, 150, 150, 100))