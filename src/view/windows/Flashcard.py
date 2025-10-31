from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect 


from utils.cleaning import cleanFlashcardContent
from view.components.GrabHandle import GrabHandle

from utils.basepath import BASE_PATH
from os import path

CLOSE_ICON = path.join(BASE_PATH,"public","icons","close.svg")
CONFIRM_ICON = path.join(BASE_PATH,"public","icons","check.svg")

class Flashcard(QtWidgets.QWidget):
    def __init__(self, path):
        super().__init__()
        
        self.save_path = path
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("FlashcardWindow")
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        
        #Header
        self.header = QtWidgets.QWidget()
        self.header.setObjectName('FlashcardHeader')
        self.header_layout = QtWidgets.QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(20, 20, 20, 20)
        
        
        #--New Flashcard Label
        self.new_flashcard_label = QtWidgets.QLabel('New Flashcard')
        self.new_flashcard_label.setObjectName('FlashcardLabel')
        self.header_layout.addWidget(self.new_flashcard_label)
        
        #--Confirm Button
        self.confirm_button = QtWidgets.QPushButton()
        self.confirm_button.setIcon(QtGui.QIcon(CONFIRM_ICON))
        self.confirm_button.setIconSize(QSize(24, 24))
        self.confirm_button.setObjectName('FlashcardConfirmButton')
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.clicked.connect(lambda: self.saveFlashcard())
        self.header_layout.addWidget(self.confirm_button)
        
        #--Close Button
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.setObjectName('FlashcardCloseButton')
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(lambda: self.close())
        self.header_layout.addWidget(self.close_button)
        
        
        #-- Grab Handle
        self.grab_handle = GrabHandle(self)
        self.header_layout.addWidget(self.grab_handle)
        
        self.window_layout.addWidget(self.header)
        
        #Body
        self.body = QtWidgets.QWidget()
        self.body.setObjectName("FlashcardBody")
        self.body_layout = QtWidgets.QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(20, 20, 20, 20)
        self.body_layout.setSpacing(20)
        
        #--Question Text Area
        self.question_text = QtWidgets.QTextEdit()
        self.question_text.setPlaceholderText('Question...')
        self.question_text.setObjectName("FlashcardTextArea")
        self.body_layout.addWidget(self.question_text)
        
        #--Answer Text Area
        self.answer_text = QtWidgets.QTextEdit()
        self.answer_text.setPlaceholderText('Answer...')
        self.answer_text.setObjectName("FlashcardTextArea")
        self.body_layout.addWidget(self.answer_text)
        
        self.window_layout.addWidget(self.body)
        
    def saveFlashcard(self):
        
        #Save to the quizlet.txt fil in the folder
        question = cleanFlashcardContent(self.question_text.toPlainText())
        answer = cleanFlashcardContent(self.answer_text.toPlainText())
        
        #Get Filepath to save to in this folder
        file_name = "export.quizlet.txt" 
        file_path = os.path.join(self.save_path, file_name)
        
        #save to txt
        with open(file_path, "a") as file:
            file.write("\n" + question + "\t" + answer)

        self.close()