import random
from copy import deepcopy


class SudokuGenerator:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):
        # Check row
        if num in self.board[row]:
            return False

        # Check column
        if num in [self.board[r][col] for r in range(9)]:
            return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == num:
                    return False

        return True

    def solve(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def generate_full_board(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        # for _ in range(20):  # Randomly fill some cells initially to help with generation
        #     row, col = random.randint(0, 8), random.randint(0, 8)
        #     num = random.randint(1, 9)
        #     while not self.is_safe(row, col, num):
        #         row, col = random.randint(0, 8), random.randint(0, 8)
        #         num = random.randint(1, 9)
        #     self.board[row][col] = num

        if not self.solve():
            raise ValueError("Failed to solve board.")

    def remove_numbers(self, difficulty):
        # Number of cells to remove based on difficulty
        cells_to_remove = [35, 45, 55]

        count = cells_to_remove[difficulty]
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            self.board[row][col] = 0
            count -= 1

    def generate_puzzle(self, difficulty):
        attempts = 10
        try:
            while attempts >= 0:
                self.generate_full_board()
                complete = deepcopy(self.board)
                self.remove_numbers(difficulty)
                return [self.board, complete]
        except Exception as e:
            print(str(e))
            print(f"Generation failed, retrying... ({attempts} attempts left)")
            attempts -= 1

        raise RuntimeError("Failed to generate a valid Sudoku puzzle after multiple attempts.")


if __name__ == "__main__":
    sg = SudokuGenerator()
    print(sg.generate_puzzle("easy"))
