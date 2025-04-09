from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QSpacerItem


class Menu(QWidget):
    def __init__(self, parent, event_handler, styles, theme, resume=None):
        super(Menu, self).__init__(parent)
        self.parent = parent
        self.event_handler = event_handler
        self.theme = theme
        self.resume = resume
        self.styles = styles
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(600, 600)
        self.setStyleSheet(self.styles)
        self.setProperty("class", f"body_{self.theme}")
        print(self.property("class"))

        label = QLabel("SUDOKU")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 40))

        menu_layout = QVBoxLayout()
        menu_layout.addWidget(label)
        menu_layout.addItem(QSpacerItem(0, 100))
        if self.resume is not None:
            button = QPushButton(f"Continue [{self.resume['level']} - {self.resume['time']}]")
            button.setStyleSheet(self.styles)
            button.setProperty("class", f"main_button_{self.theme}")
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda: self.event_handler("resume_game"))
            menu_layout.addWidget(button)

        button = QPushButton("Start")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"main_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.start_game)
        menu_layout.addWidget(button)

        button = QPushButton("Settings")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"main_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("open_settings"))
        menu_layout.addWidget(button)

        button = QPushButton("Quit")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"main_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("quit_game"))
        menu_layout.addWidget(button)

        self.setLayout(menu_layout)

    def start_game(self):
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Choose level")
        dialog.setFixedWidth(300)
        dialog.setStyleSheet(self.styles)
        dialog.setProperty("class", f"body_{self.theme}")
        dialog_layout = QVBoxLayout()
        dialog_layout.setSpacing(5)

        button = QPushButton("Easy")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"start_popup_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=0, dialog=dialog))
        dialog_layout.addWidget(button)

        button = QPushButton("Medium")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"start_popup_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=1, dialog=dialog))
        dialog_layout.addWidget(button)

        button = QPushButton("Hard")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"start_popup_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("start_game", level=2, dialog=dialog))
        dialog_layout.addWidget(button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()
