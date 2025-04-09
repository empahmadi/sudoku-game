from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QDialog, QVBoxLayout, QPushButton, QWidget

from src.gui.board import BoardUI
from src.gui.menu import Menu


class SudokuApp(QMainWindow):
    def __init__(self, styles, theme):
        super().__init__()
        self.styles = styles
        self.theme = theme
        self.setWindowTitle("Sudoku Game")
        self.setMinimumSize(1300, 800)
        self.setStyleSheet(self.styles)
        self.setProperty("class", f"body_{self.theme}")
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        self.content = None
        self.open_menu()

    def event_handler(self, event, **kwargs):
        if event == 'start_game':
            self.event_handler('done', dialog=kwargs.get('dialog'))
            self.open_board(kwargs.get('level'))
        elif event == 'open_settings':
            self.open_settings()
        elif event == 'done':
            kwargs.get('dialog').accept()
        elif event == 'quit_game':
            self.close()

    def open_menu(self):
        self.change_screen(Menu(self, self.event_handler, self.styles, self.theme))

    def open_board(self, level):
        self.change_screen(BoardUI(level, self))

    def open_settings(self):
        # todo: implement settings UI
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog_layout = QVBoxLayout()

        button = QPushButton("Under Construction !")
        button.setFont(QFont("Arial", 12))
        button.clicked.connect(lambda: self.event_handler('done', dialog=dialog))

        dialog_layout.addWidget(button)
        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def change_screen(self, screen):
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addStretch()

        central_layout.addWidget(screen, alignment=Qt.AlignCenter)
        central_layout.addStretch()

        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def resume_game(self):
        pass
