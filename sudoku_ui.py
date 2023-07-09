import tkinter
from tkinter import *
from tkinter import ttk
import sudoku_board

WINDOW_WIDTH = 340
WINDOW_HEIGHT = 600
ROWS_AND_COLS = 3
TITLE = "Suduko"
CELL_FONT=('Helvetica', 30, 'bold')
LABEL_FONT=('Helvetica', 15, 'bold')
CELLS_BORDER_COLOR = "blue"
CELL_BORDER_COLOR = "black"
LABEL_FONT_COLOR = "blue"
LABEL_FONT_WIN_COLOR = "light green"
CHECK_BUTTON_TEXT = "Check Solution"
HINT_BUTTON_TEXT = "Get a Hint"
CELL_BORDER_WIDTH = 3
CELLS_BORDER_WIDTH = 5
SOLVED_MSG = "You solved it!!! "

class SudokuUI:
    def __init__(self, board):
        self.mistakes = 0
        self.hints = 0
        self.board = board
        '''Main Window'''
        self.main_win = tkinter.Tk()
        self.main_win.title(TITLE)
        '''Upper frame'''
        self.upper_frame = Frame(self.main_win)
        self.label = Label(self.upper_frame)
        self.label.grid(row=0,column=0, columnspan=10)
        self.check_button = Button(self.upper_frame, text = CHECK_BUTTON_TEXT, command=self.check_solution)
        self.check_button.grid(row=2,column=3)
        self.check_button = Button(self.upper_frame, text = HINT_BUTTON_TEXT, command=self.get_hint)
        self.check_button.grid(row=2,column=4)
        self.upper_frame.grid(row=0, column=1)
        '''Main Frame '''
        self.main_frame = Frame(self.main_win)
        self.main_frame.grid(row=1, column=1)
        self.frames = []
        self.cells = []
        for i in range(ROWS_AND_COLS):
            frame_col = []
            for j in range(ROWS_AND_COLS):
                frame = Frame(self.main_frame, bg=CELLS_BORDER_COLOR, bd=CELLS_BORDER_WIDTH)
                frame_col.append(frame)
                frame.grid(row = i, column = j)
                vcmd = (frame.register(self.validate_input), '%P')
                for k in range(ROWS_AND_COLS):
                    cell_col = []
                    for l in range(ROWS_AND_COLS):
                        entry = Entry(frame, width=1, font=CELL_FONT, bd=CELL_BORDER_WIDTH, validate='key',validatecommand=(vcmd))
                        cell_col.append(entry)
                        entry.grid(row = k, column = l)
                    self.cells.append(cell_col)
            self.frames.append(frame_col)
            
    def run(self):
        self.main_win.mainloop()
        
    def validate_input(self, p):
        if len(p) == 0 or (len(p) == 1 and p.isdigit()):
            return True
        else:
            return False
    

    def display_nums(self, board):
        bump = 0
        for row in range (sudoku_board.MAX_NUM):
            if row % 3 == 0 and row != 0:
                bump = bump+6
            for col in range (sudoku_board.MAX_NUM):
                if board.cells[row*sudoku_board.MAX_NUM+col].visible:
                    self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].insert(0, board.cells[row*sudoku_board.MAX_NUM+col].num)
                    self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].config(state= "disabled")
                    board.cells[row*sudoku_board.MAX_NUM+col].solved = True

    def display_moves_to_win(self, board):
        msg = ""
        fg_color = None
        if len(board.unsolved_list) == 0:
            msg = SOLVED_MSG
            fg_color = LABEL_FONT_WIN_COLOR
        else:
            msg = "You have "+str(len(board.unsolved_list)) + " to go with "
            fg_color = LABEL_FONT_COLOR
            
        self.label.config(text = msg +str(self.mistakes)+" mistakes and "+str(self.hints)+" hints", font = LABEL_FONT, fg=fg_color)
        
    def check_solution(self):
        bump = 0
        for row in range (sudoku_board.MAX_NUM):
            if row % 3 == 0 and row != 0:
                bump = bump+6
            for col in range (sudoku_board.MAX_NUM):
                ui_cell = self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].get().strip()
                if ui_cell != '' and ui_cell== str(self.board.cells[row*sudoku_board.MAX_NUM+col].num):
                    self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].config(bg="green")
                    self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].config(state= "disabled")
                    self.board.cells[row*sudoku_board.MAX_NUM+col].solved = True
                elif ui_cell != '' and ui_cell != str(self.board.cells[row*sudoku_board.MAX_NUM+col].num):
                    self.cells[row+bump+int(col/3)*ROWS_AND_COLS][col%ROWS_AND_COLS].config(bg="red")
                    self.board.cells[row*sudoku_board.MAX_NUM+col].solved = False
                    self.mistakes = self.mistakes + 1
        self.board.clear_unresolved_list()
        self.board.update_unresolved_list()
        self.display_moves_to_win(self.board)
    
    def get_hint(self):
        self.hints = self.hints + 1
        self.board.set_visible_cells(1)
        self.board.clear_unresolved_list()
        self.board.update_unresolved_list()
        self.display_nums(self.board)
        self.display_moves_to_win(self.board)        