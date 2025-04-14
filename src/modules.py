import traceback

from PyQt5.QtCore import QTimer

from src.grid_generator import SudokuGenerator
from src.utils import get_border_style, update_stats


class Cell:
    def __init__(self, button, row, col, value, known, actual):
        self.row = row
        self.col = col
        self.found = known
        self.value = value
        self.known = known
        self.button = button
        self.conflicts = []
        self.actual_value = actual
        self.border_style = get_border_style(row, col)
        self.state = "common"
        self.update_style()
        self.id = row * 9 + col

    def update_style(self):
        # background setting:
        if self.state == "focus":
            background = "background-color: #bbdefb;"
        elif len(self.conflicts) != 0:
            background = "background-color: #f7cfd6;"
        elif self.state == "highlight":
            background = "background-color: #e2ebf3;"
        else:
            background = "background-color: #f8f8f8;"

        # color setting:
        if self.known:
            color = "color: #344861;"
        else:
            if self.value is not None:
                if self.value == self.actual_value:
                    color = "color: #325aaf;"
                else:
                    color = "color: #e55c6c"
            else:
                color = "color: #344861;"

        # Apply style to button:
        style = self.border_style + background + color
        self.button.setStyleSheet(style)

    def update_value(self, value):
        if value is None or value == 0:
            if self.found:
                # could play a buzz sound
                return True
            else:
                self.value = None
                self.button.setText("")
                return True

        if self.found:
            self.button.setText(str(self.value))
            return True

        self.value = value
        self.button.setText(str(value))

        if value == self.actual_value:
            self.found = True
            return True
        else:
            return False

    def __str__(self):
        return f"({self.row}, {self.col}) = {self.value}"

    def remove_conflict(self, cause):
        for conflict in self.conflicts:
            if conflict['cause'].id == cause.id:
                self.conflicts.remove(conflict)


class Board:
    def __init__(self, level, parent):
        self.level = level
        self.parent = parent
        self.current_row = 0
        self.current_col = 0
        self.cells = []
        self.conflicts = []
        self.previous_related_cells = []
        for i in range(9):
            self.cells.append([])
            for j in range(9):
                self.cells[i].append(None)
        self.puzzle_generator = SudokuGenerator()
        self.puzzle, self.complete = self.puzzle_generator.generate_puzzle(level)

    def add_cell(self, row, col, button):
        if self.puzzle[row][col] != 0:
            button.setText(str(self.puzzle[row][col]))
            cell = Cell(button, row, col, self.puzzle[row][col], True, self.complete[row][col])
        else:
            cell = Cell(button, row, col, None, False, self.complete[row][col])

        self.cells[row][col] = cell

    def update_cell_value(self, value):
        cell = self.cells[self.current_row][self.current_col]

        for conflict in cell.conflicts.copy():
            conflict['effect'].remove_conflict(cell)
            cell.remove_conflict(cell)
            conflict['effect'].update_style()

        if cell.update_value(value):
            cell.update_style()
            self.check_for_win()
            return True

        related_cells = self.get_related_cells(self.current_row, self.current_col)

        for c in related_cells:
            if c != cell:
                if c.value == value:
                    conflict = {
                        'cause': cell,
                        'effect': c
                    }
                    c.conflicts.append(conflict)
                    cell.conflicts.append(conflict)
                    c.update_style()
                    cell.update_style()

        cell.update_style()

        return False

    def update_cursor(self, row, col):
        self.current_row = row
        self.current_col = col

        for cell in self.previous_related_cells:
            cell.state = "common"
            cell.update_style()

        self.previous_related_cells = self.get_related_cells(row, col)

        for cell in self.get_related_cells(row, col):
            cell.state = "highlight"
            cell.update_style()

        self.cells[row][col].state = "focus"
        self.cells[row][col].update_style()

    def get_related_cells(self, row, col):
        related_cells = []
        for c in range(9):
            related_cells.append(self.cells[row][c])

        for r in range(9):
            if self.cells[r][col] not in related_cells:
                related_cells.append(self.cells[r][col])

        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if self.cells[r][c] not in related_cells:
                    related_cells.append(self.cells[r][c])

        return related_cells

    def move(self, direction):
        if direction == "up":
            if self.current_row > 0:
                self.current_row -= 1
        elif direction == "down":
            if self.current_row < 8:
                self.current_row += 1
        elif direction == "left":
            if self.current_col > 0:
                self.current_col -= 1
        elif direction == "right":
            if self.current_col < 8:
                self.current_col += 1

        self.update_cursor(self.current_row, self.current_col)

    def reset(self):
        for row in self.cells:
            for cell in row:
                if not cell.known:
                    cell.found = False
                    cell.update_value(None)
                    cell.conflicts = []
                    cell.state = "common"

    def reveal(self):
        cell = self.cells[self.current_row][self.current_col]
        self.update_cell_value(cell.actual_value)
        cell.known = True
        # self.god_test()

    def undo(self):
        print('undo pressed!')
        pass

    def pause(self):
        for row in self.cells:
            for cell in row:
                cell.button.setText("")

    def play(self):
        for row in self.cells:
            for cell in row:
                cell.update_value(cell.value)

    def check_for_win(self):
        count = 0
        flag = True
        for row in self.cells:
            for cell in row:
                if not cell.found:
                    flag = False
                    count += 1

        if flag:
            update_stats(self.level, True)
            self.parent.game_over("Win")
            self.parent.main.open_menu()

    def lost(self):
        update_stats(self.level, False)

    def god_test(self):
        self.test_timer = QTimer(self.parent)
        self.test_timer.timeout.connect(self.display)
        self.test_timer.start(20)

    def display(self):
        try:
            col = self.current_col + 1
            row = self.current_row
            if col == 9:
                col = 0
                row += 1
            if row >= 9:
                self.test_timer.timeout.disconnect()
                return True
            cell = self.cells[row][col]
            self.update_cursor(row, col)
            self.update_cell_value(cell.actual_value)
        except Exception as e:
            traceback.print_exc()
            print(e)
