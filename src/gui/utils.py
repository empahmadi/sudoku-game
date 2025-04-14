from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFrame


def create_round_button(action, callback, styles, theme):
    button = QPushButton()
    button.setFixedSize(100, 100)
    button.setStyleSheet(styles)
    button.setProperty("class", f"round_button_{theme}")
    button.setCursor(Qt.PointingHandCursor)

    button.setIcon(QIcon(f'assets/img/{action}.png'))
    button.setIconSize(QSize(100, 100))
    button.clicked.connect(lambda: callback(action))
    return button


class StatusBar(QHBoxLayout):
    def __init__(self):
        super().__init__()

        # Date Label
        self.date_label = QLabel(QDate.currentDate().toString("MMM dd"))
        self.date_label.setFont(QFont("Arial", 12))
        self.date_label.setAlignment(Qt.AlignRight)

        # Mistakes Label
        self.mistakes_label = QLabel("Mistakes: 0/3")
        self.mistakes_label.setFont(QFont("Arial", 12))
        self.mistakes_label.setAlignment(Qt.AlignCenter)

        # Timer Label
        self.timer_label = QLabel("Time: 00:00")
        self.timer_label.setFont(QFont("Arial", 12))
        self.timer_label.setAlignment(Qt.AlignLeft)

        # Add Widgets to Layout
        self.addWidget(self.date_label)
        self.addStretch()
        self.addWidget(self.mistakes_label)
        self.addStretch()
        self.addWidget(self.timer_label)

        # Timer
        self.is_paused = True
        self.elapsed_time = 0  # Time in seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self):
        """Start the game timer."""
        if self.is_paused:
            self.timer.start(1000)
            self.is_paused = False

    def pause_timer(self):
        if not self.is_paused:
            self.timer.stop()
            self.is_paused = True

    def update_timer(self):
        """Update the timer label every second."""
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")

    def update_mistakes(self, number):
        self.mistakes_label.setText(f"Mistakes: {number}/3")


class ActionBar(QVBoxLayout):
    def __init__(self, update_cell_callback, styles, theme):
        super().__init__()
        # Callback to update the cell when a number is selected
        self.update_cell_callback = update_cell_callback

        # Define Top Spacer
        top_spacer = QFrame()
        top_spacer.setFixedHeight(50)

        # Top Bar with Buttons
        top_bar = QHBoxLayout()

        undo_button = create_round_button('undo', self.update_cell_callback, styles, theme)
        erase_button = create_round_button('eraser', self.update_cell_callback, styles, theme)
        hint_button = create_round_button('hint', self.update_cell_callback, styles, theme)
        self.play_button = create_round_button('pause', self.update_cell_callback, styles, theme)

        top_bar.addWidget(undo_button)
        top_bar.addWidget(erase_button)
        top_bar.addWidget(hint_button)
        top_bar.addWidget(self.play_button)

        # Bottom Bar with Number Buttons
        bottom_bar = QGridLayout()
        bottom_bar.setSpacing(5)
        number = 1
        for row in range(1, 4):
            for col in range(1, 4):
                button = QPushButton(str(number))
                button.setFixedSize(160, 120)
                button.setStyleSheet(styles)
                button.setProperty("class", f"number_pad_{theme}")
                button.setCursor(Qt.PointingHandCursor)
                button.clicked.connect(lambda _, n=number: self.number_selected(n))
                bottom_bar.addWidget(button, row, col)
                number += 1

        # New Game Button:
        new_game_button = QPushButton("Main Menu")
        new_game_button.setFixedSize(495, 120)
        new_game_button.setStyleSheet(styles)
        new_game_button.setProperty("class", f"number_pad_{theme}")
        new_game_button.setCursor(Qt.PointingHandCursor)
        new_game_button.clicked.connect(lambda: self.update_cell_callback('new_game'))
        bottom_bar.addWidget(new_game_button, 4, 1, 1, 3)

        # Add Bars to Layout
        self.addWidget(top_spacer)
        self.addLayout(top_bar)
        self.addLayout(bottom_bar)

    def number_selected(self, number):
        if self.update_cell_callback:
            self.update_cell_callback('number', number)

    def play_or_pause(self, status):
        self.play_button.clicked.disconnect()
        if status:
            self.play_button.setIcon(QIcon(f'assets/img/play.png'))
            self.play_button.setIconSize(QSize(100, 100))
            self.play_button.clicked.connect(lambda: self.update_cell_callback("play"))
        else:
            self.play_button.setIcon(QIcon(f'assets/img/pause.png'))
            self.play_button.setIconSize(QSize(100, 100))
            self.play_button.clicked.connect(lambda: self.update_cell_callback("pause"))
