########################
### TETRIS FRAMEWORK ###
########################

import numpy as np

SHAPE_TYPES = [
        [[0]],

        [[1, 1, 1],
        [0, 1, 0]],

        [[0, 2, 2],
        [2, 2, 0]],

        [[3, 3, 0],
        [0, 3, 3]],

        [[4, 0, 0],
        [4, 4, 4]],

        [[0, 0, 5],
        [5, 5, 5]],

        [[6, 6, 6, 6]],

        [[7, 7],
        [7, 7]]
        ]

class Error(Exception):
    """Base class for other exceptions"""
    pass

class CollisionError(Error):
    def __init__(self, r, c):
        self.rowidx = r
        self.colidx = c

    def __str__(self):
        return (repr(self.rowidx), repr(self.colidx))

class Block(object):
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.block = np.array(SHAPE_TYPES[shape_type], dtype = int)
        self.height, self.width = self.block.shape
        self.rotate = 0

    def __str__(self):
        string = ""
        for r in range(self.height):
            for c in range(self.width):
                string += " " + str(self.block[r][c] if self.block[r][c] else " ") 
            string += "\n"
        return string
        
    def rotate(self, num):
        self.block = np.rot90(self.block, k = num)
        self.height, self.width = self.block.shape
        self.rotate = num % 4

class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = np.zeros((height, width), dtype = int)

    def __str__(self):
        frame = "+ " + "- " * self.width + "+\n"
        string = frame
        for i, row in enumerate(self.board):
            string += "|"
            for cell in row:
                string += " " + str(cell if cell else " ")
            string += " | " + str(self.height - i) + "\n"
        string += frame
        string += " "
        for i in range(1, self.width + 1):
            string += " " + str(i)
        string += "\n"
        return string

    def __eq__(self, other):
        if self is other:
            return True
        elif type(self) != type(other):
            return False
        else:
            return self.board == other.board

    def pos(self, x=0, y=0):
        return self.height - y, x - 1

    def cell(self, r, c):
        return self.board[r][c]

    def copy(self, otherBoard):
        self.board = otherBoard.board.copy()

    def addShape(self, block, x, y):
        pos_r, pos_c = self.pos(x, y)
        frame = self.board[pos_r - block.height + 1 : pos_r + 1, pos_c : pos_c + block.width]
        self.board[pos_r - block.height + 1 : pos_r + 1, pos_c : pos_c + block.width] = np.where(frame == 0, block.block, frame)

