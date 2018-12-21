########################
### TETRIS FRAMEWORK ###
########################

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

class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0 for x in range(width)] for y in range(height)]

    def __str__(self):
        frame = "+ " + "- " * self.width + "+\n"
        string += frame
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

    def copy(self, board):
        for ridx, row in enumerate(self.board):
            for cidx, cell in enumerate(row):
                self.board[ridx][cidx] = board.cell(ridx, cidx)

