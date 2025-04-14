import sys

from PyQt5.QtWidgets import QApplication

from src.gui.app import SudokuApp

if __name__ == '__main__':
    with open("src/styles/styles.css", "r") as f:
        styles = f.read()
    app = QApplication(sys.argv)
    window = SudokuApp(styles, "light")
    window.show()
    sys.exit(app.exec_())
