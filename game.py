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

class BoardError(Error):
    def __init__(self, arg):
        self.arg = arg
        if isinstance(self.arg, np.ndarray):
            self.string = "Collides at "
            self.arg = list(map(tuple, self.arg))
        else:
            self.string = "Out of frame when placing at "
            self.arg = list(self.arg)

    def __str__(self):
        return self.string + ', '.join(str(p) for p in self.arg)

class Block(object):
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.block = np.array(SHAPE_TYPES[shape_type], dtype = int)
        self.height, self.width = self.block.shape
        self.rotation = 0

    def __str__(self):
        string = ""
        for r in range(self.height):
            for c in range(self.width):
                string += " " + str(self.block[r][c] if self.block[r][c] else " ")
            string += "\n"
        return string

    def rotate(self, num=1):
        self.block = np.rot90(self.block, k = num)
        self.height, self.width = self.block.shape
        self.rotation = (self.rotation + num) % 4

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

    def xytorc(self, x=1, y=1):
        return self.height - y, x - 1

    def rctoxy(self, r=0, c=0):
        return c + 1, self.height - r

    def cell(self, r, c):
        return self.board[r][c]

    # copy given board to self
    def copy(self, copyBoard):
        self.board = copyBoard.board.copy()

    def intersection(self, block, x, y):
        pos_r, pos_c = self.xytorc(x, y)
        return slice(pos_r - block.height + 1, pos_r + 1), slice(pos_c, pos_c + block.width)

    def hasCollisionAt(self, block, x, y):
        frame = self.board[self.intersection(block, x, y)]
        board_collision = (frame != 0)
        block_collision = (block.block != 0)
        pos_r, pos_c = self.xytorc(x, y)
        local_idx_r, local_idx_c = np.where(np.logical_and(board_collision, block_collision))
        collisionLocations = np.dstack(self.rctoxy(pos_r - (block.height - local_idx_r - 1), local_idx_c + pos_c))[0]
        return collisionLocations if collisionLocations.size != 0 else None

    def canFall(self, block, x, y):
        frame = self.board[self.intersection(block, x, y)]
        print(np.where(frame == 0, block.block, frame))

    # add given block object to (x, y) on the board
    def addBlock(self, block, x, y):
        xmin, xmax = 1, self.width - block.width + 1
        ymin, ymax = 1, self.height - block.height + 1
        if x < xmin or xmax < x or y < ymin or ymax < y:
            raise BoardError((x, y))
        frame = self.board[self.intersection(block, x, y)]
        collisionLocations = self.hasCollisionAt(block, x, y)
        pos_r, pos_c = self.xytorc(x, y)
        if collisionLocations is None:
            self.board[self.intersection(block, x, y)] = np.where(frame == 0, block.block, frame)
        else:
            raise BoardError(collisionLocations)

    # remove filled rows and return the number of removed rows
    def removeFilledRow(self):
        filledRowIdx = np.where(np.all(self.board != 0, axis=1))[0]
        self.board = np.delete(self.board, filledRowIdx, axis=0)
        numRemovedRow = filledRowIdx.size
        adding_row = np.zeros((numRemovedRow, self.width), dtype = int)
        self.board = np.vstack((adding_row, self.board))
        return numRemovedRow

class Config(Board):
    def __init__(self, width, height):
        super(Config, self).__init__(width, height)

    def place(self, x):
        pass
