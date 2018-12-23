from game import *

b = Board(5, 10)
s = Shape(1)
b.addShape(s, 1 ,1)
print(b)
b = Board(5, 10)
b.addShape(s, 0, 1)
b = Board(5, 10)
b.addShape(s, 1, 0)
print(b)
print(b)

