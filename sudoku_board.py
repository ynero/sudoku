import random
MAX_NUM = 9

class SudokuCell:
    def __init__(self, row, col):
       self.row = row
       self.col = col
       self.num = 0
       self.visible = False
       self.solved = False
    
class SudokuBoard:
    def __init__(self):
        self.cells = []
        self.free_list = []
        self.unsolved_list = []
        for row in range (MAX_NUM):
            for col in range (MAX_NUM):
                self.cells.append(SudokuCell(row, col))
                self.free_list.append(SudokuCell(row, col))
       

    def set_visible_cells(self, num):
        i = 0
        while i < num:
            pos = random.randint(0,len(self.cells)-1)
            if self.cells[pos].visible == False:
                self.cells[pos].visible = True
                self.cells[pos].solved = True
                i = i + 1
            
    def populate_nums(self):
        num = 1
        while num <= MAX_NUM:
            i = 0
            retry = 0 
            while i < MAX_NUM:
                if len(self.free_list) <= 0 and retry <=3:
                    self.undo_number(num)
                    self.update_free_list()
                    i = 0
                    retry = retry + 1
                    continue
                elif retry > 3:
                    self.reset_board()
                    self.update_free_list()
                    num = 0
                    break;
                pos = random.randint(0,len(self.free_list)-1)
                row =  self.free_list[pos].row
                col =  self.free_list[pos].col
                self.remove_from_free_list(num, row, col, pos)
                self.cells[row*MAX_NUM+col].num = num
                i = i + 1
            num = num + 1
        self.print_board()
   
    def print_board(self):
        for i in range(len(self.cells)):
            if i%9 == 0 and i != 0:
                print()
            print(self.cells[i].num, end=' ')
        print()
        print()

    def reset_board(self):
        for i in range(len(self.cells)):
            self.cells[i].num = 0
                
    def undo_number(self, num):
        for i in range(len(self.cells)):
            if self.cells[i].num == num:
                self.cells[i].num = 0

    def update_free_list(self):       
        for i in range(len(self.cells)):
            if self.cells[i].num == 0:
                self.free_list.append(self.cells[i]) 
                
    def remove_from_free_list(self, num, row, col, pos):
        i=0
        self.free_list.remove(self.free_list[pos])
        q = 3*int(row/3)+int(col/3)
        while i < len(self.free_list):
            if (self.free_list[i].row == row or self.free_list[i].col == col) and not (self.free_list[i].row == row and self.free_list[i].col == col) or (q == 3*int(self.free_list[i].row/3)+int(self.free_list[i].col/3)):
                self.free_list.remove(self.free_list[i])
            else:
                i=i+1
    
    def update_unresolved_list(self):       
        for i in range(len(self.cells)):
            if self.cells[i].solved == False:
                self.unsolved_list.append(self.cells[i])
                
    def clear_unresolved_list(self):       
        self.unsolved_list.clear()