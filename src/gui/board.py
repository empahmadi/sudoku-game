from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QDialog, QLabel

from gui.utils import StatusBar, ActionBar
from src.modules import Board


class BoardUI(QWidget):
    def __init__(self, level, main, event_handler, styles, theme):
        super().__init__()
        self.main = main
        self.event_handler = event_handler
        self.styles = styles
        self.theme = theme
        self.board = Board(level, self)
        self.status_bar = StatusBar()
        self.action_bar = ActionBar(self.action_bar_controller, styles, theme)
        self.mistakes = 0
        self.play = True
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(1215, 720)
        self.setStyleSheet("background-color: #ffffff;")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        for row in range(9):
            for col in range(9):
                button = QPushButton("")
                button.setFont(QFont("Arial", 24))
                button.setFixedSize(80, 80)
                button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                button.setFocusPolicy(Qt.NoFocus)
                grid_layout.addWidget(button, row, col)
                self.board.add_cell(row, col, button)

        self.setFocusPolicy(Qt.StrongFocus)

        board_layout = QHBoxLayout()
        board_layout.addLayout(grid_layout)
        controller_layout = QVBoxLayout()
        controller_layout.addLayout(self.status_bar)
        controller_layout.addLayout(self.action_bar)
        board_layout.addLayout(controller_layout)

        self.setLayout(board_layout)
        self.status_bar.start_timer()

        self.board.update_cursor(0, 0)

    def cell_clicked(self, row, col):
        self.board.update_cursor(row, col)

    def select_number(self, number):
        if number is None:
            status = self.board.update_cell_value(None)
        elif number == 0:
            status = self.board.update_cell_value(None)
        else:
            status = self.board.update_cell_value(number)

        if not status:
            self.mistake_increment()

    def keyPressEvent(self, event):
        # Handle arrow key navigation
        if event.key() == Qt.Key_Up:
            self.board.move("up")
        elif event.key() == Qt.Key_Down:
            self.board.move("down")
        elif event.key() == Qt.Key_Left:
            self.board.move("left")
        elif event.key() == Qt.Key_Right:
            self.board.move("right")
        elif Qt.Key_1 <= event.key() <= Qt.Key_9:
            self.select_number(event.key() - Qt.Key_0)
        elif event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.select_number(None)

    def mistake_increment(self):
        self.mistakes += 1
        self.status_bar.update_mistakes(self.mistakes)
        if self.mistakes == 3:
            self.board.lost()
            self.game_over("Lost")
            self.main.open_menu()

    def action_bar_controller(self, button, number=None):
        if button == 'number':
            self.select_number(number)
        elif button == 'undo':
            self.board.undo()
        elif button == 'hint':
            self.board.reveal()
        elif button == 'erase':
            self.select_number(None)
        elif button == 'new_game':
            self.main.open_menu()
        elif button == 'pause':
            self.board.pause()
            self.action_bar.play_or_pause(True)
            self.status_bar.pause_timer()
        elif button == 'play':
            self.board.play()
            self.action_bar.play_or_pause(False)
            self.status_bar.start_timer()

    def game_over(self, status):
        dialog = QDialog(self.main)
        dialog.setWindowTitle("Game Over!")
        dialog.setFixedWidth(300)
        dialog.setStyleSheet(self.styles)
        dialog.setProperty("class", f"body_{self.theme}")
        dialog_layout = QVBoxLayout()
        dialog_layout.setSpacing(20)

        status_label = QLabel(f"You {status}!")
        status_label.setFont(QFont("Arial", 24))
        status_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(status_label)

        button = QPushButton("New Game")
        button.setStyleSheet(self.styles)
        button.setProperty("class", f"start_popup_button_{self.theme}")
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(lambda: self.event_handler("new_game", level=0, dialog=dialog))
        dialog_layout.addWidget(button)

        dialog.setLayout(dialog_layout)
        dialog.exec_()
