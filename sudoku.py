from sudoku_ui import SudokuUI
from sudoku_board import SudokuBoard

NUM_OF_VISIBLE_CELLS = 25

class Sudoku:
    def __init__(self):
        self.board = SudokuBoard()
        self.ui = SudokuUI(self.board)

        
        
    def run(self):
        self.board.populate_nums()
        self.board.set_visible_cells(NUM_OF_VISIBLE_CELLS)
        self.board.update_unresolved_list()
        self.ui.display_nums(self.board)
        self.ui.display_moves_to_win(self.board)
        self.ui.run()