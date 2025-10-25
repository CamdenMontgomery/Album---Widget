from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime



class Note(QtWidgets.QWidget):
    def __init__(self, path):
        super().__init__()
        
        self.window_layout = QtWidgets.QVBoxLayout(self)
        
        
        #Header
        self.header = QtWidgets.QWidget()
        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        
        #--New Note Label
        self.new_note_label = QtWidgets.QLabel('New Note')
        self.header_layout.addWidget(self.new_note_label)
        
        #--Confirm Button
        self.confirm_button = QtWidgets.QPushButton()
        self.header_layout.addWidget(self.confirm_button)
        
        #--Close Button
        self.close_button = QtWidgets.QPushButton()
        self.header_layout.addWidget(self.close_button)
        
        self.window_layout.addWidget(self.header)
        
        #Body
        self.body = QtWidgets.QWidget()
        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        
        #--TextArea
        self.text_area = QtWidgets.QPlainTextEdit()
        self.body_layout.addWidget(self.text_area)
        
        self.window_layout.addWidget(self.body)
        
        