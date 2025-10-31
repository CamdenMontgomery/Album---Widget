from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QColor, QPen
import os
from datetime import datetime
from PySide6.QtWidgets import QWidget, QGraphicsDropShadowEffect

from view.components.GrabHandle import GrabHandle 

from enum import Enum, unique

from utils.basepath import BASE_PATH
from os import path

CLOSE_ICON = path.join(BASE_PATH,"public","icons","close.svg")


@unique
class DIALOG_TYPES(Enum):
    WARNING = 1
    MESSAGE = 2
    INPUT = 3



class Dialog(QtWidgets.QDialog):
    def __init__(self, title: str, message: str, confirmText: str = "OK", rejectText:str = "Cancel", type: int = 2):
        super().__init__()
        
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("DialogWindow")
        self.window_layout = QtWidgets.QVBoxLayout(self)
        self.window_layout.setContentsMargins(0, 0, 0, 0)
        self.window_layout.setSpacing(0)
        
        #Container / Background
        self.container = QtWidgets.QWidget()
        self.container.setObjectName("DialogContainer")
        self.container_layout = QtWidgets.QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(30, 30, 30, 30)
        self.container_layout.setSpacing(30)
        self.window_layout.addWidget(self.container)
        
        #--Title Container
        self._title_widget = QtWidgets.QWidget()
        self._title_layout = QtWidgets.QHBoxLayout(self._title_widget)
        self._title_layout.setContentsMargins(0, 0, 0, 0)
        self._title_layout.setSpacing(8)
        
        
        #----Title Display
        self.title_display = QtWidgets.QLabel()
        self.title_display.setObjectName("DialogTitleDisplay")
        self.title_display.setText(title)
        self._title_layout.addWidget(self.title_display)
        
        #----Spacer
        self._title_layout.addStretch()
        
        #----Close Button
        self.close_button = QtWidgets.QPushButton()
        self.close_button.setObjectName("DialogCloseButton")
        self.close_button.setIcon(QtGui.QIcon(CLOSE_ICON))
        self.close_button.setIconSize(QSize(24, 24))
        self.close_button.clicked.connect(self.reject)
        self._title_layout.addWidget(self.close_button)
        
        
        self.container_layout.addWidget(self._title_widget)
        
        
        #--Message Display
        self.message_display = QtWidgets.QLabel()
        self.message_display.setObjectName("DialogMessageDisplay")
        self.message_display.setWordWrap(True)
        self.message_display.setText(message)
        self.message_display.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.container_layout.addWidget(self.message_display)


        #--Text Input (only used for INPUT dialog type)
        if type == DIALOG_TYPES.INPUT:
            self.text_input = QtWidgets.QLineEdit()
            self.text_input.setObjectName("DialogTextInput")
            self.text_input.setPlaceholderText("...")
            self.container_layout.addWidget(self.text_input)

        #--Buttons container
        self._buttons_widget = QtWidgets.QWidget()
        self._buttons_layout = QtWidgets.QHBoxLayout(self._buttons_widget)
        self._buttons_layout.setContentsMargins(0, 0, 0, 0)
        self._buttons_layout.setSpacing(8)

        #----Spacer to push buttons to the right
        self._buttons_layout.addStretch()

        #----Confirm Button
        self.confirm_button = QtWidgets.QPushButton(confirmText)
        self.confirm_button.setObjectName("DialogConfirmButton")
        self._buttons_layout.addWidget(self.confirm_button)
        self.confirm_button.clicked.connect(self.onConfirm)
        
        #----Reject Button
        self.reject_button = QtWidgets.QPushButton(rejectText)
        self.reject_button.setObjectName("DialogRejectButton")
        self.reject_button.clicked.connect(self.onReject)
        self._buttons_layout.addWidget(self.reject_button)




        self.container_layout.addWidget(self._buttons_widget)



        # window flags and basic sizing
        self.setModal(True)
        self.resize(400, 120)

    def onConfirm(self):
        """Handle confirm button click. For INPUT dialogs, the text is stored on accept()."""
        # If text input visible, ensure value can be retrieved by caller
        if hasattr(self, "text_input"): self._result_text = self.text_input.text()
        self.accept()

    def onReject(self):
        """Handle reject/close actions."""
        self._result_text = None
        self.reject()

    def getResultingText(self) -> str | None:
        """Return text entered by the user (or None if none). Call after exec()."""
        return getattr(self, "_result_text", None)
        
        