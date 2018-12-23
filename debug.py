from game import *

b = Board(5, 10)
s = Block(1)
b.addBlock(s, 1 ,1)
print(b)
b.removeRow(9)
print(b)
b = Board(5, 10)
b.addBlock(s, 0, 1)
b = Board(5, 10)
b.addBlock(s, 1, 0)
print(b)
print(b)

