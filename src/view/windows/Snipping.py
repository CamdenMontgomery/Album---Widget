from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime


OVERLAY_COLOR = QColor(255, 255, 255, 100)
SELECTION_COLOR = QColor(255, 127, 80, 100)

class SnippingOverlay(QtWidgets.QWidget):
    
    def __init__(self, path):
        super().__init__()

        #path to save the snippet to
        self.save_path = path

        self.snip_top_left = QPoint(0,0)
        self.snip_bottom_right = QPoint(0,0)
        
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowFullScreen)
        
        screen = QApplication.instance().primaryScreen()
        self.freeze_screen = screen.grabWindow(0)

        
    def paintEvent(self, event):
        
        painter = QPainter(self)
        
        #Draw Frozen Screen
        painter.drawPixmap(0, 0, self.freeze_screen)
        painter.fillRect(self.rect(), OVERLAY_COLOR)
        
        #Draw Transparent Overlay
        selection_rect = QRect(self.snip_top_left, self.snip_bottom_right)
        
        #Draw Selection Box
        pen = QPen(SELECTION_COLOR)  
        pen.setWidth(2)
        pen.setStyle(Qt.DashLine) 
        painter.setPen(pen)
        painter.fillRect(selection_rect, SELECTION_COLOR)
        painter.drawRect(selection_rect.normalized())
        

    def mousePressEvent(self, event):
        self.snip_top_left = event.pos()
        self.mousePressEvent = None
        
    def mouseMoveEvent(self, event):
        if hasattr(self, "snip_top_left"):
            self.snip_bottom_right = event.pos()
            self.update()
    

    def mouseReleaseEvent(self, event):
        self.snip_bottom_right = event.pos()
        self.mouseReleaseEvent = None
        
        #Crop freeze screen to selection
        selection_rect = QRect(self.snip_top_left, self.snip_bottom_right)
        snippet = self.freeze_screen.copy(selection_rect)
        
        #generate filename
        now = datetime.now()
        timestamp = now.strftime("%H-%M-%S_%Y-%m-%d")
        filename = timestamp + ".png"
        
        #save to png
        snippet.save(os.path.join(self.save_path, filename), 'PNG')
        
        self.close()
