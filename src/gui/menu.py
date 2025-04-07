from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QSpacerItem


class Menu(QWidget):
    def __init__(self, parent, event_handler, theme, resume=None):
        super(Menu, self).__init__(parent)
        self.parent = parent
        self.event_handler = event_handler
        self.theme = theme
        self.resume = resume
        self.init_ui()

    def init_ui(self):
        style_light = """
            QWidget {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #ffffff;
                color: #139FCE;
                border: 2px solid #139FCE;
                padding: 25px auto 25px auto;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #139FCE;
                color: #ffffff;
                cursor: pointer;
            }
        """
        style_dark = """
            QWidget {
                background-color: #ffffff;
            }
            QPushButton {
                background-color: #ffffff;
                color: #139FCE;
                border: 2px solid #139FCE;
                padding: 25px auto 25px auto;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #139FCE;
                color: #ffffff;
                cursor: pointer;
            }
        """

        style = style_light if self.theme else style_dark
        self.setFixedSize(600, 600)
        self.setStyleSheet(style)

        label = QLabel("SUDOKU")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 40))
        label.setStyleSheet("color: #139FCE;")

        menu_layout = QVBoxLayout()
        menu_layout.addWidget(label)
        menu_layout.addItem(QSpacerItem(0, 100))
        if self.resume is not None:
            button = QPushButton(f"Continue [{self.resume['level']} - {self.resume['time']}]")
            button.setFont(QFont("Arial", 14))
            button.setStyleSheet(style)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda: self.event_handler("resume_game"))
            menu_layout.addWidget(button)

        button = QPushButton("Start")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.start_game)
        menu_layout.addWidget(button)

        button = QPushButton("Settings")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("open_settings"))
        menu_layout.addWidget(button)

        button = QPushButton("Quit")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("quit_game"))
        menu_layout.addWidget(button)

        self.setLayout(menu_layout)

    def start_game(self):
        style_light = """
            QPushButton {
                background-color: #ffffff;
                color: #139FCE;
                border: 1px solid #139FCE;
                padding: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #139FCE;
                color: #ffffff;
            }
        """
        style_dark = """
            QPushButton {
                background-color: #ffffff;
                color: #139FCE;
                border: 1px solid #139FCE;
                padding: 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #139FCE;
                color: #ffffff;
            }
        """

        style = style_light if self.theme else style_dark
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Choose level")
        dialog.setFixedWidth(300)
        dialog.setStyleSheet("padding: 0; margin: 0;")
        dialog_layout = QVBoxLayout()
        dialog_layout.setSpacing(5)

        button = QPushButton("Easy")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=0, dialog=dialog))
        dialog_layout.addWidget(button)

        button = QPushButton("Medium")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=1, dialog=dialog))
        dialog_layout.addWidget(button)

        button = QPushButton("Hard")
        button.setFont(QFont("Arial", 14))
        button.setStyleSheet(style)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=2, dialog=dialog))
        dialog_layout.addWidget(button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

