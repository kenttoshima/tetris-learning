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

class Shape(object):
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.shape = np.array(SHAPE_TYPES[shape_type])
        self.shape_height, self.shape_width = self.shape.shape
        self.rotate = 0

    def __str__(self):
        string = ""
        for r in range(self.shape_height):
            for c in range(self.shape_width):
                string += " " + str(self.shape[r][c] if self.shape[r][c] else " ") 
            string += "\n"
        return string
        
    def rotate(self, num):
        self.shape = np.rot90(self.shape, k = num)
        self.shape_height, self.shape_width = self.shape.shape
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
            string += str(i) + " "
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

    def addShape(self, shape, x, y):
        pos_r, pos_c = self.pos(x, y)
        frame = self.board[pos_r-shape.shape_height+1:pos_r+1, pos_c:pos_c+shape.shape_width]
        print(frame.shape)
        print(shape.shape.shape)
        self.board[pos_r-shape.shape_height+1:pos_r+1, pos_c:pos_c+shape.shape_width] = np.where(frame == 0, shape.shape, frame)
        print(np.where(frame == 0, shape.shape, frame))

