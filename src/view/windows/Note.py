from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect

from view.components.GrabHandle import GrabHandle 
from utils.basepath import BASE_PATH
from os import path

CLOSE_ICON = path.join(BASE_PATH,"public","icons","close.svg")
CONFIRM_ICON = path.join(BASE_PATH,"public","icons","check.svg")

class Note(QtWidgets.QWidget):
    def __init__(self, path):
        super().__init__()
        
        self.save_path = path
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("NoteWindow")
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        
        #Header
        self.header = QtWidgets.QWidget()
        self.header.setObjectName('NoteHeader')
        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(20, 20, 20, 20)
        
        
        #--New Note Label
        self.new_note_label = QtWidgets.QLabel('New Note')
        self.new_note_label.setObjectName('NoteLabel')
        self.header_layout.addWidget(self.new_note_label)
        
        #--Confirm Button
        self.confirm_button = QtWidgets.QPushButton()
        self.confirm_button.setIcon(QtGui.QIcon(CONFIRM_ICON))
        self.confirm_button.setIconSize(QSize(24, 24))
        self.confirm_button.setObjectName('NoteConfirmButton')
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(lambda: self.saveNote())
        self.header_layout.addWidget(self.confirm_button)
        
        #--Close Button
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setObjectName('NoteCloseButton')
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(lambda: self.close())
        self.header_layout.addWidget(self.close_button)
        
        
        #-- Grab Handle
        self.grab_handle = GrabHandle(self)
        self.header_layout.addWidget(self.grab_handle)

        self.window_layout.addWidget(self.header)
        
        #Body
        self.body = QtWidgets.QWidget()
        self.body.setObjectName("NoteBody")
        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(20, 20, 20, 20)
        
        #--TextArea
        self.text_area = QtWidgets.QPlainTextEdit()
        self.text_area.setPlaceholderText('Content...')
        self.text_area.setObjectName("NoteTextArea")
        self.body_layout.addWidget(self.text_area)
        
        
        self.window_layout.addWidget(self.body)
        
    def saveNote(self):
        
        contents = self.text_area.toPlainText()
        
        #generate filename
        chunk = contents[0:10]
        filename = chunk + ".txt"
        file_path = os.path.join(self.save_path, filename)
        
        #save to txt
        with open(file_path, "w") as file:
            file.write(contents)

        self.close()